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
        """Record intent BEFORE any mutation (RFC-009 §2.3.2)."""
        if operation_id in self.intents:
            raise ValueError(f"operation_id {operation_id} already started")
        intent = Intent(
            operation_id=operation_id,
            key=key,
            value=value,
            actor=actor,
            previous_version=self.org.version,
        )
        self.intents[operation_id] = intent
        return intent

    def commit(self, operation_id: str) -> Intent:
        """Atomically apply a committed intent (RFC-003 §17, §34)."""
        intent = self.intents[operation_id]
        if intent.status == COMMITTED:
            # retry of an already-committed operation: do NOT re-apply
            self.duplicate_commits += 1
            return intent
        if intent.status == ABORTED:
            raise ValueError(f"operation {operation_id} was aborted")
        # atomic: field value and version change together
        self.org.fields[intent.key].value = intent.value
        prev = self.org.version
        self.org.version += 1
        self.org.transitions.append(self._transition_record(intent, prev))
        intent.resulting_version = self.org.version
        intent.status = COMMITTED
        return intent

    def abort(self, operation_id: str) -> Intent:
        """Abort a pending intent; State remains authoritative (RFC-003 §34)."""
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
            previous_version=previous_version,
            resulting_version=intent.resulting_version or 0,
            operation="commit",
            authority=intent.actor,
            provenance=f"intent:{intent.operation_id}",
            timestamp=time.time(),
        )

    def snapshot(self) -> dict:
        """Current authoritative State snapshot for comparison (RFC-009 §2.4)."""
        return {
            "version": self.org.version,
            "fields": {k: f.value for k, f in self.org.fields.items()},
            "transitions": len(self.org.transitions),
        }
