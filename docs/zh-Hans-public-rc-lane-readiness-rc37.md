# zh-Hans Public-RC Lane Readiness RC37

Date: 2026-06-02

## Current Lane Status

```text
backend_fixture: total=5 ready=0 missing=5 queue=5
disposable_object: total=3 ready=0 missing=3 queue=3
isolated_account: total=3 ready=0 missing=3 queue=3
asset lane: blocked-no-asset-approval
heavy validation lane: pending-low-load-gate
GUI lane: blocked-no-explicit-gui-smoke-approval
publication lane: blocked-no-explicit-approval
```

## RC37 Queue Outputs

```text
full text queue: python3 script/zh_public_rc_evidence_queue.py
full JSON queue: python3 script/zh_public_rc_evidence_queue.py --json
row JSON queue: python3 script/zh_public_rc_evidence_queue.py --json --row-id GUI-SET-05
category Markdown queue: python3 script/zh_public_rc_evidence_queue.py --markdown --category backend_fixture
```

## Promotion Rule

No lane can promote a row unless the matching evidence row is `status = "provided"`,
the expected row-specific artifact path exists, strict artifact lint passes, raw
evidence has been manually reviewed for safety and row match, and the user has
explicitly approved the promotion.
