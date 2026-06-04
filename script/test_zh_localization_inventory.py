#!/usr/bin/env python3

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_localization_inventory import (
    InventoryIgnoreConfig,
    is_candidate_literal,
    is_excluded_path,
    load_ignore_config,
)


class InventoryIgnoreConfigTests(unittest.TestCase):
    def _load(self, content: str) -> InventoryIgnoreConfig:
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "ignore.toml"
            config_path.write_text(content, encoding="utf-8")
            return load_ignore_config(config_path)

    def test_loads_external_ignore_config(self) -> None:
        config = self._load(
            '''
path_parts = ["/generated/"]
exact_paths = ["app/src/generated/schema.rs"]
line_patterns = ["internal_ui_name(", "#[cfg"]
literal_patterns = ["^internal-[a-z]+$"]
internal_words = ["localhost"]
'''.strip()
        )

        self.assertEqual(config.path_parts, ("/generated/",))
        self.assertEqual(config.exact_paths, ("app/src/generated/schema.rs",))
        self.assertEqual(config.line_patterns, ("internal_ui_name(", "#[cfg"))
        self.assertEqual(config.literal_patterns, ("^internal-[a-z]+$",))
        self.assertEqual(config.internal_words, ("localhost",))

    def test_external_config_excludes_paths(self) -> None:
        config = InventoryIgnoreConfig(
            path_parts=("/generated/",),
            exact_paths=("app/src/generated/schema.rs",),
        )

        self.assertTrue(is_excluded_path(Path("app/src/generated/schema.rs"), config))
        self.assertTrue(is_excluded_path(Path("app/src/generated/view.rs"), config))
        self.assertFalse(is_excluded_path(Path("app/src/visible/view.rs"), config))

    def test_external_config_filters_candidate_literals(self) -> None:
        config = InventoryIgnoreConfig(
            line_patterns=("internal_ui_name(",),
            literal_patterns=(r"^internal-[a-z]+$",),
            internal_words=("localhost",),
        )

        self.assertFalse(is_candidate_literal("Visible title", 'internal_ui_name("Visible title")', config))
        self.assertFalse(is_candidate_literal("internal-modal", 'label("internal-modal")', config))
        self.assertFalse(is_candidate_literal("localhost", 'label("localhost")', config))
        self.assertTrue(is_candidate_literal("Visible title", 'label("Visible title")', config))

    def test_filters_keybinding_literals_with_punctuation(self) -> None:
        config = InventoryIgnoreConfig()

        self.assertFalse(is_candidate_literal("cmdorctrl-,", 'binding("cmdorctrl-,")', config))
        self.assertFalse(is_candidate_literal("cmdorctrl-=", 'binding("cmdorctrl-=")', config))
        self.assertFalse(is_candidate_literal("cmdorctrl--", 'binding("cmdorctrl--")', config))
        self.assertFalse(is_candidate_literal("ctrl-shift->", 'binding("ctrl-shift->")', config))
        self.assertFalse(is_candidate_literal("shift-cmd-{", 'binding("shift-cmd-{")', config))
        self.assertFalse(is_candidate_literal("alt-{}", 'binding("alt-{}")', config))
        self.assertFalse(is_candidate_literal("cmd-meta-y", 'binding("cmd-meta-y")', config))
        self.assertFalse(is_candidate_literal("shift-?", 'binding("shift-?")', config))
        self.assertTrue(is_candidate_literal("Dark", 'label("Dark")', config))


if __name__ == "__main__":
    unittest.main()
