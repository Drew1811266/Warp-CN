# zh-Hans Full Translation Audit

This document tracks the Phase 12 full translation audit. The goal is to review every manifest entry for semantic accuracy, terminology consistency, context fit, placeholder safety, and functional safety.

## Audit Rules

Each reviewed entry must be classified as one of:

| Status | Meaning |
| --- | --- |
| `accepted` | Translation is accurate and safe in context |
| `fixed` | Translation was changed during the audit |
| `preserved` | English/token content is intentionally preserved |
| `needs-gui` | Source review passed, but GUI rendering still needs visual evidence |
| `needs-follow-up` | Requires a dedicated follow-up slice |
| `blocked` | Cannot be verified safely without account/service state |

Severity follows `docs/zh-Hans-localization-phase10.md`:

- Translation: `T0`, `T1`, `T2`, `T3`
- Functional: `F0`, `F1`, `F2`, `F3`

## Current Manifest Baseline

Baseline after P11 search review:

```text
entries: 2664
files: 198
already_applied: 2649
would_change: 0
missing: 0
```

Coverage baseline:

| Preset | Covered | Candidates | Coverage |
| --- | ---: | ---: | ---: |
| `onboarding` | 266 | 54 | 83.1% |
| `workspace` | 598 | 352 | 62.9% |
| `search` | 269 | 0 | 100.0% |
| `settings` | 1202 | 823 | 59.4% |
| `modals` | 679 | 5025 | 11.9% |
| `release` | 2892 | 6233 | 31.7% |

## Batch Plan

| Batch | Scope | Entry count target | Status | Record |
| --- | --- | ---: | --- | --- |
| P12-S01 | Search / command palette / command search / slash command menu | 269 | `reviewed-low-load` | `docs/zh-Hans-module-review-search-2026-06-01.md` |
| P12-W01 | Workspace core navigation and app menu labels | 194 | `reviewed-low-load` | This file |
| P12-W02 | Workspace views, vertical tabs, tab/session surfaces | 173 | `reviewed-low-load` | This file |
| P12-ONB | Onboarding/auth/login | 246 | `reviewed-low-load` | This file |
| P12-SET-AI | AI settings, model/provider/BYOK/custom inference | 311 | `reviewed-low-load` | This file |
| P12-SET-CORE | Settings core pages and preferences | 566 | `reviewed-low-load` | This file |
| P12-MODAL | Modals, toasts, destructive confirmations | 137 | `reviewed-low-load` | This file |
| P12-AGENT | Agent view, status, tips, conversation details | 266 | `reviewed-low-load` | This file |
| P12-BILL-CLOUD | Billing, usage, teams, cloud environments | 269 | `reviewed-low-load` | This file |
| P12-TERMINAL | Terminal input, slash commands outside search, shell-facing copy | 52 | `reviewed-low-load` | This file |
| P12-REMAINDER | Any remaining manifest paths not covered above | 251 | `reviewed-low-load` | This file |

## Completed Batches

### P12-S01 Search

Status: `reviewed-low-load`.

Summary:

- Search preset reached `269 covered / 0 candidates / 100.0%`.
- No `F0` or `F1` blocker found.
- Fixed direction wording, conversation title punctuation, natural-language search example, and search setting description.
- Remaining follow-up: `P11-SEARCH-A11Y-01`, English accessibility-label prefixes in search.

## Completed Batch: P12-W01 Workspace Core

Status: `reviewed-low-load`.

Target paths:

- `app/src/workspace/mod.rs`
- `app/src/app_menus.rs`

Entry count:

- `app/src/workspace/mod.rs`: 148 entries
- `app/src/app_menus.rs`: 46 entries
- Total: 194 entries

Reviewed groups:

| Group | Entries | Decision |
| --- | ---: | --- |
| Terminal/Agent tab and new-window labels | 7 | `accepted` |
| Notification, logout, changelog, docs, logs, privacy, shared blocks | 9 | `accepted` |
| Tab navigation, pane navigation, close/move tab actions | 31 | `accepted` |
| Zoom, font, project explorer, theme picker, tab config, palettes | 24 | `accepted` |
| Notebook/workflow/folder/environment/prompt creation labels | 28 | `accepted` |
| Left panel, global search, Warp Drive, command palette, conversation list | 20 | `accepted` |
| Keyboard shortcuts and accessibility verbosity labels | 5 | `accepted` |
| Settings and settings-section open actions | 26 | `accepted` |
| App menus: shell debug, in-band generators, PTY recording, block visibility | 13 | `accepted` |
| App menus: File/Edit/View/Tab/Drive/Window/Help menu labels | 30 | `accepted` except one fixed launch-config item |
| App menus: external links and debug/admin actions | 1 | `accepted` |

Fixes:

| Source | Previous target | New target | Severity | Reason |
| --- | --- | --- | --- | --- |
| `Save New...` in `make_launch_config_menu_items` | `另存为新项...` | `保存为新启动配置...` | `T1` | Source context is launch configuration saving; `新项` was too generic and could mislead users |

Functional safety notes:

