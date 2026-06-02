# zh-Hans Release Candidate 2026-06-02 RC25

Date: 2026-06-02

## Scope

RC25 covers Phases 153 through 164. It confirms the RC24 baseline, reruns the
source drift sentinel, reattempts compile/bundle/GUI gates under heat-safety
rules, keeps Agent lifecycle fixture evidence at source-anchor level, refreshes
the public-RC registry, rechecks isolated account/backend/disposable object
prerequisites, rechecks onboarding PNG approval, refreshes locale exports, runs
evidence hygiene, and freezes the next readiness decision.

RC25 does not add manifest translations, change PNG assets, produce GUI
evidence, build a bundle, log in, create backend fixtures, touch billing/cloud
state, create or delete managed secrets/endpoints, or mutate team state.

The RC25 delta is:

```text
RC24 baseline and drift sentinel
heat-safe full compile skip
bundle skip because compile prerequisite was unmet
no-account GUI smoke skip because no fresh bundle exists
Agent lifecycle rendered fixture Option A decision
source-anchor-only lifecycle deferral
public-RC registry refresh
isolated account blocker gate
backend fixture and disposable object blocker gate
onboarding PNG asset approval recheck
locale export readiness refresh
evidence hygiene and privacy sweep
RC25 readiness freeze
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

Coverage remains inherited from RC24 because RC25 did not add source
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

Phase 157 chose Option A because Phase 156 did not produce a fresh bundle or
GUI evidence path. Phase 158 therefore made no Rust source changes and kept
the lifecycle fixture deferred as source-anchor-only evidence.

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

No blocker was cleared in RC25.

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
reason: RC25 made no Rust source changes after RC22
```

Skipped or blocked:

```text
full Rust compile: skipped-with-heat-safety
bundle build: skipped-prerequisite-unmet-and-heat-safety
no-account GUI smoke: skipped-no-fresh-bundle
Agent lifecycle rendered fixture: deferred-source-anchor-only
isolated account evidence: blocked-no-isolated-account
backend fixture evidence: blocked-no-backend-fixture
disposable object evidence: blocked-no-disposable-object
PNG regeneration: blocked-no-asset-approval
```

## Static Visual Asset Status

```text
current branch PNG changes: none
PNG generation: not run
future asset branch: codex/zh-Hans-onboarding-assets-rc20
authorization package: docs/zh-Hans-onboarding-asset-authorization-rc20.md
script package: docs/zh-Hans-onboarding-visual-script-package.md
```

The 50 deferred onboarding PNGs still require asset-only regeneration,
design/product approval, before/after contact sheets, binary scope proof, and
visual QA.

## Locale Export Status

```text
/tmp/warp-cn-zh-Hans-locale-rc25.json: 2566862 bytes
/tmp/warp-cn-zh-Hans-locale-rc25.pretty.json: 3004049 bytes
/tmp/warp-cn-zh-Hans-locale-rc25.yaml: 2184303 bytes
exporter tests: 4 passed
```

## Low-Load Review

All validation commands were run serially. Heavy compile and bundle were not
run because Phase 154 and Phase 155 found elevated load and high
desktop/system/Codex CPU activity despite no macOS thermal warning. GUI was
not launched because the current cycle did not produce a fresh bundle.

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC25 is acceptable for local use and continued fixture/evidence development. It
is not acceptable as public RC until full Rust compile and bundle can run
safely, current-cycle GUI evidence is complete, isolated account evidence is
complete, backend/disposable fixture evidence is complete, and onboarding PNG
visual evidence is regenerated or design-approved.
