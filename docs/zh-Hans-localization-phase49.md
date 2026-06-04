# zh-Hans Localization Phase 49

Date: 2026-06-02

## Goal

Establish the post-RC11 execution queue for RC12 while preserving the low-load policy.

## Baseline

RC11 decision: `ready-for-local-use-with-fixture-evidence`.

Public RC remains blocked by missing isolated account/backend evidence and deferred onboarding visual residue.

```text
manifest entries: 7088
dry-run: would_change 0, missing 0
release coverage: 7757 covered / 1191 candidates = 86.7%
terminal coverage: 1653 covered / 718 candidates = 69.7%
AI / Agent coverage: 2223 covered / 469 candidates = 82.6%
```

## Queue

The post-RC11 queue is recorded in `.omx/plans/2026-06-02-zh-Hans-post-rc11-plan.md`.

Planned phases:

| Phase | Focus | Decision |
| --- | --- | --- |
| 50 | Terminal visible UI residue | Translate high-confidence UI; preserve URL/shell/protocol strings. |
| 51 | Terminal executor/bootstrap residue | Mostly classify/preserve command, path, env var, WSL/MSYS/bootstrap contracts. |
| 52 | AI/Agent residue | Translate visible errors/labels; preserve prompt/tool/MCP/provider/file contracts. |
| 53 | Visual/public-RC blocker refresh | Reconfirm image residue and external-state blockers without touching real state. |
| 54 | RC12 review/freeze/gate | Re-run full command-line gate and publish RC12 decision. |

## Top-Path Evidence

Release/modals top paths after RC11:

```text
13 app/src/terminal/view/link_detection.rs
12 app/src/terminal/bootstrap.rs
12 app/src/terminal/view/block_onboarding/onboarding_prompt_block.rs
11 app/src/terminal/model/session/command_executor/remote_command_executor.rs
11 app/src/terminal/model/session/command_executor/wsl_command_executor.rs
11 app/src/terminal/shared_session/viewer/terminal_manager.rs
11 app/src/terminal/view/ambient_agent/auth_secret_selector.rs
11 app/src/terminal/view/ambient_agent/loading_screen.rs
10 app/src/terminal/model/session/command_executor/local_command_executor.rs
10 app/src/terminal/view/ambient_agent/auth_secret_ftux_dropdown.rs
10 app/src/terminal/view/init_project/mod.rs
10 app/src/terminal/view/shell_terminated_banner.rs
10 app/src/terminal/warpify/settings.rs
```

AI/Agent top paths after RC11:

```text
9 app/src/ai/blocklist/local_agent_task_sync_model.rs
9 app/src/ai/skills/skill_manager.rs
8 app/src/ai/agent_sdk/driver/harness/mod.rs
8 app/src/ai/blocklist/action_model/execute/get_files.rs
8 app/src/ai/execution_profiles/profiles.rs
8 app/src/ai/facts/view/rule_editor.rs
8 app/src/ai/mcp/parsing.rs
8 app/src/ai/outline/native.rs
7 app/src/ai/agent_sdk/driver/cloud_provider/aws.rs
7 app/src/ai/agent_sdk/driver/terminal.rs
7 app/src/ai/ambient_agents/scheduled.rs
7 app/src/ai/aws_credentials.rs
7 app/src/ai/blocklist/inline_action/web_fetch.rs
7 app/src/ai/blocklist/inline_action/web_search.rs
```

## Validation

Passed:

```text
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
git diff --check
```

## Qualification

Phase 49 is accepted as `qualified-post-rc11-queue-and-plan`.
