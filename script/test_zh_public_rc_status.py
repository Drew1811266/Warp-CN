#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_public_rc_status import RegistryError, build_summary, load_registry, validate_registry


class PublicRcStatusTests(unittest.TestCase):
    def _write_fixture(self, tmpdir: str, content: str) -> tuple[Path, Path]:
        root = Path(tmpdir)
        handoff = root / "docs" / "handoff.md"
        handoff.parent.mkdir()
        handoff.write_text("# handoff\n", encoding="utf-8")
        registry = root / "registry.toml"
        registry.write_text(content.replace("HANDOFF", "docs/handoff.md"), encoding="utf-8")
        return root, registry

    def test_valid_registry_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root, registry = self._write_fixture(
                tmpdir,
                '''
[[blocker]]
id = "GUI-AUTH-01"
category = "isolated_account"
status = "blocked-no-isolated-account"
reason = "Requires isolated account."
required_evidence = ["account", "redacted screenshot"]
handoff_doc = "HANDOFF"
safety_rule = "Do not use main account."
public_rc_required = true
local_fixture_allowed = false
'''.strip(),
            )

            blockers = load_registry(registry)
            validate_registry(blockers, root)
            summary = build_summary(blockers)

            self.assertEqual(summary["total"], 1)
            self.assertEqual(summary["statuses"], {"blocked-no-isolated-account": 1})
            self.assertEqual(summary["categories"], {"isolated_account": 1})

    def test_duplicate_blocker_id_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root, registry = self._write_fixture(
                tmpdir,
                '''
[[blocker]]
id = "GUI-AUTH-01"
category = "isolated_account"
status = "blocked-no-isolated-account"
reason = "Requires isolated account."
required_evidence = ["account"]
handoff_doc = "HANDOFF"
safety_rule = "Do not use main account."
public_rc_required = true
local_fixture_allowed = false

[[blocker]]
id = "GUI-AUTH-01"
category = "isolated_account"
status = "blocked-no-isolated-account"
reason = "Requires isolated account."
required_evidence = ["account"]
handoff_doc = "HANDOFF"
safety_rule = "Do not use main account."
public_rc_required = true
local_fixture_allowed = false
'''.strip(),
            )

            blockers = load_registry(registry)
            with self.assertRaisesRegex(RegistryError, "duplicate blocker id"):
                validate_registry(blockers, root)

    def test_missing_required_field_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root, registry = self._write_fixture(
                tmpdir,
                '''
[[blocker]]
id = "GUI-AUTH-01"
category = "isolated_account"
status = "blocked-no-isolated-account"
reason = "Requires isolated account."
required_evidence = ["account"]
handoff_doc = "HANDOFF"
public_rc_required = true
local_fixture_allowed = false
'''.strip(),
            )

            blockers = load_registry(registry)
            with self.assertRaisesRegex(RegistryError, "missing fields"):
                validate_registry(blockers, root)

    def test_missing_handoff_doc_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            registry = root / "registry.toml"
            registry.write_text(
                '''
[[blocker]]
id = "GUI-AUTH-01"
category = "isolated_account"
status = "blocked-no-isolated-account"
reason = "Requires isolated account."
required_evidence = ["account"]
handoff_doc = "docs/missing.md"
safety_rule = "Do not use main account."
public_rc_required = true
local_fixture_allowed = false
'''.strip(),
                encoding="utf-8",
            )

            blockers = load_registry(registry)
            with self.assertRaisesRegex(RegistryError, "handoff_doc does not exist"):
                validate_registry(blockers, root)

    def test_json_output_shape(self) -> None:
        result = subprocess.run(
            [sys.executable, "script/zh_public_rc_status.py", "--json"],
            check=True,
            stdout=subprocess.PIPE,
            text=True,
        )

        summary = json.loads(result.stdout)

        self.assertEqual(summary["total"], 11)
        self.assertEqual(summary["public_rc_required"], 11)
        self.assertIn("blocked-no-backend-fixture", summary["statuses"])
        self.assertEqual(len(summary["blockers"]), 11)

    def test_default_registry_smoke(self) -> None:
        blockers = load_registry(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        validate_registry(blockers, Path("."))
        summary = build_summary(blockers)

        self.assertEqual(summary["total"], 11)
        self.assertEqual(summary["statuses"]["blocked-no-isolated-account"], 3)
        self.assertEqual(summary["statuses"]["blocked-no-backend-fixture"], 5)
        self.assertEqual(summary["statuses"]["blocked-no-disposable-object"], 3)


if __name__ == "__main__":
    unittest.main()
