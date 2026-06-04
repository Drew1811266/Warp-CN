# zh-Hans Release Candidate 2026-06-02 RC11

RC11 is the Phase 41-48 post-RC10 localization record for Warp CN.

Generated: 2026-06-02 Asia/Shanghai.

Decision: `ready-for-local-use-with-fixture-evidence`

Public RC decision: not ready.

## Scope

RC11 includes:

- Post-RC10 queue hygiene and safety classification.
- Terminal backlog source pass 5.
- AI/MCP/child-agent source pass 4.
- Auth-secret FTUX source localization and Agent fixture blocker audit.
- Static onboarding PNG visual-residue asset decisions.
- Public-RC external-state blocker audit.
- Language quality, preserve safety, and glossary review.
- Final manifest, export, Python, formatting, diff, and low-concurrency Rust compile gates.

RC11 does not claim first-party runtime i18n support, complete whole-repository localization, regenerated onboarding imagery, or public-RC GUI readiness.

## Manifest And Coverage

```text
python3 script/zh_apply_localization.py --metadata-summary --json
entries: 7088
key: 150 (2.1%)
context: 7088 (100.0%)
status: 7088 (100.0%)
preserve_terms: 18 (0.3%)
notes: 0
expected_count: 150 (2.1%)

python3 script/zh_apply_localization.py --dry-run --summary
entries: 7088
files: 367
already_applied: 5124
would_change: 0
missing: 0
```

Coverage:

```text
onboarding: 323 covered, 0 candidates, 100.0%
workspace: 865 covered, 1 candidate, 99.9%
search: 269 covered, 0 candidates, 100.0%
settings: 2024 covered, 3 candidates, 99.9%
modals: 4423 covered, 1187 candidates, 78.8%
release: 7757 covered, 1191 candidates, 86.7%
```

Phase-specific coverage:

```text
Terminal: 1653 covered, 718 candidates, 69.7%
AI / Agent: 2223 covered, 469 candidates, 82.6%
```

Locale exports:

```text
/tmp/warp-cn-zh-Hans-locale-rc11.json: 2291118 bytes
/tmp/warp-cn-zh-Hans-locale-rc11.pretty.json: 2681668 bytes
/tmp/warp-cn-zh-Hans-locale-rc11.yaml: 1950745 bytes
```

## Command-Line Gate

Passed:

```text
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
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
python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale-rc11.json
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc11.json > /tmp/warp-cn-zh-Hans-locale-rc11.pretty.json
python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale-rc11.yaml
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

Post-RC10 source movement:

```text
manifest entries: 6786 -> 7088
release coverage: 83.1% -> 86.7%
terminal coverage: 61.2% -> 69.7%
AI / Agent coverage: 78.0% -> 82.6%
modals coverage: 73.1% -> 78.8%
```

Phase 42 translated visible terminal settings/tooltips/shared-session/SSH upload copy and preserved terminal protocol, shell, ANSI, ConPTY, WSL, tmux, URL, env var, prompt, and diagnostic contracts.

Phase 43 translated visible MCP/attachment/artifact/child-agent/search/suggested-rule copy and preserved watcher, prompt, provider, file path, schema, and tool protocol contracts.

Phase 44 translated auth-secret FTUX and Agent task/notification copy, while documenting exact missing Agent GUI fixture hooks.

## GUI Evidence

RC11 carries forward the Phase 38 current-source local GUI screenshots from RC10 for logged-out onboarding, local no-AI flow, main window, and Settings anchors.

Phase 44 and Phase 46 did not launch GUI processes because the safe prerequisites were unavailable and the low-load policy favored source/fixture audit first.

No account, billing quota, cloud environment, managed secret, custom endpoint, production object, or team ownership state was touched.

## Static Visual Assets

Phase 45 reviewed all `54` onboarding PNGs:

- `4` assets accepted as `accepted-decorative-or-brand-art`.
- `50` assets deferred as `defer-to-design-regeneration` because they contain embedded English UI, terminal/code/editor text, notification copy, toolbar text, or sidebar labels.

RC11 remains honest as `visual-residue`: these are bitmap assets, not manifest/source drift. Public-facing polish requires a reversible asset branch, regenerated Chinese-localized preview art, before/after screenshots, and confirmation that no unrelated binary assets changed.

## Public-RC Evidence

Phase 46 completed as `qualified-public-rc-account-state-blocked`.

Public RC is still blocked by missing current-cycle isolated account/backend evidence for:

- `GUI-AUTH-01`: browser login and auth callback.
- `GUI-SET-03`: real-account AI settings, Build plan, API key, and custom inference state.
- `GUI-SET-04` and `GUI-SET-05`: disposable AWS/Bedrock profile or invalid credential fixture.
- `GUI-SET-06`: disposable environment deletion confirmation.
- `GUI-WS-04`: disposable managed auth secret deletion confirmation.
- `GUI-WS-06`: disposable custom endpoint removal confirmation without fixture env.
- `GUI-WS-07`: disposable team ownership transfer confirmation.
- `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01`: safe billing/quota/cloud backend states.

## Release Decision

RC11 is `ready-for-local-use-with-fixture-evidence`.

Reasoning:

- Manifest drift gate is clean: `missing: 0`, `would_change: 0`.
- Glossary and manifest checks pass.
- Manifest `context/status` metadata coverage is `100.0%`.
- Locale JSON/YAML exports complete and JSON parses.
- Python localization tests pass.
- Rust formatting, whitespace checks, and `cargo check -j 2 -p warp` pass.
- Release preset source-level coverage improved from RC10 `83.1%` to RC11 `86.7%`.
- Terminal and AI/Agent source residue were materially reduced while preserving protocol/tool contracts.
- Static image residue and public-RC external-state blockers are explicitly documented instead of being treated as source drift.

RC11 is not `ready-for-public-rc` because isolated-account/backend evidence and regenerated/static-art approval are still unavailable.

## Next Gate

Before public RC:

1. Provide a disposable test account/team and backend fixture states from `docs/zh-Hans-public-rc-gate-runbook.md`.
2. Capture cropped/redacted screenshots for account/state rows.
3. Confirm cleanup for every disposable object.
4. Regenerate or replace the deferred onboarding PNGs with Chinese-localized preview art.
5. Keep fixture evidence separate from true account-verified evidence.
6. Re-run the command-line gate and reconsider `ready-for-public-rc`.
