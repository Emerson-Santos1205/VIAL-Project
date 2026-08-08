"""Context Builder - Full vs Selective projection (RFC-004, RFC-007 §2.2,
SDK-004)."""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field

from .state import Organization
from .tokenizer import count_tokens

# SDK-004 §17/§38 context status values
CTX_VALID = "VALID"
CTX_STALE = "STALE"
CTX_EXPIRED = "EXPIRED"
CTX_INVALIDATED = "INVALIDATED"


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
    """A derived execution artifact (RFC-004 §5, SDK-004 §38). Carries lineage,
    the Organization to which it belongs (SDK-004 §7), its own Context identity
    (SDK-004 §6, §38) and lifecycle status (SDK-004 §17)."""
    task_id: str
    organization_id: str
    body: str
    mode: str
    state_version: int
    tokens: int
    references: list[str] = field(default_factory=list)
    context_id: str = field(default_factory=lambda: f"CTX-{uuid.uuid4().hex[:12]}")
    objective: str = ""
    scope: str = ""
    status: str = CTX_VALID
    version: int = 1
    created_at: float = field(default_factory=time.time)

    def to_row(self) -> dict:
        return {
            "context_id": self.context_id,
            "task_id": self.task_id,
            "organization_id": self.organization_id,
            "mode": self.mode,
            "state_version": self.state_version,
            "version": self.version,
            "status": self.status,
            "objective": self.objective,
            "scope": self.scope,
            "tokens": self.tokens,
            "references": self.references,
        }

    def invalidate(self) -> "Context":
        """Mark this Context as invalidated (SDK-004 §23-24, §68)."""
        self.status = CTX_INVALIDATED
        return self

    def refresh(self) -> "Context":
        """Derive a new valid Context version from this one (SDK-004 §68)."""
        import copy
        new = copy.copy(self)
        new.version += 1
        new.status = CTX_VALID
        new.created_at = time.time()
        return new


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
            organization_id=self.org.org_id,
            body=body,
            mode="full",
            state_version=self.org.state_version,
            tokens=count_tokens(body),
            objective=task.prompt,
            scope="organization",
        )

    def build_selective(self, task: Task) -> Context:
        selected = self.org.select_fields(task.required)
        body = json.dumps({
            "task": task.prompt,
            "state": {
                "org": self.org.org_id,
                "config_version": self.org.config_version,
                "state_version": self.org.state_version,
                "fields": {
                    k: {"value": f.value}
                    for k, f in sorted(selected.items())
                },
            },
            "references": [f"state:{k}" for k in sorted(selected)],
        }, sort_keys=True)
        return Context(
            task_id=task.id,
            organization_id=self.org.org_id,
            body=body,
            mode="selective",
            state_version=self.org.state_version,
            tokens=count_tokens(body),
            references=[f"state:{k}" for k in sorted(selected)],
            objective=task.prompt,
            scope="selective",
        )
