"""opencode CLI executor for RFC-007 real-model validation.

Runs `opencode run --format json` as a subprocess and parses the JSON event
stream. Extracts the model text (from `type:text` parts) and token counts
(from `type:step_finish`).

Environment:
    OPENCODE_MODEL     provider/model (e.g. opencode/deepseek-v4-flash-free)
                       default: opencode/deepseek-v4-flash-free
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

from .context import Context, Task
from .errors import wrap_network_error

# RUNTIME-002 §37 outcome status values
OUTCOME_SUCCESS = "SUCCESS"
OUTCOME_FAILED = "FAILED"
OUTCOME_UNKNOWN = "UNKNOWN"

DEFAULT_MODEL = "opencode/deepseek-v4-flash-free"

_NPM_EXE = (r"C:\Users\Emerson\AppData\Roaming\npm\node_modules\opencode-ai\bin\opencode.exe")


def _opencode_command() -> str:
    """Return an executable path for the opencode CLI.

    Prefers the npm-installed .exe; falls back to `opencode` on PATH.
    """
    if os.path.isfile(_NPM_EXE):
        return _NPM_EXE
    return "opencode"


class OpencodeExecutor:
    """Executes tasks by invoking the opencode CLI with the context."""

    def __init__(self, model: str | None = None, timeout: float = 180.0,
                 command: str | None = None):
        self.model = model or os.environ.get("OPENCODE_MODEL", DEFAULT_MODEL)
        self.timeout = timeout
        self.command = command or _opencode_command()

    def execute(self, ctx: Context, task: Task) -> dict:
        system = ("You are an execution resource in a cognitive organization. "
                  "Answer the task using ONLY the information provided. "
                  "Respond with a single JSON object: {\"answer\": <true|false>} "
                  "and nothing else.")
        prompt = (
            system + "\n\nTASK:\n" + task.prompt +
            "\n\nCONTEXT PROVIDED:\n" + ctx.body
        )
        cmd = [
            self.command, "run", "--format", "json",
            "--model", self.model, prompt,
        ]
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=self.timeout,
                encoding="utf-8", errors="replace",
            )
        except subprocess.TimeoutExpired as exc:
            raise wrap_network_error(
                exc, f"opencode timed out after {self.timeout}s",
                details={"model": self.model})
        except OSError as exc:
            raise wrap_network_error(
                exc, f"failed to start opencode CLI: {exc}",
                details={"command": self.command})
        events = [json.loads(l) for l in proc.stdout.splitlines() if l.strip()]

        text = ""
        tokens = {}
        for ev in events:
            if ev.get("type") == "text":
                text += ev.get("part", {}).get("text", "")
            if ev.get("type") == "step_finish":
                tokens = ev.get("part", {}).get("tokens", {}) or {}

        answer = self._parse_answer(text)
        return {
            "task_id": task.id,
            "mode": ctx.mode,
            "outcome": answer,
            "status": OUTCOME_SUCCESS if answer is not None else OUTCOME_UNKNOWN,
            "prompt_tokens": tokens.get("input"),
            "completion_tokens": tokens.get("output"),
            "total_tokens": tokens.get("total"),
            "reasoning_tokens": tokens.get("reasoning"),
            "raw": text.strip(),
        }

    @staticmethod
    def _parse_answer(text: str) -> bool | None:
        m = re.search(r'"(answer)"\s*:\s*(true|false)', text, re.IGNORECASE)
        if m:
            return m.group(2).lower() == "true"
        if re.search(r"^(true|false)\b", text.strip(), re.IGNORECASE):
            return text.strip().lower().startswith("true")
        return None


class OpencodeEvaluator:
    """Scores opencode outcomes: exact match against expected (0.0/1.0).

    UNKNOWN outcomes are scored 0.0 for benchmark compatibility, but remain
    distinguishable from FAILED via the row's `status` (RUNTIME-002 §37, §42).
    """

    def score(self, row: dict, task: Task) -> float:
        if row.get("status") == OUTCOME_UNKNOWN or row["outcome"] is None:
            return 0.0
        return 1.0 if row["outcome"] == bool(task.expected) else 0.0
