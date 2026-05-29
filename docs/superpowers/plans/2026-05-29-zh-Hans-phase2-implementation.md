# Warp CN Phase 2 Localization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the second phase of Warp CN localization by improving audit precision, translating deeper user-visible paths, and recording release-quality verification evidence.

**Architecture:** Keep the existing manifest-driven local fork. Translation strings continue to live in `resources/localization/zh-Hans-overrides.toml`; `script/zh_apply_localization.py` applies them; `script/zh_localization_inventory.py` measures likely user-visible gaps. Phase 2 adds a better audit filter first, then expands translations in focused user-path batches.

**Tech Stack:** Rust UI source, Python 3 scripts, TOML translation manifest, Cargo checks/tests, macOS `WarpOss.app` bundle smoke testing.

---

## Task 1: Commit Phase 2 Planning Documents

**Files:**

- Create: `docs/zh-Hans-localization-phase2.md`
- Create: `docs/superpowers/plans/2026-05-29-zh-Hans-phase2-implementation.md`

- [ ] **Step 1: Verify planning docs exist**

Run:

```bash
test -s docs/zh-Hans-localization-phase2.md
test -s docs/superpowers/plans/2026-05-29-zh-Hans-phase2-implementation.md
```

Expected: both commands exit 0.

- [ ] **Step 2: Check Markdown diff hygiene**

Run:

```bash
git diff --check
```

Expected: exit 0, no whitespace warnings.

- [ ] **Step 3: Commit planning docs**

Run:

```bash
git add docs/zh-Hans-localization-phase2.md docs/superpowers/plans/2026-05-29-zh-Hans-phase2-implementation.md
git commit -m "docs: plan phase 2 zh-Hans localization"
```

Expected: commit succeeds and includes only the two Phase 2 planning files.

## Task 2: Reduce Inventory False Positives

**Files:**

- Modify: `script/zh_localization_inventory.py`
- Modify: `docs/zh-Hans-localization.md`
- Modify: `docs/zh-Hans-localization-phase2.md`

- [ ] **Step 1: Add skip rules for non-UI strings**

Modify `script/zh_localization_inventory.py` to add these constants after `LOWER_IDENTIFIER_RE`:

```python
FILTER_TOKEN_RE = re.compile(r"^[a-z_]+:$")
KEYBINDING_RE = re.compile(
    r"^(?:cmd|ctrl|alt|shift|super|orctrl|cmdorctrl|numpad|enter|return|escape|tab|up|down|left|right|y|o|v)(?:-(?:cmd|ctrl|alt|shift|super|orctrl|cmdorctrl|numpad|enter|return|escape|tab|up|down|left|right|y|o|v))*$",
    re.IGNORECASE,
)
PLACEHOLDER_ONLY_RE = re.compile(r"^(?:\{[A-Za-z0-9_:.?]+\}|%[A-Za-z](?: %[A-Za-z])*)$")
INTERNAL_ID_WITH_PLACEHOLDER_RE = re.compile(r"^[a-z][a-z0-9_:-]*:\{[A-Za-z0-9_]+\}$")
```

Add `"search_tags"` and `"search_keywords"` to `SKIP_LINE_PATTERNS`.

Update `is_excluded_path` so telemetry files are skipped:

```python
return (
    path.name.endswith("_tests.rs")
    or path.name == "telemetry.rs"
    or any(part in normalized for part in EXCLUDED_PATH_PARTS)
)
```

Update `is_candidate_literal` after the `LOWER_IDENTIFIER_RE` check:

```python
if FILTER_TOKEN_RE.match(stripped):
    return False
if KEYBINDING_RE.match(stripped):
    return False
if PLACEHOLDER_ONLY_RE.match(stripped):
    return False
if INTERNAL_ID_WITH_PLACEHOLDER_RE.match(stripped):
    return False
```

- [ ] **Step 2: Run inventory smoke checks**

Run:

```bash
python3 -m py_compile script/zh_localization_inventory.py
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
```

Expected: all commands exit 0. Coverage numbers may change because false-positive candidates are removed.

- [ ] **Step 3: Document the new audit semantics**

In `docs/zh-Hans-localization.md`, add a note under the inventory workflow explaining:

```markdown
The inventory script intentionally filters telemetry files, keybindings, filter tokens, placeholder-only strings, and settings search tags. These strings are not treated as untranslated UI unless they are also rendered directly in a visible control.
```

In `docs/zh-Hans-localization-phase2.md`, update the P2-M1 status after running coverage commands with the new counts.

