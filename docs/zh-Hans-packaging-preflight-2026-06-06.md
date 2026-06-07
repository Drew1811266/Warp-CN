# zh-Hans Packaging Preflight - 2026-06-06

## Supersession

2026-06-07 policy update: the user cancelled the low-load development constraint. This
document remains a historical record of the 2026-06-06 preflight. Future `cargo check`,
local launch, bundle, and GUI smoke validation should run directly and record results
without using `zh_low_load_gate.py` as a prerequisite.

## Scope

Warp CN 0.19 self-defined complete release packaging preflight.

## Commands

```text
python3 script/privacy_guard.py --all-tracked
git diff --check
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
```

## Result

```text
privacy_guard: pass
diff_check: pass
low_load_gate: defer-heavy-gate
cargo_check: skipped
```

Low-load gate output:

```text
probe 1: load=2.50 2.43 2.33
probe 1: hot_process=WindowServer 32.4%
probe 1: hot_process=Codex (Renderer) 31.2%
probe 2: load=2.45 2.42 2.33
probe 2: hot_process=WindowServer 37.9%
probe 2: hot_process=Codex (Renderer) 26.9%
decision: defer-heavy-gate
reason: probe 1: hot process WindowServer at 32.4%
reason: probe 1: hot process Codex (Renderer) at 31.2%
reason: probe 2: hot process WindowServer at 37.9%
reason: probe 2: hot process Codex (Renderer) at 26.9%
```

## Notes

Rust check was skipped because low-load gate returned `defer-heavy-gate`.
This skip reason no longer applies after the 2026-06-07 policy update.
