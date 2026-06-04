# zh-Hans Public RC Prerequisites RC16

Date: 2026-06-02 Asia/Shanghai.

## Purpose

This document converts the remaining public-RC GUI blockers into exact
prerequisites for a future evidence run. Phase 83 does not launch the GUI, create
accounts, create backend objects, create/delete secrets, consume billing quota,
or mutate cloud/team state.

## Safety Policy

- Do not use the user's main account.
- Do not buy credits, spend production quota, or mutate production billing.
- Do not create, reveal, or delete real managed secrets.
- Do not delete real cloud environments.
- Do not transfer ownership of real teams.
- Do not store passwords, tokens, cookies, magic links, API keys, account IDs,
  emails, billing details, or full browser callback URLs in docs.
- Capture cropped/redacted screenshots only.
- Record cleanup proof for every disposable object.

## Required Profiles

| Purpose | Profile | Status |
| --- | --- | --- |
| Public-RC dry run | `zh-rc16-public-rc-dry-run` | `ready-with-prerequisites` |
| Isolated browser login | `zh-rc16-test-account` | `blocked-no-isolated-account` |
| Server/account-state GUI rows | `zh-rc16-server-state` | `blocked-no-backend-fixture` |
| AWS/Bedrock fixture | `zh-rc16-aws-fixture` | `blocked-no-backend-fixture` |
| Billing/capacity fixture | `zh-rc16-billing-cloud-fixture` | `blocked-no-backend-fixture` |

## Disposable Objects

| Object | Required exact name | Current status |
| --- | --- | --- |
| Custom inference endpoint | `zh-smoke-delete-endpoint` | `blocked-no-isolated-account` |
| Cloud environment | `zh-smoke-delete-environment` | `blocked-no-disposable-object` |
| Managed auth secret | `zh-smoke-delete-secret` | `blocked-no-disposable-object` |
| Owner test team | `zh-smoke-public-rc-team` | `blocked-no-disposable-object` |
| Invalid credential marker | `zh-smoke-invalid-token` | `blocked-no-backend-fixture` |

## Blocker Table

| Row | Owner | Prerequisite | Evidence path | Cleanup rule | Phase 83 status |
| --- | --- | --- | --- | --- | --- |
| `GUI-AUTH-01` | Release executor plus isolated-account owner | Isolated browser-login account, never the user's main account | Launch `zh-rc16-test-account`, complete browser auth callback, capture logged-out entry and returned account/settings UI in Chinese | Log out; remove local test profile artifacts; redact callback evidence | `blocked-no-isolated-account` |
| `GUI-SET-03` | Release executor plus isolated-account owner | Account where AI settings, Build plan, API key, custom inference, and model UI are visible | Open Settings > AI and capture Build plan/API key/custom endpoint/model anchors | Log out; do not create endpoints unless `GUI-WS-06` also runs | `blocked-no-isolated-account` |
| `GUI-SET-04` | Release executor plus AWS fixture owner | Disposable AWS/Bedrock profile or explicit manual fixture | Capture AWS Bedrock credentials, refresh/profile controls, and credential copy | Remove only the disposable AWS profile or reset fixture | `blocked-no-backend-fixture` |
| `GUI-SET-05` | Release executor plus AWS fixture owner | Invalid Bedrock credential fixture that cannot touch real credentials | Trigger invalid credential error copy in Chinese | Remove `zh-smoke-invalid-token` fixture data | `blocked-no-backend-fixture` |
| `GUI-SET-06` | Release executor plus backend fixture owner | Disposable cloud environment named exactly `zh-smoke-delete-environment` | Open delete confirmation, capture cancel path, optionally delete only approved disposable object | Confirm object is absent or restored; capture cleanup proof | `blocked-no-disposable-object` |
| `GUI-WS-04` | Release executor plus secret fixture owner | Disposable managed auth secret named exactly `zh-smoke-delete-secret` | Open delete-secret confirmation and cancel path | Confirm secret is absent or restored; capture cleanup proof | `blocked-no-disposable-object` |
| `GUI-WS-06` | Release executor plus isolated-account owner | Isolated account with custom inference enabled and endpoint named exactly `zh-smoke-delete-endpoint` | Capture remove endpoint confirmation, cancel path, approved delete path, and toast | Confirm endpoint absent after cleanup | `blocked-no-isolated-account` |
| `GUI-WS-07` | Release executor plus team fixture owner | Disposable owner test team named exactly `zh-smoke-public-rc-team`; explicit approval required before ownership mutation | Capture transfer ownership confirmation only after approval | Restore ownership or delete disposable team; capture proof | `blocked-no-disposable-object` |
| `GUI-BILL-01` | Release executor plus billing fixture owner | Safe quota/billing fixture or disposable billing test account; no purchase flow | Capture out-of-credits/buy-credits banner or modal copy in Chinese | Reset fixture; prove no purchase occurred | `blocked-no-backend-fixture` |
| `GUI-BILL-02` | Release executor plus backend billing owner | Backend test team with `sunsetted_to_build_ts` state | Capture Build plan migration modal copy in Chinese | Reset backend test flag | `blocked-no-backend-fixture` |
| `GUI-CLOUD-01` | Release executor plus cloud fixture owner | Controlled capacity/quota backend state or local fixture | Capture Cloud Agent capacity/quota modal copy in Chinese | Reset fixture/backend state; prove no real quota consumed | `blocked-no-backend-fixture` |

## Evidence Requirements

Every row must include:

```text
profile name
disposable object name when applicable
process/profile proof without secrets
accessibility anchors when available
cropped/redacted screenshot path
pass/fail wording
cleanup proof
evidence label: real-account-evidence, fixture-evidence, blocked-evidence, or accessibility-evidence
```

## Current Decision

RC16 public-RC evidence remains blocked. The rows above are execution-ready only
after their isolated account, backend fixture, or disposable object prerequisite
exists. Phase 83 does not promote any row to `verified-current-cycle`.
