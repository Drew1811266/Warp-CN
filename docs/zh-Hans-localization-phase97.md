# zh-Hans Localization Phase 97

Date: 2026-06-02

## Scope

Phase 97 planned non-public local fixture evidence for GUI rows that cannot be
promoted by source coverage alone. The phase was intentionally read-only except
for documentation artifacts.

## Candidate Classification

| Row | Status | Follow-up |
| --- | --- | --- |
| `GUI-AUTH-02` | `needs-visible-gui-only` | Launch a fresh logged-out profile when the machine is cool, open the token paste modal, paste an invalid redirect URL, and confirm the inline error is Chinese. |
| `GUI-AGENT-01` | `needs-visible-gui-only` | Open the Agent input surface and capture tips/overlap evidence. |
| `GUI-AGENT-02` | `needs-small-debug-fixture` | Seed a disposable local Agent conversation with safe metadata, then open the details panel. |
| `GUI-AGENT-03` | `needs-small-debug-fixture` | Seed lifecycle states for queued, pending, running, done, failed, blocked, and cancelled. |
| `GUI-AGENT-04` | `needs-small-debug-fixture` | Add controlled local web/stream error states; keep AWS/quota variants blocked until safe backend fixtures exist. |
| `GUI-AGENT-05` | `needs-small-debug-fixture` | Seed an Agent Assisted Environment fallback state without creating cloud resources. |
| `GUI-WS-02` | `needs-small-debug-fixture` | Seed disposable session history and delete-toast state. |
| `GUI-WS-03` | `needs-small-debug-fixture` | Seed a disposable rewindable conversation state. |
| `GUI-WS-05` | `unsafe-for-local-fixture` | Do not automate; only verify manually on a disposable machine/profile with explicit permission for admin prompts. |

## Evidence Boundaries

```text
non-public local fixture evidence: allowed for local readiness only
public-RC promotion: not allowed from debug/local fixtures alone
account/backend/billing/cloud/team/secret state: not touched
macOS administrator prompt: not triggered
```

## Qualification Review

```text
phase: 97
status: qualified-local-fixture-plan
artifact README: docs/gui-smoke-artifacts/phase97/README.md
candidate rows classified: yes
GUI launched: no
fixture code added: no
external state touched: no
```

Phase 97 is qualified to continue because all candidate rows now have a
specific fixture readiness classification and no unsafe execution occurred.
