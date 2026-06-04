# zh-Hans Release Candidate 2026-06-02 RC14

RC14 is the Phase 63-70 post-RC13 localization record for Warp CN.

Generated: 2026-06-02 Asia/Shanghai.

Decision: `ready-for-local-use-with-fixture-evidence`

Public RC decision: not ready.

## Scope

RC14 includes:

- Post-RC13 residue classification.
- Terminal residue pass 10.
- AI/Agent residue pass 8.
- Core onboarding, workspace, search, and settings straggler closure.
- Public-RC evidence package planning.
- Onboarding visual regeneration preparation.
- Manifest, glossary, target-term, coverage, and locale export maintenance.
- Final RC14 language review, formatting, diff, Python, export, and low-concurrency Rust compile gates.

RC14 does not claim first-party runtime i18n support, complete whole-repository
localization, regenerated onboarding imagery, real account/backend verification,
or public-RC GUI readiness.

## Manifest And Coverage

```text
nice -n 10 python3 script/zh_apply_localization.py --metadata-summary --json
entries: 7792
key: 150 (1.9%)
context: 7792 (100.0%)
status: 7792 (100.0%)
preserve_terms: 98 (1.3%)
notes: 0
expected_count: 192 (2.5%)

nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
entries: 7792
files: 475
already_applied: 5539
would_change: 0
missing: 0
```

Coverage:

```text
onboarding: 323 covered, 0 candidates, 100.0%
workspace: 865 covered, 1 candidate, 99.9%
search: 269 covered, 0 candidates, 100.0%
settings: 2024 covered, 3 candidates, 99.9%
modals: 5180 covered, 435 candidates, 92.3%
release: 8514 covered, 439 candidates, 95.1%
```

Phase-specific coverage:

```text
Terminal: 2106 covered, 268 candidates, 88.7%
AI / Agent: 2527 covered, 167 candidates, 93.8%
```

Locale exports:

```text
/tmp/warp-cn-zh-Hans-locale-rc14.json: 2518742 bytes
/tmp/warp-cn-zh-Hans-locale-rc14.pretty.json: 2946125 bytes
/tmp/warp-cn-zh-Hans-locale-rc14.yaml: 2143920 bytes
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
nice -n 10 python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale-rc14.json
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc14.json > /tmp/warp-cn-zh-Hans-locale-rc14.pretty.json
nice -n 10 python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale-rc14.yaml
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
Finished dev profile successfully in 16.81s
```

Known command-line warnings:

- `cargo check -j 2 -p warp` reports existing unused-variable warnings in
  `app/src/remote_server/ssh_transport/installation/scp_fallback.rs`.
- The same compile gate reports existing unused-variable warnings in
  `app/src/terminal/input/slash_commands/mod.rs`.
- These warnings did not block the final compile gate.

## Source Localization Delta

Post-RC13 source movement:

```text
manifest entries: 7681 -> 7792
release coverage: 93.8% -> 95.1%
modals coverage: 90.2% -> 92.3%
terminal coverage: 85.9% -> 88.7%
AI / Agent coverage: 92.0% -> 93.8%
```

Phase 64 translated safe terminal UI and user-facing copy while preserving
protocol payloads, shell contracts, command examples, bootstrap text, tests,
and parser-sensitive strings.

Phase 65 translated safe AI/Agent UI and user-facing copy while preserving
tool schemas, MCP/server names, provider identifiers, transcript markers,
JSON/config syntax, model IDs, code/script snippets, and parser contracts.

Phase 66 confirmed onboarding and search source coverage at `100.0%`, and
documented the remaining workspace/settings candidates as preserve-first IDs.

Phase 69 added a dry-run-only fast path in `script/zh_apply_localization.py` so
the full dry-run groups replacements by file and counts all source/target Rust
string literals in one parse per file. Non-dry-run application semantics remain
the existing sequential path.

## GUI Evidence