- Workspace action IDs, custom action names, context predicates, and menu dispatch strings remain untranslated.
- Product/technical terms such as `Warp`, `Warp Drive`, `Agent`, `Oz CLI`, `MCP`, `Slack`, `GitHub`, `CSV`, `PTY`, `SSH`, and `Shell` are preserved or mixed according to glossary style.
- Keyboard shortcut/action semantics were not changed.
- Placeholder-free short labels were reviewed for concise menu fit.

Remaining follow-up:

| ID | Severity | Issue | Follow-up |
| --- | --- | --- | --- |
| P12-W01-GUI-01 | `evidence` | This batch used source and menu-context review only; GUI menus were not rerun in this pass | Reuse existing GUI menu smoke before RC, or rerun cropped/redacted menu evidence |

Decision:

`P12-W01` is accepted as `reviewed-low-load`. No `F0` or `F1` functional blocker was found.

Validation:

```text
manifest validation passed
glossary check passed
dry-run: entries 2664, files 198, would_change 0, missing 0
workspace coverage: 598/352 = 62.9%
release coverage: 2892/6233 = 31.7%
cargo fmt --check: passed
git diff --check: passed
```

## Completed Batch: P12-W02 Workspace Views

Status: `reviewed-low-load`.

Target paths:

- `app/src/workspace/view.rs`
- `app/src/workspace/view/vertical_tabs.rs`
- `app/src/tab.rs`

Entry count:

- `app/src/workspace/view.rs`: 109 entries
- `app/src/workspace/view/vertical_tabs.rs`: 42 entries
- `app/src/tab.rs`: 22 entries
- Total: 173 entries

Reviewed groups:

| Group | Entries | Decision |
| --- | ---: | --- |
| Workspace search, tab config, settings, and side panel entry labels | 12 | `accepted` |
| Update, changelog, docs, feedback, sign-up, billing, invite, login expiry | 29 | `accepted` |
| Agent/cloud handoff status and error messages | 17 | `accepted` |
| Warp Drive plan/workflow/object sync toasts | 9 | `accepted` |
| Toolbar, pane, tab config, worktree, local Docker sandbox, API key labels | 20 | `accepted` |
| Vertical tabs display settings, density, metadata toggles, item types | 42 | `accepted` |
| Tab context menu share/copy/rename/move/close/group/config actions | 22 | `accepted` except PR wording fix |
| Mouse reporting toast | 1 | `fixed` |

Fixes:

| Source / context | Previous target or behavior | New target or behavior | Severity | Reason |
| --- | --- | --- | --- | --- |
| `You {verb} mouse reporting.` | Target was Chinese, but runtime `{verb}` still inserted English `enabled`/`disabled` | Runtime verb changed to `开启` / `关闭`; toast now reads `你已开启鼠标报告。` or `你已关闭鼠标报告。` | `T1/F2` | Prevents mixed-language toast and preserves toggle meaning |
| `Copy pull request link` | `复制拉取请求链接` | `复制 PR 链接` | `T2` | Matches existing `PR 链接` wording in vertical tab metadata settings |

Functional safety notes:

- Handoff, update, auth, and cloud error messages keep placeholders intact.
- `Oz CLI`, `Warp Drive`, `Warp Agent`, `Docker`, `API`, `Slack`, `PR`, `GitHub CLI`, and `Warp Essentials` are preserved according to current term style.
- Tab movement and close actions were checked against horizontal/vertical tab context.
- No command token, path, URL, ID, telemetry event, or dispatch string was translated in this batch.

Remaining follow-up:

| ID | Severity | Issue | Follow-up |
| --- | --- | --- | --- |
| P12-W02-GUI-01 | `evidence` | This batch did not rerun the visible workspace/tab UI | Reuse or rerun cropped/redacted workspace and tab context menu GUI smoke before RC |
| P12-W02-A11Y-01 | `T3/F3` | Some accessibility labels in surrounding workspace/search surfaces may still include English product-like prefixes | Handle together with the broader accessibility-label follow-up |

Decision:

`P12-W02` is accepted as `reviewed-low-load`. No `F0` or `F1` functional blocker was found.

Validation:

```text
manifest validation passed
glossary check passed
dry-run: entries 2664, files 198, would_change 0, missing 0
cargo fmt --check: passed
git diff --check: passed
```

## Completed Batch: P12-ONB Onboarding/Auth

Status: `reviewed-low-load`.

Target paths:

- `crates/onboarding/src/**`
- `app/src/auth/**`
- Login, anonymous, privacy, token fallback, and first-run entry paths.

Entry count:

- `app/src/auth/**`: 115 entries
- `crates/onboarding/src/**`: 131 entries
- Total: 246 entries

Reviewed groups:

