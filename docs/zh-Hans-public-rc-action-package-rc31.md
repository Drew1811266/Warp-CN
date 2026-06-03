# zh-Hans Public-RC Action Package RC31

Date: 2026-06-02

## Required Inputs

| Category | Rows | Required input |
| --- | --- | --- |
| isolated account | GUI-AUTH-01, GUI-SET-03, GUI-WS-06 | An isolated test account that is not the user's main account, plus cleanup proof. |
| backend fixture | GUI-SET-04, GUI-SET-05, GUI-BILL-01, GUI-BILL-02, GUI-CLOUD-01 | Safe AWS/Bedrock, invalid credential, billing/quota, Build plan, and cloud capacity fixtures. |
| disposable object | GUI-SET-06, GUI-WS-04, GUI-WS-07 | Exact disposable objects named `zh-smoke-delete-environment`, `zh-smoke-delete-secret`, and `zh-smoke-public-rc-team`. |
| visual assets | onboarding PNG residue | Design/product approval for an asset-only branch and before/after contact sheets. |
| heavy validation | Rust/bundle/GUI | A quiet-window `decision: run-heavy-gate` from `script/zh_low_load_gate.py`. |

## Current Registry Summary

```text
total: 11
public_rc_required: 11
blocked-no-backend-fixture: 5
blocked-no-disposable-object: 3
blocked-no-isolated-account: 3
```

## Safety Rules

- Do not use the user's main account.
- Do not enter real provider credentials.
- Do not attach payment methods, buy credits, or consume real quota.
- Do not delete or transfer any object whose name is not explicitly allowlisted here.
- Do not submit raw screenshots, screen recordings, tokens, callback URLs, account identifiers, or private team names.

## Acceptance Boundary

Public-RC promotion requires matching evidence and cleanup proof for every row
whose status changes. Fixture-only evidence may support local confidence, but it
does not upgrade rows that require real isolated-account or disposable-object
evidence.

## RC32 Evidence Intake

Before changing any blocker status, record committable metadata in
`resources/localization/zh-Hans-public-rc-evidence.toml` and run:

```bash
python3 script/zh_public_rc_evidence_lint.py
```

The linter must pass, and the raw evidence must still be manually reviewed for
redaction and row match before a public-RC blocker can be cleared.
