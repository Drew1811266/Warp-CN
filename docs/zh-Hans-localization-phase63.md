# zh-Hans Localization Phase 63

Date: 2026-06-02 Asia/Shanghai

## Goal

Classify the post-RC13 low-count localization residue before translating more
strings.

The residue is now more contract-heavy than earlier phases, so Phase 63 keeps
source and manifest files unchanged and creates the execution queue for Phase
64-70.

## Low-Load Inventory

Ran serially with `nice -n 10`:

```text
python3 script/zh_localization_inventory.py --preset release --status candidate --top-paths 25
python3 script/zh_localization_inventory.py --preset modals --status candidate --top-paths 25
python3 script/zh_localization_inventory.py app/src/terminal --status candidate --top-paths 30
python3 script/zh_localization_inventory.py app/src/ai --status candidate --top-paths 30
```

No GUI, account, backend, static image, or destructive state was touched.

## Current Queue

Release and modal top paths are identical after RC13. The largest remaining
source candidates are low-count: the release/modal top files have at most `6`
candidates each, terminal top files have at most `6`, and AI/Agent top files
have at most `4`.

## Classification

| Scope | Path cluster | Classification | Next phase |
| --- | --- | --- | --- |
| Terminal | Windows pipe errors, WSL registry errors, session shell descriptions, recorder open action | user-facing errors/settings where safe; OS and library literals preserve-first | Phase 64 |
| Terminal | Block grid, block model, interaction mode, session command executor | mostly log/debug/model contracts; only inspect for visible labels | Phase 64 with preserve-first bias |
| Terminal | Drive sharing onboarding, Warpify success, model selector, host selector, harness selector, shared-session inactivity modal, plugin instructions, init environment | visible UI/onboarding/modal copy | Phase 64 |
| Terminal | CLI plugin manager Codex/opencode instructions | mixed visible setup instructions and literal config snippets | Phase 64; preserve config snippets |
| Terminal | Ref tests, bootstrap file, terminal server protocol, iTerm image model | fixture/protocol/bootstrap/image contracts | Preserve-first |
| AI/Agent | Notifications item/view, TODO popup, pending prompt block, TODO view, header labels | visible UI labels | Phase 65 |
| AI/Agent | Admin login, ambient agent errors, provider status, artifact upload, MCP tool call errors, requested script view | user-facing errors/status where safe | Phase 65 |
| AI/Agent | Summarization cancel dialog, orchestration config block, suggestion chips, plan/todo prompt banner, permissions prompts | visible UI/dialog/action copy | Phase 65 |
| AI/Agent | Request-file-edits, upload artifact, call MCP tool, get relevant files | mixed rendered tool/action errors and contract strings | Phase 65; preserve schemas/tool names |
| AI/Agent | Conversation conversion, config file parsing, provider setup, response stream retry, skill file watcher utilities | parser/config/provider/file-watcher contracts | Preserve-first unless source inspection proves visible UI |
| Public RC | Account, billing, quota, cloud, team, secret, custom endpoint evidence | external-state blockers | Phase 67 |
| Static assets | Onboarding PNGs with embedded English UI/text | binary visual residue | Phase 68 |

## Phase 64 Scope

Confirmed terminal source queue:

- `app/src/terminal/local_tty/windows/pipes.rs`
- `app/src/terminal/model/blockgrid.rs`
- `app/src/terminal/model/blocks.rs`
- `app/src/terminal/recorder.rs`
- `app/src/terminal/session_settings/new_session_shell.rs`
- `app/src/terminal/view/block_onboarding/onboarding_drive_sharing_block.rs`
- `app/src/terminal/warpify/success_block.rs`
- `app/src/terminal/wsl/model.rs`
- `app/src/terminal/cli_agent_sessions/plugin_manager/codex.rs`
- `app/src/terminal/cli_agent_sessions/plugin_manager/opencode.rs`
- `app/src/terminal/input/models/view.rs`
- `app/src/terminal/input/rewind/search_item.rs`
- `app/src/terminal/model/block/interaction_mode.rs`
- `app/src/terminal/model/session/command_executor.rs`
- `app/src/terminal/package_installers.rs`
- `app/src/terminal/view/ambient_agent/harness_selector.rs`
- `app/src/terminal/view/ambient_agent/host_selector.rs`
- `app/src/terminal/view/ambient_agent/model_selector.rs`
- `app/src/terminal/view/ambient_agent/view_impl.rs`
- `app/src/terminal/view/init_environment/mod.rs`
- `app/src/terminal/view/plugin_instructions_block.rs`
- `app/src/terminal/view/shared_session/sharer/inactivity_modal.rs`
- `app/src/terminal/find/model.rs`
- `app/src/terminal/history.rs`
- `app/src/terminal/local_tty/docker_sandbox.rs`
- `app/src/terminal/rich_history.rs`

Preserve-first terminal files:

- `app/src/terminal/ref_tests/mod.rs`
- `app/src/terminal/writeable_pty/bootstrap_file/windows.rs`
- `app/src/terminal/local_tty/server/protocol.rs`
- `app/src/terminal/model/iterm_image.rs`

## Phase 65 Scope

Confirmed AI/Agent source queue:

- `app/src/ai/agent_management/notifications/view.rs`
- `app/src/ai/agent_management/notifications/item.rs`
- `app/src/ai/agent_sdk/admin.rs`
- `app/src/ai/ambient_agents/spawn.rs`
- `app/src/ai/ambient_agents/mod.rs`
- `app/src/ai/blocklist/action_model/execute/request_file_edits.rs`
- `app/src/ai/blocklist/action_model/execute/call_mcp_tool.rs`
- `app/src/ai/blocklist/action_model/execute/upload_artifact.rs`
- `app/src/ai/blocklist/block/cli_controller.rs`
- `app/src/ai/blocklist/block/view_impl/todos.rs`
- `app/src/ai/blocklist/block/model/model_impl.rs`
- `app/src/ai/blocklist/block/pending_user_query_block.rs`
- `app/src/ai/blocklist/block/view_impl/header.rs`
- `app/src/ai/blocklist/controller/input_context.rs`
- `app/src/ai/blocklist/handoff/touched_repos.rs`
- `app/src/ai/blocklist/suggestion_chip_view.rs`
- `app/src/ai/blocklist/summarization_cancel_dialog.rs`
- `app/src/ai/blocklist/inline_action/requested_script.rs`
- `app/src/ai/blocklist/passive_suggestions/legacy.rs`
- `app/src/ai/blocklist/permissions.rs`
- `app/src/ai/blocklist/prompt/plan_and_todo_list.rs`
- `app/src/ai/document/orchestration_config_block.rs`
- `app/src/ai/get_relevant_files/controller.rs`
- `app/src/ai/agent/todos/popup.rs`

Preserve-first AI/Agent files:

- `app/src/ai/agent/api/convert_conversation.rs`
- `app/src/ai/agent/api/convert_from.rs`
- `app/src/ai/agent_sdk/config_file.rs`
- `app/src/ai/agent_sdk/provider.rs`
- `app/src/ai/blocklist/controller/response_stream.rs`
- `app/src/ai/skills/file_watchers/utils.rs`

## Review

Phase 63 is qualified because it confirms the Phase 64 and Phase 65 scopes from
current inventories, keeps preserve-first candidates explicit, and makes no
source, manifest, GUI, account, backend, or binary asset changes.

Qualification: `qualified-post-rc13-residue-classification`.