| Group | Entries | Decision |
| --- | ---: | --- |
| Auth override warning, anonymous-session deletion, export/import recovery | 9 | `accepted` |
| Auth modal/body login, skip-login, browser URL fallback, token fallback | 28 | `accepted` except browser fallback wording fixed |
| Login failure notifications, SSO link, web handoff, paste-token modal | 18 | `accepted` |
| Privacy settings toggles and offline-use explanation | 16 | `accepted` except telemetry wording and Ambient Agent term fixed |
| Login slide: Warp Drive, AI enable/disable, skip dialog, privacy links | 28 | `accepted` except URL-link spacing fixed |
| Logout confirmation pluralized warnings | 16 | `accepted` |
| Onboarding callout for universal input, terminal mode, agent mode, project init | 20 | `accepted` |
| Onboarding shared feature lists and price badge | 10 | `accepted` |
| Agent customization, model tier, autonomy, upgrade fallback | 26 | `accepted` except premium model wording and URL-link spacing fixed |
| UI customization, intention, intro, project, theme, third-party Agent slides | 75 | `accepted` except project subtitle and support benefit fixed |

Fixes:

| Source / context | Previous target or behavior | New target or behavior | Severity | Reason |
| --- | --- | --- | --- | --- |
| `Private email support` | `私密邮件支持` | `专属邮件支持` | `T1` | Product-plan benefit means dedicated/private support channel, not confidential email content |
| `Set up a project to optimize it for coding in Warp.` | `设置项目以优化在 Warp 中编码。` | `设置项目，让它更适合在 Warp 中编码。` | `T2` | More natural Chinese and better preserves project setup intent |
| `High-level feature usage data...` | `高层级功能使用数据...` | `概括性的功能使用数据...` | `T2` | Avoids literal wording and better describes aggregate usage data |
| `ambient agents` in cloud-conversation note | `ambient agent` | `Ambient Agent` | `T2` | Treats the product-like Agent category consistently and avoids lowercase English leaking into Chinese text |
| Browser fallback fragments around `copy the URL` | Chinese fragments attached directly to `URL` or repeated `手动打开` awkwardly | Added spacing after `URL` and changed the login-slide split to `复制 URL 并手动打开` / `该页面。` | `T2/F3` | Prevents cramped rendered text in split-link UI without changing behavior |
| `State-of-the-art models require paid plans.` | `先进模型需要付费计划。` | `前沿模型需要付费计划。` | `T2` | Matches existing `frontier models` wording in the same onboarding flow |

Cross-scope consistency fix:

- `app/src/settings_view/privacy_page.rs` uses the same cloud-conversation off-state copy as auth privacy settings, so the duplicate target was aligned to `Ambient Agent` and `无法共享`.

Functional safety notes:

- Auth tokens, redirect URL handling, SSO labels, and button dispatch/action wiring were not changed.
- Placeholder and variable-bearing strings keep `{}`, `${}`, `{num_*}`, and `{plural}` intact.
- Product and technical terms such as `Warp`, `Warp Drive`, `Agent`, `Ambient Agent`, `Oz`, `Claude Code`, `Codex`, `Gemini CLI`, `SSO`, `URL`, `AI`, and `SSH` are preserved according to the current glossary style.
- English command/query examples inside onboarding callouts remain intentionally literal where they represent user input or repository questions.

Remaining follow-up:

| ID | Severity | Issue | Follow-up |
| --- | --- | --- | --- |
| P12-ONB-GUI-01 | `evidence` | This batch used source/context review only; first-run and auth GUI evidence was not rerun in this pass | Reuse or rerun cropped/redacted first-run/auth screenshots before RC |
| P12-ONB-TERM-01 | `T3` | `Ambient Agent` is currently preserved as product-like English; no repository-wide Chinese term has been accepted yet | Decide glossary policy during the broader Agent/cloud batch |

Decision:

`P12-ONB` is accepted as `reviewed-low-load`. No `F0` or `F1` functional blocker was found in source-level review.

Validation:

```text
manifest validation passed
glossary check passed
dry-run: entries 2664, files 198, would_change 0, missing 0
onboarding coverage: 266/54 = 83.1%
release coverage: 2892/6233 = 31.7%
cargo fmt --check: passed
git diff --check: passed
```

## Completed Batch: P12-SET-AI AI Settings / Models / MCP

Status: `reviewed-low-load`.

Target paths:

- `app/src/settings_view/ai_page.rs`
- `app/src/settings_view/agent_assisted_environment_modal.rs`
- `app/src/settings_view/custom_inference_modal.rs`
- `app/src/settings_view/remove_custom_endpoint_confirmation_dialog.rs`
- `app/src/settings_view/mcp_servers_page.rs`
- `app/src/settings_view/mcp_servers/**`
- `app/src/settings_view/billing_and_usage/usage_history_model.rs`
- Cross-scope AI usage row in `app/src/settings_view/billing_and_usage_page.rs`
- Dynamic AI usage period formatter in `app/src/ai/request_usage_model.rs`

Entry count:

- AI settings page: 195 entries
- Agent-assisted environment modal: 16 entries
- Custom inference and custom endpoint removal: 19 entries
- MCP server settings surfaces: 79 entries
- AI usage fetch failure: 1 entry
- Cross-scope billing AI usage description: 1 entry
- Total: 311 manifest entries, plus one dynamic formatter used by AI usage UI

Reviewed groups:

