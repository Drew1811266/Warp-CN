# zh-Hans Localization Phase 23

Date: 2026-06-01

## Goal

Run the AI SDK, editor, environment, secret, and Agent command pass while keeping validation low-load.

## Changes

- Added `335` Phase 23 manifest entries:
  - `261` translated entries.
  - `74` reviewed preserve entries for CLI templates, logs, protocol/status IDs, examples, and test fixtures.
- Covered AI and Agent surfaces:
  - Agent environment setup progress, codebase index messages, and terminal driver errors.
  - Agent Code diff application errors.
  - Execution profile editor controls, model descriptions, permission settings, and allow/deny lists.
  - Agent SDK environment, secret, integration output, ambient message, and auth/quota CLI messages.
  - Requested command view labels and permission state copy.
  - Conversation and Codex harness error messages.
- Removed `36` duplicate manifest blocks produced by repeated candidates in the same file.

## Coverage

- AI root before Phase 23: `1131 covered / 1553 candidates = 42.1%`.
- AI root after Phase 23: `1502 covered / 1182 candidates = 56.0%`.
- Modals preset after Phase 23: `2922 covered / 2637 candidates = 52.6%`.
- Release preset after Phase 23: `5955 covered / 2940 candidates = 66.9%`.
- Manifest after Phase 23: `5487` entries across `273` files.

## Validation

- `python3 script/zh_apply_localization.py --validate-manifest`
- `python3 script/zh_apply_localization.py --check-glossary`
- `python3 script/zh_apply_localization.py --dry-run --summary`
  - `already_applied: 4318`
  - `would_change: 0`
  - `missing: 0`
- `python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py`
  - `Ran 19 tests`
  - `OK`
- `cargo fmt --check`
- `git diff --check`

## Decision

Phase 23 is accepted as `qualified-ai-sdk-editor-environment-pass`.

Proceed to Phase 24/25: manifest metadata migration and RC8 gate.
