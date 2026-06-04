# zh-Hans Localization Phase 24/25

Date: 2026-06-01

## Goal

Finish manifest metadata migration and run the RC8 command-line gate without high-load local verification.

## Changes

- Added missing `status = "active"` and `context = "Legacy reviewed zh-Hans localization entry"` metadata to `2514` older manifest blocks.
- Raised manifest `context` coverage from `54.2%` to `100.0%`.
- Raised manifest `status` coverage from `54.2%` to `100.0%`.
- Created `docs/zh-Hans-release-candidate-2026-06-01-rc8.md`.

## Final Coverage

- Onboarding preset: `323 covered / 0 candidates = 100.0%`.
- Workspace preset: `817 covered / 49 candidates = 94.3%`.
- Search preset: `269 covered / 0 candidates = 100.0%`.
- Settings preset: `1771 covered / 254 candidates = 87.5%`.
- Modals preset: `2922 covered / 2637 candidates = 52.6%`.
- Release preset: `5955 covered / 2940 candidates = 66.9%`.
- AI root: `1502 covered / 1182 candidates = 56.0%`.
- Terminal root: `873 covered / 1455 candidates = 37.5%`.

## Validation

- `python3 script/zh_apply_localization.py --validate-manifest`
- `python3 script/zh_apply_localization.py --check-glossary`
- `python3 script/zh_apply_localization.py --metadata-summary --json`
  - `entries: 5487`
  - `context: 5487 (100.0%)`
  - `status: 5487 (100.0%)`
- `python3 script/zh_apply_localization.py --dry-run --summary`
  - `already_applied: 4318`
  - `would_change: 0`
  - `missing: 0`
- `python3 script/zh_export_locale.py --format json`
- `python3 -m json.tool`
- `python3 script/zh_export_locale.py --format yaml`
- `python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py`
- `python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py`
  - `Ran 19 tests`
  - `OK`
- `cargo fmt --check`
- `git diff --check`
- `cargo check -j 2 -p warp`
  - Passed with existing unused-variable warnings.

## Decision

Phase 24/25 is accepted as `qualified-rc8-source-gate`.

RC8 is `ready-for-local-use-source-level`, but not `ready-for-public-rc`.

Public RC still requires isolated account or fixture GUI evidence for browser auth, token fallback, Billing, Cloud capacity/quota, destructive confirmations, Agent lifecycle/error states, and environment/auth-secret deletion paths.