| Group | Entries | Decision |
| --- | ---: | --- |
| AI feature toggles, command-palette labels, prompt/code suggestions | 37 | `accepted` except prompt/code wording fixes |
| Agent profiles, permissions, model picker, context window, allow/deny lists | 67 | `accepted` except natural-language denylist wording fix |
| MCP permissions and MCP server management in AI settings | 31 | `accepted` |
| Rules, Warp Drive context, voice input, agent tips, thinking display | 20 | `accepted` except rules/thinking wording fixes |
| Third-party CLI Agent toolbar and Rich Input controls | 19 | `accepted` |
| Cloud Agent, Cloud Handoff, BYOK, API keys, AWS Bedrock | 44 | `accepted` except Cloud Handoff and plan wording fixes |
| Custom inference endpoint modal and removal confirmation | 19 | `accepted` |
| MCP server list, install, edit, delete, update, status cards | 79 | `accepted` except `My MCPs` wording fix |
| AI usage/reset and conversation usage failure | 2 | `accepted` after dynamic period fix |

Fixes:

| Source / context | Previous target or behavior | New target or behavior | Severity | Reason |
| --- | --- | --- | --- | --- |
| `refresh_duration_to_string()` dynamic period | Returned English `weekly` / `monthly` / `biweekly`, producing mixed Chinese UI | Returns `每周` / `每月` / `每两周` | `T1/F2` | Prevents runtime mixed-language AI usage limit descriptions |
| `Resets {formatted_next_refresh_time}` | `{formatted_next_refresh_time} 重置` | `将于 {formatted_next_refresh_time} 重置` | `T2` | More natural reset-date label |
| AI usage limit descriptions | `这是你账号的 {refresh_duration} AI 额度限制。` and related phrasing | `这是你账号 AI 额度的{refresh_duration}限制。` | `T2` | Fits Chinese grammar after dynamic period localization |
| `prompt suggestions` / `Prompt Suggestions` | `提示建议` | `提示词建议` | `T2` | Aligns with established prompt terminology |
| `Suggested Code Banners` | `建议代码横幅` | `代码建议横幅` | `T2` | Better Chinese modifier order |
| `Natural language denylist` | `自然语言拒绝列表` | `自然语言检测拒绝列表` | `T2` | Clarifies the denylist affects detection triggers, not natural language itself |
| `Let AI suggest rules to save...` | `建议要保存的规则` | `建议可保存的规则` | `T2` | Removes awkward literal phrasing |
| `Agent thinking display` | `Agent 思考显示` | `Agent 思考过程显示` | `T2` | Matches reasoning trace context |
| `Computer use in Cloud Agents` | `Cloud Agent 中的计算机使用` | `云端 Agent 中的计算机使用` | `T2` | Aligns with nearby cloud-agent Chinese wording |
| `Cloud handoff` strings | Mixed lowercase `Cloud handoff` / `cloud handoff` | `Cloud Handoff` | `T2` | Treats Handoff as a product-like feature label consistently |
| `Upgrade to the Build plan` / Enterprise plan text | `Build 方案`, `Enterprise 方案` | `Build 套餐`, `Enterprise 套餐` | `T2` | Aligns plan names with billing-plan terminology |
| `Contact sales` | `联系销售` | `联系销售团队` | `T3` | More natural CTA wording |
| `My MCPs` | `我的 MCP` | `我的 MCP 服务器` | `T2` | Avoids ambiguous abbreviation-only section title |

Functional safety notes:

- API key labels, endpoint validation rules, HTTPS/local/private-host restrictions, MCP server install/delete/update actions, and BYOK terms remain behaviorally unchanged.
- Placeholders `{}`, `{name}`, `{publisher_string}`, `{new_version}`, `{formatted_next_refresh_time}`, and `{refresh_duration}` are preserved.
- Command/search tokens, regex language, provider names, model names, URLs, email addresses, and protocol/API names remain untranslated.
- The only non-manifest code behavior change is localized display text returned by `refresh_duration_to_string()`, whose observed callers are Chinese UI strings in AI usage/billing surfaces.

Remaining follow-up:

| ID | Severity | Issue | Follow-up |
| --- | --- | --- | --- |
| P12-SET-AI-GUI-01 | `evidence` | AI settings, MCP settings, BYOK and custom inference dialogs were not visually rerun in this low-load pass | Capture cropped/redacted AI settings and MCP/custom endpoint evidence before RC |
| P12-SET-AI-TERM-01 | `T3` | `Cloud Handoff`, `Rich Input`, `Full Terminal Use`, and `BYOK` remain preserved English product/feature terms | Confirm glossary policy in a terminology-only pass |

Decision:

`P12-SET-AI` is accepted as `reviewed-low-load`. No `F0` or `F1` blocker was found in source-level review.

Validation:

```text
manifest validation passed
glossary check passed
dry-run: entries 2664, files 198, would_change 0, missing 0
settings coverage: 1202/823 = 59.4%
release coverage: 2892/6233 = 31.7%
cargo fmt: applied rustfmt formatting
cargo fmt --check: passed
git diff --check: passed
```

## Completed Batch: P12-SET-CORE Core Settings

Status: `reviewed-low-load`.

Target paths:

