"""Deterministic workload generator for RFC-007 scaling experiments.

Creates Organization State fixtures with N fields across D domains and M tasks,
where each task references a subset of fields by key. Ground truth is derived
from the generated values so results remain self-consistent at any scale.

Usage:
    python benchmark/selective-context/generate_workload.py \
        --fields 1000 --domains 10 --tasks 500 --seed 42 \
        --out workloads/w1000.json
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

DOMAINS = [
    "control", "safety", "finance", "hr", "logistics",
    "energy", "quality", "maintenance", "compliance", "procurement",
]

OPS = ["range", "bool"]


def _gen_value(rng: random.Random, domain: str) -> tuple[object, object]:
    """Return (value, expected_for_bool)."""
    if domain in ("finance", "hr", "procurement"):
        return rng.randint(-100, 10000), True
    if domain in ("logistics", "energy"):
        return round(rng.uniform(0.0, 500.0), 1), True
    # control / safety / quality / maintenance / compliance
    return round(rng.uniform(0.0, 100.0), 1), True


def generate(org_id: str, n_fields: int, n_domains: int, n_tasks: int,
             seed: int, min_req: int = 1, max_req: int = 5) -> dict:
    rng = random.Random(seed)
    domains = DOMAINS[:n_domains]

    fields = []
    for i in range(n_fields):
        domain = domains[i % len(domains)]
        value, _ = _gen_value(rng, domain)
        key = f"f_{i:05d}"
        fields.append({
            "key": key,
            "value": value,
            "relevance": [key, domain],
            "authority": "admin",
        })

    tasks = []
    for i in range(n_tasks):
        n_req = rng.randint(min_req, max_req)
        req_keys = rng.sample([f["key"] for f in fields], k=n_req)
        key = req_keys[0]
        field = next(f for f in fields if f["key"] == key)
        op = rng.choice(OPS)
        if op == "range":
            lo = max(0.0, field["value"] - 10)
            hi = field["value"] + 10
            expected = lo <= field["value"] <= hi
            args = [key, lo, hi]
            prompt = f"Is field {key} within range [{lo}, {hi}]?"
        else:
            expected = field["value"] != -99999  # always True by construction
            args = [key]
            prompt = f"Is field {key} a valid (non-missing) value?"
        tasks.append({
            "id": f"T{i:05d}",
            "prompt": prompt,
            "required": req_keys,
            "expected": expected,
            "op": op,
            "args": args,
        })

    return {
        "name": f"{org_id}-scaled",
        "org_id": org_id,
        "seed": seed,
        "quality_tolerance": 0.10,
        "cost_ratio_threshold": 2.0,
        "state_fields": fields,
        "tasks": tasks,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--org-id", default="scale-org")
    ap.add_argument("--fields", type=int, default=1000)
    ap.add_argument("--domains", type=int, default=10)
    ap.add_argument("--tasks", type=int, default=500)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--min-req", type=int, default=1)
    ap.add_argument("--max-req", type=int, default=5)
    ap.add_argument("--out", default="workloads/w1000.json")
    args = ap.parse_args()

    wl = generate(
        org_id=args.org_id,
        n_fields=args.fields,
        n_domains=args.domains,
        n_tasks=args.tasks,
        seed=args.seed,
        min_req=args.min_req,
        max_req=args.max_req,
    )
    out = Path(__file__).resolve().parent / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(wl, indent=2), encoding="utf-8")
    print(json.dumps({
        "workload": wl["name"],
        "fields": len(wl["state_fields"]),
        "tasks": len(wl["tasks"]),
        "out": str(out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
