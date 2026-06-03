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

## Post-RC27 Prerequisite Package

Phase 190 keeps the isolated-account lane blocked because no concrete isolated
account package was available in the execution context.

Required package before execution:

```text
account label: zh-rc28-test-account or equivalent isolated label
local profile: zh-rc28-test-account
browser callback: available and testable
allowed surfaces: GUI-AUTH-01, GUI-SET-03, GUI-WS-06 only
custom inference: enabled only for disposable endpoint evidence
endpoint allowlist: zh-smoke-delete-endpoint only
redaction: email, account ID, token, API key, endpoint URL, team ID, cookies,
  magic links, and any other identifiers must be removed from committed evidence
cleanup proof: logout confirmation plus local profile cleanup or explicit
  profile-retention reason
```

Missing as of Phase 190:

```text
isolated account credential/callback proof
custom inference enabled state
disposable endpoint zh-smoke-delete-endpoint
cleanup proof plan tied to an actual account
explicit approval to run browser auth and endpoint removal
```

## RC32 Evidence Intake Gate

Before any isolated-account row can be promoted, `resources/localization/zh-Hans-public-rc-evidence.toml`
must contain a `status = "provided"` row for the matching blocker, the row must
pass `python3 script/zh_public_rc_evidence_lint.py`, and the raw evidence must
still be reviewed for redaction, row match, and cleanup proof.

Rows still requiring isolated-account evidence:

```text
GUI-AUTH-01
GUI-SET-03
GUI-WS-06
```

Disposable-object rows must additionally prove that only the exact allowlisted
object names were used:

```text
GUI-SET-06: zh-smoke-delete-environment
GUI-WS-04: zh-smoke-delete-secret
GUI-WS-07: zh-smoke-public-rc-team
```

## RC36 Filtered Action Packet Commands

Use these commands to request isolated-account evidence one row at a time:

```bash
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-AUTH-01
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-SET-03
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-WS-06
python3 script/zh_public_rc_evidence_report.py --missing-actions-json --category isolated_account
```

These commands do not create evidence. They print safe handoff metadata only.
Do not use the user's main account, and do not store account identifiers,
callback URLs, cookies, tokens, or magic links in repository files.

## RC37 Evidence Queue Commands

Use these commands to inspect isolated-account queue order before collecting
evidence:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category isolated_account
python3 script/zh_public_rc_evidence_queue.py --json --row-id GUI-AUTH-01
python3 script/zh_public_rc_evidence_queue.py --json --row-id GUI-SET-03
python3 script/zh_public_rc_evidence_queue.py --json --row-id GUI-WS-06
```

These commands do not create evidence. They print queue metadata only. Do not
use the user's main account, and do not store account identifiers, callback
URLs, cookies, tokens, or magic links in repository files.

## RC38 Candidate Preflight Commands

After raw evidence is reviewed and converted to a redacted text candidate
outside Git, run preflight before proposing any ledger update:

```bash
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-AUTH-01 --artifact /path/to/gui-auth-01-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-03 --artifact /path/to/gui-set-03-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-WS-06 --artifact /path/to/gui-ws-06-candidate.txt --markdown
```

These commands do not create evidence and do not clear blockers. Keep candidate
files outside Git until human redaction review approves a committed
`artifacts/redacted/<row-id>.txt` path.
