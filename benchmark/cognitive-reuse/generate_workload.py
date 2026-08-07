"""Deterministic generator for the RFC-008 cognitive-reuse workload.

Produces an ordered operation stream over an Organization State with a
State-change schedule. The workload is self-consistent: each operation's
expected answer is computed from the State value valid at that position in the
stream, so ground truth reflects State changes (used to validate H3).

Usage:
    python benchmark/cognitive-reuse/generate_workload.py \
        --fields 50 --tasks-per-field 4 --drift-fraction 0.5 --out workloads/reuse.json
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


def _build_org(org_id: str, n_fields: int, seed: int) -> tuple[dict, dict]:
    rng = random.Random(seed)
    fields = {}
    entries = []
    for i in range(n_fields):
        key = f"f_{i:05d}"
        value = rng.randint(0, 100)
        fields[key] = value
        entries.append({
            "key": key,
            "value": value,
            "relevance": [key, "generic"],
            "authority": "admin",
        })
    return fields, entries


def _op_for(key: str, value: int, rng: random.Random) -> dict:
    lo = max(0, value - 10)
    hi = value + 10
    if rng.random() < 0.5:
        lo = value + 1  # expected False (value < lo)
        return {"op": "range", "args": [key, lo, hi], "expected": False}
    return {"op": "range", "args": [key, lo, hi], "expected": True}


def generate(n_fields: int, tasks_per_field: int, drift_fraction: float,
             seed: int) -> dict:
    rng = random.Random(seed)
    fields, entries = _build_org("reuse-org", n_fields, seed)
    keys = list(fields.keys())

    tasks = []
    transitions = []
    next_idx = 0
    for key in keys:
        base = fields[key]
        # first operation on this field
        op = _op_for(key, base, rng)
        task = {
            "id": f"op_{key}_0",
            "prompt": f"Is field {key} within range {op['args'][1]}..{op['args'][2]}?",
            "required": [key],
            "expected": op["expected"],
            "op": op["op"],
            "args": op["args"],
        }
        tasks.append(task)
        next_idx += 1

        # repeated equivalent operations (same signature)
        for r in range(1, tasks_per_field):
            task = {
                "id": f"op_{key}_{r}",
                "prompt": f"Is field {key} within range {op['args'][1]}..{op['args'][2]}?",
                "required": [key],
                "expected": op["expected"],
                "op": op["op"],
                "args": op["args"],
            }
            tasks.append(task)
            next_idx += 1

        # optional State change to exercise invalidation (H3)
        if rng.random() < drift_fraction:
            new_value = rng.randint(0, 100)
            transitions.append({
                "apply_after_op_index": next_idx - 1,
                "key": key,
                "value": new_value,
            })
            # one more operation AFTER the change, same question (same
            # signature) but expected answer recomputed against new State
            fields[key] = new_value
            lo, hi = op["args"][1], op["args"][2]
            expected_after = lo <= new_value <= hi
            task = {
                "id": f"op_{key}_after_drift",
                "prompt": f"Is field {key} within range {lo}..{hi}?",
                "required": [key],
                "expected": expected_after,
                "op": op["op"],
                "args": op["args"],
            }
            tasks.append(task)
            next_idx += 1

    return {
        "name": "reuse-bench",
        "org_id": "reuse-org",
        "seed": seed,
        "quality_tolerance": 0.10,
        "cost_ratio_threshold": 2.0,
        "state_fields": entries,
        "tasks": tasks,
        "transitions": transitions,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fields", type=int, default=50)
    ap.add_argument("--tasks-per-field", type=int, default=4)
    ap.add_argument("--drift-fraction", type=float, default=0.5)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="workloads/reuse.json")
    args = ap.parse_args()

    wl = generate(args.fields, args.tasks_per_field, args.drift_fraction, args.seed)
    out = Path(__file__).resolve().parent / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(wl, indent=2), encoding="utf-8")
    print(json.dumps({
        "workload": wl["name"],
        "fields": len(wl["state_fields"]),
        "tasks": len(wl["tasks"]),
        "transitions": len(wl["transitions"]),
        "out": str(out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
