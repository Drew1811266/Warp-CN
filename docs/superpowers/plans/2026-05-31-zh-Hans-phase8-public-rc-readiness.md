# Warp CN Phase 8 Public-RC Evidence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move Warp CN from RC4 `ready-for-local-use` to a defensible RC5 public-RC decision by verifying `GUI-WS-06` custom endpoint deletion with an isolated real product state.

**Architecture:** This repository keeps phase execution plans in `docs/zh-Hans-localization-phase*.md`. The canonical Phase 8 plan is `docs/zh-Hans-localization-phase8.md`; this Superpowers plan file records the required handoff location and should be kept in sync with that canonical document.

**Tech Stack:** Rust/Warp client source, localization manifest tooling, macOS `WarpOss.app`, `WARP_DATA_PROFILE=zh-rc5`, Computer Use, screenshot artifacts, cargo test/check gates.

---

## Implementation Source

Execute the canonical plan in:

```text
docs/zh-Hans-localization-phase8.md
```

The plan contains these implementation tasks:

- P8-M0: Entry baseline and RC4 blocker snapshot.
- P8-M1: Upstream stable freshness recheck.
- P8-M2: Evidence path selection.
- P8-M3: Launch `zh-rc5` profile and complete safe login.
- P8-M4: Revalidate current-cycle base GUI in logged-in profile.
- P8-M5: Verify custom inference visibility and create disposable endpoint.
- P8-M6: Verify remove endpoint confirmation with cancel-then-confirm.
- P8-M7: RC5 gate and release decision.
- P8-M8: Post-decision cleanup and handoff.

## Execution Rule

Do not claim `ready-for-public-rc` from this wrapper file alone. The release decision must be made from the acceptance criteria and evidence paths in `docs/zh-Hans-localization-phase8.md`.
