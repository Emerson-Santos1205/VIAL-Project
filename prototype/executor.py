"""Deterministic executor and evaluator (RFC-007 §2.2).

Executes tasks deterministically against the state present in the context.
If a required field is absent from the context, the task fails (quality 0).
"""
from __future__ import annotations

import json
from dataclasses import dataclass

from .context import Context, Task
from .errors import VIALValidationError


@dataclass
class ExecutionResult:
    task_id: str
    mode: str
    outcome: object
    correct: bool
    quality: float


class DeterministicExecutor:
    """Executes a task against the state projection inside its Context.

    Supports: numeric range checks (`value in [lo, hi]`) and boolean checks.
    This is a baseline executor per RFC-007 §6 (Alternatives); it does not
    require an LLM and is fully reproducible.
    """

    def execute(self, ctx: Context, task: Task) -> ExecutionResult:
        payload = json.loads(ctx.body)
        fields = payload["state"]["fields"]
        return self._eval(task, fields, ctx.mode)

    def _eval(self, task: Task, fields: dict, mode: str) -> ExecutionResult:
        # task.op encodes the required field and check type.
        if task.op == "range":
            key, lo, hi = task.args
            if key not in fields:
                return ExecutionResult(task.id, mode, None, False, 0.0)
            v = fields[key]["value"]
            ok = lo <= v <= hi
            return ExecutionResult(task.id, mode, ok, ok == task.expected, 1.0 if ok == task.expected else 0.0)
        if task.op == "bool":
            key = task.args[0]
            if key not in fields:
                return ExecutionResult(task.id, mode, None, False, 0.0)
            v = bool(fields[key]["value"])
            return ExecutionResult(task.id, mode, v, v == task.expected, 1.0 if v == task.expected else 0.0)
        raise VIALValidationError(
            "UNKNOWN_OPERATION",
            f"unknown op {task.op}",
            details={"op": task.op})


class Evaluator:
    """Scores quality in [0.0, 1.0] using the same rubric for both modes."""

    def score(self, result: ExecutionResult) -> float:
        return result.quality
