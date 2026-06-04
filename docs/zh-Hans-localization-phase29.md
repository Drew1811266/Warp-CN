# zh-Hans Localization Phase 29

Date: 2026-06-01

## Goal

Close visible Settings and secondary modal gaps left after RC8, with special attention to AI settings, shared blocks, code settings, external editor settings, environment forms, MCP settings, privacy regex, billing state labels, and custom inference examples.

## Scope

Phase 29 reviewed and updated:

- `app/src/settings_view/ai_page.rs`
- `app/src/settings_view/show_blocks_view.rs`
- `app/src/settings_view/code_page.rs`
- `app/src/settings_view/features/external_editor.rs`
- `app/src/settings_view/update_environment_form.rs`
- `app/src/settings_view/mcp_servers/list_page.rs`
- `app/src/settings_view/mcp_servers_page.rs`
- `app/src/settings_view/privacy_page.rs`
- `app/src/settings_view/privacy/add_regex_modal.rs`
- `app/src/settings_view/billing_and_usage_page.rs`
- `app/src/settings_view/billing_and_usage_page_v2.rs`
- `app/src/settings_view/custom_inference_modal.rs`
- `app/src/settings_view/main_page.rs`
- `app/src/settings_view/mod.rs`

## Manifest Changes

Phase 29 added `166` manifest entries:

- `125` translated visible, searchable, or modal-facing strings.
- `41` reviewed preserves for examples, date formats, IDs, commands, search tags, and diagnostics.

Skipped as intentional internal IDs because translating or preserving them in the manifest would conflict with glossary rules or runtime semantics:

- `Show_Base_Model_Picker_In_Prompt`
- `HasSettingsToImport`
- `SettingsViewInTab`

## Coverage

| Preset | Before Phase 29 | After Phase 29 |
| --- | ---: | ---: |
| Settings | `1771 covered / 254 candidates = 87.5%` | `1953 covered / 74 candidates = 96.3%` |
| Modals | `3682 covered / 1914 candidates = 65.8%` | `3682 covered / 1914 candidates = 65.8%` |
| Release | `6715 covered / 2217 candidates = 75.2%` | `6897 covered / 2037 candidates = 77.2%` |

## Notes

- Settings search keyword strings were either translated into Chinese/bilingual keyword bags or preserved when they are command examples, implementation tags, date formats, or internal identifiers.
- Account-state and billing-state strings were translated at source level only. No GUI verification status was promoted without current-cycle evidence.
- Command examples, Docker/image examples, GitHub URL fragments, date formats, and internal action names were preserved where changing them could affect behavior or search semantics.

## Validation

Passed:

- `python3 script/zh_apply_localization.py --validate-manifest`
- `python3 script/zh_apply_localization.py --check-glossary`
- Phase 29 scoped dry-run using the existing replacement engine:
  - `entries: 166`
  - `files: 14`
  - `already_applied: 125`
  - `would_change: 0`
  - `missing: 0`
- `python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py`
- `cargo fmt --check`
- `git diff --check`

Full-manifest dry-run remains deferred to the Phase 32 RC9 gate to avoid repeated high-load scans.

## Qualification

Phase 29 is accepted as `qualified-settings-modals-cleanup-low-load`.

No GUI row is promoted by this source-only pass. No account, billing quota, cloud environment, secret, or team ownership state was touched.
