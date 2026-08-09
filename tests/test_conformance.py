"""Conformance tests for the canonical prototype surfaces."""
from __future__ import annotations

import unittest

from prototype.context import CTX_CREATED, CTX_FROZEN, ContextBuilder, Task
from prototype.decision import (
    STATUS_AUTHORIZED,
    STATUS_COMPLETED,
    STATUS_DRAFT,
    STATUS_PENDING,
    Authority,
    DecisionEngine,
)
from prototype.errors import VIALConflictError, VIALStateError
from prototype.identity import Authenticator
from prototype.persistence import JsonRepository
from prototype.state import Organization
from prototype.tool import STATUS_REJECTED, STATUS_SUCCESS, Tool, ToolRegistry


class ConformanceTests(unittest.TestCase):
    def test_end_to_end_authenticated_authorized_invocation(self) -> None:
        organization = Organization("ORG-1")
        organization.add_field("temperature", 21, ["temperature"])
        task = Task("TASK-1", "read temperature", ["temperature"], 21, "read")
        context = ContextBuilder(organization).build_selective(task)
        identity = Authenticator()
        identity.register("operator", "ORG-1", "secret")
        principal = identity.authenticate("operator", "secret")
        engine = DecisionEngine("ORG-1")
        decision = engine.propose(
            objective=task.prompt,
            actor="planner",
            authority=Authority(actor=principal.actor),
            context_id=context.context_id,
            context_version=context.version,
        )
        engine.approve(decision.id, "planner")
        engine.authorize(decision.id, principal.actor)
        tool = Tool(
            "TOOL-1", "reader", "reads data", "1.0", "read", "ORG-1",
            invocation=lambda value: value["key"],
        )
        result = tool.invoke(
            {"key": "temperature"}, actor=principal.actor,
            organization_id=principal.organization_id,
            context_id=context.context_id, decision=decision,
        )
        self.assertEqual(result.status, STATUS_SUCCESS)
        self.assertEqual(tool.audit_records[0].decision_id, decision.id)

    def test_json_repository_round_trip_is_atomic(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            repository = JsonRepository(directory)
            repository.save("state.json", {"version": 1, "value": "ok"})
            self.assertEqual(repository.load("state.json")["version"], 1)
    def test_context_is_frozen_and_refresh_is_new_version(self) -> None:
        organization = Organization("ORG-1")
        organization.add_field("temperature", 21, ["temperature"])
        task = Task("TASK-1", "read temperature", ["temperature"], 21, "read")

        context = ContextBuilder(organization).build_selective(task)

        self.assertEqual(context.status, CTX_FROZEN)
        with self.assertRaises(VIALStateError):
            context.body = "mutated"

        refreshed = context.refresh()
        self.assertEqual(refreshed.status, CTX_CREATED)
        self.assertEqual(refreshed.version, 2)

    def test_decision_uses_canonical_lifecycle(self) -> None:
        engine = DecisionEngine("ORG-1")
        decision = engine.propose(
            objective="read temperature",
            actor="planner",
            authority=Authority(actor="operator", scope="organization"),
        )

        self.assertEqual(decision.status, STATUS_DRAFT)
        engine.approve(decision.id, "planner")
        self.assertEqual(decision.status, STATUS_PENDING)
        engine.authorize(decision.id, "operator")
        self.assertEqual(decision.status, STATUS_AUTHORIZED)
        self.assertEqual(decision.authorized_by, "operator")
        engine.execute(decision.id, "operator", outcome={"ok": True})
        self.assertEqual(decision.status, STATUS_COMPLETED)

    def test_tool_rejects_invocation_without_authorized_decision(self) -> None:
        calls: list[dict] = []
        tool = Tool(
            "TOOL-1", "reader", "reads data", "1.0", "read", "ORG-1",
            invocation=lambda value: calls.append(value) or value,
        )

        result = tool.invoke({"key": "temperature"}, actor="operator",
                             organization_id="ORG-1")

        self.assertEqual(result.status, STATUS_REJECTED)
        self.assertEqual(result.metadata["error_code"], "DECISION_REQUIRED")
        self.assertEqual(calls, [])
        self.assertEqual(tool.audit_records[0].status, STATUS_REJECTED)

    def test_tool_executes_only_with_matching_authorized_decision(self) -> None:
        engine = DecisionEngine("ORG-1")
        decision = engine.propose(
            objective="read temperature",
            actor="planner",
            authority=Authority(actor="operator", scope="organization"),
            context_id="CTX-1",
        )
        engine.approve(decision.id, "planner")
        engine.authorize(decision.id, "operator")
        tool = Tool(
            "TOOL-1", "reader", "reads data", "1.0", "read", "ORG-1",
            security_policy={"required_scope": "organization"},
            invocation=lambda value: value["key"],
        )

        result = tool.invoke(
            {"key": "temperature"}, actor="operator",
            organization_id="ORG-1", context_id="CTX-1", decision=decision,
        )

        self.assertEqual(result.status, STATUS_SUCCESS)
        self.assertEqual(result.output, "temperature")
        self.assertTrue(result.invocation_id.startswith("INV-"))
        self.assertEqual(tool.audit_records[0].decision_id, decision.id)

    def test_tool_registry_rejects_invalid_transition(self) -> None:
        registry = ToolRegistry("ORG-1")
        tool = Tool("TOOL-1", "reader", "reads data", "1.0", "read", "ORG-1")
        registry.register(tool)

        with self.assertRaises(VIALConflictError):
            registry.set_status("TOOL-1", "DEFINED")


if __name__ == "__main__":
    unittest.main()
