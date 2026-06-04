# zh-Hans Localization Phase 66

Date: 2026-06-02 Asia/Shanghai

## Goal

Close or classify the tiny non-terminal/non-AI source stragglers before moving
to public-RC evidence and static visual-asset preparation.

## Coverage

Ran serially with `nice -n 10`:

```text
preset: onboarding
covered: 323
candidates: 0
coverage: 100.0%

preset: workspace
covered: 865
candidates: 1
coverage: 99.9%

preset: search
covered: 269
candidates: 0
coverage: 100.0%

preset: settings
covered: 2024
candidates: 3
coverage: 99.9%

preset: modals
covered: 5180
candidates: 435
coverage: 92.3%

preset: release
covered: 8514
candidates: 439
coverage: 95.1%
```

## Straggler Review

Workspace candidate:

```text
app/src/workspace/view.rs:23501 WarpDrive_BelongsToTeam
```

Settings candidates:

```text
app/src/settings_view/mod.rs:549 Show_Base_Model_Picker_In_Prompt
app/src/settings_view/mod.rs:559 HasSettingsToImport
app/src/settings_view/mod.rs:2363 SettingsViewInTab
```

These strings are position/accessibility/test-style identifiers rather than
visible user copy. They are preserve-first and were not translated. In
particular, translating `Show_Base_Model_Picker_In_Prompt` would both mutate an
identifier and violate the glossary's `Model => 模型` rule if preserved
verbatim in the manifest.

## Result

- Onboarding source remains fully covered.
- Search source remains fully covered.
- Workspace and settings stragglers are explicitly classified as preserve-first
  identifiers.
- Modals improved from RC13 `90.2%` to `92.3%`.
- Release improved from RC13 `93.8%` to `95.1%`.

## Low-Load Review

Only scoped inventory commands were run. No source, manifest, GUI, account,
backend, static image, or destructive state was touched in this phase.

## Qualification

Phase 66 is accepted as `qualified-core-straggler-closure`.

The phase is qualified because onboarding/search are still fully covered,
workspace/settings residuals are classified as preserve-first identifiers,
release and modal coverage improved after Phase 64-65, and no unsafe identifier
translations were made.
