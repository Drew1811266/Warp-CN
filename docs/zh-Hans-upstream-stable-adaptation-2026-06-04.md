# zh-Hans 0.19 Upstream Stable Adaptation

Date: 2026-06-04

## Baseline

| Item | Value |
| --- | --- |
| Previous fork release | `0.18 / RC38` |
| Previous stable source baseline | `origin/stable_release/v0.2026.05.27.09.22.stable` |
| New upstream stable tag | `v0.2026.06.03.09.49.stable_00` |
| New upstream stable commit | `2249469e5d24e472cee6ce97d3d324293f67db71` |
| New upstream stable tree | `efe8ae7822765eb267792d441e4b1e7ddb7f8e53` |
| Adaptation branch | `codex/zh-Hans-0.19-upstream-stable-adaptation` |
| Adaptation worktree | `/Users/drew/Project/warp-cn-0.19-adaptation` |

## Upstream Diff Scope

```text
952 files changed, 47307 insertions(+), 19826 deletions(-)
changed_app_src=439
changed_crates=460
changed_resources=8
changed_script=8
changed_github=2
changed_specs=16
manifest_active_entries=7943
manifest_files=552
changed_manifest_files=170
entries_on_changed_files=4616
```

## Initial Decision

The adaptation uses a clean upstream-stable worktree plus imported durable Warp CN localization assets. Chinese source files are regenerated from the manifest instead of merged as the durable source of truth.

## Gate Status

```text
manifest validation: passed
glossary check: passed
metadata summary: passed
dry-run initial: entries=7943 files=552 already_applied=0 would_change=5658 missing=69
overlay apply: not run
inventory coverage: not run
full audit: not run
privacy guard: not run
low-load gate: not run
cargo check: not run
bundle refresh: not run
GUI launch: not run
public RC: not ready
```
