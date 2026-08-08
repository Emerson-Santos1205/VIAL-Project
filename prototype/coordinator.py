"""State Coordinator for RFC-009 - Failure & Recovery.

Implements RFC-003 §17/§34/§35/§58 and RFC-009 §2.3:
- records operation intent before mutating State;
- applies transitions atomically (version + value together);
- resolves interrupted operations from the log;
- never commits the same operation_id twice (idempotency).
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from .errors import (VIALAuthorizationError, VIALConflictError,
                     VIALStateError, VIALValidationError)
from .state import Organization

PENDING = "pending"
COMMITTED = "committed"
ABORTED = "aborted"


@dataclass
class Intent:
    """A recorded operation intent (RFC-009 §2.3.2)."""
    operation_id: str
    key: str
    value: Any
    actor: str
    previous_version: int
    status: str = PENDING
    resulting_version: int | None = None
    created_at: float = field(default_factory=time.time)


class CoordinatorFailure(Exception):
    """Raised when an executor 'fails' during an operation. Modeled as a
    deterministic interruption point, not an OS crash."""


class StateCoordinator:
    """Owns transitions for an Organization, with intent logging + recovery."""

    def __init__(self, org: Organization):
        self.org = org
        self.intents: dict[str, Intent] = {}
        self.duplicate_commits = 0
        self.interruptions = 0

    def begin(self, operation_id: str, key: str, value: Any, actor: str) -> Intent:
        """Record intent BEFORE any mutation (RFC-009 §2.3.2).

        Authority is validated against the Organization's authority
        (SDK-002 §50, §56): only the Organization authority may begin a
        State transition.
        """
        if operation_id in self.intents:
            raise VIALConflictError(
                "OPERATION_ALREADY_STARTED",
                f"operation_id {operation_id} already started",
                details={"operation_id": operation_id})
        if actor != self.org.authority:
            raise VIALAuthorizationError(
                "STATE_UNAUTHORIZED",
                f"actor '{actor}' lacks authority to begin operation",
                details={"actor": actor, "required_authority": self.org.authority})
        if key not in self.org.fields:
            raise VIALStateError(
                "FIELD_NOT_FOUND",
                f"unknown state field '{key}'",
                details={"key": key})
        intent = Intent(
            operation_id=operation_id,
            key=key,
            value=value,
            actor=actor,
            previous_version=self.org.state_version,
        )
        self.intents[operation_id] = intent
        return intent

    def commit(self, operation_id: str) -> Intent:
        """Atomically apply a committed intent (RFC-003 §17, §34)."""
        if operation_id not in self.intents:
            raise VIALStateError(
                "INTENT_NOT_FOUND",
                f"no intent recorded for operation {operation_id}",
                details={"operation_id": operation_id})
        intent = self.intents[operation_id]
        if intent.status == COMMITTED:
            # retry of an already-committed operation: do NOT re-apply
            self.duplicate_commits += 1
            return intent
        if intent.status == ABORTED:
            raise VIALValidationError(
                "OPERATION_ABORTED",
                f"operation {operation_id} was aborted",
                details={"operation_id": operation_id})
        # optimistic concurrency: the State version must not have advanced since
        # the intent was recorded (RUNTIME-003 §25-26). Detects conflicting
        # concurrent transitions before applying.
        if intent.previous_version != self.org.state_version:
            raise VIALConflictError(
                "STATE_VERSION_CONFLICT",
                f"State advanced since intent {operation_id} was recorded",
                details={"operation_id": operation_id,
                         "expected": intent.previous_version,
                         "actual": self.org.state_version})
        # atomic: field value and version change together
        self.org.fields[intent.key].value = intent.value
        prev = self.org.state_version
        self.org.state_version += 1
        self.org.transitions.append(self._transition_record(intent, prev))
        intent.resulting_version = self.org.state_version
        intent.status = COMMITTED
        return intent

    def abort(self, operation_id: str) -> Intent:
        """Abort a pending intent; State remains authoritative (RFC-003 §34)."""
        if operation_id not in self.intents:
            raise VIALStateError(
                "INTENT_NOT_FOUND",
                f"no intent recorded for operation {operation_id}",
                details={"operation_id": operation_id})
        intent = self.intents[operation_id]
        if intent.status == PENDING:
            intent.status = ABORTED
        return intent

    def resolve(self, operation_id: str) -> Intent | None:
        """Resolve an operation's outcome from the log alone (RFC-003 §58)."""
        return self.intents.get(operation_id)

    def _transition_record(self, intent: Intent, previous_version: int):
        from .state import StateTransition
        return StateTransition(
            transition_id=intent.operation_id,
            organization=self.org.org_id,
            previous_version=previous_version,
            resulting_version=intent.resulting_version or 0,
            operation="commit",
            authority=intent.actor,
            provenance=f"intent:{intent.operation_id}",
            timestamp=time.time(),
        )

    def snapshot(self) -> dict:
        """Current authoritative State snapshot for comparison (RFC-009 §2.4).

        `version` (State version) is kept for benchmark compatibility
        (RFC-009 hypothesis uses State version equality).
        """
        return {
            "version": self.org.state_version,
            "state_version": self.org.state_version,
            "config_version": self.org.config_version,
            "fields": {k: f.value for k, f in self.org.fields.items()},
            "transitions": len(self.org.transitions),
        }
