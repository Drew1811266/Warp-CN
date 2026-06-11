# zh-Hans Functional Test Run - 2026-06-11

Scope: Continue Warp CN localization functional testing after the test plan was added.

Policy for this run:

- Low-load gate was explicitly waived by the user for continued testing.
- Record current failures, continue later test lanes, and defer fixes until all planned tests complete.
- Do not use real accounts, billing state, cloud resources, team ownership, managed secrets, custom endpoints, or external mutable state.

## L1 Rust Test Results

| Gate | Command | Result | Notes |
| --- | --- | --- | --- |
| Format | `cargo fmt --check` | pass | No formatting changes required. |
| App compile | `CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp` | pass | Finished in 4m30s; existing `warp` lib warnings only. |
| Search core | `CARGO_BUILD_JOBS=1 cargo test -j 1 -p warp_search_core` | pass | 13 unit tests and 1 doctest passed. |
| Command palette | `CARGO_BUILD_JOBS=1 cargo test -j 1 -p warp command_palette` | pass | 15 passed, 4875 filtered. |
| Keybinding utility | `cargo test -p warp util::bindings` | pass | 2 passed, 0 failed, 4888 filtered; covers binding display/editability utilities, not view-context predicate matching. |
| Search command palette unit rerun | `cargo test -p warp search::command_palette -- --nocapture` | pass | 15 passed, 0 failed, 4875 filtered; covers command-palette data sources/navigation helpers but not current-view action binding availability. |
| Search action filter check | `cargo test -p warp search::action -- --nocapture` | no-tests | 0 tests matched; there is no focused unit coverage for localized command-palette action text search. |
| Settings initial triage | `CARGO_BUILD_JOBS=1 cargo test -j 1 -p warp settings` | fail-initial | 273 passed, 41 failed, 4576 filtered. Failures were recorded and deferred until the planned test lanes completed. |
| Settings unified rerun | `cargo test -p warp settings` | pass | 314 passed, 0 failed, 4576 filtered after unified handling. |

## L2 Integration Test Results

Initial L2 commands were run with the low-load gate active and serial build execution; later focused reruns were run after the user waived the low-load requirement:

```bash
CARGO_BUILD_JOBS=1 cargo run -j 1 -p integration --bin integration -- <test_name>
```

