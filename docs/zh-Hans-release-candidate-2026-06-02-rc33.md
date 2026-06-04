# zh-Hans Release Candidate 2026-06-02 RC33

Date: 2026-06-02

## Scope

RC33 covers Phases 236 through 243. It adds public-RC evidence report and packet
template helpers, optional strict-artifact linting, a lane-readiness package,
asset/GUI dependency recheck, heat-gated heavy validation retry, and the next
local-use/public-RC decision freeze.

RC33 does not add manifest translations, change PNG assets, produce GUI
evidence, log in, create backend fixtures, touch billing/cloud state, create or
delete managed secrets/endpoints, mutate team state, mutate Git refs, stage,
commit, push, merge, or rebase.

## Evidence Packet Readiness

```text
evidence report: script/zh_public_rc_evidence_report.py
evidence linter strict mode: script/zh_public_rc_evidence_lint.py --strict-artifacts
public-RC rows tracked: 11
ready rows: 0
rows promoted in RC33: 0
```

Current lane report:

```text
backend_fixture: total=5 ready=0 missing=5
disposable_object: total=3 ready=0 missing=3
isolated_account: total=3 ready=0 missing=3
decision: blocked
```

## Manifest And Coverage

```text
manifest entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
metadata context/status coverage: 100.0%
release: covered 8574, candidates 2, coverage 100.0%
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

No blocker was cleared in RC33.

## Heavy Gate And GUI Status

Phase 242 ran the helper with two probes:

```text
probe 1: load=2.20 2.56 2.69
probe 1: hot_process=WindowServer 42.5%
probe 1: hot_process=Codex (Service) 31.1%
probe 2: load=2.61 2.60 2.69
probe 2: hot_process=WindowServer 44.7%
decision: defer-heavy-gate
```

Decision:

```text
Rust compile: skipped-with-heat-safety
fresh bundle: skipped-with-heat-safety
bundle build: skipped-with-heat-safety
GUI launch: skipped-no-fresh-bundle
```

## PNG Asset Status

```text
onboarding PNG total: 54
current branch PNG changes: none
deferred asset count: 50
accepted decorative/brand asset count: 4
asset branch: deferred
decision: blocked-no-asset-approval
```

## Command-Line Gates

Passed:

```text
manifest validation
glossary check
metadata summary
dry-run summary
release inventory coverage
public-RC blocker summary
public-RC evidence report
privacy guard
Python localization, public-RC, report, and gate tests: 40 passed
cargo fmt --check
git diff --check
```

Expected blocker signal:

```text
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
exit_code: 1
decision: fail
reason: 11 rows still missing evidence
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

RC33 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until strict evidence lint passes with real
matching redacted artifacts, raw evidence is reviewed, fresh bundle/current-cycle
GUI evidence exists, onboarding PNG visual status is approved or regenerated,
and publication is explicitly approved by the user.
