# zh-Hans Localization Phase 17

Date: 2026-06-01

## Goal

Close small high-confidence localization gaps across Onboarding/Auth, Tab configs, Themes, Billing, and Warp Drive while preserving identifiers, commands, theme names, parser formats, and account-state safety.

## Changes

- Added a Phase 17 manifest batch.
- Applied 158 visible translations.
- Registered 133 reviewed preserved entries.
- Translated Billing restriction copy, Warp Drive sharing/actions/sorting/empty-state copy, onboarding command prompts, and selected Tab config labels.
- Preserved theme display names, theme file paths, command examples, provider/model IDs, component IDs, parser errors, redirect/storage keys, and diagnostic strings.
- Formatted changed Rust files with `cargo fmt`.

## Coverage After Phase 17

```text
python3 script/zh_localization_inventory.py crates/onboarding/src app/src/auth --coverage
preset: custom
covered: 323
candidates: 0
coverage: 100.0%

python3 script/zh_localization_inventory.py app/src/tab_configs --coverage
preset: custom
covered: 69
candidates: 0
coverage: 100.0%

python3 script/zh_localization_inventory.py app/src/themes --coverage
preset: custom
covered: 58
candidates: 0
coverage: 100.0%

python3 script/zh_localization_inventory.py app/src/billing --coverage
preset: custom
covered: 20
candidates: 0
coverage: 100.0%

python3 script/zh_localization_inventory.py app/src/drive --coverage
preset: custom
covered: 253
candidates: 0
coverage: 100.0%

python3 script/zh_localization_inventory.py --preset release --coverage
preset: release
covered: 4746
candidates: 4147
coverage: 53.4%
```

## Validation

```text
python3 script/zh_apply_localization.py --validate-manifest
manifest validation passed

python3 script/zh_apply_localization.py --check-glossary
glossary check passed

python3 script/zh_apply_localization.py --dry-run --summary
entries: 4376
files: 254
already_applied: 3571
would_change: 0
missing: 0

python3 -m unittest script/test_zh_apply_localization.py script/test_zh_export_locale.py script/test_zh_localization_inventory.py
19 tests passed

cargo fmt --check
passed

git diff --check
passed
```

## Decision

Phase 17 is accepted as `qualified-low-load`.

Proceed to Phase 18: GUI evidence and RC promotion.
