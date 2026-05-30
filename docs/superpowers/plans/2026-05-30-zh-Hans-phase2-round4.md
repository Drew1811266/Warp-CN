# Warp CN Phase 2 Round 4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the next Phase 2 slice from broad translation into a release-quality audit pass: improve localization inventory precision, record intentional exclusions, then translate a small set of verified user-visible English remnants.

**Architecture:** Keep the manifest-driven zh-Hans workflow as the source of truth. Improve `script/zh_localization_inventory.py` only where it makes the candidate pool more truthful, add exact `path`/`source`/`target` entries to `resources/localization/zh-Hans-overrides.toml`, apply them with `script/zh_apply_localization.py`, and verify each milestone before continuing.

**Tech Stack:** Rust UI source, TOML localization manifest, Python inventory/apply scripts, Cargo formatting/check/test commands, macOS `WarpOss.app` bundle and GUI smoke gate.

---

## Current Baseline

Baseline captured on 2026-05-30 after Phase 2 Round 3:

```text
entries: 2543
files: 184
already_applied: 2528
would_change: 0
missing: 0
```

Coverage baseline:

| Preset | Covered | Candidates | Coverage |
| --- | ---: | ---: | ---: |
| `onboarding` | 266 | 55 | 82.9% |
| `workspace` | 582 | 392 | 59.8% |
| `search` | 267 | 40 | 87.0% |
| `settings` | 1170 | 860 | 57.6% |
| `modals` | 626 | 5813 | 9.7% |
| `release` | 2789 | 7139 | 28.1% |

Round 3 also confirmed that Git HTTPS transport to GitHub can fail in this environment while `gh api` still works. Round 4 must keep that as a release-sync risk instead of assuming `git push` is always available.

## Why Round 4 Is An Audit-First Round

The remaining `workspace`, `settings`, and `modals` candidate pools are no longer simple "untranslated UI strings" lists.

Observed candidate hotspots:

| Preset | High-count paths | Interpretation |
| --- | --- | --- |
| `workspace` | `app/src/workspace/view.rs`, `app/src/workspace/mod.rs`, `app/src/workspace/tab_settings.rs`, `app/src/workspace/cross_window_tab_drag.rs` | Mix of real menu/toast labels, debug assertions, logs, worktree diagnostics, and internal command text. |
| `settings` | `app/src/settings_view/features_page.rs`, `app/src/settings_view/mod.rs`, `app/src/settings_view/teams_page.rs`, `app/src/settings_view/appearance_page.rs`, `app/src/settings_view/ai_page.rs` | Many are search terms, examples, feature metadata, and some real UI labels. |
| `modals` | `app/src/terminal/**`, `app/src/ai/agent_sdk/**`, `app/src/ai/agent/conversation_yaml.rs`, `app/src/ai/agent/mod.rs` | Large amount of terminal parser state, Agent SDK internals, YAML export schema, harness prompts, and transcript templates. |

The next step is not to chase `modals` coverage directly. The correct objective is to make the inventory better at separating user-facing UI from internal infrastructure, then translate verified visible remnants.

## Scope

Round 4 includes:

- Inventory reporting improvements that make candidate review faster and more reproducible.
- Conservative noise filtering for clearly non-UI diagnostics and serialization templates.
- A documented exclusion ledger so hidden candidates are reviewable.
- Targeted translations for verified user-visible remnants:
  - Warp on Web home pane title and content.
  - Agent conversation status labels.
  - AWS Bedrock credential error display.
  - Small settings/workspace fallback strings that can surface in toast or row labels.

Round 4 excludes:

- Broad translation of Agent SDK harness prompts, API conversion errors, YAML export field names, terminal ANSI/parser internals, telemetry event names, and debug-only menus.
- Translation of product names, model names, command syntax, URLs, file extensions, config keys, and settings search keyword blobs.
- Any runtime localization architecture refactor.
- Any claim that GUI smoke is complete if the local `WarpOss` window remains unreadable to automation.

## File Map

