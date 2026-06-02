# zh-Hans Release Candidate 2026-06-02 RC17

RC17 is the Phase 87-94 post-RC16 localization record for Warp CN.

Generated: 2026-06-02 Asia/Shanghai.

Decision: `ready-for-local-use-with-fixture-evidence`

Public RC decision: not ready.

## Scope

RC17 includes:

- RC16 branch hygiene and RC17 upstream freshness rules.
- Public-RC evidence templates and fixture readiness package.
- Low-risk local GUI smoke preparation.
- Isolated-account blocker evidence.
- Backend, billing, cloud, team, AWS, managed-secret, and disposable-object
  fixture blocker evidence.
- Onboarding visual asset branch preparation and before contact sheet.
- Onboarding PNG regeneration blocker record.
- Final RC17 language/export/Python/format/diff freeze gate.

RC17 does not claim first-party runtime i18n support, complete whole-repository
localization, regenerated onboarding imagery, real account/backend verification,
or public-RC GUI readiness.

## Manifest And Coverage

```text
entries: 7943
key: 150 (1.9%)
context: 7943 (100.0%)
status: 7943 (100.0%)
preserve_terms: 155 (2.0%)
expected_count: 195 (2.5%)

dry-run:
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

Remaining source candidates are intentional `Agent` preserve terms:

```text
app/src/ai/blocklist/usage/rollup.rs: Agent
app/src/terminal/view/ambient_agent/block/harness_session_header.rs: Agent
```

Locale exports:

```text
/tmp/warp-cn-zh-Hans-locale-rc17.json: 2566862 bytes
/tmp/warp-cn-zh-Hans-locale-rc17.pretty.json: 3004049 bytes
/tmp/warp-cn-zh-Hans-locale-rc17.yaml: 2184303 bytes
```

## Command-Line Gate

Passed:

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --check-glossary
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
nice -n 10 python3 script/zh_export_locale.py --format json > /tmp/warp-cn-zh-Hans-locale-rc17.json
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc17.json > /tmp/warp-cn-zh-Hans-locale-rc17.pretty.json
nice -n 10 python3 script/zh_export_locale.py --format yaml > /tmp/warp-cn-zh-Hans-locale-rc17.yaml
nice -n 10 python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py
nice -n 10 python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
nice -n 10 cargo fmt --check
git diff --check
```

Python tests:

```text
19 tests passed
```

Rust compile gate:

```text
skipped-with-heat-safety
```

RC16 already passed `CARGO_BUILD_JOBS=1 nice -n 15 cargo check -j 1 -p warp`.
Phases 87-93 changed documentation/planning records only plus a `/tmp` contact
sheet; no Rust source or PNG asset was modified after RC16.

## Source Localization Delta From RC16

```text
manifest entries: 7943 -> 7943
release coverage: 100.0% -> 100.0%
modals coverage: 100.0% -> 100.0%
terminal coverage: 100.0% -> 100.0%
AI / Agent coverage: 100.0% -> 100.0%
workspace coverage: 100.0% -> 100.0%
settings coverage: 100.0% -> 100.0%
```

RC17 did not add source translations. It preserved the RC16 source state and
focused on release evidence, blocker documentation, and asset preparation.

## Public-RC Evidence Status

Created or updated:

```text
docs/gui-smoke-artifacts/phase88/README.md
docs/gui-smoke-artifacts/phase88/evidence-template.md
docs/gui-smoke-artifacts/phase89/README.md
docs/gui-smoke-artifacts/phase90/README.md
docs/gui-smoke-artifacts/phase91/README.md
docs/zh-Hans-localization-phase88.md
docs/zh-Hans-localization-phase89.md
docs/zh-Hans-localization-phase90.md
docs/zh-Hans-localization-phase91.md
docs/zh-Hans-gui-smoke-matrix.md
```

Public RC remains blocked by:

```text
GUI-AUTH-01: blocked-no-isolated-account
GUI-SET-03: blocked-no-isolated-account
GUI-SET-04: blocked-no-backend-fixture
GUI-SET-05: blocked-no-backend-fixture
GUI-SET-06: blocked-no-disposable-object
GUI-WS-04: blocked-no-disposable-object
GUI-WS-06: blocked-no-isolated-account
GUI-WS-07: blocked-no-disposable-object
GUI-BILL-01: blocked-no-backend-fixture
GUI-BILL-02: blocked-no-backend-fixture
GUI-CLOUD-01: blocked-no-backend-fixture
```

No GUI, browser login, account callback, backend fixture, billing/quota state,
cloud environment, managed secret, team ownership, or endpoint was touched.

## Static Visual Asset Status

Created:

```text
/tmp/warp-cn-onboarding-assets-rc17/before-contact-sheet.png
docs/zh-Hans-localization-phase92.md
docs/zh-Hans-localization-phase93.md
```

Status:

```text
before contact sheet: generated outside repository
after contact sheet: not generated
changed PNGs: none
deferred PNGs still requiring regeneration: 50
decorative/brand PNGs kept unchanged: 4
```

Public-facing visual polish remains blocked until an asset-only branch,
approved regeneration, after contact sheet, binary-scope proof, and visual QA
exist.

## Upstream Freshness Status

Phase 87 updated `docs/zh-Hans-upstream-sync.md` with RC17 freshness rules. No
network fetch, merge, rebase, branch switch, or destructive Git operation was
performed.

## Low-Load Review

The RC17 work was run serially. Python, inventory, export, and formatting
commands used reduced priority where appropriate. Bundle build, GUI launch,
Rust compile, network fetch, account login, backend fixture creation, billing
mutation, cloud mutation, team mutation, secret mutation, endpoint mutation, and
image generation were skipped for heat and state safety.

## Release Decision

RC17 is `ready-for-local-use-with-fixture-evidence`.

Reasoning:

- Manifest validation and glossary checks pass.
- Manifest drift gate is clean: `missing: 0`, `would_change: 0`.
- Manifest `context/status` metadata coverage is `100.0%`.
- All tracked source localization inventory areas remain at `100.0%`.
- Remaining source candidates are intentional `Agent` preserve terms.
- Locale JSON/YAML exports complete and JSON parses.
- Python localization tests pass.
- Rust formatting and whitespace checks pass.
- Rust compile was skipped for heat-safety and no Rust source changed after the
  RC16 compile gate.
- Public-RC evidence and onboarding visual assets remain explicitly blocked.
