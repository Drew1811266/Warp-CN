# zh-Hans Public-RC Isolated Account Execution

## Scope

This document covers the isolated account rows:

- `GUI-AUTH-01`
- `GUI-SET-03`
- `GUI-WS-06`

## Safety Rules

- Use only an isolated test account.
- Do not use the user's main account.
- Use no personal account.
- Do not store account identifiers, cookies, tokens, magic links, callback URLs, endpoint URLs, or private profile names in Git.
- Do not touch any real team, real secret, real environment, real endpoint, billing, or cloud capacity.

## Required Approval Packet

Preparation can continue only if the approval packet explicitly includes all of
these statements:

```text
isolated account is not the user's main account
login flow is approved for public-RC evidence capture
Settings > AI visibility is approved
custom inference endpoint test object is named zh-smoke-delete-endpoint
logout or profile cleanup proof format is defined
raw evidence review owner is named
redaction reviewer is named
```

The only public smoke object name allowed in this isolated-account lane is:

- `zh-smoke-delete-endpoint`

## Safety Boundary

Raw screenshots, recordings, callback URLs, endpoint URLs, cookies, tokens, API keys, account identifiers, private profile names, and private object names must stay outside Git.

## Evidence Commands

Use these commands to inspect the queue and the missing-action packet for the isolated account category:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category isolated_account
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category isolated_account
```

## Post-Approval Boundary

Candidate creation, candidate preflight, artifact promotion, ledger updates, GUI
login, and account cleanup proof are outside this readiness document. Run those
steps only from a separately approved evidence-execution workflow after the
isolated account approval packet, raw evidence reviewer, redaction reviewer, and
cleanup proof format are all confirmed.

## Completion Criteria

This lane is complete only when all three rows have reviewed redacted evidence, logout or profile cleanup proof where required, and strict artifact lint stops failing for isolated account rows.

## Notes

This document is execution guidance only. It does not provide evidence, use an account, or clear blockers.
