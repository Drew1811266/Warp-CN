# zh-Hans Public RC Gate Runbook

Date: 2026-06-01

## Purpose

This runbook defines safe public-RC verification for GUI rows that require accounts, backend state, billing state, cloud objects, secrets, or destructive confirmations.

RC14 is `ready-for-local-use-with-fixture-evidence`, and later RCs keep the same
public-RC boundary: public RC remains blocked until current-cycle GUI evidence
exists for account/state paths and visual asset residue is regenerated or
design-approved.

Current RC19 isolated-account handoff:

- `docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md`

Current RC19 backend/disposable fixture contract:

- `docs/zh-Hans-backend-fixture-contract-rc19.md`

Current RC20 blocker registry:

- `resources/localization/zh-Hans-public-rc-blockers.toml`
- `script/zh_public_rc_status.py`

Use the registry as the first public-RC gate evidence source. A blocker cannot
be marked cleared unless the registry status, human phase/release evidence, and
the relevant GUI/backend/account artifact all agree. If any one of those three
sources still reports a blocked state, the row remains blocked.

## Non-Negotiable Safety Rules

- Do not use the user's main account.
- Do not use real billing quota or consume real production credits.
- Do not delete a production cloud environment.
- Do not create, reveal, or delete a real managed secret.
- Do not transfer ownership of a real team.
- Do not store passwords, tokens, cookies, magic links, API keys, or account identifiers in docs.
- Every screenshot must be cropped or redacted before it can be committed.

## Profiles And Naming

Use isolated local profiles:

| Purpose | Profile |
| --- | --- |
| Logged-out GUI smoke | `zh-rc8-logged-out` |
| Test-account GUI smoke | `zh-rc8-test-account` |
| Fixture-only GUI smoke | `zh-rc8-fixture` |
| Post-RC8 local fixture GUI smoke | `zh-rc9-local-fixture` |
| Post-RC8 Agent fixture GUI smoke | `zh-rc9-agent-fixture` |
| Post-RC8 isolated account GUI smoke | `zh-rc9-test-account` |
| Post-RC8 server-state GUI smoke | `zh-rc9-server-state` |
| Post-RC8 AWS fixture GUI smoke | `zh-rc9-aws-fixture` |
| Post-RC9 current-source local GUI smoke | `zh-rc10-local-fixture` |
| Post-RC9 current-source Agent fixture GUI smoke | `zh-rc10-agent-fixture` |
| Post-RC9 isolated account GUI smoke | `zh-rc10-test-account` |
| Post-RC9 server-state GUI smoke | `zh-rc10-server-state` |
| Post-RC9 AWS fixture GUI smoke | `zh-rc10-aws-fixture` |
| Post-RC14 public-RC dry-run evidence package | `zh-rc15-public-rc-dry-run` |
| Post-RC14 isolated account GUI smoke | `zh-rc15-test-account` |
| Post-RC14 server-state GUI smoke | `zh-rc15-server-state` |
| Post-RC14 visual asset review | `zh-rc15-visual-assets` |
| Post-RC15 public-RC dry-run evidence package | `zh-rc16-public-rc-dry-run` |
| Post-RC15 isolated account GUI smoke | `zh-rc16-test-account` |
| Post-RC15 server-state GUI smoke | `zh-rc16-server-state` |
| Post-RC15 AWS/Bedrock fixture GUI smoke | `zh-rc16-aws-fixture` |
| Post-RC15 billing/cloud fixture GUI smoke | `zh-rc16-billing-cloud-fixture` |
| Post-RC18 isolated account GUI smoke | `zh-rc19-test-account` |
| Post-RC18 AWS/Bedrock fixture GUI smoke | `zh-rc19-aws-fixture` |
| Post-RC18 billing/cloud fixture GUI smoke | `zh-rc19-billing-cloud-fixture` |

Disposable object names:

| Object | Name |
| --- | --- |
| Custom endpoint | `zh-smoke-delete-endpoint` |
| Cloud environment | `zh-smoke-delete-environment` |
| Managed auth secret | `zh-smoke-delete-secret` |
| Test team | `zh-smoke-public-rc-team` |
| Test conversation | `zh-smoke-agent-lifecycle` |
| Invalid token marker | `zh-smoke-invalid-token` |

## Evidence Labels

