# zh-Hans Localization Phase 21

Date: 2026-06-01

## Goal

Run the second terminal backlog classification pass under the low-load execution rule.

## Changes

- Added Phase 21 manifest entries for selected terminal surfaces:
  - `app/src/terminal/view.rs`
  - `app/src/terminal/view/ambient_agent/tips.rs`
  - `app/src/terminal/profile_model_selector.rs`
  - `app/src/terminal/view/context_menu.rs`
  - `app/src/terminal/ssh/error.rs`
  - `app/src/terminal/shared_session/viewer/network.rs`
- Translated visible terminal, Agent permission, SSH, model selector, context menu, and shared-session error copy.
- Preserved reviewed internal IDs, protocol strings, command templates, and parser/test literals as source-equals-target entries.
- Skipped unreviewed required-glossary candidates unless they were explicitly translated.

## Coverage

- Terminal preset before Phase 21: `420 covered / 1906 candidates = 18.1%`.
- Terminal preset after Phase 21: `873 covered / 1455 candidates = 37.5%`.
- Release preset after Phase 21: `5202 covered / 3693 candidates = 58.5%`.
- Manifest after Phase 21: `4787` entries across `260` files.

## Validation

- `python3 script/zh_apply_localization.py --validate-manifest`
- `python3 script/zh_apply_localization.py --check-glossary`
- `python3 script/zh_apply_localization.py --dry-run --summary`
  - `already_applied: 3815`
  - `would_change: 0`
  - `missing: 0`
- `python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py`
  - `Ran 19 tests`
  - `OK`
- `cargo fmt --check`
- `git diff --check`

## Decision

Phase 21 is accepted as `qualified-terminal-backlog-pass`.

Proceed to Phase 22: Settings and workspace second pass.
