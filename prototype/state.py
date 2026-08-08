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

from .errors import (VIALAuthorizationError, VIALConflictError,
                     VIALStateError, VIALValidationError)


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
    """An authorized, atomic state transition (RFC-003 §11, §17, §52)."""
    transition_id: str
    organization: str
    previous_version: int
    resulting_version: int
    operation: str
    authority: str
    provenance: str
    timestamp: float


class Organization:
    """A minimal Organization owning persistent State (RFC-003 §4).

    Two independent versions are tracked (SDK-002 §34):
    - `config_version`: configuration/structural version, incremented when the
      Organization's structure changes (fields added/removed);
    - `state_version`: State version, incremented on each authorized State
      transition (RFC-003 §11, §17).
    """

    def __init__(self, org_id: str, authority: str = "org-root"):
        self.org_id = org_id
        self.authority = authority
        self.config_version = 0
        self.state_version = 0
        self.fields: dict[str, StateField] = {}
        self.transitions: list[StateTransition] = []

    def add_field(self, key: str, value: Any, relevance: list[str],
                  authority: str | None = None) -> None:
        actor = authority or self.authority
        if key in self.fields:
            raise VIALConflictError(
                "FIELD_EXISTS",
                f"state field '{key}' already exists",
                details={"key": key})
        self.fields[key] = StateField(key, value, list(relevance), actor)
        # structural change: increments config_version only (SDK-002 §34);
        # no State transition is recorded.
        self.config_version += 1

    def transition(self, key: str, value: Any, actor: str,
                   operation: str, provenance: str) -> StateTransition:
        """Authorized atomic transition (RFC-003 §17, §31)."""
        if actor != self.authority:
            raise VIALAuthorizationError(
                "STATE_UNAUTHORIZED",
                f"actor '{actor}' lacks authority to transition state",
                details={"actor": actor, "required_authority": self.authority})
        if key not in self.fields:
            raise VIALStateError(
                "FIELD_NOT_FOUND",
                f"unknown state field '{key}'",
                details={"key": key})
        prev = self.state_version
        self.fields[key].value = value
        return self._commit(operation, actor, provenance)

    def _commit(self, operation: str, actor: str, provenance: str) -> StateTransition:
        prev = self.state_version
        self.state_version += 1
        t = StateTransition(
            transition_id=str(uuid.uuid4()),
            organization=self.org_id,
            previous_version=prev,
            resulting_version=self.state_version,
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
            "config_version": self.config_version,
            "state_version": self.state_version,
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