| Label | Use |
| --- | --- |
| `real-account-evidence` | Isolated account proves the actual product state. |
| `fixture-evidence` | Debug/local fixture proves rendering only; not public-RC proof. |
| `blocked-evidence` | Trigger is unavailable or unsafe. |
| `source-anchor` | Source/manifest contains the localized string. |
| `accessibility-evidence` | Computer Use read visible anchors. |
| `cropped-screenshot-evidence` | Redacted screenshot shows the target UI. |

## Required Public-RC Rows

### Auth

| Row | Required state | Allowed action | Evidence anchors | Cleanup |
| --- | --- | --- | --- | --- |
| `GUI-AUTH-01` | Isolated test account with browser auth callback available | Start logged-out profile, complete login, return to app | Login entry, callback success/failure copy, account page in Chinese | Log out and delete local `zh-rc8-test-account` profile if needed |
| `GUI-AUTH-02` | Logged-out profile and invalid token/redirect fixture | Paste only a fake invalid token or invalid redirect URL | Token paste UI, retry/error copy in Chinese | No account state created |
| `GUI-AUTH-03` | Fresh logged-out profile | Open privacy settings or skip-login confirmation | Privacy/skip-login confirmation in Chinese | Delete local profile |

### Settings / AI / Custom Inference

| Row | Required state | Allowed action | Evidence anchors | Cleanup |
| --- | --- | --- | --- | --- |
| `GUI-SET-03` | Isolated account where AI settings and custom inference are visible | Open Settings > AI and inspect only | Build plan, API 密钥, 自定义端点, 模型 | Log out; no real endpoint required unless `GUI-WS-06` runs |
| `GUI-SET-04` | Explicit disposable AWS/Bedrock test profile | Inspect settings only unless a test profile exists | AWS Bedrock, 凭据, 刷新, Profile | Remove disposable AWS profile if created |
| `GUI-SET-05` | Invalid Bedrock credential fixture | Trigger known invalid credential state | AWS credential error copy in Chinese | Remove fixture data |
| `GUI-WS-06` | Isolated account with custom inference enabled | Create and delete only `zh-smoke-delete-endpoint` | 移除端点？, 确定要移除此端点吗？, 取消, 移除端点, 端点已移除 | Confirm endpoint absent after test |

`GUI-WS-06` fixture path may use `WARP_CN_CUSTOM_INFERENCE_SMOKE=1`, but that remains `fixture-verified` only and cannot promote public RC.

### Destructive Confirmations

| Row | Required state | Allowed action | Evidence anchors | Cleanup |
| --- | --- | --- | --- | --- |
| `GUI-SET-06` | Isolated cloud environment named `zh-smoke-delete-environment` | Open delete confirmation; cancel first; delete only disposable object if approved | 删除环境？, 确定要移除, 取消, 删除环境 | Confirm disposable environment absent |
| `GUI-WS-04` | Disposable managed auth secret named `zh-smoke-delete-secret` | Open delete confirmation; cancel first; delete only disposable object if approved | 删除密钥, 确定要删除, 取消, 删除 | Confirm disposable secret absent |
| `GUI-WS-07` | Disposable owner test team only | Prefer source/fixture evidence; real transfer only with explicit approval | Transfer ownership confirmation in Chinese | Restore test ownership or delete test team |

### Billing / Cloud / Launch

| Row | Required state | Allowed action | Evidence anchors | Cleanup |
| --- | --- | --- | --- | --- |
| `GUI-CLOUD-01` | Controlled capacity/quota backend state or fixture | Trigger only mock/fixture unless backend test state exists | Capacity, 点数, upgrade copy in Chinese | Reset fixture/backend test state |
| `GUI-BILL-01` | Safe quota/billing fixture or disposable billing test account | Inspect banner/modal only; do not buy credits | 额度, 自动充值, 方案 copy in Chinese | Reset fixture; no purchase |
| `GUI-BILL-02` | Backend test team with `sunsetted_to_build_ts` state | Trigger modal only | Build plan migration copy in Chinese | Reset backend test flag |
| `GUI-LAUNCH-01` | Feature/version state fixture | Trigger launch modal | Title, CTA, body copy in Chinese | Reset local dismiss state |

### Agent Lifecycle

