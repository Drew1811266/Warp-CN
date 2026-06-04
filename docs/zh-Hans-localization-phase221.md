# zh-Hans Localization Phase 221

Date: 2026-06-02

## Scope

Phase 221 adds a repeatable low-load gate helper for future Rust, bundle, and
GUI phases.

This phase does not stage, commit, push, merge, rebase, create a worktree,
mutate tags, build a bundle, launch GUI, use accounts, create backend fixtures,
touch billing/cloud state, or modify PNG assets.

## Added Files

```text
script/zh_low_load_gate.py
script/test_zh_low_load_gate.py
```

The helper parses `uptime`, checks `pmset -g therm`, watches sustained desktop
or helper CPU pressure, and returns:

```text
0: decision: run-heavy-gate
2: decision: defer-heavy-gate
```

## Test Evidence

Initial red test:

```text
python3 -m unittest script/test_zh_low_load_gate.py
result: failed with ModuleNotFoundError for zh_low_load_gate
```

Final green test:

```text
python3 -m unittest script/test_zh_low_load_gate.py
result: Ran 6 tests, OK
```

No-wait smoke probe:

```text
python3 script/zh_low_load_gate.py --probes 1 --wait-seconds 0
probe 1: load=2.02 2.76 2.89
decision: defer-heavy-gate
reason: probe 1: load average exceeds 2.50
exit_code: 2
```

The smoke probe deferred heavy work because current 5/15 minute load stayed
above the configured threshold. No heavy command was run.

## Decision

```text
decision: low-load-gate-helper-added
script: script/zh_low_load_gate.py
tests: script/test_zh_low_load_gate.py
current heavy-gate state: defer-heavy-gate
```

## Qualification Review

```text
phase: 221
status: qualified-low-load-gate-helper
tests passed: yes
smoke probe captured: yes
heavy local command avoided: yes
external state untouched: yes
safe to continue to Phase 222: yes
```
