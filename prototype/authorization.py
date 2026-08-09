"""Authorization gate for Tool invocation (SDK-005, TOOLS-007).

The gate keeps Decision authorization separate from Tool capability. A Tool
may be callable, but it is not executable for a request until an authorized
Decision permits that invocation.
"""
from __future__ import annotations

import time
from typing import Any

from .errors import VIALAuthorizationError


class AuthorizationGate:
    """Validate the minimum authorization boundary before Tool execution."""

    def validate(self, tool: Any, decision: Any, actor: str,
                 organization_id: str = "", context_id: str = "") -> None:
        if decision is None:
            raise VIALAuthorizationError(
                "DECISION_REQUIRED",
                "an AUTHORIZED Decision is required for Tool invocation",
                details={"tool_id": tool.tool_id})

        if decision.status != "AUTHORIZED":
            raise VIALAuthorizationError(
                "DECISION_NOT_AUTHORIZED",
                f"Decision '{decision.id}' is {decision.status}",
                details={"decision_id": decision.id,
                         "status": decision.status,
                         "tool_id": tool.tool_id})

        if organization_id and decision.organization_id != organization_id:
            raise VIALAuthorizationError(
                "ORGANIZATION_MISMATCH",
                "Decision and invocation belong to different Organizations",
                details={"decision_id": decision.id,
                         "decision_organization": decision.organization_id,
                         "invocation_organization": organization_id})

        if tool.owner and decision.organization_id != tool.owner:
            raise VIALAuthorizationError(
                "TOOL_ORGANIZATION_MISMATCH",
                "Tool and Decision belong to different Organizations",
                details={"decision_id": decision.id,
                         "decision_organization": decision.organization_id,
                         "tool_organization": tool.owner})

        if context_id and decision.context_id and decision.context_id != context_id:
            raise VIALAuthorizationError(
                "CONTEXT_MISMATCH",
                "Decision is not authorized for this Context",
                details={"decision_id": decision.id,
                         "decision_context": decision.context_id,
                         "invocation_context": context_id})

        permitted_actors = {decision.actor, decision.authority.actor}
        if decision.authorized_by:
            permitted_actors.add(decision.authorized_by)
        allowed_actors = tool.security_policy.get("allowed_actors")
        if allowed_actors is not None:
            permitted_actors &= set(allowed_actors)
        if actor not in permitted_actors:
            raise VIALAuthorizationError(
                "ACTOR_NOT_AUTHORIZED",
                f"actor '{actor}' is not authorized for Tool '{tool.tool_id}'",
                details={"decision_id": decision.id,
                         "tool_id": tool.tool_id,
                         "actor": actor})

        required_capability = tool.security_policy.get("required_capability")
        if required_capability and decision.type != required_capability:
            raise VIALAuthorizationError(
                "CAPABILITY_NOT_AUTHORIZED",
                f"Decision type '{decision.type}' does not grant "
                f"capability '{required_capability}'",
                details={"decision_id": decision.id,
                         "tool_id": tool.tool_id})

        required_scope = tool.security_policy.get("required_scope")
        if required_scope and decision.authority.scope != required_scope:
            raise VIALAuthorizationError(
                "SCOPE_NOT_AUTHORIZED",
                f"Decision scope '{decision.authority.scope}' does not grant "
                f"scope '{required_scope}'",
                details={"decision_id": decision.id,
                         "tool_id": tool.tool_id})

        required_policy = tool.security_policy.get("required_policy")
        if required_policy and decision.authority.policy != required_policy:
            raise VIALAuthorizationError(
                "POLICY_NOT_AUTHORIZED",
                "Decision policy does not satisfy the Tool policy",
                details={"decision_id": decision.id,
                         "tool_id": tool.tool_id})

        if decision.expires_at is not None and time.time() > decision.expires_at:
            raise VIALAuthorizationError(
                "DECISION_EXPIRED",
                f"Decision '{decision.id}' has expired",
                details={"decision_id": decision.id})
