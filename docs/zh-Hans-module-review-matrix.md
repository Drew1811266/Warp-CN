# zh-Hans Module Review Matrix

This matrix defines the module-level review surface for Warp CN. Use it together with `docs/zh-Hans-gui-smoke-matrix.md`; the GUI matrix records concrete visual evidence, while this file records what each module must be reviewed for.

## Status Definitions

| Status | Meaning |
| --- | --- |
| `review-ready` | Current manifest can be reviewed with source and low-load gates |
| `needs-gui` | Requires visible app evidence before promotion |
| `needs-account-state` | Requires isolated account, billing, team, cloud, or feature state |
| `fixture-only` | Local fixture can validate rendering but not public-RC readiness |
| `do-not-translate-by-default` | Mostly internal strings; translate only with explicit proof |
| `reviewed-low-load` | Source, manifest, inventory, and low-load gates passed; GUI or heavy release gates may still be pending |

## Module Matrix

| Module | Main source areas | Current review status | Risk class | Review focus | Required evidence |
| --- | --- | --- | --- | --- | --- |
| Base workspace shell | `app/src/workspace`, `app/src/tab.rs`, `app/src/terminal` | `needs-gui` | `T1/F2` | Menus, tab actions, terminal labels, panel labels, toast clarity | Source review, low-load gate, GUI smoke rows `GUI-BASE-*`, `GUI-WS-*` |
| Onboarding | `app/src/onboarding`, login slides, first-run views | `needs-gui` | `T1/F1` | Fresh profile path, Agent path, terminal-only path, permission wording | Isolated fresh profile, GUI rows `GUI-ONB-*` |
| Auth and account | `app/src/auth`, login modals, token paste fallback | `needs-account-state` | `T0/F1` | Login, retry, token paste, auth failure, privacy and skip-login copy | Isolated test account or invalid-token fixture, no credentials in docs |
| Search and command palette | Command palette, action registry, search entry points | `reviewed-low-load` | `T1/F1` | Visible action labels vs search tags/keywords, shortcut labels, filter chips, accessibility label prefixes | Source review completed in `docs/zh-Hans-module-review-search-2026-06-01.md`; GUI row `GUI-BASE-05` and release-only command/search tests still apply before RC |
| Settings shell | `app/src/settings_view` | `needs-gui` | `T1/F2` | Navigation labels, tabs, toggles, warnings, short button labels | Source review, GUI row `GUI-SET-01` |
| AI settings and providers | `app/src/settings_view/ai_page.rs`, provider key sections, BYOK | `needs-account-state` | `T1/F1` | API key, model, provider, endpoint, fallback, Build plan language | Source review, isolated account or debug fixture where explicitly marked |
| Custom inference | `custom_inference_modal.rs`, remove endpoint dialog, AI API key paths | `fixture-only` until real account exists | `T0/F1` | Add/edit/remove endpoint, cancel path, endpoint values, no real data deletion | Fixture evidence may stay `fixture-verified`; public RC requires isolated account |
| Warp Drive and workflows | Warp Drive views, notebooks, workflows, saved configs | `needs-gui` | `T1/F2` | Save/share/sync wording, ownership, empty states, import/export labels | Source review, GUI smoke with disposable data |
| Agent conversation and status | `app/src/ai`, ambient agent, conversation details | `needs-account-state` | `T1/F2` | Queued/running/failed/blocked/cancelled labels, errors, tips, metadata | Model fixture or isolated Agent task lifecycle state |
| Cloud environments | Environment settings, cloud/remote environment flows | `needs-account-state` | `T0/F1` | Delete environment, capacity, unavailable state, fallback copy | Isolated cloud environment object only |
| Billing and usage | Billing settings, credits, plan modals, usage banners | `needs-account-state` | `T0/F1` | Money, quota, credits, upgrades, auto-reload, plan migration | Isolated billing-capable test state or model-level fixture |
| Teams and ownership | Team invite, role, owner transfer, member management | `needs-account-state` | `T0/F1` | Role names, transfer ownership, remove member, invite copy | Team test account only; no main account |
| Destructive confirmations | Endpoint, environment, auth secret, session, team actions | `needs-account-state` | `T0/F1` | Title, body, object name, cancel button, final destructive button | Cancel first, prove object remains, then delete disposable object only |
| Modals and toasts | Common modal components, launch modals, toasts | `review-ready` but low coverage | `T1/F2` | Button order, title clarity, dynamic object interpolation, line wrapping | Source review, GUI evidence for high-risk modals |
| Terminal commands and shell examples | Terminal command suggestions, CLI instructions, shell snippets | `review-ready` | `T1/F0` | Do not translate executable commands or flags; translate explanation only | Source review and exact token preservation |
| Logs, telemetry, protocol, tests | `TelemetryEvent`, `log::`, `tracing::`, serde/schema/test data | `do-not-translate-by-default` | `T0/F0` | Preserve internal identifiers and diagnostic strings unless clearly user-facing | Ignore rule or explicit review note |

## Module Exit Criteria

A module can move from `needs-gui` to `reviewed-local` when:

- The manifest entries pass schema, glossary, and dry-run gates.
- High-risk entries have functional-risk notes.
- At least one current-cycle GUI evidence path covers the module's primary visible surfaces.
- Any remaining account or service dependency is listed as a concrete blocker.

A module can move to `public-rc-ready` only when:

- It has no `T0`, `T1`, `F0`, or `F1` open issues.
- Destructive, billing, auth, and team flows use isolated test data.
- Fixture evidence is not used as the only proof for public-RC claims.
