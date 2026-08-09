"""Real-model code generation benchmark using the opencode CLI."""
from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE))

from prototype.opencode_executor import DEFAULT_MODEL, _opencode_command
from prototype.tokenizer import count_tokens


def load_workload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_code(text: str) -> str | None:
    match = re.search(r"```(?:python)?\s*(.*?)```", text, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else None


def generate(model: str, prompt: str, timeout: float) -> tuple[str | None, dict]:
    instruction = (
        "Return only Python source for solution.py inside one python code fence. "
        "Do not include explanations.\n\n" + prompt
    )
    proc = subprocess.run(
        [_opencode_command(), "run", "--format", "json", "--model", model, instruction],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=timeout,
    )
    text_parts = []
    tokens = {}
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "text":
            text_parts.append(event.get("part", {}).get("text", ""))
        elif event.get("type") == "step_finish":
            tokens = event.get("part", {}).get("tokens", {}) or {}
    raw = "".join(text_parts)
    return extract_code(raw), {
        "returncode": proc.returncode,
        "prompt_tokens": tokens.get("input"),
        "completion_tokens": tokens.get("output"),
        "total_tokens": tokens.get("total"),
        "raw_length": len(raw),
    }


def validate(code: str | None, tests: str) -> tuple[bool, str]:
    if not code:
        return False, "model did not return a Python code fence"
    with tempfile.TemporaryDirectory(prefix="vial-codegen-") as directory:
        root = Path(directory)
        (root / "solution.py").write_text(code + "\n", encoding="utf-8")
        (root / "test_solution.py").write_text(tests, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "-q", "test_solution.py"],
            cwd=root, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=30,
        )
        detail = (result.stdout + result.stderr).strip()[-1000:]
        return result.returncode == 0, detail


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--workload", default="workload.json")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--timeout", type=float, default=180.0)
    parser.add_argument("--out", default="results")
    args = parser.parse_args()

    base = Path(__file__).resolve().parent
    workload = load_workload(base / args.workload)
    tasks = workload["tasks"][:args.limit or None]
    rows = []
    started = time.monotonic()
    for task in tasks:
        for mode in ("full", "selective"):
            context = task[f"{mode}_context"]
            code, usage = generate(args.model, context, args.timeout)
            passed, detail = validate(code, task["tests"])
            rows.append({
                "task_id": task["id"], "mode": mode,
                "context_tokens": count_tokens(context),
                "tests_passed": passed, "validation": detail,
                **usage,
            })
    elapsed = time.monotonic() - started
    full = [row for row in rows if row["mode"] == "full"]
    selective = [row for row in rows if row["mode"] == "selective"]
    summary = lambda group: {
        "tasks": len(group),
        "tests_passed": sum(row["tests_passed"] for row in group),
        "quality": sum(row["tests_passed"] for row in group) / len(group) if group else 0,
        "context_tokens": sum(row["context_tokens"] for row in group),
        "model_tokens": sum(row.get("total_tokens") or 0 for row in group),
    }
    report = {
        "benchmark": workload["name"], "model": args.model,
        "environment": {"python": platform.python_version(), "opencode": "cli"},
        "full_context": summary(full), "selective_context": summary(selective),
        "elapsed_s": round(elapsed, 2), "per_task": rows,
    }
    output = base / args.out / f"codegen-{time.strftime('%Y%m%d-%H%M%S')}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"report": str(output), **{
        key: report[key] for key in ("full_context", "selective_context", "elapsed_s")
    }}, indent=2))
    return 0 if report["selective_context"]["quality"] >= 0.9 else 1


if __name__ == "__main__":
    raise SystemExit(main())
