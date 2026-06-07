# zh-Hans Translation Rescan - 2026-06-06

## Purpose

Validate Warp CN 0.19 self-defined complete release localization health.

## Commands

```text
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_full_translation_audit.py script/test_zh_mojibake_scan.py
```

## Result

```text
status: pass
manifest validation: passed
glossary check: passed
entries: 7943
context metadata: 7943 (100.0%)
status metadata: 7943 (100.0%)
files: 552
already_applied: 5690
would_change: 0
missing: 0
release inventory covered: 8574
release inventory candidates: 2
release inventory coverage: 100.0%
unit tests: 27 passed
```

## Release Interpretation

This rescan validates the self-defined localization release. It does not clear
public-RC backend fixture, isolated account, or disposable object evidence rows.
