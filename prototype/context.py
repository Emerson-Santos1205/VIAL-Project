"""Context Builder - Full vs Selective projection (RFC-004, RFC-007 §2.2)."""
from __future__ import annotations

import json
from dataclasses import dataclass, field

from .state import Organization
from .tokenizer import count_tokens


@dataclass
class Task:
    """A unit of work with its deterministic relevance descriptor."""
    id: str
    prompt: str
    required: list[str]
    expected: object
    op: str
    args: object = None


@dataclass
class Context:
    """A derived execution artifact (RFC-004 §5). Carries lineage."""
    task_id: str
    body: str
    mode: str
    state_version: int
    tokens: int
    references: list[str] = field(default_factory=list)

    def to_row(self) -> dict:
        return {
            "task_id": self.task_id,
            "mode": self.mode,
            "state_version": self.state_version,
            "tokens": self.tokens,
            "references": self.references,
        }


class ContextBuilder:
    """Builds either Full Context or Selective Context for a task."""

    def __init__(self, org: Organization):
        self.org = org

    def build_full(self, task: Task) -> Context:
        body = json.dumps({
            "task": task.prompt,
            "state": json.loads(self.org.serialize_full()),
        }, sort_keys=True)
        return Context(
            task_id=task.id,
            body=body,
            mode="full",
            state_version=self.org.version,
            tokens=count_tokens(body),
        )

    def build_selective(self, task: Task) -> Context:
        selected = self.org.select_fields(task.required)
        body = json.dumps({
            "task": task.prompt,
            "state": {
                "org": self.org.org_id,
                "version": self.org.version,
                "fields": {
                    k: {"value": f.value}
                    for k, f in sorted(selected.items())
                },
            },
            "references": [f"state:{k}" for k in sorted(selected)],
        }, sort_keys=True)
        return Context(
            task_id=task.id,
            body=body,
            mode="selective",
            state_version=self.org.version,
            tokens=count_tokens(body),
            references=[f"state:{k}" for k in sorted(selected)],
        )
