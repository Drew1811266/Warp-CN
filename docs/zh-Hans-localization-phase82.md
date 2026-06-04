# zh-Hans Localization Phase 82

Date: 2026-06-02 Asia/Shanghai.

## Goal

Phase 82 closes the remaining workspace/settings candidates from RC15 by
reviewing each exact string and deciding whether to translate visible UI or
preserve stable identifiers.

## Reviewed Candidates

```text
app/src/settings_view/mod.rs:549 Show_Base_Model_Picker_In_Prompt
app/src/settings_view/mod.rs:559 HasSettingsToImport
app/src/settings_view/mod.rs:2363 SettingsViewInTab
app/src/workspace/view.rs:23501 WarpDrive_BelongsToTeam
```

## Decisions

| String | Decision | Rationale |
| --- | --- | --- |
| `Show_Base_Model_Picker_In_Prompt` | Preserve / ignore | Feature or telemetry-style state ID, not visible UI copy. |
| `HasSettingsToImport` | Preserve / ignore | Import-state ID, not visible UI copy. |
| `SettingsViewInTab` | Preserve / ignore | UI state or element ID, not visible UI copy. |
| `WarpDrive_BelongsToTeam` | Preserve / ignore | Warp Drive state/telemetry ID, not visible UI copy. |

Added a Phase 82 exact literal-pattern rule in
`resources/localization/zh-Hans-inventory-ignore.toml`.

## Coverage

Before Phase 82:

```text
workspace/settings custom snapshot: 4 candidates
workspace preset: 865 covered, 1 candidate, 99.9%
settings preset: 2024 covered, 3 candidates, 99.9%
```

After Phase 82:

```text
workspace/settings candidate snapshot: 0 candidates
workspace preset: 865 covered, 0 candidates, 100.0%
settings preset: 2024 covered, 0 candidates, 100.0%
```

## Acceptance Checks

```text
nice -n 10 python3 script/zh_localization_inventory.py app/src/workspace app/src/settings_view --status candidate
no candidates

nice -n 10 python3 script/zh_localization_inventory.py --preset workspace --coverage
preset: workspace
covered: 865
candidates: 0
coverage: 100.0%

nice -n 10 python3 script/zh_localization_inventory.py --preset settings --coverage
preset: settings
covered: 2024
candidates: 0
coverage: 100.0%

nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
manifest validation passed

nice -n 10 python3 script/zh_apply_localization.py --check-glossary
glossary check passed

git diff --check
passed
```

## Qualification Result

Qualified.

Phase 82 passed because all workspace/settings candidates were reviewed and
resolved as stable IDs, workspace and settings coverage reached 100.0%, and all
acceptance checks passed.
