# zh-Hans Heat-Safe Validation

Date: 2026-06-02

## Purpose

Use `script/zh_low_load_gate.py` before heavy Warp CN validation commands.

## Default Gate

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
```

Run heavy commands only when the script prints:

```text
decision: run-heavy-gate
```

When it prints `decision: defer-heavy-gate`, record the reasons in the current
phase document and skip Rust compile, bundle build, and GUI launch for that
phase.

## Heavy Commands

```bash
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
open -n target/debug/bundle/osx/WarpOss.app
```

## Safety Rules

- Run heavy commands serially.
- Do not retry repeatedly in the same phase after a defer decision.
- Do not use GUI launch as public-RC evidence unless the current phase produced a fresh bundle.
- Never touch accounts, billing, cloud objects, secrets, endpoints, or team ownership during heat-gate checks.
