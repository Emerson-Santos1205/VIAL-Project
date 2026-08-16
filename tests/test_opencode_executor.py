"""Mocked tests for the external opencode executor boundary."""
from __future__ import annotations

import json
import subprocess
import unittest
from unittest.mock import patch

from prototype.context import ContextBuilder, Task
from prototype.errors import VIALExecutionError, VIALTimeoutError
from prototype.opencode_executor import OpencodeExecutor, OUTCOME_UNKNOWN
from prototype.state import Organization


class OpencodeExecutorTests(unittest.TestCase):
    def setUp(self) -> None:
        organization = Organization("ORG-1")
        organization.add_field("value", 7, ["value"])
        self.context = ContextBuilder(organization).build_selective(
            Task("TASK-1", "is value positive?", ["value"], True, "read"))
        self.task = Task("TASK-1", "is value positive?", ["value"], True, "read")

    @staticmethod
    def completed(*events: dict) -> subprocess.CompletedProcess:
        stdout = "\n".join(json.dumps(event) for event in events)
        return subprocess.CompletedProcess([], 0, stdout, "")

    @patch("prototype.opencode_executor.subprocess.run")
    def test_parses_answer_and_token_counts(self, run) -> None:
        run.return_value = self.completed(
            {"type": "text", "part": {"text": '{"answer": true}'}},
            {"type": "step_finish", "part": {"tokens": {
                "input": 12, "output": 3, "total": 15, "reasoning": 1}}},
        )

        result = OpencodeExecutor(model="test/model").execute(
            self.context, self.task)

        self.assertEqual(result["outcome"], True)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(result["prompt_tokens"], 12)
        self.assertEqual(result["completion_tokens"], 3)
        self.assertEqual(result["total_tokens"], 15)

    @patch("prototype.opencode_executor.subprocess.run")
    def test_marks_unparseable_response_unknown(self, run) -> None:
        run.return_value = self.completed(
            {"type": "text", "part": {"text": '{"answer": "maybe"}'}})

        result = OpencodeExecutor(model="test/model").execute(
            self.context, self.task)

        self.assertIsNone(result["outcome"])
        self.assertEqual(result["status"], OUTCOME_UNKNOWN)

    @patch("prototype.opencode_executor.subprocess.run")
    def test_wraps_timeout_as_structured_vial_error(self, run) -> None:
        run.side_effect = subprocess.TimeoutExpired("opencode", 1)

        with self.assertRaises(VIALTimeoutError) as raised:
            OpencodeExecutor(model="test/model", timeout=1).execute(
                self.context, self.task)

        self.assertEqual(raised.exception.code, "TIMEOUT")

    @patch("prototype.opencode_executor.subprocess.run")
    def test_wraps_process_start_failure(self, run) -> None:
        run.side_effect = OSError("missing executable")

        with self.assertRaises(VIALExecutionError) as raised:
            OpencodeExecutor(model="test/model").execute(
                self.context, self.task)

        self.assertEqual(raised.exception.code, "EXECUTION_ERROR")


if __name__ == "__main__":
    unittest.main()
