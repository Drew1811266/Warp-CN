# zh-Hans Release Candidate 2026-06-02 RC16

RC16 is the Phase 79-86 post-RC15 localization record for Warp CN.

Generated: 2026-06-02 Asia/Shanghai.

Decision: `ready-for-local-use-with-fixture-evidence`

Public RC decision: not ready.

## Scope

RC16 includes:

- Post-RC15 preserve-only residue classification.
- Terminal residue pass 12.
- AI/Agent residue pass 10.
- Workspace/settings straggler closure.
- Public-RC prerequisite package RC16.
- Onboarding visual asset regeneration plan RC16.
- Upstream drift preflight RC16.
- Final RC16 language review, export, Python, formatting, diff, and
  low-concurrency Rust compile gates.

RC16 does not claim first-party runtime i18n support, complete whole-repository
localization, regenerated onboarding imagery, real account/backend verification,
or public-RC GUI readiness.

## Manifest And Coverage

```text
nice -n 10 python3 script/zh_apply_localization.py --metadata-summary --json
entries: 7943
key: 150 (1.9%)
context: 7943 (100.0%)
status: 7943 (100.0%)
preserve_terms: 155 (2.0%)
notes: 0
expected_count: 195 (2.5%)

nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
entries: 7943
files: 552
already_applied: 5690
would_change: 0
missing: 0
```

Coverage:

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

Remaining source candidates:

```text
app/src/ai/blocklist/usage/rollup.rs: Agent
app/src/terminal/view/ambient_agent/block/harness_session_header.rs: Agent
```

Both remaining candidates are intentional glossary preserve terms.

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

The forbidden/awkward target-term search returned no matches. Its non-zero exit
status is expected for a no-match search and is treated as passing evidence.

Python tests:

```text
19 tests passed
```

Rust compile gate:

```text
CARGO_BUILD_JOBS=1 nice -n 15 cargo check -j 1 -p warp
Finished dev profile successfully in 13.58s
```

Known command-line warnings:

- `cargo check -j 1 -p warp` reports an existing unused-variable warning in
  `app/src/remote_server/ssh_transport/installation/scp_fallback.rs`.
- The same compile gate reports existing unused-variable warnings in
  `app/src/terminal/input/slash_commands/mod.rs`.
- These warnings did not block the final compile gate.

## Source Localization Delta

Post-RC15 source movement:

```text
manifest entries: 7843 -> 7943
release coverage: 96.7% -> 100.0%
modals coverage: 94.8% -> 100.0%
terminal coverage: 93.1% -> 100.0%
AI / Agent coverage: 95.2% -> 100.0%
workspace coverage: 99.9% -> 100.0%
settings coverage: 99.9% -> 100.0%
```

Phase 79 updated post-RC15 preserve policy so reviewed stable IDs, parser
tokens, protocol names, fixture values, and command syntax no longer count as
actionable localization residue.

Phase 80 translated terminal setting, session, ambient Agent, onboarding,
banner, shared-session, Warpify, CLI Agent, and terminal view copy until only
the intentional `Agent` preserve term remained in terminal inventory.

Phase 81 translated AI/Agent task, admin, config, cloud provider, execution,
MCP, rule editor, artifact, orchestration, and inline action copy until only the
intentional `Agent` preserve term remained in AI inventory.

Phase 82 closed workspace/settings residue as reviewed stable IDs:
`Show_Base_Model_Picker_In_Prompt`, `HasSettingsToImport`,
`SettingsViewInTab`, and `WarpDrive_BelongsToTeam`.

Phase 83 documented the public-RC prerequisite package without touching GUI,
account, backend, billing, cloud, team, environment, managed secret, endpoint,
or destructive state.

Phase 84 documented a reversible asset-only regeneration plan for the deferred
onboarding PNGs. No PNG or other binary asset changed.

Phase 85 completed an upstream drift preflight without fetch, merge, rebase, or
branch switch. Local manifest drift remained clean with `missing: 0` and
`would_change: 0`.

Phase 86 completed the language review and freeze gate. During Phase 80,
`script/zh_apply_localization.py` was updated to batch non-dry-run application
by file after the old sequential summary path was interrupted for holding one
CPU core for several minutes. The patched apply path completed subsequent runs
in roughly 2.5 seconds.

## Public-RC Evidence

Phase 83 created:

- `docs/zh-Hans-public-rc-prerequisites-rc16.md`

Phase 83 also updated:

- `docs/zh-Hans-public-rc-gate-runbook.md`
- `docs/zh-Hans-gui-smoke-matrix.md`

Public RC is still blocked by missing current-cycle isolated account/backend
fixture evidence for:

- `GUI-AUTH-01`
- `GUI-SET-03`
- `GUI-SET-04`
- `GUI-SET-05`
- `GUI-SET-06`
- `GUI-WS-04`
- `GUI-WS-06`
- `GUI-WS-07`
- `GUI-BILL-01`
- `GUI-BILL-02`
- `GUI-CLOUD-01`

## Static Visual Assets

Phase 84 created:

- `docs/zh-Hans-onboarding-visual-asset-regeneration-plan-rc16.md`

The plan covers the `50` deferred onboarding PNGs and keeps the `4`
decorative/brand assets unchanged unless design approval says otherwise. It
requires a reversible asset-only branch, before/after contact sheets, explicit
approval, and proof that no unrelated binary assets changed.

No PNG was opened, generated, uploaded, replaced, or otherwise modified in
RC16.

## Upstream Drift

Phase 85 created:

- `docs/zh-Hans-upstream-drift-preflight-rc16.md`

The local branch was `codex/zh-Hans-followup-localization` at
`24c03f567d2835176347c11d4792ef1607f509cd` before the Phase 85 preflight. It
had no configured upstream tracking branch, so fetch/merge/rebase was skipped.

The preflight confirmed:

```text
missing: 0
would_change: 0
release candidates: 2 intentional Agent preserve terms
```

## Low-Load Review

The RC16 work was run serially. Longer Python, export, formatting, and Rust
commands used reduced priority where appropriate. The final Rust compile used
`CARGO_BUILD_JOBS=1` and `cargo check -j 1 -p warp`.

No GUI, account, backend, static image, billing, cloud, team, environment,
managed secret, endpoint, or destructive state mutation was performed.

## Release Decision

RC16 is `ready-for-local-use-with-fixture-evidence`.

Reasoning:

- Manifest drift gate is clean: `missing: 0`, `would_change: 0`.
- Glossary and manifest checks pass.
- Manifest `context/status` metadata coverage is `100.0%`.
- Forbidden/awkward target-term search returned no matches.
- All tracked source localization inventory areas are at `100.0%`.
- Remaining source candidates are intentional `Agent` preserve terms.
- Locale JSON/YAML exports complete and JSON parses.
- Python localization tests pass.
- Rust formatting, whitespace checks, and `cargo check -j 1 -p warp` pass.
- Public RC blockers are documented separately and were not bypassed.
