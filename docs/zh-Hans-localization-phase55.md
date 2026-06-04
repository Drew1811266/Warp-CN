# zh-Hans Localization Phase 55

Date: 2026-06-02 Asia/Shanghai

## Goal

Establish the RC13 execution queue from the current post-RC12 candidate inventory and classify the next residue before changing source files.

## Baseline

RC12 remains the active baseline:

```text
manifest entries: 7372
dry-run: would_change 0, missing 0
release coverage: 8070 covered / 883 candidates = 90.1%
terminal coverage: 1850 covered / 524 candidates = 77.9%
AI / Agent coverage: 2339 covered / 355 candidates = 86.8%
```

## Inventory

Commands were run serially with `nice -n 10`:

```text
python3 script/zh_localization_inventory.py --preset release --status candidate --top-paths 25
python3 script/zh_localization_inventory.py --preset modals --status candidate --top-paths 25
python3 script/zh_localization_inventory.py app/src/terminal --status candidate --top-paths 30
python3 script/zh_localization_inventory.py app/src/ai --status candidate --top-paths 30
```

Release and modals top paths match. The leading residue is now mostly terminal block/view and AI blocklist/action surfaces:

| Candidates | Path | Classification | Next phase |
| ---: | --- | --- | --- |
| 9 | `app/src/terminal/block_filter.rs` | visible terminal filtering UI plus internal query/filter contracts | Phase 56 |
| 9 | `app/src/terminal/block_list_element.rs` | visible block list labels plus block identity/runtime metadata | Phase 56 |
| 9 | `app/src/terminal/cli_agent_sessions/listener/mod.rs` | CLI agent visible status plus plugin/session protocol/log strings | Phase 57 |
| 9 | `app/src/terminal/view/ambient_agent/model.rs` | ambient-agent visible model/status copy plus model contracts | Phase 57 |
| 9 | `app/src/terminal/view/pane_impl.rs` | visible pane labels/errors plus terminal runtime contracts | Phase 56 |
| 9 | `app/src/terminal/view.rs` | visible terminal view labels/errors plus view IDs/log strings | Phase 56 |
| 8 | `app/src/terminal/cli_agent_sessions/plugin_manager/mod.rs` | CLI plugin visible status plus plugin protocol IDs | Phase 57 |
| 8 | `app/src/terminal/input/models/model_spec_scores.rs` | visible model score labels plus model identifiers | Phase 56 |
| 8 | `app/src/terminal/view/ambient_agent/block/entry.rs` | visible ambient-agent block copy plus transcript/protocol values | Phase 57 |
| 8 | `app/src/terminal/view/docker_sandbox/mod.rs` | visible docker sandbox copy plus docker command contracts | Phase 57 |
| 8 | `app/src/terminal/view/inline_banner/open_in_warp.rs` | visible inline banner copy plus URL/app-open contracts | Phase 57 |
| 8 | `app/src/terminal/view/inline_banner/prompt_suggestions.rs` | visible prompt suggestion copy plus prompt examples | Phase 57 |
| 8 | `app/src/terminal/view/zero_state_block.rs` | visible zero-state copy plus terminal state guards | Phase 57 |
| 7 | `app/src/terminal/input/inline_history/view.rs` | visible inline history labels plus history/key contracts | Phase 56 |
| 7 | `app/src/terminal/model/block.rs` | visible block metadata plus block model/log values | Phase 56 |
| 7 | `app/src/terminal/safe_mode_settings.rs` | visible safe-mode settings copy plus config keys | Phase 56 |
| 7 | `app/src/terminal/ssh/warpify.rs` | visible SSH/Warpify copy plus shell/remote contracts | Phase 57 |
| 7 | `app/src/terminal/view/agent_view.rs` | visible agent view copy plus internal state/log labels | Phase 57 |
| 7 | `app/src/terminal/view/ambient_agent/first_time_setup.rs` | visible setup copy plus feature/state identifiers | Phase 57 |
| 7 | `app/src/terminal/view/ssh_remote_server_choice_view.rs` | visible SSH choice UI plus remote-server identifiers | Phase 57 |
| 7 | `app/src/terminal/view/use_agent_footer/warpify_footer.rs` | visible footer copy plus Warpify runtime contracts | Phase 57 |
| 7 | `app/src/ai/blocklist/action_model/execute/file_glob.rs` | rendered AI action copy plus glob/file contracts | Phase 58 |
| 7 | `app/src/ai/blocklist/block/view_impl.rs` | visible block rendering copy plus transcript/model state | Phase 58 |
| 7 | `app/src/ai/blocklist/codebase_index_speedbump_banner.rs` | visible speedbump banner copy plus indexing state | Phase 58 |
| 7 | `app/src/ai/blocklist/inline_action/malformed_line_heuristics.rs` | visible malformed-line explanations plus parser heuristics | Phase 58 |
| 6 | `app/src/ai/ai_document_view.rs` | visible AI document labels plus document model contracts | Phase 59 |
| 6 | `app/src/ai/blocklist/action_model/execute/edit_documents.rs` | rendered AI action copy plus edit/document contracts | Phase 58 |
| 6 | `app/src/ai/blocklist/code_block.rs` | visible code block copy plus syntax/file contracts | Phase 59 |
| 6 | `app/src/ai/blocklist/inline_action/aws_bedrock_credentials_error.rs` | visible provider credential errors plus AWS identifiers | Phase 59 |
| 6 | `app/src/ai/blocklist/telemetry_banner.rs` | visible telemetry banner copy plus event/diagnostic names | Phase 59 |
| 6 | `app/src/ai/blocklist/view_util.rs` | visible shared block UI copy plus helper contracts | Phase 59 |
| 6 | `app/src/ai/harness_display.rs` | rendered harness display copy plus transcript protocol | Phase 59 |
| 6 | `app/src/ai/persisted_workspace.rs` | visible persisted workspace copy plus persistence keys | Phase 59 |

## Execution Queue

The post-RC12 plan remains valid:

1. Phase 56: terminal block/view core backlog pass.
2. Phase 57: terminal CLI/ambient/zero-state backlog pass.
3. Phase 58: AI blocklist action execution backlog pass.
4. Phase 59: AI document/artifact/harness backlog pass.
5. Phase 60: manifest metadata, glossary, and locale export maintenance.
6. Phase 61: visual asset and public-RC evidence preflight.
7. Phase 62: RC13 language review, freeze, and final gate.

## Low-Load Review

No source files were changed in this phase. The phase used serial inventories and did not launch GUI, run Rust compilation, or touch account/backend/destructive state.

Passed:

```text
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --check-glossary
git diff --check .omx/plans/2026-06-02-zh-Hans-post-rc12-plan.md
```

## Qualification

Phase 55 is accepted as `qualified-post-rc12-queue-and-plan`.

The phase is qualified because the RC12 top-path inventory was refreshed, Phase 56-62 scopes were confirmed, no source changes were made, manifest validation and glossary checks passed, and the next execution queue separates visible UI from protocol, prompt, parser, shell, and external-state risks.
