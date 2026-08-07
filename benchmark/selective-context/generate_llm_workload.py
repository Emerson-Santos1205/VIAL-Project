"""Deterministic generator for a reasoning (non-deterministic) workload.

Unlike the numeric workload, tasks require reading a text entry and answering
a factual True/False question. Full Context contains all entries (including
irrelevant noise); Selective Context projects only entries whose relevance tag
matches the task.

This workload is designed for the real LLM executor: it tests whether
contextual noise degrades reasoning quality and whether selective projection
preserves parity at lower cost.

Usage:
    python benchmark/selective-context/generate_llm_workload.py \
        --entries 200 --tasks 100 --out workloads/reasoning.json
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

FACT_TEMPLATES = [
    "Line {n} monthly output target is {v} units.",
    "Sensor {n} alarm threshold is {v}.",
    "Vendor {n} quarterly budget is {v}.",
    "Pump {n} rated flow is {v} liters per hour.",
    "Batch {n} temperature target is {v} degrees.",
    "Server {n} power limit is {v} watts.",
]

NOUNS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]


def _entry(rng: random.Random, i: int, tag: str) -> dict:
    tpl = rng.choice(FACT_TEMPLATES)
    noun = NOUNS[i % len(NOUNS)]
    value = rng.randint(50, 5000)
    text = tpl.format(n=noun, v=value)
    return {"key": f"k_{i:05d}", "value": text, "relevance": [tag]}


def generate(n_entries: int, n_tasks: int, seed: int) -> dict:
    rng = random.Random(seed)
    n_tags = max(4, n_entries // 10)
    tags = [f"domain_{t}" for t in range(n_tags)]

    entries = []
    for i in range(n_entries):
        tag = tags[i % len(tags)]
        entries.append(_entry(rng, i, tag))

    tasks = []
    for i in range(n_tasks):
        # pick one entry whose value contains a number we can ask about
        idx = rng.randrange(len(entries))
        e = entries[idx]
        numbers = [int(w) for w in e["value"].split() if w.lstrip("-").isdigit()]
        if not numbers:
            numbers = [100]
        base = numbers[-1]
        # ask whether the value meets a bound; ~half true, half false
        if rng.random() < 0.5:
            bound = max(0, base - rng.randint(1, 50))
            expected = True
        else:
            bound = base + rng.randint(1, 50)
            expected = False
        tasks.append({
            "id": f"R{i:05d}",
            "prompt": (f"Based on the organizational facts provided, answer whether the "
                       f"statement is true: 'The value referenced in entry {e['key']} "
                       f"meets or exceeds the bound {bound}.'"),
            "required": e["relevance"],
            "expected": expected,
            "op": "llm_bool",
        })

    return {
        "name": "reasoning-bench",
        "org_id": "reason-org",
        "seed": seed,
        "quality_tolerance": 0.10,
        "cost_ratio_threshold": 2.0,
        "state_fields": entries,
        "tasks": tasks,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--entries", type=int, default=200)
    ap.add_argument("--tasks", type=int, default=100)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="workloads/reasoning.json")
    args = ap.parse_args()

    wl = generate(n_entries=args.entries, n_tasks=args.tasks, seed=args.seed)
    out = Path(__file__).resolve().parent / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(wl, indent=2), encoding="utf-8")
    print(json.dumps({"workload": wl["name"], "entries": len(wl["state_fields"]),
                      "tasks": len(wl["tasks"]), "out": str(out)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
