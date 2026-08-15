"""Direct security tests for the Tool authorization boundary."""
from __future__ import annotations

import time
import unittest

from prototype.decision import Authority, DecisionEngine
from prototype.tool import STATUS_REJECTED, Tool


def authorized_decision(*, organization_id: str = "ORG-1", context_id: str = "CTX-1",
                        scope: str = "organization", actor: str = "operator"):
    engine = DecisionEngine(organization_id)
    decision = engine.propose(
        objective="read temperature",
        actor="planner",
        authority=Authority(actor=actor, scope=scope),
        context_id=context_id,
    )
    engine.approve(decision.id, "planner")
    engine.authorize(decision.id, actor)
    return decision


class AuthorizationBoundaryTests(unittest.TestCase):
    def make_tool(self, **policy: object) -> Tool:
        return Tool(
            "TOOL-1", "reader", "reads data", "1.0", "read", "ORG-1",
            security_policy=policy,
            invocation=lambda value: value,
        )

    def test_rejects_organization_mismatch(self) -> None:
        result = self.make_tool().invoke(
            {}, actor="operator", organization_id="ORG-2",
            context_id="CTX-1", decision=authorized_decision(),
        )
        self.assertEqual(result.status, STATUS_REJECTED)
        self.assertEqual(result.metadata["error_code"], "ORGANIZATION_MISMATCH")

    def test_rejects_context_mismatch(self) -> None:
        result = self.make_tool().invoke(
            {}, actor="operator", organization_id="ORG-1",
            context_id="CTX-2", decision=authorized_decision(),
        )
        self.assertEqual(result.status, STATUS_REJECTED)
        self.assertEqual(result.metadata["error_code"], "CONTEXT_MISMATCH")

    def test_rejects_actor_not_authorized_by_decision(self) -> None:
        result = self.make_tool().invoke(
            {}, actor="intruder", organization_id="ORG-1",
            context_id="CTX-1", decision=authorized_decision(),
        )
        self.assertEqual(result.status, STATUS_REJECTED)
        self.assertEqual(result.metadata["error_code"], "ACTOR_NOT_AUTHORIZED")

    def test_rejects_insufficient_scope(self) -> None:
        tool = self.make_tool(required_scope="site")
        result = tool.invoke(
            {}, actor="operator", organization_id="ORG-1",
            context_id="CTX-1", decision=authorized_decision(),
        )
        self.assertEqual(result.status, STATUS_REJECTED)
        self.assertEqual(result.metadata["error_code"], "SCOPE_NOT_AUTHORIZED")

    def test_rejects_expired_decision(self) -> None:
        decision = authorized_decision()
        decision.expires_at = time.time() - 1
        result = self.make_tool().invoke(
            {}, actor="operator", organization_id="ORG-1",
            context_id="CTX-1", decision=decision,
        )
        self.assertEqual(result.status, STATUS_REJECTED)
        self.assertEqual(result.metadata["error_code"], "DECISION_EXPIRED")


if __name__ == "__main__":
    unittest.main()