### Inventory And Apply Tooling

- Modify: `script/zh_localization_inventory.py`
  - Add candidate summary output by path.
  - Add candidate-status filtering for focused review.
  - Add conservative skip patterns for logging and internal diagnostics.
  - Add exact-path exclusions only after each path is documented.
- Modify if needed: `script/zh_apply_localization.py`
  - Add raw string support and multiline manifest value support only if translating `app/src/workspace/home.rs` content through the manifest.
  - Preserve strict exact-match behavior and duplicate detection.

### Manifest

- Modify: `resources/localization/zh-Hans-overrides.toml`
  - Append Round 4 entries in task order.
  - Preserve placeholders such as `{model_name}`, `{error}`, `{query}`, and Markdown formatting.

### Source Files Modified By Apply Script

- `app/src/workspace/home.rs`
- `app/src/ai/agent/conversation.rs`
- `app/src/ai/agent/mod.rs`
- `app/src/settings_view/agent_assisted_environment_modal.rs`

### Documentation

- Modify: `README.md`
- Modify: `docs/zh-Hans-localization.md`
- Modify: `docs/zh-Hans-localization-phase2.md`

## Task 0: Commit The Round 4 Plan

**Files:**

- Create: `docs/superpowers/plans/2026-05-30-zh-Hans-phase2-round4.md`

- [ ] **Step 1: Verify the plan file exists**

Run:

```bash
test -s docs/superpowers/plans/2026-05-30-zh-Hans-phase2-round4.md
```

Expected: exit code 0.

- [ ] **Step 2: Scan for planning placeholders**

Run:

```bash
rg -n 'T[B]D|T[O]DO|implement late[r]|fill in detail[s]|Similar t[o]|probabl[y]' docs/superpowers/plans/2026-05-30-zh-Hans-phase2-round4.md
```

Expected: exit code 1 with no matches.

- [ ] **Step 3: Verify diff hygiene**

Run:

```bash
git diff --check
```

Expected: exit code 0.

- [ ] **Step 4: Commit the plan**

Run:

```bash
git add docs/superpowers/plans/2026-05-30-zh-Hans-phase2-round4.md
git commit -m "docs: plan phase 2 round 4 zh-Hans localization"
```

Expected: one commit containing only the Round 4 plan file.

## Task 1: Add Inventory Review Modes

**Files:**

- Modify: `script/zh_localization_inventory.py`

- [ ] **Step 1: Capture current path-count evidence**

Run:

