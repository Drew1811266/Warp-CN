# Warp CN Phase 9 Custom Inference Evidence Enablement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prepare the missing `GUI-WS-06` evidence path by adding a test-account runbook and a debug-only custom inference smoke fixture.

**Architecture:** The canonical Phase 9 plan lives in `docs/zh-Hans-localization-phase9.md`. This Superpowers handoff file points executors to that canonical plan and preserves the planning workflow's required location.

**Tech Stack:** Rust/Warp client source, `app/src/settings_view/ai_page.rs`, localization manifest tooling, macOS `WarpOss.app`, `WARP_DATA_PROFILE=zh-rc6`, optional `WARP_CN_CUSTOM_INFERENCE_SMOKE=1`, Computer Use, screenshot artifacts, cargo gates.

---

## Implementation Source

Execute the canonical plan in:

```text
docs/zh-Hans-localization-phase9.md
```

The plan contains these implementation tasks:

- P9-M0: Entry baseline and RC5 blocker snapshot.
- P9-M1: Isolated test account readiness runbook.
- P9-M2: Debug-only fixture design review.
- P9-M3: Implement debug-only custom inference smoke override.
- P9-M4: Fixture GUI smoke for custom endpoint flow.
- P9-M5: Real account public-RC path.
- P9-M6: RC6 gate and release decision.
- P9-M7: Cleanup and fixture safety audit.

## Execution Rule

Do not claim `ready-for-public-rc` from fixture evidence. Public-RC readiness requires the real-account path in `docs/zh-Hans-localization-phase9.md` to pass without `WARP_CN_CUSTOM_INFERENCE_SMOKE`.
