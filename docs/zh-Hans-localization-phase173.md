# zh-Hans Localization Phase 173

Date: 2026-06-02

## Scope

Phase 173 refreshed the static onboarding PNG asset gate. It only checked file
counts, worktree status, and the existing visual regeneration plan. It did not
generate or edit PNGs, launch GUI, compile Rust, build a bundle, log in, call
backend APIs, read credentials, create billing or cloud state, create managed
secrets/endpoints, or mutate team state.

## PNG Status

```text
git status --short -- '*.png'
result: no output

git diff --name-only -- '*.png'
result: no output
```

## Onboarding PNG Inventory

```text
find app/assets/async/png/onboarding -name '*.png' -maxdepth 4 | sort | wc -l
54

find app/assets/async/png/onboarding -maxdepth 1 -name '*.png' | wc -l
12

find app/assets/async/png/onboarding/agent_intention -maxdepth 1 -name '*.png' | wc -l
16

find app/assets/async/png/onboarding/terminal_intention -maxdepth 1 -name '*.png' | wc -l
10

find app/assets/async/png/onboarding/agent_intention/theme -maxdepth 1 -name '*.png' | wc -l
8

find app/assets/async/png/onboarding/terminal_intention/theme -maxdepth 1 -name '*.png' | wc -l
8
```

## Regeneration Plan Check

```text
test -f docs/zh-Hans-onboarding-visual-regeneration-plan.md
result: passed
```

## Matrix Update

```text
docs/zh-Hans-gui-smoke-matrix.md
added: Phase 173 static onboarding PNG asset gate
rows promoted: none
```

## Decision

```text
Phase 173 decision: qualified-static-png-assets-deferred
PNG generation approved: no
continue automatically: yes
```

Phase 173 is qualified. Static onboarding screenshot assets remain visual
residue and must stay deferred until an approved reversible asset-only
regeneration branch exists.

## Qualification Review

```text
phase: 173
status: qualified-asset-gate
PNG worktree changes: none
PNG diff changes: none
onboarding PNG total: 54
visual regeneration plan present: yes
PNG generated: no
PNG edited: no
GUI rows promoted: none
external operations run: none
heavy operations run: none
```
