# zh-Hans Release Candidate 2026-06-02 RC23

Date: 2026-06-02

## Scope

RC23 covers Phases 135 through 143. It reviews the RC22 baseline, confirms no
new source drift, reattempts heavy compile/bundle eligibility under heat-safety
rules, records a no-account GUI skip, keeps Agent lifecycle fixture evidence at
source-anchor level, refreshes public-RC prerequisites, rechecks onboarding PNG
approval, runs evidence hygiene, and freezes the next readiness decision.

RC23 does not add manifest translations, change PNG assets, produce GUI
evidence, build a bundle, log in, create backend fixtures, touch billing/cloud
state, create or delete managed secrets/endpoints, or mutate team state.

The RC23 delta is:

```text
RC22 baseline and drift sentinel
heat-safe heavy gate reattempt decision
no-account GUI smoke skip
Agent lifecycle fixture feasibility decision
source-anchor-only implementation deferral
public-RC external prerequisite refresh
onboarding PNG asset branch decision
evidence hygiene and privacy sweep
RC23 readiness freeze
```

## Manifest And Coverage

```text
manifest entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
metadata context/status: 7943 (100.0%)
```

Coverage remains inherited from RC22 because RC23 did not add source
translation entries:

```text
release: covered 8574, candidates 2, coverage 100.0%
terminal custom scan: covered 2178, candidates 1, coverage 100.0%
AI custom scan: covered 2515, candidates 1, coverage 100.0%
```

Remaining source candidates are intentional preserved terms:

```text
app/src/ai/blocklist/usage/rollup.rs: Agent
app/src/terminal/view/ambient_agent/block/harness_session_header.rs: Agent
```

## Fixture Status

```text
env gate: WARP_CN_AGENT_LIFECYCLE_SMOKE
scope: debug/test-only local lifecycle model probe
current evidence: source-anchor / fixture-prep
GUI evidence produced: no
GUI-AGENT-03 status: needs-trigger
public-RC impact: none
```

Phase 138 chose to keep the fixture source-anchor-only because no fresh bundle
or safe GUI run was available and the rendered lifecycle path still depends on
`WaitingForSession` / `ProgressUpdated` model-view state. Phase 139 therefore
made no Rust source changes.

## Public-RC Blocker Registry

```text
registry: resources/localization/zh-Hans-public-rc-blockers.toml
script: script/zh_public_rc_status.py
```

Summary:

```text
total: 11
public_rc_required: 11
blocked-no-backend-fixture: 5
blocked-no-disposable-object: 3
blocked-no-isolated-account: 3
backend_fixture: 5
disposable_object: 3
isolated_account: 3
```

No blocker was cleared in RC23.

## Command-Line Gate Results

Passed:

```text
manifest validation
glossary check
metadata summary
dry-run summary
source drift sentinel
public-RC blocker summary
JSON locale export
JSON parse
YAML locale export
Python compile checks
Python localization tests: 25 passed
cargo fmt --check
git diff --check
privacy guard
PNG diff/status check: no PNG changes
```

Carried forward:

```text
targeted Rust fixture tests from RC22: 4 passed, 0 failed, 4715 filtered out
reason: RC23 made no Rust source changes after RC22
```

Skipped or blocked:

```text
full Rust compile: skipped-with-heat-safety
bundle build / GUI launch: skipped-with-heat-safety
no-account GUI smoke: skipped-no-fresh-bundle
PNG regeneration: blocked-no-asset-approval
public-RC external evidence: blocked-no-prerequisites
```

## Static Visual Asset Status

```text
current branch PNG changes: none
PNG generation: not run
future asset branch: codex/zh-Hans-onboarding-assets-rc20
authorization package: docs/zh-Hans-onboarding-asset-authorization-rc20.md
```

The 50 deferred onboarding PNGs still require asset-only regeneration,
design/product approval, before/after contact sheets, binary scope proof, and
visual QA.

## Low-Load Review

All validation commands were run serially. Heavy compile and bundle were not
run because Phase 136 found load averages `4.22 3.74 3.58` with active
WindowServer, Codex, and mdworker CPU usage. Phase 137 skipped GUI because no
fresh bundle was available and load remained elevated.

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC23 is acceptable for local use and continued fixture/evidence development. It
is not acceptable as public RC until full Rust compile and bundle can run safely,
current-cycle GUI evidence is complete, isolated account evidence is complete,
backend/disposable fixture evidence is complete, and onboarding PNG visual
evidence is regenerated or design-approved.
