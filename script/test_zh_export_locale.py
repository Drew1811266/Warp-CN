#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_apply_localization import load_manifest
from zh_export_locale import build_locale_entries, render_json, render_yaml


class LocaleExportTests(unittest.TestCase):
    def _load_manifest(self, content: str) -> list[dict[str, object]]:
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = Path(tmpdir) / "manifest.toml"
            manifest_path.write_text(content, encoding="utf-8")
            return load_manifest(manifest_path)

    def test_builds_export_entries_without_internal_fields(self) -> None:
        replacements = self._load_manifest(
            '''
[[replace]]
key = "settings.ai.bedrock.login_command"
path = "app/src/settings_view/ai_page.rs"
source = "Login Command"
target = "登录命令"
context = "AI settings AWS Bedrock credentials form label"
status = "active"
preserve_terms = ["AWS Bedrock", "Warp"]
notes = "Keep provider names in English."
expected_count = 1
'''.strip()
        )

        entries = build_locale_entries(replacements)

        self.assertEqual(
            entries,
            [
                {
                    "key": "settings.ai.bedrock.login_command",
                    "path": "app/src/settings_view/ai_page.rs",
                    "source": "Login Command",
                    "target": "登录命令",
                    "context": "AI settings AWS Bedrock credentials form label",
                    "status": "active",
                    "preserve_terms": ["AWS Bedrock", "Warp"],
                    "notes": "Keep provider names in English.",
                }
            ],
        )
        self.assertNotIn("__line", entries[0])
        self.assertNotIn("expected_count", entries[0])

    def test_json_export_is_parseable_utf8(self) -> None:
        entries = [
            {
                "key": "workspace.open",
                "path": "app/src/example.rs",
                "source": "Open",
                "target": "打开",
                "context": "",
                "status": "",
                "preserve_terms": [],
                "notes": "",
            }
        ]

        rendered = render_json(entries)

        self.assertEqual(json.loads(rendered)[0]["target"], "打开")

    def test_yaml_export_is_human_readable(self) -> None:
        entries = [
            {
                "key": "workspace.open",
                "path": "app/src/example.rs",
                "source": "Open",
                "target": "打开",
                "context": "Toolbar action",
                "status": "active",
                "preserve_terms": ["Warp"],
                "notes": "",
            }
        ]

        rendered = render_yaml(entries)

        self.assertIn("- key: \"workspace.open\"", rendered)
        self.assertIn("  target: \"打开\"", rendered)
        self.assertIn("  preserve_terms:", rendered)
        self.assertIn("    - \"Warp\"", rendered)

    def test_yaml_export_uses_inline_empty_arrays(self) -> None:
        entries = [
            {
                "key": "",
                "path": "app/src/example.rs",
                "source": "Open",
                "target": "打开",
                "context": "",
                "status": "",
                "preserve_terms": [],
                "notes": "",
            }
        ]

        rendered = render_yaml(entries)

        self.assertIn("  preserve_terms: []", rendered)


if __name__ == "__main__":
    unittest.main()
