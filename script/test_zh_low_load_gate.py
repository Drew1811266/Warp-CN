#!/usr/bin/env python3

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_low_load_gate import LoadProbe, classify_probe, parse_load_averages, should_run_heavy_gate


class LowLoadGateTests(unittest.TestCase):
    def test_parse_load_averages_from_uptime(self) -> None:
        line = "18:15  up 6 days, 20:44, 1 user, load averages: 2.31 3.23 3.09"

        self.assertEqual(parse_load_averages(line), (2.31, 3.23, 3.09))

    def test_parse_linux_style_load_average(self) -> None:
        line = "18:15:49 up 6 days, 20:44, 1 user, load average: 0.41, 0.53, 0.61"

        self.assertEqual(parse_load_averages(line), (0.41, 0.53, 0.61))

    def test_safe_probe_when_load_and_cpu_are_low(self) -> None:
        probe = LoadProbe(
            load_averages=(0.70, 0.80, 0.90),
            thermal_warning=False,
            performance_warning=False,
            hot_processes=(),
        )

        verdict = classify_probe(probe, max_load=2.50, max_hot_process_percent=25.0)

        self.assertTrue(verdict.safe)
        self.assertEqual(verdict.reasons, ())

    def test_rejects_high_load(self) -> None:
        probe = LoadProbe(
            load_averages=(2.31, 3.23, 3.09),
            thermal_warning=False,
            performance_warning=False,
            hot_processes=(),
        )

        verdict = classify_probe(probe, max_load=2.50, max_hot_process_percent=25.0)

        self.assertFalse(verdict.safe)
        self.assertIn("load average exceeds 2.50", verdict.reasons)

    def test_rejects_hot_process(self) -> None:
        probe = LoadProbe(
            load_averages=(0.70, 0.80, 0.90),
            thermal_warning=False,
            performance_warning=False,
            hot_processes=(("WindowServer", 42.3),),
        )

        verdict = classify_probe(probe, max_load=2.50, max_hot_process_percent=25.0)

        self.assertFalse(verdict.safe)
        self.assertIn("hot process WindowServer at 42.3%", verdict.reasons)

    def test_two_probe_decision_requires_both_safe(self) -> None:
        safe = LoadProbe((0.70, 0.80, 0.90), False, False, ())
        unsafe = LoadProbe((3.44, 3.63, 3.21), False, False, ())

        self.assertTrue(should_run_heavy_gate((safe, safe), max_load=2.50, max_hot_process_percent=25.0).safe)
        self.assertFalse(should_run_heavy_gate((safe, unsafe), max_load=2.50, max_hot_process_percent=25.0).safe)


if __name__ == "__main__":
    unittest.main()
