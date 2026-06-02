use warp_cli::agent::Harness;
use warp_core::features::FeatureFlag;

pub(crate) fn local_child_harness_disabled_message(harness: Harness) -> Option<&'static str> {
    if FeatureFlag::LocalClaudeCodexChildHarnesses.is_enabled() {
        return None;
    }

    match harness {
        Harness::Claude => Some("本地 Claude Code 子 Agent 暂时已停用。"),
        Harness::Codex => Some("本地 Codex 子 Agent 暂时已停用。"),
        Harness::Oz | Harness::OpenCode | Harness::Gemini | Harness::Unknown => None,
    }
}

pub(crate) fn local_child_harness_is_enabled(harness: Harness) -> bool {
    local_child_harness_disabled_message(harness).is_none()
}
