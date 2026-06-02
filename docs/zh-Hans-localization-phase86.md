# zh-Hans Localization Phase 86

Date: 2026-06-02 Asia/Shanghai.

## Goal

Phase 86 produces the RC16 language review and freeze gate after Phases 79-85
qualified.

## Phase 79-85 Qualification Summary

```text
Phase 79: qualified; post-RC15 preserve policy updated.
Phase 80: qualified; Terminal residue reduced to intentional Agent preserve term.
Phase 81: qualified; AI/Agent residue reduced to intentional Agent preserve term.
Phase 82: qualified; workspace/settings candidates closed as stable IDs.
Phase 83: qualified; public-RC prerequisite package RC16 prepared.
Phase 84: qualified; onboarding visual asset regeneration plan RC16 prepared.
Phase 85: qualified; upstream drift preflight clean, no fetch/merge/rebase.
```

## Coverage

```text
onboarding: 323 covered, 0 candidates, 100.0%
workspace: 865 covered, 0 candidates, 100.0%
search: 269 covered, 0 candidates, 100.0%
settings: 2024 covered, 0 candidates, 100.0%
modals: 5240 covered, 2 candidates, 100.0%
release: 8574 covered, 2 candidates, 100.0%
terminal: 2178 covered, 1 candidate, 100.0%
AI / Agent: 2515 covered, 1 candidate, 100.0%
```

Remaining candidates:

```text
app/src/ai/blocklist/usage/rollup.rs: Agent
app/src/terminal/view/ambient_agent/block/harness_session_header.rs: Agent
```

Both are intentional glossary preserve terms.

## Manifest And Locale Exports

```text
entries: 7943
files: 552
already_applied: 5690
would_change: 0
missing: 0
metadata context/status: 7943 (100.0%)
preserve_terms: 155 (2.0%)
```

Locale exports:

```text
/tmp/warp-cn-zh-Hans-locale-rc16.json: 2566862 bytes
/tmp/warp-cn-zh-Hans-locale-rc16.pretty.json: 3004049 bytes
/tmp/warp-cn-zh-Hans-locale-rc16.yaml: 2184303 bytes
```

## Command-Line Gate

Passed:

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --check-glossary
rg -n 'target = ".*(智能体|智能代理|智能助手|智能助理|命令调色板|端点点|帐号)' resources/localization/zh-Hans-overrides.toml
nice -n 10 python3 script/zh_apply_localization.py --metadata-summary --json
nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
nice -n 10 python3 script/zh_localization_inventory.py --preset onboarding --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset workspace --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset search --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset settings --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset modals --coverage
nice -n 10 python3 script/zh_localization_inventory.py --preset release --coverage
nice -n 10 python3 script/zh_localization_inventory.py app/src/terminal --coverage
nice -n 10 python3 script/zh_localization_inventory.py app/src/ai --coverage
nice -n 10 python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale-rc16.json
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc16.json > /tmp/warp-cn-zh-Hans-locale-rc16.pretty.json
nice -n 10 python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale-rc16.yaml
nice -n 10 python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py
nice -n 10 python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
nice -n 10 cargo fmt --check
git diff --check
CARGO_BUILD_JOBS=1 nice -n 15 cargo check -j 1 -p warp
```

The forbidden target-term search returned no matches. Its non-zero exit status
is expected for a no-match search and is passing evidence.

Python tests:

```text
19 tests passed
```

Rust compile gate:

```text
CARGO_BUILD_JOBS=1 nice -n 15 cargo check -j 1 -p warp
Finished dev profile successfully in 13.58s
```

Known compile warnings:

- Existing unused-variable warning in
  `app/src/remote_server/ssh_transport/installation/scp_fallback.rs`.
- Existing unused-variable warnings in
  `app/src/terminal/input/slash_commands/mod.rs`.

## Low-Load Review

Commands were run serially. Longer Python, export, formatting, and Rust commands
used reduced priority. The final Rust compile gate used single-job Cargo
settings.

One Phase 80 application attempt was interrupted after the old non-dry-run
summary path held one CPU core for several minutes. `script/zh_apply_localization.py`
was updated to batch non-dry-run application by file; subsequent application
runs completed in roughly 2.5 seconds.

No GUI, account, backend, billing, cloud, team, environment, managed secret,
custom endpoint, or binary image state was touched.

## Remaining Blockers

Public RC remains blocked by:

```text
missing isolated account/backend fixture evidence for GUI-AUTH-01, GUI-SET-03,
GUI-SET-04, GUI-SET-05, GUI-SET-06, GUI-WS-04, GUI-WS-06, GUI-WS-07,
GUI-BILL-01, GUI-BILL-02, GUI-CLOUD-01

50 onboarding PNGs still requiring approved Chinese asset regeneration
```

## Qualification Result

Qualified.

Phase 86 passed because all required low-load gates passed, locale exports were
created, Python tests passed, Rust formatting and whitespace checks passed, the
low-concurrency Rust compile gate passed, and the RC16 release record was
created.
