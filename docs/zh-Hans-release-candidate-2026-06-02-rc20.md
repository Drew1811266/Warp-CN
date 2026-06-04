# zh-Hans Release Candidate 2026-06-02 RC20

Date: 2026-06-02

## Scope

RC20 covers Phases 111 through 118. It does not add new source translations,
manifest entries, PNG assets, GUI evidence, bundle evidence, account evidence,
backend fixture evidence, billing evidence, cloud evidence, managed-secret
evidence, endpoint evidence, or team evidence.

The RC20 delta is evidence automation and planning:

```text
public-RC blocker registry
public-RC blocker summary script and tests
public-RC registry integration in docs
local fixture implementation readiness plan
heat-safe compile/GUI decision refresh
RC20 onboarding asset authorization refresh
upstream drift sentinel
RC20 readiness freeze
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

Coverage remains inherited from RC19 because Phases 111 through 118 did not add
source translations or manifest entries:

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

## Public-RC Blocker Registry

```text
registry: resources/localization/zh-Hans-public-rc-blockers.toml
script: script/zh_public_rc_status.py
tests: script/test_zh_public_rc_status.py
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

No blocker was cleared in RC20.

## Local Fixture Implementation Readiness

```text
plan: docs/zh-Hans-local-fixture-implementation-plan-rc20.md
status: planning-ready
Rust fixture implementation in RC20: none
```

Visible GUI only:

```text
GUI-AUTH-02
GUI-AGENT-01
```

Debug fixture design:

```text
GUI-AGENT-02
GUI-AGENT-03
GUI-AGENT-04
GUI-AGENT-05
GUI-WS-02
GUI-WS-03
```

Manual only:

```text
GUI-WS-05
```

## Command-Line Gate Results

Passed:

```text
manifest validation
glossary check
metadata summary
dry-run summary
public-RC blocker summary
JSON locale export
JSON parse
YAML locale export
Python compile checks
Python localization tests: 25 passed
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

## Static Visual Asset Status

```text
current branch PNG changes: none
PNG generation: not run
future asset branch: codex/zh-Hans-onboarding-assets-rc20
authorization package: docs/zh-Hans-onboarding-asset-authorization-rc20.md
```

The 50 deferred onboarding PNGs still require asset-only regeneration, design
approval, before/after contact sheets, binary scope proof, and visual QA.

## Upstream Freshness Status

Phase 117 found no new source translation work. The only candidate rows remain
the two intentional preserved `Agent` terms listed above.

## Low-Load Review

All validation commands were run serially. Heavy compile, GUI, bundle, account,
backend, billing, cloud, managed-secret, endpoint, team, and PNG generation
workflows were not run because the active goal required avoiding local
overheating.

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC20 is acceptable for local use with fixture evidence. It is not acceptable as
public RC until Rust compile can run safely, current-cycle GUI evidence is
complete, isolated account evidence is complete, backend/disposable fixture
evidence is complete, and onboarding PNG visual evidence is regenerated or
design-approved.

