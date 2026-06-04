# zh-Hans Localization Phase 44

Date: 2026-06-02

## Goal

Close high-value auth-secret FTUX source gaps and audit local Agent fixture evidence without touching real accounts, secrets, cloud objects, billing, quota, or team state.

## Scope

Phase 44 added 30 scoped manifest entries:

```text
translated visible entries: 25
reviewed preserve entries: 5
files touched by scoped manifest: 3
main manifest entries after Phase 44: 7088
manifest context/status metadata: 100.0%
```

Translated visible copy:

| Area | Files |
| --- | --- |
| Auth-secret FTUX | `app/src/terminal/view/ambient_agent/auth_secret_ftux_view.rs` |
| Agent task toasts/source labels | `app/src/ai/ambient_agents/task.rs` |
| Agent management notifications | `app/src/ai/agent_management/agent_management_model.rs` |

Reviewed preserves:

| Class | Files |
| --- | --- |
| Product/source names | `app/src/ai/ambient_agents/task.rs` |
| Agent fallback display name | `app/src/ai/ambient_agents/task.rs` |

## Coverage

After Phase 44:

```text
AI / Agent coverage: 2223 covered / 469 candidates = 82.6%
release coverage: 7757 covered / 1191 candidates = 86.7%
```

The Phase 44 source target files now have no remaining inventory candidates:

```text
python3 script/zh_localization_inventory.py --status candidate \
  app/src/terminal/view/ambient_agent/auth_secret_ftux_view.rs \
  app/src/ai/ambient_agents/task.rs \
  app/src/ai/agent_management/agent_management_model.rs
```

Result:

```text
| status | path | line | literal |
| --- | --- | ---: | --- |
```

## Fixture Audit

No GUI launch was attempted in Phase 44. The execution constraint was to avoid local overheating, and source inspection did not find a safe existing Agent fixture hook worth launching.

Existing fixture support found:

- `WARP_CN_CUSTOM_INFERENCE_SMOKE=1` covers the custom inference endpoint deletion path only.
- Unit-test-only fixtures exist for shared-session/cloud-continuation internals, but they do not expose a GUI fixture trigger for local smoke evidence.

Missing Agent fixture hooks:

| Row | Missing hook |
| --- | --- |
| `GUI-AGENT-01` | Env-gated Agent tips fixture that opens the Agent input area and exposes overlap/accessibility evidence. |
| `GUI-AGENT-02` | Disposable local Agent conversation seed that opens the details panel with safe metadata. |
| `GUI-AGENT-03` | Lifecycle-state fixture for queued, pending, in progress, done, failed, blocked, and cancelled. |
| `GUI-AGENT-04` | Controlled stream/web/AWS/quota error injection fixtures that do not use main-account quota or credentials. |
| `GUI-AGENT-05` | Environment modal fixture that triggers Agent Assisted Environment fallback copy. |
| `GUI-AUTH-02` | Visible invalid-token/token-paste fallback fixture for logged-out profiles. |
| `GUI-WS-04` | Disposable managed auth secret or auth-secret deletion fixture for `zh-smoke-delete-secret`. |

The GUI matrix was updated with this Phase 44 audit. No row was promoted to public-RC `verified`, and no fixture evidence was mislabeled as real account/backend evidence.

## Safety Review

No real secret name, API-key value, auth provider ID, secure-storage key, backend object, billing quota, team state, or cloud object was created, modified, viewed, or deleted.

`cargo check` was intentionally not run in this phase because the changes are string-only, `cargo fmt --check` passed, and the low-load policy reserves Rust builds for Phase 48 or runtime-code changes.

## Validation

Passed:

```text
python3 script/zh_apply_localization.py --manifest .omx/tmp-phase44-manifest.toml --dry-run --summary
# entries: 30
# files: 3
# already_applied: 25
# would_change: 0
# missing: 0

python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py
cargo fmt --check
git diff --check
```

## Qualification

Phase 44 is accepted as `qualified-auth-secret-ftux-source-and-agent-fixture-blockers`.
