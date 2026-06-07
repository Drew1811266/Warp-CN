#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_performance_probe import (
    DEFERRED_HIGH_LOAD_COMMANDS,
    high_load_skip_payload,
    render_json,
    render_markdown,
    run_low_load_commands,
)


class PerformanceProbeTests(unittest.TestCase):
    def test_high_load_skip_payload_contains_no_execution_result(self) -> None:
        payload = high_load_skip_payload()

        self.assertEqual(payload["status"], "skipped-by-heat-safety-policy")
        self.assertEqual(payload["runtime_performance_readiness"], "not-evaluated")
        self.assertIn("cargo fmt --check", payload["not_run"])

    def test_run_low_load_commands_uses_supplied_commands_only(self) -> None:
        completed = subprocess.CompletedProcess(args=("python3", "--version"), returncode=0, stdout="ok\n", stderr="")
        with mock.patch("zh_performance_probe.subprocess.run", return_value=completed) as run:
            with mock.patch("zh_performance_probe.time.perf_counter", side_effect=[1.0, 1.25]):
                results = run_low_load_commands((("python3", "--version"),))

        self.assertEqual(results[0].command, "python3 --version")
        self.assertEqual(results[0].elapsed_seconds, 0.25)
        run.assert_called_once()
        called_command = run.call_args.args[0]
        self.assertNotIn("cargo", called_command)
        self.assertNotIn("open", called_command)

    def test_render_outputs_mark_high_load_as_skipped(self) -> None:
        markdown = render_markdown([])
        json_output = render_json([])

        self.assertIn("skipped-by-heat-safety-policy", markdown)
        self.assertIn("not-evaluated", json_output)
        for command in DEFERRED_HIGH_LOAD_COMMANDS:
            self.assertIn(command, markdown)


if __name__ == "__main__":
    unittest.main()
