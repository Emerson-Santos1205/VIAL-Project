"""Minimal Organizational Cognitive State (OCS) - RFC-003 minimal contract.

Implements the Minimal State Contract from RFC-003 §53:
    Organization Identity
    Current State
    State Version
    Transition Mechanism
    Authority Boundary
    State Validity
"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class StateField:
    """A single authoritative state field with its relevance descriptor.

    `relevance` is the deterministic descriptor used by the Context Builder
    (RFC-007 §2.3). It is fixed at model time and never changes during a run.
    """
    key: str
    value: Any
    relevance: list[str]
    authority: str = "admin"


@dataclass
class StateTransition:
    """An authorized, atomic state transition (RFC-003 §11, §17)."""
    transition_id: str
    previous_version: int
    resulting_version: int
    operation: str
    authority: str
    provenance: str
    timestamp: float


class Organization:
    """A minimal Organization owning persistent State (RFC-003 §4)."""

    def __init__(self, org_id: str, authority: str = "org-root"):
        self.org_id = org_id
        self.authority = authority
        self.version = 0
        self.fields: dict[str, StateField] = {}
        self.transitions: list[StateTransition] = []

    def add_field(self, key: str, value: Any, relevance: list[str],
                  authority: str | None = None) -> None:
        actor = authority or self.authority
        self.fields[key] = StateField(key, value, list(relevance), actor)
        self._commit(f"add_field:{key}", actor, "add-field")

    def transition(self, key: str, value: Any, actor: str,
                   operation: str, provenance: str) -> StateTransition:
        """Authorized atomic transition (RFC-003 §17, §31)."""
        if actor != self.authority:
            raise PermissionError(
                f"actor '{actor}' lacks authority to transition state")
        if key not in self.fields:
            raise KeyError(f"unknown state field '{key}'")
        prev = self.version
        self.fields[key].value = value
        return self._commit(operation, actor, provenance)

    def _commit(self, operation: str, actor: str, provenance: str) -> StateTransition:
        prev = self.version
        self.version += 1
        t = StateTransition(
            transition_id=str(uuid.uuid4()),
            previous_version=prev,
            resulting_version=self.version,
            operation=operation,
            authority=actor,
            provenance=provenance,
            timestamp=time.time(),
        )
        self.transitions.append(t)
        return t

    def get(self, key: str) -> StateField:
        return self.fields[key]

    def serialize_full(self) -> str:
        """Complete serialized State (Full Context source, RFC-007 §2.2)."""
        body = {
            "org": self.org_id,
            "version": self.version,
            "fields": {
                k: {"value": f.value, "relevance": f.relevance}
                for k, f in sorted(self.fields.items())
            },
        }
        return json.dumps(body, sort_keys=True)

    def select_fields(self, required: list[str]) -> dict[str, StateField]:
        """Selective projection: only fields whose relevance descriptor
        intersects the task's required domains (RFC-007 §2.3, RFC-003 §31)."""
        wanted = set(required)
        return {
            k: f
            for k, f in self.fields.items()
            if wanted & set(f.relevance)
        }