| Row | Required state | Allowed action | Evidence anchors | Cleanup |
| --- | --- | --- | --- | --- |
| `GUI-AGENT-01` | Agent-enabled local/fixture conversation | Open tips near input | Tips and shortcut copy in Chinese, no overlap | Delete local fixture conversation |
| `GUI-AGENT-02` | Disposable local Agent conversation | Open details panel | Metadata, status, actions in Chinese | Delete local fixture conversation |
| `GUI-AGENT-03` | Lifecycle fixture covering queued, pending, running, done, failed, blocked, cancelled | Inspect fixture states only | 排队中, 等待中, 进行中, 已完成, 失败, 已阻塞, 已取消 | Reset fixture |
| `GUI-AGENT-04` | Mock web/AWS/quota/stream error fixture | Trigger errors without consuming quota | Error fallback copy in Chinese | Reset fixture |
| `GUI-AGENT-05` | Environment modal fallback fixture | Trigger fallback path | Fallback copy in Chinese | Reset fixture |

## Execution Checklist

For each GUI row:

1. Confirm object/account is disposable.
2. Start the app with the intended `WARP_DATA_PROFILE`.
3. Capture process environment proof without secrets.
4. Capture accessibility text where possible.
5. Capture cropped/redacted screenshot.
6. Cancel first for destructive flows.
7. If deletion is part of the test, delete only the disposable object.
8. Confirm cleanup.
9. Update `docs/zh-Hans-gui-smoke-matrix.md`.

## Stop Conditions

Stop immediately if:

- The only available account is the user's main account.
- The test would spend money, consume real credits, or mutate production billing state.
- The object name does not exactly match the disposable allowlist.
- A screenshot contains unredacted secret/account data.
- GUI automation can only see process startup but not the target UI.

## Post-RC8 Execution Batches

Phase 26 groups the remaining public-RC rows into execution batches. These batches are readiness assignments only; they do not promote evidence by themselves.

| Batch | Rows | Profile | Evidence type | Status |
| --- | --- | --- | --- | --- |
| Logged-out local | `GUI-ONB-01`, `GUI-AUTH-02`, `GUI-AUTH-03`, `GUI-WS-01`, `GUI-WS-03`, `GUI-AGENT-01` | `zh-rc9-local-fixture` | `local-fixture` | Ready if GUI automation can read target UI |
| Local Agent fixture | `GUI-AGENT-02`, `GUI-AGENT-03`, `GUI-AGENT-04`, `GUI-AGENT-05` | `zh-rc9-agent-fixture` | `fixture-evidence` | Needs local conversation/lifecycle/error fixture |
| Real account auth/settings | `GUI-AUTH-01`, `GUI-SET-03`, `GUI-WS-06` | `zh-rc9-test-account` | `real-account-evidence` | Blocked until isolated test account exists |
| Destructive disposable objects | `GUI-SET-06`, `GUI-WS-04`, `GUI-WS-07` | `zh-rc9-test-account` | `real-account-evidence` | Blocked until disposable environment, secret, and team exist |
| Backend state | `GUI-CLOUD-01`, `GUI-BILL-01`, `GUI-BILL-02`, `GUI-LAUNCH-01`, `GUI-ONB-03`, `GUI-WEB-01` | `zh-rc9-server-state` | `blocked-evidence` or backend fixture | Requires backend/feature/billing state |
| AWS credentials | `GUI-SET-04`, `GUI-SET-05` | `zh-rc9-aws-fixture` | `manual-only` or `local-fixture` | Requires explicit disposable AWS profile or invalid credential fixture |

Cleanup commands are profile/object specific and must be written into the row record after execution. Do not run cleanup against any object whose name is not in the disposable allowlist.

## Post-RC9 Fixture Preparation

Phase 37 keeps fixture evidence separate from public-RC evidence. These fixture paths may prove rendering and screenshots, but they cannot promote a row to public-RC `verified` without non-fixture isolated account/backend evidence.

| Fixture area | Rows | Intended profile | Trigger policy | Evidence label |
| --- | --- | --- | --- | --- |
| Current-source logged-out onboarding | `GUI-ONB-01`, `GUI-AUTH-03`, `GUI-WS-01` | `zh-rc10-local-fixture` | Rebuild current source once, launch logged-out, capture current-source screenshots. | `fixture-evidence` or `accessibility-evidence` |
| Token fallback | `GUI-AUTH-02` | `zh-rc10-local-fixture` | Use only fake invalid token/redirect text; do not complete real auth. | `fixture-evidence` |
| Agent local fixtures | `GUI-AGENT-01` through `GUI-AGENT-05` | `zh-rc10-agent-fixture` | Use local/debug-only fixture states for tips, conversation details, lifecycle labels, error states, and environment fallback. | `fixture-evidence` |
| Static onboarding imagery | `GUI-ONB-01` | N/A | Do not treat embedded PNG English as Rust manifest drift. Regenerate localized PNGs or document as accepted product imagery before public release. | `visual-residue` |

