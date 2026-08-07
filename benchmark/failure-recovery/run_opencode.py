"""RFC-009 real-model validation harness (opencode CLI proposer).

Design A (RFC-009 §2.1 extension): a real model PROPOSES each State transition
({"key": ..., "value": ...}) from a natural-language instruction. The
StateCoordinator then executes the proposed stream under the SAME deterministic
failure schedule as the workload, and the RFC-009 hypotheses are checked on the
model-proposed stream.

Two things are validated in one run:
  1. proposal_quality: fraction of model proposals matching the intended
     transition (correct key AND value).
  2. H1/H2/H3: coordinator continuity, atomicity, idempotency + recovery hold
     with real-model proposals (not just the deterministic stream).

Usage:
    python benchmark/failure-recovery/run_opencode.py \
        [--workload workloads/failure.json] [--limit 40]

Model via --model or env OPENCODE_MODEL (default opencode/deepseek-v4-flash-free).
"""
from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(HERE))

from prototype.coordinator import StateCoordinator  # noqa: E402
from prototype.opencode_executor import DEFAULT_MODEL, _opencode_command  # noqa: E402

import importlib.util  # noqa: E402

_SC_HARNESS = BASE / "benchmark" / "selective-context" / "run_benchmark.py"
_spec = importlib.util.spec_from_file_location("sc_run_benchmark", _SC_HARNESS)
_sc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sc)
build_org, load_workload = _sc.build_org, _sc.load_workload


def _propose(executable: str, model: str, op: dict, timeout: float) -> dict:
    """Ask the model to propose a transition for one operation."""
    system = ("You are an execution resource in a cognitive organization. "
              "Propose the State transition for the operation. "
              'Respond with a single JSON object: {"key": <field key>, '
              '"value": <integer>} and nothing else.')
    prompt = (system + "\n\nOPERATION:\n"
              f"Set field {op['key']} to value {op['value']}.")
    cmd = [executable, "run", "--format", "json",
           "--model", model, prompt]
    proc = subprocess.run(cmd, capture_output=True, text=True,
                          timeout=timeout, encoding="utf-8", errors="replace")
    events = [json.loads(l) for l in proc.stdout.splitlines() if l.strip()]

    text = ""
    tokens = {}
    for ev in events:
        if ev.get("type") == "text":
            text += ev.get("part", {}).get("text", "")
        if ev.get("type") == "step_finish":
            tokens = ev.get("part", {}).get("tokens", {}) or {}

    key = None
    value = None
    m = re.search(r'"key"\s*:\s*"(f_\d+)"', text)
    if m:
        key = m.group(1)
    m = re.search(r'"value"\s*:\s*(\d+)', text)
    if m:
        value = int(m.group(1))

    return {
        "id": op["id"],
        "key": key,
        "value": value,
        "fail_point": op["fail_point"],
        "tokens": tokens.get("total"),
        "raw": text.strip(),
    }


def run_clean(org, operations: list[dict]) -> dict:
    coord = StateCoordinator(org)
    for op in operations:
        coord.begin(op["id"], op["key"], op["value"], org.authority)
        coord.commit(op["id"])
    return {"snapshot": coord.snapshot(), "committed": len(org.transitions)}


