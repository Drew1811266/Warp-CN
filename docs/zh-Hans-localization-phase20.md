# zh-Hans Localization Phase 20

Date: 2026-06-01

## Goal

Prepare safe public-RC execution for account, Billing, Cloud, destructive confirmation, and Agent lifecycle GUI gates.

## Changes

- Added `docs/zh-Hans-public-rc-gate-runbook.md`.
- Consolidated disposable profile names, object names, evidence labels, allowed actions, cleanup rules, and stop conditions.
- Kept fixture evidence separate from real-account evidence.
- Explicitly forbids using the user's main account, real billing quota, production cloud environments, real secrets, or real team ownership state.

## Rows Covered

- Auth: `GUI-AUTH-01`, `GUI-AUTH-02`, `GUI-AUTH-03`.
- Settings / AI: `GUI-SET-03`, `GUI-SET-04`, `GUI-SET-05`, `GUI-WS-06`.
- Destructive confirmations: `GUI-SET-06`, `GUI-WS-04`, `GUI-WS-07`.
- Billing / Cloud / Launch: `GUI-CLOUD-01`, `GUI-BILL-01`, `GUI-BILL-02`, `GUI-LAUNCH-01`.
- Agent lifecycle: `GUI-AGENT-01` through `GUI-AGENT-05`.

## Decision

Phase 20 is accepted as `qualified-runbook-only`.

Proceed to Phase 21: Terminal backlog classification pass 2.
