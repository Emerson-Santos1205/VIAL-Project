"""RFC-007 real-model validation harness (opencode CLI executor).

Usage:
    python benchmark/selective-context/run_opencode.py \
        [--workload workloads/reasoning.json] [--limit 10]

Model via --model or env OPENCODE_MODEL (default opencode/deepseek-v4-flash-free).
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(HERE))

from prototype.context import ContextBuilder, Task  # noqa: E402
from prototype.opencode_executor import OpencodeEvaluator, OpencodeExecutor  # noqa: E402
from prototype.state import Organization  # noqa: E402
from run_benchmark import build_org, build_tasks, load_workload  # noqa: E402


def run_condition(mode: str, tasks: list[Task], builder: ContextBuilder,
                  executor: OpencodeExecutor, evaluator: OpencodeEvaluator) -> list[dict]:
    rows = []
    for task in tasks:
        ctx = builder.build_full(task) if mode == "full" else builder.build_selective(task)
        row = executor.execute(ctx, task)
        row["tokens"] = ctx.tokens
        row["quality"] = evaluator.score(row, task)
        rows.append(row)
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
        "total_prompt_tokens": sum(r.get("prompt_tokens") or 0 for r in rows),
        "total_completion_tokens": sum(r.get("completion_tokens") or 0 for r in rows),
        "total_model_tokens": sum(r.get("total_tokens") or 0 for r in rows),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workload", default="workloads/reasoning.json")
    ap.add_argument("--limit", type=int, default=0, help="max tasks (0 = all)")
    ap.add_argument("--model", default=None, help="provider/model override")
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    base = Path(__file__).resolve().parent
    wl = load_workload(base / args.workload)
    tolerance = wl.get("quality_tolerance", 0.10)
    threshold = wl.get("cost_ratio_threshold", 2.0)

    org = build_org(wl)
    tasks = build_tasks(wl)
    if args.limit:
        tasks = tasks[: args.limit]
    builder = ContextBuilder(org)
    executor = OpencodeExecutor(model=args.model)
    evaluator = OpencodeEvaluator()

    print(f"model: {executor.model} | tasks: {len(tasks)}")
    start = time.time()
    fc_rows = run_condition("full", tasks, builder, executor, evaluator)
    sc_rows = run_condition("selective", tasks, builder, executor, evaluator)
    elapsed = time.time() - start

    fc_sum = summarize(fc_rows, len(tasks))
    sc_sum = summarize(sc_rows, len(tasks))

    cost_ratio = fc_sum["total_cost"] / sc_sum["total_cost"] if sc_sum["total_cost"] else float("inf")
    quality_delta = sc_sum["mean_quality"] - fc_sum["mean_quality"]
    quality_floor = fc_sum["mean_quality"] * (1 - tolerance)
    cost_ok = cost_ratio >= threshold
    quality_ok = sc_sum["mean_quality"] >= quality_floor
    verdict = {
        "cost_ratio": round(cost_ratio, 4),
        "quality_delta": round(quality_delta, 4),
        "quality_floor": round(quality_floor, 4),
        "cost_ok": cost_ok,
        "quality_ok": quality_ok,
        "h1_supported": cost_ok and quality_ok,
    }

    run_id = time.strftime("%Y%m%d-%H%M%S")
    out_dir = base / args.out / f"opencode-{run_id}"
    out_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "run_id": run_id,
        "rfc": "RFC-007",
        "executor": "opencode-cli",
        "model": executor.model,
        "workload": wl["name"],
        "environment": {"python": platform.python_version(),
                        "platform": platform.platform(),
                        "opencode": "cli"},
        "full_context": fc_sum,
        "selective_context": sc_sum,
        "verdict": verdict,
        "per_task": fc_rows + sc_rows,
    }
    (out_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps({
        "run_id": run_id,
        "model": executor.model,
        "full_context": fc_sum,
        "selective_context": sc_sum,
        "verdict": verdict,
        "elapsed_s": round(elapsed, 2),
        "artifacts": str(out_dir),
    }, indent=2))
    return 0 if verdict["h1_supported"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
