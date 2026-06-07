# zh-Hans Test Environment Approval Readiness - 2026-06-03

## Status

Readiness-only preparation is incomplete until the isolated account and
disposable object approval packets are provided and reviewed. This document is
repo-safe status only. It does not include raw evidence, account identifiers,
object IDs, endpoint URLs, private names, support thread contents, screenshots,
recordings, or logs.

## Isolated Account Readiness

Rows covered:

- `GUI-AUTH-01`
- `GUI-SET-03`
- `GUI-WS-06`

Pending approval packet requirements:

```text
isolated account is not the user's main account
login flow is approved for public-RC evidence capture
Settings > AI visibility is approved
custom inference endpoint test object is named zh-smoke-delete-endpoint
logout or profile cleanup proof format is defined
raw evidence review owner is named
redaction reviewer is named
```

Current readiness state:

- Preparation docs define the required approval packet.
- The public smoke endpoint object name is constrained to `zh-smoke-delete-endpoint`.
- Evidence capture, GUI login, profile cleanup, and candidate artifact creation remain blocked until explicit approval and reviewed raw evidence exist.

## Disposable Object Readiness

Rows covered:

- `GUI-SET-06`
- `GUI-WS-04`
- `GUI-WS-07`

Pending approval packet requirements:

```text
object exists and is disposable
object name exactly matches the allowlist
cancel-first path is approved
delete or transfer path is explicitly approved
cleanup absence or restoration proof format is defined
raw evidence review owner is named
redaction reviewer is named
```

Current readiness state:

- Preparation docs define the required approval packet.
- Cancel-first and cleanup proof requirements are documented.
- Object mutation, deletion, transfer, and candidate artifact creation remain blocked until exact allowlisted objects and explicit approvals are available.

## Allowed Public Smoke Object Names

Only these public smoke object names are allowed:

```text
zh-smoke-delete-environment
zh-smoke-delete-secret
zh-smoke-public-rc-team
zh-smoke-delete-endpoint
```

## No-Go Rules

```text
no personal account
no real team
no real secret
no real environment
no real endpoint
no real billing or cloud capacity mutation
```

Do not create, delete, transfer, reset, or mutate any object outside the
allowlist. Do not run GUI flows, create candidate files, promote artifacts, edit
evidence ledgers, edit blocker ledgers, stage, commit, tag, push, create a
release, or publish evidence from this preparation pass.

## Next Actions

- Obtain the isolated account approval packet with every required statement.
- Obtain disposable object approval packets for exact allowlisted public smoke objects only.
- Assign raw evidence review and redaction review ownership outside raw-evidence artifacts.
- Hand off any post-approval evidence capture, candidate creation, preflight, GUI execution, object mutation, artifact promotion, and ledger updates to a separately approved evidence-execution workflow.
- Keep strict artifact lint expected to fail until that separately approved workflow provides reviewed redacted artifacts.
