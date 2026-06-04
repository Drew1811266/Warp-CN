# zh-Hans Localization Phase 222

Date: 2026-06-02

## Scope

Phase 222 documents the repeatable heat-safe validation gate added in Phase
221.

This phase does not stage, commit, push, merge, rebase, create a worktree,
mutate tags, build a bundle, launch GUI, use accounts, create backend fixtures,
touch billing/cloud state, or modify PNG assets.

## Updated Documentation

```text
docs/zh-Hans-heat-safe-validation.md
README.md
```

README now instructs maintainers to run:

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
```

and to continue with Rust compile, bundle, and GUI only when the helper prints:

```text
decision: run-heavy-gate
```

## Decision

```text
decision: heat-safe-validation-doc-added
doc: docs/zh-Hans-heat-safe-validation.md
README updated: yes
```

## Qualification Review

```text
phase: 222
status: qualified-heat-safe-docs
docs updated: yes
heavy local command avoided: yes
external state untouched: yes
safe to continue to Phase 223: yes
```
