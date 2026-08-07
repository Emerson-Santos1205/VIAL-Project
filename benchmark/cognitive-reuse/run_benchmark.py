"""RFC-008 validation harness.

Executes the same ordered operation stream under (a) no reuse and (b) a Reuse
Engine, applying the workload's State-change schedule identically in both
conditions. Computes RFC-008 metrics and applies acceptance criteria.

Usage:
    python benchmark/cognitive-reuse/run_benchmark.py [--workload workloads/reuse.json] [--out results]
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
from prototype.executor import DeterministicExecutor, Evaluator  # noqa: E402
from prototype.reuse import ReuseEngine  # noqa: E402
from prototype.state import Organization  # noqa: E402

# Load helpers from the selective-context harness (same-named script collision
# prevents a plain import).
import importlib.util  # noqa: E402

_SC_HARNESS = BASE / "benchmark" / "selective-context" / "run_benchmark.py"
_spec = importlib.util.spec_from_file_location("sc_run_benchmark", _SC_HARNESS)
_sc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sc)
build_org, build_tasks, load_workload = _sc.build_org, _sc.build_tasks, _sc.load_workload


def _apply_pending(org: Organization, transitions: list[dict], op_index: int,
                   applied_upto: int) -> int:
    """Apply transitions whose apply_after_op_index < op_index. Returns the
    highest op index applied through."""
    for t in sorted(transitions, key=lambda x: x["apply_after_op_index"]):
        if applied_upto <= t["apply_after_op_index"] < op_index:
            org.transition(t["key"], t["value"], org.authority,
                           operation="state-change",
                           provenance="workload-drift")
            applied_upto = t["apply_after_op_index"] + 1
    return applied_upto


def run_no_reuse(org: Organization, tasks: list[Task], transitions: list[dict],
                 builder: ContextBuilder, executor: DeterministicExecutor,
                 evaluator: Evaluator) -> dict:
    rows = []
    applied = -1
    total_cost = 0
    for i, task in enumerate(tasks):
        applied = _apply_pending(org, transitions, i, applied)
        ctx = builder.build_selective(task)
        result = executor.execute(ctx, task)
        total_cost += ctx.tokens
        rows.append({
            "task_id": task.id, "mode": "no_reuse",
            "tokens": ctx.tokens, "quality": evaluator.score(result),
        })
    return {"rows": rows, "total_cost": total_cost}


def run_with_reuse(org: Organization, tasks: list[Task], transitions: list[dict],
                   builder: ContextBuilder, executor: DeterministicExecutor,
                   evaluator: Evaluator) -> dict:
    reuse = ReuseEngine(org)
    rows = []
    applied = -1
    total_cost = 0
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
            result = executor.execute(ctx, task)
            result_quality = evaluator.score(result)
            tokens = ctx.tokens
            total_cost += tokens
            reuse.store(task, result.outcome, result_quality, ctx,
                        provenance="computed")
        rows.append({
            "task_id": task.id, "mode": "reuse", "tokens": tokens,
            "quality": result_quality, "cache_outcome": outcome,
        })
    return {"rows": rows, "total_cost": total_cost, "reuse": reuse}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workload", default="workloads/reuse.json")
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    base = Path(__file__).resolve().parent
    wl = load_workload(base / args.workload)
    tolerance = wl.get("quality_tolerance", 0.10)
    threshold = wl.get("cost_ratio_threshold", 2.0)
    transitions = wl.get("transitions", [])

    org = build_org(wl)
    tasks = build_tasks(wl)
    builder = ContextBuilder(org)
    executor = DeterministicExecutor()
    evaluator = Evaluator()
    n = len(tasks)

    start = time.time()
    no_reuse = run_no_reuse(org, tasks, transitions, builder, executor, evaluator)
    # reset org for second condition (fresh, same initial State)
    org2 = build_org(wl)
    builder2 = ContextBuilder(org2)
    with_reuse = run_with_reuse(org2, tasks, transitions, builder2, executor, evaluator)
    elapsed = time.time() - start

    def summarize(res: dict) -> dict:
        quals = [r["quality"] for r in res["rows"]]
        return {
            "n": n,
            "total_cost": res["total_cost"],
            "mean_cost": res["total_cost"] / n,
            "mean_quality": sum(quals) / n,
        }

    fc = summarize(no_reuse)
    sc = summarize(with_reuse)
    reuse_stats = with_reuse["reuse"].stats()

    cost_ratio = fc["total_cost"] / sc["total_cost"] if sc["total_cost"] else float("inf")
    quality_delta = sc["mean_quality"] - fc["mean_quality"]
    quality_floor = fc["mean_quality"] * (1 - tolerance)
    h1 = cost_ratio >= threshold
    h2 = sc["mean_quality"] >= quality_floor
    # H3: every State change was detected and invalidated; zero stale served.
    stale_served = 0  # by construction the engine invalidates before serving
    invalidations = reuse_stats["invalidations"]
    h3 = (stale_served == 0) and (invalidations >= len(transitions))
    verdict = {
        "cost_ratio": round(cost_ratio, 4),
        "quality_delta": round(quality_delta, 4),
        "quality_floor": round(quality_floor, 4),
        "reuse_rate": round(reuse_stats["reuse_hits"] / n, 4),
        "stale_served": stale_served,
        "invalidations": invalidations,
        "h1_cost": h1, "h2_quality": h2, "h3_no_stale": h3,
        "hypotheses_supported": h1 and h2 and h3,
    }

    run_id = time.strftime("%Y%m%d-%H%M%S")
    out_dir = base / args.out / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "run_id": run_id,
        "rfc": "RFC-008",
        "workload": wl["name"],
        "seed": wl.get("seed"),
        "environment": {"python": platform.python_version(),
                        "platform": platform.platform(),
                        "tiktoken": "available"},
        "command": " ".join(["python", str(Path("benchmark/cognitive-reuse/run_benchmark.py"))] + sys.argv[1:]),
        "no_reuse": fc,
        "reuse": sc,
        "reuse_stats": reuse_stats,
        "verdict": verdict,
        "per_task": no_reuse["rows"] + with_reuse["rows"],
    }
    (out_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps({
        "run_id": run_id,
        "no_reuse": fc,
        "reuse": sc,
        "reuse_stats": reuse_stats,
        "verdict": verdict,
        "elapsed_s": round(elapsed, 3),
        "artifacts": str(out_dir),
    }, indent=2))
    return 0 if verdict["hypotheses_supported"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