def run_with_failures(org, operations: list[dict]) -> dict:
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
            intent = coord.begin(op["id"], op["key"], op["value"], org.authority)
            if coord.snapshot()["version"] != intent.previous_version:
                observed_intermediate += 1
            coord.interruptions += 1
            coord.abort(op["id"])
            retry_id = f"{op['id']}_retry_{retries}"
            retries += 1
            coord.begin(retry_id, op["key"], op["value"], org.authority)
            coord.commit(retry_id)
            resolutions[op["id"]] = "aborted"
            resolutions[retry_id] = "committed"

        elif op["fail_point"] == "after_commit":
            intent = coord.begin(op["id"], op["key"], op["value"], org.authority)
            coord.commit(op["id"])
            coord.interruptions += 1
            resolved = coord.resolve(op["id"])
            if resolved.status == "committed":
                resolutions[op["id"]] = "committed"
            coord.commit(op["id"])

    return {
        "snapshot": coord.snapshot(),
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
    ap.add_argument("--limit", type=int, default=0, help="max operations (0 = all)")
    ap.add_argument("--model", default=None)
    ap.add_argument("--timeout", type=float, default=180.0)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    base = Path(__file__).resolve().parent
    wl = load_workload(base / args.workload)
    model = args.model or DEFAULT_MODEL
    executable = _opencode_command()
    org = build_org(wl)
    valid_keys = set(org.fields.keys())

    ops = wl["operations"]
    if args.limit:
        ops = ops[: args.limit]

    print(f"model: {model} | operations: {len(ops)}")
    start = time.time()
    proposals = [_propose(executable, model, op, args.timeout) for op in ops]
    elapsed = time.time() - start

    n = len(proposals)
    parse_ok = sum(1 for p in proposals if p["key"] is not None and p["value"] is not None)
    key_ok = sum(1 for p in proposals if p["key"] in valid_keys)
    match = sum(1 for p, o in zip(proposals, ops)
                if p["key"] == o["key"] and p["value"] == o["value"])
    proposal_quality = match / n if n else 0.0

    # The pipeline runs on model-proposed transitions. Operations whose
    # proposal was unparseable or referenced an unknown field are excluded
    # (they are counted in proposal_quality, not in the coordinator metrics).
    run_ops = [p for p in proposals
               if p["key"] in valid_keys and p["value"] is not None]

    clean_org = build_org(wl)
    clean = run_clean(clean_org, run_ops)
    fail_org = build_org(wl)
    fail = run_with_failures(fail_org, run_ops)

    final_state_equal = clean["snapshot"]["fields"] == fail["snapshot"]["fields"]
    version_equal = clean["snapshot"]["version"] == fail["snapshot"]["version"]
    committed_ops = sum(1 for r in fail["resolutions"].values() if r == "committed")
    unresolved = sum(1 for op in run_ops if op["id"] not in fail["resolutions"])
    committed_ids = [t.transition_id for t in fail_org.transitions]
    duplicate_commits = len(committed_ids) - len(set(committed_ids))

    h1 = final_state_equal and version_equal
    h2 = fail["observed_intermediate"] == 0
    h3 = (unresolved == 0) and (duplicate_commits == 0)
    verdict = {
        "proposal_quality": round(proposal_quality, 4),
        "proposals": n, "parse_ok": parse_ok, "key_ok": key_ok, "exact_match": match,
        "pipeline_ops": len(run_ops),
        "final_state_equal": final_state_equal,
        "version_equal": version_equal,
        "h1_continuity": h1,
        "observed_intermediate_states": fail["observed_intermediate"],
        "h2_atomicity": h2,
        "unresolved_operations": unresolved,
        "duplicate_commits": duplicate_commits,
        "interruptions": fail["interruptions"],
        "h3_recovery": h3,
        "hypotheses_supported": h1 and h2 and h3,
    }

    run_id = time.strftime("%Y%m%d-%H%M%S")
    out_dir = base / args.out / f"opencode-{run_id}"
    out_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "run_id": run_id,
        "rfc": "RFC-009",
        "executor": "opencode-cli (proposer)",
        "model": model,
        "workload": wl["name"],
        "seed": wl.get("seed"),
        "environment": {"python": platform.python_version(),
                        "platform": platform.platform()},
        "no_failures": {"version": clean["snapshot"]["version"],
                        "committed": clean["committed"]},
        "with_failures": {"version": fail["snapshot"]["version"],
                          "committed": fail["committed"],
                          "interruptions": fail["interruptions"]},
        "verdict": verdict,
        "per_operation": proposals,
    }
    (out_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps({
        "run_id": run_id,
        "model": model,
        "verdict": verdict,
        "elapsed_s": round(elapsed, 2),
        "artifacts": str(out_dir),
    }, indent=2))
    return 0 if verdict["hypotheses_supported"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
