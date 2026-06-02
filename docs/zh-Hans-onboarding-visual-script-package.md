# zh-Hans Onboarding Visual Script Package

Date: 2026-06-02 Asia/Shanghai

## Purpose

This package provides Chinese replacement scripts for the `50` onboarding PNGs
that remain deferred to visual regeneration or design approval.

No PNG was opened, generated, uploaded, or replaced while creating this package.

## Non-Binary Rule

This document is copy guidance only.

- Do not change PNG files in this phase.
- Generate replacement assets only on a separate reversible asset branch.
- Keep filenames and dimensions unchanged unless design explicitly approves a change.
- Capture before/after contact sheets for every changed asset.
- Review only the deferred PNGs listed below.
- Keep the `4` accepted decorative/brand assets unchanged:
  - `app/assets/async/png/onboarding/hoa_welcome_banner.png`
  - `app/assets/async/png/onboarding/onboarding_bg.png`
  - `app/assets/async/png/onboarding/openwarp_launch_banner.png`
  - `app/assets/async/png/onboarding/orchestration_launch_banner.png`

## Script Table

| Asset | Reason category | Chinese replacement script | Layout risk | Review note |
| --- | --- | --- | --- | --- |
| `app/assets/async/png/onboarding/welcome_agent.png` | embedded product UI/text | `使用 AI Agent 更快构建`; `Agent 优先体验，并保留一流终端能力`; `开始使用 AI`; `禁用 AI 功能` | Medium | Match source onboarding terminology and keep `Agent` in English. |
| `app/assets/async/png/onboarding/welcome_terminal.png` | embedded product UI/text | `经典终端与第三方 Agent`; `现代终端，支持 Claude Code、Codex、Gemini CLI 等工作流`; `继续` | Medium | Preserve third-party product names. |
| `app/assets/async/png/onboarding/thirdparty_notifications_disabled.png` | embedded notification copy | `通知`; `Agent 需要你关注`; `已禁用`; `启用通知` | Low | Keep notification badges compact. |
| `app/assets/async/png/onboarding/thirdparty_notifications_enabled.png` | embedded notification copy | `通知`; `Agent 任务已完成`; `已启用`; `不再显示` | Low | Verify Chinese text fits notification card. |
| `app/assets/async/png/onboarding/thirdparty_toolbar_disabled_horizontal.png` | embedded toolbar text | `CLI Agent 工具栏`; `已禁用`; `编辑提示词`; `工具`; `设置` | Medium | Horizontal toolbar labels may need shorter wording. |
| `app/assets/async/png/onboarding/thirdparty_toolbar_disabled_vertical.png` | embedded toolbar text | `CLI Agent 工具栏`; `已禁用`; `编辑`; `工具`; `设置` | Medium | Prefer shorter vertical labels. |
| `app/assets/async/png/onboarding/thirdparty_toolbar_enabled_horizontal.png` | embedded toolbar text | `CLI Agent 工具栏`; `已启用`; `编辑提示词`; `工具`; `设置` | Medium | Keep visual parity with disabled state. |
| `app/assets/async/png/onboarding/thirdparty_toolbar_enabled_vertical.png` | embedded toolbar text | `CLI Agent 工具栏`; `已启用`; `编辑`; `工具`; `设置` | Medium | Prefer shorter vertical labels. |
| `app/assets/async/png/onboarding/agent_intention/customize_codereview_disabled_horizontal.png` | embedded code-review/editor text | `代码审查`; `Diff`; `接受`; `拒绝`; `编辑请求`; `已禁用` | Medium | Preserve `Diff`; keep action labels short. |
| `app/assets/async/png/onboarding/agent_intention/customize_codereview_disabled_vertical.png` | embedded code-review/editor text | `代码审查`; `Diff`; `接受`; `拒绝`; `已禁用` | Medium | Vertical layout needs shorter labels. |
| `app/assets/async/png/onboarding/agent_intention/customize_codereview_enabled_horizontal.png` | embedded code-review/editor text | `代码审查`; `Diff`; `接受`; `拒绝`; `编辑请求`; `已启用` | Medium | Preserve `Diff`; match enabled state. |
| `app/assets/async/png/onboarding/agent_intention/customize_codereview_enabled_vertical.png` | embedded code-review/editor text | `代码审查`; `Diff`; `接受`; `拒绝`; `已启用` | Medium | Vertical layout needs shorter labels. |
| `app/assets/async/png/onboarding/agent_intention/customize_conversation_horizontal.png` | embedded conversation UI text | `Agent 对话`; `开始新对话`; `继续对话`; `对话历史`; `发送` | Medium | Use `对话`, not `会话`, for Agent conversation context. |
| `app/assets/async/png/onboarding/agent_intention/customize_conversation_vertical.png` | embedded conversation UI text | `Agent 对话`; `新对话`; `继续`; `历史`; `发送` | Medium | Use compact vertical labels. |
| `app/assets/async/png/onboarding/agent_intention/customize_fileexplorer_horizontal.png` | embedded sidebar/file explorer labels | `文件`; `文件浏览器`; `搜索文件`; `打开文件`; `当前项目` | Medium | Keep sidebar labels scannable. |
| `app/assets/async/png/onboarding/agent_intention/customize_fileexplorer_vertical.png` | embedded sidebar/file explorer labels | `文件`; `浏览器`; `搜索`; `当前项目` | Medium | Use shorter labels for narrow sidebar. |
| `app/assets/async/png/onboarding/agent_intention/customize_filesearch_horizontal.png` | embedded search UI text | `搜索文件`; `输入文件名`; `最近文件`; `打开` | Low | Placeholder must not overflow search field. |
| `app/assets/async/png/onboarding/agent_intention/customize_filesearch_vertical.png` | embedded search UI text | `搜索文件`; `文件名`; `最近`; `打开` | Low | Use compact placeholder. |
| `app/assets/async/png/onboarding/agent_intention/customize_horizontal_tabs.png` | embedded tab/sidebar labels | `终端`; `Agent`; `新建标签页`; `共享会话`; `关闭标签页` | Medium | Match horizontal tab UI language. |
| `app/assets/async/png/onboarding/agent_intention/customize_vertical_tabs.png` | embedded tab/sidebar labels | `终端`; `Agent`; `标签页`; `工作区`; `关闭` | Medium | Match vertical tab UI language. |
| `app/assets/async/png/onboarding/agent_intention/customize_tools_disabled_horizontal.png` | embedded toolbar/tool text | `工具`; `MCP`; `权限`; `已禁用`; `请求权限` | Medium | Preserve `MCP`. |
| `app/assets/async/png/onboarding/agent_intention/customize_tools_disabled_vertical.png` | embedded toolbar/tool text | `工具`; `MCP`; `权限`; `禁用` | Medium | Prefer shorter vertical labels. |
| `app/assets/async/png/onboarding/agent_intention/customize_warpdrive_horizontal.png` | embedded Warp Drive/sidebar labels | `Warp Drive`; `工作流`; `笔记本`; `环境变量`; `规则` | Medium | Preserve `Warp Drive`. |
| `app/assets/async/png/onboarding/agent_intention/customize_warpdrive_vertical.png` | embedded Warp Drive/sidebar labels | `Warp Drive`; `工作流`; `笔记本`; `环境`; `规则` | Medium | Preserve `Warp Drive`; shorten `环境变量` if needed. |
| `app/assets/async/png/onboarding/agent_intention/theme/theme_adeberry_horizontal.png` | embedded terminal/editor preview text | `运行测试`; `构建完成`; `Agent 正在分析`; `打开文件` | Medium | Theme image can use neutral sample text; avoid real code claims. |
| `app/assets/async/png/onboarding/agent_intention/theme/theme_adeberry_vertical.png` | embedded terminal/editor preview text | `运行测试`; `完成`; `Agent 分析`; `文件` | Medium | Keep vertical preview compact. |
| `app/assets/async/png/onboarding/agent_intention/theme/theme_dark_horizontal.png` | embedded terminal/editor preview text | `运行测试`; `构建完成`; `Agent 正在分析`; `打开文件` | Medium | Same script as theme variants for consistency. |
| `app/assets/async/png/onboarding/agent_intention/theme/theme_dark_vertical.png` | embedded terminal/editor preview text | `运行测试`; `完成`; `Agent 分析`; `文件` | Medium | Same script as theme variants for consistency. |
| `app/assets/async/png/onboarding/agent_intention/theme/theme_light_horizontal.png` | embedded terminal/editor preview text | `运行测试`; `构建完成`; `Agent 正在分析`; `打开文件` | Medium | Same script as theme variants for consistency. |
| `app/assets/async/png/onboarding/agent_intention/theme/theme_light_vertical.png` | embedded terminal/editor preview text | `运行测试`; `完成`; `Agent 分析`; `文件` | Medium | Same script as theme variants for consistency. |
| `app/assets/async/png/onboarding/agent_intention/theme/theme_phenomenon_horizontal.png` | embedded terminal/editor preview text | `运行测试`; `构建完成`; `Agent 正在分析`; `打开文件` | Medium | Same script as theme variants for consistency. |
| `app/assets/async/png/onboarding/agent_intention/theme/theme_phenomenon_vertical.png` | embedded terminal/editor preview text | `运行测试`; `完成`; `Agent 分析`; `文件` | Medium | Same script as theme variants for consistency. |
| `app/assets/async/png/onboarding/terminal_intention/terminal_codereview_disabled.png` | embedded code-review/editor text | `代码审查`; `Diff`; `接受`; `拒绝`; `已禁用` | Medium | Preserve `Diff`; keep labels short. |
| `app/assets/async/png/onboarding/terminal_intention/terminal_codereview_enabled.png` | embedded code-review/editor text | `代码审查`; `Diff`; `接受`; `拒绝`; `已启用` | Medium | Match disabled state composition. |
| `app/assets/async/png/onboarding/terminal_intention/terminal_customize_fileexplorer_horizontal.png` | embedded sidebar/file explorer labels | `文件`; `文件浏览器`; `搜索文件`; `打开文件`; `当前项目` | Medium | Same as Agent-intention file explorer horizontal. |
| `app/assets/async/png/onboarding/terminal_intention/terminal_customize_fileexplorer_vertical.png` | embedded sidebar/file explorer labels | `文件`; `浏览器`; `搜索`; `当前项目` | Medium | Same as Agent-intention file explorer vertical. |
| `app/assets/async/png/onboarding/terminal_intention/terminal_customize_filesearch_horizontal.png` | embedded search UI text | `搜索文件`; `输入文件名`; `最近文件`; `打开` | Low | Placeholder must not overflow search field. |
| `app/assets/async/png/onboarding/terminal_intention/terminal_customize_filesearch_vertical.png` | embedded search UI text | `搜索文件`; `文件名`; `最近`; `打开` | Low | Use compact placeholder. |
| `app/assets/async/png/onboarding/terminal_intention/terminal_customize_horizontal_tabs.png` | embedded tab/sidebar labels | `终端`; `新建标签页`; `共享会话`; `关闭标签页` | Medium | Terminal-intention version should not imply Agent-first flow. |
| `app/assets/async/png/onboarding/terminal_intention/terminal_customize_vertical_tabs.png` | embedded tab/sidebar labels | `终端`; `标签页`; `工作区`; `关闭` | Medium | Keep vertical labels compact. |
| `app/assets/async/png/onboarding/terminal_intention/terminal_customize_warpdrive_horizontal.png` | embedded Warp Drive/sidebar labels | `Warp Drive`; `工作流`; `笔记本`; `环境变量`; `规则` | Medium | Preserve `Warp Drive`. |
| `app/assets/async/png/onboarding/terminal_intention/terminal_customize_warpdrive_vertical.png` | embedded Warp Drive/sidebar labels | `Warp Drive`; `工作流`; `笔记本`; `环境`; `规则` | Medium | Preserve `Warp Drive`; shorten if needed. |
| `app/assets/async/png/onboarding/terminal_intention/theme/theme_adeberry_horizontal.png` | embedded terminal/editor preview text | `运行命令`; `测试通过`; `构建完成`; `打开项目` | Medium | Terminal-intention theme sample should focus on commands. |
| `app/assets/async/png/onboarding/terminal_intention/theme/theme_adeberry_vertical.png` | embedded terminal/editor preview text | `运行命令`; `通过`; `完成`; `项目` | Medium | Keep vertical preview compact. |
| `app/assets/async/png/onboarding/terminal_intention/theme/theme_dark_horizontal.png` | embedded terminal/editor preview text | `运行命令`; `测试通过`; `构建完成`; `打开项目` | Medium | Same script as terminal theme variants for consistency. |
| `app/assets/async/png/onboarding/terminal_intention/theme/theme_dark_vertical.png` | embedded terminal/editor preview text | `运行命令`; `通过`; `完成`; `项目` | Medium | Same script as terminal theme variants for consistency. |
| `app/assets/async/png/onboarding/terminal_intention/theme/theme_light_horizontal.png` | embedded terminal/editor preview text | `运行命令`; `测试通过`; `构建完成`; `打开项目` | Medium | Same script as terminal theme variants for consistency. |
| `app/assets/async/png/onboarding/terminal_intention/theme/theme_light_vertical.png` | embedded terminal/editor preview text | `运行命令`; `通过`; `完成`; `项目` | Medium | Same script as terminal theme variants for consistency. |
| `app/assets/async/png/onboarding/terminal_intention/theme/theme_phenomenon_horizontal.png` | embedded terminal/editor preview text | `运行命令`; `测试通过`; `构建完成`; `打开项目` | Medium | Same script as terminal theme variants for consistency. |
| `app/assets/async/png/onboarding/terminal_intention/theme/theme_phenomenon_vertical.png` | embedded terminal/editor preview text | `运行命令`; `通过`; `完成`; `项目` | Medium | Same script as terminal theme variants for consistency. |

## Review Checklist

Before replacing PNGs:

1. Confirm every replacement image uses the script row for its asset path.
2. Confirm `Agent`, `Warp Drive`, `MCP`, `Diff`, product names, and third-party
   names are preserved exactly where listed.
3. Confirm no text overlaps toolbar, sidebar, or terminal preview boundaries.
4. Confirm before/after contact sheets show only the intended PNGs.
5. Confirm `git diff --stat` contains no unrelated binary files.

## Public RC Impact

Public RC remains blocked until these deferred assets are either regenerated
with Chinese-localized preview art or explicitly approved by design/product.
