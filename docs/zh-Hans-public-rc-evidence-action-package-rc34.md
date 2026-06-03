# zh-Hans Public-RC Evidence Action Package RC34

Date: 2026-06-02

## Purpose

This action package converts the RC33 evidence packet template into row-level
owner actions. It does not provide evidence and does not clear blockers.

## Generate Current Actions

```bash
python3 script/zh_public_rc_evidence_report.py --missing-actions
```

## Current Required Rows

```text
GUI-AUTH-01: isolated_account, artifacts/redacted/gui-auth-01.txt
GUI-SET-03: isolated_account, artifacts/redacted/gui-set-03.txt
GUI-SET-04: backend_fixture, artifacts/redacted/gui-set-04.txt
GUI-SET-05: backend_fixture, artifacts/redacted/gui-set-05.txt
GUI-SET-06: disposable_object, artifacts/redacted/gui-set-06.txt
GUI-WS-04: disposable_object, artifacts/redacted/gui-ws-04.txt
GUI-WS-06: isolated_account, artifacts/redacted/gui-ws-06.txt
GUI-WS-07: disposable_object, artifacts/redacted/gui-ws-07.txt
GUI-BILL-01: backend_fixture, artifacts/redacted/gui-bill-01.txt
GUI-BILL-02: backend_fixture, artifacts/redacted/gui-bill-02.txt
GUI-CLOUD-01: backend_fixture, artifacts/redacted/gui-cloud-01.txt
```

## Promotion Rule

```text
1. Raw evidence is captured outside Git.
2. Raw evidence is manually reviewed for row match and safety.
3. Redacted text is created under artifacts/redacted/*.txt only after explicit approval.
4. The matching [[evidence]] row is changed to status = "provided".
5. python3 script/zh_public_rc_evidence_lint.py --strict-artifacts passes.
6. The blocker registry is updated only after the evidence row and raw evidence review are accepted.
```

## Current Boundary

```text
ready rows: 0
rows promoted by this package: 0
real evidence artifacts created by this package: none
public RC: not ready
```
