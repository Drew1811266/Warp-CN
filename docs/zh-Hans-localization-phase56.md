# zh-Hans Localization Phase 56

Date: 2026-06-02 Asia/Shanghai

## Goal

Translate high-confidence terminal block, pane, inline-history, model-score, settings, and keybinding UI residue while preserving internal IDs, debug strings, date/time formats, and schema contracts.

## Scope

Scoped manifest:

- `.omx/tmp-phase56-manifest.toml`

Primary files:

- `app/src/terminal/block_filter.rs`
- `app/src/terminal/block_list_element.rs`
- `app/src/terminal/view.rs`
- `app/src/terminal/view/pane_impl.rs`
- `app/src/terminal/model/block.rs`
- `app/src/terminal/input/models/model_spec_scores.rs`
- `app/src/terminal/input/inline_history/view.rs`
- `app/src/terminal/find/model/async_find.rs`
- `app/src/terminal/general_settings.rs`
- `app/src/terminal/keys_settings.rs`
- `app/src/terminal/input/message_bar/attached_context.rs`
- `app/src/terminal/safe_mode_settings.rs`

## Changes

Added `86` scoped manifest entries:

- `63` source replacements applied.
- `23` reviewed preserves.

Translated visible areas:

- Block filter placeholder, tooltips, and accessibility help.
- Block hover actions, workflow-save warning, and restored-session separator copy.
- Async find status labels.
- General settings descriptions.
- Inline history tabs, header, configure action, and attached-context message bar copy.
- Model specs, reasoning-level descriptions, and score labels.
- Key settings descriptions, except the long global hotkey schema/example contract.
- Safe-mode display names and descriptions.
- Pane overflow menu items, ambient-agent cancel tooltip, details tooltip, and default Agent conversation titles.
- Terminal visible `Command` label.

Reviewed preserves:

- Accessibility/position identifiers such as `filter_button_for_block_{block}` and `context_menu_button_{block_index}`.
- View/action/state identifiers such as `BlockFilterEditor`, `CopyBlockCommands`, `CommandSearch`, and `LongRunningCommand`.
- Internal assertions and diagnostics.
- Date format `%a %b %-d at %-I:%M %p`.
- Compact duration formats such as ` ({}h {}m {:.0}s)`.
- The global activation hotkey schema/example string because it documents exact keybinding syntax and escaped examples.

## Review Results

Scoped dry-run after apply:

```text
entries: 86
files: 12
already_applied: 62
would_change: 0
missing: 0
```

Target-file inventory after apply:

```text
no remaining candidates
```

Coverage:

```text
terminal: 1939 covered / 435 candidates = 81.7%
release: 8159 covered / 794 candidates = 91.1%
```

Manifest metadata:

```text
entries: 7458
context: 7458 (100.0%)
status: 7458 (100.0%)
expected_count: 174 (2.3%)
```

## Validation

Passed:

```text
nice -n 10 python3 script/zh_apply_localization.py --manifest .omx/tmp-phase56-manifest.toml --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --check-glossary
nice -n 10 python3 script/zh_apply_localization.py --manifest .omx/tmp-phase56-manifest.toml --dry-run --summary
nice -n 10 python3 script/zh_localization_inventory.py <phase56 files> --status candidate
nice -n 10 python3 script/zh_localization_inventory.py app/src/terminal --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset release --coverage
nice -n 10 python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
nice -n 10 cargo fmt --check
git diff --check <phase56 files and manifests>
```

`cargo fmt --check` initially reported formatting-only wrapping differences in `attached_context.rs` and `model_spec_scores.rs`; `nice -n 10 cargo fmt` was run, and the follow-up check passed.

## Low-Load Review

All checks were run serially. No GUI was launched, no Rust compile gate was run, and no account/backend/destructive state was touched.

## Qualification

Phase 56 is accepted as `qualified-terminal-block-view-core-pass`.

The phase is qualified because the scoped dry-run is clean, the target files have no remaining candidates, terminal/release coverage improved, manifest validation and glossary passed, Python localization tests passed, formatting and diff checks passed, and protocol-adjacent strings were preserved with explicit context.
