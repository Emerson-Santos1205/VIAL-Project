"""Coverage tests for the 6 zero-coverage core modules:
coordinator, cost, executor, llm_executor, resource, reuse."""
from __future__ import annotations

import json
import unittest
from unittest.mock import MagicMock, patch

from prototype.context import Context, ContextBuilder, Task
from prototype.coordinator import (ABORTED, COMMITTED, PENDING, Intent,
                                   StateCoordinator)
from prototype.cost import CostComponents, CostModel, ResourceSelector
from prototype.errors import (VIALConflictError, VIALStateError,
                               VIALValidationError)
from prototype.executor import DeterministicExecutor, Evaluator
from prototype.reuse import ReuseEngine, reuse_signature
from prototype.state import Organization

# ── coordinator.py ──────────────────────────────────────────────────────

class CoordinatorTests(unittest.TestCase):
    def _org(self) -> Organization:
        org = Organization("ORG-1")
        org.add_field("temp", 21, ["temperature"])
        return org

    def test_begin_and_commit(self) -> None:
        coord = StateCoordinator(self._org())
        intent = coord.begin("op-1", "temp", 25, "org-root")
        self.assertEqual(intent.status, PENDING)
        committed = coord.commit("op-1")
        self.assertEqual(committed.status, COMMITTED)
        self.assertEqual(committed.resulting_version, 1)

    def test_begin_unauthorized_actor(self) -> None:
        coord = StateCoordinator(self._org())
        with self.assertRaises(Exception):
            coord.begin("op-1", "temp", 25, "wrong-actor")

    def test_begin_unknown_field(self) -> None:
        coord = StateCoordinator(self._org())
        with self.assertRaises(VIALStateError):
            coord.begin("op-1", "nonexistent", 25, "org-root")

    def test_begin_duplicate_operation_id(self) -> None:
        coord = StateCoordinator(self._org())
        coord.begin("op-1", "temp", 25, "org-root")
        with self.assertRaises(VIALConflictError):
            coord.begin("op-1", "temp", 30, "org-root")

    def test_commit_unknown_operation(self) -> None:
        coord = StateCoordinator(self._org())
        with self.assertRaises(VIALStateError):
            coord.commit("op-unknown")

    def test_commit_aborted_operation(self) -> None:
        coord = StateCoordinator(self._org())
        coord.begin("op-1", "temp", 25, "org-root")
        coord.abort("op-1")
        with self.assertRaises(VIALValidationError):
            coord.commit("op-1")

    def test_duplicate_commit_increments_counter(self) -> None:
        coord = StateCoordinator(self._org())
        coord.begin("op-1", "temp", 25, "org-root")
        coord.commit("op-1")
        coord.commit("op-1")
        self.assertEqual(coord.duplicate_commits, 1)

    def test_abort_pending(self) -> None:
        coord = StateCoordinator(self._org())
        intent = coord.begin("op-1", "temp", 25, "org-root")
        aborted = coord.abort("op-1")
        self.assertEqual(aborted.status, ABORTED)

    def test_abort_unknown_operation(self) -> None:
        coord = StateCoordinator(self._org())
        with self.assertRaises(VIALStateError):
            coord.abort("op-unknown")

    def test_resolve(self) -> None:
        coord = StateCoordinator(self._org())
        coord.begin("op-1", "temp", 25, "org-root")
        self.assertIsNotNone(coord.resolve("op-1"))
        self.assertIsNone(coord.resolve("op-unknown"))

    def test_snapshot(self) -> None:
        coord = StateCoordinator(self._org())
        snap = coord.snapshot()
        self.assertIn("version", snap)
        self.assertIn("fields", snap)

    def test_state_version_conflict(self) -> None:
        org = self._org()
        coord = StateCoordinator(org)
        coord.begin("op-1", "temp", 25, "org-root")
        org.state_version += 1
        with self.assertRaises(VIALConflictError):
            coord.commit("op-1")


# ── cost.py ─────────────────────────────────────────────────────────────

