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
manifest drift repair: passed
dry-run repaired: entries=7899 files=550 already_applied=0 would_change=5682 missing=0
release inventory smoke: covered=8494 candidates=83 coverage=99.0%
overlay apply: not run
inventory coverage: full Task 7 not run
full audit: not run
privacy guard: not run
low-load gate: not run
cargo check: not run
bundle refresh: not run
GUI launch: not run
public RC: not ready
```

## Manifest Drift Repair

Task 5 repaired all strict manifest drift before applying the overlay.

```text
initial missing: 69
final missing: 0
entries before: 7943
entries after: 7899
files before: 552
files after: 550
would_change after repair: 5682
```

Classification summary:

- Path-only moves: 23 entries, primarily execution profile copy moved from `app/src/ai/execution_profiles/mod.rs` and related settings surfaces into `crates/cloud_object_models/src/ai_execution_profile.rs`, remote codebase index errors moved into `app/src/remote_server/server_model.rs`, and the local Codex child-agent disabled copy moved into `app/src/ai/local_harness_setup.rs`.
- Source text drift: 1 search-keyword entry in `app/src/settings_view/ai_page.rs` was expanded for the new queue/interruption/default response settings.
- Occurrence drift: `Settings` in `app/src/workspace/view.rs` now has three expected occurrences; `Unknown setting.` in `crates/cloud_object_models/src/ai_execution_profile.rs` now has two expected occurrences.
- Removed stale overlay entries: 68 old entries were removed where the upstream source file or string no longer exists in the 0.19 stable tree. These were stale auth persistence internals, test fixtures, artifact IDs, SSH hostnames, CLI-agent notification fixtures, diagnostic logs, deleted workspace/menu copy, and deleted queued-prompt/auth-secret strings.
- Ignore additions: 4 moved auth-crate exact paths and 21 reviewed literal patterns were added for internal storage/auth details, fixtures, fake IDs, hostnames, and Claude mailbox protocol snippets that should not become user-visible translation candidates.

Task 5 did not apply the overlay and did not edit upstream Rust source files. The release inventory command was run only as a parser smoke check after ignore changes; full inventory review remains Task 7.
