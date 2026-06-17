#!/usr/bin/env python3

from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WINDOWS_INSTALLER = REPO_ROOT / "script" / "windows" / "windows-installer.iss"
WINDOWS_BUNDLE = REPO_ROOT / "script" / "windows" / "bundle.ps1"


class WindowsInstallerLocalizationTests(unittest.TestCase):
    def test_installer_uses_simplified_chinese_language_pack(self) -> None:
        installer = WINDOWS_INSTALLER.read_text(encoding="utf-8")

        self.assertIn('Name: "chinesesimplified"', installer)
        self.assertIn('MessagesFile: "compiler:Languages\\ChineseSimplified.isl"', installer)

    def test_windows_shell_visible_strings_use_chinese_custom_messages(self) -> None:
        installer = WINDOWS_INSTALLER.read_text(encoding="utf-8")

        self.assertIn("chinesesimplified.PathTask=将 Warp 添加到 PATH", installer)
        self.assertIn("chinesesimplified.TabContextAction=用 %1 在新标签页中打开", installer)
        self.assertIn("chinesesimplified.WindowContextAction=用 %1 在新窗口中打开", installer)
        self.assertIn('Description: "{cm:PathTask}"', installer)
        self.assertEqual(installer.count('ValueData: "{cm:TabContextAction,{#MyAppName}}"'), 2)
        self.assertEqual(installer.count('ValueData: "{cm:WindowContextAction,{#MyAppName}}"'), 2)

    def test_installer_does_not_leave_known_windows_ui_strings_in_english(self) -> None:
        installer = WINDOWS_INSTALLER.read_text(encoding="utf-8")
        visible_english = [
            "Add Warp to PATH",
            "Open {#MyAppName} in new tab",
            "Open {#MyAppName} in new window",
        ]

        for text in visible_english:
            with self.subTest(text=text):
                self.assertNotIn(text, installer)


class WindowsBundleNamingTests(unittest.TestCase):
    def test_oss_windows_release_output_name_is_warp_cn_specific(self) -> None:
        bundle = WINDOWS_BUNDLE.read_text(encoding="utf-8")

        self.assertRegex(
            bundle,
            re.compile(
                r'\$INSTALLER_NAME\s*=\s*"Warp-CN-\$\(\$RELEASE_VERSION\)-windows-\$\(\$ARCH\)-oss-\$\(\$SIGNING_LABEL\)"'
            ),
        )
        self.assertIn('"/DMyAppVersion=$RELEASE_VERSION"', bundle)


if __name__ == "__main__":
    unittest.main()
