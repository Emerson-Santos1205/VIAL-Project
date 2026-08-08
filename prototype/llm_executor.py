"""LLM executor for RFC-007 real-model validation (RFC-007 §2.2).

Sends the constructed Context to a real model via an OpenAI-compatible chat
completions API and evaluates the answer against the expected result.

Environment:
    VIAL_LLM_BASE_URL  default https://api.openai.com/v1
    VIAL_LLM_API_KEY   required
    VIAL_LLM_MODEL     default gpt-4o-mini

The executor is provider-agnostic (any OpenAI-compatible endpoint).
"""
from __future__ import annotations

import json
import os

import httpx

from .context import Context, Task
from .errors import wrap_network_error

# RUNTIME-002 §37 outcome status values
OUTCOME_SUCCESS = "SUCCESS"
OUTCOME_FAILED = "FAILED"
OUTCOME_UNKNOWN = "UNKNOWN"


class LLMExecutor:
    """Executes tasks by asking a real model to answer based on the context."""

    def __init__(self, base_url: str | None = None, api_key: str | None = None,
                 model: str | None = None, timeout: float = 60.0):
        self.base_url = (base_url or os.environ.get("VIAL_LLM_BASE_URL")
                         or "https://api.openai.com/v1")
        self.api_key = api_key or os.environ.get("VIAL_LLM_API_KEY")
        self.model = model or os.environ.get("VIAL_LLM_MODEL", "gpt-4o-mini")
        self.timeout = timeout
        if not self.api_key:
            raise RuntimeError(
                "VIAL_LLM_API_KEY not set. Set it before running the real-model benchmark.")

    def execute(self, ctx: Context, task: Task) -> dict:
        system = ("You are an execution resource in a cognitive organization. "
                  "Answer the task using ONLY the information provided. "
                  "Respond with a single JSON object: {\"answer\": <boolean true/false>} "
                  "and nothing else.")
        user = (
            "TASK:\n" + task.prompt +
            "\n\nCONTEXT PROVIDED:\n" + ctx.body
        )
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.0,
            "response_format": {"type": "json_object"},
        }
        resp = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=body,
            timeout=self.timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        try:
            parsed = json.loads(content)
            answer = bool(parsed["answer"])
        except Exception:
            answer = None
        usage = data.get("usage", {})
        return {
            "task_id": task.id,
            "mode": ctx.mode,
            "outcome": answer,
            "status": OUTCOME_SUCCESS if answer is not None else OUTCOME_UNKNOWN,
            "prompt_tokens": usage.get("prompt_tokens"),
            "completion_tokens": usage.get("completion_tokens"),
            "raw": content,
        }


class LLMEvaluator:
    """Scores LLM outcomes: exact match against expected (0.0/1.0).

    UNKNOWN outcomes are scored 0.0 for benchmark compatibility, but remain
    distinguishable from FAILED via the row's `status` (RUNTIME-002 §37, §42:
    unknown is not failure)."""

    def score(self, row: dict, task: Task) -> float:
        if row.get("status") == OUTCOME_UNKNOWN or row["outcome"] is None:
            return 0.0
        return 1.0 if row["outcome"] == bool(task.expected) else 0.0
