# zh-Hans Localization Phase 26

Date: 2026-06-01

## Goal

Convert the RC8 public-RC GUI blocker list into executable, safe post-RC8 GUI tasks before more source work.

## Readiness Decisions

Phase 26 does not promote any GUI row to `verified`; it prepares execution and keeps public-RC criteria strict.

Owner categories:

- `local-fixture`: can run with a fresh local profile, fake token, test conversation, or debug-only fixture.
- `test-account`: requires an isolated account or team safe to mutate.
- `server-state`: requires quota, billing, capacity, feature flag, or backend state.
- `manual-only`: high-risk or platform-permission path that needs a dedicated manual plan.

## Execution Batches

| Batch | Rows | Profile | Evidence type | Safe to run now |
| --- | --- | --- | --- | --- |
| Logged-out local | `GUI-ONB-01`, `GUI-AUTH-02`, `GUI-AUTH-03`, `GUI-WS-01`, `GUI-WS-03`, `GUI-AGENT-01` | `zh-rc9-local-fixture` | `local-fixture` | Yes, if GUI automation can read the window |
| Local Agent fixture | `GUI-AGENT-02`, `GUI-AGENT-03`, `GUI-AGENT-04`, `GUI-AGENT-05` | `zh-rc9-agent-fixture` | `fixture-evidence` | Requires fixture trigger or existing local conversation |
| Real account auth/settings | `GUI-AUTH-01`, `GUI-SET-03`, `GUI-WS-06` | `zh-rc9-test-account` | `real-account-evidence` | No, requires isolated test account |
| Destructive disposable objects | `GUI-SET-06`, `GUI-WS-04`, `GUI-WS-07` | `zh-rc9-test-account` | `real-account-evidence` | No, requires disposable environment/secret/team |
| Backend state | `GUI-CLOUD-01`, `GUI-BILL-01`, `GUI-BILL-02`, `GUI-LAUNCH-01`, `GUI-ONB-03`, `GUI-WEB-01` | `zh-rc9-server-state` | `blocked-evidence` or backend fixture | No, requires server/feature/billing state |
| AWS credentials | `GUI-SET-04`, `GUI-SET-05` | `zh-rc9-aws-fixture` | `manual-only` or `local-fixture` | No, requires explicit disposable AWS profile or invalid credential fixture |

## Disposable Names

- Custom endpoint: `zh-smoke-delete-endpoint`
- Cloud environment: `zh-smoke-delete-environment`
- Managed auth secret: `zh-smoke-delete-secret`
- Test team: `zh-smoke-public-rc-team`
- Test conversation: `zh-smoke-agent-lifecycle`
- Invalid token marker: `zh-smoke-invalid-token`

## Stop Conditions

- Stop if only the user's main account is available.
- Stop if a row would spend money, consume real credits, mutate production billing state, or touch production cloud state.
- Stop if object names differ from the disposable allowlist above.
- Stop if screenshots expose account identifiers, tokens, secrets, API keys, cookies, or magic links.
- Stop if automation can see only process startup but not target UI.

## Qualification

Phase 26 is accepted as `qualified-public-rc-readiness`.

No source files were changed. No account, billing quota, cloud environment, secret, or team ownership state was touched.