class CostComponentsTests(unittest.TestCase):
    def test_total(self) -> None:
        c = CostComponents(tokens=1.0, inference=2.0, latency=3.0,
                           retrieval=4.0, construction=5.0, validation=6.0)
        self.assertEqual(c.total(), 21.0)

    def test_to_dict(self) -> None:
        c = CostComponents(tokens=1.0, inference=2.0)
        d = c.to_dict()
        self.assertIn("total", d)
        self.assertEqual(d["tokens"], 1.0)


class CostModelTests(unittest.TestCase):
    def test_infer(self) -> None:
        model = CostModel({"tokens_per_1k": 0.01, "inference_input_per_1k": 0.02,
                           "inference_output_per_1k": 0.03, "latency_per_second": 0.001})
        c = model.infer(1000, 500, tier_multiplier=2.0)
        self.assertGreater(c.total(), 0)

    def test_retrieval(self) -> None:
        model = CostModel({"retrieval_per_op": 0.1})
        c = model.retrieval(10)
        self.assertAlmostEqual(c.retrieval, 1.0)

    def test_construction(self) -> None:
        model = CostModel({"construction_per_context": 0.5})
        c = model.construction(4)
        self.assertAlmostEqual(c.construction, 2.0)

    def test_validation(self) -> None:
        model = CostModel({"validation_per_op": 0.25})
        c = model.validation(3)
        self.assertAlmostEqual(c.validation, 0.75)

    def test_sum(self) -> None:
        model = CostModel({})
        a = CostComponents(tokens=1.0)
        b = CostComponents(tokens=2.0)
        result = model.sum(a, b)
        self.assertEqual(result.tokens, 3.0)


class ResourceSelectorTests(unittest.TestCase):
    def test_deterministic_first(self) -> None:
        sel = ResourceSelector({"deterministic": 0.0, "light": 1.0, "advanced": 2.0},
                               ["deterministic", "light", "advanced"])
        self.assertEqual(sel.select(True, ["light", "advanced"]), "deterministic")

    def test_cheapest_capable(self) -> None:
        sel = ResourceSelector({"deterministic": 0.0, "light": 1.0, "advanced": 2.0},
                               ["deterministic", "light", "advanced"])
        self.assertEqual(sel.select(False, ["light", "advanced"]), "light")

    def test_no_capable_tier(self) -> None:
        sel = ResourceSelector({}, ["deterministic", "light"])
        with self.assertRaises(VIALValidationError):
            sel.select(False, [])


# ── executor.py ─────────────────────────────────────────────────────────

class ExecutorTests(unittest.TestCase):
    def _make_ctx(self, fields: dict) -> Context:
        body = json.dumps({"state": {"fields": fields}})
        return Context(
            task_id="T-1", organization_id="ORG-1", body=body,
            mode="full", state_version=0, tokens=0)

    def test_range_in_bounds(self) -> None:
        ctx = self._make_ctx({"temp": {"value": 21}})
        task = Task("T-1", "check temp", ["temp"], True, "range", ["temp", 20, 30])
        result = DeterministicExecutor().execute(ctx, task)
        self.assertTrue(result.correct)
        self.assertEqual(result.quality, 1.0)

    def test_range_out_of_bounds(self) -> None:
        ctx = self._make_ctx({"temp": {"value": 50}})
        task = Task("T-1", "check temp", ["temp"], True, "range", ["temp", 20, 30])
        result = DeterministicExecutor().execute(ctx, task)
        self.assertFalse(result.correct)

    def test_range_missing_field(self) -> None:
        ctx = self._make_ctx({})
        task = Task("T-1", "check temp", ["temp"], True, "range", ["temp", 20, 30])
        result = DeterministicExecutor().execute(ctx, task)
        self.assertEqual(result.quality, 0.0)

    def test_bool_true(self) -> None:
        ctx = self._make_ctx({"flag": {"value": True}})
        task = Task("T-1", "check flag", ["flag"], True, "bool", ["flag"])
        result = DeterministicExecutor().execute(ctx, task)
        self.assertTrue(result.correct)

    def test_bool_missing_field(self) -> None:
        ctx = self._make_ctx({})
        task = Task("T-1", "check flag", ["flag"], True, "bool", ["flag"])
        result = DeterministicExecutor().execute(ctx, task)
        self.assertEqual(result.quality, 0.0)

    def test_unknown_op(self) -> None:
        ctx = self._make_ctx({})
        task = Task("T-1", "unknown", [], True, "unknown_op")
        with self.assertRaises(VIALValidationError):
            DeterministicExecutor().execute(ctx, task)

    def test_evaluator_scores_quality(self) -> None:
        from prototype.executor import ExecutionResult
        r = ExecutionResult("T-1", "full", True, True, 0.8)
        self.assertEqual(Evaluator().score(r), 0.8)


