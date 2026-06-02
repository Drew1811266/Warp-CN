# zh-Hans Localization Phase 119

Date: 2026-06-02

## Scope

Phase 119 ran the post-RC20 entry baseline and upstream drift sentinel. It did
not add translations, modify Rust source, launch GUI, compile, bundle, generate
PNGs, log in, or touch backend, billing, cloud, managed-secret, endpoint, or
team state.

## Baseline Commands

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
result: manifest validation passed

nice -n 10 python3 script/zh_apply_localization.py --check-glossary
result: glossary check passed

nice -n 10 python3 script/zh_apply_localization.py --metadata-summary
entries: 7943
key: 150 (1.9%)
context: 7943 (100.0%)
status: 7943 (100.0%)
preserve_terms: 155 (2.0%)
notes: 0 (0.0%)
expected_count: 195 (2.5%)

nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
entries: 7943
files: 552
already_applied: 5690
would_change: 0
missing: 0
```

## Public-RC Registry Sentinel

```text
nice -n 10 python3 script/zh_public_rc_status.py
total: 11
public_rc_required: 11
blocked-no-backend-fixture: 5
blocked-no-disposable-object: 3
blocked-no-isolated-account: 3
```

## Candidate Sentinel

```text
nice -n 10 python3 script/zh_localization_inventory.py --status candidate app/src/terminal app/src/workspace app/src/settings_view app/src/ai resources/localization
```

Remaining candidates:

```text
app/src/ai/blocklist/usage/rollup.rs:151 Agent
app/src/terminal/view/ambient_agent/block/harness_session_header.rs:35 Agent
```

Both rows are intentional preserved product/function terms. No
`new-source-translation-needed` item appeared.

## Qualification Review

```text
phase: 119
status: qualified-drift-sentinel
manifest validation: passed
glossary check: passed
dry-run clean: yes
unexpected would_change: no
unexpected missing: no
public-RC blocker registry stable: yes
new source candidates requiring translation: none
remaining candidates: intentional preserve terms only
external operations run: none
```
