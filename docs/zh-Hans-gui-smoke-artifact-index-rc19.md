# zh-Hans GUI Smoke Artifact Index RC19

Date: 2026-06-02

## Purpose

This tracked index preserves the reviewable summary of local GUI smoke artifact
notes that live under `docs/gui-smoke-artifacts/`. That directory is ignored by
`.gitignore`, so release evidence that must survive in version control needs to
be summarized in tracked Markdown outside the ignored tree.

## Artifact Policy

```text
docs/gui-smoke-artifacts/* is ignored by .gitignore
raw screenshots and recordings remain local-only by default
raw media must not be force-added unless it is cropped, redacted, reviewed, and
explicitly approved
important release facts must be duplicated or summarized in tracked docs
```

No ignored artifact was force-added for RC19 planning.

## Local README Inventory

The following ignored local README files were present during Phase 103:

```text
docs/gui-smoke-artifacts/phase100/README.md
docs/gui-smoke-artifacts/phase101/README.md
docs/gui-smoke-artifacts/phase76/README.md
docs/gui-smoke-artifacts/phase88/README.md
docs/gui-smoke-artifacts/phase89/README.md
docs/gui-smoke-artifacts/phase90/README.md
docs/gui-smoke-artifacts/phase91/README.md
docs/gui-smoke-artifacts/phase96/README.md
docs/gui-smoke-artifacts/phase97/README.md
docs/gui-smoke-artifacts/phase98/README.md
docs/gui-smoke-artifacts/phase99/README.md
```

RC19 summarizes the Phase 96 through Phase 101 local README records because
those were created in the RC18 post-run and directly affect the RC19 evidence
handoff.

## Phase 96 Summary

Phase 96 was a heat-safe low-risk GUI smoke defer. Warp was not launched, no
bundle was built, no screenshots were produced, and no account, backend,
billing, cloud, team, managed-secret, endpoint, or production state was touched.

Safe future rerun rows:

```text
GUI-BASE-01
GUI-BASE-02
GUI-BASE-03
GUI-BASE-04
GUI-BASE-05
GUI-ONB-01
GUI-ONB-02
GUI-AUTH-03
GUI-SET-01
GUI-SET-02
GUI-WS-08
```

Rows excluded from low-risk smoke remain blocked because they require isolated
account, backend fixture, disposable object, billing/quota state, cloud/team
state, managed secret, custom endpoint, or similar external state.

## Phase 97 Summary

Phase 97 classified non-public fixture feasibility without launching GUI,
building a bundle, creating fixtures, using accounts, touching backend state,
or triggering administrator prompts.

```text
GUI-AUTH-02: needs-visible-gui-only
GUI-AGENT-01: needs-visible-gui-only
GUI-AGENT-02: needs-small-debug-fixture
GUI-AGENT-03: needs-small-debug-fixture
GUI-AGENT-04: needs-small-debug-fixture for local web/stream errors only
GUI-AGENT-05: needs-small-debug-fixture
GUI-WS-02: needs-small-debug-fixture
GUI-WS-03: needs-small-debug-fixture
GUI-WS-05: unsafe-for-local-fixture
```

Fixture evidence from these rows can support local confidence only. It cannot
promote public-RC status for rows whose real path requires account, backend,
billing, cloud, team, managed secret, endpoint, or production state.

## Phase 98 Summary

Phase 98 defined the isolated account handoff for public-RC rows. No account was
created, logged into, refreshed, inspected, or mutated.

```text
account label: zh-rc18-test-account
rows: GUI-AUTH-01, GUI-SET-03, GUI-WS-06
status: account not created or used
```

Evidence requirements include a fresh or isolated profile, redacted screenshots
or accessibility snapshots, cleanup proof for `zh-smoke-delete-endpoint`, and
an explicit statement that no main account or production state was used.

## Phase 99 Summary

Phase 99 defined backend and disposable object fixture requirements. No backend
service was contacted, no test data was created, and no billing/quota, cloud,
managed-secret, endpoint, or team state was modified.

```text
zh-rc18-aws-fixture
zh-rc18-billing-cloud-fixture
zh-smoke-invalid-token
zh-smoke-delete-environment
zh-smoke-delete-secret
zh-smoke-public-rc-team
```

The fixture handoff covers `GUI-SET-04`, `GUI-SET-05`, `GUI-SET-06`,
`GUI-WS-04`, `GUI-WS-07`, `GUI-BILL-01`, `GUI-BILL-02`, and `GUI-CLOUD-01`.

## Phase 100 Summary

Phase 100 prepared asset-only branch readiness without modifying or generating
image assets.

```text
current branch at the time: codex/zh-Hans-followup-localization
required future asset branch: codex/zh-Hans-onboarding-assets-rc18
PNG diff: none
asset generation approved: no
```

Future asset work requires a clean asset-only branch, design approval, before
and after contact sheets outside the repository, binary scope proof, and visual
QA.

## Phase 101 Summary

Phase 101 checked whether PNG regeneration could run and recorded a blocker.
No PNG was generated, modified, or contact-sheeted.

```text
result: blocked-no-clean-asset-branch-or-approval
current branch at the time: codex/zh-Hans-followup-localization
current PNG diff: none
design/product approval recorded: no
before contact sheet present: no
```

The future batch order remains:

```text
Batch A: welcome screens
Batch B: notification and CLI Agent toolbar screens
Batch C: Agent intention customization screens
Batch D: Agent intention theme previews
Batch E: Terminal intention customization screens
Batch F: Terminal intention theme previews
Batch G: remaining script rows
```

## RC19 Evidence Rule

RC19 may reference this index as tracked evidence for what the ignored local
artifact records contained. It may not treat ignored raw media as public-RC
evidence unless that media is separately reviewed, redacted, approved, and
intentionally added.

## Phase 105 Summary

Phase 105 was the RC19 low-risk GUI smoke decision. It did not create a local
artifact directory, launch GUI, build a bundle, capture screenshots, capture
accessibility snapshots, or touch account/backend/billing/cloud/team/secret or
endpoint state.

```text
result: qualified-with-heat-safety-gui-defer
safe rows carried forward: GUI-BASE-01, GUI-BASE-02, GUI-BASE-03, GUI-BASE-04,
GUI-BASE-05, GUI-ONB-01, GUI-ONB-02, GUI-AUTH-03, GUI-SET-01, GUI-SET-02,
GUI-WS-08
public-RC rows promoted: none
```
