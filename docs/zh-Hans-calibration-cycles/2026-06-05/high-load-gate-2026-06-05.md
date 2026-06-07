# High-Load Gate 2026-06-05

This report records the user-approved high-load window request for Task 7, Task
8, Task 9, and Rust/Cargo/runtime/GUI checks. The gate was run before any
high-load command.

## Command

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
```

## Result

```text
probe 1: load=2.88 2.77 3.19
probe 1: hot_process=WindowServer 35.4%
probe 2: load=2.75 2.75 3.15
probe 2: hot_process=WindowServer 38.7%
probe 2: hot_process=Codex (Service) 34.5%
decision: defer-heavy-gate
reason: probe 1: load average exceeds 2.50
reason: probe 1: hot process WindowServer at 35.4%
reason: probe 2: load average exceeds 2.50
reason: probe 2: hot process WindowServer at 38.7%
reason: probe 2: hot process Codex (Service) at 34.5%
```

## High-Load Checks Not Run

The following checks were not run because the gate returned
`defer-heavy-gate`:

- `cargo fmt --check`
- `CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp`
- `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open`
- `open -n target/debug/bundle/osx/WarpOss.app`
- GUI automation.
- Runtime log probes.

## Decision

High-load Rust/Cargo/runtime/GUI readiness remains `not-evaluated`. This is a
machine-state block, not a localization pass.
