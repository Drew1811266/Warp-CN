# zh-Hans Public-RC Evidence Automation RC35

Date: 2026-06-02

## Purpose

This document records the RC35 evidence automation outputs. It does not provide
real evidence and does not clear blockers.

## Commands

```bash
python3 script/zh_public_rc_evidence_report.py
python3 script/zh_public_rc_evidence_report.py --json
python3 script/zh_public_rc_evidence_report.py --missing-actions
python3 script/zh_public_rc_evidence_report.py --missing-actions-json
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
```

## Current Summary

```text
public-RC rows tracked: 11
ready rows: 0
missing action rows: 11
decision: blocked
strict lint: expected fail until real evidence exists
```

## JSON Output Use

```text
--json: use for dashboards and release readiness summaries
--missing-actions-json: use for row-owner handoff and evidence packet generation
```

## Safety Boundary

```text
raw evidence stays outside Git
redacted artifacts under artifacts/redacted/*.txt require explicit approval
ledger promotion requires strict lint pass and manual raw evidence review
blocker registry promotion requires accepted evidence row and reviewed raw evidence
```
