# zh-Hans Translation Audit - 0.18

This document is the current-cycle execution ledger for reviewing Warp CN `0.18`
localization quality and functional safety. It complements
`docs/zh-Hans-full-translation-audit.md`, which contains older phase records.

## Baseline

Date: 2026-06-03

Branch:

```text
codex/zh-Hans-post-rc26-execution
```

Version:

```text
0.18
```

Current manifest state:

```text
entries: 7943
files: 552
already_applied: 5690
would_change: 0
missing: 0
```

Current public-RC blocker state:

```text
total: 11
blocked-no-backend-fixture: 5
blocked-no-disposable-object: 3
blocked-no-isolated-account: 3
```

Low-load gates run in this cycle:

| Gate | Result |
| --- | --- |
| `python3 script/zh_apply_localization.py --validate-manifest` | `manifest validation passed` |
| `python3 script/zh_apply_localization.py --check-glossary` | `glossary check passed` |
| `python3 script/zh_apply_localization.py --dry-run --summary` | `would_change: 0`, `missing: 0` |
| `python3 script/zh_public_rc_status.py` | 11 blockers remain |
| `python3 script/zh_apply_localization.py --metadata-summary` | `context: 100.0%`, `status: 100.0%`, `notes: 0.0%` |
| `python3 script/zh_localization_inventory.py --preset onboarding --coverage` | `323 / 0 / 100.0%` |
| `python3 script/zh_localization_inventory.py --preset workspace --coverage` | `865 / 0 / 100.0%` |
| `python3 script/zh_localization_inventory.py --preset search --coverage` | `269 / 0 / 100.0%` |
| `python3 script/zh_localization_inventory.py --preset settings --coverage` | `2024 / 0 / 100.0%` |
| `python3 script/zh_localization_inventory.py --preset modals --coverage` | `5240 / 2 / 100.0%` |
| `python3 script/zh_localization_inventory.py --preset release --coverage` | `8574 / 2 / 100.0%` |
| `python3 script/zh_export_locale.py --format json` and `python3 -m json.tool` | passed |
| `python3 script/zh_export_locale.py --format yaml` | passed |
| `python3 -m py_compile ...` for localization/public-RC/privacy/full-audit scripts | passed |
| `python3 script/zh_full_translation_audit.py --fail-on-actionable` | 7,943 entries, 0 actionable rows |
| `python3 -m json.tool docs/zh-Hans-full-translation-audit-0.18/entries.json` | passed |
| `python3 -m unittest ...` for localization/public-RC tests | 63 tests passed |
| `python3 script/zh_public_rc_evidence_report.py --json` | `decision: blocked`, 11 missing rows |
| `python3 script/zh_public_rc_evidence_queue.py --json` | `decision: blocked-until-queue-cleared` |
| `python3 script/zh_public_rc_evidence_lint.py --strict-artifacts` | expected failure: 11 missing evidence rows |
| `cargo fmt --check` | passed |
| `python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25` | `decision: defer-heavy-gate` |

## Review Method

Each entry is reviewed against:

- Source context: nearby Rust code proves whether the string is user-visible.
- Meaning: the target keeps the original product intent.
- Tone: the target is concise and suitable for a terminal/productivity app.
- Glossary: protected terms such as `Warp`, `Warp Drive`, `Agent`, `MCP`,
  `GitHub`, `AWS Bedrock`, `Codex`, `Claude Code`, and `Gemini` remain stable.
- Placeholder safety: `{}`, named placeholders, markdown, URLs, shortcuts,
  command tokens, and dynamic values are preserved where required.
- Functional risk: parsed commands, storage keys, telemetry, provider IDs,
  model IDs, URLs, config fields, tests, fixtures, and logs are not translated
  as passive UI copy.
- GUI risk: destructive, auth, billing, cloud, team, endpoint, and secret rows
  require current-cycle GUI evidence before public-RC promotion.

Review statuses:

| Status | Meaning |
| --- | --- |
| `accepted-source` | Source-level translation and functional review passed |
| `accepted-with-note` | Source-level review passed, but GUI or product-state evidence is still needed |
| `needs-copy-fix` | Chinese wording should be changed before promotion |
| `needs-functional-review` | Translation may affect behavior, parsing, or stored state |
| `blocked-public-rc` | Correctness cannot be promoted without account, fixture, or disposable object evidence |

