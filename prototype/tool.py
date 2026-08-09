"""Tool model and invocation envelope (TOOLS-001).

Implements the TOOLS-001 Tool abstraction:
- Tool identity and metadata (TOOLS-001 §86: ToolID, Name, Description,
  Version, Capability, Owner, Status, Risk, Side Effects);
- Contract (TOOLS-001 §14): Identity, Description, Inputs, Outputs, Errors;
- ToolResult with explicit status (TOOLS-001 §17-18);
- invoke() returns a ToolResult (TOOLS-001 §20).

This is additive: it wraps execution resources without changing their
benchmark-facing behavior.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable

from .errors import VIALConflictError, VIALStateError, VIALValidationError

# TOOLS-001 §18 ToolResult status values
STATUS_SUCCESS = "SUCCESS"
STATUS_FAILED = "FAILED"
STATUS_TIMEOUT = "TIMEOUT"
STATUS_CANCELLED = "CANCELLED"
STATUS_REJECTED = "REJECTED"
STATUS_UNAVAILABLE = "UNAVAILABLE"
STATUS_PARTIAL = "PARTIAL"

# TOOLS-001 §71 canonical Tool lifecycle values
TOOL_DRAFT = "DRAFT"
TOOL_DEFINED = "DEFINED"
TOOL_ACTIVE = "ACTIVE"
TOOL_DEPRECATED = "DEPRECATED"
TOOL_RETIRED = "RETIRED"
# Operational compatibility values; these are not lifecycle stages.
TOOL_DISABLED = "DISABLED"
TOOL_ARCHIVED = "ARCHIVED"


@dataclass
class ToolContract:
    """Input/output/error contract (TOOLS-001 §14)."""
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    invocation_semantics: str = ""


@dataclass
class ToolResult:
    """Result envelope returned by invoke (TOOLS-001 §17)."""
    status: str
    output: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)
    provenance: str = ""
    error: str = ""
    invocation_id: str = ""

    def ok(self) -> bool:
        return self.status == STATUS_SUCCESS

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "output": self.output,
            "metadata": self.metadata,
            "provenance": self.provenance,
            "error": self.error,
            "invocation_id": self.invocation_id,
        }


@dataclass
class AuditRecord:
    """Minimum invocation audit correlation (SDK-001 §46-51)."""
    invocation_id: str
    tool_id: str
    organization_id: str
    status: str
    timestamp: float = field(default_factory=time.time)
    actor: str = ""
    decision_id: str = ""
    context_id: str = ""


@dataclass
class Tool:
    """A tool exposed to an Organization (TOOLS-001)."""
    tool_id: str
    name: str
    description: str
    version: str
    capability: str
    owner: str
    contract: ToolContract = field(default_factory=ToolContract)
    security_policy: dict[str, Any] = field(default_factory=dict)
    risk_classification: str = "low"
    side_effect_classification: str = "none"
    status: str = TOOL_ACTIVE
    invocation: Callable | None = None
    audit_records: list[AuditRecord] = field(default_factory=list, repr=False)

    def invoke(self, input: dict[str, Any], *, organization_id: str = "",
               actor: str = "", decision_id: str = "",
               context_id: str = "") -> ToolResult:
        """Invoke the tool, producing a ToolResult (TOOLS-001 §20)."""
        invocation_id = f"INV-{uuid.uuid4().hex[:12]}"
        metadata = {"tool_id": self.tool_id, "invocation_id": invocation_id}

        def record(result: ToolResult) -> ToolResult:
            self.audit_records.append(AuditRecord(
                invocation_id=invocation_id,
                tool_id=self.tool_id,
                organization_id=organization_id or self.owner,
                status=result.status,
                actor=actor,
                decision_id=decision_id,
                context_id=context_id,
            ))
            return result

        if self.status != TOOL_ACTIVE:
            return record(ToolResult(
                status=STATUS_UNAVAILABLE,
                error=f"tool {self.tool_id} is {self.status}",
                metadata={**metadata, "status": self.status},
                invocation_id=invocation_id))
        if self.invocation is None:
            return record(ToolResult(
                status=STATUS_UNAVAILABLE,
                error=f"tool {self.tool_id} has no invocation binding",
                metadata=metadata, invocation_id=invocation_id))
        try:
            output = self.invocation(input)
        except Exception as exc:
            return record(ToolResult(
                status=STATUS_FAILED,
                error=str(exc),
                metadata=metadata, invocation_id=invocation_id))
        return record(ToolResult(
            status=STATUS_SUCCESS,
            output=output,
            metadata={**metadata, "version": self.version},
            provenance=f"tool:{self.tool_id}", invocation_id=invocation_id))

    def to_dict(self) -> dict:
        return {
            "tool_id": self.tool_id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "capability": self.capability,
            "owner": self.owner,
            "risk_classification": self.risk_classification,
            "side_effect_classification": self.side_effect_classification,
            "status": self.status,
            "contract": {
                "input_schema": self.contract.input_schema,
                "output_schema": self.contract.output_schema,
                "errors": self.contract.errors,
            },
        }


class ToolRegistry:
    """Registry of Tools owned by an Organization (TOOLS-001 lifecycle)."""

    def __init__(self, organization_id: str):
        self.organization_id = organization_id
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.tool_id in self.tools:
            raise VIALStateError(
                "TOOL_EXISTS",
                f"tool '{tool.tool_id}' already registered",
                details={"tool_id": tool.tool_id})
        self.tools[tool.tool_id] = tool

    def get(self, tool_id: str) -> Tool:
        if tool_id not in self.tools:
            raise VIALStateError(
                "TOOL_NOT_FOUND",
                f"unknown tool '{tool_id}'",
                details={"tool_id": tool_id})
        return self.tools[tool_id]

    def set_status(self, tool_id: str, status: str) -> Tool:
        tool = self.get(tool_id)
        transitions = {
            TOOL_DRAFT: {TOOL_DEFINED},
            TOOL_DEFINED: {TOOL_ACTIVE},
            TOOL_ACTIVE: {TOOL_DEPRECATED, TOOL_RETIRED},
            TOOL_DEPRECATED: {TOOL_RETIRED},
            TOOL_RETIRED: set(),
        }
        if status not in transitions:
            raise VIALValidationError(
                "INVALID_TOOL_STATUS",
                f"unknown canonical Tool status '{status}'",
                details={"tool_id": tool_id, "status": status})
        if status != tool.status and status not in transitions.get(tool.status, set()):
            raise VIALConflictError(
                "INVALID_TOOL_TRANSITION",
                f"cannot move tool '{tool_id}' from {tool.status} to {status}",
                details={"tool_id": tool_id, "from": tool.status, "to": status})
        tool.status = status
        return tool

    def list(self) -> list[Tool]:
        return list(self.tools.values())
