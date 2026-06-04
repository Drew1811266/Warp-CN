# zh-Hans Localization Phase 16

Date: 2026-06-01

## Goal

Classify AI / Agent strings and translate visible Agent UI, status, tips, action labels, and user-facing errors without changing model prompts, tool protocol contracts, or diagnostic logging behavior.

## Changes

- Added a Phase 16 manifest batch for AI / Agent surfaces.
- Applied 510 visible translations.
- Registered 282 reviewed preserved entries after duplicate cleanup.
- Preserved Agent transcript markdown, action protocol labels, debug identifiers, driver lifecycle diagnostics, MCP transport logs, component IDs, and provider names where changing text would risk model/tool behavior or diagnostics.
- Kept `app/src/ai/agent_sdk/driver/snapshot.rs` ignored as reviewed internal snapshot upload/declaration plumbing.
- Formatted changed Rust files with `cargo fmt`.

## Classification

| Surface | Decision | Notes |
| --- | --- | --- |
| Agent management and inline Agent view | Translated | Toolbar labels, shortcuts, conversation state, cloud handoff hints, orchestration actions, zero state, status header copy. |
| Agent visible output cards | Translated | Permission prompts, search/file action labels, feedback controls, credit messages, continuation/fork controls, code review action labels. |
| Agent user-facing errors | Translated | Driver setup/auth/runtime errors, MCP server errors, Warp Drive sync errors, cloud environment errors, API key and AWS Bedrock errors. |
| Static prompt suggestions | Translated | User-visible suggestions are localized even though the submitted prompt changes language by design for zh-Hans. |
| Agent transcript markdown / SDK output | Mixed | User-readable status fragments were translated; transcript protocol/debug fragments and raw command/file formats were preserved. |
| Model/tool protocol and logs | Preserved | Driver lifecycle logs, MCP transport logs, component IDs, internal assertions, provider names, and parser-like fragments remain English. |

## Coverage After Phase 16

```text
python3 script/zh_localization_inventory.py app/src/ai --coverage
preset: custom
covered: 1131
candidates: 1553
coverage: 42.1%

python3 script/zh_localization_inventory.py --preset release --coverage
preset: release
covered: 4416
candidates: 4458
coverage: 49.8%
```

Remaining AI candidates are now concentrated in smaller secondary modules such as request-file-edit application, execution profile editors, environment/secret SDK helpers, harness adapters, and integration output.

## Validation

```text
python3 script/zh_apply_localization.py --validate-manifest
manifest validation passed

python3 script/zh_apply_localization.py --check-glossary
glossary check passed

python3 script/zh_apply_localization.py --dry-run --summary
entries: 4085
files: 228
already_applied: 3418
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

Phase 16 is accepted as `qualified-low-load`.

Proceed to Phase 17: small completion passes.
