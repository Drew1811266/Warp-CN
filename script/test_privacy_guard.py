#!/usr/bin/env python3

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from privacy_guard import parse_name_status_z, scan_paths


class PrivacyGuardTests(unittest.TestCase):
    def _reasons(self, *paths: str) -> dict[str, str]:
        return {finding.path: finding.reason for finding in scan_paths(Path(path) for path in paths)}

    def test_blocks_gui_smoke_artifacts_even_if_force_added(self) -> None:
        findings = self._reasons("docs/gui-smoke-artifacts/phase9/full-desktop.png")

        self.assertIn("docs/gui-smoke-artifacts/phase9/full-desktop.png", findings)
        self.assertIn("raw GUI smoke evidence", findings["docs/gui-smoke-artifacts/phase9/full-desktop.png"])

    def test_gui_smoke_artifacts_cannot_be_allowlisted(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            allowlist = root / "script" / "privacy_guard_allowlist.txt"
            allowlist.parent.mkdir()
            allowlist.write_text("docs/gui-smoke-artifacts/**\n", encoding="utf-8")

            findings = scan_paths(["docs/gui-smoke-artifacts/phase9/full-desktop.png"], repo_root=root)

        self.assertEqual(len(findings), 1)
        self.assertIn("raw GUI smoke evidence", findings[0].reason)

    def test_blocks_docs_screenshot_media_by_default(self) -> None:
        findings = self._reasons("docs/review-evidence/Screenshot 2026-06-01 at 11.34.00.png")

        self.assertIn("docs/review-evidence/Screenshot 2026-06-01 at 11.34.00.png", findings)
        self.assertIn("documentation media", findings["docs/review-evidence/Screenshot 2026-06-01 at 11.34.00.png"])

    def test_blocks_screen_recordings_outside_approved_asset_paths(self) -> None:
        findings = self._reasons("tmp/Screen Recording 2026-06-01 at 11.34.00.mov")

        self.assertIn("tmp/Screen Recording 2026-06-01 at 11.34.00.mov", findings)
        self.assertIn("screen capture", findings["tmp/Screen Recording 2026-06-01 at 11.34.00.mov"])

    def test_allows_existing_product_assets(self) -> None:
        findings = self._reasons(
            "app/assets/async/png/onboarding/welcome_agent.png",
            "app/DockTilePlugin/Resources/preview.png",
            "crates/editor/test_fixtures/images/sample1.jpg",
        )

        self.assertEqual(findings, {})

    def test_parses_git_name_status_with_renames(self) -> None:
        payload = b"A\x00docs/gui-smoke-artifacts/new.png\x00R100\x00old.png\x00docs/evidence/Screenshot.png\x00"

        entries = parse_name_status_z(payload)

        self.assertEqual(
            entries,
            [
                ("A", Path("docs/gui-smoke-artifacts/new.png")),
                ("R100", Path("docs/evidence/Screenshot.png")),
            ],
        )


if __name__ == "__main__":
    unittest.main()