Candidate visual asset roots:

- `app/assets/async/png/onboarding/welcome_agent.png`
- `app/assets/async/png/onboarding/welcome_terminal.png`
- `app/assets/async/png/onboarding/agent_intention/`
- `app/assets/async/png/onboarding/terminal_intention/`
- `app/assets/async/png/onboarding/thirdparty_*.png`

Fixture env gates, if implemented, must be debug-only and inert without the env var. They must not create accounts, spend credits, create/delete cloud objects, reveal secrets, or mutate team ownership.

## Post-RC13 Public-RC Evidence Package

Phase 67 keeps RC14 source readiness separate from true public-RC readiness.
Rows below require current-cycle evidence. Fixture evidence may prove rendering,
but it cannot promote a row to public-RC `verified`.

| Row | Disposable prerequisite | Capture target | Cleanup target | Current status |
| --- | --- | --- | --- | --- |
| `GUI-AUTH-01` | Isolated browser-login test account, not the user's main account | Logged-out entry, browser auth callback, returned account/settings state in Chinese | Log out; remove local test profile artifacts | `blocked-until-isolated-account` |
| `GUI-SET-03` | Isolated account with AI settings, Build plan/API key/custom inference UI available | Settings > AI anchors for Build plan, API key, custom endpoint, model copy | Log out; do not create a real endpoint unless `GUI-WS-06` also runs | `blocked-until-isolated-account-state` |
| `GUI-SET-04` | Disposable AWS/Bedrock profile or explicit manual-only fixture | AWS Bedrock credential settings copy and refresh/profile controls | Remove only the disposable AWS profile | `blocked-until-disposable-aws-profile` |
| `GUI-SET-05` | Invalid Bedrock credential fixture that cannot reach real credentials | AWS credential error copy in Chinese | Remove fixture data | `blocked-until-invalid-credential-fixture` |
| `GUI-SET-06` | Disposable cloud environment named `zh-smoke-delete-environment` | Delete confirmation, cancel path, optional approved delete path | Confirm disposable environment is absent or restored | `blocked-until-disposable-environment` |
| `GUI-WS-04` | Disposable managed auth secret named `zh-smoke-delete-secret` | Delete-secret confirmation and cancel path | Confirm disposable secret is absent or restored | `blocked-until-disposable-secret` |
| `GUI-WS-06` | Isolated account with custom inference enabled and endpoint named `zh-smoke-delete-endpoint` | Remove endpoint confirmation, cancel path, optional approved delete path | Confirm disposable endpoint absent | `fixture-verified-only` |
| `GUI-WS-07` | Disposable owner test team named `zh-smoke-public-rc-team` | Transfer ownership confirmation only after explicit approval | Restore ownership or delete test team | `blocked-until-disposable-team` |
| `GUI-BILL-01` | Safe quota/billing fixture or disposable billing test account | Out-of-credits/buy-credits banner/modal copy | Reset fixture; no purchase | `blocked-until-safe-billing-state` |
| `GUI-BILL-02` | Backend test team with `sunsetted_to_build_ts` state | Build plan migration modal | Reset backend test flag | `blocked-until-backend-billing-state` |
| `GUI-CLOUD-01` | Controlled capacity/quota backend state or local fixture | Cloud Agent capacity/quota modal copy | Reset fixture/backend state | `blocked-until-capacity-fixture` |

Screenshot rules:

1. Capture cropped/redacted screenshots only.
2. Record accessibility text when available.
3. Never capture secrets, tokens, cookies, account identifiers, magic links,
   API keys, full browser URLs, or billing details.
4. Record cleanup proof for every disposable object.
5. Keep fixture-only evidence labelled `fixture-evidence` and true isolated
   account/backend evidence labelled `real-account-evidence`.

## Phase 76 Public-RC Evidence Dry-Run Package

Phase 76 makes the remaining public-RC blockers execution-ready. It does not
launch the GUI, create accounts, create backend objects, create/delete secrets,
consume billing quota, or mutate cloud/team state.

