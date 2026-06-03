# zh-Hans Upstream Sync Plan RC29

Date: 2026-06-02

## Scope

This plan resolves the RC28 upstream stable retarget finding without destructive
tag operations. It does not delete, force-fetch, rewrite, merge, rebase, or
switch branches.

## Finding

The remote stable tag target and local stable tag target are different commits:

```text
tag: v0.2026.05.27.09.22.stable_00
local commit: 7ed8bbd5dbf701c453ce90a6961f4e6dbcc8d6b4
remote commit: 2566f54af7c3e71facfe1865f2c492549b14248a
remote commit is ancestor of current HEAD: no
```

However, the two commits have the same source tree:

```text
local tree: 2281e0a3e27c328bb6bb6f3af82f2d6050780ea7
remote tree: 2281e0a3e27c328bb6bb6f3af82f2d6050780ea7
diff --stat local..remote: no output
diff --name-status local..remote: no output
```

The retarget conflict is therefore a commit/tag/history identity issue, not a
source tree drift issue.

## Selected Strategy

```text
strategy: tree-parity adoption without destructive tag mutation
upstream source baseline: remote commit 2566f54af7c3e71facfe1865f2c492549b14248a by tree parity
local cached tag target: 7ed8bbd5dbf701c453ce90a6961f4e6dbcc8d6b4
shared tree: 2281e0a3e27c328bb6bb6f3af82f2d6050780ea7
create upstream-sync branch now: no
delete or force-update tags: no
```

Because the source tree is identical, no upstream-sync branch is required for
source drift discovery in this cycle. Future release notes must avoid claiming
that current `HEAD` contains the remote stable commit by ancestry. They may say
that the selected source baseline has tree parity with the current remote stable
target.

## Follow-Up Policy

Before a public RC:

```text
1. Use explicit commit IDs and tree IDs when discussing upstream freshness.
2. Treat fork tags 0.1 through 0.15 as fork-owned release labels.
3. Do not rely on local v0.2026.* tags as current remote truth unless they are
   refreshed or checked with git ls-remote.
4. If exact remote tag ancestry becomes required, create a clean upstream-sync
   branch from 2566f54af7c3e71facfe1865f2c492549b14248a and replay the
   localization overlay there.
5. Any tag deletion or force-fetch requires explicit user approval.
```

## Exit Criteria

```text
tree parity confirmed: yes
source drift from retarget: none
destructive tag operation avoided: yes
separate branch required for this cycle: no
public-RC wording requirement: mention tree parity, not ancestry containment
```
