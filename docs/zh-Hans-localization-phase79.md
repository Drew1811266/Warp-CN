# zh-Hans Localization Phase 79

Date: 2026-06-02 Asia/Shanghai.

## Goal

Phase 79 continues from RC15 by classifying post-RC15 high-risk English residue
before translating more UI strings. The phase updates preserve/ignore policy
only for reviewed non-UI candidates.

## RC15 Baseline

```text
RC15 decision: ready-for-local-use-with-fixture-evidence
manifest entries: 7843
dry-run: entries 7843, files 492, already_applied 5590, would_change 0, missing 0
release coverage: 8533 covered, 291 candidates, 96.7%
terminal coverage: 2135 covered, 159 candidates, 93.1%
AI / Agent coverage: 2517 covered, 128 candidates, 95.2%
workspace/settings stragglers: 4 candidates
```

## Candidate Snapshots

Entry snapshots matched the post-RC15 plan. The highest release candidates were:

```text
5 app/src/terminal/writeable_pty/bootstrap_file/windows.rs
4 app/src/ai/agent_management/notifications/view.rs
4 app/src/ai/blocklist/block/cli_controller.rs
4 app/src/ai/blocklist/controller/input_context.rs
4 app/src/terminal/wsl/model.rs
3 app/src/ai/agent_sdk/config_file.rs
3 app/src/ai/blocklist/permissions.rs
3 app/src/ai/document/ai_document_model.rs
3 app/src/ai/mcp/templatable.rs
3 app/src/settings_view/mod.rs
3 app/src/terminal/links.rs
3 app/src/terminal/local_tty/spawner.rs
```

After the preserve-policy update:

```text
release: 8519 covered, 258 candidates, 97.1%
terminal: 2121 covered, 140 candidates, 93.8%
AI / Agent: 2517 covered, 114 candidates, 95.7%
workspace/settings: 2809 covered, 4 candidates, 99.9%
```

The lower release covered count is expected because exact-path ignore rules
remove reviewed non-UI residue from both numerator and denominator.

## Classification Table

| Path or literal | Classification | Decision |
| --- | --- | --- |
| `app/src/terminal/cli_agent_sessions/plugin_manager/opencode.rs` | tool-or-command-identifier | Exact-path ignore. Contains npm package descriptors for the OpenCode plugin. |
| `app/src/terminal/command_corrections_denylist.rs` | parser-or-schema-contract | Exact-path ignore. Contains command-correction enum IDs. |
| `app/src/terminal/grid_renderer.rs` | terminal-protocol-contract | Exact-path ignore. Remaining candidates are renderer position-cache IDs. |
| `app/src/terminal/local_tty/server/logging.rs` | log-or-debug-residue | Exact-path ignore. Contains logging thread name and terminal-server log forwarding diagnostics. |
| `app/src/terminal/model/grid/grid_storage/resize.rs` | log-or-debug-residue | Exact-path ignore. Contains grid invariant diagnostics. |
| `app/src/terminal/model/grid/resize.rs` | log-or-debug-residue | Exact-path ignore. Contains cursor/grid invariant diagnostics. |
| `app/src/terminal/model/header_grid.rs` | log-or-debug-residue | Exact-path ignore. Contains resize invariant and PS1 diagnostic text. |
| `app/src/terminal/recorder.rs` | shell-or-bootstrap-contract | Exact-path ignore. Remaining candidates are timestamp and PTY recording filename templates. |
| `app/src/terminal/remote_tty/event_loop.rs` | terminal-protocol-contract | Exact-path ignore. Contains remote endpoint query and env assignment snippets. |
| `app/src/ai/agent/api/convert_to.rs` | parser-or-schema-contract | Exact-path ignore. Contains API conversion and JSON number diagnostics. |
| `app/src/ai/agent_events/message_hydrator.rs` | log-or-debug-residue | Exact-path ignore. Contains Agent message hydration warnings. |
| `app/src/ai/mcp/file_based_manager.rs` | log-or-debug-residue | Exact-path ignore. Contains MCP auto-spawn and scan-complete logs. |
| `app/src/ai/mcp/templatable_manager/wasm.rs` | parser-or-schema-contract | Exact-path ignore. Contains WASM unsupported operation diagnostics. |
| `app/src/ai/predict/next_command_model.rs` | log-or-debug-residue | Exact-path ignore. Contains Next Command parser and validation diagnostics. |
| `AvailableHarnesses` | parser-or-schema-contract | Literal ignore. Stable cache key. |
| `AIRequestLimitInfo` | parser-or-schema-contract | Literal ignore. Stable request-usage cache/state key. |
| `Option<String>` | parser-or-schema-contract | Literal ignore. Config schema type name. |
| `{{{json}}}` | parser-or-schema-contract | Literal ignore. JSON template placeholder. |
| `{UNIQUENESS_KEY_PREFIX}_{}` | parser-or-schema-contract | Literal ignore. Cloud-object uniqueness key template. |

## Deferred To Later Phases

These were reviewed but not hidden in Phase 79 because they may be visible UI or
user-facing errors:

```text
app/src/terminal/writeable_pty/bootstrap_file/windows.rs
app/src/terminal/links.rs
app/src/terminal/local_tty/spawner.rs
app/src/terminal/session_settings/startup_shell.rs
app/src/ai/agent_sdk/config_file.rs
app/src/ai/agent_sdk/driver/harness/codex.rs
app/src/ai/agent_sdk/integration.rs
app/src/ai/agent_sdk/profiles.rs
app/src/ai/blocklist/persistence.rs
app/src/ai/blocklist/usage/rollup.rs
app/src/ai/harness_availability.rs
app/src/ai/local_child_harnesses.rs
app/src/ai/mcp/templatable.rs
```

`Name`, `Agent`, `Orchestrator`, shortcut labels, disabled-harness notices, and
configuration help text were intentionally not added as global ignore patterns.

## Ignore-Policy Changes

Updated `resources/localization/zh-Hans-inventory-ignore.toml` with:

- Phase 79 exact paths for reviewed internal files.
- Phase 79 literal patterns for stable cache/state keys and JSON/template
  placeholders.

No visible labels, buttons, descriptions, toasts, dialogs, or reviewed
user-facing errors were hidden.

## Phase 80 And Phase 81 Queues

Phase 80 should handle remaining Terminal UI/user-facing strings in WSL,
shared-session, banners, input menus, block onboarding, bookmarks, Warpify, and
terminal link/PTY/spawner surfaces.

Phase 81 should handle AI/Agent visible UI in notifications, blocklist action
UI, permissions, document labels, todos, suggestions, model menus, disabled
local child harness notices, and profile/status surfaces. SDK, MCP, provider,
model, schema, and tool identifiers remain preserve-first.

## Acceptance Checks

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
manifest validation passed

nice -n 10 python3 script/zh_apply_localization.py --check-glossary
glossary check passed

nice -n 10 python3 script/zh_localization_inventory.py --preset release --coverage
preset: release
covered: 8519
candidates: 258
coverage: 97.1%

git diff --check
passed
```

## Qualification Result

Qualified.

Phase 79 passed because manifest validation, glossary, release coverage, and
diff checks passed; every ignore addition has a non-UI classification rationale;
and preserved UI or possibly user-facing strings remain queued for Phase 80 or
Phase 81 instead of being hidden.