- `app/src/settings_view/appearance_page.rs`
- `app/src/settings_view/code_page.rs`
- `app/src/settings_view/environments_page.rs`
- `app/src/settings_view/execution_profile_view.rs`
- `app/src/settings_view/features_page.rs`
- `app/src/settings_view/keybindings.rs`
- `app/src/settings_view/main_page.rs`
- `app/src/settings_view/mod.rs`
- `app/src/settings_view/platform*.rs`
- `app/src/settings_view/privacy_page.rs`
- `app/src/settings_view/settings_file_footer.rs`
- `app/src/settings_view/settings_page.rs`
- `app/src/settings_view/update_environment_form.rs`
- `app/src/settings_view/warpify_page.rs`
- Small confirmation dialogs under core settings

Entry count:

- Appearance, code, features, privacy, platform, environment, keybinding, Warpify, and settings shell pages: 566 manifest entries.

Reviewed groups:

| Group | Entries | Decision |
| --- | ---: | --- |
| Appearance: themes, icon, window/input/pane/block/text/cursor/tab settings | 112 | `accepted` except prompt terminology fix |
| Code: codebase indexing, LSP status, code review, project explorer/search | 56 | `accepted` |
| Environments and environment editor | 78 | `accepted` except Ambient Agent wording fix |
| Execution profile summaries | 30 | `accepted` |
| Features: general/session/keys/text editing/terminal/notifications/system | 111 | `accepted` except quit/logout warning wording fix |
| Keybindings and settings shell/search | 38 | `accepted` |
| Account/main page and platform API keys | 77 | `accepted` |
| Privacy controls and data management | 40 | `accepted` except cloud conversation copy alignment |
| Settings file footer and shared setting metadata | 7 | `accepted` |
| Warpify / SSH Warpification | 18 | `accepted` except SSH casing and denylist wording fixes |

Fixes:

| Source / context | Previous target | New target | Severity | Reason |
| --- | --- | --- | --- | --- |
| `Use latest user prompt as conversation title in tab names` | `用用户最新提示作为标签页中的对话标题` | `用用户最新提示词作为标签页中的对话标题` | `T2` | Aligns `prompt` with established `提示词` terminology |
| `Environments define where your ambient agents run...` | `ambient agent` | `Ambient Agent` | `T2` | Matches product-like Agent category casing used elsewhere |
| `Show warning before quitting/logging out` | `退出或注销前显示警告` | `退出应用或退出登录前显示警告` | `T1` | Avoids OS-level `注销` ambiguity |
| Privacy `Store AI conversations in the cloud` | `在云端存储 AI 对话` | `将 AI 对话存储在云端` | `T2` | Aligns with auth privacy settings wording |
| Privacy cloud-conversation enabled copy | `可以分享给他人...这些数据...` | `可与他人共享...该数据...` | `T2` | Aligns duplicate wording across auth and privacy settings |
| tmux SSH wrapper description | `tmux ssh 包装器` | `tmux SSH 包装器` | `T3` | Restores standard SSH casing |
| `Denylisted commands` / `Denylisted hosts` | `拒绝列表命令` / `拒绝列表主机` | `命令拒绝列表` / `主机拒绝列表` | `T2` | Matches existing allowlist/denylist noun order |

Functional safety notes:

- Settings actions, flags, keybinding IDs, URLs, regex examples, file paths, and command tokens remain unchanged.
- Placeholders `{}`, `{max_rows}`, `{char_count}`, `{DESCRIPTION_MAX_CHARS}`, and path/repo examples are preserved.
- The privacy page duplicate cloud-conversation text now matches the auth privacy settings text reviewed in `P12-ONB`.
- Environment tests were not rewritten; `View my runs` remains `查看我的运行` because changing it would require a dedicated test update pass.

Remaining follow-up:

| ID | Severity | Issue | Follow-up |
| --- | --- | --- | --- |
| P12-SET-CORE-GUI-01 | `evidence` | Core settings pages were not visually rerun in this low-load pass | Capture cropped/redacted Settings screenshots before RC |
| P12-SET-CORE-ENV-01 | `T3` | `查看我的运行` is understandable but not ideal; tests assert this exact text today | Change to `查看我的运行记录` with corresponding test updates in a targeted environments slice |

Decision:

`P12-SET-CORE` is accepted as `reviewed-low-load`. No `F0` or `F1` blocker was found in source-level review.

Validation:

```text
manifest validation passed
glossary check passed
dry-run: entries 2664, files 198, would_change 0, missing 0
settings coverage: 1202/823 = 59.4%
release coverage: 2892/6233 = 31.7%
cargo fmt --check: passed
git diff --check: passed
```

## Completed Batch: P12-MODAL Modals / Toasts / Confirmations

Status: `reviewed-low-load`.

Target paths:

- `app/src/drive/**/*dialog*.rs`
- `app/src/drive/import/modal*.rs`
- `app/src/drive/workflows/*modal*.rs`
- `app/src/tab_configs/*modal*.rs`
- `app/src/tab_configs/*confirmation*.rs`
- `app/src/terminal/*banner*.rs`
- `app/src/terminal/*modal*.rs`
- `app/src/terminal/shared_session/**/*modal*.rs`
- `app/src/terminal/view/ambient_agent/*confirmation*.rs`
- `app/src/terminal/view/inline_banner/*.rs`
- `app/src/themes/*modal*.rs`
- `app/src/ai/agent_management/notifications/toast_stack.rs`

