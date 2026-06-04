#!/usr/bin/env python3

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_full_translation_audit import _audit_version_from_output_dir


class FullTranslationAuditTests(unittest.TestCase):
    def test_extracts_version_from_output_dir(self) -> None:
        self.assertEqual(
            _audit_version_from_output_dir(Path("docs/zh-Hans-full-translation-audit-0.19")),
            "0.19",
        )

    def test_falls_back_for_custom_output_dir(self) -> None:
        self.assertEqual(_audit_version_from_output_dir(Path("audit-output")), "current")


if __name__ == "__main__":
    unittest.main()
