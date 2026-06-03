# zh-Hans Public-RC Evidence Intake RC32

Date: 2026-06-02

## Purpose

This document defines committable metadata for public-RC evidence. It does not
authorize using the user's main account, entering real credentials, buying
credits, consuming quota, creating production cloud objects, deleting production
objects, or committing raw screenshots.

## Ledger

```text
resources/localization/zh-Hans-public-rc-evidence.toml
```

## Linter

```bash
python3 script/zh_public_rc_evidence_lint.py
```

## Evidence Row Schema

```toml
[[evidence]]
row_id = "GUI-SET-05"
status = "provided"
evidence_paths = ["artifacts/redacted/gui-set-05.txt"]
cleanup_proof = "fixture reset proof captured"
redaction = "email, token, key, endpoint url, team id, and account identifiers removed"
notes = "uses zh-smoke-invalid-token only"
```

## Committable Metadata Rules

```text
row_id must match resources/localization/zh-Hans-public-rc-blockers.toml
status must be provided before a row can be promoted
evidence_paths must point under artifacts/redacted/
cleanup_proof must describe reset or cleanup proof
redaction must list removed sensitive fields
notes must not contain email addresses, URLs, tokens, cookies, API keys, secrets, endpoint URLs, team IDs, or account identifiers
```

## Public-RC Promotion Boundary

Rows remain blocked until the linter passes and the matching human evidence is
reviewed. Linter success proves metadata completeness only; it does not prove
that raw evidence is safe, true, or visually adequate.
