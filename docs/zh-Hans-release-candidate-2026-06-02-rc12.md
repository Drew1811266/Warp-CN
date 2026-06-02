# zh-Hans Release Candidate 2026-06-02 RC12

RC12 is the Phase 49-54 post-RC11 localization record for Warp CN.

Generated: 2026-06-02 Asia/Shanghai.

Decision: `ready-for-local-use-with-fixture-evidence`

Public RC decision: not ready.

## Scope

RC12 includes:

- Post-RC11 queue hygiene and execution planning.
- Terminal visible UI backlog pass 6.
- Terminal executor/protocol preservation pass.
- AI/Agent backlog source pass 5.
- Static visual-asset and public-RC blocker refresh.
- Language quality, preserve safety, export, Python, formatting, diff, and low-concurrency Rust compile gates.

RC12 does not claim first-party runtime i18n support, complete whole-repository localization, regenerated onboarding imagery, or public-RC GUI readiness.

## Manifest And Coverage

```text
python3 script/zh_apply_localization.py --metadata-summary --json
entries: 7372
key: 150 (2.0%)
context: 7372 (100.0%)
status: 7372 (100.0%)
preserve_terms: 18 (0.2%)
notes: 0
expected_count: 171 (2.3%)

python3 script/zh_apply_localization.py --dry-run --summary
entries: 7372
files: 399
already_applied: 5261
would_change: 0
missing: 0
```

Coverage:

```text
onboarding: 323 covered, 0 candidates, 100.0%
workspace: 865 covered, 1 candidate, 99.9%
search: 269 covered, 0 candidates, 100.0%
settings: 2024 covered, 3 candidates, 99.9%
modals: 4736 covered, 879 candidates, 84.3%
release: 8070 covered, 883 candidates, 90.1%
```

Phase-specific coverage:

```text
Terminal: 1850 covered, 524 candidates, 77.9%
AI / Agent: 2339 covered, 355 candidates, 86.8%
```

Locale exports:

```text
/tmp/warp-cn-zh-Hans-locale-rc12.json: 2381963 bytes
/tmp/warp-cn-zh-Hans-locale-rc12.pretty.json: 2786034 bytes
/tmp/warp-cn-zh-Hans-locale-rc12.yaml: 2027958 bytes
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
python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale-rc12.json
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc12.json > /tmp/warp-cn-zh-Hans-locale-rc12.pretty.json
python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale-rc12.yaml
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

Post-RC11 source movement:

```text
manifest entries: 7088 -> 7372
release coverage: 86.7% -> 90.1%
terminal coverage: 69.7% -> 77.9%
AI / Agent coverage: 82.6% -> 86.8%
modals coverage: 78.8% -> 84.3%
```

Phase 50 translated terminal visible UI across auth-secret selection, loading, link detection, onboarding prompt blocks, shared-session banners, shell-terminated banners, use-agent footer copy, and Warpify settings while preserving UI identifiers, rule filenames, enum names, runtime formatting, and diagnostics.

Phase 51 translated shared-session viewer failure toasts and preserved bootstrap scripts, shell templates, Windows registry/env diagnostics, SSH arguments, WSL/MSYS2 command shapes, in-band command generators, and remote executor diagnostics.

Phase 52 translated AI/Agent management, harness terminal copy, scheduled Agent copy, AWS credential user-facing errors, web search/fetch/get-files surfaces, execution profile labels, and rule-editor copy while preserving AWS/OIDC/provider contracts, MCP JSON/env templates, prompt/schema/tool protocols, URL formats, and skill identifiers.

## GUI Evidence

RC12 carries forward the Phase 38 current-source local GUI screenshots from RC10/RC11 for logged-out onboarding, local no-AI flow, main window, and Settings anchors.

Phase 53 intentionally did not launch GUI processes because no new safe isolated account/backend-state prerequisites were available and the low-load policy favored source, manifest, and fixture audit first.

No account, billing quota, cloud environment, managed secret, custom endpoint, production object, or team ownership state was touched.

## Static Visual Assets

Phase 53 rechecked the onboarding PNG inventory:

```text
total PNGs: 54
agent customize: 16
terminal customize: 10
agent theme: 8
terminal theme: 8
```

The Phase 45 asset decision is unchanged:

- `4` assets accepted as `accepted-decorative-or-brand-art`.
- `50` assets deferred as `defer-to-design-regeneration` because they contain embedded English UI, terminal/code/editor text, notification copy, toolbar text, or sidebar labels.

RC12 remains honest as `visual-residue`: these are bitmap assets, not manifest/source drift. Public-facing polish requires a reversible asset branch, regenerated Chinese-localized preview art, before/after screenshots, and confirmation that no unrelated binary assets changed.

## Public-RC Evidence

Phase 53 refreshed the Phase 46 blocker list. Public RC is still blocked by missing current-cycle isolated account/backend evidence for:

- `GUI-AUTH-01`: browser login and auth callback.
- `GUI-SET-03`: real-account AI settings, Build plan, API key, and custom inference state.
- `GUI-SET-04` and `GUI-SET-05`: disposable AWS/Bedrock profile or invalid credential fixture.
- `GUI-SET-06`: disposable environment deletion confirmation.
- `GUI-WS-04`: disposable managed auth secret deletion confirmation.
- `GUI-WS-06`: disposable custom endpoint removal confirmation without fixture env.
- `GUI-WS-07`: disposable team ownership transfer confirmation.
- `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01`: safe billing/quota/cloud backend states.

## Release Decision

RC12 is `ready-for-local-use-with-fixture-evidence`.

Reasoning:

- Manifest drift gate is clean: `missing: 0`, `would_change: 0`.
- Glossary and manifest checks pass.
- Manifest `context/status` metadata coverage is `100.0%`.
- Forbidden/awkward target-term search returned no matches.
- Locale JSON/YAML exports complete and JSON parses.
- Python localization tests pass.
- Rust formatting, whitespace checks, and `cargo check -j 2 -p warp` pass.
- Release preset source-level coverage improved from RC11 `86.7%` to RC12 `90.1%`.
- Terminal and AI/Agent source residue were materially reduced while preserving protocol/tool contracts.
- Static image residue and public-RC external-state blockers are explicitly documented instead of being treated as source drift.

RC12 is not `ready-for-public-rc` because isolated-account/backend evidence and regenerated/static-art approval are still unavailable.

## Next Gate

Before public RC:

1. Provide a disposable test account/team and backend fixture states from `docs/zh-Hans-public-rc-gate-runbook.md`.
2. Capture cropped/redacted screenshots for account/state rows.
3. Confirm cleanup for every disposable object.
4. Regenerate or replace the deferred onboarding PNGs with Chinese-localized preview art.
5. Keep fixture evidence separate from true account-verified evidence.
6. Re-run the command-line gate and reconsider `ready-for-public-rc`.
