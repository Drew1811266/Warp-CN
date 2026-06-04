#!/usr/bin/env python3

from __future__ import annotations

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_public_rc_evidence_lint import lint_evidence, load_toml


class PublicRcEvidenceLintTests(unittest.TestCase):
    def write_temp(self, content: str) -> Path:
        temp = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".toml", delete=False)
        temp.write(textwrap.dedent(content).strip() + "\n")
        temp.close()
        return Path(temp.name)

    def test_empty_evidence_reports_missing_required_rows(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence_path = self.write_temp(
            """
            generated_on = "2026-06-02"
            [[evidence]]
            row_id = "GUI-AUTH-01"
            status = "missing"
            evidence_paths = []
            cleanup_proof = ""
            redaction = "none"
            notes = "not provided"
            """
        )

        result = lint_evidence(blockers, load_toml(evidence_path))

        self.assertFalse(result.ok)
        self.assertEqual(result.total_required, 11)
        self.assertIn("GUI-AUTH-01: missing evidence", result.errors)

    def test_complete_safe_fixture_row_passes(self) -> None:
        blockers = {
            "blocker": [
                {
                    "id": "GUI-SET-05",
                    "category": "backend_fixture",
                    "required_evidence": ["invalid credential fixture", "redacted error GUI evidence"],
                    "public_rc_required": True,
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
                    "redaction": "email, token, key, endpoint url removed",
                    "notes": "uses zh-smoke-invalid-token only",
                }
            ]
        }

        result = lint_evidence(blockers, evidence)

        self.assertTrue(result.ok)
        self.assertEqual(result.ready_rows, ("GUI-SET-05",))

    def test_rejects_unknown_row(self) -> None:
        blockers = {"blocker": []}
        evidence = {
            "evidence": [
                {
                    "row_id": "GUI-NOT-REAL",
                    "status": "provided",
                    "evidence_paths": ["artifacts/redacted/gui-not-real.txt"],
                    "cleanup_proof": "cleanup proof captured",
                    "redaction": "identifiers removed",
                    "notes": "unknown",
                }
            ]
        }

        result = lint_evidence(blockers, evidence)

        self.assertFalse(result.ok)
        self.assertIn("GUI-NOT-REAL: unknown row_id", result.errors)

    def test_rejects_sensitive_terms_in_committable_metadata(self) -> None:
        blockers = {
            "blocker": [
                {
                    "id": "GUI-AUTH-01",
                    "category": "isolated_account",
                    "required_evidence": ["isolated account", "redacted login"],
                    "public_rc_required": True,
                }
            ]
        }
        evidence = {
            "evidence": [
                {
                    "row_id": "GUI-AUTH-01",
                    "status": "provided",
                    "evidence_paths": ["artifacts/redacted/gui-auth-01.txt"],
                    "cleanup_proof": "logout captured",
                    "redaction": "token removed",
                    "notes": "test email is person@example.com",
                }
            ]
        }

        result = lint_evidence(blockers, evidence)

        self.assertFalse(result.ok)
        self.assertIn("GUI-AUTH-01: sensitive-looking metadata in notes", result.errors)

    def test_strict_artifacts_rejects_missing_referenced_path(self) -> None:
        blockers = {
            "blocker": [
                {
                    "id": "GUI-SET-05",
                    "category": "backend_fixture",
                    "required_evidence": ["invalid credential fixture"],
                    "public_rc_required": True,
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

        result = lint_evidence(blockers, evidence, strict_artifacts=True, repo_root=Path("/tmp/nonexistent-warp-cn"))

        self.assertFalse(result.ok)
        self.assertIn("GUI-SET-05: referenced artifact does not exist: artifacts/redacted/gui-set-05.txt", result.errors)

    def test_strict_artifacts_rejects_sensitive_artifact_text(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            artifact = Path(root) / "artifacts/redacted/gui-set-05.txt"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("email person@example.com leaked\n", encoding="utf-8")
            blockers = {
                "blocker": [
                    {
                        "id": "GUI-SET-05",
                        "category": "backend_fixture",
                        "required_evidence": ["invalid credential fixture"],
                        "public_rc_required": True,
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

            result = lint_evidence(blockers, evidence, strict_artifacts=True, repo_root=Path(root))

        self.assertFalse(result.ok)
        self.assertIn("GUI-SET-05: sensitive-looking text in artifact artifacts/redacted/gui-set-05.txt", result.errors)

    def test_strict_artifacts_accepts_safe_redacted_text(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            artifact = Path(root) / "artifacts/redacted/gui-set-05.txt"
            artifact.parent.mkdir(parents=True)
            artifact.write_text(
                "row: GUI-SET-05\nredacted evidence summary only\nfixture reset proof reviewed\n",
                encoding="utf-8",
            )
            blockers = {
                "blocker": [
                    {
                        "id": "GUI-SET-05",
                        "category": "backend_fixture",
                        "required_evidence": ["invalid credential fixture"],
                        "public_rc_required": True,
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

            result = lint_evidence(blockers, evidence, strict_artifacts=True, repo_root=Path(root))

        self.assertTrue(result.ok)
        self.assertEqual(result.ready_rows, ("GUI-SET-05",))

    def test_strict_artifacts_rejects_wrong_row_artifact_path(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            artifact = Path(root) / "artifacts/redacted/gui-auth-01.txt"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("safe redacted text for another row\n", encoding="utf-8")
            blockers = {
                "blocker": [
                    {
                        "id": "GUI-SET-05",
                        "category": "backend_fixture",
                        "required_evidence": ["invalid credential fixture"],
                        "public_rc_required": True,
                    }
                ]
            }
            evidence = {
                "evidence": [
                    {
                        "row_id": "GUI-SET-05",
                        "status": "provided",
                        "evidence_paths": ["artifacts/redacted/gui-auth-01.txt"],
                        "cleanup_proof": "fixture reset proof captured",
                        "redaction": "identifiers removed",
                        "notes": "safe marker only",
                    }
                ]
            }

            result = lint_evidence(blockers, evidence, strict_artifacts=True, repo_root=Path(root))

        self.assertFalse(result.ok)
        self.assertIn(
            "GUI-SET-05: evidence_paths must include artifacts/redacted/gui-set-05.txt",
            result.errors,
        )


if __name__ == "__main__":
    unittest.main()
