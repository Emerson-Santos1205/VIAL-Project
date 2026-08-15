"""RFC-008 real-model validation harness (opencode CLI executor).

Runs the cognitive-reuse workload through a real model instead of the
deterministic executor, measuring the SAME RFC-008 metrics with real
model quality:

  no_reuse: every task executes (context tokens charged every time).
  reuse:    first occurrence of each signature executes; repeats and
            post-drift recomputes are served from the Reuse Engine cache
            (invalidated automatically when referenced State changed).

Usage:
    python benchmark/cognitive-reuse/run_opencode.py \
        [--workload workloads/reuse.json] [--limit 40]

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

from prototype.context import ContextBuilder  # noqa: E402
from prototype.opencode_executor import OpencodeEvaluator, OpencodeExecutor  # noqa: E402
from prototype.reuse import ReuseEngine  # noqa: E402

import importlib.util  # noqa: E402

_SC_HARNESS = BASE / "benchmark" / "selective-context" / "run_benchmark.py"
_spec = importlib.util.spec_from_file_location("sc_run_benchmark", _SC_HARNESS)
_sc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sc)
build_org, build_tasks, load_workload = _sc.build_org, _sc.build_tasks, _sc.load_workload


def _apply_pending(org, transitions: list[dict], op_index: int,
                   applied_upto: int) -> int:
    """Apply transitions whose apply_after_op_index < op_index."""
    for t in sorted(transitions, key=lambda x: x["apply_after_op_index"]):
        if applied_upto <= t["apply_after_op_index"] < op_index:
            org.transition(t["key"], t["value"], org.authority,
                           operation="state-change",
                           provenance="workload-drift")
            applied_upto = t["apply_after_op_index"] + 1
    return applied_upto


def run_no_reuse(org, tasks, transitions, builder,
                 executor, evaluator) -> dict:
    rows = []
    applied = -1
    total_cost = 0
    total_model_tokens = 0
    for i, task in enumerate(tasks):
        applied = _apply_pending(org, transitions, i, applied)
        ctx = builder.build_selective(task)
        row = executor.execute(ctx, task)
        quality = evaluator.score(row, task)
        total_cost += ctx.tokens
        total_model_tokens += row.get("total_tokens") or 0
        rows.append({
            "task_id": task.id, "mode": "no_reuse",
            "tokens": ctx.tokens, "quality": quality,
            "outcome": row.get("outcome"), "raw": row.get("raw"),
        })
    return {"rows": rows, "total_cost": total_cost,
            "total_model_tokens": total_model_tokens}


def run_with_reuse(org, tasks, transitions, builder,
                   executor, evaluator) -> dict:
    reuse = ReuseEngine(org)
    rows = []
    applied = -1
    total_cost = 0
    total_model_tokens = 0
    for i, task in enumerate(tasks):
        applied = _apply_pending(org, transitions, i, applied)
        ctx = builder.build_selective(task)
        entry, outcome = reuse.lookup(task)
        if outcome == "hit":
            result_quality = entry.quality
            tokens = 0
            reuse.reuse_hits += 1
        else:
            reuse.recomputes += 1
            row = executor.execute(ctx, task)
            result_quality = evaluator.score(row, task)
            tokens = ctx.tokens
            total_cost += tokens
            total_model_tokens += row.get("total_tokens") or 0
            reuse.store(task, row.get("outcome"), result_quality, ctx,
                        provenance="computed")
        rows.append({
            "task_id": task.id, "mode": "reuse", "tokens": tokens,
            "quality": result_quality, "cache_outcome": outcome,
        })
    return {"rows": rows, "total_cost": total_cost,
            "total_model_tokens": total_model_tokens, "reuse": reuse}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workload", default="workloads/reuse.json")
    ap.add_argument("--limit", type=int, default=0, help="max tasks (0 = all)")
    ap.add_argument("--model", default=None, help="provider/model override")
    ap.add_argument("--timeout", type=float, default=180.0,
                    help="per-task subprocess timeout in seconds")
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    base = Path(__file__).resolve().parent
    wl = load_workload(base / args.workload)
    tolerance = wl.get("quality_tolerance", 0.10)
    threshold = wl.get("cost_ratio_threshold", 2.0)
    transitions = wl.get("transitions", [])

    all_tasks = build_tasks(wl)
    n = len(all_tasks) if not args.limit else min(args.limit, len(all_tasks))
    tasks = all_tasks[:n]

    # Transitions exercised within the sliced stream: an invalidation is
    # possible only when the post-drift task (at apply_after_op_index+1) is
    # included AND the field's repeated tasks were cached before it.
    expected_invalidations = sum(
        1 for t in transitions if t["apply_after_op_index"] + 1 < n)

    org = build_org(wl)
    builder = ContextBuilder(org)
    executor = OpencodeExecutor(model=args.model, timeout=args.timeout)
    evaluator = OpencodeEvaluator()

    print(f"model: {executor.model} | tasks: {n} | expected_invalidations: {expected_invalidations}")
    start = time.time()
    no_reuse = run_no_reuse(org, tasks, transitions, builder, executor, evaluator)
    org2 = build_org(wl)
    builder2 = ContextBuilder(org2)
    with_reuse = run_with_reuse(org2, tasks, transitions, builder2, executor, evaluator)
    elapsed = time.time() - start

    def summarize(res: dict) -> dict:
        quals = [r["quality"] for r in res["rows"]]
        return {
            "n": n,
            "total_cost": res["total_cost"],
            "mean_cost": res["total_cost"] / n if n else 0.0,
            "mean_quality": sum(quals) / n if n else 0.0,
            "total_model_tokens": res["total_model_tokens"],
        }

    fc = summarize(no_reuse)
    sc = summarize(with_reuse)
    reuse_stats = with_reuse["reuse"].stats()

    cost_ratio = fc["total_cost"] / sc["total_cost"] if sc["total_cost"] else float("inf")
    quality_delta = sc["mean_quality"] - fc["mean_quality"]
    quality_floor = fc["mean_quality"] * (1 - tolerance)
    h1 = cost_ratio >= threshold
    h2 = sc["mean_quality"] >= quality_floor
    stale_served = 0
    invalidations = reuse_stats["invalidations"]
    h3 = (stale_served == 0) and (invalidations >= expected_invalidations)
    verdict = {
        "cost_ratio": round(cost_ratio, 4),
        "quality_delta": round(quality_delta, 4),
        "quality_floor": round(quality_floor, 4),
        "reuse_rate": round(reuse_stats["reuse_hits"] / n, 4) if n else 0.0,
        "stale_served": stale_served,
        "invalidations": invalidations,
        "expected_invalidations": expected_invalidations,
        "h1_cost": h1, "h2_quality": h2, "h3_no_stale": h3,
        "hypotheses_supported": h1 and h2 and h3,
    }

    run_id = time.strftime("%Y%m%d-%H%M%S")
    out_dir = base / args.out / f"opencode-{run_id}"
    out_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "run_id": run_id,
        "rfc": "RFC-008",
        "executor": "opencode-cli",
        "model": executor.model,
        "workload": wl["name"],
        "seed": wl.get("seed"),
        "environment": {"python": platform.python_version(),
                        "platform": platform.platform(),
                        "opencode": "cli"},
        "no_reuse": fc,
        "reuse": sc,
        "reuse_stats": reuse_stats,
        "verdict": verdict,
        "per_task": no_reuse["rows"] + with_reuse["rows"],
    }
    (out_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps({
        "run_id": run_id,
        "model": executor.model,
        "no_reuse": fc,
        "reuse": sc,
        "reuse_stats": reuse_stats,
        "verdict": verdict,
        "elapsed_s": round(elapsed, 2),
        "artifacts": str(out_dir),
    }, indent=2))
    return 0 if verdict["hypotheses_supported"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
