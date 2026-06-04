# zh-Hans Localization Phase 206

Date: 2026-06-02

## Scope

Phase 206 defines tag namespace policy after the RC28 upstream retarget audit
and Phase 201 tree-parity finding.

This phase did not delete tags, force-fetch tags, rewrite refs, switch branches,
merge, rebase, stage, commit, push, build a bundle, launch GUI, or mutate
external state.

## Policy

```text
fork release tags: 0.1 through 0.15 are fork-owned release labels
local v0.2026.* tags: cached upstream labels, not automatically current remote truth
remote truth check: use git ls-remote --tags origin ... or explicit commit/tree IDs
tree parity wording: allowed when tree IDs match
ancestry containment wording: not allowed unless remote stable commit is ancestor of HEAD
destructive tag operations: require explicit user approval
```

Updated:

```text
docs/zh-Hans-upstream-sync.md
```

## Decision

```text
decision: keep-local-tags-and-use-explicit-remote-commit-tree-ids
delete/refetch same-name upstream tags: not run
mirror namespace: not created in this phase
```

## Qualification Review

```text
phase: 206
status: qualified-tag-namespace-policy
fork tag ownership recorded: yes
remote truth lookup rule recorded: yes
destructive tag operation avoided: yes
safe to continue to Phase 207: yes
```
