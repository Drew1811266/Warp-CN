# zh-Hans Localization Phase 13

Date: 2026-06-01

## Goal

Phase 13 reduces false remaining-candidate noise before continuing broad translation work. The priority is to keep later coverage metrics meaningful and avoid translating strings that are not product UI.

## Changes

- Expanded `script/zh_localization_inventory.py` keybinding detection so bindings such as `cmdorctrl-,`, `cmdorctrl-=`, `cmdorctrl--`, `ctrl-shift->`, `shift-cmd-{`, and `alt-{}` are no longer counted as localization candidates.
- Added unit coverage in `script/test_zh_localization_inventory.py` for punctuation keybinding literals.
- Added `app/src/workspace/cross_window_tab_drag.rs` to `resources/localization/zh-Hans-inventory-ignore.toml`.

## Classification Notes

Reviewed categories:

| Category | Decision | Reason |
| --- | --- | --- |
| Keybinding strings | Ignore from candidate inventory | They are command binding syntax, not display copy. Translating them would break shortcut parsing or documentation consistency. |
| `app/src/workspace/cross_window_tab_drag.rs` | Ignore exact path | Reviewed strings are diagnostic log/state text around cross-window tab dragging. They are not visible labels, buttons, descriptions, toasts, dialogs, or user-facing errors. |
| Settings action labels | Keep as candidates | `ToggleSettingActionPair` descriptions are explicitly documented as user-readable in `app/src/settings_view/mod.rs`, so they remain translation targets. |
| Settings `search_terms` | Keep as candidates for now | They are not visible UI copy, but they affect discoverability. Later phases should either localize them with Chinese+English terms or document a preservation policy. |
| AI/Terminal candidates | Needs later classification | These remain the largest buckets and must be split into visible UI, user-facing transcript text, prompt/protocol text, logs, and internal state before translation. |

## Coverage After Phase 13

```text
preset: release
covered: 2892
candidates: 6091
coverage: 32.2%

preset: workspace
covered: 598
candidates: 268
coverage: 69.1%

preset: settings
covered: 1202
candidates: 823
coverage: 59.4%
```

## Validation

```text
python3 script/test_zh_localization_inventory.py
4 tests passed

python3 script/zh_apply_localization.py --validate-manifest
manifest validation passed

python3 script/zh_apply_localization.py --check-glossary
glossary check passed

python3 script/zh_apply_localization.py --dry-run --summary
entries: 2664
files: 198
already_applied: 2650
would_change: 0
missing: 0
```

## Decision

Phase 13 is accepted as `qualified-low-load`.

Proceed to Phase 14: high-visibility Settings and Workspace localization.