## High-Risk Heuristic Snapshot

This is a heuristic grouping from the manifest and source/target/context text.
Counts are for prioritization, not final risk classification.

| Risk bucket | Candidate entries | Highest-density areas |
| --- | ---: | --- |
| Destructive actions | 424 | workspace, teams, features, MCP destructive dialog, Agent actions |
| Billing / quota / team | 729 | teams, billing and usage, Build plan migration, AI settings |
| Auth / security | 685 | features, privacy, auth views, secret/API key surfaces |
| AI / provider / Agent | 2691 | Agent views, AI settings, driver output, provider/model flows |
| Command / protocol / terminal | 1764 | terminal view, terminal input, workspace view, slash commands |

## Batch A01 - Public-RC High-Risk Source Review

Scope:

- `app/src/auth`
- `app/src/settings_view/ai_page.rs`
- `app/src/settings_view/custom_inference_modal.rs`
- `app/src/settings_view/delete_environment_confirmation_dialog.rs`
- `app/src/settings_view/transfer_ownership_confirmation_modal.rs`
- `app/src/settings_view/teams_page.rs`
- `app/src/settings_view/billing_and_usage*`

Out of scope:

- GUI launch.
- Login with a real account.
- Backend fixture creation.
- Billing, cloud, team, secret, endpoint, or environment mutation.
- Deleting any real object.

### A01 Results

