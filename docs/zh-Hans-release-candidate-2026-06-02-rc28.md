# zh-Hans Release Candidate 2026-06-02 RC28

Date: 2026-06-02

## Scope

RC28 covers Phases 187 through 199. It settles the RC27 branch state, reruns
low-load validation, rechecks fresh bundle and no-account GUI prerequisites,
keeps external public-RC lanes safely blocked, reviews Agent render evidence,
rechecks onboarding PNG authorization, performs a non-destructive upstream tag
conflict audit, and freezes the next readiness decision.

RC28 does not add manifest translations, change PNG assets, produce GUI
evidence, build a bundle, log in, create backend fixtures, touch billing/cloud
state, create or delete managed secrets/endpoints, mutate team state, or mutate
Git refs.

The RC28 delta is:

```text
RC27 branch state settled without stage/commit/push/merge
fresh bundle skipped under heat-safety rules
no-account GUI smoke skipped because no fresh bundle exists
isolated-account prerequisites and execution blocked
backend-fixture contract hardened; execution blocked
disposable-object prerequisites and execution blocked
Agent lifecycle render evidence remains needs-trigger
onboarding PNG asset lane remains blocked-no-asset-approval
upstream v0.2026.* tag conflicts audited non-destructively
remote stable tag retarget conflict identified
RC28 readiness freeze
```

## Manifest And Coverage

Manifest and source coverage remain inherited from RC27 because RC28 did not add
translation entries.

```text
manifest entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
release: covered 8574, candidates 2, coverage 100.0%
```

Remaining source candidates are still intentional preserved terms:

```text
app/src/ai/blocklist/usage/rollup.rs: Agent
app/src/terminal/view/ambient_agent/block/harness_session_header.rs: Agent
```

## Bundle And GUI Status

Phase 188 ran two probes with a 60-second cooling interval. No thermal warning
was recorded, but load and desktop process activity stayed high.

```text
probe 1 load: 3.71 3.27 3.16
probe 1 top CPU: WindowServer 42.6%, Finder 17.0%, Codex Service 15.5%
probe 2 load: 3.12 3.17 3.13
probe 2 top CPU: WindowServer 43.7%, Codex Service 18.5%, Finder 17.5%
bundle build: skipped-with-heat-safety
```

Phase 189 did not launch GUI because no fresh current-cycle bundle existed.

```text
historical bundle: target/debug/bundle/osx/WarpOss.app
historical bundle mtime: 2026-06-01 21:53:26 CST
no-account GUI smoke: skipped-no-fresh-bundle
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

No blocker was cleared in RC28.

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

## External-State Lane Decisions

```text
isolated account package: blocked-no-isolated-account
isolated account execution: blocked-no-isolated-account
backend fixture package: blocked-no-backend-fixture
backend fixture execution: blocked-no-backend-fixture
disposable object package: blocked-no-disposable-object
disposable object execution: blocked-no-disposable-object
```

No account, backend, billing, cloud, managed secret, custom endpoint,
disposable object, or team state was read or mutated.

## Agent And PNG Status

Agent lifecycle:

```text
source harness: retained
labels present: 排队中, 等待中, 已分配, 进行中, 已完成, 失败, 错误, 已阻塞, 已取消
rendered GUI evidence: absent
GUI-AGENT-03: needs-trigger
```

Onboarding PNG assets:

```text
onboarding PNG total: 54
current branch PNG changes: none
deferred asset count: 50
accepted decorative/brand asset count: 4
asset branch: codex/zh-Hans-onboarding-assets-rc20
decision: blocked-no-asset-approval
```

## Upstream Tag Conflict

Phase 198 performed a non-destructive local/remote tag audit.

```text
local tag count: 51
remote v0.2026 tag count: 44
local-only tags: 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, repo-sync/watermark/private-to-public
same-name v0.2026 peeled conflicts: 41
force update tags: not run
delete local tags: not run
merge/rebase: not run
```

Latest stable conflict:

```text
tag: v0.2026.05.27.09.22.stable_00
local tag commit: 7ed8bbd5dbf701c453ce90a6961f4e6dbcc8d6b4
remote tag commit: 2566f54af7c3e71facfe1865f2c492549b14248a
remote latest stable commit is ancestor of current HEAD: no
```

This blocks any public-RC claim that the current branch follows the current
remote stable tag target. A separate upstream-sync plan is required before
adopting the remote retargeted stable commit.

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
low-concurrency Rust compile: CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
```

Final summary:

```text
manifest entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
release coverage: 8574 covered, 2 candidates, 100.0%
public-RC blockers: 11
Rust compile result: passed in 0.65s incremental check
Rust warnings: 46 existing unused-variable warnings
```

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
upstream-sync follow-up required: yes
```

RC28 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until fresh bundle/current-cycle GUI evidence
exists, all 11 public-RC blockers are cleared with real matching evidence,
onboarding PNG visual status is approved or regenerated, and the remote stable
tag retarget conflict is resolved through a separate upstream-sync plan.