```bash
python3 script/zh_localization_inventory.py --preset workspace | awk -F'`' '/candidate/ {count[$2]++} END {for (p in count) print count[p], p}' | sort -nr | sed -n '1,40p'
python3 script/zh_localization_inventory.py --preset settings | awk -F'`' '/candidate/ {count[$2]++} END {for (p in count) print count[p], p}' | sort -nr | sed -n '1,40p'
python3 script/zh_localization_inventory.py --preset modals | awk -F'`' '/candidate/ {count[$2]++} END {for (p in count) print count[p], p}' | sort -nr | sed -n '1,50p'
```

Expected: output is saved in the task notes or summarized in `docs/zh-Hans-localization-phase2.md` after implementation.

- [ ] **Step 2: Add focused review CLI flags**

Implement:

```text
--status candidate|covered-source|covered-target
--top-paths N
```

Behavior:

- `--status candidate` prints only candidate rows.
- `--status covered-source` prints only original English strings that are declared in the manifest.
- `--status covered-target` prints only strings that have already been replaced in source.
- `--top-paths N` prints a Markdown table with candidate counts grouped by path and capped at `N`.
- If both `--coverage` and `--top-paths` are passed, fail with exit code 2 and a clear argparse error because they are different report modes.

- [ ] **Step 3: Verify the new review modes**

Run:

```bash
python3 script/zh_localization_inventory.py --preset workspace --status candidate | sed -n '1,20p'
python3 script/zh_localization_inventory.py --preset settings --status covered-target | sed -n '1,20p'
python3 script/zh_localization_inventory.py --preset modals --top-paths 20
python3 script/zh_localization_inventory.py --preset release --coverage
python3 -m py_compile script/zh_localization_inventory.py
```

Expected:

- Candidate-only output does not include `covered-source` or `covered-target`.
- Top-path output is a stable Markdown table.
- Existing coverage output remains unchanged in shape.
- Python compile check exits 0.

- [ ] **Step 4: Commit inventory review modes**

Run:

```bash
git add script/zh_localization_inventory.py
git commit -m "chore: add zh-Hans inventory review modes"
```

## Task 2: Apply Conservative Inventory Noise Filtering

**Files:**

- Modify: `script/zh_localization_inventory.py`
- Modify: `docs/zh-Hans-localization-phase2.md`

- [ ] **Step 1: Add logging and diagnostic line filters**

Extend `SKIP_LINE_PATTERNS` only with patterns that clearly identify non-UI diagnostic code, such as:

```python
"tracing::",
"debug!(",
"info!(",
"warn!(",
"error!(",
"println!(",
"eprintln!(",
".context(",
"bail!(",
"ensure!(",
```

Do not add a generic filter for strings that begin with `Failed to` because some user-facing toasts use that phrasing.

- [ ] **Step 2: Add exact-path exclusion review list**

Add a small exact-path exclusion mechanism for files that have been reviewed and classified as non-UI. The first Round 4 list should be conservative:

```text
app/src/ai/agent/conversation_yaml.rs
app/src/themes/theme.rs
app/src/terminal/model/ansi/mod.rs
app/src/terminal/model/ansi/dcs_hooks.rs
```

Before adding any other path, inspect it with `python3 script/zh_localization_inventory.py <path> --status candidate` and record why it is safe to exclude.

- [ ] **Step 3: Verify no high-visible strings were hidden**

Run:

```bash
python3 script/zh_localization_inventory.py --preset workspace --top-paths 30
python3 script/zh_localization_inventory.py --preset settings --top-paths 30
python3 script/zh_localization_inventory.py --preset modals --top-paths 30
python3 script/zh_localization_inventory.py --preset release --coverage
rg -n '"更新 Warp"|"设置"|"账单和用量"|"Agent 对话"|"云端 Agent"' app/src/workspace app/src/settings_view app/src/ai
python3 -m py_compile script/zh_localization_inventory.py script/zh_apply_localization.py
```

Expected:

- Top-path reports still include real UI-heavy files.
- Known Chinese UI strings remain in source.
- `release` coverage changes are documented as an inventory denominator change, not a product translation jump.

- [ ] **Step 4: Document exclusion rationale**

Append a Round 4 subsection to `docs/zh-Hans-localization-phase2.md` with:

- Before/after coverage counts for `workspace`, `settings`, `modals`, and `release`.
- The exact excluded paths.
- The reason each path is classified as non-UI.
- A note that future contributors must inspect paths before adding them to the exclusion list.

- [ ] **Step 5: Commit inventory filtering**

Run:

```bash
git add script/zh_localization_inventory.py docs/zh-Hans-localization-phase2.md
git commit -m "chore: refine zh-Hans inventory noise filters"
```

## Task 3: Support And Translate Warp On Web Home Content

**Files:**

- Modify: `script/zh_apply_localization.py`
- Modify: `script/zh_localization_inventory.py`
- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify after apply: `app/src/workspace/home.rs`

- [ ] **Step 1: Confirm raw string limitation**

Run:

```bash
rg -n 'WARP_HOME_TITLE|WARP_HOME_CONTENT|r#"' app/src/workspace/home.rs script/zh_apply_localization.py script/zh_localization_inventory.py
python3 script/zh_localization_inventory.py app/src/workspace/home.rs
```

Expected:

- `WARP_HOME_TITLE` appears as a candidate.
- `WARP_HOME_CONTENT` is not covered by current inventory because raw strings are skipped.

- [ ] **Step 2: Add raw string and multiline manifest support**

Update `load_manifest`, `replace_rust_string_literals`, and `extract_string_literals` so raw string literals can be represented in the manifest and matched exactly while preserving delimiter syntax.

Rules:

- Keep existing one-line `key = "value"` behavior unchanged.
- Add support for multiline manifest values delimited as `key = """` followed by content lines and a closing `"""`.
- Allow multiline values for `source` and `target`; integer fields such as `expected_count` remain one-line only.
- Parsed multiline values must preserve internal newlines exactly.
- Preserve the existing raw string delimiter count.
- Do not unescape or reinterpret raw string content.
- Replace only when the full raw string content exactly equals the manifest `source`.
- Continue to skip comments and char literals.
- Existing non-raw replacement behavior must remain unchanged.

- [ ] **Step 3: Add manifest entries**

Append:

```toml
[[replace]]
path = "app/src/workspace/home.rs"
source = "Welcome to Warp on Web"
target = "欢迎使用网页版 Warp"