| Row | Manifest line | Source path | Source | Target | Decision | Notes |
| --- | ---: | --- | --- | --- | --- | --- |
| A01-001 | 525 | `app/src/auth/login_slide.rs` | `Auth Token` | `认证令牌` | `accepted-source` | Auth terminology is clear; token value remains data, not translated. |
| A01-002 | 609 | `app/src/auth/login_slide.rs` | `Disable Warp Drive` | `禁用 Warp Drive` | `accepted-with-note` | High-risk opt-out action; wording is clear, but needs GUI evidence for button order and surrounding consequences. |
| A01-003 | 619 | `app/src/auth/login_slide.rs` | `Disable AI features` | `禁用 AI 功能` | `accepted-with-note` | Clear feature opt-out copy; needs GUI evidence in the login skip path. |
| A01-004 | 1487 | `app/src/auth/auth_override_warning_body.rs` | Anonymous session objects and preferences will be permanently deleted | 匿名会话中的个人 Warp Drive 对象和偏好设置将被永久删除 | `accepted-with-note` | Strong destructive warning is preserved; public-RC path still needs isolated-account evidence. |
| A01-005 | 1505 | `app/src/auth/auth_override_warning_body.rs` | `Delete personal Warp Drive objects and preferences?` | `删除个人 Warp Drive 对象和偏好设置？` | `accepted-with-note` | Destructive title is explicit; blocked from public-RC promotion without isolated login state. |
| A01-006 | 1460 | `app/src/auth/paste_auth_token_modal.rs` | `Enter auth token` | `输入认证令牌` | `accepted-source` | Safe UI label; auth token contents are not localized. |
| A01-007 | 9039 | `app/src/settings_view/ai_page.rs` | `Add custom endpoint` | `添加自定义端点` | `accepted-with-note` | Endpoint term follows glossary; GUI remains blocked by isolated custom-inference account state. |
| A01-008 | 9067 | `app/src/settings_view/ai_page.rs` | `Edit custom endpoint` | `编辑自定义端点` | `accepted-with-note` | Clear action label; requires product-state evidence. |
| A01-009 | 9088 | `app/src/settings_view/ai_page.rs` | `Endpoint removed` | `端点已移除` | `accepted-with-note` | Completion toast is clear; public-RC evidence must use only `zh-smoke-delete-endpoint`. |
| A01-010 | 44520 | `app/src/settings_view/custom_inference_modal.rs` | `Please include 'https://'` | `请包含 https://` | `accepted-source` | URL token remains visible; quote style is not behaviorally significant in the placeholder text. |
| A01-011 | 11188 | `app/src/settings_view/environments_page.rs` | `Search environments...` | `搜索环境...` | `accepted-source` | Passive search placeholder; no parser or storage risk found. |
| A01-012 | 11209 | `app/src/settings_view/environments_page.rs` | `Environment deleted successfully` | `环境已成功删除` | `accepted-with-note` | Destructive completion copy is clear; real verification requires disposable environment cleanup proof. |
| A01-013 | source | `app/src/settings_view/delete_environment_confirmation_dialog.rs` | `Delete environment?` | `删除环境？` | `accepted-with-note` | Title and primary button are explicit; GUI evidence requires `zh-smoke-delete-environment`. |
| A01-014 | source | `app/src/settings_view/delete_environment_confirmation_dialog.rs` | `Are you sure you want to remove the {} environment?` | `确定要删除 {} 环境吗？` | `accepted-source` | Body now aligns with title/button wording for a destructive delete confirmation. |
| A01-015 | 17924 | `app/src/settings_view/transfer_ownership_confirmation_modal.rs` | Transfer team ownership to `{}` | `将团队所有权转让给 {}` | `accepted-with-note` | Placeholder is preserved and consequence is explicit; blocked from public-RC promotion without disposable owner test team and approval. |
| A01-016 | 17931 | `app/src/settings_view/transfer_ownership_confirmation_modal.rs` | `Cancel` | `取消` | `accepted-source` | Safe cancel action. |
| A01-017 | 17938 | `app/src/settings_view/transfer_ownership_confirmation_modal.rs` | `Transfer` | `转让` | `accepted-with-note` | Accurate but high-risk; GUI must prove button placement and no accidental owner mutation. |
| A01-018 | 18310 | `app/src/settings_view/teams_page.rs` | `Delete team` | `删除团队` | `accepted-with-note` | Clear destructive label; public-RC evidence requires disposable team. |
| A01-019 | 18301 | `app/src/settings_view/teams_page.rs` | `Leave team` | `离开团队` | `accepted-with-note` | Clear action label; still needs team-state GUI evidence. |
| A01-020 | 12119 | `app/src/settings_view/billing_and_usage/billing_cycle_usage_common.rs` | `Pay-as-you-go` | `按量付费` | `accepted-with-note` | Billing meaning is accurate; public-RC evidence requires safe billing fixture. |
| A01-021 | 12189 | `app/src/settings_view/billing_and_usage/billing_cycle_usage_common.rs` | `Total usage` | `总使用量` | `accepted-source` | Passive billing metric label; no functional risk found. |
| A01-022 | 8941 | `app/src/settings_view/ai_page.rs` | `Warp credit fallback` | `Warp 额度兜底` | `accepted-with-note` | Meaning is acceptable for a fallback toggle, but GUI evidence should confirm surrounding help text makes the behavior clear. |
| A01-023 | 9179 | `app/src/settings_view/ai_page.rs` | `Restricted due to billing issue` | `因账单问题受限` | `accepted-with-note` | Billing restriction is accurately communicated; needs account/backend state evidence before public-RC promotion. |

### A01 Findings

| ID | Severity | Finding | Required action |
| --- | --- | --- | --- |
| A01-F01 | `T2/F2` | `DeleteEnvironmentConfirmationDialog` previously mixed `删除` in title/button with `移除` in body. This was not a crash risk, but it was a destructive-action clarity risk. | Fixed in this cycle by changing the body to `确定要删除 {} 环境吗？`; low-load gates must remain clean. |
| A01-F02 | `evidence` | All public-RC blocker rows remain blocked from promotion because this batch did not use isolated accounts, backend fixtures, or disposable objects. | Keep rows as source-reviewed only until current-cycle GUI evidence exists. |

Decision:

```text
Batch A01 source review: passed after one copy fix
Functional blocker: none found
Public-RC promotion: blocked
```

## Machine Token Preservation Scan

The current-cycle token preservation scan compared source and target strings
for named or empty brace placeholders, environment variables, long flags,
slash commands, angle-bracket hint tokens, URLs, and backtick code spans.

Result:

```text
heuristic warnings: 17
functional blockers: 0
```

Classification:

| Class | Count | Decision |
| --- | ---: | --- |
| Price units such as `/month`, `/year`, `/mo` localized to `/月`, `/年`, `/月起` | 5 | `accepted-source`; these are display price units, not slash commands |
| Slash-command argument hints such as `<tab name>` localized to Chinese hint text | 11 | `accepted-source`; command names remain English and tests assert the localized hint text |
| SDK cancelled sentinel `<cancelled>` localized to `<已取消>` | 1 | `accepted-source`; this is user-facing formatted output, not a parser token in this path |

