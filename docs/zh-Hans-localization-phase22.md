# zh-Hans Localization Phase 22

Date: 2026-06-01

## Goal

Run the second Settings and Workspace pass while keeping validation low-load.

## Changes

- Added `365` Phase 22 manifest entries:
  - `242` translated entries.
  - `123` reviewed preserve entries for debug commands, state IDs, test fixtures, logs, paths, and product/theme names.
- Covered high-visibility Settings surfaces:
  - Team membership, invites, billing limit warnings, plan actions, discovery, and join-team copy.
  - Referrals page actions, rewards, validation messages, and sent-invite feedback.
  - Appearance search/control keywords for theme, icon, input, tab, cursor, and typography settings.
- Covered Workspace surfaces:
  - Global search zero states, unavailable states, result count messages, and capped-result warning.
  - Code review right-panel unavailable reasons.
  - Debug action labels and selected workspace toasts/errors.
- Removed `17` duplicate manifest blocks produced by repeated candidates in the same file.
- Avoided unsafe nested-quote replacement by translating `Forked "{title}"` as `已 fork {title}`.

## Coverage

- Settings preset before Phase 22: `1551 covered / 474 candidates = 76.6%`.
- Workspace preset before Phase 22: `655 covered / 211 candidates = 75.6%`.
- Settings preset after Phase 22: `1771 covered / 254 candidates = 87.5%`.
- Workspace preset after Phase 22: `817 covered / 49 candidates = 94.3%`.
- Release preset after Phase 22: `5584 covered / 3311 candidates = 62.8%`.
- Manifest after Phase 22: `5152` entries across `262` files.

## Validation

- `python3 script/zh_apply_localization.py --validate-manifest`
- `python3 script/zh_apply_localization.py --check-glossary`
- `python3 script/zh_apply_localization.py --dry-run --summary`
  - `already_applied: 4057`
  - `would_change: 0`
  - `missing: 0`
- `python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py`
  - `Ran 19 tests`
  - `OK`
- `cargo fmt --check`
- `git diff --check`

## Decision

Phase 22 is accepted as `qualified-settings-workspace-pass`.

Proceed to Phase 23: AI SDK/editor/environment pass.
