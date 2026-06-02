use warp_graphql::ai::{AgentTaskState, PlatformErrorCode};

use super::terminal::ShareSessionError;
use super::AgentDriverError;
use crate::ai::blocklist::local_agent_task_sync_model::classify_renderable_error;
use crate::server::server_api::ai::TaskStatusUpdate;

/// Classify an `AgentDriverError` into a task state and a `TaskStatusUpdate`
/// suitable for reporting via `update_agent_task`.
pub fn classify_driver_error(error: &AgentDriverError) -> (AgentTaskState, TaskStatusUpdate) {
    match error {
        // --- Warp-side errors (task → ERROR) ---
        AgentDriverError::TerminalUnavailable | AgentDriverError::InvalidRuntimeState => (
            AgentTaskState::Error,
            TaskStatusUpdate::with_error_code(
                "发生内部错误。请尝试重新运行任务。如果问题仍然存在，请联系支持团队。",
                PlatformErrorCode::InternalError,
            ),
        ),
        AgentDriverError::BootstrapFailed => (
            AgentTaskState::Error,
            TaskStatusUpdate::with_error_code(
                "终端会话启动失败。请尝试重新运行任务。",
                PlatformErrorCode::InternalError,
            ),
        ),
        AgentDriverError::ShareSessionFailed { error: share_err } => {
            let message = match share_err {
                ShareSessionError::Internal(_) => {
                    "由于内部错误，Agent 会话共享失败。请尝试重新运行任务。".to_string()
                }
                ShareSessionError::Failed(reason) => {
                    // The reason string comes from the session-sharing layer and is aimed at
                    // interactive users (e.g. "try sharing again"). Provide a cloud-agent-
                    // appropriate message instead of wrapping it, which would produce
                    // repetitive "try again" text.
                    format!("Agent 会话共享失败：{reason}")
                }
                ShareSessionError::Disabled => {
                    "你的账号未启用会话共享。这可能是因为管理员为你的团队禁用了会话共享。请确认团队设置中已启用会话共享，或尝试不带 --share 标志运行。"
                    .to_string()
                }
                ShareSessionError::Timeout => {
                    "Agent 会话共享失败：等待会话共享服务器响应超时。请检查网络连接后重试。"
                    .to_string()
                }
                ShareSessionError::Interrupted => {
                    "会话共享在完成前被中断。请尝试重新运行任务。".to_string()
                }
            };
            (
                AgentTaskState::Error,
                TaskStatusUpdate::with_error_code(
                    message,
                    match share_err {
                        ShareSessionError::Disabled => PlatformErrorCode::FeatureNotAvailable,
                        _ => PlatformErrorCode::InternalError,
                    },
                ),
            )
        }
        AgentDriverError::WarpDriveSyncFailed => (
            AgentTaskState::Error,
            TaskStatusUpdate::with_error_code(
                "Warp Drive 同步失败。请检查网络连接后重试。",
                PlatformErrorCode::InternalError,
            ),
        ),
        AgentDriverError::NotLoggedIn => {
            let bin = warp_cli::binary_name().unwrap_or_else(|| "warp".to_string());
            (
                AgentTaskState::Error,
                TaskStatusUpdate::with_error_code(
                    format!(
                        "需要认证。请通过 '{bin} login' 登录、通过 '--api-key' 提供 API 密钥，或设置 WARP_API_KEY 环境变量。"
                    ),
                    PlatformErrorCode::AuthenticationRequired,
                ),
            )
        }
        AgentDriverError::CloudProviderSetupFailed(err) => (
            AgentTaskState::Error,
            TaskStatusUpdate::with_error_code(
                format!("配置云端访问时出错：{err:#}"),
                PlatformErrorCode::InternalError,
            ),
        ),

        // --- User-side errors (task → FAILED) ---
        AgentDriverError::MCPServerNotFound(uuid) => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                format!(
                    "未找到 MCP server {uuid}。请确认该 server 存在于你的 Warp Drive 中，且 UUID 正确。"
                ),
                PlatformErrorCode::EnvironmentSetupFailed,
            ),
        ),
        AgentDriverError::MCPStartupFailed => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                "一个或多个 MCP server 启动失败。请检查 MCP server 配置是否有效，并确认 server 进程可以运行。",
                PlatformErrorCode::EnvironmentSetupFailed,
            ),
        ),
        AgentDriverError::MCPJsonParseError(msg) => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                format!("解析 MCP server JSON 配置失败：{msg}"),
                PlatformErrorCode::EnvironmentSetupFailed,
            ),
        ),
        AgentDriverError::MCPMissingVariables => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                "MCP server 配置缺少必需变量。请提供所有必需的环境变量或模板值。",
                PlatformErrorCode::EnvironmentSetupFailed,
            ),
        ),
        AgentDriverError::ProfileError(name) => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                format!(
                    "未找到 Agent 配置文件“{name}”。请检查配置文件 ID，并确保它存在于团队的 Warp Drive 中。"
                ),
                PlatformErrorCode::ResourceNotFound,
            ),
        ),
        AgentDriverError::AIWorkflowNotFound(id) => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                format!(
                    "未找到 ID 为 {id} 的已保存提示词。请确认该提示词存在于你的 Warp Drive 中。"
                ),
                PlatformErrorCode::ResourceNotFound,
            ),
        ),
        AgentDriverError::EnvironmentNotFound(id) => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                format!(
                    "未找到环境 '{id}'。请确认环境 ID，并确保它存在于团队设置中。"
                ),
                PlatformErrorCode::ResourceNotFound,
            ),
        ),
        AgentDriverError::EnvironmentSetupFailed(msg) => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                format!(
                    "环境设置失败：{msg}。请检查仓库 URL 和设置命令。"
                ),
                PlatformErrorCode::EnvironmentSetupFailed,
            ),
        ),
        AgentDriverError::InvalidWorkingDirectory { path, .. } => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                format!(
                    "工作目录 '{}' 不存在或不是目录。请检查环境配置中的路径。",
                    path.display()
                ),
                PlatformErrorCode::EnvironmentSetupFailed,
            ),
        ),

        // --- Conversation errors ---
        // Delegate to classify_renderable_error for proper ERROR vs FAILED
        // distinction and PlatformErrorCode. This is a belt-and-suspenders
        // fallback — LocalAgentTaskSyncModel handles most conversation errors,
        // but the driver catches them too if the conversation ends with an error.
        AgentDriverError::ConversationError { error } => {
            let (state, update) = classify_renderable_error(error);
            (
                state,
                update.unwrap_or_else(|| {
                    TaskStatusUpdate::with_error_code(
                        error.to_string(),
                        PlatformErrorCode::InternalError,
                    )
                }),
            )
        }

        // --- Cancellation / Blocked (no error code) ---
        AgentDriverError::ConversationCancelled { .. } => (
            AgentTaskState::Cancelled,
            TaskStatusUpdate::message("任务已取消。"),
        ),
        AgentDriverError::ConversationBlocked { blocked_action } => (
            AgentTaskState::Blocked,
            TaskStatusUpdate::message(format!(
                "Agent 在等待用户确认操作时卡住：{blocked_action}"
            )),
        ),

        // --- Setup errors ---
        AgentDriverError::TeamMetadataRefreshTimeout => (
            AgentTaskState::Error,
            TaskStatusUpdate::with_error_code(
                "刷新团队元数据超时。请检查网络连接后重试。",
                PlatformErrorCode::InternalError,
            ),
        ),
        AgentDriverError::SkillResolutionFailed(msg) => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                format!("Skill 解析失败：{msg}"),
                PlatformErrorCode::ResourceNotFound,
            ),
        ),
        AgentDriverError::ConfigBuildFailed(err) => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                format!("构建 Agent 配置失败：{err}"),
                PlatformErrorCode::EnvironmentSetupFailed,
            ),
        ),
        AgentDriverError::PromptResolutionFailed(err) => (
            AgentTaskState::Error,
            TaskStatusUpdate::with_error_code(
                format!("解析本次运行的提示词失败：{err}"),
                PlatformErrorCode::InternalError,
            ),
        ),
        AgentDriverError::SecretsFetchFailed(err) => (
            AgentTaskState::Error,
            TaskStatusUpdate::with_error_code(
                format!("获取任务密钥失败：{err}"),
                PlatformErrorCode::InternalError,
            ),
        ),
        AgentDriverError::AwsBedrockCredentialsFailed(msg) => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                format!("初始化 AWS Bedrock 凭据失败：{msg}"),
                PlatformErrorCode::EnvironmentSetupFailed,
            ),
        ),
        AgentDriverError::ConversationLoadFailed(msg) => (
            AgentTaskState::Error,
            TaskStatusUpdate::with_error_code(
                format!("加载对话失败：{msg}"),
                PlatformErrorCode::InternalError,
            ),
        ),
        AgentDriverError::ConversationHarnessMismatch {
            conversation_id,
            expected,
            got,
        } => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                format!(
                    "对话 {conversation_id} 由 {expected} harness 生成，但当前请求了 --harness {got}。请使用 --harness {expected} 重新运行（或省略 --harness）来继续此对话。"
                ),
                PlatformErrorCode::EnvironmentSetupFailed,
            ),
        ),
        AgentDriverError::TaskHarnessMismatch {
            task_id,
            expected,
            got,
        } => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                format!(
                    "任务 {task_id} 使用 {expected} harness 创建，但当前请求了 --harness {got}。请使用 --harness {expected} 重新运行（或省略 --harness）来继续此任务。"
                ),
                PlatformErrorCode::EnvironmentSetupFailed,
            ),
        ),
        AgentDriverError::ConversationResumeStateMissing {
            harness,
            conversation_id,
        } => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                format!(
                    "对话 {conversation_id} 没有 {harness} harness 的已存转录。上一次运行可能在保存状态前崩溃。"
                ),
                PlatformErrorCode::ResourceNotFound,
            ),
        ),
        AgentDriverError::HarnessCommandFailed { exit_code } => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                format!("Harness 命令退出，代码为 {exit_code}"),
                PlatformErrorCode::InternalError,
            ),
        ),
        AgentDriverError::HarnessSetupFailed { harness, reason } => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                format!("Harness '{harness}' 校验失败：{reason}"),
                PlatformErrorCode::EnvironmentSetupFailed,
            ),
        ),
        AgentDriverError::HarnessConfigSetupFailed { harness, error } => (
            AgentTaskState::Failed,
            TaskStatusUpdate::with_error_code(
                format!("Harness '{harness}' config setup failed: {error}"),
                PlatformErrorCode::EnvironmentSetupFailed,
            ),
        ),
        AgentDriverError::HarnessAuthCheckFailed { harness, detail } => {
            let message = format!(
                "Harness '{harness}' 认证检查失败：登录凭据无效或已过期。请确认为此 harness 配置的认证密钥正确。"
            );
            log::error!("Preflight detail for {harness}: {detail}");
            (
                AgentTaskState::Failed,
                TaskStatusUpdate::with_error_code(
                    message,
                    PlatformErrorCode::AuthenticationRequired,
                ),
            )
        }
        AgentDriverError::HarnessRuntimeFailureDetected {
            harness,
            pattern,
            excerpt,
        } => {
            let message = format!(
                "Harness '{harness}' 无法成功发起 API 请求。在 harness 输出中匹配到失败模式 '{pattern}'，输出片段为 {excerpt}。这通常表示 API 密钥无效、点数不足，或账号配置有误。"
            );
            log::error!("Runtime failure for {harness}: pattern={pattern}, excerpt={excerpt}");
            (
                AgentTaskState::Failed,
                TaskStatusUpdate::with_error_code(
                    message,
                    PlatformErrorCode::AuthenticationRequired,
                ),
            )
        }
    }
}

#[cfg(test)]
#[path = "error_classification_tests.rs"]
mod tests;
