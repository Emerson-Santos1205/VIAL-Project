"""Supplemental multi-model validation protocol.

This runner preserves the canonical deterministic benchmarks and compares
actual opencode model behavior across repeated runs. It records model quality,
real token usage, latency and hypothesis verdicts without treating a failed
provider call as a successful zero-quality result.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BENCHMARKS = {
    "selective": {
        "script": ROOT / "benchmark" / "selective-context" / "run_opencode.py",
        "cwd": ROOT / "benchmark" / "selective-context",
        "workload": "workloads/hard-reasoning.json",
        "limit": 20,
        "rfc": "RFC-007",
    },
    "reuse": {
        "script": ROOT / "benchmark" / "cognitive-reuse" / "run_opencode.py",
        "cwd": ROOT / "benchmark" / "cognitive-reuse",
        "workload": "workloads/reuse.json",
        "limit": 50,
        "rfc": "RFC-008",
    },
    "failure": {
        "script": ROOT / "benchmark" / "failure-recovery" / "run_opencode.py",
        "cwd": ROOT / "benchmark" / "failure-recovery",
        "workload": "workloads/failure.json",
        "limit": 40,
        "rfc": "RFC-009",
    },
}


def _last_json(stdout: str) -> dict[str, Any] | None:
    for index in (i for i, char in enumerate(stdout) if char == "{"):
        try:
            value = json.JSONDecoder().raw_decode(stdout[index:])[0]
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and "verdict" in value:
            result = value
    return locals().get("result")


def run_one(name: str, model: str, repeat: int, out_root: Path) -> dict:
    spec = BENCHMARKS[name]
    command = [
        sys.executable, str(spec["script"]),
        "--model", model,
        "--workload", spec["workload"],
        "--limit", str(spec["limit"]),
        "--out", str(out_root / model.replace("/", "_") / name),
    ]
    started = time.monotonic()
    proc = subprocess.run(command, cwd=spec["cwd"], capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    elapsed = time.monotonic() - started
    report = _last_json(proc.stdout)
    verdict = report.get("verdict", {}) if report else {}
    rows = [] if not report else report.get("per_task", report.get("per_operation", []))
    unknown_rows = sum(1 for row in rows if row.get("status") == "UNKNOWN")
    malformed_proposals = sum(
        1 for row in rows
        if name == "failure" and (row.get("key") is None or row.get("value") is None)
    )
    execution_errors = unknown_rows + malformed_proposals
    hypotheses_supported = bool(
        verdict.get("hypotheses_supported", verdict.get("h1_supported", False))
    ) and execution_errors == 0 and proc.returncode == 0
    return {
        "model": model,
        "benchmark": name,
        "rfc": spec["rfc"],
        "repeat": repeat,
        "returncode": proc.returncode,
        "elapsed_s": round(elapsed, 2),
        "hypotheses_supported": hypotheses_supported,
        "execution_errors": execution_errors,
        "verdict": verdict,
        "artifacts": report.get("artifacts") if report else None,
        "error": proc.stderr[-1000:] if proc.returncode and proc.stderr else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", required=True)
    parser.add_argument("--benchmarks", nargs="+", choices=BENCHMARKS,
                        default=list(BENCHMARKS))
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--out", default="results")
    args = parser.parse_args()

    out_root = Path(args.out)
    if not out_root.is_absolute():
        out_root = ROOT / out_root
    results = []
    for model in args.models:
        for repeat in range(1, args.repeats + 1):
            for benchmark in args.benchmarks:
                print(f"running model={model} benchmark={benchmark} repeat={repeat}",
                      flush=True)
                results.append(run_one(benchmark, model, repeat, out_root))

    output = out_root / f"comparison-{time.strftime('%Y%m%d-%H%M%S')}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "protocol": "supplemental-model-comparison-v1",
        "models": args.models,
        "benchmarks": args.benchmarks,
        "repeats": args.repeats,
        "results": results,
        "all_supported": all(r["hypotheses_supported"] for r in results),
    }
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"report": str(output),
                      "all_supported": report["all_supported"],
                      "runs": len(results)}, indent=2))
    return 0 if report["all_supported"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
