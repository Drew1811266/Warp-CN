# zh-Hans Release Candidate 2026-06-02 RC31

Date: 2026-06-02

## Scope

RC31 covers Phases 220 through 227. It adds a repeatable low-load gate helper,
documents heat-safe validation, retries heavy validation through that helper,
records current-cycle GUI dependency status, creates a public-RC action package,
separates publication readiness from evidence readiness, and freezes the next
local-use decision.

RC31 does not add manifest translations, change PNG assets, produce GUI
evidence, build a bundle, log in, create backend fixtures, touch billing/cloud
state, create or delete managed secrets/endpoints, mutate team state, mutate
Git refs, stage, commit, push, merge, or rebase.

The RC31 delta is:

```text
post-RC30 branch baseline checked
repeatable low-load gate helper added
heat-safe validation docs added
heavy Rust/bundle validation skipped by helper defer decision
current-cycle GUI smoke skipped because no fresh bundle exists
public-RC action package created
publication readiness separated from evidence completion
RC31 readiness freeze
```

## Manifest And Coverage

Manifest and source coverage remain inherited from RC30 because RC31 did not add
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

## Low-Load Gate Helper

Added:

```text
script/zh_low_load_gate.py
script/test_zh_low_load_gate.py
docs/zh-Hans-heat-safe-validation.md
```

The helper returns:

```text
0: decision: run-heavy-gate
2: decision: defer-heavy-gate
```

Phase 221 tests:

```text
python3 -m unittest script/test_zh_low_load_gate.py
result: Ran 6 tests, OK
```

Final RC31 Python test suite:

```text
Python localization and gate tests: 31 passed
```

## Heavy Gate And GUI Status

Phase 223 ran the helper with two probes:

```text
probe 1: load=2.75 2.82 2.90
probe 2: load=2.31 2.70 2.85
decision: defer-heavy-gate
reason: probe 1: load average exceeds 2.50
reason: probe 2: load average exceeds 2.50
```

Decision:

```text
Rust compile: skipped-with-heat-safety
fresh bundle: skipped-with-heat-safety
bundle build: skipped-with-heat-safety
GUI launch: skipped-no-fresh-bundle
```

Phase 224 did not launch GUI because no fresh current-cycle bundle existed.

```text
current-cycle GUI smoke: skipped-no-fresh-bundle
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

No blocker was cleared in RC31. The actionable input list is now centralized in:

```text
docs/zh-Hans-public-rc-action-package-rc31.md
```

No account, backend, billing, cloud, managed secret, custom endpoint,
disposable object, or team state was read or mutated.

## Publication Boundary

Publication readiness is documented separately:

```text
docs/zh-Hans-publication-readiness-rc31.md
```

Current publication decision:

```text
stage: not run
commit: not run
push: not run
merge: not run
tag mutation: not run
```

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
Python localization and gate tests: 31 passed
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

RC31 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until the low-load helper allows fresh
bundle/current-cycle GUI evidence, all 11 public-RC blockers are cleared with
real matching evidence, onboarding PNG visual status is approved or regenerated,
and any public wording about upstream stable ancestry is backed by an approved
upstream-sync branch or explicit commit/tree evidence.