- [ ] **Step 4: Validate and commit**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
cargo fmt --check
git diff --check
```

Expected: all commands exit 0.

Commit:

```bash
git add script/zh_localization_inventory.py docs/zh-Hans-localization.md docs/zh-Hans-localization-phase2.md
git commit -m "chore: reduce zh-Hans inventory noise"
```

## Task 3: Localize Workspace HOA Onboarding

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify after apply: `app/src/workspace/hoa_onboarding/hoa_onboarding_flow.rs`
- Modify after apply: `app/src/workspace/hoa_onboarding/tab_config_step.rs`
- Modify after apply: `app/src/workspace/hoa_onboarding/welcome_banner.rs`

- [ ] **Step 1: Add HOA onboarding manifest entries**

Append these entries near existing workspace/search entries in `resources/localization/zh-Hans-overrides.toml`:

```toml
[[replace]]
path = "app/src/workspace/hoa_onboarding/hoa_onboarding_flow.rs"
source = "See what's new"
target = "查看新增内容"

[[replace]]
path = "app/src/workspace/hoa_onboarding/hoa_onboarding_flow.rs"
source = "Next"
target = "下一步"

[[replace]]
path = "app/src/workspace/hoa_onboarding/hoa_onboarding_flow.rs"
source = "Dismiss"
target = "关闭"

[[replace]]
path = "app/src/workspace/hoa_onboarding/hoa_onboarding_flow.rs"
source = "Finish"
target = "完成"

[[replace]]
path = "app/src/workspace/hoa_onboarding/hoa_onboarding_flow.rs"
source = "Switch back to horizontal tabs"
target = "切回水平标签页"

[[replace]]
path = "app/src/workspace/hoa_onboarding/hoa_onboarding_flow.rs"
source = "Introducing vertical tabs - the new default"
target = "介绍垂直标签页：新的默认布局"

[[replace]]
path = "app/src/workspace/hoa_onboarding/hoa_onboarding_flow.rs"
source = "Vertical tabs show all open agent and terminal panes, grouped by tab. Customize what information you want to see to support your workflow."
target = "垂直标签页会按标签页分组显示所有打开的 Agent 和终端窗格。你可以自定义显示信息，以匹配自己的工作流。"

[[replace]]
path = "app/src/workspace/hoa_onboarding/hoa_onboarding_flow.rs"
source = "Meet your new agent inbox"
target = "认识新的 Agent 收件箱"

[[replace]]
path = "app/src/workspace/hoa_onboarding/hoa_onboarding_flow.rs"
source = "Learn more"
target = "了解更多"

[[replace]]
path = "app/src/workspace/hoa_onboarding/hoa_onboarding_flow.rs"
source = "Warp pipes through notifications from any CLI coding agent into a unified notification center that works across all coding agents and harnesses. "
target = "Warp 会把任何 CLI 编码 Agent 的通知汇总到统一通知中心，可跨所有编码 Agent 和执行环境使用。"

[[replace]]
path = "app/src/workspace/hoa_onboarding/tab_config_step.rs"
source = "Create your first tab config"
target = "创建你的第一个标签页配置"

[[replace]]
path = "app/src/workspace/hoa_onboarding/tab_config_step.rs"
source = "Set up a reusable starting point for your tabs. Pick a repo, choose a session type, and optionally attach a worktree. Use it whenever you want to open a tab with this setup."
target = "为标签页设置可复用的起点。选择仓库、会话类型，并可选附加 worktree。之后想用这套设置打开标签页时即可直接使用。"

[[replace]]
path = "app/src/workspace/hoa_onboarding/welcome_banner.rs"
source = "Vertical tabs"
target = "垂直标签页"

[[replace]]
path = "app/src/workspace/hoa_onboarding/welcome_banner.rs"
source = "Rich tab titles and metadata like git branch, worktree, and PR. Fully customizable."
target = "显示丰富的标签页标题和元数据，例如 Git 分支、worktree 和 PR，并支持完全自定义。"

[[replace]]
path = "app/src/workspace/hoa_onboarding/welcome_banner.rs"
source = "Tab configs"
target = "标签页配置"

[[replace]]
path = "app/src/workspace/hoa_onboarding/welcome_banner.rs"
source = "Tab-level schema to set your directory, startup commands, theme, and worktree with one click"
target = "用标签页级配置一键设置目录、启动命令、主题和 worktree"

[[replace]]
path = "app/src/workspace/hoa_onboarding/welcome_banner.rs"
source = "Agent inbox"
target = "Agent 收件箱"

[[replace]]
path = "app/src/workspace/hoa_onboarding/welcome_banner.rs"
source = "Notifications when any agent needs your attention, also accessible in a central inbox"
target = "当任何 Agent 需要你关注时发送通知，也可在统一收件箱中查看"

