# zh-Hans 上游同步与 stable 适配流程

本流程用于把 Warp CN 的汉化 overlay 跟随上游 Warp 更新，同时避免把中文源码 fork 维护成独立主线。

当前本地约定：

| 项目 | 值 |
| --- | --- |
| 汉化分支 | `drew/zh-Hans-localization` |
| 上游远程 | `origin  https://github.com/warpdotdev/warp.git` |
| 中文 fork 远程 | `github  https://github.com/Drew1811266/Warp-CN.git` |
| manifest | `resources/localization/zh-Hans-overrides.toml` |
| GUI 矩阵 | `docs/zh-Hans-gui-smoke-matrix.md` |

RC16 预检备注（2026-06-02）：

- 当前执行分支为 `codex/zh-Hans-followup-localization`。
- 该分支没有配置 upstream tracking branch。
- RC16 低负载预检默认不执行 `git fetch origin --tags`。
- 在用户明确要求刷新上游前，不 merge、不 rebase、不切换分支。
- 当前 manifest drift gate 为 `missing: 0`、`would_change: 0`。

RC17 freshness 规则（2026-06-02）：

- RC17 必须显式决定是否刷新上游，不能把 freshness 当成隐含通过。
- 如果当前分支没有 upstream tracking branch，记录该状态并跳过 fetch。
- 如果用户明确批准 fetch，先单独运行 `git fetch origin --tags` 并记录精确基线。
- fetch 步骤不得同时执行 merge、rebase 或 branch switch。
- 任何上游移动后，必须重新运行 manifest validation 和 dry-run summary。

Phase 185 freshness 备注（2026-06-02）：

- 当前执行分支为 `codex/zh-Hans-post-rc26-execution`。
- `git fetch origin --tags` 部分刷新了远端分支，并将 `origin/master` 更新到 `ac4225c1805811a46bfa9df7531e6a4f0058ab12`，但因为多个本地 tag 会被覆盖而退出 1。
- 本轮没有强制覆盖 tag，没有 merge、rebase 或切换分支。
- `git ls-remote --tags origin 'refs/tags/v0.2026.*stable_00'` 显示最新 stable 仍是 `v0.2026.05.27.09.22.stable_00`。
- 当前分支仍包含该 stable 基线；`origin/master` 仅作为预检信息，不作为发布基线。
- 后续如需完整刷新上游 tag，先做非破坏性 tag 冲突审计，再决定是否处理本地同名 tag。

Phase 198 tag 冲突审计备注（2026-06-02）：

- 本轮只读比较了本地 tag、`git ls-remote --tags origin 'refs/tags/v0.2026.*'`、本地 peeled tag commit 和远端 tag commit。
- 本地 tag 总数为 51；远端 `v0.2026.*` tag 总数为 44；本地私有/发布标签 `0.1`、`0.11`、`0.12`、`0.13`、`0.14`、`0.15` 和 `repo-sync/watermark/private-to-public` 是本地-only。
- 同名 `v0.2026.*` tag 的 peeled commit 冲突数为 41。
- 最新 stable 名称仍是 `v0.2026.05.27.09.22.stable_00`，但本地该 tag 指向 `7ed8bbd5dbf701c453ce90a6961f4e6dbcc8d6b4`，远端同名 tag 指向 `2566f54af7c3e71facfe1865f2c492549b14248a`。
- 远端同名 stable commit 当前不是本分支 `HEAD` 的祖先。
- 本轮没有删除 tag、没有 force-fetch、没有 merge、rebase 或切换分支。
- 结论：后续公开 RC 不能再声称当前分支跟随“当前远端 stable tag 目标”；需要单独 upstream-sync 计划来决定是否采纳远端 retarget 后的 stable commit。

Phase 201-206 tree-parity 与 tag namespace 策略（2026-06-02）：

