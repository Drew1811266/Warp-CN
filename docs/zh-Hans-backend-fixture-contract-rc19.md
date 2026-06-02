# zh-Hans Backend Fixture Contract RC19

Date: 2026-06-02

## Scope

This contract defines the backend and disposable object fixtures required for
public-RC zh-Hans GUI evidence. It is a handoff document only and does not
contact backend services or create test data.

## Fixture Names

```text
zh-rc19-aws-fixture
zh-rc19-billing-cloud-fixture
zh-smoke-invalid-token
zh-smoke-delete-environment
zh-smoke-delete-secret
zh-smoke-public-rc-team
```

## Row Mapping

| Row | Fixture | Evidence Target |
| --- | --- | --- |
| `GUI-SET-04` | `zh-rc19-aws-fixture` | Disposable AWS/Bedrock settings copy without real credentials. |
| `GUI-SET-05` | `zh-smoke-invalid-token` | Invalid Bedrock credential state and user-facing error copy. |
| `GUI-SET-06` | `zh-smoke-delete-environment` | Environment delete confirmation and cleanup proof. |
| `GUI-WS-04` | `zh-smoke-delete-secret` | Managed auth secret delete confirmation and cleanup proof. |
| `GUI-WS-07` | `zh-smoke-public-rc-team` | Team ownership transfer confirmation on a disposable owner test team only. |
| `GUI-BILL-01` | `zh-rc19-billing-cloud-fixture` | Out-of-credits or monthly-limit copy without purchase or quota consumption. |
| `GUI-BILL-02` | `zh-rc19-billing-cloud-fixture` | Build plan migration modal with safe backend test team state. |
| `GUI-CLOUD-01` | `zh-rc19-billing-cloud-fixture` | Controlled cloud capacity/quota modal state. |

## Fixture Safety Requirements

Every fixture must provide:

```text
fixture owner
reset procedure
allowed mutations
cleanup procedure
redaction requirements
expected evidence
expiration or teardown date
statement that no production object is affected
```

## Row-Specific Cleanup Proof

```text
GUI-SET-04:
  AWS/Bedrock fixture never uses real credentials.
  Cleanup proves any local disposable profile/config is removed or reset.

GUI-SET-05:
  Invalid token marker is zh-smoke-invalid-token or equivalent safe test value.
  Cleanup proves invalid fixture state is reset.

GUI-SET-06:
  Deleted environment is named exactly zh-smoke-delete-environment.
  Cleanup proves the environment is absent or restored by fixture reset.

GUI-WS-04:
  Deleted managed secret is named exactly zh-smoke-delete-secret.
  Cleanup proves the secret is absent or restored by fixture reset.

GUI-WS-07:
  Ownership transfer is approved only on zh-smoke-public-rc-team.
  Cleanup proves ownership is restored or the disposable team is deleted.

GUI-BILL-01:
  Fixture never purchases credits or consumes real quota.
  Cleanup proves billing/quota state is reset.

GUI-BILL-02:
  Build-plan migration state is backend test state only.
  Cleanup proves sunset/migration flags are reset.

GUI-CLOUD-01:
  Capacity/quota state is controlled fixture state only.
  Cleanup proves backend fixture state is reset.
```

## Prohibited Evidence

```text
real AWS credentials
real payment method or billing ID
real credit purchase
real quota consumption
production cloud environment
production managed secret
production team ownership transfer
unredacted account, team, endpoint, token, key, or secret data
```

## Public-RC Promotion Rule

Rows covered by this contract remain blocked until the fixture owner provides
redacted evidence and cleanup proof. Source inspection or local debug fixture
evidence alone cannot promote these rows to public-RC verified.

