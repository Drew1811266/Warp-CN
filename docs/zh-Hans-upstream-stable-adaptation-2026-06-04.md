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
overlay apply: passed
overlay idempotent: entries=7899 files=550 already_applied=5681 would_change=0 missing=0
cargo fmt: passed
inventory coverage: passed; release covered=8534 candidates=0 coverage=100.0%
translation update idempotent: entries=7937 files=550 already_applied=5717 would_change=0 missing=0
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

## Overlay Application

Task 6 applied the repaired manifest to the 0.19 stable source tree and formatted the Rust workspace.

```text
applied replacements: 5681
dry-run after apply: entries=7899 files=550 already_applied=5681 would_change=0 missing=0
cargo fmt: passed
```

During formatting, `cargo fmt` exposed invalid Rust generated for ordinary string literals whose localized targets contain embedded double quotes. The overlay tool now escapes replacement text when writing normal Rust strings, and `script/test_zh_apply_localization.py` covers the idempotent quote-preserving case. This was required for the CLI install AppleScript prompts and the Command Search sample query `# 在文件中查找 "foo"` to remain valid Rust while still matching the manifest on dry-run.

The `User canceled` osascript stderr token remains in English because it is a control-flow sentinel used to detect administrator prompt cancellation. The returned cancellation errors remain localized.

## 0.19 Candidate Translation Update

Task 7 reviewed the release inventory candidates after applying the baseline overlay.

```text
onboarding coverage: covered=314 candidates=0 coverage=100.0%
workspace coverage: covered=874 candidates=0 coverage=100.0%
search coverage: covered=267 candidates=0 coverage=100.0%
settings coverage: covered=2040 candidates=0 coverage=100.0%
modals coverage: covered=5177 candidates=0 coverage=100.0%
release coverage before Task 7 edits: covered=8494 candidates=83 coverage=99.0%
release coverage after Task 7 edits: covered=8534 candidates=0 coverage=100.0%
dry-run after Task 7 edits: entries=7937 files=550 already_applied=5717 would_change=0 missing=0
```

Task 7 added 36 reviewed manifest entries and narrow ignore rules for internal-only 0.19 strings. User-visible updates covered vertical tab group menus, queued prompt actions, AI prompt submission settings, staging IAP credential status, shared-session metadata access, Claude Code platform plugin user errors, and duplicate child-agent guidance. Internal logs, protocol IDs, config keys, position IDs, test assertions, and orchestration viewer diagnostics were ignored with literal patterns instead of translated.

See `docs/zh-Hans-translation-audit-0.19.md` for the Task 7 summary.
