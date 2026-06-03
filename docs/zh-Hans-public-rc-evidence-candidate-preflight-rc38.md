# zh-Hans Public-RC Evidence Candidate Preflight RC38

Date: 2026-06-03

## Purpose

RC38 adds an offline preflight step for reviewed redacted public-RC evidence
candidate text files. The preflight helps reject unsafe or incomplete candidate
artifacts before anyone edits `resources/localization/zh-Hans-public-rc-evidence.toml`.

The preflight does not collect evidence, does not review raw screenshots, does
not update the ledger, and does not clear blockers.

## Candidate File Format

```text
row_id: GUI-SET-05
profile: zh-rc38-fixture-profile
visible_anchors:
- 设置
- AI
- AWS Bedrock
- 无效凭据
redaction: account identifiers, callback URLs, endpoint URLs, tokens, cookies, API keys, and secrets removed
cleanup_proof: fixture reset proof captured and no production state was touched
safety_confirmation: no main account, real credential, billing state, cloud capacity, team ownership, or production object was used
artifact_kind: redacted-text
```

Disposable-object rows must include the exact allowlisted object name:

```text
GUI-SET-06 object_name: zh-smoke-delete-environment
GUI-WS-04 object_name: zh-smoke-delete-secret
GUI-WS-07 object_name: zh-smoke-public-rc-team
```

## Commands

```bash
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-05 --artifact /path/to/redacted-candidate.txt
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-05 --artifact /path/to/redacted-candidate.txt --json
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-05 --artifact /path/to/redacted-candidate.txt --markdown
```

## Decision Semantics

```text
candidate-ready-for-human-review: candidate text passed machine preflight only
candidate-rejected: candidate text is unsafe, incomplete, mismatched, or not row-specific
```

## Safety Boundary

```text
raw evidence stays outside Git
candidate text must not contain emails, callback URLs, endpoint URLs, tokens,
cookies, API keys, secret values, team IDs, billing IDs, or private object names
candidate-ready-for-human-review does not update the ledger
ledger promotion requires human review, approved redaction, cleanup proof, and strict artifact lint
```
