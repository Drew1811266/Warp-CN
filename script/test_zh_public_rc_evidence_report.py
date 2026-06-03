#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_public_rc_evidence_lint import load_toml
from zh_public_rc_evidence_report import (
    build_report,
    filter_actions,
    missing_actions,
    render_json,
    render_missing_action_markdown,
    render_missing_actions,
    render_missing_actions_json,
    render_templates,
    render_text,
)


class PublicRcEvidenceReportTests(unittest.TestCase):
    def test_current_empty_ledger_summary(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        report = build_report(blockers, evidence)

        self.assertEqual(report.total_required, 11)
        self.assertEqual(report.ready_rows, ())
        self.assertEqual(report.status_counts["missing"], 11)
        self.assertEqual(report.category_counts["backend_fixture"], 5)
        self.assertEqual(report.category_counts["disposable_object"], 3)
        self.assertEqual(report.category_counts["isolated_account"], 3)

    def test_text_report_contains_lane_counts(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        text = render_text(build_report(blockers, evidence))

        self.assertIn("backend_fixture: total=5 ready=0 missing=5", text)
        self.assertIn("disposable_object: total=3 ready=0 missing=3", text)
        self.assertIn("isolated_account: total=3 ready=0 missing=3", text)
        self.assertIn("decision: blocked", text)

    def test_json_report_contains_stable_counts_and_rows(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        data = json.loads(render_json(build_report(blockers, evidence)))

        self.assertEqual(data["total_required"], 11)
        self.assertEqual(data["ready_rows"], [])
        self.assertEqual(data["decision"], "blocked")
        self.assertEqual(data["category_counts"]["backend_fixture"], 5)
        self.assertEqual(data["category_ready_counts"].get("backend_fixture", 0), 0)
        self.assertEqual(data["rows"][0]["row_id"], "GUI-AUTH-01")
        self.assertEqual(data["rows"][0]["status"], "missing")

    def test_template_output_uses_redacted_paths(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))

        templates = render_templates(blockers)

        self.assertIn('row_id = "GUI-SET-05"', templates)
        self.assertIn('evidence_paths = ["artifacts/redacted/gui-set-05.txt"]', templates)
        self.assertNotIn("@", templates)
        self.assertNotIn("https://", templates)

    def test_missing_actions_include_handoff_and_redacted_path(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        actions = render_missing_actions(blockers, evidence)

        self.assertIn("row_id: GUI-AUTH-01", actions)
        self.assertIn("category: isolated_account", actions)
        self.assertIn("handoff_doc: docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md", actions)
        self.assertIn("artifact_path: artifacts/redacted/gui-auth-01.txt", actions)
        self.assertIn("- isolated browser-login test account", actions)
        self.assertIn("safety_rule:", actions)
        self.assertNotIn("person@example.com", actions)
        self.assertNotIn("https://", actions)

    def test_missing_actions_omit_ready_rows(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = {
            "evidence": [
                {
                    "row_id": "GUI-AUTH-01",
                    "status": "provided",
                    "evidence_paths": ["artifacts/redacted/gui-auth-01.txt"],
                    "cleanup_proof": "redacted cleanup proof reviewed",
                    "redaction": "identifiers removed",
                    "notes": "safe isolated account packet",
                }
            ]
        }

        actions = render_missing_actions(blockers, evidence)

        self.assertNotIn("row_id: GUI-AUTH-01", actions)
        self.assertIn("row_id: GUI-SET-03", actions)

    def test_missing_actions_data_is_structured_and_safe(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        actions = missing_actions(blockers, evidence)

        self.assertEqual(len(actions), 11)
        self.assertEqual(actions[0]["row_id"], "GUI-AUTH-01")
        self.assertEqual(actions[0]["artifact_path"], "artifacts/redacted/gui-auth-01.txt")
        self.assertIn("required_evidence", actions[0])
        self.assertIn("safety_rule", actions[0])

    def test_missing_actions_json_contains_actions_and_decision(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        data = json.loads(render_missing_actions_json(blockers, evidence))

        self.assertEqual(data["total_actions"], 11)
        self.assertEqual(data["decision"], "blocked-until-matching-evidence-is-reviewed")
        self.assertEqual(data["actions"][0]["row_id"], "GUI-AUTH-01")
        self.assertEqual(data["actions"][0]["category"], "isolated_account")

    def test_filter_actions_by_row_id(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        actions = filter_actions(missing_actions(blockers, evidence), row_ids=("GUI-SET-05",))

        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["row_id"], "GUI-SET-05")
        self.assertEqual(actions[0]["artifact_path"], "artifacts/redacted/gui-set-05.txt")

    def test_filter_actions_by_category(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        actions = filter_actions(missing_actions(blockers, evidence), categories=("backend_fixture",))

        self.assertEqual(len(actions), 5)
        self.assertTrue(all(action["category"] == "backend_fixture" for action in actions))

    def test_filter_actions_allows_empty_result(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        actions = filter_actions(missing_actions(blockers, evidence), row_ids=("GUI-NOT-REAL",))

        self.assertEqual(actions, ())

    def test_missing_action_markdown_is_row_scoped_and_safe(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        markdown = render_missing_action_markdown(blockers, evidence, row_ids=("GUI-SET-05",))

        self.assertIn("# zh-Hans Public-RC Missing Evidence Action Packet", markdown)
        self.assertIn("## GUI-SET-05", markdown)
        self.assertIn("artifacts/redacted/gui-set-05.txt", markdown)
        self.assertIn("Use only safe invalid marker values", markdown)
        self.assertNotIn("GUI-AUTH-01", markdown)
        self.assertNotIn("@", markdown)
        self.assertNotIn("https://", markdown)


if __name__ == "__main__":
    unittest.main()