Preserved command/protocol tokens observed:

- Static slash command names remain English, for example `/agent`,
  `/cloud-agent`, `/create-environment`, `/rename-tab`, `/set-tab-color`,
  `/compact`, `/queue`, and `/export-to-file`.
- Shell/config examples with flags such as `--force`, `--template`, and
  `--no-config` remain in code contexts where they are executable.
- URL tokens such as `https://` and `https://github.com/owner/repo` remain
  visible.

## Batch A02 - AI Provider, BYOK, Custom Endpoint

Scope:

- `app/src/settings_view/ai_page.rs`
- `app/src/settings_view/custom_inference_modal.rs`
- provider key editors
- AWS Bedrock settings
- custom endpoint add/edit/remove copy

Reviewed rows:

| Row | Source path | Surface | Decision | Notes |
| --- | --- | --- | --- | --- |
| A02-001 | `app/src/settings_view/ai_page.rs` | `OpenAI API 密钥`, `Anthropic API 密钥`, `Google API 密钥` | `accepted-source` | Provider names and `API` term are preserved; only user-facing label text is localized. |
| A02-002 | `app/src/settings_view/ai_page.rs` | BYOK explanatory text | `accepted-with-note` | Copy clearly states keys are stored locally and Warp credits are used when no key exists; needs account-state GUI evidence. |
| A02-003 | `app/src/settings_view/ai_page.rs` | `Warp 额度兜底` toggle | `accepted-with-note` | Meaning is acceptable, but GUI should verify the adjacent helper text makes fallback behavior clear. |
| A02-004 | `app/src/settings_view/custom_inference_modal.rs` | endpoint name / URL / API key / model labels | `accepted-source` | Field labels are user-visible and preserve URL/API/model meaning. |
| A02-005 | `app/src/settings_view/custom_inference_modal.rs` | `请包含 https://` | `accepted-source` | URL token remains visible; no parser or formatting risk. |
| A02-006 | `app/src/settings_view/ai_page.rs` | AWS Bedrock credentials and auto-login copy | `accepted-with-note` | AWS Bedrock product term is preserved; public-RC evidence still requires safe fixture, never real AWS credentials. |

Decision:

```text
Batch A02 source review: passed
Functional blocker: none found
Public-RC promotion: blocked by GUI-SET-03, GUI-SET-04, GUI-SET-05, GUI-WS-06
```

## Batch A03 - Billing, Credits, Quota, Capacity

Scope:

- `app/src/settings_view/billing_and_usage*`
- `app/src/workspace/view/free_tier_limit_hit_modal.rs`
- `app/src/workspace/view/cloud_agent_capacity_modal/mod.rs`
- Build/Business plan upgrade copy

Reviewed rows:

| Row | Source path | Surface | Decision | Notes |
| --- | --- | --- | --- | --- |
| A03-001 | `app/src/settings_view/billing_and_usage/billing_cycle_usage_common.rs` | `按量付费`, `总使用量`, `附加包`, `仅云端`, `合计` | `accepted-source` | Passive billing metric labels; no parser or storage risk. |
| A03-002 | `app/src/settings_view/billing_and_usage_page.rs` | add-on credit and overage descriptions | `accepted-with-note` | Cost semantics are clear enough for source review; real promotion requires safe billing fixture. |
| A03-003 | `app/src/workspace/view/free_tier_limit_hit_modal.rs` | Build plan price and credit list | `accepted-with-note` | `${price}` placeholder is preserved; `/month` localized to `/月` as display copy. |
| A03-004 | `app/src/workspace/view/cloud_agent_capacity_modal/mod.rs` | out-of-credits / cloud concurrency upgrade copy | `accepted-with-note` | Quota and upgrade intent are clear; public-RC proof requires backend capacity or quota fixture. |
| A03-005 | `app/src/settings_view/teams_page.rs` | additional member monthly/yearly billing copy | `accepted-with-note` | `${monthly_cost:.0}`, `${yearly_cost:.0}`, and `{prorated_message}` are preserved; `/month` and `/year` localize to `/月` and `/年`. |

