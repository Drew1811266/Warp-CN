# zh-Hans Localization Phase 111

Date: 2026-06-02

## Scope

Phase 111 converted the RC19 public-RC blocker list into a machine-readable
registry. It did not run GUI, compile, bundle, PNG generation, account login,
backend, billing, cloud, managed-secret, endpoint, or team operations.

## Registry

```text
registry path: resources/localization/zh-Hans-public-rc-blockers.toml
source RC document: docs/zh-Hans-release-candidate-2026-06-02-rc19.md
```

Required schema keys per entry:

```text
id
category
status
reason
required_evidence
handoff_doc
safety_rule
public_rc_required
local_fixture_allowed
```

## Blocker Counts

```text
total: 11
```

Status counts:

```text
blocked-no-isolated-account: 3
blocked-no-backend-fixture: 5
blocked-no-disposable-object: 3
```

Category counts:

```text
isolated_account: 3
backend_fixture: 5
disposable_object: 3
```

## Handoff Docs Referenced

```text
docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md
docs/zh-Hans-backend-fixture-contract-rc19.md
```

## Safety Boundary

The registry records why rows are blocked and what evidence is required. It
does not clear any blocker and does not authorize use of the user's main
account, real backend state, real billing/quota, cloud resources, managed
secrets, custom endpoints, or team ownership changes.

## Lightweight Review

Registry parse check with `script/zh_public_rc_status.py` compatible parsing
logic for the local Python 3.9 runtime:

```text
total 11
ids ['GUI-AUTH-01', 'GUI-BILL-01', 'GUI-BILL-02', 'GUI-CLOUD-01', 'GUI-SET-03', 'GUI-SET-04', 'GUI-SET-05', 'GUI-SET-06', 'GUI-WS-04', 'GUI-WS-06', 'GUI-WS-07']
status {'blocked-no-isolated-account': 3, 'blocked-no-backend-fixture': 5, 'blocked-no-disposable-object': 3}
category {'isolated_account': 3, 'backend_fixture': 5, 'disposable_object': 3}
```

## Qualification Review

```text
phase: 111
status: qualified
registry exists: yes
all 11 RC19 public-RC blockers represented: yes
required keys present by construction: yes
handoff docs exist: yes
external operations run: none
```