[[replace]]
path = "app/src/workspace/hoa_onboarding/welcome_banner.rs"
source = "Native code review"
target = "原生代码审查"

[[replace]]
path = "app/src/workspace/hoa_onboarding/welcome_banner.rs"
source = "Send inline comments from Warp's code review directly to Claude Code, Codex, or OpenCode"
target = "从 Warp 代码审查中直接将行内评论发送给 Claude Code、Codex 或 OpenCode"

[[replace]]
path = "app/src/workspace/hoa_onboarding/welcome_banner.rs"
source = "New"
target = "新增"

[[replace]]
path = "app/src/workspace/hoa_onboarding/welcome_banner.rs"
source = "Introducing universal agent support: level up any coding agent with Warp"
target = "介绍通用 Agent 支持：用 Warp 强化任何编码 Agent"
```

- [ ] **Step 2: Apply translations**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
```

Expected: apply command lists the three HOA files as changed.

- [ ] **Step 3: Verify workspace surface**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset workspace --coverage
cargo fmt --check
git diff --check
cargo check -p warp
```

Expected: all commands exit 0. `cargo check -p warp` may print pre-existing unused-variable warnings only.

- [ ] **Step 4: Commit HOA localization**

Run:

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/workspace/hoa_onboarding/hoa_onboarding_flow.rs app/src/workspace/hoa_onboarding/tab_config_step.rs app/src/workspace/hoa_onboarding/welcome_banner.rs
git commit -m "feat: localize HOA onboarding to zh-Hans"
```

## Task 4: Localize AI Settings Deep Paths

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify after apply: `app/src/settings_view/ai_page.rs`

- [ ] **Step 1: Add AI settings manifest entries**

Append these entries in `resources/localization/zh-Hans-overrides.toml` near existing settings entries:

```toml
[[replace]]
path = "app/src/settings_view/ai_page.rs"
source = "Upgrade to the Build plan"
target = "升级到 Build 方案"

[[replace]]
path = "app/src/settings_view/ai_page.rs"
source = " to use your own API keys."
target = "以使用你自己的 API keys。"

[[replace]]
path = "app/src/settings_view/ai_page.rs"
source = "Ask your team's admin to upgrade to the Build plan to use your own API keys."
target = "请让团队管理员升级到 Build 方案，以使用你自己的 API keys。"

[[replace]]
path = "app/src/settings_view/ai_page.rs"
source = "Create an account"
target = "创建账号"

[[replace]]
path = "app/src/settings_view/ai_page.rs"
source = "Refresh"
target = "刷新"

[[replace]]
path = "app/src/settings_view/ai_page.rs"
source = "Warp loads and sends local AWS CLI credentials for Bedrock-supported models. This setting is managed by your organization."
target = "Warp 会加载并发送本地 AWS CLI 凭据，用于支持 Bedrock 的模型。此设置由你的组织管理。"

[[replace]]
path = "app/src/settings_view/ai_page.rs"
source = "Warp loads and sends local AWS CLI credentials for Bedrock-supported models."
target = "Warp 会加载并发送本地 AWS CLI 凭据，用于支持 Bedrock 的模型。"

[[replace]]
path = "app/src/settings_view/ai_page.rs"
source = "Use AWS Bedrock credentials"
target = "使用 AWS Bedrock 凭据"

[[replace]]
path = "app/src/settings_view/ai_page.rs"
source = "Login Command"
target = "登录命令"

[[replace]]
path = "app/src/settings_view/ai_page.rs"
source = "AWS Profile"
target = "AWS 配置档"

[[replace]]
path = "app/src/settings_view/ai_page.rs"
source = "Automatically run login command"
target = "自动运行登录命令"

[[replace]]
path = "app/src/settings_view/ai_page.rs"
source = "When enabled, the login command will run automatically when AWS Bedrock credentials expire."
target = "启用后，当 AWS Bedrock 凭据过期时会自动运行登录命令。"
```

- [ ] **Step 2: Apply translations**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
```

Expected: `app/src/settings_view/ai_page.rs` changes.

- [ ] **Step 3: Verify settings surface**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset settings --coverage
cargo fmt --check
git diff --check
cargo check -p warp
```

Expected: all commands exit 0. API key examples such as `sk-...`, `sk-ant-...`, and command examples such as `aws login` remain unchanged.

- [ ] **Step 4: Commit AI settings localization**

