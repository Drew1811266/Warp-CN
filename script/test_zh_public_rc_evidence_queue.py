#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_public_rc_evidence_lint import load_toml
from zh_public_rc_evidence_queue import (
    build_queue,
    filter_queue,
    render_json,
    render_markdown,
)


class PublicRcEvidenceQueueTests(unittest.TestCase):
    def test_current_queue_contains_all_missing_rows_with_priority(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        queue = build_queue(blockers, evidence)

        self.assertEqual(len(queue), 11)
        self.assertEqual(queue[0].row_id, "GUI-BILL-01")
        self.assertEqual(queue[0].category, "backend_fixture")
        self.assertEqual(queue[0].priority, 10)
        self.assertEqual(queue[0].approval_gate, "fixture-owner-approval")
        self.assertEqual(queue[0].artifact_path, "artifacts/redacted/gui-bill-01.txt")

    def test_filter_queue_by_category_and_row_id(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        queue = build_queue(blockers, evidence)
        backend_queue = filter_queue(queue, categories=("backend_fixture",))
        row_queue = filter_queue(queue, row_ids=("GUI-SET-05",))

        self.assertEqual(len(backend_queue), 5)
        self.assertTrue(all(row.category == "backend_fixture" for row in backend_queue))
        self.assertEqual([row.row_id for row in row_queue], ["GUI-SET-05"])

    def test_json_output_has_stable_counts_and_no_ready_rows(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        data = json.loads(render_json(build_queue(blockers, evidence)))

        self.assertEqual(data["total_rows"], 11)
        self.assertEqual(data["decision"], "blocked-until-queue-cleared")
        self.assertEqual(data["category_counts"]["backend_fixture"], 5)
        self.assertEqual(data["rows"][0]["row_id"], "GUI-BILL-01")
        self.assertEqual(data["rows"][0]["approval_gate"], "fixture-owner-approval")

    def test_markdown_output_is_safe_and_scoped(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        markdown = render_markdown(filter_queue(build_queue(blockers, evidence), row_ids=("GUI-SET-05",)))

        self.assertIn("# zh-Hans Public-RC Evidence Collection Queue", markdown)
        self.assertIn("## GUI-SET-05", markdown)
        self.assertIn("artifacts/redacted/gui-set-05.txt", markdown)
        self.assertIn("fixture-owner-approval", markdown)
        self.assertNotIn("GUI-AUTH-01", markdown)
        self.assertNotIn("@", markdown)
        self.assertNotIn("https://", markdown)

    def test_ready_rows_are_omitted_from_queue(self) -> None:
        blockers = {
            "blocker": [
                {
                    "id": "GUI-SET-05",
                    "category": "backend_fixture",
                    "status": "blocked-no-backend-fixture",
                    "handoff_doc": "docs/zh-Hans-backend-fixture-contract-rc19.md",
                    "safety_rule": "Use safe invalid marker values only.",
                    "required_evidence": ["invalid credential fixture"],
                    "public_rc_required": True,
                    "local_fixture_allowed": True,
                }
            ]
        }
        evidence = {
            "evidence": [
                {
                    "row_id": "GUI-SET-05",
                    "status": "provided",
                    "evidence_paths": ["artifacts/redacted/gui-set-05.txt"],
                    "cleanup_proof": "fixture reset proof captured",
                    "redaction": "identifiers removed",
                    "notes": "safe marker only",
                }
            ]
        }

        queue = build_queue(blockers, evidence)

        self.assertEqual(queue, ())


if __name__ == "__main__":
    unittest.main()
