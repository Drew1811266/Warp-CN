# zh-Hans Localization Phase 15

Date: 2026-06-01

## Goal

Translate Terminal visible surfaces without changing shell commands, escape sequences, parser fixtures, SSH detection behavior, or protocol strings.

## Changes

- Expanded keybinding inventory filtering for `meta` and `?` shortcut forms.
- Added `app/src/terminal/ssh/util.rs` to the inventory ignore list after reviewing it as SSH prompt detection, command parsing, option lists, and command-example text.
- Added a Phase 15 manifest batch.
- Applied 217 visible Terminal translations.
- Registered 27 reviewed preserved terminal settings schema/internal entries.
- Formatted changed Rust files with `cargo fmt`.

## Translated Surfaces

- Terminal input placeholders, accessibility description, search labels, and Agent steering/follow-up hints.
- Warp-anything example prompts in the universal input.
- Command-generation states and error toasts.
- Conversation export toasts and file errors.
- Attachment/image limit errors.
- Cloud handoff and read-only viewer errors.
- Terminal command palette/action labels from `app/src/terminal/view/init.rs`.
- Project initialization and codebase-indexing prompts in `app/src/terminal/view/init_project/mod.rs`.
- Selected onboarding suggestion titles and terminal zero-state copy.
- Shell picker display labels where safe.

## Preserved / Not Translated

- SSH command examples, parser tokens, option lists, prompt-detection probes, and shell command samples in `app/src/terminal/ssh/util.rs`.
- Terminal settings schema descriptions in `app/src/terminal/session_settings.rs`.
- ANSI/escape sequences, command strings, file extensions, object ids, context ids, and debug-only labels.

## Coverage After Phase 15

```text
python3 script/zh_localization_inventory.py app/src/terminal --coverage
preset: custom
covered: 420
candidates: 1906
coverage: 18.1%

python3 script/zh_localization_inventory.py --preset release --coverage
preset: release
covered: 3571
candidates: 5362
coverage: 40.0%
```

## Validation

```text
python3 script/zh_apply_localization.py --validate-manifest
manifest validation passed

python3 script/zh_apply_localization.py --check-glossary
glossary check passed

python3 script/zh_apply_localization.py --dry-run --summary
entries: 3293
files: 207
already_applied: 2936
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

Phase 15 is accepted as `qualified-low-load`.

Proceed to Phase 16: AI / Agent classification and visible UI localization.
