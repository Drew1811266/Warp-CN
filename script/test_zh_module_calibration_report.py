#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_module_calibration_report import (
    load_rows,
    module_summary,
    render_copy_findings,
    render_functional_findings,
    render_module_matrix,
    write_reports,
)


SAMPLE_ROWS = [
    {
        "entry_index": 1,
        "manifest_line": 10,
        "path": "app/src/settings_view/ai_page.rs",
        "source": "API key",
        "target": "API 密钥",
        "decision": "simulated-accepted-with-note",
        "machine_copy_score": 2,
        "copy_status": "clean",
        "functional_status": "clean",
        "mojibake_status": "clean",
        "ui_density_risk": "clean",
        "risk_tags": "api-key-secret",
        "public_rc_rows": "GUI-WS-04",
        "module_group": "settings",
        "token_status": "clean",
        "notes": "",
    },
    {
        "entry_index": 2,
        "manifest_line": 20,
        "path": "app/src/terminal/view.rs",
        "source": "Run --help",
        "target": "运行 --help",
        "decision": "needs-functional-review",
        "machine_copy_score": 1,
        "copy_status": "note",
        "functional_status": "token-critical-review",
        "mojibake_status": "clean",
        "ui_density_risk": "clean",
        "risk_tags": "terminal-command;dynamic-placeholder",
        "public_rc_rows": "",
        "module_group": "terminal-command",
        "token_status": "critical-mismatch",
        "notes": "placeholder mismatch",
    },
]


class ModuleCalibrationReportTests(unittest.TestCase):
    def test_module_summary_counts_groups_and_public_rc_rows(self) -> None:
        summary = module_summary(SAMPLE_ROWS)
        by_group = {item["module_group"]: item for item in summary}

        self.assertEqual(by_group["settings"]["entries"], 1)
        self.assertEqual(by_group["settings"]["public_rc_rows"]["GUI-WS-04"], 1)
        self.assertEqual(by_group["terminal-command"]["next_action"], "resolve-actionable-findings")

    def test_markdown_reports_include_expected_sections(self) -> None:
        self.assertIn("zh-Hans Module Calibration Matrix", render_module_matrix(SAMPLE_ROWS))
        self.assertIn("English Preserved Review Queue", render_copy_findings(SAMPLE_ROWS))
        self.assertIn("Critical Token Mismatches", render_functional_findings(SAMPLE_ROWS))

    def test_write_reports_creates_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            write_reports(SAMPLE_ROWS, output_dir)

            self.assertTrue((output_dir / "module-matrix.md").exists())
            self.assertTrue((output_dir / "copy-review-findings.md").exists())
            self.assertTrue((output_dir / "functional-risk-findings.md").exists())

    def test_load_rows_reads_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "entries.json"
            path.write_text(json.dumps(SAMPLE_ROWS), encoding="utf-8")

            self.assertEqual(load_rows(path), SAMPLE_ROWS)


if __name__ == "__main__":
    unittest.main()