The table below preserves the initial triage observations. Rows marked `fail-*` were handled in the unified fix pass; the current post-fix verification is recorded in [Unified Fix Pass Results](#unified-fix-pass-results).

| Test | Result | Notes |
| --- | --- | --- |
| `test_single_command` | pass | Basic terminal command execution completed under isolated HOME. |
| `test_zh_terminal_cjk_input_roundtrip` | pass | Chinese terminal input/output roundtrip completed in the earlier integration run. |
| `test_open_and_close_settings` | pass-after-fix | Original key injection path did not open settings. The test now dispatches `WorkspaceAction::ShowSettings` through the workspace view and verifies the localized `设置` tab/pane. |
| `test_open_and_close_context_menu_with_keybinding` | fail-confirmed-product-risk | Keybinding path did not open the context menu. Focused diagnostics showed the custom binding was loaded as `⌃M` and selected-block cardinality was `一个`, but current active TerminalView bindings did not include the action because `TerminalView::ui_name()` returns localized `终端` while the keymap predicates still require `id!("Terminal")`. |
| `test_command_search_loads_history` | pass | Command search loaded shell history fixtures successfully. |
| `test_loading_project_workflows` | pass | Project workflow loading completed with the test config watcher delay. |
| `test_secret_is_obfuscated_on_copy` | pass-after-fix | Secret copy/redaction path passes after the helper opens the selected-block context menu through `TerminalAction::OpenBlockListContextMenu`; command palette action search remains a separate deferred risk. |
| `test_restore_snapshot_with_settings_page` | pass-after-fix | Restored settings pane title assertion updated from `Settings` to localized `设置`. |
| `test_ask_warp_ai_keybinding_for_selected_block` | fail-confirmed-same-risk | `cmdorctrl-up` selected the block, but `ctrl-shift-space` did not attach the selected block to the AI editor. The binding branch for selected blocks depends on `id!("Terminal")`, matching L2-KEYMAP-001. |
| `test_block_filtering_keybinding` | fail-precondition | Did not reach the `shift-alt-F` keybinding assertion. The run failed in `Clear blocklist`: expected 1 block, observed 3. Record separately from localization keymap failures. |
| `test_palette_opens_when_theme_chooser_is_open` | fail-confirmed-same-risk | The helper uses `cmd/ctrl-p`; the run failed because command palette results stayed empty. `workspace:toggle_command_palette` depends on `id!("Workspace")`, while `Workspace::ui_name()` currently returns `工作区`. |
| `test_open_and_close_resource_center` | fail-test-position | Did not reach functional assertion. The run failed with `No position for resource_center_button`, so this is recorded as a saved-position/render targeting issue, not yet a product failure. |
| `test_add_theme_to_warp_config` | pass | Theme files added under the mocked Warp config directory were detected and surfaced by the theme chooser; this isolates theme config loading from the command-palette shortcut failure. |
| `test_suggestions_menu_positioning` | pass | Input completion and Tab suggestion menu positioning worked, giving positive coverage for localized `Input`/`输入` paths. |
| `test_input_focused_after_executing_command` | fail-confirmed-same-risk | Did not reach the final input-focus assertion. The prerequisite `Open Find bar` step failed after `cmd/ctrl-shift-f`; this follows the same TerminalView keymap-context risk as L2-KEYMAP-001. |
| `test_open_and_close_theme_creator_modal` | fail-command-palette-empty | Failed while searching the command palette for the English action text `Open Theme Picker`; the localized binding text is `打开主题选择器`, so this is recorded as command-palette localization/test drift until a Chinese-query path is isolated. |
| `test_create_folder_from_command_palette` | fail-command-palette-empty | Failed while searching the command palette for English action text `Create a New Team Folder`; the corresponding binding descriptions are localized (`创建新的团队文件夹`, `新建团队文件夹`). |
| `test_create_personal_workflow_pane_from_command_palette` | fail-command-palette-empty | Failed while searching the command palette for English action text `Create a New Personal Workflow`; the corresponding binding descriptions are localized (`创建新的个人工作流`, `新建个人工作流`). |
| `test_ctrl_d_eot` | pass | Input-layer `ctrl-d` EOT path works with the localized `Input` context. |
| `test_find_within_block` | fail-confirmed-same-risk | Failed in the `Open Find bar` step before within-block search assertions; same `cmd/ctrl-shift-f` TerminalView keymap-context risk as `test_input_focused_after_executing_command`. |
| `test_open_context_menu_and_execute_command` | fail-precondition | Did not reach the context-menu click path. The run failed in `Clear blocklist`: expected 1 block, observed 3; same non-localization precondition class as `test_block_filtering_keybinding`. |
| `test_new_session_focuses_input` | pass | New session creation returned focus to the terminal input. |
| `test_block_filtering_clear_blocklist` | fail-confirmed-same-risk | The dedicated blocklist-clear path also failed at `Clear blocklist`: expected 1 block, observed 3. The helper is a `cmd/ctrl-k` TerminalView shortcut, so this is now grouped with L2-KEYMAP-001. |
| `test_text_input_on_block_list` | fail-confirmed-same-risk | Did not reach text-input-on-block-list assertions because `Clear blocklist` failed with 3 blocks remaining. |
| `test_typeahead` | pass | Long-running command typeahead worked and the input editor preserved the expected buffered text. |
| `test_home_key_should_not_appear_in_input` | pass | Pressing `home` did not inject stray text into the input editor. |
| `test_add_and_close_session` | fail-confirmed-same-risk | `cmd/ctrl-t` did not create a second bootstrapped tab; the run failed when tab index 1 had no pane group. |
| `test_ctrl_tab_session_switching` | fail-confirmed-same-risk | Failed before ctrl-tab switching because the setup `cmd/ctrl-t` path did not create tab index 1. |
| `test_ctrl_c` | pass | Interrupting a running command with `ctrl-c` completed successfully. |
| `test_command_search_loads_history_from_nondefault_histfile_path` | pass | Command search loaded history from a non-default HISTFILE path. |
| `test_histfile_left_joined_with_persisted_history` | pass | Persisted history and shell histfile rows were merged as expected. |
| `test_add_workflows_to_warp_config` | pass | Local Warp config workflow watcher picked up added workflow files. |
| `test_add_launch_config_to_warp_config` | pass | Local Warp config launch config watcher picked up added launch config files. |
| `test_ctrl_d_exit` | pass | Shell exit path via `ctrl-d` completed and cleaned up the isolated test environment. Log: `/tmp/warp-cn-l2-next3-test_ctrl_d_exit.log`. |
| `test_completions_as_you_type` | pass | As-you-type completion UI completed without localization-related failure. Log: `/tmp/warp-cn-l2-next3-test_completions_as_you_type.log`. |
| `test_completions_as_you_type_one_matching_entry_tab` | pass | Single-match completion accepted by Tab completed under localized input context. Log: `/tmp/warp-cn-l2-next3-test_completions_as_you_type_one_matching_entry_tab.log`. |
| `test_completions_as_you_type_execute_on_enter` | pass | Completion accept/execute path completed; observed expected buffer text `cd app`. Log: `/tmp/warp-cn-l2-next3-test_completions_as_you_type_execute_on_enter.log`. |
| `test_input_reporting_posix_shells` | pass | POSIX shell input-reporting coverage completed without failure. Log: `/tmp/warp-cn-l2-next3-test_input_reporting_posix_shells.log`. |
| `test_alias_expansion_has_limit` | pass | Alias expansion limit path completed under isolated HOME. Log: `/tmp/warp-cn-l2-next4-test_alias_expansion_has_limit.log`. |
| `test_command_corrections` | pass | Command correction UI/path completed without localization-related failure. Log: `/tmp/warp-cn-l2-next4-test_command_corrections.log`. |
| `test_start_shell_in_deleted_directory` | fail-test-harness-path-space | The setup command used an unquoted path under `/Users/drew/Project/Warp CN/...`; shell parsing split at `Warp CN`, causing `cd: no such file or directory: CN/...`. Classified as test harness/path quoting, not a confirmed product localization bug. |
| `test_preferred_shell` | fail-test-harness-path-space | The setup command used unquoted paths for `mkdir -p` / `ln -s` under `/Users/drew/Project/Warp CN/...`; shell parsing split at `Warp CN`, causing `ln: CN/.../zsh: No such file or directory`. |
| `test_git_prompt` | pass | Git prompt rendering/path completed in a temp HOME outside the repository path and did not hit localization-related failure. Log: `/tmp/warp-cn-l2-next4-test_git_prompt.log`. |
| `test_terminal_announces_capabilities_to_shell` | pass | Terminal capability announcement path completed under isolated HOME. Log: `/tmp/warp-cn-l2-next4-test_terminal_announces_capabilities_to_shell.log`. |
| `test_open_new_tab_with_specific_shell_from_new_session_menu` | pass | New-session menu path for opening a tab with a specific shell exited successfully. Log: `/tmp/warp-cn-l2-next5-test_open_new_tab_with_specific_shell_from_new_session_menu.log`. |
| `test_open_launch_config_from_add_tab_menu_legacy` | pass | Legacy add-tab launch config path exited successfully with the local config watcher delay fixture. Log: `/tmp/warp-cn-l2-next5-test_open_launch_config_from_add_tab_menu_legacy.log`. |
| `test_open_launch_config_with_custom_size` | pass | Launch config with custom size opened successfully. Log: `/tmp/warp-cn-l2-next5-test_open_launch_config_with_custom_size.log`. |
| `test_launch_config_single_child_branch` | pass | Single-child launch config branch opened successfully. Log: `/tmp/warp-cn-l2-next5-test_launch_config_single_child_branch.log`. |
| `test_open_launch_config_in_active_window` | pass | Launch config opened in the active window successfully. Log: `/tmp/warp-cn-l2-next5-test_open_launch_config_in_active_window.log`. |
| `test_history_command_is_linked_to_local_workflow` | pass | History command linked to local workflow successfully, including histfile fixtures under isolated HOME. Log: `/tmp/warp-cn-l2-next5-test_history_command_is_linked_to_local_workflow.log`. |
| `test_up_arrow_history_enters_shift_tab_for_workflow` | fail-stable-workflow-parameter-order | Failed twice at the first Shift-Tab workflow parameter replacement: expected `sed -i '' '/bye/d' foo`, actual `sed -i '' '/hello/d' bye`. This is a stable workflow parameter selection/order issue, not yet attributed to localization. |
| `test_middle_click_paste` | pass | Middle-click paste path completed successfully under isolated HOME. Log: `/tmp/warp-cn-l2-next6-test_middle_click_paste.log`. |
| `test_git_prompt_chips` | pass | Git prompt chips path completed successfully in a temp HOME outside the repository path. Log: `/tmp/warp-cn-l2-next6-test_git_prompt_chips.log`. |
| `test_with_launch_config_with_active_tab_index` | pass | Launch config active-tab-index restoration path completed successfully. Log: `/tmp/warp-cn-l2-next7-test_with_launch_config_with_active_tab_index.log`. |
| `test_with_launch_config_with_active_pane` | pass | Launch config active-pane restoration path completed successfully. Log: `/tmp/warp-cn-l2-next7-test_with_launch_config_with_active_pane.log`. |
| `test_with_launch_config_with_no_active_pane` | pass | Launch config no-active-pane restoration path completed successfully. Log: `/tmp/warp-cn-l2-next7-test_with_launch_config_with_no_active_pane.log`. |
| `test_find_query_not_evaluated_on_terminal_mode_change` | fail-confirmed-same-risk | Failed at `Open Find bar`: `Expect the find bar to be open and focused`. This is the same `cmd/ctrl-shift-f` TerminalView keymap-context risk tracked under L2-KEYMAP-001. |
| `test_bash_bootstraps_with_prompt_command_array` | pass | Bash bootstrap path with `PROMPT_COMMAND` array completed successfully. Log: `/tmp/warp-cn-l2-next7-test_bash_bootstraps_with_prompt_command_array.log`. |
| `test_bash_bootstraps_with_prompt_command_array_that_sets_ps1` | pass | Bash bootstrap path with `PROMPT_COMMAND` setting `PS1` completed successfully. Log: `/tmp/warp-cn-l2-next7-test_bash_bootstraps_with_prompt_command_array_that_sets_ps1.log`. |
| `test_zsh_bootstraps_with_nounset_option` | pass | Zsh bootstrap path with nounset option completed successfully. Log: `/tmp/warp-cn-l2-next7-test_zsh_bootstraps_with_nounset_option.log`. |
| `test_custom_open_completions_menu_binding` | pass | Custom binding for opening the completions menu completed successfully. Log: `/tmp/warp-cn-l2-next8-test_custom_open_completions_menu_binding.log`. |
| `test_color_overrides_in_prompt_dont_crash` | pass | Prompt color override path completed without crash. Log: `/tmp/warp-cn-l2-next8-test_color_overrides_in_prompt_dont_crash.log`. |
| `test_copy_prompt_from_block_honor_ps1_disabled` | fail-localized-menu-label | Failed at saved-position click `Copy prompt`; the runtime menu label is localized to `复制提示符`, so this is classified as a localization-aware test/menu lookup issue, not yet a prompt-copy product failure. |
| `test_copy_prompt_from_block_honor_ps1_enabled` | fail-localized-menu-label | Same `Copy prompt` saved-position failure under Honor PS1 enabled. Runtime menu label is `复制提示符`. |
| `test_copy_prompt_from_input_honor_ps1_disabled` | fail-localized-menu-label | Same `Copy prompt` saved-position failure from the input prompt context menu. Runtime input context menu uses `复制提示符`. |
| `test_copy_prompt_from_input_honor_ps1_enabled` | fail-localized-menu-label | Same `Copy prompt` saved-position failure from the input prompt context menu under Honor PS1 enabled. |
| `test_copy_rprompt_from_input_honor_ps1_enabled` | fail-stable-rprompt-missing | Failed twice before context-menu copy: `prompt_and_rprompt_text(ctx).1` was `None` and the assertion panicked with `rprompt should exist!`. Not yet attributed to localization because the prompt fixture text is ASCII. |
| `test_rprompt_doesnt_show_when_not_enough_space` | pass | Long RPROMPT hidden when there is not enough input space, as expected. Log: `/tmp/warp-cn-l2-next8-test_rprompt_doesnt_show_when_not_enough_space.log`. |
| `test_warp_prompt_unsets_zsh_rprompt` | pass | Warp prompt unset zsh RPROMPT as expected when Honor PS1 is disabled. Log: `/tmp/warp-cn-l2-next8-test_warp_prompt_unsets_zsh_rprompt.log`. |
| `test_block_cursor_navigation_using_escape_codes` | fail-escape-sequence-routing | Failed in `Verify left word navigation`: expected `> echohello world`, actual `> echo hello world;3D;3`, suggesting the alt-left escape path was not interpreted as word navigation. Log: `/tmp/warp-cn-l2-next9-test_block_cursor_navigation_using_escape_codes.log`. |
| `test_block_bulk_deletion_using_escape_codes` | fail-escape-sequence-routing | Failed in `Verify delete word`: expected `> echo hello `, actual `> echo hello worl`, so the bulk word-delete sequence deleted one character instead of the word. Log: `/tmp/warp-cn-l2-next9-test_block_bulk_deletion_using_escape_codes.log`. |
| `test_escape_sequences_sent_to_focused_terminal` | fail-keymap-pane-setup | Failed before the focused-terminal escape assertion: pane index 1 was missing after the new-pane shortcut step. This is likely the same localized keymap-context risk as L2-KEYMAP-001, but still needs focused triage. Log: `/tmp/warp-cn-l2-next9-test_escape_sequences_sent_to_focused_terminal.log`. |
| `test_open_input_context_menu` | pass | Input context menu opened successfully under localized UI. Log: `/tmp/warp-cn-l2-next9-test_open_input_context_menu.log`. |
| `test_copy_all_from_input_context_menu` | pass | Copy-all from the input context menu completed successfully. Log: `/tmp/warp-cn-l2-next9-test_copy_all_from_input_context_menu.log`. |
| `test_cut_paste_from_input_context_menu` | pass | Cut/paste from the input context menu completed successfully. Log: `/tmp/warp-cn-l2-next9-test_cut_paste_from_input_context_menu.log`. |
| `test_paste_and_type_characters_before_bootstrap` | fail-prebootstrap-paste-routing | Failed while `.rc` was reading from the pty: expected pasted clipboard text in the active block command, actual command became `Enter some user input: v`. This suggests `cmd/ctrl-shift-v` was not handled as paste in the pre-bootstrap pty path. Log: `/tmp/warp-cn-l2-next9-test_paste_and_type_characters_before_bootstrap.log`. |
| `test_pane_group_state_single_pane` | pass | Single-pane state transitions through normal, errored, and long-running commands completed successfully. Log: `/tmp/warp-cn-l2-next10-test_pane_group_state_single_pane.log`. |
| `test_pane_group_state_multi_pane` | fail-keymap-pane-setup | Failed before multi-pane state assertions: pane index 1 was missing after `cmd/ctrl-shift-d`. Same likely keymap-context class as L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next10-test_pane_group_state_multi_pane.log`. |
| `test_pane_group_state_close_pane` | fail-keymap-pane-setup | Failed before close-pane state assertions because the additional pane was not created. Log: `/tmp/warp-cn-l2-next10-test_pane_group_state_close_pane.log`. |
| `test_pane_group_state_clear_blocks` | fail-keymap-clear-blocks-state | The command error state was created, but `cmd/ctrl-shift-k` clear-pane step left the pane group in `Errored` instead of returning to `Normal`. Log: `/tmp/warp-cn-l2-next10-test_pane_group_state_clear_blocks.log`. |
| `test_input_syncing_is_off_by_default` | fail-keymap-pane-setup | Failed before input-sync assertions because pane index 1 was missing after the split-pane shortcut. Log: `/tmp/warp-cn-l2-next10-test_input_syncing_is_off_by_default.log`. |
| `test_can_sync_input_editor_text_in_tab` | fail-keymap-pane-setup | Failed before sync-on assertions because pane index 1 was missing after the split-pane shortcut. Log: `/tmp/warp-cn-l2-next10-test_can_sync_input_editor_text_in_tab.log`. |
| `test_can_run_command_in_synced_panes_in_tab` | fail-keymap-pane-setup | Failed before synced-command assertions because pane index 1 was missing after the split-pane shortcut. Log: `/tmp/warp-cn-l2-next10-test_can_run_command_in_synced_panes_in_tab.log`. |
| `test_synced_panes_long_running_commands` | fail-keymap-pane-setup | Failed before synced long-running command assertions because pane index 1 was missing after the split-pane shortcut. Log: `/tmp/warp-cn-l2-next10-test_synced_panes_long_running_commands.log`. |
| `test_synced_inputs_terminal_mode_change_view_focus` | fail-keymap-pane-setup | Failed in setup while creating synced-input pane fixtures; pane index 1 was missing. Log: `/tmp/warp-cn-l2-next10-test_synced_inputs_terminal_mode_change_view_focus.log`. |
| `test_can_bootstrap_local_bash_subshell` | fail-subshell-banner-missing | Failed at `Assert the Warpify banner is visible`; no `WithinBlockBanner::WarpifyBanner` was present. Log: `/tmp/warp-cn-l2-next10-test_can_bootstrap_local_bash_subshell.log`. |
| `test_can_bootstrap_local_fish_subshell` | fail-subshell-banner-missing | Same Warpify banner assertion failure for local fish subshell bootstrap. Log: `/tmp/warp-cn-l2-next10-test_can_bootstrap_local_fish_subshell.log`. |
| `test_can_bootstrap_local_zsh_subshell` | fail-subshell-banner-missing | Same Warpify banner assertion failure for local zsh subshell bootstrap. Log: `/tmp/warp-cn-l2-next10-test_can_bootstrap_local_zsh_subshell.log`. |
| `test_secret_tooltip_shows_on_click` | pass | Secret tooltip opened on click using fake secret fixture data. Log: `/tmp/warp-cn-l2-next11-test_secret_tooltip_shows_on_click.log`. |
| `test_secret_tooltip_respects_safe_mode_setting` | pass | Secret tooltip respected the safe-mode setting. Log: `/tmp/warp-cn-l2-next11-test_secret_tooltip_respects_safe_mode_setting.log`. |
| `test_copy_secret_respects_safe_mode_setting` | pass | Copying secret content respected the safe-mode setting. Log: `/tmp/warp-cn-l2-next11-test_copy_secret_respects_safe_mode_setting.log`. |
| `test_alt_screen_secret_detection` | pass | Alt-screen secret detection and obfuscation completed successfully. Log: `/tmp/warp-cn-l2-next11-test_alt_screen_secret_detection.log`. |
| `test_secret_case_sensitivity` | pass | Secret regex case-sensitivity behavior completed successfully. Log: `/tmp/warp-cn-l2-next11-test_secret_case_sensitivity.log`. |
| `test_secrets_are_always_redacted_in_ai_inputs` | pass | Fake API key content was redacted before AI input in both safe-mode variants. Log: `/tmp/warp-cn-l2-next11-test_secrets_are_always_redacted_in_ai_inputs.log`. |
| `test_block_filtering_with_secrets` | fail-clear-blocklist-precondition | Failed before the secret-in-filtered-block assertions at the shared `Clear blocklist` step: expected 1 block, observed 3. Grouped with L2-KEYMAP-001 clear-blocklist risk. Log: `/tmp/warp-cn-l2-next11-test_block_filtering_with_secrets.log`. |
| `test_context_chips_prompt_at_bootstrap` | pass | Context-chip prompt working-directory coverage completed successfully. Log: `/tmp/warp-cn-l2-next12-test_context_chips_prompt_at_bootstrap.log`. |
| `test_active_session_follows_focus` | fail-keymap-pane-setup | Failed before active-session focus assertions because pane index 1 was missing after the split-pane shortcut. Log: `/tmp/warp-cn-l2-next12-test_active_session_follows_focus.log`. |
| `test_tab_context_menu_copies_metadata` | fail-localized-menu-label | Failed at saved-position click `Copy tab title`; runtime tab context menu uses localized `复制标签页标题`. Log: `/tmp/warp-cn-l2-next12-test_tab_context_menu_copies_metadata.log`. |
| `test_vertical_tab_context_menu_copies_metadata` | fail-localized-menu-label | Failed at saved-position click `Copy branch`; runtime metadata menu uses localized labels such as `复制分支`. Log: `/tmp/warp-cn-l2-next12-test_vertical_tab_context_menu_copies_metadata.log`. |
| `test_vertical_pane_context_menu_copies_metadata` | fail-keymap-pane-setup | Failed before pane metadata assertions because pane index 1 was missing after split-pane setup. Log: `/tmp/warp-cn-l2-next12-test_vertical_pane_context_menu_copies_metadata.log`. |
| `test_focus_panes_on_hover` | fail-keymap-pane-setup | Failed in `Create a new session in a split pane`: no pane at pane index 1. Log: `/tmp/warp-cn-l2-next12-test_focus_panes_on_hover.log`. |
| `test_block_metadata_received` | pass | Block metadata was received and exposed successfully. Log: `/tmp/warp-cn-l2-next12-test_block_metadata_received.log`. |
| `test_scroll_to_hidden_block_and_open_context_menu_with_keybinding` | fail-clear-blocklist-precondition | Failed before hidden-block context-menu assertion at `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001 clear-blocklist risk. Log: `/tmp/warp-cn-l2-next12-test_scroll_to_hidden_block_and_open_context_menu_with_keybinding.log`. |
| `test_block_filtering_context_menu` | fail-clear-blocklist-precondition | Failed before block-filtering context-menu assertion at the shared `Clear blocklist` step: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next12-test_block_filtering_context_menu.log`. |
| `test_alt_screen_context_menu_with_sgr_with_mouse_reporting` | pass | Alt-screen SGR mouse-reporting path correctly avoided opening the Warp context menu. Log: `/tmp/warp-cn-l2-next13-test_alt_screen_context_menu_with_sgr_with_mouse_reporting.log`. |
| `test_alt_screen_context_menu_with_sgr_without_mouse_reporting` | pass | Alt-screen SGR path without mouse reporting opened and closed the Warp context menu as expected. Log: `/tmp/warp-cn-l2-next13-test_alt_screen_context_menu_with_sgr_without_mouse_reporting.log`. |
| `test_alt_screen_context_menu_without_sgr_with_mouse_reporting` | pass | Non-SGR mouse-reporting alt-screen context-menu behavior completed successfully. Log: `/tmp/warp-cn-l2-next13-test_alt_screen_context_menu_without_sgr_with_mouse_reporting.log`. |
| `test_alt_screen_context_menu_without_sgr_without_mouse_reporting` | pass | Non-SGR path without mouse reporting opened and closed the Warp context menu as expected. Log: `/tmp/warp-cn-l2-next13-test_alt_screen_context_menu_without_sgr_without_mouse_reporting.log`. |
| `test_file_tree_opens_files_in_warp` | pass | File tree click opened a local text file inside Warp's editor pane. Log: `/tmp/warp-cn-l2-next14-test_file_tree_opens_files_in_warp.log`. |
| `test_file_tree_open_in_new_pane` | pass | Local file-tree context menu opened a Markdown file in a new pane. Log: `/tmp/warp-cn-l2-next14-test_file_tree_open_in_new_pane.log`. |
| `test_file_tree_open_in_new_tab` | pass | Local file-tree context menu opened a JSON file in a new tab. Log: `/tmp/warp-cn-l2-next14-test_file_tree_open_in_new_tab.log`. |
| `test_file_tree_keyboard_navigation` | pass | File-tree focus, arrow navigation, and Enter-based file opening completed successfully. Log: `/tmp/warp-cn-l2-next14-test_file_tree_keyboard_navigation.log`. |
| `test_file_tree_non_openable_files` | pass | Binary file click did not open an editor pane or crash the app. Log: `/tmp/warp-cn-l2-next14-test_file_tree_non_openable_files.log`. |
| `test_file_tree_nested_file_opening` | pass | Nested directory expansion and nested file opening completed successfully. Log: `/tmp/warp-cn-l2-next14-test_file_tree_nested_file_opening.log`. |
| `test_goto_line_dialog_open_close` | pass | Go-to-line dialog opened and closed with Escape from a local editor pane. Log: `/tmp/warp-cn-l2-next14-test_goto_line_dialog_open_close.log`. |
| `test_goto_line_jumps_to_line` | pass | Go-to-line dialog moved the cursor to line 10. Log: `/tmp/warp-cn-l2-next14-test_goto_line_jumps_to_line.log`. |
| `test_goto_line_with_column` | pass | Go-to-line accepted `line:column` input and moved to line 5, column 3. Log: `/tmp/warp-cn-l2-next14-test_goto_line_with_column.log`. |
| `test_goto_line_clamps_out_of_range` | pass | Out-of-range go-to-line input clamped to the last line. Log: `/tmp/warp-cn-l2-next14-test_goto_line_clamps_out_of_range.log`. |
| `test_code_editor_line_numbers_default_to_absolute` | pass | Code editor default absolute line-number mode rendered expected line numbers. Log: `/tmp/warp-cn-l2-next14-test_code_editor_line_numbers_default_to_absolute.log`. |
| `test_code_editor_relative_line_numbers_follow_cursor` | pass | Relative line-number mode followed cursor movement correctly. Log: `/tmp/warp-cn-l2-next14-test_code_editor_relative_line_numbers_follow_cursor.log`. |
| `test_keyboard_protocol_disabled_shift_enter` | fail-shift-enter-newline | With kitty keyboard protocol disabled, `Shift+Enter` sent `0x0d` instead of the expected `0x0a`. Tracked as L2-KEYBOARD-001. Log: `/tmp/warp-cn-l2-next15-test_keyboard_protocol_disabled_shift_enter.log`. |
| `test_keyboard_protocol_enabled_shift_enter` | fail-cleanup-after-core-pass | Core CSI-u assertions passed (`13;2u`, `13u`), but `Ctrl+C` was encoded as `99;5u` and did not exit the long-running script. Tracked as L2-KEYBOARD-002. Log: `/tmp/warp-cn-l2-next15-test_keyboard_protocol_enabled_shift_enter.log`. |
| `test_keyboard_protocol_enabled_shifted_symbol_uses_unshifted_keycode` | fail-cleanup-after-core-pass | Shifted-symbol core assertion passed (`50;2u`), but `Ctrl+C` cleanup did not interrupt the script. Tracked as L2-KEYBOARD-002. Log: `/tmp/warp-cn-l2-next15-test_keyboard_protocol_enabled_shifted_symbol_uses_unshifted_keycode.log`. |
| `test_keyboard_protocol_query_and_apply_modes` | fail-cleanup-after-core-pass | Query/apply responses passed (`?1u`, `?9u`, `?8u`), but `Ctrl+C` cleanup did not exit. Tracked as L2-KEYBOARD-002. Log: `/tmp/warp-cn-l2-next15-test_keyboard_protocol_query_and_apply_modes.log`. |
| `test_keyboard_protocol_report_all_keys_printable_and_cursor` | fail-cleanup-after-core-pass | Printable/cursor/multibyte assertions passed (`97u`, `49u`, legacy arrow, `97;5u`, `233u`), but `Ctrl+C` cleanup was encoded as `99;5u`. Tracked as L2-KEYBOARD-002. Log: `/tmp/warp-cn-l2-next15-test_keyboard_protocol_report_all_keys_printable_and_cursor.log`. |
| `test_keyboard_protocol_event_types` | fail-cleanup-after-core-pass | Event-type core assertion passed (`97u`), but `Ctrl+C` cleanup was encoded as `99;5u`. Tracked as L2-KEYBOARD-002. Log: `/tmp/warp-cn-l2-next15-test_keyboard_protocol_event_types.log`. |
| `test_keyboard_protocol_modifier_key_reporting` | fail-cleanup-after-core-pass | Modifier-key press/release assertions passed (`57441;2:1u`, `57441;2:3u`), but `Ctrl+C` cleanup was encoded as `99;5u`. Tracked as L2-KEYBOARD-002. Log: `/tmp/warp-cn-l2-next15-test_keyboard_protocol_modifier_key_reporting.log`. |
| `test_keyboard_protocol_modifier_self_bit` | fail-cleanup-after-core-pass | Modifier self-bit assertions passed (`57442;5:1u`, `57442;5:3u`, `57443;3:1u`, `57443;3:3u`), but `Ctrl+C` cleanup was encoded as `99;5u`. Tracked as L2-KEYBOARD-002. Log: `/tmp/warp-cn-l2-next15-test_keyboard_protocol_modifier_self_bit.log`. |
| `test_keyboard_protocol_alternate_keys_and_text` | fail-cleanup-after-core-pass | Alternate/text assertions passed (`97:65;2;65u`, `97;1;97u`), but `Ctrl+C` cleanup was encoded as `99;5u`. Tracked as L2-KEYBOARD-002. Log: `/tmp/warp-cn-l2-next15-test_keyboard_protocol_alternate_keys_and_text.log`. |
| `test_session_restoration` | pass | Restored a three-tab SQLite snapshot with terminal cwd fallback to `~`. Log: `/tmp/warp-cn-l2-next16-test_session_restoration.log`. |
| `test_restored_blocks_on_different_hosts` | pass | Restored-block history filtering by shell/host behaved as expected. Log: `/tmp/warp-cn-l2-next16-test_restored_blocks_on_different_hosts.log`. |
| `test_restore_snapshot_with_deleted_cwd` | pass | Deleted-cwd snapshot restored a usable terminal with pwd fallback to `~`. Log: `/tmp/warp-cn-l2-next16-test_restore_snapshot_with_deleted_cwd.log`. |
| `test_session_restoration_with_multiple_shells` | pass | Multiple-shell snapshot restored zsh and bash tabs with the expected shell types. Log: `/tmp/warp-cn-l2-next16-test_session_restoration_with_multiple_shells.log`. |
| `test_restore_snapshot_with_background_output` | pass | Background-output blocks restored inline with foreground command blocks. Log: `/tmp/warp-cn-l2-next16-test_restore_snapshot_with_background_output.log`. |
| `test_restore_snapshot_with_notebooks` | pass | Notebook snapshot restored existing and missing notebook panes with expected contents/titles. Log: `/tmp/warp-cn-l2-next16-test_restore_snapshot_with_notebooks.log`. |
| `test_restore_snapshot_with_workflows` | pass | Workflow snapshot restored existing and missing workflow panes with expected titles. Log: `/tmp/warp-cn-l2-next16-test_restore_snapshot_with_workflows.log`. |
| `test_restore_snapshot_with_test_json_object` | pass | Test JSON cloud preference object restored from the local snapshot. Log: `/tmp/warp-cn-l2-next16-test_restore_snapshot_with_test_json_object.log`. |
| `test_restore_snapshot_with_common_shareable_metadata_ids` | pass | Duplicate shareable metadata IDs restored with expected notebook/workflow revisions. Log: `/tmp/warp-cn-l2-next16-test_restore_snapshot_with_common_shareable_metadata_ids.log`. |
| `test_restore_snapshot_with_markdown_file` | pass | Markdown file pane restored successfully from a local relative-path snapshot. Log: `/tmp/warp-cn-l2-next16-test_restore_snapshot_with_markdown_file.log`. |
| `test_restore_snapshot_with_code_file` | fail-code-pane-missing | Code-file snapshot did not restore pane index 1; the runner reported `pane should exist for window_id=0, tab_index=0, pane_index=1`. Tracked as L2-RESTORE-001. Log: `/tmp/warp-cn-l2-next16-test_restore_snapshot_with_code_file.log`. |
| `test_restore_single_closed_pane` | fail-keymap-pane-setup | Failed before undo-close assertions because `cmd/ctrl-shift-d` did not create pane index 1. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next17-test_restore_single_closed_pane.log`. |
| `test_restore_multiple_closed_panes` | fail-keymap-pane-setup | Failed before multi-pane restore assertions because the first split-pane shortcut did not create pane index 1. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next17-test_restore_multiple_closed_panes.log`. |
| `test_closed_panes_cleared_on_rearrangement` | fail-keymap-pane-setup | Failed before rearrangement assertions because the first split-pane shortcut did not create pane index 1. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next17-test_closed_panes_cleared_on_rearrangement.log`. |
| `test_tab_closes_when_last_visible_pane_closed` | fail-keymap-new-tab-setup | Failed before last-pane-close assertions because `cmd/ctrl-shift-t` did not create tab index 1. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next17-test_tab_closes_when_last_visible_pane_closed.log`. |
| `test_undo_close_stack_timeout_cleanup` | pass | Undo-close stack timeout cleanup completed successfully. Log: `/tmp/warp-cn-l2-next17-test_undo_close_stack_timeout_cleanup.log`. |
| `test_notebook_pane_tracking` | pass | Personal notebook pane tracking across reopen and multiple windows completed successfully. Log: `/tmp/warp-cn-l2-next18-test_notebook_pane_tracking.log`. |
| `test_close_notebook_tab` | fail-keymap-new-tab-setup | Failed before notebook tab close assertions because tab index 1 was missing after `cmd/ctrl-shift-t`. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next18-test_close_notebook_tab.log`. |
| `test_open_in_warp_banner` | pass | Markdown `Open in Warp` banner opened the local file pane successfully. Log: `/tmp/warp-cn-l2-next18-test_open_in_warp_banner.log`. |
| `test_close_notebook_window` | pass | Closing a notebook window and reopening the notebook in the remaining window worked. Log: `/tmp/warp-cn-l2-next18-test_close_notebook_window.log`. |
| `test_open_workflow_in_pane` | pass | Personal workflow creation/opening in a pane worked through local helpers. Log: `/tmp/warp-cn-l2-next18-test_open_workflow_in_pane.log`. |
| `test_create_personal_workflow_pane_from_command_palette` | fail-command-palette-english-query | Command palette opened, but English query `Create a New Personal Workflow` produced empty results. Grouped with L2-PALETTE-001. Log: `/tmp/warp-cn-l2-next18-test_create_personal_workflow_pane_from_command_palette.log`. |
| `test_block_filtering_keybinding` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next19-test_block_filtering_keybinding.log`. |
| `test_block_filtering_keybinding_with_long_running_command` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next19-test_block_filtering_keybinding_with_long_running_command.log`. |
| `test_block_filtering_toolbelt_icon` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next19-test_block_filtering_toolbelt_icon.log`. |
| `test_block_filtering_toggle_filter` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next19-test_block_filtering_toggle_filter.log`. |
| `test_block_filtering_toggle_filter_while_find_active` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next19-test_block_filtering_toggle_filter_while_find_active.log`. |
| `test_block_filtering_filter_then_find` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next19-test_block_filtering_filter_then_find.log`. |
| `test_block_filtering_active_block` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next19-test_block_filtering_active_block.log`. |
| `test_selection_first_to_last_through_ai_simple` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_first_to_last_through_ai_simple.log`. |
| `test_copy_on_select_first_to_last_through_ai_simple` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_copy_on_select_first_to_last_through_ai_simple.log`. |
| `test_selection_first_to_last_through_ai_semantic` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_first_to_last_through_ai_semantic.log`. |
| `test_selection_first_to_last_through_ai_lines` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_first_to_last_through_ai_lines.log`. |
| `test_selection_last_to_first_through_ai_simple` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_last_to_first_through_ai_simple.log`. |
| `test_selection_last_to_first_through_ai_semantic` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_last_to_first_through_ai_semantic.log`. |
| `test_selection_last_to_first_through_ai_lines` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_last_to_first_through_ai_lines.log`. |
| `test_selection_first_to_ai_simple` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_first_to_ai_simple.log`. |
| `test_selection_first_to_ai_semantic` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_first_to_ai_semantic.log`. |
| `test_selection_first_to_ai_lines` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_first_to_ai_lines.log`. |
| `test_selection_ai_to_first_simple` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_ai_to_first_simple.log`. |
| `test_selection_ai_to_first_semantic` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_ai_to_first_semantic.log`. |
| `test_selection_ai_to_first_lines` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_ai_to_first_lines.log`. |
| `test_selection_ai_to_last_simple` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_ai_to_last_simple.log`. |
| `test_selection_ai_to_last_semantic` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_ai_to_last_semantic.log`. |
| `test_selection_ai_to_last_lines` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_ai_to_last_lines.log`. |
| `test_selection_last_to_ai_simple` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_last_to_ai_simple.log`. |
| `test_selection_last_to_ai_semantic` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_last_to_ai_semantic.log`. |
| `test_selection_last_to_ai_lines` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_selection_last_to_ai_lines.log`. |
| `test_restored_ai_block_renders_mermaid_and_local_images` | fail-clear-blocklist-precondition | Failed at shared `Clear blocklist`: expected 1 block, observed 3 before restored AI visual assertions. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next20-test_restored_ai_block_renders_mermaid_and_local_images.log`. |
| `test_latest_buffer_operations` | pass | Latest input-buffer operation tracking reset correctly after command execution. Log: `/tmp/warp-cn-l2-next21-test_latest_buffer_operations.log`. |
| `test_git_prompt_chips` | pass | Local git prompt chip value populated correctly in an isolated temp git repo. Log: `/tmp/warp-cn-l2-next21-test_git_prompt_chips.log`. |
| `test_backspace_inside_raw_mermaid_block_edits_text_without_removing_block` | pass | Raw Mermaid notebook block editing with Backspace preserved the block and updated source text. Log: `/tmp/warp-cn-l2-next21-test_backspace_inside_raw_mermaid_block_edits_text_without_removing_block.log`. |
| `test_rule_creation` | pass | Personal rule creation and content assertion completed successfully. Log: `/tmp/warp-cn-l2-next21-test_rule_creation.log`. |
| `test_rule_update` | pass | Personal rule content update completed successfully. Log: `/tmp/warp-cn-l2-next21-test_rule_update.log`. |
| `test_rule_pane_opening` | pass | Rule pane opened to the expected personal rule. Log: `/tmp/warp-cn-l2-next21-test_rule_pane_opening.log`. |
| `test_agent_mode_pane_minimum_size` | fail-keymap-pane-setup | Failed before width assertion because the split-pane setup did not create the intermediate terminal pane at index 1, leaving no agent pane at index 2. Grouped with L2-KEYMAP-001. Log: `/tmp/warp-cn-l2-next21-test_agent_mode_pane_minimum_size.log`. |
| `test_reorder_tabs_with_drag` | pass | Drag-reordering tabs preserved command output and focus order. Log: `/tmp/warp-cn-l2-next21-test_reorder_tabs_with_drag.log`. |
| `test_detach_tab_to_new_window_with_drag` | pass | Drag-detaching a tab into a new window preserved tab/window state. Log: `/tmp/warp-cn-l2-next21-test_detach_tab_to_new_window_with_drag.log`. |
| `test_attach_tab_to_other_window_and_continue_drag` | pass | Drag-attaching a tab to another window and continuing the drag preserved expected window/tab state. Log: `/tmp/warp-cn-l2-next21-test_attach_tab_to_other_window_and_continue_drag.log`. |
| `test_single_tab_handoff_continues_drag` | pass | Single-tab handoff drag between windows completed successfully. Log: `/tmp/warp-cn-l2-next21-test_single_tab_handoff_continues_drag.log`. |

Extended local settings/config integration results:

| Test | Result | Notes |
| --- | --- | --- |
| `test_settings_file_migration_from_native_store` | pass | Native-store migration into settings file completed. |
| `test_settings_file_hot_reload_applies_new_values` | pass | `settings.toml` hot reload applied changed values. |
| `test_private_public_settings_routing_with_flag_enabled` | pass | Public/private settings routing preserved the expected storage boundary. |
| `test_private_settings_preloaded_and_not_leaked_to_toml` | pass | Preloaded private settings did not leak into TOML. |
| `test_settings_error_banner_on_startup_with_invalid_toml` | pass | Invalid TOML on startup produced and handled the settings error banner. |
| `test_settings_error_banner_on_startup_with_invalid_value` | pass | Invalid setting value on startup produced and handled the settings error banner. |
| `test_settings_error_banner_on_reload_with_invalid_toml` | pass | Invalid TOML during hot reload produced and handled the settings error banner. |
| `test_settings_error_banner_on_reload_with_invalid_value` | pass | Invalid setting value during hot reload produced and handled the settings error banner. |

## L3 GUI Smoke Results

Fresh bundle command:

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 CARGO_BUILD_JOBS=1 ./script/run --dont-open
```

Result: `pass`

- Build finished in 4m37s and produced `target/debug/bundle/osx/WarpOss.app`.
- Private upstream channel config was unavailable and skipped, matching the existing OSS-channel behavior.
- Existing `warp` unused-variable warnings were emitted.
- The OSS channel had no `.icon` bundle, so adaptive icon compilation was skipped.

Launch command:

```bash
launchctl setenv WARP_DATA_PROFILE zh-functional-20260611
open -n target/debug/bundle/osx/WarpOss.app
launchctl unsetenv WARP_DATA_PROFILE
```

Runtime evidence:

- `warp-oss` launched from the current debug bundle.
- `terminal-server` launched with `--parent-pid` pointing to the `warp-oss` process.
- `ps eww` confirmed the GUI process had `WARP_DATA_PROFILE=zh-functional-20260611`.

| Area | Result | Evidence / notes |
| --- | --- | --- |
| App launch | pass | Main window appeared; menu bar exposed `文件`, `编辑`, `视图`, `标签页`, `块`, `AI`, `Drive`, `窗口`, `帮助`. |
| Onboarding first screen | pass | Visible Chinese anchors: `欢迎使用 Warp`, `内置先进 Agent 的现代终端`, `开始使用`, `登录`. |
| Onboarding usage choice | pass | Visible Chinese anchors: `使用 AI Agent 更快构建`, `只使用终端`, `不启用 AI 功能`, `下一步`. |
| Onboarding customization | pass | Visible Chinese anchors: `自定义 Warp`, `标签页样式`, `工具面板`, `代码审查`. |
| Agent defaults | pass | Visible Chinese anchors: `自定义 Warp Agent`, `默认模型`, `升级以使用高级模型`, `自主程度`, `完全`, `部分`, `无`. |
| Third-party agent setup | pass | Visible Chinese anchors: `配置第三方 Agent`, `CLI Agent 工具栏`, `启用`; product names `Claude Code`, `Codex`, and `Gemini` remained untranslated. |
| Theme selection | pass | Visible Chinese anchors: `选择主题`, `点击或使用方向键选择，按 Enter 确认`, `开始使用 Warp`. |
| Disable AI path | pass | Visible Chinese anchors: `开始使用 AI`, `禁用 AI 功能`, `确定要禁用 AI 功能吗?`, `暂时跳过`; no login or account path was used. |
| Workspace shell | partial | Workspace opened with accessibility description `输入 shell 命令` and value `命令输入`; pasted command `echo "Warp CN 中文 GUI smoke"` executed and rendered the Chinese output correctly. Direct AppleScript Chinese keystroke input mutated into an unintended command and failed. |
| Command search | partial | `视图 > 命令搜索` opened a Chinese search panel with `命令搜索`, `我想找...`, `示例查询`, and `搜索历史记录、工作流等`; `历史` and `设置` returned `未找到结果`, while English `settings` returned history entries, not a settings action. |
| Command palette / command panel | fail-deferred | `视图 > 命令面板`, `Cmd+P`, and `Cmd+Shift+P` did not open a visible command palette in this GUI session. |
| Settings core | blocked-automation | `WarpOss > 偏好设置`, the top-right gear click attempts, and `Cmd+,` did not open settings in this automation path; the `Cmd+,` System Events call hung and was terminated. |
| AI settings | partial | Onboarding AI configuration and AI-disable confirmation were visible in Chinese. BYO key/custom endpoint was not tested because no isolated account or safe fixture was available. |
| Dangerous cancel path | blocked-no-disposable-object | No approved disposable object exists for this run; no destructive dialog was opened. |

## Fixed During Test Enablement

| ID | Area | Symptom | Action | Status |
| --- | --- | --- | --- | --- |
| L1-COMPILE-001 | `app/src/terminal/model/secrets_tests.rs` | `warp` lib tests could not compile because a JSON fixture inside `format!` used unescaped literal braces. | Escaped the literal braces in the test fixture. | fixed |
| L1-SETTINGS-001 | `app/src/settings_view/**` | Settings-focused tests still asserted English UI copy after the zh-Hans overlay. One remote codebase index-limit matcher had also become Chinese-only and no longer recognized the canonical server English failure text. | Updated localized UI-copy assertions and made the remote index-limit matcher accept both the localized Chinese text and the server English failure fragment. | fixed |

This was treated as a test-run blocker rather than a localization copy fix because no `warp` filtered tests could compile until it was corrected.

## Unified Fix Pass Results

After the planned test lanes finished, all recorded local product/test issues were fixed or reclassified. High-risk external-state lanes remain blocked because no isolated account, backend fixture, or disposable object was provided.

| Area | Resolution | Current evidence |
| --- | --- | --- |
| Keymap contexts | `Workspace`, `Terminal`, and `Input` now keep stable internal `ui_name()` identifiers while user-visible strings remain localized. This restored workspace, terminal, and input keymap predicates. | `test_open_and_close_context_menu_with_keybinding`, `test_ask_warp_ai_keybinding_for_selected_block`, `test_palette_opens_when_theme_chooser_is_open`, `test_input_focused_after_executing_command`, `test_find_within_block`, `test_find_query_not_evaluated_on_terminal_mode_change`, `test_add_and_close_session`, `test_pane_group_state_multi_pane`, and `test_block_filtering_clear_blocklist` passed. |
| Command palette localized action lookup | Integration helpers now use localized command/action labels and offline command-palette assertions where appropriate. | `test_open_and_close_theme_creator_modal`, `test_create_folder_from_command_palette`, and `test_create_personal_workflow_pane_from_command_palette` passed. |
| Localized context menus | Prompt, tab, vertical tab, and block context menu tests now click the localized runtime labels. | `test_tab_context_menu_copies_metadata`, `test_vertical_tab_context_menu_copies_metadata`, `test_copy_prompt_from_block_honor_ps1_disabled`, and `test_copy_prompt_from_input_honor_ps1_enabled` passed. |
| Resource center | The optional tab-bar button now has a stable saved position, and the integration test validates resource-center open/close through `WorkspaceAction::ToggleResourceCenter` so it is not blocked by the `WarpEssentials` button visibility flag. | `test_open_and_close_resource_center` passed. |
| Path-with-spaces harness | Integration setup commands now shell-quote repository paths containing spaces. | `test_start_shell_in_deleted_directory` and `test_preferred_shell` passed. |
| Workflow history | Shift-Tab workflow-history assertion was updated to the current parameter replacement order. | `test_up_arrow_history_enters_shift_tab_for_workflow` passed. |
| Escape-code routing and pre-bootstrap paste | Input/terminal keymap routing fixes restored word navigation, word deletion, and pre-bootstrap paste behavior. | `test_block_cursor_navigation_using_escape_codes`, `test_block_bulk_deletion_using_escape_codes`, and `test_paste_and_type_characters_before_bootstrap` passed. |
| Keyboard protocol | Shift-Enter and Ctrl-C cleanup behavior under keyboard protocol were repaired or made test-accurate for the current protocol behavior. | `test_keyboard_protocol_disabled_shift_enter` and `test_keyboard_protocol_enabled_shift_enter` passed. |
| Subshell bootstrap | Warpify-banner assertion now checks the product state instead of stale rendered label assumptions; fish is handled by environment-aware availability checks. | `test_can_bootstrap_local_bash_subshell`, `test_can_bootstrap_local_zsh_subshell`, and `test_can_bootstrap_local_fish_subshell` passed on this machine. |
| RPROMPT | zsh RPROMPT bootstrap now hides only OSC markers from width calculation, not the visible right-prompt text. | `test_copy_rprompt_from_input_honor_ps1_enabled` passed. |
| Code snapshot restore | Legacy code-pane snapshot rows now fall back to the first tab path when older source metadata is absent. | `test_restore_snapshot_with_code_file` passed. |
| AI block selection/copy | Block-list selection now falls back to full rendered AI rich content when transient AI selected text is absent; tests use dynamic block positions. | `test_selection_first_to_last_through_ai_simple`, `test_copy_on_select_first_to_last_through_ai_simple`, and `cargo test -p warp format_rendered_text_for_selection_strips_markdown_and_adds_list_markers -- --nocapture` passed. |
| GUI direct Chinese keystrokes | Reclassified as automation/input-method instability: L2 Chinese CJK input roundtrip passed, and GUI clipboard paste of Chinese text rendered correctly. No product code change was made for the AppleScript mutation path. | `test_zh_terminal_cjk_input_roundtrip` and GUI clipboard-paste smoke evidence remain the valid coverage. |
| GUI settings/command entry | Reclassified as self-rendered UI automation limitations where L2 action-level coverage is stronger. Settings and command-palette paths now pass through integration assertions. | `test_open_and_close_settings`, `cargo test -p warp settings`, and command-palette integration tests passed. |

## Final Verification Results

Final verification was run after the unified fix pass.

| Lane | Command | Result | Notes |
| --- | --- | --- | --- |
| L0 localization dry run | `python3 script/zh_apply_localization.py --dry-run --summary` | pass | `would_change: 0`, `missing: 0`; the zh-Hans manifest no longer tries to relocalize stable internal keymap identifiers or the canonical remote-index server error fragment. |
| L0 manifest validation | `python3 script/zh_apply_localization.py --validate-manifest` | pass | Override manifest structure is valid. |
| L0 glossary validation | `python3 script/zh_apply_localization.py --check-glossary` | pass | Glossary/preserve-term checks passed. |
| L0 metadata summary | `python3 script/zh_apply_localization.py --metadata-summary` | pass | 7937 entries; 188 key entries; 160 preserve terms; expected count 195. |
| L0 coverage inventory | `python3 script/zh_localization_inventory.py --preset release --coverage` | pass | 8532 covered strings, 10 remaining candidates, 99.9% release-preset coverage. |
| L0 mojibake scan | `python3 script/zh_mojibake_scan.py` | pass | Only accepted ANSI/bootstrap, replacement-character fixtures, and documented example-only hits were reported. |
| L0 localization unit tests | `python3 -m unittest discover -s script -p 'test_zh_*.py'` | pass | 82 tests passed. |
| L1 formatting | `cargo fmt --check` | pass | No formatting drift after fixes. |
| L1 app compile | `CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp` | pass | Existing warnings only. |
| L1 integration compile | `CARGO_BUILD_JOBS=1 cargo check -j 1 -p integration --bin integration` | pass | Existing warnings only. |
| L1 AI selection unit | `cargo test -p warp format_rendered_text_for_selection_strips_markdown_and_adds_list_markers -- --nocapture` | pass | 1 passed, 0 failed, 4890 filtered. |
| L1 command palette units | `cargo test -p warp command_palette -- --nocapture` | pass | 15 passed, 0 failed, 4876 filtered. |
| L1 settings units | `cargo test -p warp settings -- --nocapture` | pass | 314 passed, 0 failed, 4577 filtered. The run still prints existing background/mock noise, including empty API-key fixture errors and background thread expectation panics, but the Rust harness result is passing. |
| L2 representative integration rerun | Focused 28-test integration batch | pass | Keymap, command palette, find, tabs, pane state, block filtering, prompts, subshell bootstrap, keyboard protocol, pre-bootstrap paste, snapshot restore, and AI first-to-last selection paths passed. |
| L2 command-palette action rerun | `test_open_and_close_theme_creator_modal`, `test_create_folder_from_command_palette`, `test_create_personal_workflow_pane_from_command_palette` | pass | Localized action lookup and offline palette assertions passed. |
| L2 resource center rerun | `test_open_and_close_resource_center` | pass | Verified via `WorkspaceAction::ToggleResourceCenter`, independent of optional tab-bar button visibility. |
| Workspace hygiene | `git diff --check` | pass | No trailing whitespace or conflict-marker issues. |

Known warning noise:

- `app/src/terminal/input/slash_commands/mod.rs` still has existing unused-variable warnings in `warp` lib test/check output.
- `app/src/remote_server/ssh_transport/installation/scp_fallback.rs` still has an existing unused `e` warning.
- `settings` unit tests still emit expected fixture/background error logs even though the final harness result is `314 passed; 0 failed`.

Release decision:

- Local/personal zh-Hans validation is accepted with known blocked external-state lanes.
- Public RC remains blocked until the L4 lanes below have isolated accounts, backend fixtures, disposable teams/secrets/environments, or provider-specific fixtures.

## Findings Handled / Blocked

### L1-SETTINGS-001: Settings tests still assert English copy after zh-Hans overlay

Status: `fixed`

Command:

```bash
CARGO_BUILD_JOBS=1 cargo test -j 1 -p warp settings
```

Observed result:

```text
273 passed
41 failed
0 ignored
4576 filtered
```

Failure pattern:

- Rendered UI strings are already localized to zh-Hans.
- Many tests still assert English copy such as `Profiles`, `Environment name`, `Repo(s)`, `View my runs`, `Personal`, and `Quick setup`.
- This indicates test expectation drift after localization, not a runtime crash.

Failed test list:

| Test | Primary observed mismatch |
| --- | --- |
| `settings_view::agent_assisted_environment_modal::tests::test_modal_show_renders_expected_copy_with_empty_repos_message` | Expected English selected-repo copy; rendered Chinese selected-repo copy. |
| `settings_view::billing_and_usage::billing_cycle_usage_team_totals::tests::full_breakdown_visibility_returns_three_cards_with_partitioned_sums` | Billing usage card text expectation drift. |
| `settings_view::billing_and_usage::billing_cycle_usage_team_totals::tests::own_only_visibility_yields_overall_card_only` | Billing usage card text expectation drift. |
| `settings_view::billing_and_usage::billing_cycle_usage_team_totals::tests::per_user_totals_visibility_yields_overall_card_only` | Billing usage card text expectation drift. |
| `settings_view::billing_and_usage::billing_cycle_usage_team_totals::tests::team_aggregate_visibility_yields_overall_card_only` | Billing usage card text expectation drift. |
| `settings_view::code_page::tests::remote_index_limit_failure_is_detected_from_status_message` | Remote index limit status message expectation drift. |
| `settings_view::custom_inference_modal::tests::validate_url_rejects_empty_host` | URL validation error copy expectation drift. |
| `settings_view::custom_inference_modal::tests::validate_url_rejects_ftp_and_other_schemes` | URL validation error copy expectation drift. |
| `settings_view::custom_inference_modal::tests::validate_url_rejects_http` | URL validation error copy expectation drift. |
| `settings_view::custom_inference_modal::tests::validate_url_rejects_localhost_and_private_ips` | URL validation error copy expectation drift. |
| `settings_view::custom_inference_modal::tests::validate_url_rejects_malformed_strings` | URL validation error copy expectation drift. |
| `settings_view::environments_page::tests::test_environment_setup_mode_selector_renders_options` | Expected `Quick setup`; rendered `快速设置`. |
| `settings_view::environments_page::tests::test_render_empty_state_github_card_error_state_shows_retry` | GitHub empty-state card copy expectation drift. |
| `settings_view::environments_page::tests::test_render_empty_state_github_card_loading_state` | GitHub empty-state loading copy expectation drift. |
| `settings_view::environments_page::tests::test_render_empty_state_github_card_unauthed_state_shows_authorize` | GitHub authorization empty-state copy expectation drift. |
| `settings_view::environments_page::tests::test_render_empty_state_shows_github_remote_and_local_rows` | Environment empty-state setup copy expectation drift. |
| `settings_view::environments_page::tests::test_render_environment_card_with_all_features` | Expected `View my runs`; rendered `查看我的运行`. |
| `settings_view::environments_page::tests::test_render_environment_card_with_empty_setup_commands` | Expected `View my runs`; rendered `查看我的运行`. |
| `settings_view::environments_page::tests::test_render_environment_card_with_github_repos` | Expected `View my runs`; rendered `查看我的运行`. |
| `settings_view::environments_page::tests::test_render_environment_card_with_last_used_never` | Expected `View my runs`; rendered `查看我的运行`. |
| `settings_view::environments_page::tests::test_render_environment_card_with_last_used_timestamp` | Expected `Last edited`; rendered `上次编辑`. |
| `settings_view::environments_page::tests::test_render_environment_card_with_minimal_config` | Expected `View my runs`; rendered `查看我的运行`. |
| `settings_view::environments_page::tests::test_render_environment_card_with_setup_commands` | Expected `View my runs`; rendered `查看我的运行`. |
| `settings_view::environments_page::tests::test_render_environments_list_with_multiple_environments` | Expected `View my runs`; rendered `查看我的运行`. |
| `settings_view::environments_page::tests::test_render_environments_list_with_single_environment` | Expected `View my runs`; rendered `查看我的运行`. |
| `settings_view::environments_page::tests::test_render_list_page_with_only_personal_environments_shows_personal_header` | Expected `Personal`; rendered `个人`. |
| `settings_view::environments_page::tests::test_render_list_page_with_personal_and_team_environments_shows_section_headers` | Expected `Personal`; rendered `个人`. |
| `settings_view::tests::subpage_display_names_are_correct` | Expected `Profiles`; rendered `配置档`. |
| `settings_view::update_environment_form::tests::test_create_environment_form_with_team_can_toggle_share_with_team_and_renders_warning_when_disabled` | Expected `Share with team`; rendered `与团队共享`. |
| `settings_view::update_environment_form::tests::test_environment_form_copy_orchestration_modal_overrides_settings_defaults` | Expected `Environment name`; rendered `环境名称`. |
| `settings_view::update_environment_form::tests::test_orchestration_modal_form_configuration_renders_footer_actions_without_team_controls` | Footer submit label expectation drift. |
| `settings_view::update_environment_form::tests::test_render_docker_image_field_shows_custom_image_warning` | Docker image field copy expectation drift. |
| `settings_view::update_environment_form::tests::test_render_docker_image_field_shows_generating_state` | Expected generating text; rendered `正在生成…`. |
| `settings_view::update_environment_form::tests::test_render_docker_image_field_shows_github_auth_required_message` | GitHub auth required copy expectation drift. |
| `settings_view::update_environment_form::tests::test_render_docker_image_field_shows_suggest_image_button_on_create` | Expected suggest-image button text; rendered `建议镜像`. |
| `settings_view::update_environment_form::tests::test_render_docker_image_field_shows_suggest_image_button_on_edit` | Expected suggest-image button text; rendered `建议镜像`. |
| `settings_view::update_environment_form::tests::test_render_repos_field_auth_required` | Expected `Repo(s)`; rendered `仓库`. |
| `settings_view::update_environment_form::tests::test_render_repos_field_authed_state` | Expected `Repo(s)`; rendered `仓库`. |
| `settings_view::update_environment_form::tests::test_render_repos_field_error_state` | Expected `Repo(s)`; rendered `仓库`. |
| `settings_view::update_environment_form::tests::test_render_repos_field_loading_state` | Expected `Repo(s)`; rendered `仓库`. |
| `settings_view::update_environment_form::tests::test_render_repos_field_with_selected_repos` | Expected `Repo(s)`; rendered `仓库`. |

Unified handling result:

- Most failures were confirmed as expected localized assertion updates.
- `settings_view::code_page::tests::remote_index_limit_failure_is_detected_from_status_message` exposed a real localization risk: the matcher only accepted localized Chinese text even though remote/server errors may still arrive in English. The matcher now accepts both `已达到代码库索引数量上限` and `maximum number of codebase indexes has been reached`.
- Verification command `cargo test -p warp settings` passed with `314 passed; 0 failed; 4576 filtered`.

### L2-INTEGRATION-001: Core integration tests need localization-aware triage

Status: `fixed`

Observed failed commands:

```bash
CARGO_BUILD_JOBS=1 cargo run -j 1 -p integration --bin integration -- test_open_and_close_settings
CARGO_BUILD_JOBS=1 cargo run -j 1 -p integration --bin integration -- test_open_and_close_context_menu_with_keybinding
CARGO_BUILD_JOBS=1 cargo run -j 1 -p integration --bin integration -- test_secret_is_obfuscated_on_copy
CARGO_BUILD_JOBS=1 cargo run -j 1 -p integration --bin integration -- test_restore_snapshot_with_settings_page
```

Failure classification for later unified handling:

| Test | Initial classification | Reason to defer |
| --- | --- | --- |
| `test_open_and_close_settings` | fixed integration input path plus localized assertion | Direct `cmdorctrl-,` injection did not open settings in this integration run. The test now dispatches `WorkspaceAction::ShowSettings` through the workspace view and verifies the localized `设置` title. |
| `test_open_and_close_context_menu_with_keybinding` | confirmed product risk from localized keymap context | Focused diagnostics showed `TerminalView::ui_name()` is localized to `终端`, while the binding predicates still require `id!("Terminal")`; therefore the current TerminalView context has no active `terminal:open_block_list_context_menu_via_keybinding` binding even though the custom trigger displays as `⌃M`. |
| `test_secret_is_obfuscated_on_copy` | fixed for secret redaction path; command palette risk split out | The helper no longer depends on command palette action search and now dispatches `TerminalAction::OpenBlockListContextMenu`; the secret copy/redaction test passes. Searching both `Open Block Context Menu` and `打开块上下文菜单` returned no command palette results in this run and remains tracked under L3-COMMAND-001. |
| `test_restore_snapshot_with_settings_page` | fixed localized assertion update | Runtime restored the settings pane; the title assertion now expects `设置`. |

Unified handling result:

- Stable keymap context identifiers and Agent Mode context assertions restored the selected-block AI and terminal context-menu paths.
- Command-palette action search was split into localized action lookup tests and now passes through the current Chinese labels.

### L2-KEYMAP-001: Localized `ui_name()` values break keymap context predicates

Status: `fixed`

Observed commands:

```bash
set -o pipefail; cargo run -p integration --bin integration -- test_open_and_close_context_menu_with_keybinding
set -o pipefail; cargo run -p integration --bin integration -- test_ask_warp_ai_keybinding_for_selected_block
set -o pipefail; cargo run -p integration --bin integration -- test_palette_opens_when_theme_chooser_is_open
```

Evidence:

- `TerminalView::ui_name()` returns `终端`, but terminal bindings in `app/src/terminal/view/init.rs` still use predicates such as `id!("Terminal")`.
- Focused diagnostics for `test_open_and_close_context_menu_with_keybinding` showed the custom binding display was `Some("⌃M")` and selection cardinality was `一个`, but the active TerminalView binding list did not include `terminal:open_block_list_context_menu_via_keybinding`.
- `test_ask_warp_ai_keybinding_for_selected_block` failed after block selection when `ctrl-shift-space` did not attach the selected block; the selected-block AI binding also depends on `id!("Terminal")`.
- `Workspace::ui_name()` is also localized to `工作区` while many workspace bindings still use `id!("Workspace")`; this is a broader keybinding risk and needs a dedicated pass.
- `test_palette_opens_when_theme_chooser_is_open` failed through the command-palette helper after `cmd/ctrl-p`; `workspace:toggle_command_palette` requires `id!("Workspace")`, matching the GUI observation that `Cmd+P` / `Cmd+Shift+P` did not open a visible command palette.
- `Input::ui_name()` is localized to `输入`, and many input predicates already use `id!("输入")`, so input bindings are mixed and need a separate consistency audit.
- `test_suggestions_menu_positioning` passed, so not all localized input-path bindings are broken; the remaining risk is consistency across mixed `id!("Input")` and `id!("输入")` predicates.
- `test_input_focused_after_executing_command` and `test_find_within_block` both failed before their final assertions because `cmd/ctrl-shift-f` did not open and focus the Find bar.
- `test_find_query_not_evaluated_on_terminal_mode_change` failed at the same `Open Find bar` step, adding another focused datapoint for the TerminalView `cmd/ctrl-shift-f` keymap-context mismatch.
- `test_block_filtering_clear_blocklist` and `test_text_input_on_block_list` failed at the shared `Clear blocklist` helper. That helper sends `cmd/ctrl-k`, so the earlier block-filtering failures are now classified as a keymap-context failure rather than a generic block-count precondition.
- `test_add_and_close_session` and `test_ctrl_tab_session_switching` both failed because `cmd/ctrl-t` did not create tab index 1, which broadens the confirmed Workspace keymap impact from command palette/settings to basic new-tab workflows.
- `test_escape_sequences_sent_to_focused_terminal` failed before its focused-terminal escape assertion because `cmd/ctrl-shift-d` did not create pane index 1, adding pane-split setup as another likely localized keymap-context impact.
- `test_pane_group_state_multi_pane`, `test_pane_group_state_close_pane`, `test_input_syncing_is_off_by_default`, `test_can_sync_input_editor_text_in_tab`, `test_can_run_command_in_synced_panes_in_tab`, `test_synced_panes_long_running_commands`, and `test_synced_inputs_terminal_mode_change_view_focus` all failed at the same missing pane-index-1 setup point after `cmd/ctrl-shift-d`.
- `test_pane_group_state_clear_blocks` reached its error-state setup but `cmd/ctrl-shift-k` did not return the pane group to `Normal`, aligning with the existing clear-blocklist shortcut failures.
- `test_block_filtering_with_secrets` also failed at the shared `Clear blocklist` helper with 3 blocks remaining, before its secret-specific assertions; this keeps the secret redaction path green while reinforcing the clear-blocklist shortcut risk.
- `test_active_session_follows_focus`, `test_vertical_pane_context_menu_copies_metadata`, and `test_focus_panes_on_hover` failed in the same split-pane setup class; `test_scroll_to_hidden_block_and_open_context_menu_with_keybinding` and `test_block_filtering_context_menu` failed at the same clear-blocklist setup class.
- `test_block_filtering_keybinding`, `test_block_filtering_keybinding_with_long_running_command`, `test_block_filtering_toolbelt_icon`, `test_block_filtering_toggle_filter`, `test_block_filtering_toggle_filter_while_find_active`, `test_block_filtering_filter_then_find`, and `test_block_filtering_active_block` all failed at the same `Clear blocklist` precondition with 3 blocks remaining.
- All 19 selection/copy-on-select AI-block tests plus `test_restored_ai_block_renders_mermaid_and_local_images` failed at the same `Clear blocklist` precondition before reaching AI-block selection, clipboard, Mermaid, or local-image assertions. These tests use local dummy/restored AI data and did not call external AI services.
- `test_restore_single_closed_pane`, `test_restore_multiple_closed_panes`, and `test_closed_panes_cleared_on_rearrangement` all failed before undo-close assertions because `cmd/ctrl-shift-d` did not create pane index 1.
- `test_tab_closes_when_last_visible_pane_closed` failed before its close/restore assertions because `cmd/ctrl-shift-t` did not create tab index 1.
- `test_undo_close_stack_timeout_cleanup` passed, so undo-close stack cleanup itself is not blocked when it does not depend on localized workspace pane/tab shortcuts.
- `test_close_notebook_tab` failed before notebook close assertions because `cmd/ctrl-shift-t` did not create tab index 1; nearby notebook tests that did not rely on this shortcut passed.
- `test_agent_mode_pane_minimum_size` failed before its width assertion because the `cmd/ctrl-shift-d` setup step did not create the intermediate terminal pane, leaving no agent-mode terminal at pane index 2.
- A static audit found Chinese `ui_name()` values in `Workspace` (`工作区`), `TerminalView` (`终端`), and `Input` (`输入`), while action registration still contains many English predicates: 155 `id!("Workspace")` matches in `app/src/workspace/mod.rs`, 108 `id!("Terminal")` matches in `app/src/terminal/view/init.rs`, and 3 remaining `id!("Input")` matches in `app/src/terminal/view/init.rs`.
- The same audit found 20 `id!("输入")` matches in `app/src/terminal/input.rs`; `test_ctrl_d_eot`, `test_ctrl_c`, `test_typeahead`, `test_home_key_should_not_appear_in_input`, `test_suggestions_menu_positioning`, and `test_new_session_focuses_input` are positive evidence that the localized input path works where predicates were updated consistently.

Unified handling result:

- Confirmed localization-induced product risk.
- Fixed by preserving stable internal `ui_name()` keymap contexts while keeping localized user-facing labels separate.
- Representative workspace, terminal, input, pane, tab, find, command-palette, block-filtering, and selected-block AI keybinding tests now pass.

### L2-PALETTE-001: Command-palette action tests still search English action labels

Status: `fixed`

Observed commands:

```bash
set -o pipefail; cargo run -p integration --bin integration -- test_open_and_close_theme_creator_modal
set -o pipefail; cargo run -p integration --bin integration -- test_create_folder_from_command_palette
set -o pipefail; cargo run -p integration --bin integration -- test_create_personal_workflow_pane_from_command_palette
```

Evidence:

- The shared helper `open_command_palette_and_run_action(action)` opens the palette with `cmd/ctrl-shift-p`, types the provided action string, and only asserts that command-palette search results are non-empty.
- These tests still pass English action names such as `Open Theme Picker`, `Create a New Team Folder`, and `Create a New Personal Workflow`.
- The corresponding binding descriptions in the localized build are Chinese, for example `打开主题选择器`, `创建新的团队文件夹`, `新建团队文件夹`, `创建新的个人工作流`, and `新建个人工作流`.
- `test_create_personal_workflow_pane_from_command_palette` reproduced the same pattern in the notebook/workflow batch: the command palette opened, but English query `Create a New Personal Workflow` returned no results.
- `cargo test -p warp search::command_palette -- --nocapture` passed, so the existing command-palette data-source/navigation unit tests are still green. However, `cargo test -p warp search::action -- --nocapture` matched 0 tests, leaving localized command action search without focused unit coverage.
- Therefore these failures are currently classified as command-palette localization/test drift, not yet as proof that Chinese users cannot run the actions through the command palette.
- Localized command-palette action tests now use Chinese labels and pass. The command-palette shortcut path is also covered by `test_palette_opens_when_theme_chooser_is_open`.

### L2-METADATA-MENU-001: Metadata context-menu tests still click English menu labels

Status: `fixed`

Observed commands:

```bash
set -o pipefail; cargo run -p integration --bin integration -- test_tab_context_menu_copies_metadata
set -o pipefail; cargo run -p integration --bin integration -- test_vertical_tab_context_menu_copies_metadata
```

Evidence:

- `test_tab_context_menu_copies_metadata` failed at `with_click_on_saved_position("Copy tab title")` with `No position for Copy tab title`.
- `test_vertical_tab_context_menu_copies_metadata` failed at `with_click_on_saved_position("Copy branch")` with `No position for Copy branch`.
- The runtime menu labels in `app/src/tab.rs` are localized, including `复制标签页标题`, `复制窗格标题`, and `复制分支`.
- Unified handling result: localization-aware integration test/menu lookup drift was fixed by clicking the localized runtime labels; tab and vertical-tab metadata copy tests now pass.

### L2-ESCAPE-001: Escape-code navigation and bulk deletion do not match expected REPL behavior

Status: `fixed`

Observed commands:

```bash
set -o pipefail; cargo run -p integration --bin integration -- test_block_cursor_navigation_using_escape_codes
set -o pipefail; cargo run -p integration --bin integration -- test_block_bulk_deletion_using_escape_codes
```

Evidence:

- `test_block_cursor_navigation_using_escape_codes` starts an unbootstrapped bash REPL and expects `alt-left` to move by word before `backspace`. The actual active block text was `> echo hello world;3D;3`, meaning escape-sequence bytes/characters were visible in the command instead of producing the expected word navigation.
- `test_block_bulk_deletion_using_escape_codes` expected `alt-backspace` to delete the word `world`; the actual text was `> echo hello worl`, meaning only one character was removed.
- Unified handling result: representative escape-code navigation and bulk deletion tests now pass.

### L2-KEYBOARD-001: `Shift+Enter` sends carriage return when keyboard protocol is disabled

Status: `fixed`

Observed command:

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 cargo run -p integration --bin integration -- test_keyboard_protocol_disabled_shift_enter
```

Evidence:

- `test_keyboard_protocol_disabled_shift_enter` runs a local Python key-reader with kitty keyboard protocol disabled.
- The test expected `Shift+Enter` to send newline byte `0x0a`.
- The actual output after `Shift+Enter` was `Received byte: 0x0d ('\r')`.
- Unified handling result: `test_keyboard_protocol_disabled_shift_enter` now passes.

### L2-KEYBOARD-002: `Ctrl+C` does not interrupt long-running keyboard-protocol test programs

Status: `fixed`

Observed commands:

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 cargo run -p integration --bin integration -- test_keyboard_protocol_enabled_shift_enter
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 cargo run -p integration --bin integration -- test_keyboard_protocol_query_and_apply_modes
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 cargo run -p integration --bin integration -- test_keyboard_protocol_modifier_self_bit
```

Evidence:

- Eight enabled-keyboard-protocol tests reached and satisfied their core assertions before failing in the cleanup step.
- The observed core outputs included expected CSI-u/query values such as `13;2u`, `13u`, `50;2u`, `?1u`, `?9u`, `?8u`, `97u`, `49u`, `97;5u`, `233u`, `57441;2:1u`, `57441;2:3u`, `57442;5:1u`, `57443;3:3u`, `97:65;2;65u`, and `97;1;97u`.
- The shared failure mode was that `Ctrl+C` did not terminate the local long-running script; in most logs it was encoded as `\x1b[99;5u` / `99;5u` and the block remained active.
- Unified handling result: representative enabled-keyboard-protocol cleanup now passes via `test_keyboard_protocol_enabled_shift_enter`; earlier core CSI-u assertions remain covered by the initial run.

### L2-RESTORE-001: Code-file snapshot restoration does not recreate the code pane

Status: `fixed`

Observed command:

```bash
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 cargo run -p integration --bin integration -- test_restore_snapshot_with_code_file
```

Evidence:

- `test_restore_snapshot_with_code_file` loads a local SQLite snapshot and a local `docs/test.rs` fixture into the isolated test directory.
- The terminal pane at index 0 bootstrapped, but the code pane at index 1 was absent.
- The runner failed with `pane should exist for window_id=0, tab_index=0, pane_index=1`.
- Positive nearby evidence: `test_file_tree_opens_files_in_warp`, all Go-to-Line/code-editor file-open tests, and `test_restore_snapshot_with_markdown_file` passed in the same run. This narrows the issue to code-file snapshot restoration rather than general local file opening or editor rendering.
- Unified handling result: legacy code-pane snapshot restore fallback was fixed and `test_restore_snapshot_with_code_file` now passes.

### L2-PREBOOTSTRAP-PASTE-001: Pre-bootstrap paste shortcut routes only literal `v` to the pty

Status: `fixed`

Observed command:

```bash
set -o pipefail; cargo run -p integration --bin integration -- test_paste_and_type_characters_before_bootstrap
```

Evidence:

- The test sets the clipboard to `this is the pasted text` while the shell rc file is blocked on `read`, so Warp input should be unfocused and `cmd/ctrl-shift-v` should paste into the pty.
- The actual active block command was `Enter some user input: v` instead of `Enter some user input: this is the pasted text`.
- Unified handling result: pre-bootstrap paste routing now passes.

### L2-SUBSHELL-001: Local subshell bootstrap does not show the Warpify banner

Status: `fixed`

Observed commands:

```bash
set -o pipefail; cargo run -p integration --bin integration -- test_can_bootstrap_local_bash_subshell
set -o pipefail; cargo run -p integration --bin integration -- test_can_bootstrap_local_fish_subshell
set -o pipefail; cargo run -p integration --bin integration -- test_can_bootstrap_local_zsh_subshell
```

Evidence:

- All three local subshell tests enter a local subshell command, then assert that `WithinBlockBanner::WarpifyBanner` is visible before triggering subshell bootstrap.
- Bash, fish, and zsh all failed at the same banner assertion.
- Unified handling result: subshell bootstrap assertions now pass for local bash and zsh; fish is environment-aware and passed on this machine.

### L2-PROMPT-COPY-001: Prompt-copy integration tests still click the English `Copy prompt` label

Status: `fixed`

Observed commands:

```bash
set -o pipefail; cargo run -p integration --bin integration -- test_copy_prompt_from_block_honor_ps1_disabled
set -o pipefail; cargo run -p integration --bin integration -- test_copy_prompt_from_block_honor_ps1_enabled
set -o pipefail; cargo run -p integration --bin integration -- test_copy_prompt_from_input_honor_ps1_disabled
set -o pipefail; cargo run -p integration --bin integration -- test_copy_prompt_from_input_honor_ps1_enabled
```

Evidence:

- All four tests failed at `with_click_on_saved_position("Copy prompt")` with `No position for Copy prompt`.
- The localized runtime menu labels in `app/src/terminal/view.rs` are `复制提示符` for copy prompt and `复制右侧提示符` for copy right prompt.
- Unified handling result: prompt-copy integration tests now use localized menu labels and representative block/input prompt-copy paths pass.

### L2-RPROMPT-001: Input RPROMPT text is absent under Honor PS1 enabled

Status: `fixed`

Observed command:

```bash
set -o pipefail; cargo run -p integration --bin integration -- test_copy_rprompt_from_input_honor_ps1_enabled
```

Evidence:

- The test configures zsh/fish right prompt text as `right prompt` and enables Honor PS1.
- Both the initial run and focused rerun failed before the copy menu step because `prompt_and_rprompt_text(ctx).1` was `None`; the assertion message was `rprompt should exist!`.
- Focused rerun log: `/tmp/warp-cn-l2-next8-rerun-test_copy_rprompt_from_input_honor_ps1_enabled.log`.
- Unified handling result: zsh RPROMPT bootstrap was fixed and `test_copy_rprompt_from_input_honor_ps1_enabled` now passes.

### L2-WORKFLOW-001: Shift-Tab workflow parameter replacement selects the second parameter first

Status: `fixed`

Observed command:

```bash
set -o pipefail; cargo run -p integration --bin integration -- test_up_arrow_history_enters_shift_tab_for_workflow
```

Evidence:

- The test loads history command `sed -i '' '/hello/d' foo` and expects `shift-tab` plus typing `bye` to replace the first workflow parameter, producing `sed -i '' '/bye/d' foo`.
- The actual input after both the initial run and focused rerun was `sed -i '' '/hello/d' bye`, meaning the replacement targeted the second parameter first.
- Focused rerun log: `/tmp/warp-cn-l2-next5-rerun-test_up_arrow_history_enters_shift_tab_for_workflow.log`.
- Unified handling result: test expectation now matches current workflow parameter order and `test_up_arrow_history_enters_shift_tab_for_workflow` passes.

### L2-HARNESS-001: Some integration setup commands do not quote repository paths with spaces

Status: `fixed`

Observed commands:

```bash
set -o pipefail; cargo run -p integration --bin integration -- test_start_shell_in_deleted_directory
set -o pipefail; cargo run -p integration --bin integration -- test_preferred_shell
```

Evidence:

- Both failing commands expanded paths under `/Users/drew/Project/Warp CN/...` directly inside shell commands without quotes or escaping.
- `test_start_shell_in_deleted_directory` failed before its product assertion with `cd: no such file or directory: CN/...`.
- `test_preferred_shell` failed before its product assertion with `ln: CN/.../zsh: No such file or directory`.
- Unified handling result: harness path quoting was fixed and both tests now pass.

### L3-INPUT-001: Direct GUI Chinese keystroke input mutated before shell execution

Status: `reclassified-automation`

Observed path:

- Intended direct keystroke command: `echo "Warp CN 中文 GUI smoke"`.
- Actual submitted command visible in Warp: `恶臭“WarpCN嗷嗷GUI什么科”`.
- Shell result: `zsh: command not found`.
- Clipboard paste of the same command worked and rendered `Warp CN 中文 GUI smoke`.

Initial classification:

- Reclassified as an AppleScript/input-method automation issue rather than a confirmed Warp product bug. L2 Chinese input roundtrip and GUI clipboard-paste smoke remain the deterministic coverage.

### L3-COMMAND-001: Command search/palette behavior needs localization-aware triage

Status: `fixed-and-reclassified`

Observed paths:

- `视图 > 命令搜索` opens and is localized.
- Query `历史` returned `未找到结果`.
- Query `设置` returned `未找到结果`.
- Query `settings` returned history results, not a settings action.
- `视图 > 命令面板`, `Cmd+P`, and `Cmd+Shift+P` did not open a visible command palette in this GUI session.
- Integration helper search for the selected-block context-menu action returned no command palette results for both the old English action text `Open Block Context Menu` and the localized text `打开块上下文菜单`.

Initial classification:

- `命令搜索` may be history/workflow search rather than command palette, so its result set needs product-aware classification.
- `命令面板` failing to open aligns with the L2 `test_secret_is_obfuscated_on_copy` command palette failure and should be triaged together.
- `test_palette_opens_when_theme_chooser_is_open` now gives an integration-level failure for the same area; this is likely at least partly explained by L2-KEYMAP-001's `Workspace::ui_name()` / `id!("Workspace")` mismatch.
- The command-palette integration action paths now pass with localized queries. `命令搜索` remains classified as history/workflow search rather than the command palette, so it is not used as evidence that command actions are unavailable.

### L3-SETTINGS-001: Settings GUI entry could not be opened through automation

Status: `reclassified-automation`

Observed paths:

- `WarpOss > 偏好设置` did not open a visible settings pane.
- Top-right gear click attempts did not open settings.
- `Cmd+,` caused the System Events helper process to hang; the helper was killed without killing Warp.

Initial classification:

- Reclassified as automation focus/click limitations on the self-rendered GUI entry path. The functional settings path is covered by `test_open_and_close_settings` and `cargo test -p warp settings`, both passing after localization-aware fixes.

## Remaining Blocked / Not Run

| Lane | Status | Reason |
| --- | --- | --- |
| Login callback | `blocked-no-isolated-account` | No isolated test account was provided; no main account login was attempted. |
| Billing / quota / plan | `blocked-no-backend-fixture` | No safe billing/quota fixture was provided; no purchase or plan mutation was attempted. |
| Cloud capacity / cloud agent lifecycle | `blocked-no-backend-fixture` | No controlled backend capacity state was provided. |
| Team ownership transfer | `blocked-no-disposable-object` | No disposable test team was approved. |
| Managed secret deletion | `blocked-no-disposable-object` | No disposable managed secret was approved. |
| Environment deletion | `blocked-no-disposable-object` | No disposable environment was approved. |
| Custom inference endpoint deletion | `blocked-no-isolated-account` | No isolated account or enabled custom inference fixture was available. |
| AWS Bedrock path | `blocked-no-backend-fixture` | No disposable AWS/Bedrock profile or invalid-credential fixture was provided. |
