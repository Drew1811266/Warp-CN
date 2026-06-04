//! Tips for cloud mode loading screen.

use warpui::keymap::Keystroke;
use warpui::AppContext;

use crate::ai::agent_tips::AITip;

/// A cloud mode tip with text and optional link.
#[derive(Clone, Debug)]
pub struct CloudModeTip {
    text: String,
    link: Option<String>,
}

impl CloudModeTip {
    pub fn new(text: impl Into<String>, link: Option<impl Into<String>>) -> Self {
        Self {
            text: text.into(),
            link: link.map(|l| l.into()),
        }
    }
}

impl AITip for CloudModeTip {
    fn keystroke(&self, _app: &AppContext) -> Option<Keystroke> {
        None
    }

    fn link(&self) -> Option<String> {
        self.link.clone()
    }

    fn description(&self) -> &str {
        &self.text
    }

    // Uses the default implementation which adds "Tip: " prefix and parses backticks as inline code
}

/// Returns a collection of tips for the cloud mode loading screen.
pub fn get_cloud_mode_tips() -> Vec<CloudModeTip> {
    vec![
        CloudModeTip::new(
            "安装 Oz Slack 集成，即可从任意频道或私信触发 Agent。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/integrations/slack"),
        ),
        CloudModeTip::new(
            "使用 Oz 的 TypeScript 和 Python SDK 构建可编程 Agent。",
            Some("https://docs.warp.dev/reference/api-and-sdk"),
        ),
        CloudModeTip::new(
            "使用 `oz secret` 命令为 Agent 设置团队或个人密钥。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/secrets"),
        ),
        CloudModeTip::new(
            "在 Oz Web 应用中查看所有 Agent 运行及其状态。",
            Some("https://oz.warp.dev"),
        ),
        CloudModeTip::new(
            "使用 Agent Session Sharing 实时加入任意 Oz 云端 Agent 运行。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/viewing-cloud-agent-runs"),
        ),
        CloudModeTip::new(
            "设置按 cron 计划运行的周期性 Agent，用于自动维护。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/triggers/scheduled-agents"),
        ),
        CloudModeTip::new(
            "创建 Agent，在 Linear 中提交 issue 时自动修复 bug。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/integrations/linear"),
        ),
        CloudModeTip::new(
            "构建 Agent 来响应 CI 失败并尝试自动修复。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/integrations/github-actions"),
        ),
        CloudModeTip::new(
            "使用 `oz-agent-action` 从 GitHub Actions 运行 Agent。",
            Some("https://github.com/warpdotdev/oz-agent-action"),
        ),
        CloudModeTip::new(
            "调用 Oz REST API，从任意后端服务或内部工具触发 Agent。",
            Some("https://docs.warp.dev/reference/api-and-sdk"),
        ),
        CloudModeTip::new(
            "使用 Docker 镜像创建可复用环境，确保 Agent 执行一致。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/environments"),
        ),
        CloudModeTip::new(
            "与团队共享 Agent 会话链接以协作调试。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/viewing-cloud-agent-runs"),
        ),
        CloudModeTip::new(
            "在 Oz CLI 中使用 `--share` 标志，即可从任意位置启用会话共享。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/platform"),
        ),
        CloudModeTip::new(
            "将已完成的 Oz 云端 Agent 会话复刻到 Warp，以便在本地继续工作。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/viewing-cloud-agent-runs"),
        ),
        CloudModeTip::new(
            "构建使用 Agent 回答数据库问题的内部工具。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/integrations"),
        ),
        CloudModeTip::new(
            "创建计划 Agent，每周清理过期 feature flag。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/triggers/scheduled-agents"),
        ),
        CloudModeTip::new(
            "在 Linear issue 中标记 @Oz，以自动调查并提出修复。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/integrations/linear"),
        ),
        CloudModeTip::new(
            "使用 Oz CLI 在远程开发机或 CI runner 上运行 Agent。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/platform"),
        ),
        CloudModeTip::new(
            "配置 MCP server，让 Oz 云端 Agent 访问 GitHub、Linear 和 Sentry。",
            Some("https://docs.warp.dev/agent-platform/capabilities/mcp"),
        ),
        CloudModeTip::new(
            "使用 `oz agent run` 启动任务，无需打开 Warp 终端。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/platform"),
        ),
        CloudModeTip::new(
            "在 Oz Web 应用中查看团队成员的 Agent 运行，以共享可见性。",
            Some("https://oz.warp.dev"),
        ),
        CloudModeTip::new(
            "构建 Agent，自动分流并标记新进入的 GitHub issue。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/integrations/github-actions"),
        ),
        CloudModeTip::new(
            "设置 Agent，每天生成新开 issue 的摘要。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/integrations/github-actions"),
        ),
        CloudModeTip::new(
            "创建 Agent，自动审查 PR 并提出改进建议。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/integrations/github-actions"),
        ),
        CloudModeTip::new(
            "使用 `oz environment create` 定义可复现的执行上下文。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/environments"),
        ),
        CloudModeTip::new(
            "通过 webhook 触发 Agent，以响应生产事故。",
            Some("https://docs.warp.dev/reference/api-and-sdk"),
        ),
        CloudModeTip::new(
            "构建 Agent，在告警触发时重启服务或扩缩部署。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/triggers"),
        ),
        CloudModeTip::new(
            "使用个人密钥保存仅供你的 Agent 使用的凭据。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/secrets"),
        ),
        CloudModeTip::new(
            "使用团队密钥保存所有 Agent 共享的基础设施凭据。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/secrets"),
        ),
        CloudModeTip::new(
            "创建每晚运行的 Agent，用于检查依赖更新。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/triggers/scheduled-agents"),
        ),
        CloudModeTip::new(
            "构建按计划自动格式化和 lint 代码的 Agent。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/triggers/scheduled-agents"),
        ),
        CloudModeTip::new(
            "使用 `oz schedule create` 设置由 cron 触发的 Agent。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/triggers/scheduled-agents"),
        ),
        CloudModeTip::new(
            "使用 `oz schedule pause` 暂停和恢复计划 Agent，而无需删除它们。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/triggers/scheduled-agents"),
        ),
        CloudModeTip::new(
            "使用 `oz mcp list` 查看 Agent 可用的 MCP server。",
            Some("https://docs.warp.dev/agent-platform/capabilities/mcp"),
        ),
        CloudModeTip::new(
            "构建内部 Slack bot，将编码任务委派给 Oz Agent。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/integrations/slack"),
        ),
        CloudModeTip::new(
            "创建 Agent，在 Slack 线程中带完整上下文响应 @ 提及。",
            Some("https://docs.warp.dev/agent-platform/cloud-agents/integrations/slack"),
        ),
        CloudModeTip::new(
            "使用 Oz TypeScript SDK 构建自定义自动化流水线。",
            Some("https://docs.warp.dev/reference/api-and-sdk"),
        ),
        CloudModeTip::new(
            "使用 Oz Python SDK 将 Agent 集成到你的数据流水线中。",
            Some("https://docs.warp.dev/reference/api-and-sdk"),
        ),
        CloudModeTip::new(
            "使用 Oz API 监控 Agent 成功率和运行时长。",
            Some("https://docs.warp.dev/reference/api-and-sdk"),
        ),
        CloudModeTip::new(
            "构建仪表盘，跟踪整个团队的所有 Agent 活动。",
            Some("https://docs.warp.dev/reference/api-and-sdk"),
        ),
    ]
}
