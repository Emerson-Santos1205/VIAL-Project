"""Scaling sweep for RFC-007.

Runs the selective-context benchmark across increasing Organization State sizes
and reports cost_ratio and quality parity per size, testing the prediction that
the benefit of selective context grows with state size (RFC-003 §41).

Usage:
    python benchmark/selective-context/run_scaling.py [--sizes 100,1000,10000] [--tasks 300]
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE))

from generate_workload import generate  # noqa: E402
from prototype.context import ContextBuilder, Task  # noqa: E402
from prototype.executor import DeterministicExecutor, Evaluator  # noqa: E402
from prototype.state import Organization  # noqa: E402
from run_benchmark import (  # noqa: E402
    apply_criteria,
    build_org,
    build_tasks,
    run_condition,
    summarize,
)


def build_tasks_from_wl(wl: dict) -> list[Task]:
    return build_tasks(wl)


def run_size(n_fields: int, n_tasks: int, seed: int, tolerance: float,
             threshold: float) -> dict:
    wl = generate(
        org_id=f"scale-{n_fields}",
        n_fields=n_fields,
        n_domains=10,
        n_tasks=n_tasks,
        seed=seed,
    )
    org = build_org(wl)
    tasks = build_tasks_from_wl(wl)
    builder = ContextBuilder(org)
    executor = DeterministicExecutor()
    evaluator = Evaluator()

    start = time.time()
    fc_rows = run_condition("full", tasks, builder, executor, evaluator, seed)
    sc_rows = run_condition("selective", tasks, builder, executor, evaluator, seed)
    elapsed = time.time() - start

    fc_sum = summarize(fc_rows, len(tasks))
    sc_sum = summarize(sc_rows, len(tasks))
    verdict = apply_criteria(fc_sum, sc_sum, tolerance, threshold)

    mean_req = sum(len(t.required) for t in tasks) / len(tasks)
    return {
        "n_fields": n_fields,
        "n_tasks": len(tasks),
        "mean_required_per_task": round(mean_req, 2),
        "full_total_cost": fc_sum["total_cost"],
        "selective_total_cost": sc_sum["total_cost"],
        "cost_ratio": verdict["cost_ratio"],
        "full_mean_quality": fc_sum["mean_quality"],
        "selective_mean_quality": sc_sum["mean_quality"],
        "quality_delta": verdict["quality_delta"],
        "h1_supported": verdict["h1_supported"],
        "elapsed_s": round(elapsed, 2),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", default="100,1000,10000,100000")
    ap.add_argument("--tasks", type=int, default=300)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="results/scaling.json")
    args = ap.parse_args()

    sizes = [int(s) for s in args.sizes.split(",")]
    tolerance, threshold = 0.10, 2.0

    rows = []
    for n in sizes:
        row = run_size(n, args.tasks, args.seed, tolerance, threshold)
        rows.append(row)
        print(json.dumps(row))

    out = Path(__file__).resolve().parent / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "rfc": "RFC-007",
        "experiment": "scaling sweep",
        "seed": args.seed,
        "tasks_per_size": args.tasks,
        "quality_tolerance": tolerance,
        "cost_ratio_threshold": threshold,
        "environment": {"python": platform.python_version(),
                        "platform": platform.platform(),
                        "tiktoken": "available"},
        "rows": rows,
    }
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("\n=== SUMMARY ===")
    print(f"{'fields':>9} {'tasks':>6} {'cost_ratio':>10} {'qFc':>7} {'qSc':>7} {'H1':>4}")
    for r in rows:
        print(f"{r['n_fields']:>9} {r['n_tasks']:>6} {r['cost_ratio']:>10.2f} "
              f"{r['full_mean_quality']:>7.2f} {r['selective_mean_quality']:>7.2f} "
              f"{str(r['h1_supported']):>4}")
    print(f"\nartifacts: {out}")
    return 0 if all(r["h1_supported"] for r in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
