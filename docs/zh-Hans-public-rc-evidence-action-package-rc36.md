# zh-Hans Public-RC Evidence Action Package RC36

Date: 2026-06-02

## Purpose

RC36 adds filtered missing-evidence action packets. These packets let an operator
request one row or one category at a time without exposing raw evidence and
without changing the evidence ledger.

## Commands

```bash
python3 script/zh_public_rc_evidence_report.py --missing-actions --row-id GUI-SET-05
python3 script/zh_public_rc_evidence_report.py --missing-actions-json --row-id GUI-SET-05
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-SET-05
python3 script/zh_public_rc_evidence_report.py --missing-actions --category backend_fixture
python3 script/zh_public_rc_evidence_report.py --missing-actions-json --category backend_fixture
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category backend_fixture
```

## Row Filters

```text
--row-id GUI-AUTH-01
--row-id GUI-SET-03
--row-id GUI-SET-04
--row-id GUI-SET-05
--row-id GUI-SET-06
--row-id GUI-WS-04
--row-id GUI-WS-06
--row-id GUI-WS-07
--row-id GUI-BILL-01
--row-id GUI-BILL-02
--row-id GUI-CLOUD-01
```

## Category Filters

```text
--category isolated_account
--category backend_fixture
--category disposable_object
```

## Safety Boundary

```text
filtered packets are handoff metadata only
raw evidence stays outside Git
redacted artifact text requires explicit approval before adding to artifacts/redacted/
ledger promotion requires reviewed raw evidence and strict artifact lint pass
blocker promotion requires accepted evidence row and explicit approval
```

## RC36 Status

```text
public-RC rows tracked: 11
ready rows: 0
filtered packet output: available
decision: blocked
```
