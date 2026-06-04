# zh-Hans Backend Fixture Contract RC19

Date: 2026-06-02

## Scope

This contract defines the backend and disposable object fixtures required for
public-RC zh-Hans GUI evidence. It is a handoff document only and does not
contact backend services or create test data.

## Fixture Names

```text
zh-rc19-aws-fixture
zh-rc19-billing-cloud-fixture
zh-smoke-invalid-token
zh-smoke-delete-environment
zh-smoke-delete-secret
zh-smoke-public-rc-team
```

## Row Mapping

| Row | Fixture | Evidence Target |
| --- | --- | --- |
| `GUI-SET-04` | `zh-rc19-aws-fixture` | Disposable AWS/Bedrock settings copy without real credentials. |
| `GUI-SET-05` | `zh-smoke-invalid-token` | Invalid Bedrock credential state and user-facing error copy. |
| `GUI-SET-06` | `zh-smoke-delete-environment` | Environment delete confirmation and cleanup proof. |
| `GUI-WS-04` | `zh-smoke-delete-secret` | Managed auth secret delete confirmation and cleanup proof. |
| `GUI-WS-07` | `zh-smoke-public-rc-team` | Team ownership transfer confirmation on a disposable owner test team only. |
| `GUI-BILL-01` | `zh-rc19-billing-cloud-fixture` | Out-of-credits or monthly-limit copy without purchase or quota consumption. |
| `GUI-BILL-02` | `zh-rc19-billing-cloud-fixture` | Build plan migration modal with safe backend test team state. |
| `GUI-CLOUD-01` | `zh-rc19-billing-cloud-fixture` | Controlled cloud capacity/quota modal state. |

## Fixture Safety Requirements

Every fixture must provide:

```text
fixture owner
reset procedure
allowed mutations
cleanup procedure
redaction requirements
expected evidence
expiration or teardown date
statement that no production object is affected
```

## Row-Specific Cleanup Proof

```text
GUI-SET-04:
  AWS/Bedrock fixture never uses real credentials.
  Cleanup proves any local disposable profile/config is removed or reset.

GUI-SET-05:
  Invalid token marker is zh-smoke-invalid-token or equivalent safe test value.
  Cleanup proves invalid fixture state is reset.

GUI-SET-06:
  Deleted environment is named exactly zh-smoke-delete-environment.
  Cleanup proves the environment is absent or restored by fixture reset.

GUI-WS-04:
  Deleted managed secret is named exactly zh-smoke-delete-secret.
  Cleanup proves the secret is absent or restored by fixture reset.

GUI-WS-07:
  Ownership transfer is approved only on zh-smoke-public-rc-team.
  Cleanup proves ownership is restored or the disposable team is deleted.

GUI-BILL-01:
  Fixture never purchases credits or consumes real quota.
  Cleanup proves billing/quota state is reset.

GUI-BILL-02:
  Build-plan migration state is backend test state only.
  Cleanup proves sunset/migration flags are reset.

GUI-CLOUD-01:
  Capacity/quota state is controlled fixture state only.
  Cleanup proves backend fixture state is reset.
```

## Prohibited Evidence

```text
real AWS credentials
real payment method or billing ID
real credit purchase
real quota consumption
production cloud environment
production managed secret
production team ownership transfer
unredacted account, team, endpoint, token, key, or secret data
```

## Public-RC Promotion Rule

Rows covered by this contract remain blocked until the fixture owner provides
redacted evidence and cleanup proof. Source inspection or local debug fixture
evidence alone cannot promote these rows to public-RC verified.

## Post-RC27 Fixture Readiness Audit

Phase 192 keeps the backend fixture lane blocked because no concrete fixture
owner or executable reset package was available in the execution context.

Required fixture package before execution:

```text
fixture owner
allowed mutations
reset command or reset procedure
cleanup proof format
redaction requirements
expiration or teardown date
statement that no production object is affected
```

Rows still missing executable fixture packages:

```text
GUI-SET-04: disposable AWS/Bedrock fixture without real credentials
GUI-SET-05: invalid Bedrock credential fixture
GUI-BILL-01: safe quota or billing fixture with no purchase/quota consumption
GUI-BILL-02: backend test team with Build-plan migration state
GUI-CLOUD-01: controlled capacity or quota fixture
```

Disposable-object rows are also not executable until exact object existence and
cleanup proof are provided:

```text
GUI-SET-06: zh-smoke-delete-environment
GUI-WS-04: zh-smoke-delete-secret
GUI-WS-07: zh-smoke-public-rc-team
```

## RC32 Evidence Intake Gate

Before any backend fixture row can be promoted, `resources/localization/zh-Hans-public-rc-evidence.toml`
must contain a `status = "provided"` row for the matching blocker, the row must
pass `python3 script/zh_public_rc_evidence_lint.py`, and the raw fixture evidence
must still be reviewed for redaction, row match, and cleanup proof.

Rows still requiring backend fixture evidence:

```text
GUI-SET-04
GUI-SET-05
GUI-BILL-01
GUI-BILL-02
GUI-CLOUD-01
```

## RC36 Filtered Action Packet Commands

Use these commands to request backend-fixture and disposable-object evidence by
category:

```bash
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category backend_fixture
python3 script/zh_public_rc_evidence_report.py --missing-actions-json --category backend_fixture
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category disposable_object
python3 script/zh_public_rc_evidence_report.py --missing-actions-json --category disposable_object
```

Use these commands to request high-risk rows one at a time:

```bash
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-SET-06
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-WS-04
python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --row-id GUI-WS-07
```

These commands do not create evidence. They print safe handoff metadata only.
Do not attach payment methods, use real credentials, mutate production teams,
delete real objects, or consume cloud capacity while collecting evidence.

## RC37 Evidence Queue Commands

Use these commands to inspect backend-fixture and disposable-object queue order
before collecting evidence:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category backend_fixture
python3 script/zh_public_rc_evidence_queue.py --json --category backend_fixture
python3 script/zh_public_rc_evidence_queue.py --markdown --category disposable_object
python3 script/zh_public_rc_evidence_queue.py --json --category disposable_object
```

Use these commands to inspect high-risk disposable rows one at a time:

```bash
python3 script/zh_public_rc_evidence_queue.py --json --row-id GUI-SET-06
python3 script/zh_public_rc_evidence_queue.py --json --row-id GUI-WS-04
python3 script/zh_public_rc_evidence_queue.py --json --row-id GUI-WS-07
```

These commands do not create evidence. They print queue metadata only. Do not
attach payment methods, use real credentials, mutate production teams, delete
real objects, or consume cloud capacity while collecting evidence.

## RC38 Candidate Preflight Commands

After raw fixture or disposable-object evidence is reviewed and converted to a
redacted text candidate outside Git, run preflight before proposing any ledger
update:

```bash
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-04 --artifact /path/to/gui-set-04-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-05 --artifact /path/to/gui-set-05-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-BILL-01 --artifact /path/to/gui-bill-01-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-BILL-02 --artifact /path/to/gui-bill-02-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-CLOUD-01 --artifact /path/to/gui-cloud-01-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-06 --artifact /path/to/gui-set-06-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-WS-04 --artifact /path/to/gui-ws-04-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-WS-07 --artifact /path/to/gui-ws-07-candidate.txt --markdown
```

Disposable-object candidate files must include the exact allowlisted
`object_name`. These commands do not mutate fixtures, do not create evidence,
and do not clear blockers.