Artifact directory:

- `docs/gui-smoke-artifacts/phase76/`

Default dry-run profile:

```text
zh-rc15-public-rc-dry-run
```

Allowed evidence in this directory:

```text
cropped/redacted screenshots
accessibility text excerpts
process profile proof without secrets
fixture state descriptions
cleanup proof for disposable objects
```

Forbidden evidence:

```text
passwords
tokens
cookies
magic links
API keys
full browser URLs
account identifiers
billing details
unredacted team names
raw full-screen desktop screenshots
```

Dry-run blocker table:

| Row | Prerequisite | Profile | Safe object | Screen to capture | Pass wording | Fail wording | Cleanup proof | Current status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `GUI-AUTH-01` | Isolated browser-login test account; never the user's main account | `zh-rc15-test-account` | N/A | Logged-out entry, browser callback result, returned account/settings state | `real-account-evidence`: login and callback UI are Chinese, account state returns to app | `blocked-evidence`: no isolated account or callback unavailable | Screenshot/log out proof; local profile removal if created | `blocked-until-isolated-account` |
| `GUI-SET-03` | Isolated account with AI settings, Build plan, API key, custom inference visible | `zh-rc15-test-account` | Optional endpoint only if `GUI-WS-06` also runs | Settings > AI anchors for Build plan, API key, custom endpoint, model copy | `real-account-evidence`: all visible anchors are Chinese | `blocked-evidence`: account state unavailable or custom inference hidden | Logout proof; no endpoint cleanup unless created | `blocked-until-isolated-account-state` |
| `GUI-SET-04` | Disposable AWS/Bedrock test profile or explicit manual fixture | `zh-rc15-aws-fixture` | Disposable AWS profile only | AWS Bedrock credential settings, refresh/profile controls | `real-account-evidence` or `fixture-evidence`: credential UI is Chinese | `blocked-evidence`: no disposable AWS profile/fixture | Disposable profile removed or fixture reset | `blocked-until-disposable-aws-profile` |
| `GUI-SET-05` | Invalid Bedrock credential fixture that cannot access real credentials | `zh-rc15-aws-fixture` | `zh-smoke-invalid-token` marker only | AWS credential error copy | `fixture-evidence`: invalid credential error is Chinese | `blocked-evidence`: fixture unavailable | Fixture marker removed | `blocked-until-invalid-credential-fixture` |
| `GUI-SET-06` | Disposable cloud environment named exactly `zh-smoke-delete-environment` | `zh-rc15-test-account` | `zh-smoke-delete-environment` | Delete environment confirmation and cancel path | `real-account-evidence`: confirmation/cancel/delete copy is Chinese | `blocked-evidence`: object missing or not exact allowlist name | Object absent or restored; screenshot of cleanup state | `blocked-until-disposable-environment` |
| `GUI-WS-04` | Disposable managed auth secret named exactly `zh-smoke-delete-secret` | `zh-rc15-test-account` | `zh-smoke-delete-secret` | Delete-secret confirmation and cancel path | `real-account-evidence`: confirmation/cancel/delete copy is Chinese | `blocked-evidence`: secret missing or not exact allowlist name | Secret absent or restored; screenshot of cleanup state | `blocked-until-disposable-secret` |
| `GUI-WS-06` | Isolated account with custom inference enabled and endpoint named exactly `zh-smoke-delete-endpoint` | `zh-rc15-test-account` | `zh-smoke-delete-endpoint` | Remove endpoint confirmation, cancel path, approved delete path | `real-account-evidence`: remove confirmation, cancel, delete, and toast are Chinese | `fixture-evidence-only`: debug env path used; cannot promote public RC | Endpoint absent after cleanup | `fixture-verified-only` |
| `GUI-WS-07` | Disposable owner test team named exactly `zh-smoke-public-rc-team`; explicit approval required | `zh-rc15-test-account` | `zh-smoke-public-rc-team` | Transfer ownership confirmation | `real-account-evidence`: confirmation copy is Chinese and ownership restored | `blocked-evidence`: no disposable owner team or approval | Ownership restored or team deleted | `blocked-until-disposable-team` |
| `GUI-BILL-01` | Safe billing/quota fixture or disposable billing test account; no purchases | `zh-rc15-server-state` | Fixture only | Out-of-credits or buy-credits banner/modal | `fixture-evidence` or backend test evidence: billing copy is Chinese without purchase | `blocked-evidence`: would spend money or use real quota | Fixture reset; no purchase proof | `blocked-until-safe-billing-state` |
| `GUI-BILL-02` | Backend test team with `sunsetted_to_build_ts` state | `zh-rc15-server-state` | Backend test flag only | Build plan migration modal | `real-account-evidence`: migration copy is Chinese | `blocked-evidence`: backend state unavailable | Backend flag reset proof | `blocked-until-backend-billing-state` |
| `GUI-CLOUD-01` | Controlled capacity/quota backend state or local fixture | `zh-rc15-server-state` | Fixture only | Cloud Agent capacity/quota modal | `fixture-evidence` or backend test evidence: capacity/quota copy is Chinese | `blocked-evidence`: would consume real quota or state unavailable | Fixture/backend state reset proof | `blocked-until-capacity-fixture` |