- 本地 `v0.2026.05.27.09.22.stable_00` 目标 `7ed8bbd5dbf701c453ce90a6961f4e6dbcc8d6b4` 和远端同名 tag 目标 `2566f54af7c3e71facfe1865f2c492549b14248a` 的 tree SHA 完全相同：`2281e0a3e27c328bb6bb6f3af82f2d6050780ea7`。
- `git diff --stat` 与 `git diff --name-status` 对这两个 commit 没有输出；本轮 retarget 冲突是 commit/tag/parent 身份差异，不是源码树差异。
- 当前策略是 **tree-parity adoption without destructive tag mutation**：公开表述可以说当前选定源码基线与远端 stable 目标 tree-parity 一致，但不能声称当前 `HEAD` 在祖先关系上包含远端 stable commit。
- 本地 fork release tags `0.1` 到 `0.15` 视为 fork-owned release labels。
- 本地 `v0.2026.*` tag 视为 cached upstream labels；判断当前远端 truth 时必须使用 `git ls-remote --tags origin ...` 或明确 commit/tree ID。
- 不删除、不 force-fetch、不覆盖本地 `v0.2026.*` tag，除非用户明确批准 exact tag/ref action。
- 如果未来必须满足 ancestry-based remote stable adoption，再创建独立 upstream-sync branch，从 `2566f54af7c3e71facfe1865f2c492549b14248a` replay localization overlay。

## 1. 发布策略

用户发布版只跟随 **stable 或明确选定的上游基线**。不要追着上游 dev/nightly 每天发布中文构建版。

如果上游没有可直接使用的 stable tag，就在每次发布前明确记录一个 `UPSTREAM_BASE`：

- 上游 release tag。
- 上游 release branch。
- 上游 `origin/master` 上经过人工选定的 commit。

`origin/master` 可以用于预检，但预检结果不等同于可发布版本。

## 2. 同步前检查

先确认当前工作区没有未理解的改动：

```bash
git status --short
git branch --show-current
git remote -v
```

如果有未提交文件，先判断来源：

- 本轮汉化工具或文档改动：继续纳入当前工作。
- 用户未提交改动：不要覆盖，必要时先让用户确认。
- 构建产物或临时文件：不要纳入发布记录。

记录当前汉化基线：

```bash
git rev-parse HEAD
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
```

## 3. 获取上游基线

获取上游：

```bash
git fetch origin --tags
```

选择基线并记录：

```bash
UPSTREAM_BASE=<tag-or-commit>
git rev-parse "$UPSTREAM_BASE"
```

建议把本次同步记录写入 release notes 或维护文档：

```text
Upstream base: <tag-or-commit>
Upstream commit: <sha>
Sync date: YYYY-MM-DD
Manifest entries before sync: <n>
```

## 4. 合并或重放上游

默认使用 merge，便于保留本地汉化历史：

```bash
git switch drew/zh-Hans-localization
git merge "$UPSTREAM_BASE"
```

如果明确需要线性历史，可以使用 rebase：

```bash
git switch drew/zh-Hans-localization
git rebase "$UPSTREAM_BASE"
```

如果发生冲突，优先保留上游源码结构，再用 manifest 重新应用中文 overlay。不要手工把中文源码当作唯一真相。

## 5. 漂移检查

