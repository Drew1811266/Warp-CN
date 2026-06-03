#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_public_rc_evidence_candidate import preflight_candidate, render_json, render_markdown
from zh_public_rc_evidence_lint import load_toml


def candidate_text(row_id: str = "GUI-SET-05") -> str:
    return f"""row_id: {row_id}
profile: zh-rc38-fixture-profile
visible_anchors:
- 设置
- AI
- AWS Bedrock
- 无效凭据
redaction: account identifiers, callback URLs, endpoint URLs, tokens, cookies, API keys, and secrets removed
cleanup_proof: fixture reset proof captured and no production state was touched
safety_confirmation: no main account, real credential, billing state, cloud capacity, team ownership, or production object was used
artifact_kind: redacted-text
"""


class PublicRcEvidenceCandidateTests(unittest.TestCase):
    def load_docs(self) -> tuple[dict[str, object], dict[str, object]]:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))
        return blockers, evidence

    def write_candidate(self, text: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "candidate.txt"
        path.write_text(text, encoding="utf-8")
        return path

    def test_accepts_safe_backend_fixture_candidate_for_human_review(self) -> None:
        blockers, evidence = self.load_docs()
        result = preflight_candidate(blockers, evidence, row_id="GUI-SET-05", artifact_path=self.write_candidate(candidate_text()))

        self.assertTrue(result.ok)
        self.assertEqual(result.row_id, "GUI-SET-05")
        self.assertEqual(result.category, "backend_fixture")
        self.assertEqual(result.decision, "candidate-ready-for-human-review")
        self.assertEqual(result.errors, ())

    def test_rejects_missing_cleanup_proof(self) -> None:
        blockers, evidence = self.load_docs()
        path = self.write_candidate(candidate_text().replace("cleanup_proof:", "cleanup_missing:"))

        result = preflight_candidate(blockers, evidence, row_id="GUI-SET-05", artifact_path=path)

        self.assertFalse(result.ok)
        self.assertIn("cleanup_proof is required", result.errors)

    def test_rejects_sensitive_looking_content(self) -> None:
        blockers, evidence = self.load_docs()
        path = self.write_candidate(candidate_text() + "debug_url: https://example.invalid/callback?token=abc\n")

        result = preflight_candidate(blockers, evidence, row_id="GUI-SET-05", artifact_path=path)

        self.assertFalse(result.ok)
        self.assertIn("sensitive-looking text in candidate artifact", result.errors)

    def test_rejects_row_mismatch(self) -> None:
        blockers, evidence = self.load_docs()
        path = self.write_candidate(candidate_text(row_id="GUI-AUTH-01"))

        result = preflight_candidate(blockers, evidence, row_id="GUI-SET-05", artifact_path=path)

        self.assertFalse(result.ok)
        self.assertIn("candidate row_id does not match requested row", result.errors)

    def test_disposable_rows_require_allowlisted_object_name(self) -> None:
        blockers, evidence = self.load_docs()
        path = self.write_candidate(
            candidate_text(row_id="GUI-SET-06").replace(
                "artifact_kind: redacted-text",
                "object_name: zh-smoke-delete-environment\nartifact_kind: redacted-text",
            )
        )

        result = preflight_candidate(blockers, evidence, row_id="GUI-SET-06", artifact_path=path)

        self.assertTrue(result.ok)
        self.assertEqual(result.decision, "candidate-ready-for-human-review")

    def test_disposable_rows_reject_wrong_object_name(self) -> None:
        blockers, evidence = self.load_docs()
        path = self.write_candidate(
            candidate_text(row_id="GUI-SET-06").replace(
                "artifact_kind: redacted-text",
                "object_name: production-environment\nartifact_kind: redacted-text",
            )
        )

        result = preflight_candidate(blockers, evidence, row_id="GUI-SET-06", artifact_path=path)

        self.assertFalse(result.ok)
        self.assertIn("object_name must be zh-smoke-delete-environment", result.errors)

    def test_json_and_markdown_outputs_are_stable(self) -> None:
        blockers, evidence = self.load_docs()
        result = preflight_candidate(blockers, evidence, row_id="GUI-SET-05", artifact_path=self.write_candidate(candidate_text()))

        data = json.loads(render_json(result))
        markdown = render_markdown(result)

        self.assertEqual(data["row_id"], "GUI-SET-05")
        self.assertEqual(data["decision"], "candidate-ready-for-human-review")
        self.assertIn("# zh-Hans Public-RC Evidence Candidate Preflight", markdown)
        self.assertIn("GUI-SET-05", markdown)
        self.assertNotIn("https://", markdown)


if __name__ == "__main__":
    unittest.main()
