# zh-Hans Release Candidate 2026-06-02 RC15

RC15 is the Phase 71-78 post-RC14 localization record for Warp CN.

Generated: 2026-06-02 Asia/Shanghai.

Decision: `ready-for-local-use-with-fixture-evidence`

Public RC decision: not ready.

## Scope

RC15 includes:

- Post-RC14 residue classification and preserve policy.
- Terminal residue pass 11.
- AI/Agent residue pass 9.
- Inventory precision and preserve/ignore cleanup.
- Translation quality and glossary audit.
- Public-RC evidence dry-run package.
- Onboarding visual asset Chinese script package.
- Final RC15 language review, export, Python, formatting, diff, and low-concurrency Rust compile gates.

RC15 does not claim first-party runtime i18n support, complete whole-repository
localization, regenerated onboarding imagery, real account/backend verification,
or public-RC GUI readiness.

## Manifest And Coverage

```text
nice -n 10 python3 script/zh_apply_localization.py --metadata-summary --json
entries: 7843
key: 150 (1.9%)
context: 7843 (100.0%)
status: 7843 (100.0%)
preserve_terms: 113 (1.4%)
notes: 0
expected_count: 195 (2.5%)

nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
entries: 7843
files: 492
already_applied: 5590
would_change: 0
missing: 0
```

Coverage:

```text
onboarding: 323 covered, 0 candidates, 100.0%
workspace: 865 covered, 1 candidate, 99.9%
search: 269 covered, 0 candidates, 100.0%
settings: 2024 covered, 3 candidates, 99.9%
modals: 5199 covered, 287 candidates, 94.8%
release: 8533 covered, 291 candidates, 96.7%
```

Phase-specific coverage:

```text
Terminal: 2135 covered, 159 candidates, 93.1%
AI / Agent: 2517 covered, 128 candidates, 95.2%
```

Phase 74 added exact-path ignore rules for reviewed non-UI residue, so the
`covered` counts for release, terminal, and AI/Agent are lower than a pure
translation-only pass. Candidate reduction and coverage percentage are the
relevant RC15 inventory signal.

Locale exports:

```text
/tmp/warp-cn-zh-Hans-locale-rc15.json: 2534285 bytes
/tmp/warp-cn-zh-Hans-locale-rc15.pretty.json: 2964752 bytes
/tmp/warp-cn-zh-Hans-locale-rc15.yaml: 2156891 bytes
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
nice -n 10 python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale-rc15.json
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc15.json > /tmp/warp-cn-zh-Hans-locale-rc15.pretty.json
nice -n 10 python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale-rc15.yaml
nice -n 10 python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py
nice -n 10 python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
nice -n 10 cargo fmt --check
git diff --check
CARGO_BUILD_JOBS=2 nice -n 10 cargo check -j 2 -p warp
```

The forbidden/awkward target-term search returned no matches. Its non-zero exit
status is expected for a no-match search and is treated as passing evidence.

Python tests:

```text
19 tests passed
```

Rust compile gate:

```text
CARGO_BUILD_JOBS=2 nice -n 10 cargo check -j 2 -p warp
Finished dev profile successfully in 15.03s
```

Known command-line warnings:

- `cargo check -j 2 -p warp` reports an existing unused-variable warning in
  `app/src/remote_server/ssh_transport/installation/scp_fallback.rs`.
- The same compile gate reports existing unused-variable warnings in
  `app/src/terminal/input/slash_commands/mod.rs`.
- These warnings did not block the final compile gate.

## Source Localization Delta

Post-RC14 source movement:

```text
manifest entries: 7792 -> 7843
release coverage: 95.1% -> 96.7%
modals coverage: 92.3% -> 94.8%
terminal coverage: 88.7% -> 93.1%
AI / Agent coverage: 93.8% -> 95.2%
```

Phase 72 translated terminal settings descriptions, inline menu hints, skill
menu copy, project language-support prompt/actions, AWS Bedrock and SSH banners,
Open-in-Warp accessibility copy, queued prompt panel labels, shared-session role
items, and ambient Agent footer/status text.

Phase 73 translated provider CLI table/status output, execution-profile model
menu default badge, and AI rules page labels/offline notice.

Phase 74 removed reviewed false positives from inventory through exact-path
ignore rules for terminal protocols, fixtures, command templates, internal
diagnostics, AI parser/conversion diagnostics, git parsing, skill filenames, and
LLM/MCP detection or diagnostic strings.

Phase 75 audited high-frequency terminology and made no broad correction
because glossary checks passed and forbidden target terms were absent.

## Public-RC Evidence

Phase 76 created a dry-run evidence package for remaining public-RC blockers:

- `docs/zh-Hans-public-rc-gate-runbook.md`
- `docs/zh-Hans-gui-smoke-matrix.md`
- `docs/gui-smoke-artifacts/phase76/README.md`

No GUI, account, backend, billing, cloud, team, environment, managed secret,
custom endpoint, or destructive state was touched.

Public RC is still blocked by missing current-cycle isolated account/backend
evidence for:

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

Phase 77 created:

- `docs/zh-Hans-onboarding-visual-script-package.md`

The package provides Chinese replacement scripts for all `50` deferred
onboarding PNGs. No PNG was opened, generated, uploaded, replaced, or otherwise
modified.

Public-facing polish still requires a reversible asset branch, regenerated
Chinese-localized preview art or explicit design approval, before/after contact
sheets, and confirmation that no unrelated binary assets changed.

## Low-Load Review

The RC15 work was run serially. Longer Python, export, formatting, and Rust
commands used reduced priority where appropriate. The final Rust compile used
`CARGO_BUILD_JOBS=2` and `cargo check -j 2 -p warp`.

No GUI, account, backend, static image, billing, cloud, team, environment,
managed secret, endpoint, or destructive state mutation was performed.

## Release Decision

RC15 is `ready-for-local-use-with-fixture-evidence`.

Reasoning:

- Manifest drift gate is clean: `missing: 0`, `would_change: 0`.
- Glossary and manifest checks pass.
- Manifest `context/status` metadata coverage is `100.0%`.
- Forbidden/awkward target-term search returned no matches.
- Locale JSON/YAML exports complete and JSON parses.
- Python localization tests pass.
- Rust formatting, whitespace checks, and `cargo check -j 2 -p warp` pass.
- Release preset source-level coverage is now `96.7%`.
- Terminal and AI/Agent source residue was reduced while preserving protocols,
  parser contracts, fixtures, command templates, provider/model identifiers,
  and diagnostics.
- Public-RC external-state blockers and static image blockers are explicitly
  documented and not conflated with source localization readiness.

RC15 is not `ready-for-public-rc` because isolated-account/backend evidence and
regenerated/static-art approval are still unavailable.

## Next Gate

Before public RC:

1. Execute `docs/zh-Hans-public-rc-gate-runbook.md` only with disposable
   prerequisites and cropped/redacted evidence.
2. Confirm cleanup proof for every disposable object.
3. Regenerate or replace the deferred onboarding PNGs using
   `docs/zh-Hans-onboarding-visual-script-package.md`, or record explicit
   design approval for the current assets.
4. Re-run the command-line gate and reconsider `ready-for-public-rc`.
