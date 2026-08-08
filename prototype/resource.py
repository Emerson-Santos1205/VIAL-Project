"""Resource model and registry (SDK-003).

Implements the SDK-003 Resource abstraction:
- Resource identity is stable and unique (SDK-003 §4);
- Resource exposes Capabilities (SDK-003 §7, §22-25);
- Resource status follows an explicit lifecycle (SDK-003 §14);
- Resource selection filters by capability AND status/availability
  (SDK-003 §52-53), and authority is validated separately from capability
  (SDK-003 §25: capability is not authority).

This is additive to the benchmark prototype: executors (Deterministic,
LLM, Opencode) remain available; they can be registered as Resources.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from .errors import VIALConflictError, VIALStateError, VIALValidationError

# SDK-003 §14 resource status values
STATUS_AVAILABLE = "available"
STATUS_UNAVAILABLE = "unavailable"
STATUS_BUSY = "busy"
STATUS_ERROR = "error"
STATUS_DEGRADED = "degraded"
STATUS_OFFLINE = "offline"
STATUS_DISABLED = "disabled"
STATUS_RETIRED = "retired"
STATUS_MAINTENANCE = "maintenance"


@dataclass
class Capability:
    """A declared ability of a Resource (SDK-003 §22-25)."""
    capability_id: str
    description: str = ""
    version: str = "1.0.0"
    status: str = STATUS_AVAILABLE
    constraints: dict[str, Any] = field(default_factory=dict)
    required_authority: str | None = None

    def to_dict(self) -> dict:
        return {
            "capability_id": self.capability_id,
            "description": self.description,
            "version": self.version,
            "status": self.status,
            "constraints": self.constraints,
            "required_authority": self.required_authority,
        }


@dataclass
class Resource:
    """An execution resource with stable identity (SDK-003 §3-7, §14)."""
    resource_id: str
    type: str
    organization_id: str
    name: str = ""
    description: str = ""
    status: str = STATUS_AVAILABLE
    availability: float = 1.0
    health: str = STATUS_AVAILABLE
    version: str = "1.0.0"
    capabilities: dict[str, Capability] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_capability(self, cap: Capability) -> None:
        if cap.capability_id in self.capabilities:
            raise VIALConflictError(
                "CAPABILITY_EXISTS",
                f"capability '{cap.capability_id}' already declared",
                details={"resource_id": self.resource_id,
                         "capability_id": cap.capability_id})
        self.capabilities[cap.capability_id] = cap

    def has_capability(self, capability_id: str) -> bool:
        cap = self.capabilities.get(capability_id)
        return cap is not None and cap.status == STATUS_AVAILABLE

    def set_status(self, status: str) -> None:
        self.status = status
        self.health = status

    def to_dict(self) -> dict:
        return {
            "resource_id": self.resource_id,
            "type": self.type,
            "organization_id": self.organization_id,
            "name": self.name,
            "status": self.status,
            "availability": self.availability,
            "health": self.health,
            "version": self.version,
            "capabilities": [c.to_dict() for c in self.capabilities.values()],
        }


class ResourceRegistry:
    """Registry of Resources belonging to an Organization (SDK-003 §27-33)."""

    def __init__(self, organization_id: str):
        self.organization_id = organization_id
        self.resources: dict[str, Resource] = {}

    def register(self, resource: Resource) -> None:
        if resource.organization_id != self.organization_id:
            raise VIALValidationError(
                "ORGANIZATION_MISMATCH",
                f"resource {resource.resource_id} belongs to "
                f"{resource.organization_id}, registry is for {self.organization_id}",
                details={"resource_id": resource.resource_id})
        if resource.resource_id in self.resources:
            raise VIALConflictError(
                "RESOURCE_EXISTS",
                f"resource '{resource.resource_id}' already registered",
                details={"resource_id": resource.resource_id})
        self.resources[resource.resource_id] = resource

    def get(self, resource_id: str) -> Resource:
        if resource_id not in self.resources:
            raise VIALStateError(
                "RESOURCE_NOT_FOUND",
                f"unknown resource '{resource_id}'",
                details={"resource_id": resource_id})
        return self.resources[resource_id]

    def select(self, capability_id: str, actor: str | None = None) -> Resource | None:
        """Select a resource that declares the capability AND is available
        (SDK-003 §52-53). Authority is validated by the caller against the
        capability's required_authority; capability alone is not authority."""
        for r in self.resources.values():
            if r.status != STATUS_AVAILABLE:
                continue
            cap = r.capabilities.get(capability_id)
            if cap is None or cap.status != STATUS_AVAILABLE:
                continue
            if cap.required_authority is not None and actor != cap.required_authority:
                continue
            return r
        return None

    def list(self) -> list[Resource]:
        return list(self.resources.values())
