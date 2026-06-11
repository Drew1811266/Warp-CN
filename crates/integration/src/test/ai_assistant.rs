use warp::integration_testing::step::new_step_with_default_assertions;
use warp::integration_testing::terminal::util::ExpectedExitStatus;
use warp::integration_testing::terminal::{
    assert_agent_context_contains_block, assert_selected_block_index_is_last_renderable,
    execute_command_for_single_terminal_in_tab, wait_until_bootstrapped_single_pane_for_tab,
};

use super::new_builder;
use crate::Builder;

/// Checks if the Ask Warp AI keybinding works correctly when a block is selected.
/// This is a regression test: https://linear.app/warpdotdev/issue/WAR-6758/warp-ai-ask-from-block-keybinding-doesnt-work-as-expected.
pub fn test_ask_warp_ai_keybinding_for_selected_block() -> Builder {
    new_builder()
        .with_step(wait_until_bootstrapped_single_pane_for_tab(0))
        .with_step(execute_command_for_single_terminal_in_tab(
            0,
            String::from("echo foo"),
            ExpectedExitStatus::Success,
            "foo",
        ))
        .with_step(
            new_step_with_default_assertions("select block")
                .with_keystrokes(&["cmdorctrl-up"])
                .add_named_assertion(
                    "ensure block is selected",
                    assert_selected_block_index_is_last_renderable(),
                ),
        )
        .with_step(
            new_step_with_default_assertions("attach selected block as agent context")
                .with_keystrokes(&["ctrl-shift-space"])
                .add_named_assertion(
                    "selected block is attached as Agent context",
                    assert_agent_context_contains_block(0, "echo foo", "foo"),
                ),
        )
}
