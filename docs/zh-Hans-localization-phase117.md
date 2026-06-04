# zh-Hans Localization Phase 117

Date: 2026-06-02

## Scope

Phase 117 ran a low-load upstream drift sentinel. It classified current
localization state only; it did not add translations, modify Rust, run GUI,
compile, bundle, generate PNGs, or touch account/backend/billing/cloud/team
state.

## Manifest And Glossary Gates

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
result: manifest validation passed

nice -n 10 python3 script/zh_apply_localization.py --check-glossary
result: glossary check passed
```

## Metadata Summary

```text
entries: 7943
key: 150 (1.9%)
context: 7943 (100.0%)
status: 7943 (100.0%)
preserve_terms: 155 (2.0%)
notes: 0 (0.0%)
expected_count: 195 (2.5%)
```

## Dry-Run Summary

```text
entries: 7943
files: 552
already_applied: 5690
would_change: 0
missing: 0
```

## Inventory Snapshot

The planned inventory form used `--summary --paths`, but the current script CLI
uses positional roots and `--status`. The equivalent candidate-only command was:

```text
nice -n 10 python3 script/zh_localization_inventory.py --status candidate app/src/terminal app/src/workspace app/src/settings_view app/src/ai resources/localization
```

Output:

```text
| status | path | line | literal |
| --- | --- | ---: | --- |
| candidate | `app/src/ai/blocklist/usage/rollup.rs` | 151 | Agent |
| candidate | `app/src/terminal/view/ambient_agent/block/harness_session_header.rs` | 35 | Agent |
```

## Drift Classification

```text
app/src/ai/blocklist/usage/rollup.rs:151 Agent
classification: intentional-preserve-term

app/src/terminal/view/ambient_agent/block/harness_session_header.rs:35 Agent
classification: intentional-preserve-term
```

No `new-source-translation-needed` item appeared, so the RC20 freeze path can
continue.

## Qualification Review

```text
phase: 117
status: qualified
manifest validation: passed
glossary check: passed
dry-run clean: yes
unexpected would_change: no
unexpected missing: no
new source candidates requiring translation: none
remaining candidates: intentional preserve terms only
external operations run: none
```
