# zh-Hans Localization Phase 14

Date: 2026-06-01

## Goal

Finish a high-visibility Settings and Workspace pass, while preserving reviewed internal keys that should not be translated.

## Changes

- Added a Phase 14 batch to `resources/localization/zh-Hans-overrides.toml`.
- Applied 69 visible Settings / Workspace translations.
- Registered 316 reviewed preserved entries for compatibility parse keys, telemetry action ids, settings context flags, settings schema descriptions, and hidden search/index tokens.
- Formatted changed Rust files with `cargo fmt`.

## Settings Scope

Translated visible `Features` command/action labels in `app/src/settings_view/features_page.rs`, including:

- Meta key toggles.
- Copy-on-select and Linux selection clipboard.
- Completions, command corrections, syntax highlighting, error underlining.
- Terminal reporting, notifications, Vim, smart select, slash command, and global workflow labels.
- Global hotkey configuration and restart notice.

Reviewed and preserved:

- Telemetry action ids.
- Settings section compatibility parse keys.
- Settings context flags.
- Hidden search terms retained for follow-up discoverability policy work.

## Workspace Scope

Translated selected visible Workspace copy:

- Sync-input command labels and disable toast.
- Generic access-denied toast.
- Codex modal copy.
- Cloud agent capacity modal plan/credit copy.
- Menu field labels.
- Warp-on-Web local network access toast.
- `settings.toml` repair prompt.

Reviewed and preserved:

- `app/src/workspace/tab_settings.rs` schema descriptions.
- Internal menu/debug field names where changing the literal could affect behavior or diagnostics.

## Coverage After Phase 14

```text
preset: settings
covered: 1548
candidates: 477
coverage: 76.4%

preset: workspace
covered: 655
candidates: 211
coverage: 75.6%

preset: release
covered: 3295
candidates: 5688
coverage: 36.7%
```

## Validation

```text
python3 script/zh_apply_localization.py --validate-manifest
manifest validation passed

python3 script/zh_apply_localization.py --check-glossary
glossary check passed

python3 script/zh_apply_localization.py --dry-run --summary
entries: 3049
files: 202
already_applied: 2719
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

Phase 14 is accepted as `qualified-low-load`.

Proceed to Phase 15: Terminal visible-surface localization.
