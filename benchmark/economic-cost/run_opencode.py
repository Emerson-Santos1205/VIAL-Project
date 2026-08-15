"""Real-model validation harness for RFC-010.

The run has two phases. Calibration measures each candidate model on the same
reasoning operations. Evaluation then freezes policy choices from calibration
and compares token-minimal, total-cost-minimal, deterministic-first and
reason-everything policies on a fresh execution pass.
"""
from __future__ import annotations

import argparse
import json
import platform
import time
from pathlib import Path
from typing import Any

from prototype.context import ContextBuilder, Task
from prototype.opencode_executor import OpencodeExecutor
from prototype.state import Organization


BASE = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def load_workload(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def make_tasks(workload: dict[str, Any]) -> list[Task]:
    return [Task(
        op["id"], op["prompt"], op["required"], op["expected"], "economic",
    ) for op in workload["operations"]]


def make_org(workload: dict[str, Any]) -> Organization:
    org = Organization(workload["org_id"])
    for key, value in workload["state"].items():
        org.add_field(key, value, [key])
    return org


def run_model(model: str, task: Task, builder: ContextBuilder,
              timeout: float) -> dict[str, Any]:
    context = builder.build_selective(task)
    started = time.monotonic()
    row = OpencodeExecutor(model=model, timeout=timeout).execute(context, task)
    elapsed = time.monotonic() - started
    output_tokens = row.get("completion_tokens") or 0
    input_tokens = row.get("prompt_tokens") or context.tokens
    return {
        "model": model,
        "task_id": task.id,
        "context_tokens": context.tokens,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_model_tokens": row.get("total_tokens"),
        "latency_s": round(elapsed, 4),
        "answer": row.get("outcome"),
        "quality": 1.0 if row.get("outcome") == task.expected else 0.0,
        "status": row.get("status"),
    }


def cost(row: dict[str, Any], prices: dict[str, float]) -> dict[str, float]:
    tokens = row["context_tokens"]
    inference = (
        row["input_tokens"] / 1000 * prices["inference_input_per_1k"]
        + row["output_tokens"] / 1000 * prices["inference_output_per_1k"]
    )
    components = {
        "tokens": tokens / 1000 * prices["tokens_per_1k"],
        "inference": inference,
        "latency": row["latency_s"] * prices["latency_per_second"],
        "retrieval": prices["retrieval_per_op"],
        "construction": prices["construction_per_context"],
        "validation": prices["validation_per_op"],
    }
    components["total"] = sum(components.values())
    return components


def summarize(rows: list[dict[str, Any]], prices: dict[str, float]) -> dict[str, Any]:
    totals = {key: 0.0 for key in
              ("tokens", "inference", "latency", "retrieval",
               "construction", "validation", "total")}
    for row in rows:
        for key, value in cost(row, prices).items():
            totals[key] += value
    totals["mean_quality"] = (
        sum(row["quality"] for row in rows) / len(rows) if rows else 0.0
    )
    totals["runs"] = len(rows)
    totals["errors"] = sum(row["status"] != "SUCCESS" for row in rows)
    return totals


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs=2, required=True)
    parser.add_argument("--workload", default="workloads/economic-real.json")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--timeout", type=float, default=180.0)
    parser.add_argument("--out", default="results")
    args = parser.parse_args()
    if args.limit < 0 or args.timeout <= 0:
        parser.error("--limit must be non-negative and --timeout must be positive")

    workload = load_workload(HERE / args.workload)
    operations = workload["operations"][:args.limit or None]
    tasks = make_tasks({**workload, "operations": operations})
    prices = workload["price_table"]
    calibration: dict[str, list[dict[str, Any]]] = {}
    for model in args.models:
        builder = ContextBuilder(make_org(workload))
        calibration[model] = [
            run_model(model, task, builder, args.timeout)
            for task, op in zip(tasks, operations) if not op["deterministic_solvable"]
        ]

    estimates = {
        model: summarize(rows, prices) for model, rows in calibration.items()
    }
    token_model = min(args.models, key=lambda m: estimates[m]["tokens"] +
                      estimates[m]["inference"] / prices["inference_input_per_1k"])
    total_model = min(args.models, key=lambda m: estimates[m]["total"])
    expensive_model = max(args.models, key=lambda m: estimates[m]["total"])
    policy_models = {
        "token_optimal": token_model,
        "total_cost_optimal": total_model,
        "deterministic_first": total_model,
        "reason_everything": expensive_model,
    }

    policy_rows: dict[str, list[dict[str, Any]]] = {}
    for policy, model in policy_models.items():
        rows = []
        builder = ContextBuilder(make_org(workload))
        for task, op in zip(tasks, operations):
            if op["deterministic_solvable"]:
                rows.append({
                    "task_id": task.id, "model": "deterministic",
                    "context_tokens": 0, "input_tokens": 0,
                    "output_tokens": 0, "total_model_tokens": 0,
                    "latency_s": 0.0, "answer": op["deterministic_answer"],
                    "quality": 1.0, "status": "SUCCESS",
                })
            else:
                rows.append(run_model(model, task, builder, args.timeout))
        policy_rows[policy] = rows

    summaries = {policy: summarize(rows, prices)
                 for policy, rows in policy_rows.items()}
    token_cheapest = min(summaries, key=lambda p: summaries[p]["tokens"])
    total_cheapest = min(summaries, key=lambda p: summaries[p]["total"])
    tolerance = workload.get("quality_tolerance", 0.1)
    verdict = {
        "token_cheapest_policy": token_cheapest,
        "total_cheapest_policy": total_cheapest,
        "divergence_exists": token_cheapest != total_cheapest,
        "det_first_total": summaries["deterministic_first"]["total"],
        "reason_total": summaries["reason_everything"]["total"],
        "det_first_le_reason": summaries["deterministic_first"]["total"] <= summaries["reason_everything"]["total"],
        "quality_ok": summaries["deterministic_first"]["mean_quality"] >= summaries["reason_everything"]["mean_quality"] * (1 - tolerance),
    }
    verdict["h1_token_total_divergence"] = verdict["divergence_exists"]
    verdict["h2_deterministic_first"] = verdict["det_first_le_reason"] and verdict["quality_ok"]
    verdict["hypotheses_supported"] = verdict["h1_token_total_divergence"] and verdict["h2_deterministic_first"]

    run_id = time.strftime("%Y%m%d-%H%M%S")
    out_dir = HERE / args.out / f"opencode-{run_id}"
    out_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "run_id": run_id, "rfc": "RFC-010", "executor": "opencode-cli",
        "models": args.models, "workload": workload["name"],
        "limit": args.limit, "timeout": args.timeout,
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "calibration": estimates, "policy_models": policy_models,
        "policies": summaries, "verdict": verdict,
        "per_policy": policy_rows,
    }
    (out_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"report": str(out_dir / "report.json"), "verdict": verdict}, indent=2))
    return 0 if verdict["hypotheses_supported"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
