"""Decision model and engine (SDK-005, RUNTIME-006).

Implements a minimal Decision object with the SDK-005 lifecycle:
    propose -> (approve/reject) -> authorize -> (execute/supersede/expire)

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

# SDK-005 decision lifecycle statuses
STATUS_PROPOSED = "proposed"
STATUS_APPROVED = "approved"
STATUS_REJECTED = "rejected"
STATUS_AUTHORIZED = "authorized"
STATUS_EXECUTED = "executed"
STATUS_SUPERSEDED = "superseded"
STATUS_EXPIRED = "expired"
STATUS_CANCELLED = "cancelled"

_EXECUTABLE = {STATUS_AUTHORIZED, STATUS_EXECUTED}


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
    status: str = STATUS_PROPOSED
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
            "actor": self.actor,
            "authority": {"actor": self.authority.actor,
                          "role": self.authority.role,
                          "scope": self.authority.scope,
                          "policy": self.authority.policy},
            "status": self.status,
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
                context_version: int = 0, alternatives: list[Any] | None = None,
                rationale: str = "", evidence: list[str] | None = None,
                constraints: list[str] | None = None,
                confidence: float = 1.0, risk: str = "",
                priority: str = "normal") -> Decision:
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
            alternatives=alternatives or [],
            rationale=rationale,
            evidence=evidence or [],
            constraints=constraints or [],
            confidence=confidence,
            risk=risk,
            priority=priority,
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
        if d.status != STATUS_PROPOSED:
            raise VIALConflictError(
                "DECISION_NOT_PROPOSED",
                f"decision '{decision_id}' is {d.status}, not proposed",
                details={"decision_id": decision_id, "status": d.status})
        d.status = STATUS_APPROVED
        d.updated_at = time.time()
        return d

    def reject(self, decision_id: str, actor: str) -> Decision:
        d = self._require(decision_id)
        if d.status not in (STATUS_PROPOSED, STATUS_APPROVED):
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
        if d.status not in (STATUS_APPROVED, STATUS_PROPOSED):
            raise VIALConflictError(
                "DECISION_NOT_APPROVED",
                f"decision '{decision_id}' is {d.status}, not approved",
                details={"decision_id": decision_id, "status": d.status})
        d.status = STATUS_AUTHORIZED
        d.updated_at = time.time()
        return d

    def execute(self, decision_id: str, actor: str, outcome: Any = None) -> Decision:
        """Mark an authorized decision as executed (SDK-005 lifecycle)."""
        d = self._require(decision_id)
        if d.status != STATUS_AUTHORIZED:
            raise VIALConflictError(
                "DECISION_NOT_AUTHORIZED",
                f"decision '{decision_id}' is {d.status}, not authorized",
                details={"decision_id": decision_id, "status": d.status})
        d.outcome = outcome
        d.status = STATUS_EXECUTED
        d.updated_at = time.time()
        return d

    def supersede(self, decision_id: str, successor: Decision, actor: str) -> Decision:
        d = self._require(decision_id)
        if not self._authorized(d, actor):
            raise VIALAuthorizationError(
                "DECISION_UNAUTHORIZED",
                f"actor '{actor}' lacks authority to supersede '{decision_id}'",
                details={"decision_id": decision_id})
        d.status = STATUS_SUPERSEDED
        d.superseded_by = successor.id
        successor.supersedes = decision_id
        successor.updated_at = time.time()
        return d

    def expire(self, decision_id: str) -> Decision:
        d = self._require(decision_id)
        if d.expires_at is not None and time.time() > d.expires_at:
            d.status = STATUS_EXPIRED
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

    def get(self, decision_id: str) -> Decision:
        return self._require(decision_id)

    def history(self, organization_id: str | None = None) -> list[Decision]:
        org = organization_id or self.organization_id
        return [d for d in self.decisions.values()
                if d.organization_id == org]
