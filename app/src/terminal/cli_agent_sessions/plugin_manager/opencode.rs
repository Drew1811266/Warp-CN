use std::sync::LazyLock;

use async_trait::async_trait;

use super::{CliAgentPluginManager, PluginInstructionStep, PluginInstructions};

// Keep in sync with the opencode-warp npm package version.
// This version is also hardcoded into UPDATE_INSTRUCTIONS below (so the update
// instructions tell users to pin to this specific version to force OpenCode's
// plugin cache to re-fetch). Update both together.
const MINIMUM_PLUGIN_VERSION: &str = "0.1.5";

pub(super) struct OpenCodePluginManager;

#[async_trait]
impl CliAgentPluginManager for OpenCodePluginManager {
    fn minimum_plugin_version(&self) -> &'static str {
        MINIMUM_PLUGIN_VERSION
    }

    fn can_auto_install(&self) -> bool {
        false
    }

    fn install_instructions(&self) -> &'static PluginInstructions {
        &INSTALL_INSTRUCTIONS
    }

    fn update_instructions(&self) -> &'static PluginInstructions {
        &UPDATE_INSTRUCTIONS
    }
}

static INSTALL_INSTRUCTIONS: LazyLock<PluginInstructions> = LazyLock::new(|| {
    PluginInstructions {
        title: "为 OpenCode 安装 Warp 插件",
        subtitle:
            "将 Warp 插件添加到 OpenCode 配置中，然后重启 OpenCode。",
        steps: &[
            PluginInstructionStep {
                description: "打开或创建 opencode.json。它可以位于项目根目录，也可以位于全局配置路径：",
                command: "~/.config/opencode/opencode.json",
                executable: false,
                link: None,
            },
            PluginInstructionStep {
                description: "Add \"@warp-dot-dev/opencode-warp\" to the \"plugin\" array in the top-level JSON object:",
                command: "\"plugin\": [\"@warp-dot-dev/opencode-warp\"]",
                executable: false,
                link: None,
            },
        ],
        post_install_notes: &["重启 OpenCode 以激活插件。"],
    }
});

static UPDATE_INSTRUCTIONS: LazyLock<PluginInstructions> = LazyLock::new(|| {
    PluginInstructions {
        title: "更新 OpenCode 的 Warp 插件",
        subtitle: "在 opencode.json 中将插件固定到最新版本。OpenCode 会按版本规格缓存插件，因此更改固定版本会在重启时强制重新获取。",
        steps: &[
            PluginInstructionStep {
                description: "打开或创建 opencode.json。它可以位于项目根目录，也可以位于全局配置路径：",
                command: "~/.config/opencode/opencode.json",
                executable: false,
                link: None,
            },
            PluginInstructionStep {
                description: "Replace the existing \"@warp-dot-dev/opencode-warp\" entry in the \"plugin\" array with the explicit version:",
                command: "\"plugin\": [\"@warp-dot-dev/opencode-warp@0.1.5\"]",
                executable: false,
                link: None,
            },
        ],
        post_install_notes: &["重启 OpenCode 以加载更新后的插件。"],
    }
});

#[cfg(test)]
#[path = "opencode_tests.rs"]
mod tests;