Entry count:

- 137 manifest entries.

Reviewed groups:

| Group | Entries | Decision |
| --- | ---: | --- |
| Team/member delete/leave confirmations and trash/delete dialogs | 20 | `accepted` except Reload credit wording fixes |
| Drive import, workflow modal, naming/sharing dialogs | 27 | `accepted` |
| Tab config, worktree, params, and remove confirmation dialogs | 19 | `accepted` |
| Billing/credits banners and auto-reload modal | 14 | `accepted` |
| Share block modal and shared-session role/share modals | 42 | `accepted` except secrets and scrollback wording fixes |
| Ambient Agent secret delete, notification banners, theme modals, toast | 15 | `accepted` |

Fixes:

| Source / context | Previous target | New target | Severity | Reason |
| --- | --- | --- | --- | --- |
| `reload credits` in leave/remove team confirmations | `充值额度` | `Reload 额度` | `T1` | `Reload credits` is a product/billing credit concept, not generic top-up wording |
| `Redact secrets (API keys, passwords, IP addresses, PII etc.)` | `遮盖密钥...` | `遮盖敏感信息...` | `T1/F2` | The redaction scope includes passwords, IP addresses, and PII, not only keys |
| `Share without scrollback` | `不包含回滚内容共享` | `共享时不包含回滚内容` | `T2` | More natural action label |
| Disabled share-options explanation | `由于共享大小限制且...` | `由于共享大小限制以及...` | `T3` | Improves readability without changing meaning |

Functional safety notes:

- Destructive actions (`delete`, `remove`, `empty trash`, `discard changes`) were checked for clear irreversible wording.
- Placeholders `{}`, team/member names, URLs, and copied-link/embed-code behavior were not changed.
- Permission escalation copy for shared sessions remains split across spans but reads as a complete warning.
- Sensitive-data redaction wording now matches the actual listed categories.

Remaining follow-up:

| ID | Severity | Issue | Follow-up |
| --- | --- | --- | --- |
| P12-MODAL-GUI-01 | `evidence` | Modal and toast layout was not visually rerun in this low-load pass | Capture cropped/redacted destructive confirmation and sharing modals before RC |

Decision:

`P12-MODAL` is accepted as `reviewed-low-load`. No `F0` or `F1` blocker was found in source-level review.

Validation:

```text
manifest validation passed
glossary check passed
dry-run: entries 2664, files 198, would_change 0, missing 0
modals coverage: 679/5025 = 11.9%
release coverage: 2892/6233 = 31.7%
cargo fmt --check: passed
git diff --check: passed
```

## Completed Batch: P12-AGENT Agent Views / Status / Tips

Status: `reviewed-low-load`.

Target paths:

- `app/src/ai/agent/**/*.rs`
- `app/src/ai/agent_conversations_model.rs`
- `app/src/ai/agent_management/**/*.rs` excluding modal/toast paths already reviewed in P12-MODAL
- `app/src/ai/agent_tips.rs`
- `app/src/ai/ai_document_view.rs`
- `app/src/ai/ambient_agents/task.rs`
- `app/src/ai/artifacts/mod.rs`
- `app/src/ai/aws_credentials.rs`
- `app/src/ai/blocklist/agent_view/agent_input_footer/**/*.rs`
- `app/src/ai/blocklist/block/pending_user_query_block.rs`
- `app/src/ai/blocklist/history_model.rs`
- `app/src/ai/conversation_details_panel.rs`
- `app/src/terminal/cli_agent_sessions/plugin_manager/*.rs`

Entry count:

- 266 manifest entries.

Reviewed groups:

| Group | Entries | Decision |
| --- | ---: | --- |
| Agent status/error strings and conversation lifecycle states | 37 | `accepted` except `Blocked` consistency fix |
| Agent management: type selector, cloud setup guide, runs table, notifications | 73 | `accepted` except docs-link spacing and run wording fixes |
| Agent tips and command/action helper text | 40 | `accepted` except prompt/Handoff/palette wording fixes |
| AI plan document view and plan sync/update controls | 17 | `accepted` except tooltip composition fix |
| Ambient Agent task states, artifacts, AWS credentials | 21 | `accepted` |
| Agent input footer, environment selector, plugin notifications, context usage | 49 | `accepted` |
| Conversation details panel and CLI Agent plugin setup instructions | 29 | `accepted` |

Fixes:

| Source / context | Previous target or behavior | New target or behavior | Severity | Reason |
| --- | --- | --- | --- | --- |
| `Blocked` in `agent/conversation.rs` | `已阻止` | `已阻塞` | `T2` | Aligns with other Agent task state strings |
| Oz docs link fragments | `查看` + `Oz 文档` + `以了解更多。` | `查看 ` + `Oz 文档` + ` 以了解更多。` | `T3` | Avoids cramped mixed Chinese/English link text |
| `Runs` / `Loading cloud agent runs` | `运行`, `正在加载云端 Agent 运行` | `运行记录`, `正在加载云端 Agent 运行记录` | `T2` | Clarifies this is the runs list/history |
| `@` prompt tip | `添加到提示中` | `添加到提示词中` | `T2` | Aligns `prompt` terminology |
| AI plan update tooltip | `{save_action} 以停止...`; fallback only `点击` | `{save_action} 可停止...`; fallback `点击“更新 Agent”` | `T1/F2` | Prevents malformed tooltip when no keybinding is available |
| Handoff tip | `handoff chip` | `Handoff 组件` | `T2` | Makes UI component understandable in Chinese |
| `Open palette` action label | `打开面板` | `打开命令面板` | `T2` | Disambiguates command palette from generic panels |