Decision:

```text
Batch A03 source review: passed
Functional blocker: none found
Public-RC promotion: blocked by GUI-BILL-01, GUI-BILL-02, GUI-CLOUD-01
```

## Batch A04 - Teams, Ownership, Destructive Member Actions

Scope:

- `app/src/settings_view/teams_page.rs`
- `app/src/settings_view/transfer_ownership_confirmation_modal.rs`

Reviewed rows:

| Row | Source path | Surface | Decision | Notes |
| --- | --- | --- | --- | --- |
| A04-001 | `app/src/settings_view/transfer_ownership_confirmation_modal.rs` | transfer ownership body | `accepted-with-note` | Target explicitly states the user will no longer be owner and cannot perform admin operations. |
| A04-002 | `app/src/settings_view/transfer_ownership_confirmation_modal.rs` | `取消` / `转让` buttons | `accepted-with-note` | Correct labels; GUI must prove placement and avoid accidental confirmation. |
| A04-003 | `app/src/settings_view/teams_page.rs` | `删除团队`, `离开团队`, `从团队中移除` | `accepted-with-note` | Destructive labels are clear; public-RC evidence requires disposable team/member state. |
| A04-004 | `app/src/settings_view/teams_page.rs` | invite and role-management copy | `accepted-with-note` | Admin/member wording is understandable; account/team state remains required. |
| A04-005 | `app/src/settings_view/teams_page.rs` | seat cap and payment restriction warnings | `accepted-with-note` | Cost/access impact is clear; billing/team fixture evidence still required. |

Decision:

```text
Batch A04 source review: passed
Functional blocker: none found
Public-RC promotion: blocked by GUI-WS-07 and billing/team fixture rows
```

## Batch A05 - Terminal, Slash Commands, Command Tokens

Scope:

- `app/src/search/slash_command_menu/static_commands/commands.rs`
- terminal command/help examples touched by token scan
- AI SDK formatted driver output

Reviewed rows:

| Row | Source path | Surface | Decision | Notes |
| --- | --- | --- | --- | --- |
| A05-001 | `app/src/search/slash_command_menu/static_commands/commands.rs` | static slash command names | `accepted-source` | Command names remain English parser tokens. |
| A05-002 | `app/src/search/slash_command_menu/static_commands/commands.rs` | localized argument hints | `accepted-source` | Hints are UI guidance, not parser grammar; Rust tests assert localized hint text. |
| A05-003 | `app/src/terminal/view/init_environment/mod.rs` | `/create-environment <filepath> <GitHub URL>` example | `accepted-source` | Executable slash command and angle placeholders are preserved in the help text. |
| A05-004 | `app/src/ai/agent_sdk/driver/output.rs` | `<已取消>` cancelled message | `accepted-source` | User-facing formatted output; no evidence this is parsed as a protocol token in this path. |
| A05-005 | terminal shell/config examples | flags such as `--force`, `--template`, `--no-config` | `accepted-source` | Executable flags remain English in source contexts reviewed by scanner. |

Decision:

```text
Batch A05 source review: passed
Functional blocker: none found
Targeted Rust tests still required before completion
```

Targeted Rust execution note:

The required Rust/build follow-up was not executed in this cycle because the
heat-safety gate returned `defer-heavy-gate`.

Observed load gate output:

```text
probe 1: load=3.45 3.34 3.28
probe 1: hot_process=WindowServer 41.1%
probe 2: load=2.70 3.12 3.20
probe 2: hot_process=WindowServer 42.1%
decision: defer-heavy-gate
```

## Batch A06 - GUI Non-Destructive Smoke

Status:

```text
not-run-current-cycle
```

Reason:

The current-cycle low-load gate returned `defer-heavy-gate`, so this cycle did
not rebuild a fresh bundle or launch the GUI. Launching an older bundle would
not prove the current source overlay, including the deletion-confirmation copy
fix, so it is intentionally not counted as evidence.

