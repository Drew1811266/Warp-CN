# zh-Hans Release Candidate 2026-06-02 RC26

Date: 2026-06-02

## Scope

RC26 covers Phases 165 through 176. It confirms the RC25 baseline, reruns the
source drift sentinel, checks the machine quiet-window gate, keeps full compile,
bundle, and GUI work skipped under heat-safety rules, keeps Agent lifecycle
fixture evidence at source-anchor level, refreshes the public-RC handoff,
rechecks onboarding PNG assets, refreshes locale exports, runs evidence hygiene,
and freezes the next readiness decision.

RC26 does not add manifest translations, change PNG assets, produce GUI
evidence, build a bundle, log in, create backend fixtures, touch billing/cloud
state, create or delete managed secrets/endpoints, or mutate team state.

The RC26 delta is:

```text
RC25 baseline and drift sentinel
quiet-window eligibility gate
heat-safe full compile skip
bundle skip because compile prerequisite was unmet
no-account GUI smoke skip because no fresh bundle exists
Agent lifecycle rendered fixture Option A decision
source-anchor-only lifecycle deferral
public-RC registry and handoff refresh
onboarding PNG asset gate
locale export readiness refresh
evidence hygiene and privacy sweep
RC26 readiness freeze
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

Coverage remains inherited from RC25 because RC26 did not add source
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

## Quiet-Window Gate

Phase 166 ran two probes with a 60-second cooling window. No target
`cargo`/`rustc`/`WarpOss` process or macOS thermal/performance warning was
found, but desktop/Codex/Finder CPU activity remained elevated.

```text
probe 1 load: 2.75 2.71 2.86
probe 2 load: 2.29 2.59 2.80
probe 2 high CPU: WindowServer, Finder, Codex
decision: heavy-gates-not-eligible
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

Phase 170 chose Option A because Phase 169 did not produce a fresh bundle or
GUI evidence path. Phase 171 therefore made no Rust source changes and kept
the lifecycle fixture deferred as source-anchor-only evidence.

## Public-RC Blocker Registry

```text
registry: resources/localization/zh-Hans-public-rc-blockers.toml
script: script/zh_public_rc_status.py
handoff docs:
  docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md
  docs/zh-Hans-backend-fixture-contract-rc19.md
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

No blocker was cleared in RC26.

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
reason: RC26 made no Rust source changes after RC22
```

Skipped or blocked:

```text
full Rust compile: skipped-no-quiet-window
bundle build: skipped-prerequisite-unmet-and-no-quiet-window
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
onboarding PNG total: 54
future asset branch: codex/zh-Hans-onboarding-assets-rc20
authorization package: docs/zh-Hans-onboarding-asset-authorization-rc20.md
script package: docs/zh-Hans-onboarding-visual-script-package.md
regeneration plan: docs/zh-Hans-onboarding-visual-regeneration-plan.md
```

The 50 deferred onboarding PNGs still require asset-only regeneration,
design/product approval, before/after contact sheets, binary scope proof, and
visual QA.

## Locale Export Status

```text
/tmp/warp-cn-zh-Hans-locale-rc26.json: 2566862 bytes
/tmp/warp-cn-zh-Hans-locale-rc26.pretty.json: 3004049 bytes
/tmp/warp-cn-zh-Hans-locale-rc26.yaml: 2184303 bytes
exporter tests: 4 passed
localization Python tests: 25 passed
```

## Low-Load Review

All validation commands were run serially. Heavy compile and bundle were not
run because Phase 166 found elevated load and high desktop/Codex/Finder CPU
activity despite no macOS thermal warning. GUI was not launched because the
current cycle did not produce a fresh bundle.

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC26 is acceptable for local use and continued fixture/evidence development. It
is not acceptable as public RC until full Rust compile and bundle can run
safely, current-cycle GUI evidence is complete, isolated account evidence is
complete, backend/disposable fixture evidence is complete, and onboarding PNG
visual evidence is regenerated or design-approved.
