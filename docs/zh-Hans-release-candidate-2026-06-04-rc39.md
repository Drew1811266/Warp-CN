# zh-Hans Release Candidate 2026-06-04 RC39

Date: 2026-06-04

## Scope

RC39 covers the Warp CN `0.19` adaptation to the official upstream stable tag
`v0.2026.06.03.09.49.stable_00`.

```text
upstream stable tag: v0.2026.06.03.09.49.stable_00
upstream stable commit: 2249469e5d24e472cee6ce97d3d324293f67db71
upstream stable tree: efe8ae7822765eb267792d441e4b1e7ddb7f8e53
adaptation branch: codex/zh-Hans-0.19-upstream-stable-adaptation
adaptation worktree: /Users/drew/Project/warp-cn-0.19-adaptation
```

RC39 imported the durable Warp CN localization assets into a clean upstream
stable worktree, repaired manifest drift, applied the zh-Hans overlay, translated
new 0.19 source candidates, generated full per-entry audit artifacts, and
refreshed the repository-facing adaptation docs.

RC39 does not publish, tag, push, launch the GUI, create backend fixtures, use an
isolated account, create or delete disposable objects, touch billing/cloud state,
or claim public-RC readiness.

## Manifest And Coverage

```text
manifest validation: passed
glossary check: passed
dry-run entries: 7937
dry-run files: 550
dry-run already_applied: 5717
dry-run would_change: 0
dry-run missing: 0
release inventory covered: 8534
release inventory candidates: 0
release inventory coverage: 100.0%
full audit actionable rows: 0
```

Preset coverage:

| Area | Covered | Candidates | Coverage |
| --- | ---: | ---: | ---: |
| Onboarding / Auth | 314 | 0 | 100.0% |
| Workspace | 874 | 0 | 100.0% |
| Search | 267 | 0 | 100.0% |
| Settings | 2,040 | 0 | 100.0% |
| Modals | 5,177 | 0 | 100.0% |
| Release aggregate | 8,534 | 0 | 100.0% |

## Full Translation Audit

Artifacts:

```text
docs/zh-Hans-full-translation-audit-0.19/entries.tsv
docs/zh-Hans-full-translation-audit-0.19/entries.json
docs/zh-Hans-full-translation-audit-0.19/summary.md
```

Summary:

```text
entries reviewed: 7937
blocked-public-rc: 1034
simulated-accepted: 1772
simulated-accepted-with-note: 5131
needs-copy-review: 0
needs-functional-review: 0
json validation: passed
```

The audit has no actionable copy or functional rows. The
`blocked-public-rc` rows remain tied to the public-RC evidence workflow.

## Gate Status

Passed in this adaptation cycle:

```text
privacy guard
manifest validation
glossary check
metadata summary
dry-run summary
release inventory coverage
full translation audit
public-RC blocker summary
public-RC evidence report JSON generation
public-RC evidence queue JSON generation
Python compile
Python localization/public-RC/full-audit tests: 66 tests OK
cargo fmt --check
git diff --check
```

Additional reviewer evidence:

```text
cargo check -q: passed during Task 7 review after the 0.19 translation update
```

Deferred in this cycle:

```text
low-load gate: defer-heavy-gate
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp: not rerun after low-load defer
script/run --dont-open: deferred
fresh bundle refresh: deferred
GUI launch: deferred
```

Low-load defer reasons recorded in the adaptation log:

```text
load average exceeds 2.50
hot process Codex (Renderer)
hot process syspolicyd
hot process WindowServer
hot process codex
```

## Public-RC Blocker Registry

```text
total: 11
public_rc_required: 11
blocked-no-backend-fixture: 5
blocked-no-disposable-object: 3
blocked-no-isolated-account: 3
```

Blocked rows:

```text
GUI-AUTH-01
GUI-BILL-01
GUI-BILL-02
GUI-CLOUD-01
GUI-SET-03
GUI-SET-04
GUI-SET-05
GUI-SET-06
GUI-WS-04
GUI-WS-06
GUI-WS-07
```

Strict evidence lint is expected to fail until all 11 rows have matching,
redacted, current-cycle artifacts.

## Release Decision

```text
source-localization candidate: ready for continued engineering verification
heavy build gate: deferred
bundle refresh: deferred
GUI evidence: deferred and requires explicit approval
public RC: not ready
publication/tagging: not approved and not performed
```

RC39 should be treated as the 0.19 source-localization adaptation record, not as
a public release record.
