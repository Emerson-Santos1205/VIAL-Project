"""RFC-009 validation harness.

Runs the same operation stream (a) without failures and (b) with a
deterministic failure schedule, then compares convergence, atomicity,
resolution and idempotency (RFC-009 §2.1).

Recovery policy (deterministic):
- before_commit: intent exists, not committed → abort and retry the operation
  once with the same operation_id? No: RFC-009 §2.3.6 forbids re-using a
  started id. A NEW operation_id is assigned for the retry.
- after_commit: intent committed → recovery returns the committed outcome;
  the caller does NOT re-apply (the coordinator blocks duplicate commit).

Usage:
    python benchmark/failure-recovery/run_benchmark.py [--workload workloads/failure.json] [--out results]
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

from prototype.coordinator import StateCoordinator  # noqa: E402
from prototype.state import Organization  # noqa: E402

import importlib.util  # noqa: E402

_SC_HARNESS = BASE / "benchmark" / "selective-context" / "run_benchmark.py"
_spec = importlib.util.spec_from_file_location("sc_run_benchmark", _SC_HARNESS)
_sc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sc)
build_org, load_workload = _sc.build_org, _sc.load_workload


def run_clean(org: Organization, operations: list[dict]) -> dict:
    coord = StateCoordinator(org)
    for op in operations:
        coord.begin(op["id"], op["key"], op["value"], org.authority)
        coord.commit(op["id"])
    return {
        "snapshot": coord.snapshot(),
        "committed": len(org.transitions),
        "coord": coord,
    }


def run_with_failures(org: Organization, operations: list[dict]) -> dict:
    coord = StateCoordinator(org)
    observed_intermediate = 0
    resolutions = {}
    retries = 0

    for op in operations:
        if op["fail_point"] == "clean":
            intent = coord.begin(op["id"], op["key"], op["value"], org.authority)
            coord.commit(op["id"])
            resolutions[op["id"]] = "committed"
            continue

        if op["fail_point"] == "before_commit":
            # intent recorded, then interrupted before commit
            intent = coord.begin(op["id"], op["key"], op["value"], org.authority)
            # observable read during pending state MUST equal pre-op State
            if coord.snapshot()["version"] != intent.previous_version:
                observed_intermediate += 1
            coord.interruptions += 1
            resolved = coord.resolve(op["id"])
            # recovery: abort, then retry with a fresh operation_id
            coord.abort(op["id"])
            retry_id = f"{op['id']}_retry_{retries}"
            retries += 1
            coord.begin(retry_id, op["key"], op["value"], org.authority)
            coord.commit(retry_id)
            resolutions[op["id"]] = "aborted"
            resolutions[retry_id] = "committed"

        elif op["fail_point"] == "after_commit":
            # commit applied, then ack lost; caller retries same operation
            intent = coord.begin(op["id"], op["key"], op["value"], org.authority)
            coord.commit(op["id"])
            coord.interruptions += 1
            resolved = coord.resolve(op["id"])
            # recovery: already committed → do NOT re-apply
            if resolved.status == "committed":
                resolutions[op["id"]] = "committed"
            coord.commit(op["id"])  # simulated misinformed retry

    snapshot = coord.snapshot()
    return {
        "snapshot": snapshot,
        "committed": len(org.transitions),
        "coord": coord,
        "observed_intermediate": observed_intermediate,
        "resolutions": resolutions,
        "duplicate_commits": coord.duplicate_commits,
        "interruptions": coord.interruptions,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workload", default="workloads/failure.json")
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    base = Path(__file__).resolve().parent
    wl = load_workload(base / args.workload)
    operations = wl["operations"]

    clean_org = build_org(wl)
    clean = run_clean(clean_org, operations)

    fail_org = build_org(wl)
    fail = run_with_failures(fail_org, operations)

    final_state_equal = clean["snapshot"]["fields"] == fail["snapshot"]["fields"]
    version_equal = clean["snapshot"]["version"] == fail["snapshot"]["version"]

    committed_ops = sum(1 for r in fail["resolutions"].values() if r == "committed")
    aborted_ops = sum(1 for r in fail["resolutions"].values() if r == "aborted")
    # unresolved = stream operations without a resolution entry for their own id
    unresolved = sum(1 for op in operations if op["id"] not in fail["resolutions"])
    # duplicate commits = operation_ids that appear more than once as committed
    # transitions (RFC-009 §2.2). Retries that were BLOCKED do not create
    # transitions, so they are not duplicates.
    committed_ids = [t.transition_id for t in fail_org.transitions]
    duplicate_commits = len(committed_ids) - len(set(committed_ids))

    h1 = final_state_equal and version_equal
    h2 = fail["observed_intermediate"] == 0
    h3 = (unresolved == 0) and (duplicate_commits == 0)

    verdict = {
        "final_state_equal": final_state_equal,
        "version_equal": version_equal,
        "h1_continuity": h1,
        "observed_intermediate_states": fail["observed_intermediate"],
        "h2_atomicity": h2,
        "unresolved_operations": unresolved,
        "duplicate_commits": duplicate_commits,
        "resolved_committed": committed_ops,
        "resolved_aborted": aborted_ops,
        "interruptions": fail["interruptions"],
        "h3_recovery": h3,
        "hypotheses_supported": h1 and h2 and h3,
    }

    run_id = time.strftime("%Y%m%d-%H%M%S")
    out_dir = base / args.out / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "run_id": run_id,
        "rfc": "RFC-009",
        "workload": wl["name"],
        "seed": wl.get("seed"),
        "environment": {"python": platform.python_version(),
                        "platform": platform.platform()},
        "command": " ".join(["python", str(Path("benchmark/failure-recovery/run_benchmark.py"))] + sys.argv[1:]),
        "no_failures": {"version": clean["snapshot"]["version"],
                        "committed": clean["committed"]},
        "with_failures": {"version": fail["snapshot"]["version"],
                          "committed": fail["committed"],
                          "interruptions": fail["interruptions"]},
        "verdict": verdict,
        "per_operation": [
            {"id": op["id"], "fail_point": op["fail_point"],
             "resolved": fail["resolutions"].get(op["id"], "unresolved"),
             "retry_id": f"{op['id']}_retry" if op["fail_point"] == "before_commit" else None}
            for op in operations
        ],
    }
    (out_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps({
        "run_id": run_id,
        "no_failures": {"version": clean["snapshot"]["version"], "committed": clean["committed"]},
        "with_failures": {"version": fail["snapshot"]["version"],
                          "committed": fail["committed"],
                          "interruptions": fail["interruptions"]},
        "verdict": verdict,
        "elapsed_s": 0.0,
        "artifacts": str(out_dir),
    }, indent=2))
    return 0 if verdict["hypotheses_supported"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