Required next safe execution when the machine is cool enough:

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
open -n target/debug/bundle/osx/WarpOss.app
```

Minimum non-destructive GUI anchors to verify:

- Welcome/onboarding labels.
- Main menu labels: file/edit/view/tabs/blocks/AI/Drive/window/help.
- Command palette and command search entry points.
- Settings shell, Appearance, AI settings entry, billing entry, teams entry.
- Delete environment confirmation only with a disposable environment; otherwise
  leave this as source-reviewed only.

## Batch A07 - Public-RC Blocker Rows

Status:

```text
blocked-current-cycle
```

Evidence tools passed mechanically, but strict artifact lint correctly failed:

```text
total_required: 11
ready_rows: 0
errors: 11
decision: fail
```

Blocked rows:

| Row | Blocker |
| --- | --- |
| `GUI-AUTH-01` | isolated browser-login test account |
| `GUI-SET-03` | isolated account with AI settings/custom inference state |
| `GUI-SET-04` | disposable AWS or Bedrock fixture |
| `GUI-SET-05` | safe invalid Bedrock credential fixture |
| `GUI-SET-06` | disposable environment named `zh-smoke-delete-environment` |
| `GUI-WS-04` | disposable managed auth secret named `zh-smoke-delete-secret` |
| `GUI-WS-06` | isolated custom-inference account and `zh-smoke-delete-endpoint` |
| `GUI-WS-07` | disposable owner test team named `zh-smoke-public-rc-team` |
| `GUI-BILL-01` | safe billing/quota fixture |
| `GUI-BILL-02` | backend build-plan migration test team state |
| `GUI-CLOUD-01` | controlled cloud capacity/quota fixture |

No public-RC blocker was promoted in this cycle.

## Batch A08 - Full Per-Entry Simulated Review

Status:

```text
passed-after-fixes
```

Command:

```bash
python3 script/zh_full_translation_audit.py
```

Artifacts:

| Artifact | Purpose |
| --- | --- |
| `docs/zh-Hans-full-translation-audit-0.18/entries.tsv` | One row per `[[replace]]` entry for spreadsheet-style review |
| `docs/zh-Hans-full-translation-audit-0.18/entries.json` | Same rows in machine-readable form |
| `docs/zh-Hans-full-translation-audit-0.18/summary.md` | Aggregate counters and actionable-row summary |

Final simulated-review result:

| Metric | Count |
| --- | ---: |
| Manifest entries reviewed | 7,943 |
| `simulated-accepted` | 1,774 |
| `simulated-accepted-with-note` | 5,139 |
| `blocked-public-rc` | 1,030 |
| `needs-copy-review` | 0 |
| `needs-functional-review` | 0 |

Findings resolved during the full pass:

| Area | Finding | Resolution |
| --- | --- | --- |
| Environment delete dialog | Body text used `移除` while title/action used `删除` | Changed to `确定要删除 {} 环境吗？` in source and manifest |
| Suggestion prompt tooltip | Upstream tooltip used `Suggested prompt:\n{prompt}`, but zh-Hans target had collapsed the newline | Restored the escaped newline in source and updated the manifest to the parser-compatible representation |

Notes:

- This batch is a Codex simulated per-entry review. It gives every manifest row
  a deterministic audit decision and token/copy/risk classification; it is not
  external human sign-off.
- The `blocked-public-rc` rows are not current source copy bugs. They are rows
  whose final public-RC promotion still depends on isolated-account, backend
  fixture, or disposable-object GUI evidence.

## Current-Cycle Decision

```text
localization low-load gates: passed
source-level high-risk audit A01-A05: passed after one copy fix
full per-entry simulated audit A08: passed after one tooltip behavior fix
functional blockers found: 0
copy/behavior fixes made: 2
heavy Rust/build gate: deferred by low-load gate
GUI current-cycle evidence: not run
public-RC status: blocked by 11 missing evidence rows
```

## Next Batches

| Batch | Scope | Purpose | Gate |
| --- | --- | --- | --- |
| A06 | GUI non-destructive smoke rows | Prove base local-use GUI anchors in current cycle | Build bundle and collect accessibility anchors |
| A07 | Public-RC blocker rows | Promote only rows with isolated account, backend fixture, or disposable object proof | Strict evidence lint |

## Required Gate After Copy Fixes

After any manifest/source change from this audit, run:

```bash
python3 script/privacy_guard.py --all-tracked
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_public_rc_status.py
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py script/test_zh_low_load_gate.py
git diff --check
```

For release-candidate escalation, also run:

```bash
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```
