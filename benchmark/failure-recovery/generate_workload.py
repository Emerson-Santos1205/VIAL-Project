"""Deterministic generator for the RFC-009 failure-recovery workload.

Produces an ordered operation stream (State transitions) plus a deterministic
failure schedule. Failure points select WHERE an executor 'fails':
- before_commit: intent recorded, then interrupted (no commit)
- after_commit: intent committed, then interrupted (ack lost)
- clean: no interruption

Usage:
    python benchmark/failure-recovery/generate_workload.py \
        --fields 20 --operations 60 --fail-fraction 0.4 --out workloads/failure.json
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

FAIL_POINTS = ["clean", "before_commit", "after_commit"]


def generate(n_fields: int, n_operations: int, fail_fraction: float,
             seed: int) -> dict:
    rng = random.Random(seed)

    fields = []
    for i in range(n_fields):
        key = f"f_{i:05d}"
        fields.append({
            "key": key,
            "value": rng.randint(0, 100),
            "relevance": [key, "generic"],
            "authority": "admin",
        })

    operations = []
    for i in range(n_operations):
        key = f"f_{rng.randrange(n_fields):05d}"
        new_value = rng.randint(0, 100)
        roll = rng.random()
        if roll < fail_fraction:
            point = rng.choice(FAIL_POINTS[1:])
        else:
            point = "clean"
        operations.append({
            "id": f"op_{i:04d}",
            "key": key,
            "value": new_value,
            "fail_point": point,
        })

    return {
        "name": "failure-recovery-bench",
        "org_id": "failure-org",
        "seed": seed,
        "state_fields": fields,
        "operations": operations,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fields", type=int, default=20)
    ap.add_argument("--operations", type=int, default=60)
    ap.add_argument("--fail-fraction", type=float, default=0.4)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="workloads/failure.json")
    args = ap.parse_args()

    wl = generate(args.fields, args.operations, args.fail_fraction, args.seed)
    out = Path(__file__).resolve().parent / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(wl, indent=2), encoding="utf-8")
    n_fail = sum(1 for o in wl["operations"] if o["fail_point"] != "clean")
    print(json.dumps({
        "workload": wl["name"],
        "fields": len(wl["state_fields"]),
        "operations": len(wl["operations"]),
        "failures": n_fail,
        "out": str(out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
