# zh-Hans Public-RC Evidence Packet Template RC33

Date: 2026-06-02

## Purpose

This document defines how future public-RC evidence packets should be prepared
before any blocker status is promoted.

## Generate Packet TOML

```bash
python3 script/zh_public_rc_evidence_report.py --templates
```

## Required Review Order

```text
1. Capture raw evidence outside the repository.
2. Redact account identifiers, callback URLs, cookies, tokens, API keys,
   endpoint URLs, team IDs, billing IDs, and private object names.
3. Convert the reviewed artifact to redacted text under artifacts/redacted/*.txt
   only after explicit approval.
4. Add the matching [[evidence]] block to resources/localization/zh-Hans-public-rc-evidence.toml.
5. Run python3 script/zh_public_rc_evidence_lint.py --strict-artifacts.
6. Manually review the raw evidence and the redacted artifact before changing
   any blocker status.
```

## Current Boundary

```text
ready rows: 0
blockers cleared by this document: 0
real evidence artifacts created by this document: none
```
