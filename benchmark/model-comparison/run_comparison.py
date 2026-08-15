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
from collections import defaultdict
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
    "economic": {
        "script": ROOT / "benchmark" / "economic-cost" / "run_opencode.py",
        "cwd": ROOT / "benchmark" / "economic-cost",
        "workload": "workloads/economic-real.json",
        "rfc": "RFC-010",
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


def run_one(name: str, model: str, repeat: int, out_root: Path,
            limit: int | None, timeout: float | None) -> dict:
    spec = BENCHMARKS[name]
    command = [
        sys.executable, str(spec["script"]),
        "--model", model,
        "--workload", spec["workload"],
        "--limit", str(limit if limit is not None else spec["limit"]),
        "--out", str(out_root / model.replace("/", "_") /
                       f"repeat-{repeat}" / name),
    ]
    if timeout is not None:
        command.extend(["--timeout", str(timeout)])
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


def run_economic(models: list[str], repeat: int, out_root: Path,
                 limit: int | None, timeout: float | None) -> dict:
    spec = BENCHMARKS["economic"]
    command = [
        sys.executable, str(spec["script"]), "--models", *models,
        "--workload", spec["workload"],
        "--out", str(out_root / "economic" / f"repeat-{repeat}"),
    ]
    if limit is not None:
        command.extend(["--limit", str(limit)])
    if timeout is not None:
        command.extend(["--timeout", str(timeout)])
    started = time.monotonic()
    proc = subprocess.run(command, cwd=spec["cwd"], capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    report = _last_json(proc.stdout)
    verdict = report.get("verdict", {}) if report else {}
    return {
        "model": " vs ".join(models), "models": models,
        "benchmark": "economic", "rfc": "RFC-010", "repeat": repeat,
        "returncode": proc.returncode,
        "elapsed_s": round(time.monotonic() - started, 2),
        "hypotheses_supported": bool(verdict.get("hypotheses_supported", False)) and proc.returncode == 0,
        "execution_errors": 0, "verdict": verdict,
        "artifacts": report.get("report") if report else None,
        "error": proc.stderr[-1000:] if proc.returncode and proc.stderr else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", required=True)
    parser.add_argument("--benchmarks", nargs="+", choices=BENCHMARKS,
                        default=list(BENCHMARKS))
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--limit", type=int, default=None,
                        help="override tasks per benchmark")
    parser.add_argument("--timeout", type=float, default=None,
                        help="override per-task model timeout in seconds")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    if args.repeats < 1:
        parser.error("--repeats must be at least 1")
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be at least 1")
    if args.timeout is not None and args.timeout <= 0:
        parser.error("--timeout must be greater than 0")
    if len(set(args.models)) != len(args.models):
        parser.error("--models must not contain duplicates")
    if "economic" in args.benchmarks and len(args.models) != 2:
        parser.error("the economic benchmark requires exactly two models")

    out_root = Path(args.out) if args.out else ROOT / "benchmark" / "model-comparison" / "results"
    if not out_root.is_absolute():
        out_root = ROOT / out_root
    results = []
    single_benchmarks = [name for name in args.benchmarks if name != "economic"]
    for model in args.models:
        for repeat in range(1, args.repeats + 1):
            for benchmark in single_benchmarks:
                print(f"running model={model} benchmark={benchmark} repeat={repeat}",
                      flush=True)
                results.append(run_one(benchmark, model, repeat, out_root,
                                       args.limit, args.timeout))
    if "economic" in args.benchmarks:
        for repeat in range(1, args.repeats + 1):
            print(f"running models={'/'.join(args.models)} benchmark=economic repeat={repeat}",
                  flush=True)
            results.append(run_economic(args.models, repeat, out_root,
                                        args.limit, args.timeout))

    output = out_root / f"comparison-{time.strftime('%Y%m%d-%H%M%S')}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "protocol": "supplemental-model-comparison-v1",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "models": args.models,
        "benchmarks": args.benchmarks,
        "repeats": args.repeats,
        "limit": args.limit,
        "timeout": args.timeout,
        "results": results,
    }
    by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for result in results:
        by_model[result["model"]].append(result)
    report["model_summaries"] = {
        model: {
            "runs": len(model_results),
            "successful_runs": sum(
                1 for result in model_results
                if result["hypotheses_supported"]
            ),
            "all_supported": all(
                result["hypotheses_supported"] for result in model_results
            ),
        }
        for model, model_results in by_model.items()
    }
    report["all_supported"] = bool(results) and all(
        result["hypotheses_supported"] for result in results
    )
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"report": str(output),
                      "all_supported": report["all_supported"],
                      "runs": len(results)}, indent=2))
    return 0 if report["all_supported"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
