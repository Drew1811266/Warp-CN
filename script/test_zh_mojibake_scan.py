#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_mojibake_scan import render_json, scan


class MojibakeScanTests(unittest.TestCase):
    def test_clean_chinese_text_has_no_findings(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "clean.md"
            path.write_text("设置\nAPI 密钥\n", encoding="utf-8")

            findings = scan([path], manifest_path=None)

            self.assertEqual(findings, [])

    def test_replacement_character_is_actionable(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "bad.md"
            path.write_text("坏字符 �\n", encoding="utf-8")

            findings = scan([path], manifest_path=None)

            self.assertEqual(findings[0].category, "replacement-character")
            self.assertEqual(findings[0].decision, "needs-review")

    def test_documentation_example_is_not_product_finding(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            docs = Path(tmpdir) / "docs"
            docs.mkdir()
            path = docs / "example.md"
            path.write_text("例如 mojibake: Ã\n", encoding="utf-8")

            findings = scan([path], manifest_path=None)

            self.assertEqual(findings[0].category, "mojibake-signature")
            self.assertEqual(findings[0].decision, "example-only")

    def test_json_output_is_parseable(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "bad.md"
            path.write_text("坏字符 �\n", encoding="utf-8")
            data = json.loads(render_json(scan([path], manifest_path=None)))

            self.assertEqual(data["total_findings"], 1)
            self.assertEqual(data["actionable_findings"], 1)


if __name__ == "__main__":
    unittest.main()