Functional safety notes:

- Agent lifecycle states, provider/API errors, AWS credential placeholders, URLs, and CLI paths are preserved.
- Slash commands such as `/open-mcp-servers`, `/plan`, `/init`, `/compact`, `/usage`, `/reload-plugins`, `AGENTS.md`, `CLAUDE.md`, and config paths remain literal.
- The AI plan tooltip still preserves `{save_action}` and now makes both keybinding and click fallback grammatically safe.
- Handoff keeps the `&` trigger literal.

Remaining follow-up:

| ID | Severity | Issue | Follow-up |
| --- | --- | --- | --- |
| P12-AGENT-GUI-01 | `evidence` | Agent runs list, input footer, cloud setup guide, and plan tooltip were not visually rerun in this low-load pass | Capture cropped/redacted Agent views before RC |

Decision:

`P12-AGENT` is accepted as `reviewed-low-load`. No `F0` or `F1` blocker was found in source-level review.

Validation:

```text
manifest validation passed
glossary check passed
dry-run: entries 2664, files 198, would_change 0, missing 0
release coverage: 2892/6233 = 31.7%
cargo fmt --check: passed
git diff --check: passed
```

## Completed Batch: P12-TERMINAL / P12-REMAINDER Final Sweep

Status: `reviewed-low-load`.

Target paths:

- Terminal input, rewind, slash command, shared-session, notification, and init-environment surfaces
- Drive export/index actions
- Menu accessibility strings
- Tab config sidecar/rendering leftovers
- Theme chooser/creator/deletion bodies
- Workspace action, CLI install, close/delete/rewind confirmations, toolbar items, HOA onboarding, web home, native modal, conversation list, launch modals, right panel, WASM view
- `crates/warp_search_core/src/data_source.rs`

Entry count:

- `P12-TERMINAL`: 52 entries
- `P12-REMAINDER`: 251 entries
- Total: 303 manifest entries.

Reviewed groups:

| Group | Entries | Decision |
| --- | ---: | --- |
| Terminal input, slash commands, rewind, shared-session network/roles | 52 | `accepted` except prompt wording fix |
| Drive export/index and object actions | 17 | `accepted` except prompt wording fix |
| Menu accessibility and generic menu narration | 16 | `accepted` |
| Tab config sidecar/rendering/session config leftovers | 17 | `accepted` |
| Theme chooser/creator/deletion | 22 | `accepted` |
| Workspace action, CLI install, close/delete/rewind confirmations | 36 | `accepted` |
| Header toolbar, HOA onboarding, home/native modal, conversation list | 40 | `accepted` |
| Launch modals, right panel, WASM cloud runs | 52 | `accepted` except harness/runs/right-panel wording fixes |
| Search core data sources | 51 | `accepted` except Full Terminal Use/current-directory wording fixes |

Fixes:

| Source / context | Previous target | New target | Severity | Reason |
| --- | --- | --- | --- | --- |
| `Copy prompt` | `复制提示` | `复制提示词` | `T2` | Aligns prompt terminology |
| `/queue requires a prompt argument` | `提示参数` | `提示词参数` | `T2` | Aligns prompt terminology in slash-command errors |
| `Run any agent harness in the cloud` | `Agent harness` | `Agent 执行框架` | `T2` | Avoids unexplained English developer term in launch copy |
| `Navigate to a repo and initialize it for coding` | `前往仓库并初始化用于编码` | `前往仓库并初始化，以便编码使用` | `T2` | Fixes awkward Chinese tooltip |
| `View all cloud runs` | `查看所有云端运行` | `查看所有云端运行记录` | `T2` | Aligns cloud run terminology |
| `full terminal use models` | `完整终端使用模型` | `Full Terminal Use 模型` | `T2` | Preserves product-like feature name used elsewhere |
| `current directory conversations` | `当前目录对话` | `当前目录中的对话` | `T3` | Improves data-source label readability |

Functional safety notes:

- Slash-command names, shell commands, AppleScript command wrappers, paths, Markdown bullets, URLs, and placeholders remain literal.
- Destructive confirmations and shared-session permission warnings were checked for clear irreversible/permission language.
- Search data-source names preserve technical/product labels where needed.

Remaining follow-up:

| ID | Severity | Issue | Follow-up |
| --- | --- | --- | --- |
| P12-FINAL-GUI-01 | `evidence` | Final sweep did not rerun GUI evidence for launch modals, shared-session flows, theme creation, or command errors | Add cropped/redacted visual smoke when preparing RC |

Decision:

`P12-TERMINAL` and `P12-REMAINDER` are accepted as `reviewed-low-load`. No `F0` or `F1` blocker was found in source-level review.

