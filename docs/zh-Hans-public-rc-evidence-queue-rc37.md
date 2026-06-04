# zh-Hans Public-RC Evidence Queue RC37

Date: 2026-06-02

## Purpose

RC37 adds prioritized public-RC evidence queue output. The queue helps operators
choose safe evidence work by row, category, risk, priority, and approval gate.

The queue is planning metadata only. It does not provide evidence, does not
change `resources/localization/zh-Hans-public-rc-evidence.toml`, and does not
clear blockers.

## Commands

```bash
python3 script/zh_public_rc_evidence_queue.py
python3 script/zh_public_rc_evidence_queue.py --json
python3 script/zh_public_rc_evidence_queue.py --markdown
python3 script/zh_public_rc_evidence_queue.py --json --row-id GUI-SET-05
python3 script/zh_public_rc_evidence_queue.py --markdown --category backend_fixture
python3 script/zh_public_rc_evidence_queue.py --markdown --category isolated_account
python3 script/zh_public_rc_evidence_queue.py --markdown --category disposable_object
```

## Queue Semantics

```text
priority 10-19: backend fixture lane
priority 20-29: isolated account lane
priority 30-39: disposable object lane
approval_gate fixture-owner-approval: requires fixture owner and reset proof
approval_gate isolated-account-approval: requires isolated account and cleanup proof
approval_gate disposable-object-approval: requires explicit object mutation approval
```

## Current Queue

```text
total_rows: 11
backend_fixture: 5
isolated_account: 3
disposable_object: 3
ready rows: 0
decision: blocked-until-queue-cleared
```

## Safety Boundary

```text
raw evidence stays outside Git
redacted artifact text requires explicit approval before adding to artifacts/redacted/
ledger promotion requires reviewed raw evidence and strict artifact lint pass
blocker promotion requires accepted evidence row and explicit approval
queue output alone cannot promote any row
```
