#!/usr/bin/env python3

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_apply_localization import (
    GlossaryConfig,
    check_glossary,
    load_glossary_config,
    load_manifest,
    metadata_summary,
    metadata_summary_report,
    print_metadata_summary,
    replace_rust_string_literals_many,
    replace_rust_string_literals_many_apply,
    validate_manifest,
)


class ManifestValidationTests(unittest.TestCase):
    def _load(self, content: str) -> list[dict[str, object]]:
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = Path(tmpdir) / "manifest.toml"
            manifest_path.write_text(content, encoding="utf-8")
            return load_manifest(manifest_path)

    def test_loads_v2_metadata_fields(self) -> None:
        replacements = self._load(
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

        self.assertEqual(replacements[0]["key"], "settings.ai.bedrock.login_command")
        self.assertEqual(replacements[0]["context"], "AI settings AWS Bedrock credentials form label")
        self.assertEqual(replacements[0]["status"], "active")
        self.assertEqual(replacements[0]["preserve_terms"], ["AWS Bedrock", "Warp"])
        self.assertEqual(replacements[0]["notes"], "Keep provider names in English.")
        self.assertEqual(validate_manifest(replacements), [])

    def test_accepts_v1_entries_without_v2_metadata(self) -> None:
        replacements = self._load(
            '''
[[replace]]
path = "app/src/example.rs"
source = "Open"
target = "打开"
'''.strip()
        )

        self.assertEqual(validate_manifest(replacements), [])

    def test_rejects_duplicate_v2_keys(self) -> None:
        replacements = self._load(
            '''
[[replace]]
key = "workspace.open"
path = "app/src/one.rs"
source = "Open"
target = "打开"

[[replace]]
key = "workspace.open"
path = "app/src/two.rs"
source = "Open"
target = "打开"
'''.strip()
        )

        errors = validate_manifest(replacements)

        self.assertTrue(any("duplicate key" in error for error in errors))

    def test_rejects_invalid_status(self) -> None:
        replacements = self._load(
            '''
[[replace]]
key = "workspace.open"
path = "app/src/example.rs"
source = "Open"
target = "打开"
status = "todo"
'''.strip()
        )

        errors = validate_manifest(replacements)

        self.assertTrue(any("invalid status" in error for error in errors))


class ManifestMetadataSummaryTests(unittest.TestCase):
    def test_counts_v2_metadata_coverage(self) -> None:
        replacements: list[dict[str, object]] = [
            {
                "path": "app/src/workspace/view.rs",
                "source": "Open",
                "target": "打开",
                "key": "workspace.open",
                "context": "Workspace toolbar action",
                "status": "active",
                "expected_count": 1,
            },
            {
                "path": "app/src/settings_view/mod.rs",
                "source": "Settings",
                "target": "设置",
                "status": "needs-review",
            },
        ]

        summary = metadata_summary(replacements)

        self.assertEqual(summary["entries"], 2)
        self.assertEqual(summary["key"], 1)
        self.assertEqual(summary["context"], 1)
        self.assertEqual(summary["status"], 2)
        self.assertEqual(summary["expected_count"], 1)
        self.assertEqual(summary["preserve_terms"], 0)

    def test_metadata_summary_report_includes_percentages(self) -> None:
        replacements: list[dict[str, object]] = [
            {
                "path": "app/src/workspace/view.rs",
                "source": "Open",
                "target": "打开",
                "key": "workspace.open",
                "context": "Workspace toolbar action",
                "status": "active",
                "expected_count": 1,
            },
            {
                "path": "app/src/settings_view/mod.rs",
                "source": "Settings",
                "target": "设置",
                "status": "needs-review",
            },
        ]

        report = metadata_summary_report(replacements)

        self.assertEqual(report["entries"], 2)
        self.assertEqual(report["key"], {"count": 1, "percent": 50.0})
        self.assertEqual(report["context"], {"count": 1, "percent": 50.0})
        self.assertEqual(report["status"], {"count": 2, "percent": 100.0})
        self.assertEqual(report["expected_count"], {"count": 1, "percent": 50.0})
        self.assertEqual(report["preserve_terms"], {"count": 0, "percent": 0.0})

    def test_prints_metadata_summary_as_json(self) -> None:
        replacements: list[dict[str, object]] = [
            {
                "path": "app/src/workspace/view.rs",
                "source": "Open Warp",
                "target": "打开 Warp",
                "key": "workspace.open_warp",
                "context": "Workspace action",
                "status": "active",
                "preserve_terms": ["Warp"],
                "expected_count": 1,
            },
        ]

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            print_metadata_summary(replacements, json_output=True)

        payload = json.loads(output.getvalue())
        self.assertEqual(payload["entries"], 1)
        self.assertEqual(payload["key"], {"count": 1, "percent": 100.0})
        self.assertEqual(payload["preserve_terms"], {"count": 1, "percent": 100.0})


class GlossaryValidationTests(unittest.TestCase):
    def _load_glossary(self, content: str) -> GlossaryConfig:
        with tempfile.TemporaryDirectory() as tmpdir:
            glossary_path = Path(tmpdir) / "glossary.toml"
            glossary_path.write_text(content, encoding="utf-8")
            return load_glossary_config(glossary_path)

    def test_loads_glossary_config(self) -> None:
        glossary = self._load_glossary(
            '''
preserve_terms = ["Warp", "Agent"]
required_translations = ["Command Palette => 命令面板"]
forbidden_targets = ["智能体"]
'''.strip()
        )

        self.assertEqual(glossary.preserve_terms, ("Warp", "Agent"))
        self.assertEqual(glossary.required_translations, (("Command Palette", "命令面板"),))
        self.assertEqual(glossary.forbidden_targets, ("智能体",))

    def test_reports_missing_preserved_term(self) -> None:
        errors = check_glossary(
            [
                {
                    "__line": 10,
                    "path": "app/src/example.rs",
                    "source": "Open Warp Drive",
                    "target": "打开云端硬盘",
                }
            ],
            GlossaryConfig(preserve_terms=("Warp Drive",)),
        )

        self.assertTrue(any("missing preserved term" in error for error in errors))

    def test_reports_required_translation_mismatch(self) -> None:
        errors = check_glossary(
            [
                {
                    "__line": 11,
                    "path": "app/src/example.rs",
                    "source": "Open Command Palette",
                    "target": "打开命令板",
                }
            ],
            GlossaryConfig(required_translations=(("Command Palette", "命令面板"),)),
        )

        self.assertTrue(any("expected translation" in error for error in errors))

    def test_reports_forbidden_target_term(self) -> None:
        errors = check_glossary(
            [
                {
                    "__line": 12,
                    "path": "app/src/example.rs",
                    "source": "Agent",
                    "target": "智能体",
                }
            ],
            GlossaryConfig(forbidden_targets=("智能体",)),
        )

        self.assertTrue(any("forbidden target term" in error for error in errors))


class RustStringReplacementTests(unittest.TestCase):
    def test_escapes_quotes_when_replacing_normal_string_literals(self) -> None:
        source = 'do shell script "ln -sf {source} {target}"'
        target = 'do shell script "ln -sf {source} {target}" with prompt "需要管理员权限。"'
        text = 'let script = "do shell script \\"ln -sf {source} {target}\\"";\n'

        updated, found_counts, target_counts = replace_rust_string_literals_many_apply(
            text,
            {source: target},
        )

        self.assertEqual(found_counts[source], 1)
        self.assertEqual(target_counts[source], 0)
        self.assertEqual(
            updated,
            'let script = "do shell script \\"ln -sf {source} {target}\\" with prompt \\"需要管理员权限。\\"";\n',
        )

        found_counts, target_counts = replace_rust_string_literals_many(
            updated,
            {source: target},
        )
        self.assertEqual(found_counts[source], 0)
        self.assertEqual(target_counts[source], 1)


if __name__ == "__main__":
    unittest.main()
