#!/usr/bin/env python3

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_full_translation_audit import (
    _audit_version_from_output_dir,
    _machine_copy_score,
    _module_group_for_path,
    _module_for_path,
    _mojibake_status,
    _review_lane,
    _ui_density_risk,
)


class FullTranslationAuditTests(unittest.TestCase):
    def test_extracts_version_from_output_dir(self) -> None:
        self.assertEqual(
            _audit_version_from_output_dir(Path("docs/zh-Hans-full-translation-audit-0.19")),
            "0.19",
        )

    def test_falls_back_for_custom_output_dir(self) -> None:
        self.assertEqual(_audit_version_from_output_dir(Path("audit-output")), "current")


class FullTranslationAuditCalibrationFieldTests(unittest.TestCase):
    def test_module_group_for_known_paths(self) -> None:
        self.assertEqual(_module_group_for_path("app/src/ai/agent/mod.rs"), "ai-agent")
        self.assertEqual(_module_group_for_path("app/src/terminal/view.rs"), "terminal-command")
        self.assertEqual(_module_group_for_path("app/src/settings_view/teams_page.rs"), "teams-ownership")
        self.assertEqual(_module_group_for_path("app/src/settings_view/billing_and_usage_page.rs"), "billing-quota")
        self.assertEqual(_module_group_for_path("crates/onboarding/src/slides/intro_slide.rs"), "onboarding")
        self.assertEqual(_module_for_path("app/src/settings_view/ai_page.rs"), "app/src/settings_view")

    def test_mojibake_status_identifies_target_issue(self) -> None:
        self.assertEqual(_mojibake_status("Open", "打开"), "clean")
        self.assertEqual(_mojibake_status("Open", "Ã¦"), "target-issue")

    def test_ui_density_risk_flags_long_compact_copy(self) -> None:
        risk = _ui_density_risk(
            "app/src/settings_view/mod.rs",
            "Save",
            "保存当前设置并立即应用到所有可见工作区视图",
            "Settings button label",
        )

        self.assertIn(risk, {"note", "high"})

    def test_machine_copy_score_and_lane_are_deterministic(self) -> None:
        self.assertEqual(
            _machine_copy_score(
                copy_status="issue",
                copy_notes=["forbidden project term"],
                risk_tags=[],
                ui_density_risk="clean",
                mojibake_status="clean",
            ),
            0,
        )
        self.assertEqual(
            _machine_copy_score(
                copy_status="clean",
                copy_notes=[],
                risk_tags=["english-preserved"],
                ui_density_risk="clean",
                mojibake_status="clean",
            ),
            1,
        )
        self.assertEqual(
            _review_lane(
                decision="blocked-public-rc",
                functional_status="clean",
                copy_status="clean",
                public_rc_rows=["GUI-BILL-01"],
                ui_density_risk="clean",
                mojibake_status="clean",
            ),
            "public-rc",
        )


if __name__ == "__main__":
    unittest.main()