Validation:

```text
manifest validation passed
glossary check passed
dry-run: entries 2664, files 198, would_change 0, missing 0
metadata summary: entries 2664; key/context/status/expected_count 150 each; preserve_terms 18
onboarding coverage: 266/54 = 83.1%
workspace coverage: 598/352 = 62.9%
search coverage: 269/0 = 100.0%
settings coverage: 1202/823 = 59.4%
modals coverage: 679/5025 = 11.9%
release coverage: 2892/6233 = 31.7%
python unittest localization suite: 18 passed
cargo fmt --check: passed
git diff --check: passed
```

## Final P12 Decision

Status: `complete-source-audit-low-load`.

All 2,664 manifest entries were assigned to a P12 review batch and reviewed at source/context level. The pass found no `F0` or `F1` functional blocker. Remaining risks are evidence-related: GUI rendering, cropped screenshots, and a few terminology policy choices still need RC evidence passes, but they do not block the source-level translation audit.

## Completed Batch: P12-BILL-CLOUD Billing / Teams / Cloud

Status: `reviewed-low-load`.

Target paths:

- `app/src/settings_view/billing_and_usage/**/*.rs`
- `app/src/settings_view/billing_and_usage_page.rs`
- `app/src/settings_view/billing_and_usage_page_v2.rs`
- `app/src/settings_view/teams_page.rs`
- `app/src/terminal/buy_credits_banner.rs`
- `app/src/terminal/input/slash_commands/cloud_mode_v2_view.rs`
- `app/src/workspace/view/build_plan_migration_modal.rs`
- `app/src/workspace/view/cloud_agent_capacity_modal/mod.rs`
- `app/src/workspace/view/free_tier_limit_hit_modal.rs`

Entry count:

- 269 manifest entries.

Reviewed groups:

| Group | Entries | Decision |
| --- | ---: | --- |
| Billing usage tables, credit categories, team totals | 39 | `accepted` |
| Overage limit modal and usage history loading | 7 | `accepted` |
| Billing and usage page v1 | 97 | `accepted` except credit/usage/key wording fixes |
| Billing and usage page v2 | 53 | `accepted` except credit/usage wording fixes |
| Teams creation/invite copy | 15 | `accepted` except cloud run wording fix |
| Cloud Mode slash-command categories | 6 | `accepted` except prompts terminology fix |
| Build plan migration, cloud capacity, free-tier limit modals | 49 | `accepted` except plan/credit/model wording fixes |
| Buy credits banner | 3 | `accepted` except credit unit wording fix |

Fixes:

| Source / context | Previous target | New target | Severity | Reason |
| --- | --- | --- | --- | --- |
| `credit(s)` count labels | `个额度` | `点额度` | `T1` | Aligns billing unit wording with existing product copy such as `1,500 点额度` |
| `Usage History` / empty history copy | `使用历史` | `使用记录` | `T2` | More natural for billing/activity history |
| `bring your own key` | `自带密钥` | `自带 API 密钥` | `T2` | Clarifies BYOK refers to model-provider API keys |
| `Prompts` in Cloud Mode slash command view | `提示` | `提示词` | `T2` | Aligns prompt terminology |
| `cloud agent runs` in team description | `云端 Agent 运行` | `云端 Agent 运行记录` | `T2` | Matches Agent runs list terminology |
| `plan` in billing/upgrade modals | Mixed `方案` / `套餐` | `套餐` | `T2` | Keeps billing plan terminology consistent |
| `AI credits` in capacity modal | `AI 点数` | `AI 额度` | `T2` | Aligns with billing/usage copy |
| `Access to frontier OpenAI...` | `访问前沿...模型` | `可使用 OpenAI、Anthropic 和 Google 的前沿模型` | `T2` | Matches onboarding plan-benefit wording |
| `Access to Reload credits and volume-based discounts` | `基于用量的折扣` | `阶梯折扣` | `T2` | Aligns with existing plan-benefit wording |
| `Extended cloud agents access` | `扩展云端 Agent 访问权限` | `更多云端 Agent 使用额度` | `T2` | Better reflects usage allowance, not just access permission |

Functional safety notes:

- Money amounts, currency symbols, billing placeholders, credit counts, and Stripe/admin URLs are preserved.
- Auto-reload, overage, spend-limit, and plan-upgrade action semantics were not changed.
- Billing copy now avoids mixing `点数`, `个额度`, and `方案` in the same purchase/upgrade flows.

Remaining follow-up:

| ID | Severity | Issue | Follow-up |
| --- | --- | --- | --- |
| P12-BILL-GUI-01 | `evidence` | Billing/usage and upgrade modals were not visually rerun in this low-load pass | Capture cropped/redacted billing and upgrade screens before RC |

Decision:

`P12-BILL-CLOUD` is accepted as `reviewed-low-load`. No `F0` or `F1` blocker was found in source-level review.

Validation:

```text
manifest validation passed
glossary check passed
dry-run: entries 2664, files 198, would_change 0, missing 0
release coverage: 2892/6233 = 31.7%
cargo fmt --check: passed
git diff --check: passed
```
