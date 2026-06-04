# zh-Hans Release Candidate 2026-06-02 RC13

RC13 is the Phase 55-62 post-RC12 localization record for Warp CN.

Generated: 2026-06-02 Asia/Shanghai.

Decision: `ready-for-local-use-with-fixture-evidence`

Public RC decision: not ready.

## Scope

RC13 includes:

- Post-RC12 queue and safety classification.
- Terminal block/view core backlog pass.
- Terminal CLI/ambient/zero-state backlog pass.
- AI blocklist action execution backlog pass.
- AI document/artifact/harness/provider backlog pass.
- Manifest metadata, glossary, and locale export maintenance.
- Static visual-asset and public-RC evidence preflight.
- Language quality, preserve safety, export, Python, formatting, diff, and low-concurrency Rust compile gates.

RC13 does not claim first-party runtime i18n support, complete whole-repository localization, regenerated onboarding imagery, or public-RC GUI readiness.

## Manifest And Coverage

```text
python3 script/zh_apply_localization.py --metadata-summary --json
entries: 7681
key: 150 (2.0%)
context: 7681 (100.0%)
status: 7681 (100.0%)
preserve_terms: 67 (0.9%)
notes: 0
expected_count: 188 (2.4%)

python3 script/zh_apply_localization.py --dry-run --summary
entries: 7681
files: 444
already_applied: 5431
would_change: 0
missing: 0
```

Coverage:

```text
onboarding: 323 covered, 0 candidates, 100.0%
workspace: 865 covered, 1 candidate, 99.9%
search: 269 covered, 0 candidates, 100.0%
settings: 2024 covered, 3 candidates, 99.9%
modals: 5065 covered, 550 candidates, 90.2%
release: 8399 covered, 554 candidates, 93.8%
```

Phase-specific coverage:

```text
Terminal: 2040 covered, 334 candidates, 85.9%
AI / Agent: 2478 covered, 216 candidates, 92.0%
```

Locale exports:

```text
/tmp/warp-cn-zh-Hans-locale-rc13.json: 2482815 bytes
/tmp/warp-cn-zh-Hans-locale-rc13.pretty.json: 2902985 bytes
/tmp/warp-cn-zh-Hans-locale-rc13.yaml: 2113575 bytes
```

## Command-Line Gate

Passed:

```text
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
rg -n 'target = ".*(智能体|智能代理|智能助手|智能助理|命令调色板|端点点|帐号)' resources/localization/zh-Hans-overrides.toml
python3 script/zh_apply_localization.py --metadata-summary --json
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_localization_inventory.py app/src/terminal --coverage
python3 script/zh_localization_inventory.py app/src/ai --coverage
python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale-rc13.json
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc13.json > /tmp/warp-cn-zh-Hans-locale-rc13.pretty.json
python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale-rc13.yaml
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
cargo fmt --check
git diff --check
CARGO_BUILD_JOBS=2 cargo check -j 2 -p warp
```

Python tests:

```text
19 tests passed
```

Rust compile gate:

```text
cargo check -j 2 -p warp
Finished dev profile successfully
```

Known command-line warnings:

- `cargo check -j 2 -p warp` reports existing unused-variable warnings in `app/src/remote_server/ssh_transport/installation/scp_fallback.rs` and `app/src/terminal/input/slash_commands/mod.rs`.
- The final dry-run and Rust compile were run serially with reduced priority/concurrency to avoid sustained local load.

## Source Localization Delta

Post-RC12 source movement:

```text
manifest entries: 7372 -> 7681
release coverage: 90.1% -> 93.8%
terminal coverage: 77.9% -> 85.9%
AI / Agent coverage: 86.8% -> 92.0%
modals coverage: 84.3% -> 90.2%
```

Phase 56 translated terminal block filtering, block list, pane overflow menu, inline history, model spec, settings description, safe-mode, attached-context, and visible command labels while preserving action IDs, view IDs, date/time formats, debug structs, and keybinding schema contracts.

Phase 57 translated CLI plugin visible errors/toasts, SSH/Warpify copy, ambient Agent setup/status copy, docker sandbox user errors, open-in-Warp banners, prompt suggestions, SSH remote choice UI, Warpify footer, and terminal zero-state copy while preserving CLI notification fixtures, command transcript formats, bootstrap hooks, OS literals, environment IDs, and diagnostics.

