"""Decision model and engine (SDK-005, RUNTIME-006).

Implements a minimal Decision object with the SDK-005 lifecycle:
    propose -> (approve/reject) -> authorize -> execute

Expiration is a validity condition and supersession is a relationship; neither
creates an additional Decision lifecycle state.

Authority is validated explicitly before a Decision becomes executable
(SDK-005 §34, RUNTIME-006 §73-74). Capability and authority are distinct:
a Decision may be technically possible yet not authorized.

The engine is additive and does not modify the benchmark execution path.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from .errors import (VIALAuthorizationError, VIALConflictError,
                     VIALStateError, VIALValidationError)

# SDK-005 canonical Decision lifecycle statuses
STATUS_DRAFT = "DRAFT"
STATUS_PENDING = "PENDING"
STATUS_AUTHORIZED = "AUTHORIZED"
STATUS_EXECUTING = "EXECUTING"
STATUS_COMPLETED = "COMPLETED"
STATUS_REJECTED = "REJECTED"
# Compatibility conditions; neither is a Decision lifecycle state.
STATUS_SUPERSEDED = "SUPERSEDED"
STATUS_EXPIRED = "EXPIRED"
STATUS_CANCELLED = "CANCELLED"
STATUS_REVOKED = "REVOKED"
STATUS_FAILED = "FAILED"

# Compatibility names for callers using the earlier prototype vocabulary.
STATUS_PROPOSED = STATUS_DRAFT
STATUS_APPROVED = STATUS_PENDING
STATUS_EXECUTED = STATUS_COMPLETED

_EXECUTABLE = {STATUS_AUTHORIZED, STATUS_EXECUTING}


@dataclass
class Authority:
    """Structured authority descriptor (SDK-005 §29)."""
    actor: str
    role: str = ""
    scope: str = "organization"
    policy: str = ""


@dataclass
class Decision:
    """A recorded, versioned organizational decision (SDK-005)."""
    id: str
    organization_id: str
    type: str
    objective: str
    actor: str
    authority: Authority
    context_id: str = ""
    context_version: int = 0
    context_fingerprint: str = ""
    execution_fingerprint: str = ""
    alternatives: list[Any] = field(default_factory=list)
    rationale: str = ""
    evidence: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    preconditions: list[str] = field(default_factory=list)
    postconditions: list[str] = field(default_factory=list)
    outcome: Any = None
    confidence: float = 1.0
    risk: str = ""
    priority: str = "normal"
    status: str = STATUS_DRAFT
    authorized_by: str = ""
    validity: str = "VALID"
    version: int = 1
    execution_refs: list[str] = field(default_factory=list)
    supersedes: str | None = None
    superseded_by: str | None = None
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    expires_at: float | None = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "type": self.type,
            "objective": self.objective,
            "context_id": self.context_id,
            "context_version": self.context_version,
            "context_fingerprint": self.context_fingerprint,
            "execution_fingerprint": self.execution_fingerprint,
            "actor": self.actor,
            "authority": {"actor": self.authority.actor,
                          "role": self.authority.role,
                          "scope": self.authority.scope,
                          "policy": self.authority.policy},
            "status": self.status,
            "authorized_by": self.authorized_by,
            "validity": self.validity,
            "version": self.version,
            "outcome": self.outcome,
            "confidence": self.confidence,
            "risk": self.risk,
            "priority": self.priority,
            "evidence": self.evidence,
            "supersedes": self.supersedes,
            "superseded_by": self.superseded_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "expires_at": self.expires_at,
        }


class DecisionEngine:
    """Owns Decisions for an Organization and enforces authority."""

    def __init__(self, organization_id: str, root_authority: str = "org-root"):
        self.organization_id = organization_id
        self.root_authority = root_authority
        self.decisions: dict[str, Decision] = {}

    def propose(self, objective: str, actor: str, authority: Authority,
                type: str = "operation", context_id: str = "",
                context_version: int = 0, context_fingerprint: str = "",
                execution_fingerprint: str = "",
                alternatives: list[Any] | None = None,
                rationale: str = "", evidence: list[str] | None = None,
                constraints: list[str] | None = None,
                confidence: float = 1.0, risk: str = "",
                priority: str = "normal",
                expires_at: float | None = None) -> Decision:
        """Record a proposed Decision (SDK-005 §51: create/propose)."""
        decision_id = f"DEC-{uuid.uuid4().hex[:12]}"
        decision = Decision(
            id=decision_id,
            organization_id=self.organization_id,
            type=type,
            objective=objective,
            actor=actor,
            authority=authority,
            context_id=context_id,
            context_version=context_version,
            context_fingerprint=context_fingerprint,
            execution_fingerprint=execution_fingerprint,
            alternatives=alternatives or [],
            rationale=rationale,
            evidence=evidence or [],
            constraints=constraints or [],
            confidence=confidence,
            risk=risk,
            priority=priority,
            expires_at=expires_at,
        )
        self.decisions[decision_id] = decision
        return decision

    def _require(self, decision_id: str) -> Decision:
        if decision_id not in self.decisions:
            raise VIALStateError(
                "DECISION_NOT_FOUND",
                f"unknown decision '{decision_id}'",
                details={"decision_id": decision_id})
        return self.decisions[decision_id]

    def _authorized(self, decision: Decision, actor: str) -> bool:
        """A decision is authorized when the acting authority matches the
        declared authority or the organizational root (SDK-005 §34)."""
        return actor in (decision.authority.actor, self.root_authority)

    def approve(self, decision_id: str, actor: str) -> Decision:
        """Approve a proposed decision (SDK-005 lifecycle)."""
        d = self._require(decision_id)
        if d.status != STATUS_DRAFT:
            raise VIALConflictError(
                "DECISION_NOT_PROPOSED",
                f"decision '{decision_id}' is {d.status}, not proposed",
                details={"decision_id": decision_id, "status": d.status})
        d.status = STATUS_PENDING
        d.updated_at = time.time()
        return d

    def reject(self, decision_id: str, actor: str) -> Decision:
        d = self._require(decision_id)
        if d.status not in (STATUS_DRAFT, STATUS_PENDING):
            raise VIALConflictError(
                "DECISION_NOT_REJECTABLE",
                f"decision '{decision_id}' is {d.status}",
                details={"decision_id": decision_id, "status": d.status})
        d.status = STATUS_REJECTED
        d.updated_at = time.time()
        return d

    def authorize(self, decision_id: str, actor: str) -> Decision:
        """Authorize an approved decision, validating authority (SDK-005 §34,
        RUNTIME-006 §73-74)."""
        d = self._require(decision_id)
        if not self._authorized(d, actor):
            raise VIALAuthorizationError(
                "DECISION_UNAUTHORIZED",
                f"actor '{actor}' lacks authority to authorize decision "
                f"'{decision_id}'",
                details={"decision_id": decision_id,
                         "required_authority": d.authority.actor})
        if d.status != STATUS_PENDING:
            raise VIALConflictError(
                "DECISION_NOT_APPROVED",
                f"decision '{decision_id}' is {d.status}, not approved",
                details={"decision_id": decision_id, "status": d.status})
        d.status = STATUS_AUTHORIZED
        d.authorized_by = actor
        d.updated_at = time.time()
        return d

    def execute(self, decision_id: str, actor: str, outcome: Any = None) -> Decision:
        """Mark an authorized decision as executed (SDK-005 lifecycle)."""
        d = self._require(decision_id)
        if not self._authorized(d, actor):
            raise VIALAuthorizationError(
                "DECISION_UNAUTHORIZED",
                f"actor '{actor}' lacks authority to execute decision "
                f"'{decision_id}'",
                details={"decision_id": decision_id})
        if d.status != STATUS_AUTHORIZED:
            raise VIALConflictError(
                "DECISION_NOT_AUTHORIZED",
                f"decision '{decision_id}' is {d.status}, not authorized",
                details={"decision_id": decision_id, "status": d.status})
        d.outcome = outcome
        d.status = STATUS_EXECUTING
        d.status = STATUS_COMPLETED
        d.updated_at = time.time()
        return d

    def supersede(self, decision_id: str, successor: Decision, actor: str) -> Decision:
        d = self._require(decision_id)
        if not self._authorized(d, actor):
            raise VIALAuthorizationError(
                "DECISION_UNAUTHORIZED",
                f"actor '{actor}' lacks authority to supersede '{decision_id}'",
                details={"decision_id": decision_id})
        d.superseded_by = successor.id
        successor.supersedes = decision_id
        successor.updated_at = time.time()
        return d

    def expire(self, decision_id: str) -> Decision:
        d = self._require(decision_id)
        if d.expires_at is not None and time.time() > d.expires_at:
            d.validity = STATUS_EXPIRED
            d.updated_at = time.time()
        return d

    def cancel(self, decision_id: str, actor: str) -> Decision:
        d = self._require(decision_id)
        if not self._authorized(d, actor):
            raise VIALAuthorizationError(
                "DECISION_UNAUTHORIZED",
                f"actor '{actor}' lacks authority to cancel '{decision_id}'",
                details={"decision_id": decision_id})
        d.status = STATUS_CANCELLED
        d.updated_at = time.time()
        return d

    def revoke(self, decision_id: str, actor: str) -> Decision:
        """Revoke an authorized decision, preventing execution (SDK-005 §44,
        RUNTIME-002 §31)."""
        d = self._require(decision_id)
        if not self._authorized(d, actor):
            raise VIALAuthorizationError(
                "DECISION_UNAUTHORIZED",
                f"actor '{actor}' lacks authority to revoke '{decision_id}'",
                details={"decision_id": decision_id})
        if d.status != STATUS_AUTHORIZED:
            raise VIALConflictError(
                "DECISION_NOT_REVOCABLE",
                f"decision '{decision_id}' is {d.status}, not revocable",
                details={"decision_id": decision_id, "status": d.status})
        d.status = STATUS_REVOKED
        d.updated_at = time.time()
        return d

    def get(self, decision_id: str) -> Decision:
        return self._require(decision_id)

    def history(self, organization_id: str | None = None) -> list[Decision]:
        org = organization_id or self.organization_id
        return [d for d in self.decisions.values()
                if d.organization_id == org]
