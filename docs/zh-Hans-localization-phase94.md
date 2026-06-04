# zh-Hans Localization Phase 94

Date: 2026-06-02 Asia/Shanghai.

## Goal

Phase 94 produces the RC17 freeze and public-readiness decision after Phases
87-93 qualified.

## Phase 87-93 Qualification Summary

```text
Phase 87: qualified; RC17 upstream freshness rules documented, no fetch/merge/rebase.
Phase 88: qualified; public-RC evidence templates and fixture statuses prepared.
Phase 89: qualified as preparation-only; safe local GUI smoke rows identified, bundle skipped for heat-safety.
Phase 90: qualified as blocked-with-evidence; isolated account profile absent.
Phase 91: qualified as blocked-with-evidence; backend/disposable fixtures absent.
Phase 92: qualified as preparation-only; before contact sheet generated outside repo, no PNG modified.
Phase 93: qualified as blocked-with-evidence; PNG regeneration blocked by missing asset branch and approval.
```

## Manifest And Dry-Run

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
manifest validation passed

nice -n 10 python3 script/zh_apply_localization.py --check-glossary
glossary check passed

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

Remaining source candidates remain the intentional `Agent` preserve term:

```text
app/src/ai/blocklist/usage/rollup.rs: Agent
app/src/terminal/view/ambient_agent/block/harness_session_header.rs: Agent
```

## Locale Exports

```text
/tmp/warp-cn-zh-Hans-locale-rc17.json: 2566862 bytes
/tmp/warp-cn-zh-Hans-locale-rc17.pretty.json: 3004049 bytes
/tmp/warp-cn-zh-Hans-locale-rc17.yaml: 2184303 bytes
```

JSON parse passed via:

```text
python3 -m json.tool /tmp/warp-cn-zh-Hans-locale-rc17.json
```

## Command-Line Gate

Passed:

```text
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

Reason: the user explicitly requested avoiding local machine overheating. RC16
already passed `CARGO_BUILD_JOBS=1 nice -n 15 cargo check -j 1 -p warp`, and
Phases 87-93 changed documentation/planning records only plus a `/tmp` contact
sheet. No Rust source or PNG asset was modified after the RC16 compile gate.

## Public-RC Decision

Public RC remains blocked.

Missing evidence:

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

Static visual asset polish remains blocked:

```text
50 deferred onboarding PNGs still require an asset-only branch, approved regeneration, after contact sheet, and visual QA.
```

## Low-Load Review

Commands were run serially. Python, inventory, export, and formatting commands
used reduced priority where appropriate. GUI launch, bundle build, network
fetch, account login, backend fixture creation, billing/quota mutation, cloud
mutation, team ownership mutation, secret mutation, endpoint mutation, and image
generation were not run.

## Qualification Result

Qualified.

RC17 is `ready-for-local-use-with-fixture-evidence`, not public-RC ready.

Phase 94 passed because manifest validation, glossary, dry-run, coverage,
locale export, JSON parse, Python compile, Python tests, formatting, and diff
hygiene passed; Rust compile was intentionally skipped for heat-safety with
unchanged Rust source since RC16; and all remaining public-RC and visual-asset
blockers are explicit.
