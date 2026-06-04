# zh-Hans Release Candidate 2026-06-02 RC30

Date: 2026-06-02

## Scope

RC30 covers Phases 212 through 219. It audits the post-RC29 evidence branch,
rechecks the heavy validation window, records GUI smoke dependency status,
refreshes isolated-account/backend-fixture/disposable-object gates, rechecks the
PNG asset branch decision, and freezes the next local-use decision.

RC30 does not add manifest translations, change PNG assets, produce GUI
evidence, build a bundle, log in, create backend fixtures, touch billing/cloud
state, create or delete managed secrets/endpoints, mutate team state, mutate
Git refs, stage, commit, push, merge, or rebase.

The RC30 delta is:

```text
post-RC29 evidence branch hygiene checked
publication/integration confirmed to require explicit user approval
heavy Rust/bundle validation skipped under heat-safety rules
no-account GUI smoke skipped because no fresh bundle exists
isolated-account prerequisites still blocked
backend-fixture prerequisites still blocked
disposable-object prerequisites still blocked
PNG asset branch deferred because no design/product approval exists
RC30 readiness freeze
```

## Manifest And Coverage

Manifest and source coverage remain inherited from RC29 because RC30 did not add
translation entries.

```text
manifest entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
metadata context/status coverage: 100.0%
release: covered 8574, candidates 2, coverage 100.0%
```

Remaining source candidates are still intentional preserved terms:

```text
app/src/ai/blocklist/usage/rollup.rs: Agent
app/src/terminal/view/ambient_agent/block/harness_session_header.rs: Agent
```

## Heavy Gate And GUI Status

Phase 213 captured two load probes before heavy validation:

```text
probe 1 load: 3.44 3.63 3.21
probe 1 top CPU: WindowServer 46.9%, Codex Service 31.7%, Finder 15.9%
probe 2 load: 2.31 3.23 3.09
probe 2 top CPU: WindowServer 42.3%, Codex Service 18.3%, Finder 15.7%, trustd 15.4%
```

Decision:

```text
Rust compile: skipped-with-heat-safety
fresh bundle: skipped-with-heat-safety
bundle build: skipped-with-heat-safety
GUI launch: skipped-no-fresh-bundle
```

Phase 214 did not launch GUI because no fresh current-cycle bundle existed.

```text
no-account GUI smoke: skipped-no-fresh-bundle
screenshots/accessibility snapshots: none
rows promoted: none
```

## Public-RC Blocker Registry

```text
registry: resources/localization/zh-Hans-public-rc-blockers.toml
script: script/zh_public_rc_status.py
total: 11
blocked-no-backend-fixture: 5
blocked-no-disposable-object: 3
blocked-no-isolated-account: 3
```

No blocker was cleared in RC30.

Blocked rows:

```text
GUI-AUTH-01
GUI-SET-03
GUI-SET-04
GUI-SET-05
GUI-SET-06
GUI-WS-04
GUI-WS-06
GUI-WS-07
GUI-BILL-01
GUI-BILL-02
GUI-CLOUD-01
```

No account, backend, billing, cloud, managed secret, custom endpoint,
disposable object, or team state was read or mutated.

## PNG Asset Status

Onboarding PNG assets remain unchanged:

```text
onboarding PNG total: 54
current branch PNG changes: none
deferred asset count: 50
accepted decorative/brand asset count: 4
asset branch: deferred
decision: blocked-no-asset-approval
```

The visual residue is still bitmap/static-art residue, not source-string or
manifest drift.

## Command-Line Gates

Passed:

```text
manifest validation
glossary check
metadata summary
dry-run summary
release inventory coverage
public-RC blocker summary
privacy guard
Python localization tests: 25 passed
cargo fmt --check
git diff --check
```

Skipped for heat-safety:

```text
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
open -n target/debug/bundle/osx/WarpOss.app
```

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC30 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until fresh bundle/current-cycle GUI evidence
exists, all 11 public-RC blockers are cleared with real matching evidence,
onboarding PNG visual status is approved or regenerated, and any public wording
about upstream stable ancestry is backed by an approved upstream-sync branch or
explicit commit/tree evidence.