# ── llm_executor.py ────────────────────────────────────────────────────

class LLMExecutorTests(unittest.TestCase):
    def test_missing_api_key_raises(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(RuntimeError):
                from prototype.llm_executor import LLMExecutor
                LLMExecutor(api_key=None)

    def test_llm_evaluator_score(self) -> None:
        from prototype.llm_executor import LLMEvaluator, OUTCOME_UNKNOWN
        task = Task("T-1", "test", [], True, "bool", ["flag"])
        ev = LLMEvaluator()
        self.assertEqual(ev.score({"outcome": True, "status": "SUCCESS"}, task), 1.0)
        self.assertEqual(ev.score({"outcome": False, "status": "SUCCESS"}, task), 0.0)
        self.assertEqual(ev.score({"outcome": None, "status": OUTCOME_UNKNOWN}, task), 0.0)


# ── resource.py ─────────────────────────────────────────────────────────

class ResourceTests(unittest.TestCase):
    def test_add_capability(self) -> None:
        from prototype.resource import Resource, Capability, STATUS_AVAILABLE
        r = Resource("R-1", "executor", "ORG-1")
        cap = Capability("cap-read", status=STATUS_AVAILABLE)
        r.add_capability(cap)
        self.assertTrue(r.has_capability("cap-read"))

    def test_duplicate_capability_raises(self) -> None:
        from prototype.resource import Resource, Capability
        r = Resource("R-1", "executor", "ORG-1")
        cap = Capability("cap-read")
        r.add_capability(cap)
        with self.assertRaises(VIALConflictError):
            r.add_capability(cap)

    def test_has_capability_unavailable(self) -> None:
        from prototype.resource import Resource, Capability, STATUS_UNAVAILABLE
        r = Resource("R-1", "executor", "ORG-1")
        cap = Capability("cap-read", status=STATUS_UNAVAILABLE)
        r.add_capability(cap)
        self.assertFalse(r.has_capability("cap-read"))

    def test_set_status(self) -> None:
        from prototype.resource import Resource, STATUS_BUSY
        r = Resource("R-1", "executor", "ORG-1")
        r.set_status(STATUS_BUSY)
        self.assertEqual(r.status, STATUS_BUSY)
        self.assertEqual(r.health, STATUS_BUSY)

    def test_to_dict(self) -> None:
        from prototype.resource import Resource
        r = Resource("R-1", "executor", "ORG-1", name="Test")
        d = r.to_dict()
        self.assertEqual(d["resource_id"], "R-1")

    def test_capability_to_dict(self) -> None:
        from prototype.resource import Capability
        cap = Capability("cap-1", description="test cap")
        d = cap.to_dict()
        self.assertEqual(d["capability_id"], "cap-1")


class ResourceRegistryTests(unittest.TestCase):
    def test_register_and_get(self) -> None:
        from prototype.resource import Resource, ResourceRegistry
        reg = ResourceRegistry("ORG-1")
        r = Resource("R-1", "executor", "ORG-1")
        reg.register(r)
        self.assertEqual(reg.get("R-1").resource_id, "R-1")

    def test_register_wrong_org(self) -> None:
        from prototype.resource import Resource, ResourceRegistry
        reg = ResourceRegistry("ORG-1")
        r = Resource("R-1", "executor", "ORG-2")
        with self.assertRaises(VIALValidationError):
            reg.register(r)

    def test_register_duplicate(self) -> None:
        from prototype.resource import Resource, ResourceRegistry
        reg = ResourceRegistry("ORG-1")
        r = Resource("R-1", "executor", "ORG-1")
        reg.register(r)
        with self.assertRaises(VIALConflictError):
            reg.register(r)

    def test_get_unknown(self) -> None:
        from prototype.resource import ResourceRegistry
        reg = ResourceRegistry("ORG-1")
        with self.assertRaises(VIALStateError):
            reg.get("R-unknown")

    def test_select_matching(self) -> None:
        from prototype.resource import (Resource, Capability, ResourceRegistry,
                                        STATUS_AVAILABLE)
        reg = ResourceRegistry("ORG-1")
        r = Resource("R-1", "executor", "ORG-1")
        cap = Capability("cap-read", status=STATUS_AVAILABLE)
        r.add_capability(cap)
        reg.register(r)
        found = reg.select("cap-read")
        self.assertIsNotNone(found)
        self.assertEqual(found.resource_id, "R-1")

    def test_select_no_match(self) -> None:
        from prototype.resource import Resource, ResourceRegistry
        reg = ResourceRegistry("ORG-1")
        r = Resource("R-1", "executor", "ORG-1")
        reg.register(r)
        self.assertIsNone(reg.select("nonexistent"))

    def test_select_unavailable_resource(self) -> None:
        from prototype.resource import (Resource, Capability, ResourceRegistry,
                                        STATUS_UNAVAILABLE, STATUS_AVAILABLE)
        reg = ResourceRegistry("ORG-1")
        r = Resource("R-1", "executor", "ORG-1", status=STATUS_UNAVAILABLE)
        cap = Capability("cap-read", status=STATUS_AVAILABLE)
        r.add_capability(cap)
        reg.register(r)
        self.assertIsNone(reg.select("cap-read"))

    def test_select_by_authority(self) -> None:
        from prototype.resource import (Resource, Capability, ResourceRegistry,
                                        STATUS_AVAILABLE)
        reg = ResourceRegistry("ORG-1")
        r = Resource("R-1", "executor", "ORG-1")
        cap = Capability("cap-secured", status=STATUS_AVAILABLE,
                         required_authority="admin")
        r.add_capability(cap)
        reg.register(r)
        self.assertIsNone(reg.select("cap-secured", actor="user"))
        self.assertIsNotNone(reg.select("cap-secured", actor="admin"))

    def test_list(self) -> None:
        from prototype.resource import Resource, ResourceRegistry
        reg = ResourceRegistry("ORG-1")
        reg.register(Resource("R-1", "executor", "ORG-1"))
        reg.register(Resource("R-2", "llm", "ORG-1"))
        self.assertEqual(len(reg.list()), 2)


# ── reuse.py ────────────────────────────────────────────────────────────

class ReuseTests(unittest.TestCase):
    def _org_with_field(self) -> Organization:
        org = Organization("ORG-1")
        org.add_field("temp", 21, ["temp"])
        return org

    def _task(self) -> Task:
        return Task("T-1", "check temp", ["temp"], True, "range", ["temp", 20, 30])

    def _ctx(self, org: Organization) -> Context:
        return ContextBuilder(org).build_selective(self._task())

    def test_reuse_signature_deterministic(self) -> None:
        t = self._task()
        self.assertEqual(reuse_signature(t), reuse_signature(t))

    def test_store_and_lookup_hit(self) -> None:
        org = self._org_with_field()
        engine = ReuseEngine(org)
        task = self._task()
        ctx = self._ctx(org)
        engine.store(task, True, 1.0, ctx, provenance="test")
        entry, outcome = engine.lookup(task)
        self.assertEqual(outcome, "hit")
        self.assertIsNotNone(entry)

    def test_lookup_miss(self) -> None:
        org = self._org_with_field()
        engine = ReuseEngine(org)
        entry, outcome = engine.lookup(self._task())
        self.assertEqual(outcome, "miss")
        self.assertIsNone(entry)

    def test_lookup_stale(self) -> None:
        org = self._org_with_field()
        engine = ReuseEngine(org)
        task = self._task()
        ctx = self._ctx(org)
        engine.store(task, True, 1.0, ctx, provenance="test")
        org.fields["temp"].value = 99
        entry, outcome = engine.lookup(task)
        self.assertEqual(outcome, "stale")
        self.assertEqual(engine.invalidations, 1)

    def test_stats(self) -> None:
        org = self._org_with_field()
        engine = ReuseEngine(org)
        stats = engine.stats()
        self.assertIn("reuse_hits", stats)
        self.assertIn("recomputes", stats)
        self.assertIn("invalidations", stats)


if __name__ == "__main__":
    unittest.main()
