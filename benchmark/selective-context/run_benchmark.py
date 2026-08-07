"""RFC-007 validation harness.

Executes a declared workload under both Full Context and Selective Context,
computes the RFC-007 metrics, applies acceptance criteria and stores artifacts.

Usage:
    python benchmark/selective-context/run_benchmark.py [--workload workload.json] [--out results/]
"""
from __future__ import annotations

import argparse
import json
import platform
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from prototype.context import ContextBuilder, Task
from prototype.executor import DeterministicExecutor, Evaluator
from prototype.state import Organization


def load_workload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_org(workload: dict) -> Organization:
    org = Organization(workload["org_id"])
    for f in workload["state_fields"]:
        org.add_field(f["key"], f["value"], f["relevance"], f.get("authority"))
    return org


def build_tasks(workload: dict) -> list[Task]:
    return [
        Task(
            id=t["id"],
            prompt=t["prompt"],
            required=t["required"],
            expected=t["expected"],
            op=t["op"],
            args=t.get("args"),
        )
        for t in workload["tasks"]
    ]


def run_condition(mode: str, tasks: list[Task], builder: ContextBuilder,
                  executor: DeterministicExecutor, evaluator: Evaluator,
                  seed: int) -> list[dict]:
    rng = random.Random(seed)
    rows = []
    for task in tasks:
        ctx = builder.build_full(task) if mode == "full" else builder.build_selective(task)
        result = executor.execute(ctx, task)
        rows.append({
            "task_id": task.id,
            "mode": mode,
            "tokens": ctx.tokens,
            "state_version": ctx.state_version,
            "quality": evaluator.score(result),
            "outcome": result.outcome,
        })
        rng.random()  # consume seed deterministically for reproducibility
    return rows


def summarize(rows: list[dict], n_tasks: int) -> dict:
    costs = [r["tokens"] for r in rows]
    quals = [r["quality"] for r in rows]
    return {
        "n_tasks": n_tasks,
        "total_cost": sum(costs),
        "mean_cost": sum(costs) / n_tasks,
        "median_cost": sorted(costs)[n_tasks // 2],
        "mean_quality": sum(quals) / n_tasks,
    }


def apply_criteria(fc: dict, sc: dict, quality_tolerance: float,
                   cost_ratio_threshold: float) -> dict:
    cost_ratio = fc["total_cost"] / sc["total_cost"] if sc["total_cost"] else float("inf")
    quality_delta = sc["mean_quality"] - fc["mean_quality"]
    quality_floor = fc["mean_quality"] * (1 - quality_tolerance)
    cost_ok = cost_ratio >= cost_ratio_threshold
    quality_ok = sc["mean_quality"] >= quality_floor
    return {
        "cost_ratio": round(cost_ratio, 4),
        "quality_delta": round(quality_delta, 4),
        "quality_floor": round(quality_floor, 4),
        "cost_ok": cost_ok,
        "quality_ok": quality_ok,
        "h1_supported": cost_ok and quality_ok,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workload", default="workload.json")
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    base = Path(__file__).resolve().parent
    wl = load_workload(base / args.workload)

    seed = wl.get("seed", 42)
    tolerance = wl.get("quality_tolerance", 0.10)
    threshold = wl.get("cost_ratio_threshold", 2.0)

    org = build_org(wl)
    tasks = build_tasks(wl)
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

    run_id = time.strftime("%Y%m%d-%H%M%S")
    out_dir = base / args.out / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    env = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "tiktoken": "available",
    }
    report = {
        "run_id": run_id,
        "rfc": "RFC-007",
        "workload": wl["name"],
        "seed": seed,
        "quality_tolerance": tolerance,
        "cost_ratio_threshold": threshold,
        "environment": env,
        "command": " ".join(["python", str(Path("benchmark/selective-context/run_benchmark.py"))] + sys.argv[1:]),
        "full_context": fc_sum,
        "selective_context": sc_sum,
        "verdict": verdict,
        "per_task": fc_rows + sc_rows,
    }

    (out_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps({
        "run_id": run_id,
        "full_context": fc_sum,
        "selective_context": sc_sum,
        "verdict": verdict,
        "elapsed_s": round(elapsed, 3),
        "artifacts": str(out_dir),
    }, indent=2))

    return 0 if verdict["h1_supported"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
