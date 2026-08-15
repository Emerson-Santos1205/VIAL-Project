"""Tests for the RFC-010 real-model harness without invoking a provider."""
from __future__ import annotations

import unittest
import importlib.util
from pathlib import Path


_MODULE_PATH = Path(__file__).resolve().parents[1] / "benchmark" / "economic-cost" / "run_opencode.py"
_SPEC = importlib.util.spec_from_file_location("economic_real", _MODULE_PATH)
run_opencode = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(run_opencode)


class EconomicRealHarnessTests(unittest.TestCase):
    def test_cost_breakdown_contains_all_declared_components(self) -> None:
        row = {
            "context_tokens": 100,
            "input_tokens": 100,
            "output_tokens": 20,
            "latency_s": 2.0,
        }
        prices = {
            "tokens_per_1k": 0.2,
            "inference_input_per_1k": 1.0,
            "inference_output_per_1k": 2.0,
            "latency_per_second": 0.5,
            "retrieval_per_op": 0.1,
            "construction_per_context": 0.2,
            "validation_per_op": 0.3,
        }
        result = run_opencode.cost(row, prices)
        self.assertEqual(set(result), {
            "tokens", "inference", "latency", "retrieval",
            "construction", "validation", "total",
        })
        self.assertAlmostEqual(result["total"], sum(result[key] for key in (
            "tokens", "inference", "latency", "retrieval",
            "construction", "validation",
        )))

    def test_workload_has_deterministic_and_reasoning_operations(self) -> None:
        workload = run_opencode.load_workload(
            run_opencode.HERE / "workloads/economic-real.json")
        operations = workload["operations"]
        self.assertTrue(any(op["deterministic_solvable"] for op in operations))
        self.assertTrue(any(not op["deterministic_solvable"] for op in operations))


if __name__ == "__main__":
    unittest.main()
