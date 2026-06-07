zh-Hans public-RC missing evidence actions
Only use these rows after external evidence has been captured, redacted, and approved.

row_id: GUI-AUTH-01
category: isolated_account
status: missing
handoff_doc: docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md
artifact_path: artifacts/redacted/gui-auth-01.txt
required_evidence:
- isolated browser-login test account
- redacted login and callback GUI evidence
- logout or profile cleanup proof
safety_rule: Do not use the user's main account or store account identifiers, cookies, tokens, or magic links in evidence.

row_id: GUI-BILL-01
category: backend_fixture
status: missing
handoff_doc: docs/zh-Hans-backend-fixture-contract-rc19.md
artifact_path: artifacts/redacted/gui-bill-01.txt
required_evidence:
- safe quota or billing fixture
- redacted billing GUI evidence
- fixture reset proof
safety_rule: Do not buy credits, attach payment methods, expose billing IDs, or consume real quota.

row_id: GUI-BILL-02
category: backend_fixture
status: missing
handoff_doc: docs/zh-Hans-backend-fixture-contract-rc19.md
artifact_path: artifacts/redacted/gui-bill-02.txt
required_evidence:
- backend test team with build-plan migration state
- redacted modal GUI evidence
- backend flag reset proof
safety_rule: Use backend test state only; do not mutate production team or billing state.

row_id: GUI-CLOUD-01
category: backend_fixture
status: missing
handoff_doc: docs/zh-Hans-backend-fixture-contract-rc19.md
artifact_path: artifacts/redacted/gui-cloud-01.txt
required_evidence:
- controlled capacity or quota fixture
- redacted cloud capacity GUI evidence
- fixture reset proof
safety_rule: Do not create, delete, or exhaust production cloud capacity; use controlled fixture state only.

row_id: GUI-SET-03
category: isolated_account
status: missing
handoff_doc: docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md
artifact_path: artifacts/redacted/gui-set-03.txt
required_evidence:
- isolated account with AI settings visible
- redacted Settings > AI GUI evidence
- logout or profile cleanup proof
safety_rule: Inspect only; do not create real endpoints, API keys, or account state while collecting this evidence.

row_id: GUI-SET-04
category: backend_fixture
status: missing
handoff_doc: docs/zh-Hans-backend-fixture-contract-rc19.md
artifact_path: artifacts/redacted/gui-set-04.txt
required_evidence:
- disposable AWS or Bedrock fixture
- redacted settings GUI evidence
- fixture reset proof
safety_rule: Never use real AWS credentials or expose profile names that identify a real account.

row_id: GUI-SET-05
category: backend_fixture
status: missing
handoff_doc: docs/zh-Hans-backend-fixture-contract-rc19.md
artifact_path: artifacts/redacted/gui-set-05.txt
required_evidence:
- invalid credential fixture
- redacted error GUI evidence
- fixture reset proof
safety_rule: Use only safe invalid marker values; do not enter real API keys or provider credentials.

row_id: GUI-SET-06
category: disposable_object
status: missing
handoff_doc: docs/zh-Hans-backend-fixture-contract-rc19.md
artifact_path: artifacts/redacted/gui-set-06.txt
required_evidence:
- disposable environment named zh-smoke-delete-environment
- redacted confirmation GUI evidence
- cleanup proof that the environment is absent or restored
safety_rule: Cancel first and delete only the exact disposable environment after explicit approval.

row_id: GUI-WS-04
category: disposable_object
status: missing
handoff_doc: docs/zh-Hans-backend-fixture-contract-rc19.md
artifact_path: artifacts/redacted/gui-ws-04.txt
required_evidence:
- disposable secret named zh-smoke-delete-secret
- redacted confirmation GUI evidence
- cleanup proof that the secret is absent or restored
safety_rule: Cancel first and delete only the exact disposable secret after explicit approval.

row_id: GUI-WS-06
category: isolated_account
status: missing
handoff_doc: docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md
artifact_path: artifacts/redacted/gui-ws-06.txt
required_evidence:
- isolated account with custom inference enabled
- disposable endpoint named zh-smoke-delete-endpoint
- redacted remove confirmation GUI evidence
- cleanup proof that the endpoint is absent
safety_rule: Do not create, edit, or delete any endpoint whose name is not zh-smoke-delete-endpoint.

row_id: GUI-WS-07
category: disposable_object
status: missing
handoff_doc: docs/zh-Hans-backend-fixture-contract-rc19.md
artifact_path: artifacts/redacted/gui-ws-07.txt
required_evidence:
- disposable owner test team named zh-smoke-public-rc-team
- redacted transfer confirmation GUI evidence
- cleanup proof that ownership is restored or the team is deleted
safety_rule: Do not transfer ownership of any real team; automate nothing for admin/ownership prompts without explicit approval.

decision: blocked-until-matching-evidence-is-reviewed