[[replace]]
path = "app/src/workspace/home.rs"
source = """
Welcome to Warp on Web - your browser-based home for Warp! 
Use Warp on Web to:
* Join Shared Sessions
* Create, View, and Edit Warp Drive Objects
* Manage your Warp Settings

Warp on Web can also be used by your teammates and peers who don't have Warp downloaded yet to view your shared sessions, notebooks, and workflows."""
target = """
欢迎使用网页版 Warp，这是你在浏览器中的 Warp 主页！
你可以使用网页版 Warp：
* 加入共享会话
* 创建、查看和编辑 Warp Drive 对象
* 管理 Warp 设置

尚未下载 Warp 的团队成员和协作者，也可以通过网页版 Warp 查看你共享的会话、Notebook 和工作流。"""
```

- [ ] **Step 4: Apply and verify**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py app/src/workspace/home.rs
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py
cargo fmt --check
git diff --check
```

Expected:

- Apply dry-run reports `would_change: 0` and `missing: 0` after applying.
- `app/src/workspace/home.rs` no longer reports the English Warp on Web title/content as candidates.
- Raw string syntax remains valid after `cargo fmt`.

- [ ] **Step 5: Commit Warp on Web home translation**

Run:

```bash
git add script/zh_apply_localization.py script/zh_localization_inventory.py resources/localization/zh-Hans-overrides.toml app/src/workspace/home.rs
git commit -m "feat: localize Warp on Web home"
```

## Task 4: Translate Agent Status And Error Residue

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify after apply: `app/src/ai/agent/conversation.rs`
- Modify after apply: `app/src/ai/agent/mod.rs`

- [ ] **Step 1: Confirm target strings still exist**

Run:

```bash
rg -n '"In progress"|"Done"|"Error"|"Cancelled"|"Blocked"|"Error: \\{error\\}"|"AWS Bedrock credentials expired or invalid for \\{model_name\\}"|"Web search failed for: \\{query\\}"|"Web fetch failed"' app/src/ai/agent/conversation.rs app/src/ai/agent/mod.rs resources/localization/zh-Hans-overrides.toml
```

Expected: target strings appear in source files, and no duplicate `path`/`source` entry already exists in the manifest.

- [ ] **Step 2: Add manifest entries**

Append:

```toml
[[replace]]
path = "app/src/ai/agent/conversation.rs"
source = "In progress"
target = "进行中"

[[replace]]
path = "app/src/ai/agent/conversation.rs"
source = "Done"
target = "已完成"

[[replace]]
path = "app/src/ai/agent/conversation.rs"
source = "Error"
target = "错误"

[[replace]]
path = "app/src/ai/agent/conversation.rs"
source = "Cancelled"
target = "已取消"

[[replace]]
path = "app/src/ai/agent/conversation.rs"
source = "Blocked"
target = "已阻止"

[[replace]]
path = "app/src/ai/agent/mod.rs"
source = "Error: {error}"
target = "错误：{error}"

[[replace]]
path = "app/src/ai/agent/mod.rs"
source = "AWS Bedrock credentials expired or invalid for {model_name}"
target = "AWS Bedrock 凭据已过期，或对 {model_name} 无效"

[[replace]]
path = "app/src/ai/agent/mod.rs"
source = "Web search failed for: {query}"
target = "网页搜索失败：{query}"

[[replace]]
path = "app/src/ai/agent/mod.rs"
source = "Web fetch failed"
target = "网页获取失败"
```

