# zh-Hans Public-RC Backend Fixture Execution

## Scope

This document covers the backend fixture rows:

- `GUI-BILL-01`
- `GUI-BILL-02`
- `GUI-CLOUD-01`
- `GUI-SET-04`
- `GUI-SET-05`

## Safety Rules

- Do not buy credits.
- Do not attach payment methods.
- Do not expose billing IDs.
- Do not consume real quota.
- Do not use real AWS credentials.
- Do not enter real provider credentials.

## Safety Boundary

Raw screenshots, recordings, callback URLs, endpoint URLs, cookies, tokens, API keys, account identifiers, team IDs, billing IDs, and private object names must stay outside Git.

## Evidence Commands

Use these commands to inspect the queue and the missing-action packet for the backend fixture category:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category backend_fixture
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category backend_fixture
```

## Candidate Preflight

Use the helper to read an existing reviewed redacted candidate text file from a temporary out-of-Git path. Do not treat the helper as permission to create in-repo artifacts before explicit approval.

```bash
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-BILL-01 --artifact /tmp/gui-bill-01-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-BILL-02 --artifact /tmp/gui-bill-02-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-CLOUD-01 --artifact /tmp/gui-cloud-01-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-04 --artifact /tmp/gui-set-04-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-05 --artifact /tmp/gui-set-05-candidate.txt --markdown
```

Final approved destinations after explicit approval:

- `artifacts/redacted/gui-bill-01.txt`
- `artifacts/redacted/gui-bill-02.txt`
- `artifacts/redacted/gui-cloud-01.txt`
- `artifacts/redacted/gui-set-04.txt`
- `artifacts/redacted/gui-set-05.txt`

## Completion Criteria

This lane is complete only when all five rows have reviewed redacted evidence and strict artifact lint stops failing for backend fixture rows.

## Notes

This document is execution guidance only. It does not provide evidence or clear blockers.
