# zh-Hans Release Candidate 2026-06-02 RC18

Date: 2026-06-02

## Scope

RC18 covers the post-RC17 evidence pass from Phases 95 through 102. It does not
add new source translations, manifest entries, scripts, locale schema changes,
or PNG assets. The delta is release evidence, GUI/public-RC handoff
documentation, and an RC18 readiness decision.

## Manifest And Coverage

```text
manifest entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
metadata context/status: 7943 (100.0%)
```

```text
onboarding: covered 323, candidates 0, coverage 100.0%
workspace: covered 865, candidates 0, coverage 100.0%
search: covered 269, candidates 0, coverage 100.0%
settings: covered 2024, candidates 0, coverage 100.0%
modals: covered 5240, candidates 2, coverage 100.0%
release: covered 8574, candidates 2, coverage 100.0%
terminal: covered 2178, candidates 1, coverage 100.0%
AI / Agent: covered 2515, candidates 1, coverage 100.0%
```

Remaining candidates are intentional preserved terms:

```text
app/src/ai/blocklist/usage/rollup.rs: Agent
app/src/terminal/view/ambient_agent/block/harness_session_header.rs: Agent
```

## Command-Line Gates

Passed:

```text
manifest validation
glossary check
metadata summary
dry-run summary
coverage snapshots
JSON locale export
JSON parse
YAML locale export
Python compile checks
Python localization tests: 19 passed
cargo fmt --check
git diff --check
PNG diff/status check: no PNG changes
```

Skipped or blocked:

```text
Rust compile: skipped-with-heat-safety
bundle build / GUI launch: skipped-with-heat-safety
PNG regeneration: blocked-no-clean-asset-branch-or-approval
```

## Source Localization Delta From RC17

```text
new manifest entries: 0
new source translations: 0
new script behavior: 0
new PNG assets: 0
documentation/evidence records: Phases 95-102 and GUI smoke artifact READMEs
```

## Public-RC Evidence Status

Public RC remains blocked.

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

Phase 98 defines the isolated account handoff for `zh-rc18-test-account`. Phase
99 defines the backend and disposable fixture handoff names.

## Static Visual Asset Status

```text
onboarding PNG changes in current branch: none
PNG regeneration status: blocked-no-clean-asset-branch-or-approval
future asset branch: codex/zh-Hans-onboarding-assets-rc18
```

The 50 deferred onboarding PNGs still require asset-only regeneration, design
approval, before/after contact sheets, binary scope proof, and visual QA.

## Upstream Freshness Status

RC18 inherits RC17 source freshness because Phases 95 through 102 did not add
new source translations or manifest entries. The final dry-run remains clean
with `would_change: 0` and `missing: 0`.

## Low-Load Review

All commands were run serially. Heavy gates were skipped or blocked rather than
executed because the active goal required avoiding local overheating.

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC18 is acceptable for local use with fixture evidence. It is not acceptable as
public RC until isolated account, backend/disposable fixture, GUI/bundle, and
approved PNG visual evidence are complete.

