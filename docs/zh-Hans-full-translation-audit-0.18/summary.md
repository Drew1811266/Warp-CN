# zh-Hans Full Translation Audit 0.18

Scope: Codex simulated per-entry review for every `[[replace]]` row in the zh-Hans override manifest.

- Manifest: `resources/localization/zh-Hans-overrides.toml`
- Entries reviewed: 7943
- Review mode: deterministic Codex simulation; this is not external human sign-off.

## Decision Counts

- blocked-public-rc: 1030
- simulated-accepted: 1774
- simulated-accepted-with-note: 5139

## Token Status Counts

- clean: 7942
- note: 1

## Source State Counts

- missing-in-current-source: 130
- target-and-source-present: 2923
- target-present: 4890

## Risk Tag Counts

- api-key-secret: 459
- auth-login: 119
- billing-quota: 482
- destructive-action: 221
- dynamic-placeholder: 1662
- english-preserved: 2226
- environment-endpoint: 787
- error-state: 353
- team-workspace: 1179
- terminal-command: 3187

## Public-RC Evidence Row Tags

- GUI-AUTH-01: 95
- GUI-BILL-01: 482
- GUI-BILL-02: 351
- GUI-CLOUD-01: 21
- GUI-SET-03: 3
- GUI-SET-04: 73
- GUI-SET-05: 73
- GUI-SET-06: 7
- GUI-WS-04: 459
- GUI-WS-06: 3
- GUI-WS-07: 5

## Actionable Review Rows

No `needs-copy-review` or `needs-functional-review` rows were produced.

## Artifacts

- `entries.tsv`: one row per manifest entry, intended for spreadsheet-style review.
- `entries.json`: same rows in machine-readable form.
- `summary.md`: this aggregate summary.