Phase 58 translated AI citation labels, Autonomy settings link copy, and codebase-index speedbump UI while preserving AI tool execution results, shell/glob/git/find/PowerShell templates, remote diff contracts, orchestration diagnostics, file-existence commands, binding IDs, and parser heuristic prefixes.

Phase 59 translated AI document restored titles, artifact labels/errors, code block actions, AWS Bedrock credential UI, host picker labels, telemetry banner copy, AI block context menu, credit display, harness fallback, and persisted-workspace install messages while preserving Oz CLI examples, Codex transcript formats, MCP JSON/config validation contracts, filename templates, product/model/provider names, LSP diagnostics, and invariants.

## GUI Evidence

RC13 carries forward the Phase 38 current-source local GUI screenshots from RC10/RC11/RC12 for logged-out onboarding, local no-AI flow, main window, and Settings anchors.

Phase 61 intentionally did not launch GUI processes because no new safe isolated account/backend-state prerequisites were available and the low-load policy favored source, manifest, and blocker audit first.

No account, billing quota, cloud environment, managed secret, custom endpoint, production object, or team ownership state was touched.

## Static Visual Assets

Phase 61 rechecked the onboarding PNG inventory:

```text
total PNGs: 54
root-level onboarding PNGs: 12
agent_intention root PNGs: 16
terminal_intention root PNGs: 10
agent_intention/theme PNGs: 8
terminal_intention/theme PNGs: 8
```

The Phase 45/53 asset decision is unchanged:

- `4` assets accepted as `accepted-decorative-or-brand-art`.
- `50` assets deferred as `defer-to-design-regeneration` because they contain embedded English UI, terminal/code/editor text, notification copy, toolbar text, or sidebar labels.

Created:

- `docs/zh-Hans-onboarding-visual-regeneration-plan.md`

RC13 remains honest as `visual-residue`: these are bitmap assets, not manifest/source drift. Public-facing polish requires a reversible asset branch, regenerated Chinese-localized preview art, before/after screenshots, and confirmation that no unrelated binary assets changed.

## Public-RC Evidence

Phase 61 refreshed the blocker list. Public RC is still blocked by missing current-cycle isolated account/backend evidence for:

- `GUI-AUTH-01`: browser login and auth callback.
- `GUI-SET-03`: real-account AI settings, Build plan, API key, and custom inference state.
- `GUI-SET-04` and `GUI-SET-05`: disposable AWS/Bedrock profile or invalid credential fixture.
- `GUI-SET-06`: disposable environment deletion confirmation.
- `GUI-WS-04`: disposable managed auth secret deletion confirmation.
- `GUI-WS-06`: disposable custom endpoint removal confirmation without fixture env.
- `GUI-WS-07`: disposable team ownership transfer confirmation.
- `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01`: safe billing/quota/cloud backend states.

## Release Decision

RC13 is `ready-for-local-use-with-fixture-evidence`.

Reasoning:

- Manifest drift gate is clean: `missing: 0`, `would_change: 0`.
- Glossary and manifest checks pass.
- Manifest `context/status` metadata coverage is `100.0%`.
- Forbidden/awkward target-term search returned no matches.
- Locale JSON/YAML exports complete and JSON parses.
- Python localization tests pass.
- Rust formatting, whitespace checks, and `cargo check -j 2 -p warp` pass.
- Release preset source-level coverage improved from RC12 `90.1%` to RC13 `93.8%`.
- Terminal and AI/Agent source residue were materially reduced while preserving protocol/tool contracts.
- Static image residue and public-RC external-state blockers are explicitly documented instead of being treated as source drift.

RC13 is not `ready-for-public-rc` because isolated-account/backend evidence and regenerated/static-art approval are still unavailable.

## Next Gate

Before public RC:

1. Provide a disposable test account/team and backend fixture states from `docs/zh-Hans-public-rc-gate-runbook.md`.
2. Capture cropped/redacted screenshots for account/state rows.
3. Confirm cleanup for every disposable object.
4. Regenerate or replace the deferred onboarding PNGs with Chinese-localized preview art.
5. Keep fixture evidence separate from true account-verified evidence.
6. Re-run the command-line gate and reconsider `ready-for-public-rc`.