合并后先不直接构建，先检查 manifest 漂移：

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
```

期望：

```text
missing: 0
```

如果出现 `missing`：

1. 打开报错中的 `path`。
2. 查找上游新的英文文案、移动后的文件或被删除的功能。
3. 更新对应 manifest 条目的 `path`、`source`、`target` 或 `status`。
4. 如果功能被上游删除，将条目标记为 `deprecated` 或移除，并记录原因。
5. 重新运行 dry-run，直到 `missing: 0`。

如果 `would_change` 大于 0，说明当前工作树还没有应用 overlay：

```bash
python3 script/zh_apply_localization.py
cargo fmt
```

## 6. 覆盖率和候选审计

同步后记录覆盖率：

```bash
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
```

如果候选数量大幅变化，先看热点路径：

```bash
python3 script/zh_localization_inventory.py --preset workspace --top-paths 20
python3 script/zh_localization_inventory.py --preset settings --top-paths 20
python3 script/zh_localization_inventory.py --preset modals --top-paths 20
```

新增 ignore 规则前必须先审查候选：

```bash
python3 script/zh_localization_inventory.py app/src/example.rs --status candidate
```

不要为了提高覆盖率隐藏真实 UI 文案。

## 7. 命令行 release gate

发布前运行完整命令行 gate：

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_export_locale.py --format json > /tmp/zh-CN.json
python3 script/zh_export_locale.py --format yaml > /tmp/zh-CN.yaml
cargo fmt --check
git diff --check
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py script/zh_export_locale.py script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
python3 script/test_zh_apply_localization.py
python3 script/test_zh_localization_inventory.py
python3 script/test_zh_export_locale.py
cargo check -p warp
cargo test -p warp_search_core
cargo test -p warp command_palette
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

当前 app crate package 名称是 `warp`，不要使用旧的 `cargo check -p app`。

## 8. GUI release gate

命令行 gate 通过后，按 GUI 矩阵复验：

```bash
open -n target/debug/bundle/osx/WarpOss.app
```

更新 `docs/zh-Hans-gui-smoke-matrix.md` 中的状态：

- 能看到对应中文文案：`verified`。
- 需要账号、计费、团队、云端、错误状态：保持或标记为 `manual-gate` / `needs-trigger`。
- 窗口读取失败：记录为 `automation-blocked`，不要写成 `verified`。

必须至少确认基础工作区：

- macOS 菜单栏。
- 全局搜索占位符。
- `新会话` 入口。
- 命令面板筛选标签。

## 9. 发布记录模板

每次同步完成后记录：

```markdown
## zh-Hans sync YYYY-MM-DD

- Upstream base: `<tag-or-commit>`
- Upstream commit: `<sha>`
- Manifest: `<entries>` entries, `<files>` files
- Dry-run: `missing: 0`
- Release coverage: `<covered>` covered, `<candidates>` candidates, `<coverage>%`
- Locale export: JSON/YAML generated and JSON parse passed
- Command-line gate: passed / failed
- GUI matrix: `<n>` verified, `<n>` manual-gate, `<n>` needs-trigger
- Bundle: `target/debug/bundle/osx/WarpOss.app`
- Notes:
  - ...
