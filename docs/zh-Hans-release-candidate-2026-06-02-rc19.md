# zh-Hans Release Candidate 2026-06-02 RC19

Date: 2026-06-02

## Scope

RC19 covers the evidence-hardening pass from Phases 103 through 110. It does
not add new source translations, manifest entries, scripts, locale schema
changes, or PNG assets. The delta is tracked evidence durability, RC19 runbooks
and fixture contracts, asset authorization, and an updated release decision.

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

Remaining source candidates are intentional preserved terms:

```text
app/src/ai/blocklist/usage/rollup.rs: Agent
app/src/terminal/view/ambient_agent/block/harness_session_header.rs: Agent
```

## Command-Line Gate Results

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
PNG regeneration: documentation-only authorization package, no generation
```

## Source Localization Delta From RC18

```text
new manifest entries: 0
new source translations: 0
new script behavior: 0
new PNG assets: 0
documentation/evidence records: Phases 103-110, artifact index, fixture specs,
isolated-account runbook, backend fixture contract, and asset authorization
```

## Tracked Evidence Durability Status

Phase 103 created tracked evidence for local ignored artifact README summaries:

```text
docs/zh-Hans-gui-smoke-artifact-index-rc19.md
```

The ignored artifact directory remains ignored by `.gitignore`; raw screenshots
and recordings are not public-RC evidence unless separately reviewed, redacted,
approved, and intentionally added.

## GUI Evidence Status

Phase 105 did not run bundle or GUI because of heat-safety constraints. The
low-risk GUI rows remain ready for a future cool-machine run:

```text
GUI-BASE-01
GUI-BASE-02
GUI-BASE-03
GUI-BASE-04
GUI-BASE-05
GUI-ONB-01
GUI-ONB-02
GUI-AUTH-03
GUI-SET-01
GUI-SET-02
GUI-WS-08
```

No row was promoted to current-cycle public-RC verified in RC19.

## Public-RC Account And Backend Fixture Status

New handoff documents:

```text
docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md
docs/zh-Hans-backend-fixture-contract-rc19.md
docs/zh-Hans-local-fixture-spec-rc19.md
```

Current blockers:

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

## Static Visual Asset Status

```text
current branch PNG changes: none
PNG generation: not run
future asset branch: codex/zh-Hans-onboarding-assets-rc19
authorization package: docs/zh-Hans-onboarding-asset-authorization-rc19.md
```

The 50 deferred onboarding PNGs still require asset-only regeneration, design
approval, before/after contact sheets, binary scope proof, and visual QA.

## Upstream Freshness Status

RC19 inherits RC18 source freshness because Phases 103 through 110 did not add
source translations or manifest entries. The final dry-run remains clean with
`would_change: 0` and `missing: 0`.

## Low-Load Review

All commands were run serially. Heavy gates were skipped or blocked rather than
executed because the active goal required avoiding local overheating.

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC19 is acceptable for local use with fixture evidence. It is not acceptable as
public RC until Rust compile can be run safely, current-cycle GUI evidence is
complete, isolated account evidence is complete, backend/disposable fixture
evidence is complete, and onboarding PNG visual evidence is regenerated or
design-approved.

