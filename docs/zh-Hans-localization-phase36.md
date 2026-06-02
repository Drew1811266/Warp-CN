# zh-Hans Localization Phase 36

Date: 2026-06-01

## Goal

Close high-confidence visible UI gaps in Settings, Workspace, and modal-adjacent surfaces before the next GUI smoke.

## Scope

Phase 36 added `127` manifest entries:

- `43` translated visible entries.
- `84` reviewed preserves for internal IDs, date formats, command fragments, search tags, telemetry/debug strings, and product identifiers.

Primary translated areas:

- Settings working-directory and startup-shell labels.
- Billing/settings dispatch labels and small environment modal labels.
- Warp Drive enable/disable labels.
- Workspace conversation list empty/search/new-conversation labels.
- Left-panel tooltips.
- Local-network redirect guidance.
- Billing/credits banner copy.

## Preserved Classes

- Billing row keys, usage IDs, and date/time format strings.
- MCP template/gallery IDs and file-based IDs.
- Search tags and internal Settings/workspace IDs.
- CLI install command switches.
- Capacity multiplier labels such as `2x` and `5x`.
- Product identifiers where translating would change semantics or search behavior.

## Coverage

```text
settings before: 1953 covered / 74 candidates = 96.3%
settings after: 2024 covered / 3 candidates = 99.9%

workspace before: 817 covered / 49 candidates = 94.3%
workspace after: 865 covered / 1 candidate = 99.9%

modals before Phase 36: 4077 covered / 1522 candidates = 72.8%
modals after: 4091 covered / 1508 candidates = 73.1%

release after: 7425 covered / 1512 candidates = 83.1%
```

## Validation

Passed:

```text
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --manifest .omx/tmp-phase36-manifest.toml --dry-run --summary
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
cargo fmt --check
git diff --check
```

Scoped dry-run:

```text
entries: 127
files: 48
already_applied: 43
would_change: 0
missing: 0
```

## Qualification

Phase 36 is accepted as `qualified-settings-workspace-modal-polish-low-load`.

The phase is qualified because Settings, Workspace, and Modals all exceed their post-RC9 targets, account-state modal copy remains tracked without GUI promotion, and the validation gate passed.