```

## 10. 失败处理

| 失败 | 处理 |
| --- | --- |
| manifest parse 或 validation 失败 | 修复 manifest schema，再继续。 |
| glossary check 失败 | 判断是误译、合理历史译法，还是 glossary 过严；不要直接删除规则绕过。 |
| dry-run `missing` | 更新 `path/source/status`，说明上游漂移原因。 |
| coverage 分母突增 | 用 `--top-paths` 找热点，先审查再决定翻译或 ignore。 |
| Rust 编译失败 | 先确认是否由上游同步引入，再判断是否和翻译替换有关。 |
| bundle gate 失败 | 记录完整输出；`TERM=xterm-256color` 是当前本地规避 `ColorOutOfRange` 的必要条件。 |
| GUI 自动化失败 | 记录为 `automation-blocked`，不要替代人工视觉复验。 |

## zh-Hans sync rehearsal 2026-05-30

This P4-M7 rehearsal did not merge or rebase. It only checked the current localization branch against the latest locally available stable tag and recorded the network state.

- Branch: `drew/zh-Hans-localization`
- Local HEAD: `305b2821f493eb2d0526a13669bbdf0fe8f74d51`
- Local HEAD subject: `docs: record phase 2 round 4 audit`
- Selected upstream base: `v0.2026.05.27.09.22.stable_00`
- Selected upstream commit: `2566f54af7c3e71facfe1865f2c492549b14248a`
- Selected upstream subject: `Enable async find on dogfood, add toggle for Preview/Stable (#11555)`
- Local `origin/master` ref at rehearsal time: `ce73fe07bfd80f778bc21b60fd1ed987a22d5840`
- Merge-base of `HEAD` and selected stable tag: `2566f54af7c3e71facfe1865f2c492549b14248a`
- Ahead/behind against selected stable tag: `88 0`

Fetch attempts:

```text
git fetch origin --tags
fatal: unable to access 'https://github.com/warpdotdev/warp.git/': Error in the HTTP2 framing layer

git -c http.version=HTTP/1.1 fetch origin --tags
fatal: unable to access 'https://github.com/warpdotdev/warp.git/': Failed to connect to github.com port 443 after 75004 ms: Couldn't connect to server
```

Decision:

- No upstream merge/rebase was performed because the current branch is already ahead of the latest locally available stable tag and not behind it.
- Before a public release, retry `git fetch origin --tags` on a working network and reselect the upstream base if a newer stable tag appears.

Post-rehearsal preflight:

```text
manifest validation passed
glossary check passed
entries: 2619
files: 190
already_applied: 2604
would_change: 0
missing: 0
preset: release
covered: 2845
candidates: 6453
coverage: 30.6%
```

## zh-Hans stable refresh 2026-05-30 P5-M1

This Phase 5 refresh attempted to remove the Phase 4 uncertainty around stale upstream refs. The network still could not reach GitHub reliably, so no merge/rebase was performed and no public-release freshness claim should be made.

- Branch: `drew/zh-Hans-localization`
- Local HEAD: `305b2821f493eb2d0526a13669bbdf0fe8f74d51`
- Latest locally available stable tag before/after refresh attempt: `v0.2026.05.27.09.22.stable_00`
- Selected local stable commit: `2566f54af7c3e71facfe1865f2c492549b14248a`
- Selected local stable subject: `Enable async find on dogfood, add toggle for Preview/Stable (#11555)`
- Merge-base of `HEAD` and selected local stable tag: `2566f54af7c3e71facfe1865f2c492549b14248a`
- Ahead/behind against selected local stable tag: `88 0`

Fetch attempts:

```text
git fetch origin --tags
fatal: unable to access 'https://github.com/warpdotdev/warp.git/': Failed to connect to github.com port 443 after 75004 ms: Couldn't connect to server

git -c http.version=HTTP/1.1 ls-remote --tags origin '*stable*'
fatal: unable to access 'https://github.com/warpdotdev/warp.git/': SSL connection timeout
```

Decision:

- Continue Phase 5 using local stable refs for engineering validation only.
- Keep public release freshness blocked until `git fetch origin --tags` or equivalent upstream ref refresh succeeds.

## zh-Hans stable refresh 2026-05-31 P6-M1

This Phase 6 refresh successfully reached upstream and refreshed refs. No newer stable tag appeared after fetch, so RC3 remains pinned to the latest fetched stable tag rather than a stale local-only assumption.

- Branch: `drew/zh-Hans-localization`
- Remotes:
  - `origin  https://github.com/warpdotdev/warp.git`
  - `github  https://github.com/Drew1811266/Warp-CN.git`
- Fetch command: `git fetch origin --tags`
- Fetch result: passed
- New dev tags observed in fetch output:
  - `v0.2026.05.29.09.24.dev_00`
  - `v0.2026.05.30.08.57.dev_00`
- Newer stable tag after fetch: none
- Selected stable base: `v0.2026.05.27.09.22.stable_00`
- Selected stable commit: `2566f54af7c3e71facfe1865f2c492549b14248a`
- Selected stable subject: `Enable async find on dogfood, add toggle for Preview/Stable (#11555)`
- Current `origin/master`: `74d256646c24f5ac8cc93af1792e57e35062cc44`
- Current `origin/master` subject: `[4/5] Use remote-aware skill locations in UI consumers (#11581)`
- Ahead/behind against selected stable tag: `0 88` from `git rev-list --left-right --count "$UPSTREAM_BASE...HEAD"`

Post-refresh drift check:

```text
entries: 2645
files: 194
already_applied: 2630
would_change: 0
missing: 0
```

Decision:

- Upstream freshness blocker is cleared for stable refs as of 2026-05-31.
- No merge or rebase is needed because the latest fetched stable tag is unchanged and the current branch is not behind it.
- Public-RC readiness still depends on GUI evidence and state fixture records.

## zh-Hans stable refresh 2026-06-04 0.19 adaptation

- Selected upstream base: `v0.2026.06.03.09.49.stable_00`
- Selected upstream commit: `2249469e5d24e472cee6ce97d3d324293f67db71`
- Selected upstream tree: `efe8ae7822765eb267792d441e4b1e7ddb7f8e53`
- Selected upstream branch: `stable_release/v0.2026.06.03.09.49.stable`
- Adaptation branch: `codex/zh-Hans-0.19-upstream-stable-adaptation`
- Worktree: `/Users/drew/Project/warp-cn-0.19-adaptation`
- Strategy: clean upstream stable worktree plus durable zh-Hans asset import, followed by manifest overlay regeneration.
- Public-release posture: blocked until 0.19 command-line gates, fresh bundle, GUI evidence, and public-RC evidence gates are complete.

## zh-Hans latest-source sync 2026-06-24 pre-merge baseline

This record captures the baseline before merging latest upstream source into the
Warp CN sync branch. No upstream merge, rebase, package, release, or tag mutation
was performed in this step.

- Branch: `codex/zh-Hans-upstream-latest-2026-06-24`
- Branch point: `3229258e3cb055b40daf563e0cabb36bfc3a65f9`
- Current branch head after planning commits: `61ca8ac7`
- Current branch subject: `docs: refresh latest upstream sync base`
- Current fork release tag: `0.20.6`
- Upstream product changelog latest checked: `2026.06.17 (v0.2026.06.17.09.49)`
- GitHub latest stable release checked: `v0.2026.06.03.09.49.stable_00`
- GitHub latest dev release checked: `v0.2026.06.09.19.54.dev_00`
- Selected upstream source base: `origin/master`
- Selected upstream source commit: `6691e1e0e0408be8bdcb1891e3a795564cedd897`
- Selected upstream source subject: `Make the New API key modal's Agent picker searchable (#12972)`
- Selected upstream source date: `2026-06-23T19:42:07-07:00`
- Stable source branch still available: `stable_release/v0.2026.06.03.09.49.stable`
- Stable source branch commit: `2249469e5d24e472cee6ce97d3d324293f67db71`
- Ahead/behind against selected latest source: `895 305`
- Diff scale against selected latest source: `1914 files changed, 101928 insertions(+), 803509 deletions(-)`

Release API evidence:

```text
gh api repos/warpdotdev/warp/releases/latest
tag_name: v0.2026.06.03.09.49.stable_00
name: Stable Release v0.2026.06.03.09.49.stable_00
published_at: 2026-06-03T09:49:25Z
prerelease: false
draft: false

gh api 'repos/warpdotdev/warp/releases?per_page=20'
newest listed release: v0.2026.06.09.19.54.dev_00
newest listed stable release: v0.2026.06.03.09.49.stable_00
```

Pre-merge zh-Hans validation:

```text
python3 script/zh_apply_localization.py --validate-manifest
manifest validation passed

python3 script/zh_apply_localization.py --check-glossary
glossary check passed

python3 script/zh_apply_localization.py --dry-run --summary
entries: 7937
files: 550
already_applied: 5713
would_change: 0
missing: 0

python3 script/zh_localization_inventory.py --preset release --coverage
preset: release
covered: 8532
candidates: 10
coverage: 99.9%

git diff --check
passed

cargo fmt --check
passed
```

Mojibake scan result:

```text
python3 script/zh_mojibake_scan.py
app/assets/bundled/bootstrap/subshell_bootstrap_block_command.txt: terminal-ansi-sequence: accepted-token
crates/editor/test_data/test_rust_file.rs: replacement-character: fixture-only
docs/zh-Hans-localization-calibration-plan.md: replacement-character: example-only
docs/zh-Hans-localization-calibration-plan.md: mojibake-signature: example-only
```

Decision:

- Continue with a latest-source sync against `origin/master`, not a newer official stable tag adoption.
- Preserve local upstream tag namespace; do not force-fetch or overwrite local `v0.2026.*` tags.
- Proceed to upstream merge only after this durable baseline is committed.
