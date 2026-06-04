# zh-Hans Release Candidate 2026-06-02 RC29

Date: 2026-06-02

## Scope

RC29 covers Phases 200 through 211. It settles the post-RC28 upstream retarget
question, records tree parity with the current remote stable tag target, keeps
the current evidence branch intact, rechecks public-RC and PNG blockers, and
freezes the next local-use decision under the active heat-safety constraint.

RC29 does not add manifest translations, change PNG assets, produce GUI
evidence, build a bundle, log in, create backend fixtures, touch billing/cloud
state, create or delete managed secrets/endpoints, mutate team state, mutate
Git refs, stage, commit, push, merge, or rebase.

The RC29 delta is:

```text
RC28 evidence branch kept as the active local evidence branch
remote stable retarget audited non-destructively
local and remote stable commits confirmed to share the same source tree
upstream-sync branch creation deferred because no source-tree drift exists
overlay repair skipped because dry-run remains clean
tag namespace policy recorded without destructive tag mutation
fresh bundle skipped under heat-safety rules
no-account GUI smoke skipped because no fresh bundle exists
public-RC blocker registry refreshed and still blocked
PNG asset branch deferred because no design/product approval exists
RC29 readiness freeze
```

## Manifest And Coverage

Manifest and source coverage remain inherited from RC28 because RC29 did not add
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

## Upstream Stable Retarget

Phase 201 compared the local cached stable tag target with the current remote
stable tag target:

```text
tag: v0.2026.05.27.09.22.stable_00
local tag commit: 7ed8bbd5dbf701c453ce90a6961f4e6dbcc8d6b4
remote tag commit: 2566f54af7c3e71facfe1865f2c492549b14248a
local tree ID: 2281e0a3e27c328bb6bb6f3af82f2d6050780ea7
remote tree ID: 2281e0a3e27c328bb6bb6f3af82f2d6050780ea7
source-tree drift: none
remote commit ancestry contained in current HEAD: no
```

Decision:

```text
strategy: tree-parity-adoption
source overlay repair needed: no
upstream-sync source-drift branch needed: no
destructive tag operation: not run
allowed wording: source-tree equivalent to the current remote stable target
disallowed wording: current branch contains the remote stable commit
```

## Bundle And GUI Status

Phase 207 ran two probes with a 60-second cooling interval. No thermal warning
was recorded, but the machine was not quiet enough for a conservative bundle
retry.

```text
probe 1 load: 2.32 2.69 2.66
probe 1 top CPU: WindowServer 44.6%, Codex 23.2%, Finder 17.8%
probe 2 load: 2.30 2.65 2.65
probe 2 top CPU: syspolicyd 53.1%, WindowServer 42.0%, Codex Service 16.8%, Finder 16.7%
bundle build: skipped-with-heat-safety
```

Phase 208 did not launch GUI because no fresh current-cycle bundle existed.

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

No blocker was cleared in RC29.

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

Skipped for heat-safety after a final load probe:

```text
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
open -n target/debug/bundle/osx/WarpOss.app
```

Final load probe before heavy gates:

```text
load averages: 5.51 3.31 2.88
top CPU: Codex 61.7%, deleted 52.8%, node 36.1%, syspolicyd 35.9%, WindowServer 34.5%, npm/playwright MCP 34.3%, mds 28.9%
```

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
upstream source-tree follow-up required: no
upstream ancestry/commit-identity follow-up required for public wording: yes
```

RC29 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until fresh bundle/current-cycle GUI evidence
exists, all 11 public-RC blockers are cleared with real matching evidence,
onboarding PNG visual status is approved or regenerated, and any public wording
about upstream stable ancestry is backed by an approved upstream-sync branch or
explicit commit/tree evidence.
