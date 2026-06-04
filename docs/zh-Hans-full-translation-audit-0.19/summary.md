# zh-Hans Full Translation Audit 0.19

Scope: Codex simulated per-entry review for every `[[replace]]` row in the zh-Hans override manifest.

- Manifest: `resources/localization/zh-Hans-overrides.toml`
- Entries reviewed: 7937
- Review mode: deterministic Codex simulation; this is not external human sign-off.

## Decision Counts

- blocked-public-rc: 1034
- simulated-accepted: 1772
- simulated-accepted-with-note: 5131

## Token Status Counts

- clean: 7936
- note: 1

## Source State Counts

- missing-in-current-source: 124
- target-and-source-present: 2908
- target-present: 4905

## Risk Tag Counts

- api-key-secret: 462
- auth-login: 119
- billing-quota: 483
- destructive-action: 223
- dynamic-placeholder: 1659
- english-preserved: 2193
- environment-endpoint: 776
- error-state: 355
- team-workspace: 1189
- terminal-command: 3172

## Public-RC Evidence Row Tags

- GUI-AUTH-01: 95
- GUI-BILL-01: 483
- GUI-BILL-02: 352
- GUI-CLOUD-01: 21
- GUI-SET-03: 3
- GUI-SET-04: 73
- GUI-SET-05: 73
- GUI-SET-06: 7
- GUI-WS-04: 462
- GUI-WS-06: 3
- GUI-WS-07: 5

## Actionable Review Rows

No `needs-copy-review` or `needs-functional-review` rows were produced.

## Artifacts

- `entries.tsv`: one row per manifest entry, intended for spreadsheet-style review.
- `entries.json`: same rows in machine-readable form.
- `summary.md`: this aggregate summary.