## Phase 83 Public-RC Prerequisites RC16

Phase 83 updates the dry-run package for RC16. It does not launch GUI, create
accounts, create backend objects, create/delete secrets, consume billing quota,
or mutate cloud/team state.

Primary document:

- `docs/zh-Hans-public-rc-prerequisites-rc16.md`

RC16 statuses:

| Row | RC16 profile | Exact prerequisite | Evidence target | Cleanup proof | Current status |
| --- | --- | --- | --- | --- | --- |
| `GUI-AUTH-01` | `zh-rc16-test-account` | Isolated browser-login account, never the user's main account | Logged-out entry, browser callback, returned account/settings UI | Log out and remove local test profile artifacts | `blocked-no-isolated-account` |
| `GUI-SET-03` | `zh-rc16-test-account` | Account where AI settings, Build plan, API key, custom inference, and model UI are visible | Settings > AI anchors | Log out; no endpoint unless `GUI-WS-06` runs | `blocked-no-isolated-account` |
| `GUI-SET-04` | `zh-rc16-aws-fixture` | Disposable AWS/Bedrock profile or manual fixture | AWS Bedrock credentials and refresh/profile controls | Remove profile or reset fixture | `blocked-no-backend-fixture` |
| `GUI-SET-05` | `zh-rc16-aws-fixture` | Invalid Bedrock credential fixture | AWS credential error copy | Remove fixture marker | `blocked-no-backend-fixture` |
| `GUI-SET-06` | `zh-rc16-server-state` | `zh-smoke-delete-environment` cloud environment | Delete environment confirmation and cancel path | Object absent or restored | `blocked-no-disposable-object` |
| `GUI-WS-04` | `zh-rc16-test-account` | `zh-smoke-delete-secret` managed auth secret | Delete-secret confirmation and cancel path | Secret absent or restored | `blocked-no-disposable-object` |
| `GUI-WS-06` | `zh-rc16-test-account` | Custom inference endpoint `zh-smoke-delete-endpoint` | Remove endpoint confirmation, cancel, delete, toast | Endpoint absent | `blocked-no-isolated-account` |
| `GUI-WS-07` | `zh-rc16-test-account` | Owner test team `zh-smoke-public-rc-team`; explicit approval required | Transfer ownership confirmation | Ownership restored or team deleted | `blocked-no-disposable-object` |
| `GUI-BILL-01` | `zh-rc16-billing-cloud-fixture` | Safe quota/billing fixture or disposable billing test account | Out-of-credits/buy-credits banner/modal | Fixture reset; no purchase | `blocked-no-backend-fixture` |
| `GUI-BILL-02` | `zh-rc16-server-state` | Backend test team with `sunsetted_to_build_ts` | Build plan migration modal | Backend flag reset | `blocked-no-backend-fixture` |
| `GUI-CLOUD-01` | `zh-rc16-billing-cloud-fixture` | Controlled capacity/quota backend state or local fixture | Cloud Agent capacity/quota modal | Fixture/backend reset; no real quota consumed | `blocked-no-backend-fixture` |

Do not promote any Phase 83 row to `verified-current-cycle` until cropped or
redacted screenshots, accessibility anchors, and cleanup proof exist for the
current RC cycle.

For every row, record:

```text
row id
profile
evidence type
screens captured
accessibility anchors captured
redactions applied
cleanup result
remaining blocker
```

Fixture evidence remains useful for rendering confidence, but only true isolated
account/backend evidence plus cleanup proof can promote public RC.
