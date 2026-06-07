# zh-Hans Public-RC Independent Lanes Execution

Date: 2026-06-03

## Purpose

This document defines the work that can continue while backend fixture approval
is pending in [warpdotdev/warp#12129](https://github.com/warpdotdev/warp/issues/12129).
It is an execution guide for preparation, low-load verification, and release
documentation only. It does not provide evidence and does not clear public-RC
blockers.

## Current Baseline

```text
backend fixture approval: waiting on warpdotdev/warp#12129
public-RC blockers: 11
backend_fixture blockers: 5
isolated_account blockers: 3
disposable_object blockers: 3
ready evidence rows: 0
strict artifact lint: expected fail until reviewed evidence exists
```

Low-load localization state remains clean:

```text
manifest entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
release inventory: 8574 covered, 2 candidates, 100.0%
```

## Parallel Work Matrix

| Lane | Can proceed now | Must wait for |
| --- | --- | --- |
| Isolated account | Request isolated account approval, define cleanup proof, run queue/action packet commands | actual isolated account, login approval, reviewed raw evidence |
| Disposable object | Request allowlisted object approval, prepare cancel-first/delete/transfer proof format, run queue/action packet commands | exact disposable objects, explicit delete/transfer approval, reviewed raw evidence |
| Release notes | Draft current status, known blockers, evidence policy, no-go wording, version checklist | all evidence rows, heavy gate results, final version approval |
| Packaging check | Run low-load manifest/inventory/status checks, document heavy-gate commands and expected outputs | low-load gate, explicit approval for Rust compile, bundle, GUI launch |
| Translation rescan | Run manifest, glossary, dry-run, inventory, public-RC status, and unit evidence tests | only required if source drift or glossary errors appear |

## Isolated Account Lane

Rows:

- `GUI-AUTH-01`
- `GUI-SET-03`
- `GUI-WS-06`

Safe preparation commands:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category isolated_account
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category isolated_account
```

Required approval packet:

```text
isolated account is not the user's main account
login flow is approved for public-RC evidence capture
Settings > AI visibility is approved
custom inference endpoint test object is named zh-smoke-delete-endpoint
logout or profile cleanup proof format is defined
raw evidence review owner is named
redaction reviewer is named
```

Candidate creation, candidate preflight, artifact promotion, ledger updates, GUI
login, and account cleanup proof are outside this independent-lanes preparation
workflow. Run those steps only from a separately approved evidence-execution
workflow after the isolated account approval packet, raw evidence reviewer,
redaction reviewer, and cleanup proof format are all confirmed.

## Disposable Object Lane

Rows:

- `GUI-SET-06`
- `GUI-WS-04`
- `GUI-WS-07`

Allowlisted objects:

- `zh-smoke-delete-environment`
- `zh-smoke-delete-secret`
- `zh-smoke-public-rc-team`

Safe preparation commands:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category disposable_object
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category disposable_object
```

Required approval packet:

```text
object exists and is disposable
object name exactly matches the allowlist
cancel-first path is approved
delete or transfer path is explicitly approved
cleanup absence or restoration proof format is defined
raw evidence review owner is named
redaction reviewer is named
```

Candidate creation, candidate preflight, artifact promotion, ledger updates,
delete or transfer execution, and cleanup proof are outside this
independent-lanes preparation workflow. Run those steps only from a separately
approved evidence-execution workflow after exact allowlisted objects, explicit
delete or transfer approval, raw evidence reviewer, redaction reviewer, and
cleanup proof format are all confirmed.

## Release Notes Draft Lane

Create release notes only as a draft until all gates pass.

Draft sections:

```text
status: draft-only
version target: 0.19 unless changed by maintainer
scope: Simplified Chinese localization fork
not official Warp release: true
source overlay status: clean
public-RC evidence: incomplete
known blockers: backend_fixture 5, isolated_account 3, disposable_object 3
backend fixture request: warpdotdev/warp#12129
heavy gate: not yet run for formal release
publication: not approved
```

Do not create a tag, push, GitHub release, or claim public-RC readiness from this
draft.

## Packaging Check Lane

Low-load packaging preparation can verify scripts and current status without
building:

```bash
git status --short --branch
python3 script/privacy_guard.py --all-tracked
python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
```

Heavy packaging commands require low-load approval and explicit user approval:

```bash
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Do not run GUI launch or bundle packaging as part of documentation-only planning.

## Translation Rescan Lane

Run this lightweight rescan before any release-note or packaging checkpoint:

```bash
python3 script/zh_apply_localization.py --validate-manifest
python3 script/zh_apply_localization.py --check-glossary
python3 script/zh_apply_localization.py --metadata-summary
python3 script/zh_apply_localization.py --dry-run --summary
python3 script/zh_localization_inventory.py --preset release --coverage
python3 script/zh_public_rc_status.py
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
```

Expected current result:

```text
manifest validation passed
glossary check passed
would_change: 0
missing: 0
release coverage: 100.0%
public-RC blockers: 11
strict artifact lint: fail until 11 evidence rows exist
```

## No-Go

Do not do any of the following from this independent-lanes workflow:

- use the user's main account
- use any personal account
- store login callbacks, magic links, cookies, tokens, account identifiers, team
  IDs, billing IDs, endpoint URLs, or private object names in Git
- create, delete, transfer, or reset real objects
- touch any real team
- touch any real secret
- touch any real environment
- touch any real endpoint
- perform any real billing or cloud capacity mutation
- create candidate files before approval and raw-evidence review
- promote redacted artifacts before human review
- mark evidence rows as `provided` before strict artifact lint can pass
- run heavy build, GUI launch, tag, push, or release without explicit approval

Allowed public smoke object names only:

```text
zh-smoke-delete-environment
zh-smoke-delete-secret
zh-smoke-public-rc-team
zh-smoke-delete-endpoint
```

Real-object no-go checklist:

```text
no personal account
no real team
no real secret
no real environment
no real endpoint
no real billing or cloud capacity mutation
```
