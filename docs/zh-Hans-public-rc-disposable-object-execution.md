# zh-Hans Public-RC Disposable Object Execution

## Scope

This document covers the disposable object rows:

- `GUI-SET-06`
- `GUI-WS-04`
- `GUI-WS-07`

The allowlisted disposable object names for this lane are:

- `zh-smoke-delete-environment`
- `zh-smoke-delete-secret`
- `zh-smoke-public-rc-team`

## Safety Rules

- Cancel first before any destructive path.
- Delete, transfer, or mutate only the exact allowlisted disposable objects after explicit approval.
- Use no personal account.
- Touch no real team, no real secret, no real environment, no real endpoint, and perform no real billing or cloud capacity mutation.

## Required Approval Packet

Preparation can continue only if the approval packet explicitly includes all of
these statements:

```text
object exists and is disposable
object name exactly matches the allowlist
cancel-first path is approved
delete or transfer path is explicitly approved
cleanup absence or restoration proof format is defined
raw evidence review owner is named
redaction reviewer is named
```

## Safety Boundary

Raw screenshots, recordings, callback URLs, endpoint URLs, cookies, tokens, API keys, account identifiers, team IDs, private object names, and cleanup-private identifiers must stay outside Git.

## Evidence Commands

Use these commands to inspect the queue and the missing-action packet for the disposable object category:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category disposable_object
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category disposable_object
```

## Post-Approval Boundary

Candidate creation, candidate preflight, artifact promotion, ledger updates,
delete or transfer execution, and cleanup proof are outside this readiness
document. Run those steps only from a separately approved evidence-execution
workflow after exact allowlisted objects, explicit delete or transfer approval,
raw evidence reviewer, redaction reviewer, and cleanup proof format are all
confirmed.

## Completion Criteria

This lane is complete only when each row has reviewed redacted evidence, cancel-path proof where relevant, explicit delete/transfer approval where relevant, cleanup absence/restoration proof, and strict artifact lint stops failing for disposable object rows.

## Notes

This document is execution guidance only. It does not provide evidence, approve deletion or transfer, create objects, mutate objects, or clear blockers.
