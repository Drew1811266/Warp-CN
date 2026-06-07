# zh-Hans Packaging Preflight - 2026-06-07

## Scope

Warp CN 0.19 self-defined complete release packaging preflight after the low-load development constraint was cancelled.

## Commands

```text
python3 script/privacy_guard.py --all-tracked
git diff --check
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

## Result

```text
privacy_guard: pass
diff_check: pass
cargo_check: pass
bundle_or_launch: pass
```

## Notes

- Low-load gate is not required for this run after the 2026-06-07 policy update.
- `CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp` exited 0 and finished with `Finished 'dev' profile [unoptimized + debuginfo]`.
- `TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open` exited 0 after bundling `target/debug/bundle/osx/WarpOss.app` and running the packaging preparation steps.
- This preflight did not open the GUI; current-cycle GUI launch smoke remains tracked separately in `docs/zh-Hans-gui-smoke-artifact-index-0.19.md`.
- Both heavy commands emitted existing `unused variable` warnings in Rust sources but did not fail the run.
