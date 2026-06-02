# zh-Hans Public RC Isolated Account Runbook RC19

Date: 2026-06-02

## Scope

This runbook defines the isolated-account evidence path for public-RC GUI rows.
It is a handoff document only. It does not create, log into, refresh, inspect,
or mutate any account.

## Account Label

```text
zh-rc19-test-account
```

The account must be separate from the user's main account and must not carry
production admin, billing, cloud, team, managed-secret, or endpoint state that
cannot be safely reset.

## Rows Covered

```text
GUI-AUTH-01
GUI-SET-03
GUI-WS-06
```

## Prerequisites

```text
account is isolated from the user's main account
local test profile is disposable
browser auth callback can be received by the app
AI settings state is available
custom inference is enabled
disposable endpoint name is zh-smoke-delete-endpoint
all sensitive values are redacted in artifacts
cleanup proof is captured after the run
```

## Prohibited Actions

```text
do not use the user's main account
do not expose email addresses, auth tokens, API keys, endpoint URLs, team IDs,
billing IDs, managed secret names beyond the disposable allowlist, or secret
values in artifacts
do not delete a real custom endpoint
do not mutate production team, billing, cloud, managed-secret, or endpoint state
```

## Evidence Checklist

For every attempted row, record:

```text
fresh or isolated profile name
row ID
account label only, never the email or token
redacted screenshot or accessibility snapshot path
visible Chinese anchors
whether the action was completed, cancelled, blocked, or skipped
cleanup proof
statement that no main account or production state was used
```

## Row Instructions

### GUI-AUTH-01

Required evidence:

```text
logged-out entry point is visible in Chinese
browser login is started from the isolated profile
auth callback returns to the app or failure fallback is visible in Chinese
account state after callback is redacted
```

Cleanup:

```text
log out of zh-rc19-test-account
remove only the disposable local test profile if cleanup is approved
```

### GUI-SET-03

Required evidence:

```text
Settings > AI opens under zh-rc19-test-account
Build plan, API key, custom inference, and model UI anchors are visible in Chinese
all account, token, key, endpoint URL, and team data is redacted
```

Cleanup:

```text
do not create an endpoint for this row unless GUI-WS-06 is also approved
log out of the isolated account after evidence capture
```

### GUI-WS-06

Required evidence:

```text
custom inference is enabled without debug fixture env
disposable endpoint is named zh-smoke-delete-endpoint
remove endpoint confirmation is visible in Chinese
cancel path is captured first
approved remove path captures cleanup proof
```

Cleanup:

```text
confirm zh-smoke-delete-endpoint is absent or restored by fixture reset
do not delete any endpoint with a different name
```

## Public-RC Promotion Rule

```text
these rows remain blocked until the runbook is executed with redacted evidence
fixture evidence alone cannot promote these rows
main-account evidence is invalid
```