Run:

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/settings_view/ai_page.rs
git commit -m "feat: localize AI settings deep paths"
```

## Task 5: Localize Rewind And Secret Confirmation Paths

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify after apply: `app/src/terminal/input.rs`
- Modify after apply: `app/src/terminal/input/rewind/search_item.rs`
- Modify after apply: `app/src/terminal/view/ambient_agent/delete_auth_secret_confirmation_dialog.rs`

- [ ] **Step 1: Add terminal confirmation manifest entries**

Append these entries in `resources/localization/zh-Hans-overrides.toml`:

```toml
[[replace]]
path = "app/src/terminal/input.rs"
source = "Search queries to rewind to"
target = "搜索要回退到的查询"

[[replace]]
path = "app/src/terminal/input/rewind/search_item.rs"
source = "Current state (no rewind)"
target = "当前状态（不回退）"

[[replace]]
path = "app/src/terminal/view/ambient_agent/delete_auth_secret_confirmation_dialog.rs"
source = "Are you sure you want to delete {}? This action cannot be undone. Any agents or environments referencing this secret will no longer have access to it."
target = "确定要删除 {} 吗？此操作无法撤销。任何引用此密钥的 Agent 或环境都将无法再访问它。"
```

- [ ] **Step 2: Apply translations**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
```

Expected: terminal input/rewind/auth-secret dialog files change.

- [ ] **Step 3: Verify modal/terminal surface**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset modals --coverage
cargo fmt --check
git diff --check
cargo check -p warp
```

Expected: all commands exit 0.

- [ ] **Step 4: Commit confirmation path localization**

Run:

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/terminal/input.rs app/src/terminal/input/rewind/search_item.rs app/src/terminal/view/ambient_agent/delete_auth_secret_confirmation_dialog.rs
git commit -m "feat: localize terminal confirmation paths"
```

## Task 6: Record Phase 2 Release Audit

**Files:**

- Modify: `docs/zh-Hans-localization.md`
- Modify: `docs/zh-Hans-localization-phase2.md`
- Modify: `README.md`

- [ ] **Step 1: Run final command-line audit**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
cargo fmt --check
git diff --check
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py
cargo check -p warp
cargo test -p warp_search_core
cargo test -p warp command_palette
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Expected: all commands exit 0. Pre-existing `cargo check -p warp` warnings about unused variables are acceptable and must be recorded as pre-existing warning noise.

- [ ] **Step 2: Run GUI smoke for changed surfaces**

Run:

```bash
open -n target/debug/bundle/osx/WarpOss.app
```

Check:

- Workspace launches with Chinese shell/workspace entry text.
- `Cmd-P` command palette still shows Chinese placeholder and Chinese filter chips.
- Settings surfaces touched in this phase do not show obvious English in the translated labels.

Quit the app after smoke.

- [ ] **Step 3: Update release audit docs**

Update `docs/zh-Hans-localization.md`:

- Set manifest entry count to the final dry-run `entries` count.
- Set dry-run summary to the final summary.
- Set coverage snapshot to the final coverage outputs.
- Add Phase 2 validation commands to the passed validation list.
- Add GUI smoke note for HOA onboarding, AI settings deep paths, rewind, and auth secret confirmation if verified.
- Add manual gate notes for account/login paths that still require credentials.

Update `docs/zh-Hans-localization-phase2.md`:

- Add a `Phase 2 execution result` section.
- Record each P2 milestone as completed or manual-gated.
- Record final coverage numbers.

Update `README.md`:

- Change the status wording from first-stage completion to Phase 2 deep coverage in progress or completed, matching actual final verification.

- [ ] **Step 4: Validate docs and commit release audit**

Run:

```bash
git diff --check
git status --short
```

Expected: only planned docs are modified.

Commit:

```bash
git add docs/zh-Hans-localization.md docs/zh-Hans-localization-phase2.md README.md
git commit -m "docs: record phase 2 zh-Hans release audit"
```

## Task 7: Push Phase 2 To GitHub

**Files:** no file edits.

- [ ] **Step 1: Verify local status**

Run:

```bash
git status -sb
git log --oneline --decorate -8
```

Expected: current branch is ahead of `github/main` only by Phase 2 commits; untracked `docs/superpowers/` may contain earlier local plan artifacts not included unless intentionally staged.

- [ ] **Step 2: Push current HEAD to GitHub main**

Run:

```bash
git push github HEAD:main
```

Expected: push exits 0 and updates `Drew1811266/Warp-CN` `main`.

- [ ] **Step 3: Confirm remote**

Run:

```bash
git ls-remote github refs/heads/main
gh repo view Drew1811266/Warp-CN --json nameWithOwner,defaultBranchRef,url
```

Expected: remote `main` points to the current local HEAD, and the repo URL is `https://github.com/Drew1811266/Warp-CN`.
