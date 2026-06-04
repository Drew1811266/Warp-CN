# zh-Hans Localization Phase 69

Date: 2026-06-02 Asia/Shanghai

## Goal

Refresh manifest, glossary, target-term safety, coverage, and locale exports
after Phase 64-68.

## Low-Load Script Maintenance

The first two full dry-run attempts were stopped because the original dry-run
path scanned the same files repeatedly and ran too long for the low-load policy.

Updated:

- `script/zh_apply_localization.py`

Change:

- Added a dry-run-only fast path that groups replacements by file and counts
  all source/target string literals in a single Rust string-literal pass per
  file.
- Non-dry-run application keeps the existing replacement semantics.

Validation for the script change:

```text
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
```

Python tests:

```text
19 tests passed
```

## Manifest And Glossary

Passed:

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --check-glossary
rg -n 'target = ".*(智能体|智能代理|智能助手|智能助理|命令调色板|端点点|帐号)' resources/localization/zh-Hans-overrides.toml
```

The target-term search returned no matches.

Metadata:

```json
{
  "entries": 7792,
  "key": {"count": 150, "percent": 1.9},
  "context": {"count": 7792, "percent": 100.0},
  "status": {"count": 7792, "percent": 100.0},
  "preserve_terms": {"count": 98, "percent": 1.3},
  "notes": {"count": 0, "percent": 0.0},
  "expected_count": {"count": 192, "percent": 2.5}
}
```

Full dry-run after the dry-run fast path:

```text
entries: 7792
files: 475
already_applied: 5539
would_change: 0
missing: 0
```

## Coverage

```text
onboarding: 323 covered, 0 candidates, 100.0%
workspace: 865 covered, 1 candidate, 99.9%
search: 269 covered, 0 candidates, 100.0%
settings: 2024 covered, 3 candidates, 99.9%
modals: 5180 covered, 435 candidates, 92.3%
release: 8514 covered, 439 candidates, 95.1%
terminal: 2106 covered, 268 candidates, 88.7%
AI / Agent: 2527 covered, 167 candidates, 93.8%
```

Known source-level preserve-first residues:

- Workspace `1` candidate is `WarpDrive_BelongsToTeam`.
- Settings `3` candidates are `Show_Base_Model_Picker_In_Prompt`,
  `HasSettingsToImport`, and `SettingsViewInTab`.
- Remaining terminal and AI/Agent top paths are mostly protocol, log, parser,
  fixture, command-template, provider, MCP, or identifier strings.

## Locale Exports

Created:

```text
/tmp/warp-cn-zh-Hans-locale-rc14.json: 2518742 bytes
/tmp/warp-cn-zh-Hans-locale-rc14.pretty.json: 2946125 bytes
/tmp/warp-cn-zh-Hans-locale-rc14.yaml: 2143920 bytes
```

Passed:

```text
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc14.json > /tmp/warp-cn-zh-Hans-locale-rc14.pretty.json
```

## Low-Load Review

Commands were run serially with `nice -n 10` where appropriate. The long-running
full dry-run attempts were stopped and replaced by a lower-load dry-run
implementation instead of letting the machine continue heating. No GUI, account,
backend, static image, or destructive state was touched.

## Qualification

Phase 69 is accepted as `qualified-manifest-glossary-export-maintenance`.

The phase is qualified because manifest validation, glossary, target-term
search, metadata, full dry-run, coverage, JSON/YAML export, JSON parse,
py_compile, and Python tests passed, and the dry-run path is now fast enough for
the final RC14 gate.