- [ ] **Step 3: Apply and verify**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py app/src/ai/agent/conversation.rs --status candidate | sed -n '1,80p'
python3 script/zh_localization_inventory.py app/src/ai/agent/mod.rs --status candidate | sed -n '1,120p'
cargo fmt --check
git diff --check
cargo check -p warp
```

Expected:

- Apply dry-run reports `would_change: 0` and `missing: 0` after applying.
- The translated status labels are no longer candidates.
- Remaining candidates in `app/src/ai/agent/mod.rs` are mostly transcript templates, command snippets, programming language names, or internal diagnostics.
- `cargo check -p warp` exits 0 with only known warnings.

- [ ] **Step 4: Commit Agent residue translation**

Run:

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/ai/agent/conversation.rs app/src/ai/agent/mod.rs
git commit -m "feat: localize agent status residue"
```

## Task 5: Translate Small Verified Settings Fallbacks

**Files:**

- Modify: `resources/localization/zh-Hans-overrides.toml`
- Modify after apply: `app/src/settings_view/agent_assisted_environment_modal.rs`

- [ ] **Step 1: Confirm target strings still exist**

Run:

```bash
rg -n '"\\(unknown\\)"|"No directory selected"' app/src/settings_view/agent_assisted_environment_modal.rs resources/localization/zh-Hans-overrides.toml
```

Expected: both strings appear in source and are not duplicate manifest entries.

- [ ] **Step 2: Add manifest entries**

Append:

```toml
[[replace]]
path = "app/src/settings_view/agent_assisted_environment_modal.rs"
source = "(unknown)"
target = "（未知）"

[[replace]]
path = "app/src/settings_view/agent_assisted_environment_modal.rs"
source = "No directory selected"
target = "未选择目录"
```

- [ ] **Step 3: Apply and verify**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_apply_localization.py
cargo fmt
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py app/src/settings_view/agent_assisted_environment_modal.rs --status candidate
cargo fmt --check
git diff --check
cargo check -p warp
```

Expected:

- Apply dry-run reports `would_change: 0` and `missing: 0` after applying.
- The remaining candidates in the file are reviewed and classified as internal, examples, or already out of Round 4 scope.
- `cargo check -p warp` exits 0 with only known warnings.

- [ ] **Step 4: Commit settings fallback translation**

Run:

```bash
git add resources/localization/zh-Hans-overrides.toml app/src/settings_view/agent_assisted_environment_modal.rs
git commit -m "feat: localize environment modal fallbacks"
```

## Task 6: Round 4 Release Audit And Documentation

**Files:**

- Modify: `README.md`
- Modify: `docs/zh-Hans-localization.md`
- Modify: `docs/zh-Hans-localization-phase2.md`

- [ ] **Step 1: Capture final apply and coverage snapshot**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset onboarding --coverage
python3 script/zh_localization_inventory.py --preset workspace --coverage
python3 script/zh_localization_inventory.py --preset search --coverage
python3 script/zh_localization_inventory.py --preset settings --coverage
python3 script/zh_localization_inventory.py --preset modals --coverage
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_localization_inventory.py --preset workspace --top-paths 20
python3 script/zh_localization_inventory.py --preset settings --top-paths 20
python3 script/zh_localization_inventory.py --preset modals --top-paths 20
```

Expected: documentation records both coverage and top candidate paths so the numbers are interpretable.

- [ ] **Step 2: Update docs**

Update:

- `README.md`
  - Current manifest entry count and file count.
  - Round 4 summary.
  - Note that remaining low `modals` coverage is dominated by non-UI Agent/terminal internals after review.
