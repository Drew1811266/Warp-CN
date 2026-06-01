# zh-Hans Search Module Review - 2026-06-01

This is the first Phase 11 module review. It applies the Phase 10 checklist to the search, command palette, command search, slash command, and search-core surfaces without running heavy Rust build gates.

## Scope

Reviewed areas:

- `app/src/search/action`
- `app/src/search/ai_context_menu`
- `app/src/search/command_palette`
- `app/src/search/command_search`
- `app/src/search/external_secrets`
- `app/src/search/notebook_embedding`
- `app/src/search/search_bar.rs`
- `app/src/search/search_results_menu`
- `app/src/search/slash_command_menu`
- `app/src/search/welcome_palette`
- `crates/warp_search_core/src/data_source.rs`
- `crates/warp_search_core/src/mixer.rs`
- `crates/warp_search_core/src/searcher.rs`

Out of scope for this pass:

- Real GUI rerun.
- Full accessibility localization cleanup.
- Heavy Rust compile/test gates.
- Settings-wide schema description localization beyond the one search setting reviewed here.

## Baseline

Initial search preset state:

```text
preset: search
covered: 267
candidates: 26
coverage: 91.1%
```

Post-review search preset state:

```text
preset: search
covered: 269
candidates: 0
coverage: 100.0%
```

Dry-run after fixes:

```text
entries: 2664
files: 198
already_applied: 2649
would_change: 0
missing: 0
```

Validation run:

```text
manifest validation passed
glossary check passed
locale JSON/YAML export passed
Python localization tests: 18 passed
cargo fmt --check: passed
git diff --check: passed
```

## Fixes Made

| Area | Change | Severity | Reason |
| --- | --- | --- | --- |
| Command palette new session | Changed `"{direction}拆分窗格：{}"` to `"向{direction}拆分窗格：{}"` | `T2` | Avoids awkward labels such as `下拆分窗格` |
| Conversation search accessibility help | Changed `按 Enter 导航到对话 {}。` to `按 Enter 导航到对话“{}”。` | `T3` | Restores the title boundary that existed in the English source |
| Command search zero state | Translated `# find "foo" in files` to `# 在文件中查找 "foo"` | `T2/F3` | Keeps the `#` natural-language filter token while localizing the example query |
| Command search setting description | Translated `Whether to show global workflows in universal search results.` | `T2/F3` | User-facing setting/schema description; `toml_path` remains unchanged |
| Inventory ignore rules | Added reviewed ignore patterns for UI internal names, logs, test assertions, command tokens, filter keys, and preserved `Warp Drive` | `F2 process` | Removes non-UI candidates without hiding visible search labels |

## Candidate Classification

The original 26 candidates were classified as:

| Class | Examples | Decision |
| --- | --- | --- |
| Internal generated text/token | `<block:{}>`, `{truncated}...`, `none>`, `--porcelain` | Preserve and ignore |
| UI internal view names | `ExternalSecretsMenu`, `EmbeddingSearchMenu`, `SearchBar`, `WelcomePalette` | Preserve and ignore |
| Logs and diagnostics | `OpenProjectConvo action unexpectedly handled...`, `Failed to execute search`, `Ignoring duplicate results...` | Preserve and ignore |
| Test assertions and fixtures | `duplicate slash command name`, `/orchestrate deploy services`, `just a normal query`, `/planning something` | Preserve and ignore |
| Search parser/filter keys | `workflows.show_global_workflows_in_universal_search` | Preserve and ignore |
| Preserved product term | `Warp Drive` | Preserve |
| User-facing example/settings copy | `# find "foo" in files`, search setting description | Translated |

## Functional Safety Review

Passed:

- Slash command names remain English command tokens, for example `/agent`, `/open-file`, `/set-tab-color`, `/orchestrate`.
- Search filter atoms remain parser-safe: `history:`, `workflows:`, `files:`, `commands:`, `slash:`, `#`, and aliases are not translated.
- TOML setting key `workflows.show_global_workflows_in_universal_search` remains unchanged.
- Git command argument `--porcelain` remains unchanged.
- Dynamic placeholders are preserved in edited strings.
- `dry-run` reports `missing: 0`, so the manifest still matches the current source overlay.

No `F0` or `F1` functional blocker was found in this pass.

## Translation Quality Review

Accepted:

- Core search labels: `命令搜索`, `搜索命令`, `未找到结果`, `搜索历史记录`, `搜索工作流`, `搜索文件`, `搜索命令`.
- Command palette categories: `文件`, `操作`, `会话`, `启动配置`, `标签页`, `对话`.
- Slash command descriptions keep product names and command concepts stable: `Agent`, `MCP`, `GitHub`, `Oz`, `Markdown`, `TOML`.
- AI/search quota messages are understandable and do not change billing semantics.

Fixed:

- Directional split-pane label naturalness.
- Conversation title punctuation in accessibility help.
- Natural-language search example localization.
- Search setting description localization.

## Remaining Issues

| ID | Severity | Issue | Impact | Follow-up |
| --- | --- | --- | --- | --- |
| P11-SEARCH-A11Y-01 | `T2/F2` | Several `accessibility_label()` prefixes in search still use English, such as `Conversation:`, `Block:`, `Workflow:`, `Notebook:`, `File:`, `Directory:`, `Project:`, `Repo:`, `Secret:`, and `Section:` | Does not break parsing or visible UI, but screen-reader output remains partially English | Create a dedicated accessibility-label localization slice and update related Rust tests that assert English prefixes |
| P11-SEARCH-GUI-01 | `evidence` | This pass did not rerun GUI | Source and inventory evidence are current, but current-cycle visual proof is unchanged | Reuse command palette GUI smoke in the next release-candidate gate |

## Decision

Search module review status: `reviewed-low-load`.

The search preset has zero remaining inventory candidates after reviewed translations and ignore rules. No functional blocker was found. The remaining risk is accessibility-label English residue, which should be handled as a focused follow-up rather than mixed into parser/search-token work.
