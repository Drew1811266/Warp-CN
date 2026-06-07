# zh-Hans Functional Risk Findings

This report separates behavior-sensitive strings from copy-only review. Public-RC rows remain evidence-gated.

- Critical token mismatches: 0
- Source-state review rows: 130
- Placeholder and URL risk rows: 1663
- Command and slash command risk rows: 3187
- Search, action, storage, protocol risk rows: 1341
- Public-RC evidence gated rows: 1030

## Critical Token Mismatches

No rows.

## Source State Review

| entry | line | path | source | target | notes |
| ---: | ---: | --- | --- | --- | --- |
| 683 | 4853 | `app/src/search/command_search/zero_state.rs` | # find "foo" in files | # 在文件中查找 "foo" | source state is missing-in-current-source |
| 2538 | 17868 | `app/src/workspace/cli_install.rs` | do shell script "ln -sf {escaped_source} {escaped_target}" with prompt "Warp needs administrator privileges to install the command in /usr/l | do shell script "ln -sf {escaped_source} {escaped_target}" with prompt "Warp 需要管理员权限才能将命令安装到 /usr/local/bin。" with administrator privileges | source state is missing-in-current-source |
| 2539 | 17875 | `app/src/workspace/cli_install.rs` | do shell script "rm {escaped_target}" with prompt "Warp needs administrator privileges to uninstall the command from /usr/local/bin." with a | do shell script "rm {escaped_target}" with prompt "Warp 需要管理员权限才能从 /usr/local/bin 卸载该命令。" with administrator privileges | source state is missing-in-current-source |
| 3310 | 23109 | `app/src/ai/agent/mod.rs` | n**Command Executed:**n```bashn{command}n```nn**Output:**n```n{output}n``` | n**Command Executed:**n```bashn{command}n```nn**Output:**n```n{output}n``` | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3311 | 23116 | `app/src/ai/agent/mod.rs` | n```bashn{command}n```nn**Current Output:**n```n{grid_contents}n``` | n```bashn{command}n```nn**Current Output:**n```n{grid_contents}n``` | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3314 | 23137 | `app/src/ai/agent/mod.rs` | n```n{output}n``` | n```n{output}n``` | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3315 | 23144 | `app/src/ai/agent/mod.rs` | n```n{grid_contents}n``` | n```n{grid_contents}n``` | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3317 | 23158 | `app/src/ai/agent/mod.rs` | nn**Diff:**n```diffn{diff}n```nn | nn**Diff:**n```diffn{diff}n```nn | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3320 | 23179 | `app/src/ai/agent/mod.rs` | nn**Files Read:**nn | nn**Files Read:**nn | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3321 | 23186 | `app/src/ai/agent/mod.rs` | ```n{text}n```n | ```n{text}n```n | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3325 | 23214 | `app/src/ai/agent/mod.rs` | nn**File:** `{filepath}` | nn**File:** `{filepath}` | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3326 | 23221 | `app/src/ai/agent/mod.rs` | nn**MIME Type:** `{mime_type}`nn**Size:** `{size_bytes}` bytes | nn**MIME Type:** `{mime_type}`nn**Size:** `{size_bytes}` bytes | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3327 | 23228 | `app/src/ai/agent/mod.rs` | nn**Description:** {description} | nn**Description:** {description} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3330 | 23249 | `app/src/ai/agent/mod.rs` | nn**Codebase Search Results:**nn | nn**Codebase Search Results:**nn | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3333 | 23270 | `app/src/ai/agent/mod.rs` | nn**File Glob Results:**nn | nn**File Glob Results:**nn | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3336 | 23291 | `app/src/ai/agent/mod.rs` | nn**Grep Results:**nn | nn**Grep Results:**nn | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3339 | 23312 | `app/src/ai/agent/mod.rs` | nn**Documents Read:**nn | nn**Documents Read:**nn | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3341 | 23326 | `app/src/ai/agent/mod.rs` | ```n{}n```n | ```n{}n```n | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3344 | 23347 | `app/src/ai/agent/mod.rs` | nn**Documents Edited:**nn | nn**Documents Edited:**nn | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3347 | 23368 | `app/src/ai/agent/mod.rs` | nn**Documents Created:**nn | nn**Documents Created:**nn | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3437 | 23998 | `app/src/ai/agent_sdk/driver/output.rs` | {uri} ({})n{text} | {uri} ({})n{text} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3495 | 24404 | `app/src/ai/agent_sdk/driver/output.rs` | {code}n``` | {code}n``` | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3569 | 24922 | `app/src/ai/agent_sdk/driver.rs` | Ignoring runtime failure for {harness_name}: session already marked Success (pattern={}, excerpt={}) | Ignoring runtime failure for {harness_name}: session already marked Success (pattern={}, excerpt={}) | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3582 | 25013 | `app/src/ai/agent_sdk/driver.rs` | Skipping auth secret '{name}' ({:?}): '{conflict}' is already set in the process environment | Skipping auth secret '{name}' ({:?}): '{conflict}' is already set in the process environment | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3588 | 25055 | `app/src/ai/blocklist/agent_view/agent_input_footer/mod.rs` | Failed plugin operation for {agent:?}: {err}n{log} | Failed plugin operation for {agent:?}: {err}n{log} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3593 | 25090 | `app/src/ai/blocklist/agent_view/agent_input_footer/mod.rs` | Warp plugin installation — {agent:?}n{now}nn{log} | Warp plugin installation — {agent:?}n{now}nn{log} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3681 | 25706 | `app/src/ai/blocklist/agent_view/orchestration_pill_bar.rs` | {truncated}u{2026} | {truncated}u{2026} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3760 | 26259 | `app/src/ai/blocklist/block/view_impl/common.rs` | {ERROR_APOLOGY_TEXT}nn{message} | {ERROR_APOLOGY_TEXT}nn{message} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3763 | 26280 | `app/src/ai/blocklist/block/view_impl/common.rs` | {ERROR_APOLOGY_TEXT}nn{INTERNAL_WARP_ERROR} | {ERROR_APOLOGY_TEXT}nn{INTERNAL_WARP_ERROR} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3766 | 26301 | `app/src/ai/blocklist/block/view_impl/common.rs` | {ERROR_APOLOGY_TEXT}nn{error_message} | {ERROR_APOLOGY_TEXT}nn{error_message} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3902 | 27253 | `app/src/ai/blocklist/block.rs` | {prompt_text}nn{output_text} | {prompt_text}nn{output_text} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3911 | 27316 | `app/src/ai/blocklist/controller.rs` | Skipping event piggyback for conversation {conversation_id:?}: {} | Skipping event piggyback for conversation {conversation_id:?}: {} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3942 | 27533 | `app/src/ai/blocklist/controller.rs` | Found tool call result with ID '{action_id_str}' but no corresponding tool call in task context. Server conversation ID: '{server_conversati | Found tool call result with ID '{action_id_str}' but no corresponding tool call in task context. Server conversation ID: '{server_conversati | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 3981 | 27806 | `app/src/ai/blocklist/inline_action/code_diff_view.rs` | ...n | ...n | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 4074 | 28457 | `app/src/ai/mcp/templatable_manager/native.rs` | [error] MCP: Failed to spawn '{server_name}': command '{command_for_log}' not found (cwd: {cwd_display}). If your MCP server depends on a sp | [error] MCP: Failed to spawn '{server_name}': command '{command_for_log}' not found (cwd: {cwd_display}). If your MCP server depends on a sp | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 4285 | 29936 | `app/src/drive/workflows/enum_creation_dialog.rs` | # Enter a shell command that generates variants, delimited by newlines.nngit branch -a | # Enter a shell command that generates variants, delimited by newlines.nngit branch -a | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 4286 | 29943 | `app/src/drive/workflows/modal.rs` | echo "Hello {{your_name}}" # insert arguments with curly bracesn# enter a single-line command or an entire shell script | echo "Hello {{your_name}}" # insert arguments with curly bracesn# enter a single-line command or an entire shell script | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 4593 | 32096 | `app/src/terminal/view.rs` | No conversation ID found for requested command: ID: {:?}, command: {command} | No conversation ID found for requested command: ID: {:?}, command: {command} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 4602 | 32159 | `app/src/terminal/view.rs` | emit_long_running_command_agent_interaction_state_changed: agent_has_control={agent_has_control}, emitting state={state:?} | emit_long_running_command_agent_interaction_state_changed: agent_has_control={agent_has_control}, emitting state={state:?} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 4629 | 32348 | `app/src/terminal/view.rs` | Could not find session {session_id:?} in sessions model after being notified that the session had bootstrapped! | Could not find session {session_id:?} in sessions model after being notified that the session had bootstrapped! | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 4630 | 32355 | `app/src/terminal/view.rs` | cd "{path}" | cd "{path}" | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 4689 | 32768 | `app/src/terminal/view.rs` |  &&n |  &&n | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 4697 | 32824 | `app/src/terminal/view.rs` | ```n{}n``` | ```n{}n``` | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 4702 | 32859 | `app/src/terminal/view.rs` | {}n{} | {}n{} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 4712 | 32929 | `app/src/terminal/view.rs` | Pure is not yet supported in Warp. You might consider one of the supported prompts as an alternative.   | Pure is not yet supported in Warp. You might consider one of the supported prompts as an alternative.   | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 4730 | 33055 | `app/src/terminal/view.rs` | {{"request_id":"{}","conversation_id":"{}"}} | {{"request_id":"{}","conversation_id":"{}"}} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 4731 | 33062 | `app/src/terminal/view.rs` | {{"conversation_id":"{}"}} | {{"conversation_id":"{}"}} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 4734 | 33083 | `app/src/terminal/view.rs` | Block {index}: {}, {}.n | Block {index}: {}, {}.n | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 4747 | 33174 | `app/src/terminal/view.rs` | Block {}.nOutput: {} | Block {}.nOutput: {} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5098 | 35633 | `app/src/workspace/view.rs` | is_right_panel_open() returned true, but neither the resource center nor AI assistant are open | is_right_panel_open() returned true, but neither the resource center nor AI assistant are open | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5149 | 35990 | `app/src/workspace/view.rs` | {json_str}n | {json_str}n | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5251 | 36706 | `app/src/ai/agent_sdk/driver/harness/codex.rs` | {cli_name} resume --dangerously-bypass-approvals-and-sandbox {session_id} "$(cat '{prompt_path}')" | {cli_name} resume --dangerously-bypass-approvals-and-sandbox {session_id} "$(cat '{prompt_path}')" | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5252 | 36713 | `app/src/ai/agent_sdk/driver/harness/codex.rs` | {cli_name} --dangerously-bypass-approvals-and-sandbox "$(cat '{prompt_path}')" | {cli_name} --dangerously-bypass-approvals-and-sandbox "$(cat '{prompt_path}')" | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5269 | 36832 | `app/src/ai/agent_sdk/environment.rs` | All Warp dev images contain Python and Node. For more information, see: {}n | All Warp dev images contain Python and Node. For more information, see: {}n | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5274 | 36867 | `app/src/ai/agent_sdk/environment.rs` | All warpdotdev images contain Python and Node, in addition to language-specific tooling. For more info: {}n | All warpdotdev images contain Python and Node, in addition to language-specific tooling. For more info: {}n | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5279 | 36902 | `app/src/ai/agent_sdk/environment.rs` | All private repositories in an environment must belong to the same owner. Found multiple owners: {}.nIf you need support for private repos f | All private repositories in an environment must belong to the same owner. Found multiple owners: {}.nIf you need support for private repos f | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5325 | 37224 | `app/src/ai/agent_sdk/mod.rs` | - {}n | - {}n | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5332 | 37273 | `app/src/ai/agent_sdk/mod.rs` | {base_prompt}nn{user_prompt} | {base_prompt}nn{user_prompt} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5432 | 37973 | `app/src/ai/blocklist/inline_action/requested_command.rs` | {command_text}nnResponse: {result_text} | {command_text}nnResponse: {result_text} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5448 | 38085 | `app/src/ai/execution_profiles/editor/mod.rs` | e.g. "YOLO code" | e.g. "YOLO code" | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5530 | 38661 | `app/src/terminal/cli_agent.rs` | {file_path} L{start_line}-L{end_line} (+{lines_added} -{lines_removed}) -- run `git diff` to see the full context. | {file_path} L{start_line}-L{end_line} (+{lines_added} -{lines_removed}) -- run `git diff` to see the full context. | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5639 | 39424 | `app/src/terminal/input.rs` | # Environment variablesn{}nn | # Environment variablesn{}nn | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5725 | 40026 | `app/src/terminal/model/terminal_model.rs` | $$$rn | $$$rn | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5811 | 40628 | `app/src/ai/agent_sdk/artifact.rs` | Artifact UIDtArtifact typetCreated attDownload URLtExpires attContent typetFilepathtFilenametDescriptiontSize bytes | Artifact UIDtArtifact typetCreated attDownload URLtExpires attContent typetFilepathtFilenametDescriptiontSize bytes | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5812 | 40635 | `app/src/ai/agent_sdk/artifact.rs` | {}t{}t{}t{}t{}t{}t{}t{}t{}t{} | {}t{}t{}t{}t{}t{}t{}t{}t{}t{} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5814 | 40649 | `app/src/ai/agent_sdk/artifact.rs` | Artifact UIDtArtifact typetPath | Artifact UIDtArtifact typetPath | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5815 | 40656 | `app/src/ai/agent_sdk/artifact.rs` | {}t{}t{} | {}t{}t{} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5819 | 40684 | `app/src/ai/agent_sdk/artifact.rs` | Artifact UIDtFilepathtDescriptiontMIME typetSize bytes | Artifact UIDtFilepathtDescriptiontMIME typetSize bytes | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5820 | 40691 | `app/src/ai/agent_sdk/artifact.rs` | {}t{}t{}t{}t{} | {}t{}t{}t{}t{} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5829 | 40754 | `app/src/ai/agent_sdk/common.rs` | No environments are configured for this account.nYou can create an environment with `{cli_name} environment create`.nOr, re-run this command | No environments are configured for this account.nYou can create an environment with `{cli_name} environment create`.nOr, re-run this command | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5846 | 40873 | `app/src/ai/agent_sdk/driver/git_credentials.rs` | {}:n | {}:n | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5847 | 40880 | `app/src/ai/agent_sdk/driver/git_credentials.rs` |     oauth_token: {}n |     oauth_token: {}n | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5848 | 40887 | `app/src/ai/agent_sdk/driver/git_credentials.rs` |     git_protocol: httpsn |     git_protocol: httpsn | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5862 | 40985 | `app/src/ai/agent_sdk/driver/harness/claude_code/parent_bridge.rs` | Lead-agent updates arrived from Oz. Treat the latest lead-agent instructions below as authoritative.n | Lead-agent updates arrived from Oz. Treat the latest lead-agent instructions below as authoritative.n | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5863 | 40992 | `app/src/ai/agent_sdk/driver/harness/claude_code/parent_bridge.rs` | nnMore lead-agent messages are still staged and will be surfaced on a later turn. | nnMore lead-agent messages are still staged and will be surfaced on a later turn. | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5869 | 41034 | `app/src/ai/agent_sdk/driver/harness/claude_code/parent_bridge.rs` | ---nLead-agent message | ---nLead-agent message | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5945 | 41566 | `app/src/ai/blocklist/block/cli.rs` | Grep for the following patterns in {display_path}:n{patterns_list} | Grep for the following patterns in {display_path}:n{patterns_list} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5948 | 41587 | `app/src/ai/blocklist/block/cli.rs` | Find files that match the following patterns in {display_path}:n{patterns_list} | Find files that match the following patterns in {display_path}:n{patterns_list} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5951 | 41608 | `app/src/ai/blocklist/history_model.rs` | No agent identifier for parent conversation {parent_conversation_id:?}; child agent will not be linked to parent on the server. | No agent identifier for parent conversation {parent_conversation_id:?}; child agent will not be linked to parent on the server. | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5952 | 41615 | `app/src/ai/blocklist/history_model.rs` | set_conversation_pinned called for conversation {conversation_id:?} that is not loaded; pin state change to {pinned} will not be persisted. | set_conversation_pinned called for conversation {conversation_id:?} that is not loaded; pin state change to {pinned} will not be persisted. | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 5954 | 41629 | `app/src/ai/blocklist/history_model.rs` | mark_active_conversation_id: conversation {conversation_id:?} is not in terminal view {terminal_view_id:?} live list, skipping | mark_active_conversation_id: conversation {conversation_id:?} is not in terminal view {terminal_view_id:?} live list, skipping | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6418 | 44877 | `app/src/terminal/local_tty/terminal_manager.rs` | Session sharing was requested, but CreatingSharedSessions is disabled; skipping shared-session startup | Session sharing was requested, but CreatingSharedSessions is disabled; skipping shared-session startup | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6425 | 44926 | `app/src/terminal/local_tty/terminal_manager.rs` | [sharer] UniversalDeveloperInputContextUpdated: applying LRC interaction_state={interaction_state:?} | [sharer] UniversalDeveloperInputContextUpdated: applying LRC interaction_state={interaction_state:?} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6428 | 44947 | `app/src/terminal/local_tty/terminal_manager.rs` | Ignoring request to start sharing current session because CreatingSharedSessions is disabled | Ignoring request to start sharing current session because CreatingSharedSessions is disabled | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6443 | 45052 | `app/src/terminal/view/load_ai_conversation.rs` | cd "{path}" | cd "{path}" | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6511 | 45528 | `app/src/ai/blocklist/orchestration_event_streamer.rs` | register_consumer for {conversation_id:?}: {consumer_id:?} (total={}) | register_consumer for {conversation_id:?}: {consumer_id:?} (total={}) | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6512 | 45535 | `app/src/ai/blocklist/orchestration_event_streamer.rs` | unregister_consumer for {conversation_id:?}: {consumer_id:?} (remaining={remaining}) | unregister_consumer for {conversation_id:?}: {consumer_id:?} (remaining={remaining}) | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6515 | 45556 | `app/src/ai/blocklist/orchestration_event_streamer.rs` | Opening dormant Claude wake listener for {conversation_id:?} (gen={generation}, run_id={run_id:?}, since={local_cursor}) | Opening dormant Claude wake listener for {conversation_id:?} (gen={generation}, run_id={run_id:?}, since={local_cursor}) | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6516 | 45563 | `app/src/ai/blocklist/orchestration_event_streamer.rs` | Dormant Claude wake listener observed wake message for {conversation_id:?} at sequence {} message_id={} | Dormant Claude wake listener observed wake message for {conversation_id:?} at sequence {} message_id={} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6517 | 45570 | `app/src/ai/blocklist/orchestration_event_streamer.rs` | Dormant Claude wake listener stopped for {conversation_id:?} without observing an event | Dormant Claude wake listener stopped for {conversation_id:?} without observing an event | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6518 | 45577 | `app/src/ai/blocklist/orchestration_event_streamer.rs` | Dormant Claude wake listener failed for {conversation_id:?} (gen={generation}): {err:#} | Dormant Claude wake listener failed for {conversation_id:?} (gen={generation}): {err:#} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6519 | 45584 | `app/src/ai/blocklist/orchestration_event_streamer.rs` | Tearing down dormant Claude wake listener for {conversation_id:?} (gen={}) | Tearing down dormant Claude wake listener for {conversation_id:?} (gen={}) | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6520 | 45591 | `app/src/ai/blocklist/orchestration_event_streamer.rs` | Opening SSE stream for {conversation_id:?} (gen={generation}, run_ids={run_ids:?}, since={cursor}) | Opening SSE stream for {conversation_id:?} (gen={generation}, run_ids={run_ids:?}, since={cursor}) | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6523 | 45612 | `app/src/ai/blocklist/orchestration_event_streamer.rs` | Failed to read server cursor for dormant Claude wake listener run {run_id}: {err:#}; using local cursor {local_cursor} | Failed to read server cursor for dormant Claude wake listener run {run_id}: {err:#}; using local cursor {local_cursor} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6552 | 45815 | `app/src/ai/blocklist/action_model/execute/grep.rs` | {NON_ZERO_EXIT_CODE_ERROR}, output:n{output} | {NON_ZERO_EXIT_CODE_ERROR}, output:n{output} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6556 | 45843 | `app/src/ai/blocklist/action_model/execute/grep.rs` |  "{target_path}" |  "{target_path}" | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6558 | 45857 | `app/src/ai/blocklist/action_model/execute/grep.rs` |  -e "{}" |  -e "{}" | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6559 | 45864 | `app/src/ai/blocklist/action_model/execute/grep.rs` | Get-ChildItem -Path "{}" -Recurse -File / Select-String -NoEmphasis -CaseSensitive -Pattern {} | Get-ChildItem -Path "{}" -Recurse -File / Select-String -NoEmphasis -CaseSensitive -Pattern {} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6621 | 46298 | `app/src/ai/conversation_details_panel.rs` |  && n |  && n | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6649 | 46494 | `app/src/ai/agent_sdk/driver/harness/gemini.rs` | {ctx}nn{prompt} | {ctx}nn{prompt} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6650 | 46501 | `app/src/ai/agent_sdk/driver/harness/gemini.rs` | {cli_name} --yolo -i "$(cat '{prompt_path}')" | {cli_name} --yolo -i "$(cat '{prompt_path}')" | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6757 | 47240 | `app/src/workspace/view/codex_modal.rs` | Use Codex directly in Oz and leverage features like in-app code review, agent session sharing and file editing. | Use Codex directly in Oz and leverage features like in-app code review, agent session sharing and file editing. | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6768 | 47317 | `app/src/workspace/view/crash_recovery.rs` | We detected a crash during application startup, and adjusted your settings to use Xwayland for windowing. This can result in blurry text if  | We detected a crash during application startup, and adjusted your settings to use Xwayland for windowing. This can result in blurry text if  | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6784 | 47429 | `app/src/workspace/view.rs` | Have Warp installed but redirecting to download page?nEnable Local Network Access for {} in your browser. | Have Warp installed but redirecting to download page?nEnable Local Network Access for {} in your browser. | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6888 | 48157 | `app/src/terminal/local_tty/unix.rs` | 500n | 500n | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6939 | 48514 | `app/src/terminal/model/tmux/commands.rs` | refresh-client -C {num_cols},{num_rows}n | refresh-client -C {num_cols},{num_rows}n | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6940 | 48521 | `app/src/terminal/model/tmux/commands.rs` | set destroy-unattached onn | set destroy-unattached onn | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6941 | 48528 | `app/src/terminal/model/tmux/commands.rs` | set window-size smallestn | set window-size smallestn | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6959 | 48654 | `app/src/terminal/model/tmux/commands.rs` | list-panes -F "#{{?pane_active,{PRIMARY_WINDOW_PANE_PREFIX}: ,}}#{{window_id}} #{{pane_id}}"n | list-panes -F "#{{?pane_active,{PRIMARY_WINDOW_PANE_PREFIX}: ,}}#{{window_id}} #{{pane_id}}"n | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6969 | 48724 | `app/src/ai/agent_sdk/driver/attachments.rs` | fetch_and_download_handoff_snapshot_attachments called with OzHandoff disabled; call sites should gate on the flag before invoking | fetch_and_download_handoff_snapshot_attachments called with OzHandoff disabled; call sites should gate on the flag before invoking | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6996 | 48913 | `app/src/ai/blocklist/action_model/execute/run_agents.rs` | {base_prompt}nn{per_agent_prompt} | {base_prompt}nn{per_agent_prompt} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6998 | 48927 | `app/src/ai/blocklist/controller/shared_session.rs` | should_skip_replayed_response: no existing conversation id, not skipping (request_id={init_request_id}) | should_skip_replayed_response: no existing conversation id, not skipping (request_id={init_request_id}) | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 6999 | 48934 | `app/src/ai/blocklist/controller/shared_session.rs` | should_skip_replayed_response: not skipping (request_id={init_request_id}, conversation_id={conversation_id:?}, is_receiving_replay={is_rece | should_skip_replayed_response: not skipping (request_id={init_request_id}, conversation_id={conversation_id:?}, is_receiving_replay={is_rece | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 7000 | 48941 | `app/src/ai/blocklist/controller/shared_session.rs` | should_skip_replayed_response: not skipping, request_id not found in local conversation (request_id={init_request_id}, conversation_id={conv | should_skip_replayed_response: not skipping, request_id not found in local conversation (request_id={init_request_id}, conversation_id={conv | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 7198 | 50336 | `app/src/terminal/local_tty/windows/environment.rs` | System\CurrentControlSet\Control\Session Manager\Environment | System\CurrentControlSet\Control\Session Manager\Environment | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 7258 | 50762 | `app/src/terminal/shared_session/viewer/terminal_manager.rs` | [viewer] UniversalDeveloperInputContextUpdated: applying LRC interaction_state={interaction_state:?} | [viewer] UniversalDeveloperInputContextUpdated: applying LRC interaction_state={interaction_state:?} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 7289 | 50980 | `app/src/ai/agent_sdk/driver/terminal.rs` | Session sharing requested but the CreatingSharedSessions feature flag is not enabled. This is likely due to a team administrator disabling s | Session sharing requested but the CreatingSharedSessions feature flag is not enabled. This is likely due to a team administrator disabling s | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 7341 | 51346 | `app/src/ai/execution_profiles/profiles.rs` | Reconciled default execution profile with cloud after initial load: profile_id={id:?}, sync_id={sync_id:?} | Reconciled default execution profile with cloud after initial load: profile_id={id:?}, sync_id={sync_id:?} | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 7424 | 51939 | `app/src/terminal/keys_settings.rs` | The keybinding used for the global activation hotkey. Format: modifiers (cmd, ctrl, alt, shift, meta) and a key joined by '-', e.g. "cmd-shi | The keybinding used for the global activation hotkey. Format: modifiers (cmd, ctrl, alt, shift, meta) and a key joined by '-', e.g. "cmd-shi | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| 7464 | 52228 | `app/src/terminal/cli_agent_sessions/plugin_manager/mod.rs` | $ {display_cmd}n | $ {display_cmd}n | English preserved; verify this is product/internal text / source state is missing-in-current-source |
| ... | ... | ... | ... | ... | 10 more rows omitted |

## Placeholder And URL Risks

| entry | line | path | source | target | notes |
| ---: | ---: | --- | --- | --- | --- |
| 143 | 1045 | `crates/onboarding/src/callout/view.rs` | Your terminal input accepts both terminal commands and agent prompts and automatically detects which you're using. Use {} to lock the input  | Warp 输入框既可输入终端命令，也可输入 Agent 提示词，并会自动识别你的输入类型。使用 {} 可锁定为 Agent 模式（自然语言）或终端模式（命令）。 |  |
| 151 | 1101 | `crates/onboarding/src/callout/view.rs` | Run commands here, just like a regular terminal. If you type a question or task using natural language, Warp can suggest opening it in agent | 在这里像常规终端一样运行命令。如果你用自然语言输入问题或任务，Warp 可以建议在 Agent 模式中打开。你也可以随时使用 {} 覆盖。 |  |
| 155 | 1129 | `crates/onboarding/src/callout/view.rs` | Agent mode gives your questions and tasks their own conversation, so you can ask follow-ups without leaving your terminal workflow. Press {} | Agent 模式会为你的问题和任务创建独立对话，因此你可以继续追问而不离开终端工作流。随时按 {} 返回终端模式。 |  |
| 253 | 1841 | `app/src/auth/mod.rs` | You have {num_long_running_commands} {plural} running. | 你有 {num_long_running_commands} 个正在运行的{plural}。 |  |
| 257 | 1869 | `app/src/auth/mod.rs` | You have {num_shared_sessions} shared {plural}. | 你有 {num_shared_sessions} 个已共享的{plural}。 |  |
| 260 | 1890 | `app/src/auth/mod.rs` | You have {num_unsaved_objects} unsynced Warp Drive {plural}. Logging out will cause you to lose the {plural}. | 你有 {num_unsaved_objects} 个未同步的 Warp Drive {plural}。退出登录会导致这些{plural}丢失。 |  |
| 263 | 1911 | `app/src/auth/mod.rs` | You have {num_unsaved_files} unsaved {plural}. Logging out will cause you to lose the {plural}. | 你有 {num_unsaved_files} 个未保存的{plural}。退出登录会导致这些{plural}丢失。 |  |
| 265 | 1925 | `crates/onboarding/src/model.rs` | Starting at ${}/mo | ${}/月起 |  |
| 322 | 2324 | `app/src/menu.rs` | {} Selected | 已选择 {} |  |
| 323 | 2331 | `app/src/menu.rs` | {selected_item_text} Selected | 已选择 {selected_item_text} |  |
| 324 | 2338 | `app/src/menu.rs` | {} Expanded | 已展开 {} |  |
| 344 | 2478 | `app/src/workspace/bonus_grant_notification_model.rs` | {} Reload Credits have been added to your {}. | {} 点 Reload 额度已添加到你的 {}。 |  |
| 347 | 2499 | `app/src/workspace/cli_install.rs` | Failed to create symlink with admin privileges: {stderr} | 使用管理员权限创建符号链接失败：{stderr} |  |
| 348 | 2506 | `app/src/workspace/cli_install.rs` | Failed to remove file with admin privileges: {stderr} | 使用管理员权限移除文件失败：{stderr} |  |
| 350 | 2520 | `app/src/workspace/cli_install.rs` | Cannot install: {:?} exists but is not a symlink. Please remove it manually first. | 无法安装：{:?} 已存在但不是符号链接。请先手动移除。 |  |
| 352 | 2534 | `app/src/workspace/cli_install.rs` | Cannot uninstall: {:?} exists but is not a symlink. Please remove it manually. | 无法卸载：{:?} 已存在但不是符号链接。请手动移除。 |  |
| 361 | 2597 | `app/src/workspace/delete_conversation_confirmation_dialog.rs` | Delete '{}'? | 删除“{}”？ |  |
| 399 | 2863 | `app/src/workspace/view/vertical_tabs.rs` | {member_count} tabs | {member_count} 个标签页 |  |
| 412 | 2956 | `app/src/workspace/view/vertical_tabs.rs` | + {hidden_count} more | 另有 {hidden_count} 项 |  |
| 417 | 2991 | `app/src/workspace/view/vertical_tabs.rs` | and {extra_open_tabs} more | 以及另外 {extra_open_tabs} 项 |  |
| 439 | 3145 | `app/src/workspace/view.rs` | Current version is {version} | 当前版本为 {version} |  |
| 440 | 3152 | `app/src/workspace/view.rs` | Install update ({}) | 安装更新 ({}) |  |
| 441 | 3159 | `app/src/workspace/view.rs` | Updating to ({}) | 正在更新到 ({}) |  |
| 443 | 3173 | `app/src/workspace/view.rs` | Successfully installed the Oz CLI! You can now run '{command_name}' from the command line. | 已成功安装 Oz CLI！你现在可以在命令行运行 '{command_name}'。 |  |
| 445 | 3187 | `app/src/workspace/view.rs` | Failed to install Oz command: {error} | 安装 Oz 命令失败：{error} |  |
| 447 | 3201 | `app/src/workspace/view.rs` | Failed to uninstall Oz command: {error} | 卸载 Oz 命令失败：{error} |  |
| 475 | 3397 | `app/src/workspace/view.rs` | {t} (Moved to cloud) | {t}（已移至云端） |  |
| 488 | 3488 | `app/src/workspace/view.rs` | You {verb} mouse reporting. | 你已{verb}鼠标报告。 |  |
| 489 | 3495 | `app/src/workspace/view.rs` |  Press {} to undo. |  按 {} 撤销。 |  |
| 508 | 3628 | `app/src/search/action/search_item.rs` | Selected {}, {}. | 已选择 {}，{}。 |  |
| 510 | 3642 | `app/src/search/action/search_item.rs` | Press enter to confirm. Use {} binding to run this action in the future. | 按 Enter 确认。以后可使用 {} 快捷键运行此操作。 |  |
| 512 | 3656 | `app/src/search/ai_context_menu/blocks/search_item.rs` | {} minutes ago | {} 分钟前 |  |
| 513 | 3663 | `app/src/search/ai_context_menu/blocks/search_item.rs` | {} hours ago | {} 小时前 |  |
| 514 | 3670 | `app/src/search/ai_context_menu/blocks/search_item.rs` | {} days ago | {} 天前 |  |
| 517 | 3691 | `app/src/search/ai_context_menu/code/search_item.rs` | Code symbol: {} in {}:{} | 代码符号：{}，位于 {}:{} |  |
| 522 | 3726 | `app/src/search/ai_context_menu/diffset/search_item.rs` | Changes vs. {branch} | 相对 {branch} 的更改 |  |
| 525 | 3747 | `app/src/search/ai_context_menu/diffset/search_item.rs` | All changes compared to {branch} | 与 {branch} 相比的所有更改 |  |
| 556 | 3964 | `app/src/search/command_palette/conversations/search_item.rs` | Fork current conversation ({title}) | 分叉当前对话（{title}） |  |
| 557 | 3971 | `app/src/search/command_palette/conversations/search_item.rs` | Press enter to navigate to conversation "{}". | 按 Enter 导航到对话“{}”。 |  |
| 562 | 4006 | `app/src/search/command_palette/files/search_item.rs` | Create a file named {}… | 创建名为 {} 的文件… |  |
| 563 | 4013 | `app/src/search/command_palette/files/search_item.rs` | Create file: {} | 创建文件：{} |  |
| 564 | 4020 | `app/src/search/command_palette/files/search_item.rs` | Press Enter to create {} in the current directory | 按 Enter 在当前目录中创建 {} |  |
| 565 | 4027 | `app/src/search/command_palette/launch_config/search_item.rs` | Selected {}. | 已选择 {}。 |  |
| 570 | 4062 | `app/src/search/command_palette/navigation/render.rs` | Completed {mins} minute ago | 已完成，{mins} 分钟前 |  |
| 571 | 4069 | `app/src/search/command_palette/navigation/render.rs` | Completed {mins} minutes ago | 已完成，{mins} 分钟前 |  |
| 575 | 4097 | `app/src/search/command_palette/navigation/search_item.rs` | Selected {}. {}. | 已选择 {}。{}。 |  |
| 587 | 4181 | `app/src/search/command_palette/new_session/new_session_option.rs` | Create New Tab: {} | 创建新标签页：{} |  |
| 588 | 4188 | `app/src/search/command_palette/new_session/new_session_option.rs` | Create New Window: {} | 创建新窗口：{} |  |
| 589 | 4195 | `app/src/search/command_palette/new_session/new_session_option.rs` | Split Pane {direction}: {} | 向{direction}拆分窗格：{} |  |
| 590 | 4202 | `app/src/search/command_palette/new_session/search_item.rs` | Selected {}. | 已选择 {}。 |  |
| 592 | 4216 | `app/src/search/command_palette/tabs/search_item.rs` | [Tab {}] {} | [标签页 {}] {} |  |
| 593 | 4223 | `app/src/search/command_palette/tabs/search_item.rs` | Selected tab: {}. | 已选择标签页：{}。 |  |
| 594 | 4230 | `app/src/search/command_palette/tabs/search_item.rs` | Press enter to navigate to tab: {}. | 按 Enter 导航到标签页：{}。 |  |
| 651 | 4629 | `app/src/search/command_palette/warp_drive/env_var_collection_search_item.rs` | Environment Variables: {} | 环境变量：{} |  |
| 655 | 4657 | `app/src/search/command_search/ai_queries/ai_queries_search_item.rs` | Ran {} | 已运行 {} |  |
| 656 | 4664 | `app/src/search/command_search/ai_queries/ai_queries_search_item.rs` | AI query: {} | AI 查询：{} |  |
| 658 | 4678 | `app/src/search/command_search/env_var_collections/env_var_collection_search_item.rs` | Environment Variables: {} | 环境变量：{} |  |
| 659 | 4685 | `app/src/search/command_search/history/history_search_item.rs` | History item: {} | 历史项：{} |  |
| 677 | 4811 | `app/src/search/command_search/warp_ai.rs` | Warp AI: {} | Warp AI：{} |  |
| 691 | 4909 | `app/src/search/search_bar.rs` | Loading {} suggestions | 正在加载 {} 条建议 |  |
| 693 | 4923 | `app/src/search/search_bar.rs` | Selected {} | 已选择 {} |  |
| 696 | 4944 | `app/src/search/slash_command_menu/static_commands/bindings.rs` | Slash command: {} | 斜杠命令：{} |  |
| 896 | 6365 | `app/src/search/welcome_palette/view.rs` | Add repository {keystroke} | 添加仓库 {keystroke} |  |
| 898 | 6379 | `app/src/search/welcome_palette/view.rs` | Terminal session {keystroke} | 终端会话 {keystroke} |  |
| 906 | 6435 | `app/src/settings_view/mod.rs` | Enable {description_suffix} | 启用 {description_suffix} |  |
| 907 | 6442 | `app/src/settings_view/mod.rs` | Disable {description_suffix} | 停用 {description_suffix} |  |
| 969 | 6876 | `app/src/settings_view/appearance_page.rs` | {} (default) | {}（默认） |  |
| 1016 | 7205 | `app/src/settings_view/appearance_page.rs` | Window Opacity: {opacity_value} | 窗口不透明度：{opacity_value} |  |
| 1019 | 7226 | `app/src/settings_view/appearance_page.rs` | Window Blur Radius: {blur_value} | 窗口模糊半径：{blur_value} |  |
| 1112 | 7877 | `app/src/settings_view/features_page.rs` | Setting the limit above 100k lines may impact performance. Maximum rows supported is {max_rows}. | 将限制设置为超过 10 万行可能影响性能。支持的最大行数为 {max_rows}。 |  |
| 1144 | 8101 | `app/src/settings_view/features_page.rs` | {} accepts autosuggestions. | {} 接受自动建议。 |  |
| 1146 | 8115 | `app/src/settings_view/features_page.rs` | Completions open as you type (or {}). | 补全会在输入时打开（或按 {}）。 |  |
| 1148 | 8129 | `app/src/settings_view/features_page.rs` | {} opens completion menu. | {} 打开补全菜单。 |  |
| 1172 | 8297 | `app/src/settings_view/features_page.rs` | Current backend: {} | 当前后端：{} |  |
| 1301 | 9200 | `app/src/settings_view/ai_page.rs` | Resets {formatted_next_refresh_time} | 将于 {formatted_next_refresh_time} 重置 |  |
| 1302 | 9207 | `app/src/settings_view/ai_page.rs` | This is the {} limit of AI credits for your account. | 这是你账号 AI 额度的{}限制。 |  |
| 1434 | 10131 | `app/src/settings_view/code_page.rs` | Discovered {total_nodes} chunks | 已发现 {total_nodes} 个块 |  |
| 1435 | 10138 | `app/src/settings_view/code_page.rs` | Syncing - {completed_nodes} / {total_nodes} | 正在同步 - {completed_nodes} / {total_nodes} |  |
| 1446 | 10215 | `app/src/settings_view/code_page.rs` | Indexing - {completed} / {total} | 正在索引 - {completed} / {total} |  |
| 1447 | 10222 | `app/src/settings_view/code_page.rs` | Indexing - {completed} | 正在索引 - {completed} |  |
| 1448 | 10229 | `app/src/settings_view/code_page.rs` | Indexing - 0 / {total} | 正在索引 - 0 / {total} |  |
| 1502 | 10607 | `app/src/settings_view/mcp_servers_page.rs` | Successfully logged out of {name} MCP server | 已成功退出 {name} MCP 服务器登录 |  |
| 1505 | 10628 | `app/src/settings_view/mcp_servers_page.rs` | Unknown MCP server '{autoinstall_param}' | 未知 MCP 服务器“{autoinstall_param}” |  |
| 1521 | 10740 | `app/src/settings_view/mcp_servers/edit_page.rs` | Edit {name} MCP Server | 编辑 {name} MCP 服务器 |  |
| 1528 | 10789 | `app/src/settings_view/mcp_servers/installation_modal.rs` | Install {name} | 安装 {name} |  |
| 1546 | 10915 | `app/src/settings_view/mcp_servers/list_page.rs` | Shared by Warp and {name} | 由 Warp 和 {name} 共享 |  |
| 1549 | 10936 | `app/src/settings_view/mcp_servers/list_page.rs` | Detected from {} | 检测自 {} |  |
| 1551 | 10950 | `app/src/settings_view/mcp_servers/list_page.rs` | Shared by: {creator} | 共享者：{creator} |  |
| 1559 | 11006 | `app/src/settings_view/mcp_servers/server_card.rs` | {} tools available | {} 个工具可用 |  |
| 1570 | 11083 | `app/src/settings_view/mcp_servers/update_modal.rs` | Update {name} | 更新 {name} |  |
| 1571 | 11090 | `app/src/settings_view/mcp_servers/update_modal.rs` | This server has {} updates available, which would you like to proceed with? | 此服务器有 {} 个可用更新，你想继续哪一个？ |  |
| 1574 | 11111 | `app/src/settings_view/mcp_servers/update_modal.rs` | Update from {publisher_string} | 从 {publisher_string} 更新 |  |
| 1575 | 11118 | `app/src/settings_view/mcp_servers/update_modal.rs` | Update from {name} | 从 {name} 更新 |  |
| 1576 | 11125 | `app/src/settings_view/mcp_servers/update_modal.rs` | Version {new_version} | 版本 {new_version} |  |
| 1582 | 11167 | `app/src/settings_view/environments_page.rs` | Last edited: {} | 上次编辑：{} |  |
| 1583 | 11174 | `app/src/settings_view/environments_page.rs` | Last used: {} | 上次使用：{} |  |
| 1597 | 11272 | `app/src/settings_view/environments_page.rs` | Shared by Warp and {} | 由 Warp 和 {} 共享 |  |
| 1611 | 11370 | `app/src/settings_view/environments_page.rs` | Setup commands: {} | 设置命令：{} |  |
| 1625 | 11468 | `app/src/settings_view/agent_assisted_environment_modal.rs` | Selected folder is not a Git repository: {path} | 所选文件夹不是 Git 仓库：{path} |  |
| 1650 | 11643 | `app/src/settings_view/update_environment_form.rs` | {char_count} / {DESCRIPTION_MAX_CHARS} characters | {char_count} / {DESCRIPTION_MAX_CHARS} 个字符 |  |
| 1785 | 12588 | `app/src/settings_view/billing_and_usage_page.rs` | {discount}% off | {discount}% 折扣 |  |
| 1796 | 12665 | `app/src/settings_view/billing_and_usage_page.rs` | {} credits remaining | 剩余 {} 点额度 |  |
| 1812 | 12777 | `app/src/settings_view/billing_and_usage_page.rs` | {} credits | {} 点额度 |  |
| 1815 | 12798 | `app/src/settings_view/billing_and_usage_page.rs` | When enabled, auto reload will automatically purchase {auto_reload_amount} credits when your add-on credit balance reaches 100 credits remai | 启用后，当你的附加额度余额达到剩余 100 点额度时，自动充值会自动购买 {auto_reload_amount} 点额度。 |  |
| 1823 | 12854 | `app/src/settings_view/billing_and_usage_page.rs` | Usage resets on {formatted_date} | 使用量将在 {formatted_date} 重置 |  |
| 1828 | 12889 | `app/src/settings_view/billing_and_usage_page.rs` | This is the {refresh_duration} limit of AI credits for your account. | 这是你账号 AI 额度的{refresh_duration}限制。 |  |
| 1832 | 12917 | `app/src/settings_view/billing_and_usage_page.rs` | Resets {formatted_next_refresh_time} | 重置时间：{formatted_next_refresh_time} |  |
| 1882 | 13267 | `app/src/settings_view/billing_and_usage_page_v2.rs` | {} credits remaining | 剩余 {} 点额度 |  |
| 1886 | 13295 | `app/src/settings_view/billing_and_usage_page_v2.rs` | {} credits | {} 点额度 |  |
| 1888 | 13309 | `app/src/settings_view/billing_and_usage_page_v2.rs` | When any member on your team’s credit balance reaches 100 credits remaining, automatically purchase {auto_reload_credit_amount}. | 当你团队中任一成员的额度余额达到剩余 100 点额度时，自动购买 {auto_reload_credit_amount}。 |  |
| 1893 | 13344 | `app/src/settings_view/billing_and_usage_page_v2.rs` | Your admin has enabled auto-reload for add-on credits. When your personal add-on credit balance runs low, Warp will automatically purchase { | 你的管理员已为附加额度启用自动充值。当你的个人附加额度余额不足时，Warp 会自动以 {price} 购买 {credits} 点额度并添加到你的余额。 |  |
| 1911 | 13470 | `app/src/settings_view/billing_and_usage_page_v2.rs` | Auto-reload enabled. We'll refill with {credits} credits when your balance runs low. | 自动充值已启用。余额不足时，我们会补充 {credits} 点额度。 |  |
| 1961 | 13820 | `app/src/drive/sharing/dialog/mod.rs` | Already shared with {} | 已与 {} 共享 |  |
| 1993 | 14044 | `app/src/tab_configs/params_modal.rs` | Enter {name} | 输入 {name} |  |
| 1996 | 14065 | `app/src/tab_configs/remove_confirmation_dialog.rs` | Remove '{}'? | 移除“{}”？ |  |
| 2030 | 14303 | `app/src/themes/theme_creator_body.rs` | Failed to process selected image due to error: {e}. Please try again with a different image. | 由于错误 {e}，无法处理所选图片。请换一张图片后重试。 |  |
| 2041 | 14380 | `app/src/terminal/buy_credits_banner.rs` | When enabled, auto reload will purchase {} credits when your credit balance gets low | 启用后，当你的额度余额不足时，自动充值会购买 {} 点额度 |  |
| 2058 | 14499 | `app/src/terminal/input/slash_commands/cloud_mode_v2_view.rs` | Show {hidden_count} more | 再显示 {hidden_count} 个 |  |
| 2059 | 14506 | `app/src/terminal/input/slash_commands/mod.rs` | {} requires AI to be enabled | {} 需要启用 AI |  |
| 2062 | 14527 | `app/src/terminal/input/slash_commands/mod.rs` | Please provide a color after /set-tab-color ({}) | 请在 /set-tab-color 后提供颜色（{}） |  |
| ... | ... | ... | ... | ... | 1543 more rows omitted |

## Command And Slash Command Risks

| entry | line | path | source | target | notes |
| ---: | ---: | --- | --- | --- | --- |
| 4 | 28 | `crates/onboarding/src/slides/intro_slide.rs` | A modern terminal with state of the art agents built in. | 内置先进 Agent 的现代终端。 |  |
| 9 | 63 | `crates/onboarding/src/slides/intention_slide.rs` | An agent-first experience with best in class terminal support. Get terminal and agent driven development AI features like: | Agent 优先体验，并保留一流终端能力。启用终端与 Agent 驱动开发功能： |  |
| 10 | 70 | `crates/onboarding/src/slides/intention_slide.rs` | Just use the terminal | 只使用终端 |  |
| 12 | 84 | `crates/onboarding/src/slides/intention_slide.rs` | A modern terminal optimized for speed, context, and control without AI. | 一个重视速度、上下文和掌控感的现代终端，不启用 AI。 |  |
| 39 | 273 | `crates/onboarding/src/slides/agent_slide.rs` | Runs commands, writes code, and reads files without asking. | 无需确认即可运行命令、写代码和读取文件。 |  |
| 41 | 287 | `crates/onboarding/src/slides/agent_slide.rs` | Can plan, read files, and execute low-risk commands. Asks before making any changes or executing sensitive commands. | 可以规划、读取文件并执行低风险命令；修改文件或执行敏感命令前会请求确认。 |  |
| 78 | 554 | `app/src/auth/login_slide.rs` | Connect your account to save and share notebooks, workflows, and more across devices. | 连接账号以在多台设备间保存和共享笔记本、工作流等内容。 |  |
| 91 | 670 | `app/src/auth/login_slide.rs` | Warp Drive lets you save workflows and knowledge across devices and share them with your team. By continuing, you won't have access to the f | Warp Drive 可让你跨设备保存工作流和知识，并与团队共享。继续后，你将无法使用以下功能： |  |
| 105 | 779 | `app/src/workspace/view/vertical_tabs.rs` | Terminal | 终端 |  |
| 117 | 863 | `app/src/workspace/view/vertical_tabs.rs` | Command / Conversation | 命令 / 对话 |  |
| 126 | 926 | `crates/onboarding/src/slides/free_user_no_ai_slide.rs` | Classic terminal with third-party agents | 经典终端与第三方 Agent |  |
| 127 | 933 | `crates/onboarding/src/slides/free_user_no_ai_slide.rs` | A modern terminal that supports third-party agents (Claude Code, Codex, Gemini CLI) and classic terminal workflows. | 支持 Claude Code、Codex、Gemini CLI 等第三方 Agent 和经典终端工作流的现代终端。 |  |
| 143 | 1045 | `crates/onboarding/src/callout/view.rs` | Your terminal input accepts both terminal commands and agent prompts and automatically detects which you're using. Use {} to lock the input  | Warp 输入框既可输入终端命令，也可输入 Agent 提示词，并会自动识别你的输入类型。使用 {} 可锁定为 Agent 模式（自然语言）或终端模式（命令）。 |  |
| 150 | 1094 | `crates/onboarding/src/callout/view.rs` | Welcome to terminal mode | 欢迎进入终端模式 |  |
| 151 | 1101 | `crates/onboarding/src/callout/view.rs` | Run commands here, just like a regular terminal. If you type a question or task using natural language, Warp can suggest opening it in agent | 在这里像常规终端一样运行命令。如果你用自然语言输入问题或任务，Warp 可以建议在 Agent 模式中打开。你也可以随时使用 {} 覆盖。 |  |
| 152 | 1108 | `crates/onboarding/src/callout/view.rs` | You’re in terminal mode | 你正在使用终端模式 |  |
| 155 | 1129 | `crates/onboarding/src/callout/view.rs` | Agent mode gives your questions and tasks their own conversation, so you can ask follow-ups without leaving your terminal workflow. Press {} | Agent 模式会为你的问题和任务创建独立对话，因此你可以继续追问而不离开终端工作流。随时按 {} 返回终端模式。 |  |
| 158 | 1150 | `crates/onboarding/src/callout/view.rs` | Back to terminal | 返回终端 |  |
| 211 | 1533 | `app/src/auth/auth_override_warning_body.rs` | Export your data | 导出数据 |  |
| 231 | 1687 | `crates/onboarding/src/lib.rs` | Next command predictions | 下一条命令预测 |  |
| 232 | 1694 | `crates/onboarding/src/lib.rs` | Prompt suggestions | 提示词建议 |  |
| 238 | 1736 | `crates/onboarding/src/callout/view.rs` | Agent mode gives your questions and tasks their own conversation, so you can ask follow-ups without leaving your terminal workflow.nnSubmit  | Agent 模式会为你的问题和任务创建独立对话，因此你可以继续追问而不离开终端工作流。提交下面的查询，让 Agent 初始化此项目；或按 ⊗ 清空输入并开始自己的任务！ |  |
| 253 | 1841 | `app/src/auth/mod.rs` | You have {num_long_running_commands} {plural} running. | 你有 {num_long_running_commands} 个正在运行的{plural}。 |  |
| 274 | 1988 | `app/src/app_menus.rs` | Enable Shell Debug Mode (-x) for New Sessions | 为新会话启用 Shell 调试模式 (-x) |  |
| 275 | 1995 | `app/src/app_menus.rs` | Disable Shell Debug Mode (-x) for New Sessions | 为新会话停用 Shell 调试模式 (-x) |  |
| 282 | 2044 | `app/src/app_menus.rs` | Show In-band Command Blocks | 显示带内命令块 |  |
| 283 | 2051 | `app/src/app_menus.rs` | Hide In-band Command Blocks | 隐藏带内命令块 |  |
| 286 | 2072 | `app/src/app_menus.rs` | Export Default Settings as CSV to home dir | 将默认设置导出为 CSV 到主目录 |  |
| 291 | 2107 | `app/src/app_menus.rs` | Set Warp as Default Terminal | 将 Warp 设为默认终端 |  |
| 295 | 2135 | `app/src/app_menus.rs` | Use Warp's Prompt | 使用 Warp 提示符 |  |
| 296 | 2142 | `app/src/app_menus.rs` | Copy on Select within the Terminal | 在终端中选中即复制 |  |
| 316 | 2282 | `app/src/app_menus.rs` | New Terminal Tab | 新建终端标签页 |  |
| 338 | 2436 | `app/src/workspace/action.rs` | Creating a team workflow | 正在创建团队工作流 |  |
| 341 | 2457 | `app/src/workspace/action.rs` | Creating a team prompt | 正在创建团队提示词 |  |
| 367 | 2639 | `app/src/workspace/mod.rs` | New Terminal Tab | 新建终端标签页 |  |
| 390 | 2800 | `app/src/workspace/rewind_confirmation_dialog.rs` | Rewinding does not affect files edited manually or via shell commands. | 回退不会影响手动或通过 shell 命令编辑的文件。 |  |
| 391 | 2807 | `app/src/workspace/rewind_confirmation_dialog.rs` | Are you sure you want to rewind? This will restore your code and conversation to before this point, and cancel any commands the agent is cur | 确定要回退吗？这会将你的代码和对话恢复到此点之前，并取消 Agent 当前正在运行的所有命令。原始对话的副本会保存到对话历史记录中。 |  |
| 404 | 2898 | `app/src/workspace/view/vertical_tabs.rs` | Workflow | 工作流 |  |
| 429 | 3075 | `app/src/workspace/view.rs` | Terminal | 终端 |  |
| 443 | 3173 | `app/src/workspace/view.rs` | Successfully installed the Oz CLI! You can now run '{command_name}' from the command line. | 已成功安装 Oz CLI！你现在可以在命令行运行 '{command_name}'。 |  |
| 445 | 3187 | `app/src/workspace/view.rs` | Failed to install Oz command: {error} | 安装 Oz 命令失败：{error} |  |
| 446 | 3194 | `app/src/workspace/view.rs` | Successfully uninstalled the Oz command. | 已成功卸载 Oz 命令。 |  |
| 447 | 3201 | `app/src/workspace/view.rs` | Failed to uninstall Oz command: {error} | 卸载 Oz 命令失败：{error} |  |
| 471 | 3369 | `app/src/workspace/view.rs` | No active terminal session to hand off. Focus a pane and try again. | 没有可交接的活动终端会话。请聚焦一个窗格后重试。 |  |
| 473 | 3383 | `app/src/workspace/view.rs` | Can't hand off while a command is running. Cancel the command or wait for it to finish. | 命令运行时无法交接。请取消命令或等待其完成。 |  |
| 479 | 3425 | `app/src/workspace/view.rs` | No terminal pane open. Open a new pane to attach as context. | 没有打开的终端窗格。请打开一个新窗格以附加为上下文。 |  |
| 481 | 3439 | `app/src/workspace/view.rs` | A command in this session is still running. | 此会话中仍有命令正在运行。 |  |
| 482 | 3446 | `app/src/workspace/view.rs` | Cannot open a new terminal session | 无法打开新的终端会话 |  |
| 483 | 3453 | `app/src/workspace/view.rs` | Run Agent Mode Workflow | 运行 Agent 模式工作流 |  |
| 484 | 3460 | `app/src/workspace/view.rs` | This workflow is no longer available. | 此工作流已不再可用。 |  |
| 490 | 3502 | `app/src/workspace/view.rs` | Command from Warp AI | 来自 Warp AI 的命令 |  |
| 491 | 3509 | `app/src/workspace/view.rs` | Ask Warp AI to explain errors, suggest commands or write scripts. | 让 Warp AI 解释错误、建议命令或编写脚本。 |  |
| 529 | 3775 | `app/src/search/ai_context_menu/view.rs` | Commands | 命令 |  |
| 531 | 3789 | `app/src/search/ai_context_menu/view.rs` | Workflows | 工作流 |  |
| 539 | 3845 | `app/src/search/ai_context_menu/view.rs` | Terminal | 终端 |  |
| 550 | 3922 | `app/src/search/command_palette/conversations/data_source.rs` | Active pane conversations | 当前窗格对话 |  |
| 551 | 3929 | `app/src/search/command_palette/conversations/data_source.rs` | Other active conversations | 其他活动对话 |  |
| 552 | 3936 | `app/src/search/command_palette/conversations/data_source.rs` | Past conversations | 历史对话 |  |
| 553 | 3943 | `app/src/search/command_palette/conversations/search_item.rs` | New conversation | 新建对话 |  |
| 554 | 3950 | `app/src/search/command_palette/conversations/search_item.rs` | Fork current conversation | 分叉当前对话 |  |
| 555 | 3957 | `app/src/search/command_palette/conversations/search_item.rs` | Fork conversation | 分叉对话 |  |
| 556 | 3964 | `app/src/search/command_palette/conversations/search_item.rs` | Fork current conversation ({title}) | 分叉当前对话（{title}） |  |
| 557 | 3971 | `app/src/search/command_palette/conversations/search_item.rs` | Press enter to navigate to conversation "{}". | 按 Enter 导航到对话“{}”。 |  |
| 558 | 3978 | `app/src/search/command_palette/conversations/search_item.rs` | Press enter to fork the current conversation into a new conversation. | 按 Enter 将当前对话分叉为新对话。 |  |
| 559 | 3985 | `app/src/search/command_palette/conversations/search_item.rs` | Press enter to create a new conversation. | 按 Enter 创建新对话。 |  |
| 560 | 3992 | `app/src/search/command_palette/files/search_item.rs` | Press Enter to navigate to this directory | 按 Enter 导航到此目录 |  |
| 561 | 3999 | `app/src/search/command_palette/files/search_item.rs` | Press Enter to open this file | 按 Enter 打开此文件 |  |
| 562 | 4006 | `app/src/search/command_palette/files/search_item.rs` | Create a file named {}… | 创建名为 {} 的文件… |  |
| 563 | 4013 | `app/src/search/command_palette/files/search_item.rs` | Create file: {} | 创建文件：{} |  |
| 564 | 4020 | `app/src/search/command_palette/files/search_item.rs` | Press Enter to create {} in the current directory | 按 Enter 在当前目录中创建 {} |  |
| 565 | 4027 | `app/src/search/command_palette/launch_config/search_item.rs` | Selected {}. | 已选择 {}。 |  |
| 566 | 4034 | `app/src/search/command_palette/launch_config/search_item.rs` | Press enter to use this launch configuration. | 按 Enter 使用此启动配置。 |  |
| 567 | 4041 | `app/src/search/command_palette/navigation/render.rs` | Current | 当前 |  |
| 568 | 4048 | `app/src/search/command_palette/navigation/render.rs` | Running... | 正在运行... |  |
| 569 | 4055 | `app/src/search/command_palette/navigation/render.rs` | Completed over 1 hour ago | 已完成，超过 1 小时前 |  |
| 570 | 4062 | `app/src/search/command_palette/navigation/render.rs` | Completed {mins} minute ago | 已完成，{mins} 分钟前 |  |
| 571 | 4069 | `app/src/search/command_palette/navigation/render.rs` | Completed {mins} minutes ago | 已完成，{mins} 分钟前 |  |
| 572 | 4076 | `app/src/search/command_palette/navigation/render.rs` | No timestamp found | 未找到时间戳 |  |
| 573 | 4083 | `app/src/search/command_palette/navigation/render.rs` | Completed | 已完成 |  |
| 574 | 4090 | `app/src/search/command_palette/navigation/render.rs` | Empty Session | 空会话 |  |
| 575 | 4097 | `app/src/search/command_palette/navigation/search_item.rs` | Selected {}. {}. | 已选择 {}。{}。 |  |
| 576 | 4104 | `app/src/search/command_palette/navigation/search_item.rs` | Press enter to navigate to this session. | 按 Enter 导航到此会话。 |  |
| 577 | 4111 | `app/src/search/command_palette/new_session/data_source.rs` | Create New Tab | 创建新标签页 |  |
| 578 | 4118 | `app/src/search/command_palette/new_session/data_source.rs` | Create New Window | 创建新窗口 |  |
| 579 | 4125 | `app/src/search/command_palette/new_session/data_source.rs` | Split Pane Down | 向下拆分窗格 |  |
| 580 | 4132 | `app/src/search/command_palette/new_session/data_source.rs` | Split Pane Right | 向右拆分窗格 |  |
| 581 | 4139 | `app/src/search/command_palette/new_session/data_source.rs` | Split Pane Up | 向上拆分窗格 |  |
| 582 | 4146 | `app/src/search/command_palette/new_session/data_source.rs` | Split Pane Left | 向左拆分窗格 |  |
| 583 | 4153 | `app/src/search/command_palette/new_session/new_session_option.rs` | Down | 下 |  |
| 584 | 4160 | `app/src/search/command_palette/new_session/new_session_option.rs` | Right | 右 |  |
| 585 | 4167 | `app/src/search/command_palette/new_session/new_session_option.rs` | Up | 上 |  |
| 586 | 4174 | `app/src/search/command_palette/new_session/new_session_option.rs` | Left | 左 |  |
| 587 | 4181 | `app/src/search/command_palette/new_session/new_session_option.rs` | Create New Tab: {} | 创建新标签页：{} |  |
| 588 | 4188 | `app/src/search/command_palette/new_session/new_session_option.rs` | Create New Window: {} | 创建新窗口：{} |  |
| 589 | 4195 | `app/src/search/command_palette/new_session/new_session_option.rs` | Split Pane {direction}: {} | 向{direction}拆分窗格：{} |  |
| 590 | 4202 | `app/src/search/command_palette/new_session/search_item.rs` | Selected {}. | 已选择 {}。 |  |
| 591 | 4209 | `app/src/search/command_palette/new_session/search_item.rs` | Press enter to launch this session. | 按 Enter 启动此会话。 |  |
| 592 | 4216 | `app/src/search/command_palette/tabs/search_item.rs` | [Tab {}] {} | [标签页 {}] {} |  |
| 593 | 4223 | `app/src/search/command_palette/tabs/search_item.rs` | Selected tab: {}. | 已选择标签页：{}。 |  |
| 594 | 4230 | `app/src/search/command_palette/tabs/search_item.rs` | Press enter to navigate to tab: {}. | 按 Enter 导航到标签页：{}。 |  |
| 595 | 4237 | `app/src/search/command_palette/view.rs` | Search for a command | 搜索命令 |  |
| 596 | 4244 | `app/src/search/command_palette/view.rs` | No results found | 未找到结果 |  |
| 598 | 4258 | `crates/warp_search_core/src/data_source.rs` | Search workflows | 搜索工作流 |  |
| 599 | 4265 | `crates/warp_search_core/src/data_source.rs` | Search prompts | 搜索提示词 |  |
| 610 | 4342 | `crates/warp_search_core/src/data_source.rs` | Search prompt history | 搜索提示词历史 |  |
| 612 | 4356 | `crates/warp_search_core/src/data_source.rs` | Search commands | 搜索命令 |  |
| 618 | 4398 | `crates/warp_search_core/src/data_source.rs` | Search static slash commands | 搜索静态斜杠命令 |  |
| 621 | 4419 | `crates/warp_search_core/src/data_source.rs` | Search full terminal use models | 搜索 Full Terminal Use 模型 |  |
| 624 | 4440 | `crates/warp_search_core/src/data_source.rs` | workflows | 工作流 |  |
| 625 | 4447 | `crates/warp_search_core/src/data_source.rs` | prompts | 提示词 |  |
| 628 | 4468 | `crates/warp_search_core/src/data_source.rs` | AI command suggestions | AI 命令建议 |  |
| 635 | 4517 | `crates/warp_search_core/src/data_source.rs` | prompt history | 提示词历史 |  |
| 637 | 4531 | `crates/warp_search_core/src/data_source.rs` | commands | 命令 |  |
| 643 | 4573 | `crates/warp_search_core/src/data_source.rs` | slash commands | 斜杠命令 |  |
| 646 | 4594 | `crates/warp_search_core/src/data_source.rs` | full terminal use models | Full Terminal Use 模型 |  |
| 648 | 4608 | `app/src/search/command_palette/view.rs` | Cannot switch conversations while agent is monitoring a command. | Agent 正在监控命令时无法切换对话。 |  |
| 649 | 4615 | `app/src/search/command_palette/view.rs` | Cannot start a new conversation while agent is monitoring a command. | Agent 正在监控命令时无法开始新对话。 |  |
| 650 | 4622 | `app/src/search/command_palette/warp_drive/env_var_collection_search_item.rs` | Untitled | 未命名 |  |
| 651 | 4629 | `app/src/search/command_palette/warp_drive/env_var_collection_search_item.rs` | Environment Variables: {} | 环境变量：{} |  |
| 652 | 4636 | `app/src/search/command_palette/warp_drive/notebook_search_item.rs` | Untitled | 未命名 |  |
| ... | ... | ... | ... | ... | 3067 more rows omitted |

## Search, Action, Storage, Protocol Risks

| entry | line | path | source | target | notes |
| ---: | ---: | --- | --- | --- | --- |
| 70 | 490 | `crates/onboarding/src/slides/project_slide.rs` | Prepares the project environment, builds an index of your code, and generates project rules—giving the agent deeper understanding and better | 准备项目环境、建立代码索引并生成项目规则，让 Agent 更深入理解项目并提升表现。 |  |
| 75 | 525 | `app/src/auth/login_slide.rs` | Auth Token | 认证令牌 |  |
| 88 | 647 | `app/src/auth/login_slide.rs` | Click here to paste your token from the browser | 点击此处粘贴浏览器中的令牌 |  |
| 166 | 1206 | `app/src/auth/auth_view_body.rs` | Auth Token | 认证令牌 |  |
| 167 | 1213 | `app/src/auth/auth_view_body.rs` | Browser auth token | 浏览器认证令牌 |  |
| 168 | 1220 | `app/src/auth/auth_view_body.rs` | Click here to paste your token from the browser | 点击此处粘贴浏览器中的令牌 |  |
| 201 | 1451 | `app/src/auth/paste_auth_token_modal.rs` | Paste | 粘贴 | target_count 3 differs from expected_count 1 |
| 202 | 1460 | `app/src/auth/paste_auth_token_modal.rs` | Enter auth token | 输入认证令牌 |  |
| 203 | 1469 | `app/src/auth/paste_auth_token_modal.rs` | Paste your auth token below | 在下方粘贴认证令牌 |  |
| 204 | 1478 | `app/src/auth/paste_auth_token_modal.rs` | Paste your auth token from the browser to get complete login. | 粘贴浏览器中的认证令牌以完成登录。 |  |
| 205 | 1487 | `app/src/auth/paste_auth_token_modal.rs` | Cancel | 取消 |  |
| 206 | 1496 | `app/src/auth/paste_auth_token_modal.rs` | Continue | 继续 |  |
| 217 | 1579 | `app/src/auth/login_failure_notification.rs` | An invalid auth token was entered into the modal. | 输入的认证令牌无效。 |  |
| 218 | 1588 | `app/src/auth/login_failure_notification.rs` | Failed to log in. Try manually copying the auth token from the authentication web page and pasting into the modal. | 登录失败。请尝试从认证网页手动复制认证令牌并粘贴到弹窗中。 |  |
| 226 | 1652 | `app/src/auth/needs_sso_link_view.rs` | Click the button below to link your Warp account to your SSO provider. | 点击下方按钮，将你的 Warp 账号关联到 SSO 提供方。 |  |
| 270 | 1960 | `crates/onboarding/src/slides/agent_slide.rs` |  to paste your token from the browser. | 以粘贴浏览器中的令牌。 |  |
| 340 | 2450 | `app/src/workspace/action.rs` | Creating a team environment variable collection | 正在创建团队环境变量集合 |  |
| 405 | 2905 | `app/src/workspace/view/vertical_tabs.rs` | Environment Variables | 环境变量 |  |
| 406 | 2914 | `app/src/workspace/view/vertical_tabs.rs` | Environments | 环境 |  |
| 468 | 3348 | `app/src/workspace/view.rs` | New API key | 新建 API 密钥 |  |
| 469 | 3355 | `app/src/workspace/view.rs` | Starting cloud environment for this session... | 正在为此会话启动云端环境... |  |
| 508 | 3628 | `app/src/search/action/search_item.rs` | Selected {}, {}. | 已选择 {}，{}。 |  |
| 509 | 3635 | `app/src/search/action/search_item.rs` | Press enter to confirm. | 按 Enter 确认。 |  |
| 510 | 3642 | `app/src/search/action/search_item.rs` | Press enter to confirm. Use {} binding to run this action in the future. | 按 Enter 确认。以后可使用 {} 快捷键运行此操作。 |  |
| 511 | 3649 | `app/src/search/ai_context_menu/blocks/search_item.rs` | Just now | 刚刚 |  |
| 512 | 3656 | `app/src/search/ai_context_menu/blocks/search_item.rs` | {} minutes ago | {} 分钟前 |  |
| 513 | 3663 | `app/src/search/ai_context_menu/blocks/search_item.rs` | {} hours ago | {} 小时前 |  |
| 514 | 3670 | `app/src/search/ai_context_menu/blocks/search_item.rs` | {} days ago | {} 天前 |  |
| 515 | 3677 | `app/src/search/ai_context_menu/blocks/search_item.rs` | No output | 无输出 |  |
| 516 | 3684 | `app/src/search/ai_context_menu/code/data_source.rs` | Code search failed | 代码搜索失败 |  |
| 517 | 3691 | `app/src/search/ai_context_menu/code/search_item.rs` | Code symbol: {} in {}:{} | 代码符号：{}，位于 {}:{} |  |
| 518 | 3698 | `app/src/search/ai_context_menu/diffset/data_source.rs` | uncommitted changes | 未提交的更改 |  |
| 519 | 3705 | `app/src/search/ai_context_menu/diffset/data_source.rs` | changes vs. main branch | 相对 main 分支的更改 |  |
| 520 | 3712 | `app/src/search/ai_context_menu/diffset/search_item.rs` | Uncommitted changes | 未提交的更改 |  |
| 521 | 3719 | `app/src/search/ai_context_menu/diffset/search_item.rs` | Changes vs. main branch | 相对 main 分支的更改 |  |
| 522 | 3726 | `app/src/search/ai_context_menu/diffset/search_item.rs` | Changes vs. {branch} | 相对 {branch} 的更改 |  |
| 523 | 3733 | `app/src/search/ai_context_menu/diffset/search_item.rs` | All uncommitted changes in the working directory | 工作目录中的所有未提交更改 |  |
| 524 | 3740 | `app/src/search/ai_context_menu/diffset/search_item.rs` | All changes compared to the main branch | 与 main 分支相比的所有更改 |  |
| 525 | 3747 | `app/src/search/ai_context_menu/diffset/search_item.rs` | All changes compared to {branch} | 与 {branch} 相比的所有更改 |  |
| 526 | 3754 | `app/src/search/ai_context_menu/notebooks/search_item.rs` | Untitled | 未命名 |  |
| 527 | 3761 | `app/src/search/ai_context_menu/rules/search_item.rs` | Rule | 规则 |  |
| 528 | 3768 | `app/src/search/ai_context_menu/view.rs` | Files and folders | 文件和文件夹 |  |
| 529 | 3775 | `app/src/search/ai_context_menu/view.rs` | Commands | 命令 |  |
| 530 | 3782 | `app/src/search/ai_context_menu/view.rs` | Blocks | 块 |  |
| 531 | 3789 | `app/src/search/ai_context_menu/view.rs` | Workflows | 工作流 |  |
| 532 | 3796 | `app/src/search/ai_context_menu/view.rs` | Notebooks | 笔记本 |  |
| 533 | 3803 | `app/src/search/ai_context_menu/view.rs` | Plans | 计划 |  |
| 534 | 3810 | `app/src/search/ai_context_menu/view.rs` | Diffs | 差异 |  |
| 535 | 3817 | `app/src/search/ai_context_menu/view.rs` | Docs | 文档 |  |
| 536 | 3824 | `app/src/search/ai_context_menu/view.rs` | Past tasks | 历史任务 |  |
| 537 | 3831 | `app/src/search/ai_context_menu/view.rs` | Rules | 规则 |  |
| 538 | 3838 | `app/src/search/ai_context_menu/view.rs` | Servers and integrations | 服务器和集成 |  |
| 539 | 3845 | `app/src/search/ai_context_menu/view.rs` | Terminal | 终端 |  |
| 540 | 3852 | `app/src/search/ai_context_menu/view.rs` | Web | 网页 |  |
| 541 | 3859 | `app/src/search/ai_context_menu/view.rs` | Most recent diff | 最近的差异 |  |
| 542 | 3866 | `app/src/search/ai_context_menu/view.rs` | Most recent block | 最近的块 |  |
| 543 | 3873 | `app/src/search/ai_context_menu/view.rs` | Code | 代码 |  |
| 544 | 3880 | `app/src/search/ai_context_menu/view.rs` | Diff sets | 差异集 |  |
| 545 | 3887 | `app/src/search/ai_context_menu/view.rs` | Conversations | 对话 |  |
| 546 | 3894 | `app/src/search/ai_context_menu/view.rs` | Skills | 技能 |  |
| 547 | 3901 | `app/src/search/ai_context_menu/view.rs` | No results found | 未找到结果 |  |
| 548 | 3908 | `app/src/search/ai_context_menu/view.rs` | Loading results... | 正在加载结果... |  |
| 549 | 3915 | `app/src/search/ai_context_menu/view.rs` | Code symbols indexing... | 正在索引代码符号... |  |
| 550 | 3922 | `app/src/search/command_palette/conversations/data_source.rs` | Active pane conversations | 当前窗格对话 |  |
| 551 | 3929 | `app/src/search/command_palette/conversations/data_source.rs` | Other active conversations | 其他活动对话 |  |
| 552 | 3936 | `app/src/search/command_palette/conversations/data_source.rs` | Past conversations | 历史对话 |  |
| 553 | 3943 | `app/src/search/command_palette/conversations/search_item.rs` | New conversation | 新建对话 |  |
| 554 | 3950 | `app/src/search/command_palette/conversations/search_item.rs` | Fork current conversation | 分叉当前对话 |  |
| 555 | 3957 | `app/src/search/command_palette/conversations/search_item.rs` | Fork conversation | 分叉对话 |  |
| 556 | 3964 | `app/src/search/command_palette/conversations/search_item.rs` | Fork current conversation ({title}) | 分叉当前对话（{title}） |  |
| 557 | 3971 | `app/src/search/command_palette/conversations/search_item.rs` | Press enter to navigate to conversation "{}". | 按 Enter 导航到对话“{}”。 |  |
| 558 | 3978 | `app/src/search/command_palette/conversations/search_item.rs` | Press enter to fork the current conversation into a new conversation. | 按 Enter 将当前对话分叉为新对话。 |  |
| 559 | 3985 | `app/src/search/command_palette/conversations/search_item.rs` | Press enter to create a new conversation. | 按 Enter 创建新对话。 |  |
| 560 | 3992 | `app/src/search/command_palette/files/search_item.rs` | Press Enter to navigate to this directory | 按 Enter 导航到此目录 |  |
| 561 | 3999 | `app/src/search/command_palette/files/search_item.rs` | Press Enter to open this file | 按 Enter 打开此文件 |  |
| 562 | 4006 | `app/src/search/command_palette/files/search_item.rs` | Create a file named {}… | 创建名为 {} 的文件… |  |
| 563 | 4013 | `app/src/search/command_palette/files/search_item.rs` | Create file: {} | 创建文件：{} |  |
| 564 | 4020 | `app/src/search/command_palette/files/search_item.rs` | Press Enter to create {} in the current directory | 按 Enter 在当前目录中创建 {} |  |
| 565 | 4027 | `app/src/search/command_palette/launch_config/search_item.rs` | Selected {}. | 已选择 {}。 |  |
| 566 | 4034 | `app/src/search/command_palette/launch_config/search_item.rs` | Press enter to use this launch configuration. | 按 Enter 使用此启动配置。 |  |
| 567 | 4041 | `app/src/search/command_palette/navigation/render.rs` | Current | 当前 |  |
| 568 | 4048 | `app/src/search/command_palette/navigation/render.rs` | Running... | 正在运行... |  |
| 569 | 4055 | `app/src/search/command_palette/navigation/render.rs` | Completed over 1 hour ago | 已完成，超过 1 小时前 |  |
| 570 | 4062 | `app/src/search/command_palette/navigation/render.rs` | Completed {mins} minute ago | 已完成，{mins} 分钟前 |  |
| 571 | 4069 | `app/src/search/command_palette/navigation/render.rs` | Completed {mins} minutes ago | 已完成，{mins} 分钟前 |  |
| 572 | 4076 | `app/src/search/command_palette/navigation/render.rs` | No timestamp found | 未找到时间戳 |  |
| 573 | 4083 | `app/src/search/command_palette/navigation/render.rs` | Completed | 已完成 |  |
| 574 | 4090 | `app/src/search/command_palette/navigation/render.rs` | Empty Session | 空会话 |  |
| 575 | 4097 | `app/src/search/command_palette/navigation/search_item.rs` | Selected {}. {}. | 已选择 {}。{}。 |  |
| 576 | 4104 | `app/src/search/command_palette/navigation/search_item.rs` | Press enter to navigate to this session. | 按 Enter 导航到此会话。 |  |
| 577 | 4111 | `app/src/search/command_palette/new_session/data_source.rs` | Create New Tab | 创建新标签页 |  |
| 578 | 4118 | `app/src/search/command_palette/new_session/data_source.rs` | Create New Window | 创建新窗口 |  |
| 579 | 4125 | `app/src/search/command_palette/new_session/data_source.rs` | Split Pane Down | 向下拆分窗格 |  |
| 580 | 4132 | `app/src/search/command_palette/new_session/data_source.rs` | Split Pane Right | 向右拆分窗格 |  |
| 581 | 4139 | `app/src/search/command_palette/new_session/data_source.rs` | Split Pane Up | 向上拆分窗格 |  |
| 582 | 4146 | `app/src/search/command_palette/new_session/data_source.rs` | Split Pane Left | 向左拆分窗格 |  |
| 583 | 4153 | `app/src/search/command_palette/new_session/new_session_option.rs` | Down | 下 |  |
| 584 | 4160 | `app/src/search/command_palette/new_session/new_session_option.rs` | Right | 右 |  |
| 585 | 4167 | `app/src/search/command_palette/new_session/new_session_option.rs` | Up | 上 |  |
| 586 | 4174 | `app/src/search/command_palette/new_session/new_session_option.rs` | Left | 左 |  |
| 587 | 4181 | `app/src/search/command_palette/new_session/new_session_option.rs` | Create New Tab: {} | 创建新标签页：{} |  |
| 588 | 4188 | `app/src/search/command_palette/new_session/new_session_option.rs` | Create New Window: {} | 创建新窗口：{} |  |
| 589 | 4195 | `app/src/search/command_palette/new_session/new_session_option.rs` | Split Pane {direction}: {} | 向{direction}拆分窗格：{} |  |
| 590 | 4202 | `app/src/search/command_palette/new_session/search_item.rs` | Selected {}. | 已选择 {}。 |  |
| 591 | 4209 | `app/src/search/command_palette/new_session/search_item.rs` | Press enter to launch this session. | 按 Enter 启动此会话。 |  |
| 592 | 4216 | `app/src/search/command_palette/tabs/search_item.rs` | [Tab {}] {} | [标签页 {}] {} |  |
| 593 | 4223 | `app/src/search/command_palette/tabs/search_item.rs` | Selected tab: {}. | 已选择标签页：{}。 |  |
| 594 | 4230 | `app/src/search/command_palette/tabs/search_item.rs` | Press enter to navigate to tab: {}. | 按 Enter 导航到标签页：{}。 |  |
| 595 | 4237 | `app/src/search/command_palette/view.rs` | Search for a command | 搜索命令 |  |
| 596 | 4244 | `app/src/search/command_palette/view.rs` | No results found | 未找到结果 |  |
| 609 | 4335 | `crates/warp_search_core/src/data_source.rs` | Search environment variables | 搜索环境变量 |  |
| 634 | 4510 | `crates/warp_search_core/src/data_source.rs` | environment variables | 环境变量 |  |
| 648 | 4608 | `app/src/search/command_palette/view.rs` | Cannot switch conversations while agent is monitoring a command. | Agent 正在监控命令时无法切换对话。 |  |
| 649 | 4615 | `app/src/search/command_palette/view.rs` | Cannot start a new conversation while agent is monitoring a command. | Agent 正在监控命令时无法开始新对话。 |  |
| 650 | 4622 | `app/src/search/command_palette/warp_drive/env_var_collection_search_item.rs` | Untitled | 未命名 |  |
| 651 | 4629 | `app/src/search/command_palette/warp_drive/env_var_collection_search_item.rs` | Environment Variables: {} | 环境变量：{} |  |
| 652 | 4636 | `app/src/search/command_palette/warp_drive/notebook_search_item.rs` | Untitled | 未命名 |  |
| 653 | 4643 | `app/src/search/command_palette/zero_state/items.rs` | Recent | 最近 |  |
| 654 | 4650 | `app/src/search/command_palette/zero_state/items.rs` | Suggested | 建议 |  |
| 655 | 4657 | `app/src/search/command_search/ai_queries/ai_queries_search_item.rs` | Ran {} | 已运行 {} |  |
| ... | ... | ... | ... | ... | 1221 more rows omitted |

## Public-RC Evidence Gated

| entry | line | path | source | target | notes |
| ---: | ---: | --- | --- | --- | --- |
| 41 | 287 | `crates/onboarding/src/slides/agent_slide.rs` | Can plan, read files, and execute low-risk commands. Asks before making any changes or executing sensitive commands. | 可以规划、读取文件并执行低风险命令；修改文件或执行敏感命令前会请求确认。 |  |
| 46 | 322 | `crates/onboarding/src/slides/agent_slide.rs` | State-of-the-art models require paid plans. | 前沿模型需要付费计划。 |  |
| 75 | 525 | `app/src/auth/login_slide.rs` | Auth Token | 认证令牌 |  |
| 76 | 534 | `app/src/auth/login_slide.rs` | Get started with Warp Drive | 开始使用 Warp Drive |  |
| 77 | 544 | `app/src/auth/login_slide.rs` | Get started with AI | 开始使用 AI |  |
| 78 | 554 | `app/src/auth/login_slide.rs` | Connect your account to save and share notebooks, workflows, and more across devices. | 连接账号以在多台设备间保存和共享笔记本、工作流等内容。 |  |
| 79 | 563 | `app/src/auth/login_slide.rs` | Connect your account to enable AI-powered planning, coding, and automation. | 连接账号以启用 AI 驱动的规划、编码和自动化。 |  |
| 80 | 573 | `app/src/auth/login_slide.rs` | By continuing, you agree to Warp's  | 继续即表示你同意 Warp 的 |  |
| 81 | 582 | `app/src/auth/login_slide.rs` | Terms of Service | 服务条款 |  |
| 82 | 591 | `app/src/auth/login_slide.rs` | Privacy Settings | 隐私设置 | target_count 4 differs from expected_count 2 |
| 83 | 600 | `app/src/auth/login_slide.rs` | Back | 返回 | target_count 4 differs from expected_count 3 |
| 84 | 609 | `app/src/auth/login_slide.rs` | Disable Warp Drive | 禁用 Warp Drive | target_count 2 differs from expected_count 1 |
| 85 | 619 | `app/src/auth/login_slide.rs` | Disable AI features | 禁用 AI 功能 | target_count 2 differs from expected_count 1 |
| 86 | 629 | `app/src/auth/login_slide.rs` | Continue | 继续 | target_count 5 differs from expected_count 1 |
| 87 | 638 | `app/src/auth/login_slide.rs` | Sign in on your browser to continue | 在浏览器中登录以继续 |  |
| 88 | 647 | `app/src/auth/login_slide.rs` | Click here to paste your token from the browser | 点击此处粘贴浏览器中的令牌 |  |
| 89 | 656 | `app/src/auth/login_slide.rs` | Are you sure you want to disable Warp Drive? | 确定要禁用 Warp Drive 吗？ |  |
| 90 | 663 | `app/src/auth/login_slide.rs` | Are you sure you want to disable AI features? | 确定要禁用 AI 功能吗？ |  |
| 91 | 670 | `app/src/auth/login_slide.rs` | Warp Drive lets you save workflows and knowledge across devices and share them with your team. By continuing, you won't have access to the f | Warp Drive 可让你跨设备保存工作流和知识，并与团队共享。继续后，你将无法使用以下功能： |  |
| 92 | 677 | `app/src/auth/login_slide.rs` | Warp is better with AI. By continuing, you won't have access to any of the following features: | Warp 配合 AI 会更强。继续后，你将无法使用以下功能： |  |
| 93 | 684 | `app/src/auth/login_slide.rs` | Enable Warp Drive | 启用 Warp Drive |  |
| 94 | 691 | `app/src/auth/login_slide.rs` | Enable AI features | 启用 AI 功能 |  |
| 95 | 698 | `app/src/auth/login_slide.rs` | Skip for now | 暂时跳过 |  |
| 125 | 919 | `crates/onboarding/src/slides/free_user_no_ai_slide.rs` | Iterate, plan, and build with Oz: Warp's built-in agent. Available locally or in the cloud. | 使用 Oz（Warp 内置 Agent）迭代、规划和构建，可在本地或云端运行。 |  |
| 134 | 982 | `crates/onboarding/src/slides/free_user_no_ai_slide.rs` | 1,500 credits per month | 每月 1,500 点额度 |  |
| 136 | 996 | `crates/onboarding/src/slides/free_user_no_ai_slide.rs` | Access to Reload credits and volume-based discounts | 可使用 Reload 额度和阶梯折扣 |  |
| 160 | 1164 | `app/src/auth/login_slide.rs` | If you'd like to opt out of analytics and AI features, you can adjust your  | 如需停用分析和 AI 功能，你可以调整 |  |
| 161 | 1171 | `app/src/auth/login_slide.rs` | If you'd like to opt out of analytics, you can adjust your  | 如需停用分析，你可以调整 |  |
| 162 | 1178 | `app/src/auth/login_slide.rs` | If your browser hasn't launched,  | 如果浏览器没有打开， |  |
| 163 | 1185 | `app/src/auth/login_slide.rs` | copy the URL | 复制 URL |  |
| 164 | 1192 | `app/src/auth/login_slide.rs` |  and open |  并手动打开 |  |
| 165 | 1199 | `app/src/auth/login_slide.rs` | the page manually. | 该页面。 |  |
| 166 | 1206 | `app/src/auth/auth_view_body.rs` | Auth Token | 认证令牌 |  |
| 167 | 1213 | `app/src/auth/auth_view_body.rs` | Browser auth token | 浏览器认证令牌 |  |
| 168 | 1220 | `app/src/auth/auth_view_body.rs` | Click here to paste your token from the browser | 点击此处粘贴浏览器中的令牌 |  |
| 179 | 1297 | `app/src/auth/auth_view_body.rs` | Are you sure you want to skip login? | 确定要跳过登录吗？ |  |
| 182 | 1318 | `app/src/auth/auth_view_body.rs` | Yes, skip login | 是，跳过登录 |  |
| 201 | 1451 | `app/src/auth/paste_auth_token_modal.rs` | Paste | 粘贴 | target_count 3 differs from expected_count 1 |
| 202 | 1460 | `app/src/auth/paste_auth_token_modal.rs` | Enter auth token | 输入认证令牌 |  |
| 203 | 1469 | `app/src/auth/paste_auth_token_modal.rs` | Paste your auth token below | 在下方粘贴认证令牌 |  |
| 204 | 1478 | `app/src/auth/paste_auth_token_modal.rs` | Paste your auth token from the browser to get complete login. | 粘贴浏览器中的认证令牌以完成登录。 |  |
| 205 | 1487 | `app/src/auth/paste_auth_token_modal.rs` | Cancel | 取消 |  |
| 206 | 1496 | `app/src/auth/paste_auth_token_modal.rs` | Continue | 继续 |  |
| 209 | 1519 | `app/src/auth/auth_override_warning_body.rs` | New login detected | 检测到新的登录 |  |
| 215 | 1561 | `app/src/auth/login_failure_notification.rs` |  Not the first time? See our  |  不是第一次遇到？查看我们的 |  |
| 216 | 1570 | `app/src/auth/login_failure_notification.rs` | troubleshooting docs | 故障排查文档 |  |
| 217 | 1579 | `app/src/auth/login_failure_notification.rs` | An invalid auth token was entered into the modal. | 输入的认证令牌无效。 |  |
| 218 | 1588 | `app/src/auth/login_failure_notification.rs` | Failed to log in. Try manually copying the auth token from the authentication web page and pasting into the modal. | 登录失败。请尝试从认证网页手动复制认证令牌并粘贴到弹窗中。 |  |
| 219 | 1597 | `app/src/auth/login_failure_notification.rs` | Request to log in failed. | 登录请求失败。 |  |
| 220 | 1606 | `app/src/auth/login_failure_notification.rs` | Request to sign up failed. | 注册请求失败。 |  |
| 221 | 1615 | `app/src/auth/login_failure_notification.rs` | The redirect URL pasted did not originate from this app. Please click the button below to try again. | 粘贴的重定向 URL 并非来自此应用。请点击下方按钮重试。 |  |
| 239 | 1743 | `app/src/auth/login_slide.rs` | Paste | 粘贴 |  |
| 241 | 1757 | `app/src/auth/auth_override_warning_body.rs` | Warp has detected a new login from a web browser. Press escape to cancel and continue using Warp without login. | Warp 检测到来自浏览器的新登录。按 Esc 可取消并继续以未登录状态使用 Warp。 |  |
| 270 | 1960 | `crates/onboarding/src/slides/agent_slide.rs` |  to paste your token from the browser. | 以粘贴浏览器中的令牌。 |  |
| 271 | 1967 | `crates/onboarding/src/slides/agent_slide.rs` | Plan successfully activated. All premium models are available. | 计划已成功激活。所有高级模型现已可用。 |  |
| 344 | 2478 | `app/src/workspace/bonus_grant_notification_model.rs` | {} Reload Credits have been added to your {}. | {} 点 Reload 额度已添加到你的 {}。 |  |
| 408 | 2928 | `app/src/workspace/view/vertical_tabs.rs` | Plan | 计划 |  |
| 455 | 3257 | `app/src/workspace/view.rs` | Billing and usage | 账单和用量 |  |
| 459 | 3285 | `app/src/workspace/view.rs` | Looks like you're out of AI credits. | 看起来你的 AI 额度已用完。 |  |
| 460 | 3292 | `app/src/workspace/view.rs` | Upgrade for more credits. | 升级以获取更多额度。 |  |
| 468 | 3348 | `app/src/workspace/view.rs` | New API key | 新建 API 密钥 |  |
| 480 | 3432 | `app/src/workspace/view.rs` | This plan is already in context. | 此计划已在上下文中。 |  |
| 485 | 3467 | `app/src/workspace/view.rs` | Plan synced to your Warp Drive | 计划已同步到你的 Warp Drive |  |
| 502 | 3586 | `app/src/workspace/view.rs` | Your login has expired. | 你的登录已过期。 |  |
| 533 | 3803 | `app/src/search/ai_context_menu/view.rs` | Plans | 计划 |  |
| 601 | 4279 | `crates/warp_search_core/src/data_source.rs` | Search plans | 搜索计划 |  |
| 627 | 4461 | `crates/warp_search_core/src/data_source.rs` | plans | 计划 |  |
| 667 | 4741 | `app/src/search/command_search/view.rs` | Looks like you're out of credits. Contact a team admin to upgrade for more credits. | 看起来你的额度已用完。请联系团队管理员升级以获取更多额度。 |  |
| 669 | 4755 | `app/src/search/command_search/view.rs` | Looks like you're out of credits.  | 看起来你的额度已用完。 |  |
| 670 | 4762 | `app/src/search/command_search/view.rs` |  for more credits. | 以获取更多额度。 |  |
| 680 | 4832 | `app/src/search/command_search/warp_ai.rs` | Looks like you're out of AI credits. Please try again later. | 看起来你的 AI 额度已用完。请稍后重试。 |  |
| 685 | 4867 | `app/src/search/external_secrets/view.rs` | Search for a secret | 搜索密钥 |  |
| 686 | 4874 | `app/src/search/external_secrets/view.rs` | No results found. | 未找到结果。 |  |
| 735 | 5217 | `app/src/search/slash_command_menu/static_commands/commands.rs` | Prompt the agent to do some research and create a plan for a task | 让 Agent 先做研究并为任务创建计划 |  |
| 748 | 5308 | `app/src/search/slash_command_menu/static_commands/commands.rs` | Open billing and usage settings | 打开账单和用量设置 |  |
| 750 | 5322 | `app/src/search/slash_command_menu/static_commands/commands.rs` | Toggle credit usage details | 切换额度使用详情 |  |
| 861 | 6107 | `app/src/workspace/mod.rs` | Copy access token to clipboard | 将访问令牌复制到剪贴板 |  |
| 885 | 6286 | `app/src/workspace/mod.rs` | Open Settings: Billing and usage | 打开设置：账单和用量 |  |
| 931 | 6610 | `app/src/settings_view/main_page.rs` | Upgrade Plan | 升级套餐 |  |
| 932 | 6617 | `app/src/settings_view/main_page.rs` | Generate Stripe Billing Portal Link | 生成 Stripe 账单门户链接 |  |
| 937 | 6652 | `app/src/settings_view/main_page.rs` | Compare plans | 比较套餐 |  |
| 939 | 6666 | `app/src/settings_view/main_page.rs` | Manage billing | 管理账单 |  |
| 940 | 6673 | `app/src/settings_view/main_page.rs` | Upgrade to Turbo plan | 升级到 Turbo 套餐 |  |
| 941 | 6680 | `app/src/settings_view/main_page.rs` | Upgrade to Lightspeed plan | 升级到 Lightspeed 套餐 |  |
| 1100 | 7793 | `app/src/settings_view/features_page.rs` | Start Warp at login (requires macOS 13+) | 登录时启动 Warp（需要 macOS 13+） |  |
| 1101 | 7800 | `app/src/settings_view/features_page.rs` | Start Warp at login | 登录时启动 Warp |  |
| 1176 | 8325 | `app/src/settings_view/privacy_page.rs` | Secret redaction | 敏感信息遮盖 |  |
| 1178 | 8339 | `app/src/settings_view/privacy_page.rs` | Custom secret redaction | 自定义敏感信息遮盖 |  |
| 1179 | 8346 | `app/src/settings_view/privacy_page.rs` | Use regex to define additional secrets or data you'd like to redact. This will take effect when the next command runs. You can use the inlin | 使用正则表达式定义更多要遮盖的敏感信息或数据。此设置会在下一条命令运行时生效。你可以在正则前加内联 (?i) 标记，使其不区分大小写。 |  |
| 1192 | 8437 | `app/src/settings_view/privacy_page.rs` | Enterprise secret redaction cannot be modified. | 无法修改企业敏感信息遮盖。 |  |
| 1197 | 8472 | `app/src/settings_view/privacy_page.rs` | Secret visual redaction mode | 敏感信息视觉遮盖模式 |  |
| 1198 | 8479 | `app/src/settings_view/privacy_page.rs` | Choose how secrets are visually presented in the block list while keeping them searchable. This setting only affects what you see in the blo | 选择敏感信息在块列表中的视觉呈现方式，同时保持可搜索。此设置只影响你在块列表中看到的内容。 |  |
| 1213 | 8584 | `app/src/settings_view/privacy_page.rs` | secret redaction | 敏感信息遮盖 |  |
| 1264 | 8941 | `app/src/settings_view/ai_page.rs` | Warp credit fallback | Warp 额度兜底 |  |
| 1298 | 9179 | `app/src/settings_view/ai_page.rs` | Restricted due to billing issue | 因账单问题受限 |  |
| 1302 | 9207 | `app/src/settings_view/ai_page.rs` | This is the {} limit of AI credits for your account. | 这是你账号 AI 额度的{}限制。 |  |
| 1303 | 9214 | `app/src/settings_view/ai_page.rs` | Credits | 额度 |  |
| 1306 | 9235 | `app/src/settings_view/ai_page.rs` | Compare plans | 比较套餐 |  |
| 1317 | 9312 | `app/src/settings_view/ai_page.rs` | Profiles let you define how your Agent operates — from the actions it can take and when it needs approval, to the models it uses for tasks l | 配置档可定义 Agent 的运行方式，包括它可以执行的操作、何时需要批准，以及执行编码和规划等任务时使用的模型。你也可以将其限定到单个项目。 |  |
| 1319 | 9326 | `app/src/settings_view/ai_page.rs` | Context window (tokens) | 上下文窗口（tokens） |  |
| 1334 | 9431 | `app/src/settings_view/ai_page.rs` | This model serves as the primary engine behind the Warp Agent. It powers most interactions and invokes other models for tasks like planning  | 此模型是 Warp Agent 的主要引擎，负责大多数交互，并在需要时调用其他模型完成规划或代码生成等任务。Warp 可能会根据模型可用性，或在对话摘要等辅助任务中自动切换到其他模型。 |  |
| 1403 | 9914 | `app/src/settings_view/ai_page.rs` | OpenAI API key | OpenAI API 密钥 |  |
| 1404 | 9921 | `app/src/settings_view/ai_page.rs` | Anthropic API key | Anthropic API 密钥 |  |
| 1405 | 9928 | `app/src/settings_view/ai_page.rs` | Google API key | Google API 密钥 |  |
| 1406 | 9935 | `app/src/settings_view/ai_page.rs` | Use your own API keys from model providers for Warp Agent. You can also add custom endpoints to use third-party models. Custom endpoints mus | 为 Warp Agent 使用你自己的模型提供商 API 密钥。你也可以添加自定义端点来使用第三方模型。自定义端点必须支持 OpenAI 兼容的 Chat Completions API。API 密钥只存储在你的设备上，绝不会存储在 Warp 服务器上。它们用于向你选择的模型提供 |  |
| 1410 | 9963 | `app/src/settings_view/ai_page.rs` | When enabled, agent requests may be routed to one of Warp's provided models in the event of an error. Warp will prioritize using your API ke | 启用后，如果发生错误，Agent 请求可能会路由到 Warp 提供的模型之一。Warp 会优先使用你的 API 密钥，而不是 Warp 额度。 |  |
| 1411 | 9970 | `app/src/settings_view/ai_page.rs` | Custom inference | 自定义推理 |  |
| 1412 | 9977 | `app/src/settings_view/ai_page.rs` | API Keys | API 密钥 |  |
| 1425 | 10068 | `app/src/settings_view/code_page.rs` | You have reached the maximum number of codebase indices for your plan. Delete existing indices to auto-index new codebases. | 你已达到当前套餐的代码库索引数量上限。请删除现有索引以自动索引新的代码库。 |  |
| 1484 | 10481 | `app/src/settings_view/execution_profile_view.rs` | Auto-sync plans to Warp Drive: | 自动同步计划到 Warp Drive： |  |
| 1524 | 10761 | `app/src/settings_view/mcp_servers/edit_page.rs` | This MCP server contains secrets. Visit Settings > Privacy to modify your secret redaction settings. | 此 MCP 服务器包含密钥。请前往“设置 > 隐私”修改密钥遮盖设置。 |  |
| 1588 | 11209 | `app/src/settings_view/environments_page.rs` | Environment deleted successfully | 环境已成功删除 |  |
| 1638 | 11559 | `app/src/settings_view/update_environment_form.rs` | Delete environment | 删除环境 |  |
| 1646 | 11615 | `app/src/settings_view/update_environment_form.rs` | Personal environments cannot be used with external integrations or team API keys. For the best experience, use shared environments. | 个人环境不能与外部集成或团队 API 密钥一起使用。为获得最佳体验，请使用共享环境。 |  |
| 1668 | 11769 | `app/src/settings_view/platform_page.rs` | Search API keys | 搜索 API 密钥 |  |
| 1669 | 11776 | `app/src/settings_view/platform_page.rs` | New API key | 新建 API 密钥 |  |
| 1671 | 11790 | `app/src/settings_view/platform_page.rs` | API key deleted | API 密钥已删除 |  |
| 1673 | 11804 | `app/src/settings_view/platform_page.rs` | Oz Cloud API Keys | Oz Cloud API 密钥 |  |
| 1674 | 11811 | `app/src/settings_view/platform_page.rs` | + Create API Key | + 创建 API 密钥 |  |
| 1685 | 11888 | `app/src/settings_view/platform_page.rs` | No API Keys | 没有 API 密钥 |  |
| ... | ... | ... | ... | ... | 910 more rows omitted |