- `docs/zh-Hans-localization.md`
  - Final Round 4 validation commands.
  - GUI smoke gate result.
  - GitHub sync note.
- `docs/zh-Hans-localization-phase2.md`
  - Add `## 7.3 第二阶段 Round 4 执行结果`.
  - Include coverage table, top-path table summary, exclusion ledger, translated files, and residual risks.

- [ ] **Step 3: Run full verification**

Run:

```bash
python3 script/zh_apply_localization.py --dry-run --summary
python3 -m py_compile script/zh_apply_localization.py script/zh_localization_inventory.py
cargo fmt --check
git diff --check
cargo check -p warp
cargo test -p warp_search_core
cargo test -p warp command_palette
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Expected:

- Apply dry-run reports `would_change: 0` and `missing: 0`.
- Python compile check exits 0.
- Cargo checks/tests exit 0, allowing only known warnings.
- macOS bundle is produced at `target/debug/bundle/osx/WarpOss.app`.

- [ ] **Step 4: Run GUI smoke or record manual gate**

Run:

```bash
open -n target/debug/bundle/osx/WarpOss.app
pgrep -fl WarpOss
```

Attempt to inspect:

- Warp on Web home pane if reachable.
- Agent conversation status labels if a conversation list/details surface is reachable.
- Agent Assisted Environment modal fallback paths if reachable.
- Previously translated Round 3 launch/credit/plan/conversation details surfaces if reachable.

If desktop automation times out again, record:

- The app process launched.
- The GUI inspection target.
- The automation failure mode.
- The manual smoke item that remains for the user.

- [ ] **Step 5: Commit Round 4 docs**

Run:

```bash
git add README.md docs/zh-Hans-localization.md docs/zh-Hans-localization-phase2.md
git commit -m "docs: record phase 2 round 4 audit"
```

## Task 7: Remote Sync

**Files:** none unless Git metadata changes.

- [ ] **Step 1: Try normal Git transport first**

Run:

```bash
git push github drew/zh-Hans-localization:main
```

Expected: branch pushes to `Drew1811266/Warp-CN` if HTTPS transport is available.

- [ ] **Step 2: If Git HTTPS fails, use GitHub API fallback**

Only use this fallback if `git push` fails with the known network timeout.

Required checks before API fallback:

```bash
git rev-parse HEAD^{tree}
gh api repos/Drew1811266/Warp-CN/branches/main --jq '.commit.sha'
```

Fallback must create remote commits that preserve:

- Commit order.
- Commit messages.
- Final tree equality with local `HEAD`.

After fallback, verify:

```bash
git rev-parse HEAD^{tree}
gh api repos/Drew1811266/Warp-CN/git/refs/heads/main --jq '.object.sha'
gh api repos/Drew1811266/Warp-CN/git/commits/<remote-main-sha> --jq '.tree.sha'
```

Expected: remote main tree SHA equals local `HEAD^{tree}`.

## Automatic Review Gates

After each task:

- Run the task-specific verification commands.
- Inspect `git diff --stat` and `git diff --check`.
- Confirm the changed files match the task file map.
- Confirm no unrelated untracked files are staged.
- If a task changes inventory filters, compare before/after coverage and explain the denominator change.
- If a task changes translations, verify `script/zh_apply_localization.py --dry-run --summary` reports `would_change: 0` and `missing: 0`.

Do not start the next task until the current task passes its review gate.

## Completion Criteria

Round 4 is complete only when:

- The Round 4 plan is committed.
- Inventory review modes are implemented and documented.
- Conservative noise filters are applied with an exclusion ledger.
- Verified visible residues listed in this plan are translated through the manifest.
- README and localization docs are updated with Round 4 results.
- Full verification passes or any GUI limitation is explicitly recorded as a manual gate.
- Remote `main` in `Drew1811266/Warp-CN` matches the final local `HEAD` tree, using either normal `git push` or the documented GitHub API fallback.