RC14 carries forward the existing current-source local GUI evidence from the
RC10-RC13 cycle for logged-out onboarding, local no-AI flow, main window, and
Settings anchors.

Phase 67 intentionally did not launch GUI processes because no disposable
account/team/backend prerequisites were available. No account, billing quota,
cloud environment, managed secret, custom endpoint, production object, or team
ownership state was touched.

## Static Visual Assets

Phase 68 rechecked the onboarding PNG inventory:

```text
total PNGs: 54
root-level onboarding PNGs: 12
agent_intention root PNGs: 16
terminal_intention root PNGs: 10
agent_intention/theme PNGs: 8
terminal_intention/theme PNGs: 8
```

The asset decision is unchanged:

- `4` assets are accepted as decorative or brand art.
- `50` assets are deferred to regeneration or explicit design approval because
  they contain embedded English UI, terminal/code/editor text, notification
  copy, toolbar text, or sidebar labels.

Public-facing polish still requires a reversible asset branch, regenerated
Chinese-localized preview art, before/after screenshots, and confirmation that
no unrelated binary assets changed.

## Public-RC Evidence

Public RC is still blocked by missing current-cycle isolated account/backend
evidence for:

- `GUI-AUTH-01`: browser login and auth callback.
- `GUI-SET-03`: real-account AI settings, Build plan, API key, and custom inference state.
- `GUI-SET-04` and `GUI-SET-05`: disposable AWS/Bedrock profile or invalid credential fixture.
- `GUI-SET-06`: disposable environment deletion confirmation.
- `GUI-WS-04`: disposable managed auth secret deletion confirmation.
- `GUI-WS-06`: disposable custom endpoint removal confirmation without fixture env.
- `GUI-WS-07`: disposable team ownership transfer confirmation.
- `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01`: safe billing/quota/cloud backend states.

Phase 67 records prerequisites, screenshot/redaction rules, cleanup proof, and
fixture-vs-account evidence wording in:

- `docs/zh-Hans-public-rc-gate-runbook.md`
- `docs/zh-Hans-gui-smoke-matrix.md`

## Low-Load Review

The RC14 work was run serially. Longer Python, export, formatting, and Rust
commands used reduced priority where appropriate. The final Rust compile used
`CARGO_BUILD_JOBS=2` and `cargo check -j 2 -p warp`.

When the full dry-run became too hot and slow under the original implementation,
the running dry-run was stopped and the script was optimized for dry-run
counting instead of continuing to stress the local machine.

No GUI, account, backend, static image, or destructive state mutation was
performed.

## Release Decision

RC14 is `ready-for-local-use-with-fixture-evidence`.

Reasoning:

- Manifest drift gate is clean: `missing: 0`, `would_change: 0`.
- Glossary and manifest checks pass.
- Manifest `context/status` metadata coverage is `100.0%`.
- Forbidden/awkward target-term search returned no matches.
- Locale JSON/YAML exports complete and JSON parses.
- Python localization tests pass.
- Rust formatting, whitespace checks, and `cargo check -j 2 -p warp` pass.
- Release preset source-level coverage improved from RC13 `93.8%` to RC14 `95.1%`.
- Terminal and AI/Agent source residue were reduced while preserving protocol,
  tool, parser, fixture, and provider contracts.
- Static image residue and public-RC external-state blockers are explicitly
  documented instead of being treated as source drift.

RC14 is not `ready-for-public-rc` because isolated-account/backend evidence and
regenerated/static-art approval are still unavailable.

## Next Gate

Before public RC:

1. Provide a disposable test account/team and backend fixture states from
   `docs/zh-Hans-public-rc-gate-runbook.md`.
2. Capture cropped/redacted screenshots for account/state rows.
3. Confirm cleanup for every disposable object.
4. Regenerate or replace the deferred onboarding PNGs with Chinese-localized
   preview art, or record explicit design approval for the current assets.
5. Keep fixture evidence separate from true account-verified evidence.
6. Re-run the command-line gate and reconsider `ready-for-public-rc`.
