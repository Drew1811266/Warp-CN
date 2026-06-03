# zh-Hans Post-RC37 Evidence Candidate Preflight Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move Warp CN from RC37 to RC38 by adding an offline preflight tool for reviewed redacted public-RC evidence candidates, without collecting real evidence or promoting any blocker automatically.

**Architecture:** Keep `resources/localization/zh-Hans-public-rc-blockers.toml` and `resources/localization/zh-Hans-public-rc-evidence.toml` as the only public-RC state sources. Add a small `script/zh_public_rc_evidence_candidate.py` helper that validates an operator-supplied redacted text file against row metadata, required fields, allowlisted object names, cleanup proof wording, and existing sensitive-pattern checks. The helper only returns review decisions; ledger edits, blocker promotion, GUI launch, account use, backend fixture mutation, PNG edits, and publication all remain approval-gated.

**Tech Stack:** Python `unittest`, dataclasses, JSON serialization, Markdown output, existing TOML subset parser, existing public-RC lint/queue helpers, `nice` for lightweight checks, low-concurrency Rust gates only after `script/zh_low_load_gate.py` allows them.

---

## Current Baseline

RC37 status:

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
manifest entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
release coverage: 8574 covered, 2 candidates, 100.0%
public-RC blockers: 11
evidence ledger rows: 11
ready evidence rows: 0
strict evidence linter: expected fail, exit_code 1, errors 11
prioritized evidence queue: available
candidate artifact preflight: not available
fresh bundle: not refreshed in RC37
GUI launch: not run
PNG changes: none
```

Next-cycle priority:

```text
1. Keep public-RC blocked until real reviewed evidence exists.
2. Add an offline candidate preflight helper for redacted text artifacts.
3. Validate candidate artifacts without writing to resources/localization/zh-Hans-public-rc-evidence.toml.
4. Reuse existing sensitive-pattern checks so URLs, emails, tokens, cookies, API keys, and secrets are rejected.
5. Require row ID, visible Chinese anchors, redaction statement, cleanup proof, and safety confirmation in candidate files.
6. Enforce exact allowlisted object names for disposable-object rows.
7. Document candidate preflight commands for isolated-account, backend-fixture, and disposable-object lanes.
8. Retry heavy validation only if script/zh_low_load_gate.py returns decision: run-heavy-gate.
9. Do not stage, commit, push, merge, rebase, tag, launch GUI, create accounts, create backend fixtures, or mutate external state unless explicitly approved.
```

## File Structure

- Create `script/zh_public_rc_evidence_candidate.py` to preflight a redacted evidence candidate text file for one public-RC row.
- Create `script/test_zh_public_rc_evidence_candidate.py` to test accepted candidates, missing required sections, sensitive text rejection, row mismatch rejection, allowlisted disposable object checks, JSON output, and Markdown output.
- Create `docs/zh-Hans-public-rc-evidence-candidate-preflight-rc38.md` to document candidate-file format, commands, and safety boundaries.
- Create `docs/zh-Hans-public-rc-lane-readiness-rc38.md` to record lane status after candidate-preflight planning.
- Create `docs/zh-Hans-localization-phase276.md` through `docs/zh-Hans-localization-phase283.md`.
- Create `docs/zh-Hans-release-candidate-2026-06-03-rc38.md` only during Phase 283.
- Modify `docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md` to add RC38 candidate preflight commands for `GUI-AUTH-01`, `GUI-SET-03`, and `GUI-WS-06`.
- Modify `docs/zh-Hans-backend-fixture-contract-rc19.md` to add RC38 candidate preflight commands for backend-fixture and disposable-object rows.
- Modify `docs/zh-Hans-gui-smoke-matrix.md` only when candidate-preflight, heavy-gate, GUI, or lane-readiness status changes.
- Modify `docs/zh-Hans-localization.md` during Phase 276 and Phase 283.
- Modify `README.md` only during Phase 283 to point to RC38 and the candidate preflight helper.
- Do not modify `resources/localization/zh-Hans-public-rc-evidence.toml` unless reviewed redacted evidence is provided and explicit approval is given.
- Do not modify `resources/localization/zh-Hans-public-rc-blockers.toml` unless a blocker is genuinely cleared with reviewed evidence and explicit approval is given.
- Do not create files under `artifacts/redacted/` except temporary files inside tests.
- Do not modify `app/assets/async/png/onboarding/**/*.png` without explicit asset approval.
- Do not stage, commit, push, merge, rebase, or mutate tags without explicit user approval.

## Phase Map

| Phase | Purpose | Qualification Gate |
| --- | --- | --- |
| 276 | Post-RC37 baseline and scope lock | RC37 status confirmed; queue helper still works; privacy/diff checks pass |
| 277 | Candidate preflight tests | failing tests define candidate-file and output contracts |
| 278 | Candidate preflight implementation | accepted/rejected candidate cases pass tests |
| 279 | RC38 candidate-preflight documentation | docs explain candidate format without creating evidence |
| 280 | Runbook preflight-command refresh | isolated/backend/disposable operators have exact preflight commands |
| 281 | RC38 lane readiness refresh | candidate preflight is available; no blockers are cleared |
| 282 | Low-load heavy validation retry | heavy commands run only after `decision: run-heavy-gate`; otherwise record defer |
| 283 | RC38 freeze and final review | validation passes; public-RC decision remains honest |

### Task 1: Phase 276 Post-RC37 Baseline

**Files:**
- Create: `docs/zh-Hans-localization-phase276.md`
- Modify: `docs/zh-Hans-localization.md`

- [ ] **Step 1: Inspect current branch and RC37 evidence state**

Run:

```bash
git status --short --branch
nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
nice -n 10 python3 script/zh_public_rc_status.py
nice -n 10 python3 script/zh_public_rc_evidence_report.py --json
nice -n 10 python3 script/zh_public_rc_evidence_queue.py --json
nice -n 10 python3 script/zh_public_rc_evidence_queue.py --json --row-id GUI-SET-05
nice -n 10 python3 script/zh_public_rc_evidence_queue.py --markdown --category backend_fixture
set +e
nice -n 10 python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
lint_code=$?
set -e
printf 'strict_evidence_lint_exit_code=%s\n' "$lint_code"
test "$lint_code" -eq 1
nice -n 10 python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
branch remains codex/zh-Hans-post-rc26-execution
dry-run reports would_change: 0 and missing: 0
public-RC blocker total remains 11
evidence report decision remains blocked
queue JSON returns total_rows: 11
row-scoped queue JSON returns total_rows: 1 for GUI-SET-05
backend Markdown queue returns 5 backend_fixture rows
strict evidence lint exits 1 because real evidence is still missing
privacy_guard.py exits 0
git diff --check exits 0
```

- [ ] **Step 2: Create Phase 276 record**

Create `docs/zh-Hans-localization-phase276.md`:

````markdown
# zh-Hans Localization Phase 276

Date: 2026-06-03

## Scope

Phase 276 audits the post-RC37 baseline before adding redacted evidence
candidate preflight output.

This phase does not stage, commit, push, merge, rebase, mutate tags, launch GUI,
use accounts, create backend fixtures, touch billing/cloud state, create real
evidence artifacts, run Rust compile, build a bundle, or modify PNG assets.

## Findings

```text
branch: codex/zh-Hans-post-rc26-execution
dry-run: would_change 0, missing 0
public-RC blockers: 11
evidence ready rows: 0
full queue JSON: passed
row queue JSON GUI-SET-05: passed
backend queue Markdown: passed
strict evidence lint: expected fail, exit_code 1
privacy guard: passed
git diff --check: passed
```

## Decision

```text
decision: proceed-to-redacted-evidence-candidate-preflight
public RC: still blocked by evidence
publication/integration: requires explicit user approval
```

## Qualification Review

```text
phase: 276
status: qualified-post-rc37-baseline
safe to continue to Phase 277: yes
```
````

- [ ] **Step 3: Update localization index**

Add this line near the RC37 status in `docs/zh-Hans-localization.md`:

````markdown
- Phase 276 records the post-RC37 baseline before adding redacted evidence candidate preflight output.
````

- [ ] **Step 4: Verify Task 1**

Run:

```bash
nice -n 10 python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 2: Phase 277 Candidate Preflight Tests

**Files:**
- Create: `script/test_zh_public_rc_evidence_candidate.py`
- Create: `docs/zh-Hans-localization-phase277.md`

- [ ] **Step 1: Write failing candidate preflight tests**

Create `script/test_zh_public_rc_evidence_candidate.py`:

```python
#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_public_rc_evidence_candidate import preflight_candidate, render_json, render_markdown
from zh_public_rc_evidence_lint import load_toml


def candidate_text(row_id: str = "GUI-SET-05") -> str:
    return f"""row_id: {row_id}
profile: zh-rc38-fixture-profile
visible_anchors:
- 设置
- AI
- AWS Bedrock
- 无效凭据
redaction: account identifiers, callback URLs, endpoint URLs, tokens, cookies, API keys, and secrets removed
cleanup_proof: fixture reset proof captured and no production state was touched
safety_confirmation: no main account, real credential, billing state, cloud capacity, team ownership, or production object was used
artifact_kind: redacted-text
"""


class PublicRcEvidenceCandidateTests(unittest.TestCase):
    def load_docs(self) -> tuple[dict[str, object], dict[str, object]]:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))
        return blockers, evidence

    def write_candidate(self, text: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "candidate.txt"
        path.write_text(text, encoding="utf-8")
        return path

    def test_accepts_safe_backend_fixture_candidate_for_human_review(self) -> None:
        blockers, evidence = self.load_docs()
        result = preflight_candidate(blockers, evidence, row_id="GUI-SET-05", artifact_path=self.write_candidate(candidate_text()))

        self.assertTrue(result.ok)
        self.assertEqual(result.row_id, "GUI-SET-05")
        self.assertEqual(result.category, "backend_fixture")
        self.assertEqual(result.decision, "candidate-ready-for-human-review")
        self.assertEqual(result.errors, ())

    def test_rejects_missing_cleanup_proof(self) -> None:
        blockers, evidence = self.load_docs()
        path = self.write_candidate(candidate_text().replace("cleanup_proof:", "cleanup_missing:"))

        result = preflight_candidate(blockers, evidence, row_id="GUI-SET-05", artifact_path=path)

        self.assertFalse(result.ok)
        self.assertIn("cleanup_proof is required", result.errors)

    def test_rejects_sensitive_looking_content(self) -> None:
        blockers, evidence = self.load_docs()
        path = self.write_candidate(candidate_text() + "debug_url: https://example.invalid/callback?token=abc\n")

        result = preflight_candidate(blockers, evidence, row_id="GUI-SET-05", artifact_path=path)

        self.assertFalse(result.ok)
        self.assertIn("sensitive-looking text in candidate artifact", result.errors)

    def test_rejects_row_mismatch(self) -> None:
        blockers, evidence = self.load_docs()
        path = self.write_candidate(candidate_text(row_id="GUI-AUTH-01"))

        result = preflight_candidate(blockers, evidence, row_id="GUI-SET-05", artifact_path=path)

        self.assertFalse(result.ok)
        self.assertIn("candidate row_id does not match requested row", result.errors)

    def test_disposable_rows_require_allowlisted_object_name(self) -> None:
        blockers, evidence = self.load_docs()
        path = self.write_candidate(candidate_text(row_id="GUI-SET-06").replace(
            "artifact_kind: redacted-text",
            "object_name: zh-smoke-delete-environment\nartifact_kind: redacted-text",
        ))

        result = preflight_candidate(blockers, evidence, row_id="GUI-SET-06", artifact_path=path)

        self.assertTrue(result.ok)
        self.assertEqual(result.decision, "candidate-ready-for-human-review")

    def test_disposable_rows_reject_wrong_object_name(self) -> None:
        blockers, evidence = self.load_docs()
        path = self.write_candidate(candidate_text(row_id="GUI-SET-06").replace(
            "artifact_kind: redacted-text",
            "object_name: production-environment\nartifact_kind: redacted-text",
        ))

        result = preflight_candidate(blockers, evidence, row_id="GUI-SET-06", artifact_path=path)

        self.assertFalse(result.ok)
        self.assertIn("object_name must be zh-smoke-delete-environment", result.errors)

    def test_json_and_markdown_outputs_are_stable(self) -> None:
        blockers, evidence = self.load_docs()
        result = preflight_candidate(blockers, evidence, row_id="GUI-SET-05", artifact_path=self.write_candidate(candidate_text()))

        data = json.loads(render_json(result))
        markdown = render_markdown(result)

        self.assertEqual(data["row_id"], "GUI-SET-05")
        self.assertEqual(data["decision"], "candidate-ready-for-human-review")
        self.assertIn("# zh-Hans Public-RC Evidence Candidate Preflight", markdown)
        self.assertIn("GUI-SET-05", markdown)
        self.assertNotIn("https://", markdown)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests and verify the expected red failure**

Run:

```bash
nice -n 10 python3 -m unittest script/test_zh_public_rc_evidence_candidate.py
```

Expected:

```text
ModuleNotFoundError: No module named 'zh_public_rc_evidence_candidate'
```

- [ ] **Step 3: Create Phase 277 record**

Create `docs/zh-Hans-localization-phase277.md`:

````markdown
# zh-Hans Localization Phase 277

Date: 2026-06-03

## Scope

Phase 277 defines red tests for redacted evidence candidate preflight.

No production evidence is collected. Test artifacts are temporary files only.

## Red Test

```text
test command: python3 -m unittest script/test_zh_public_rc_evidence_candidate.py
expected failure: ModuleNotFoundError for zh_public_rc_evidence_candidate
```

## Decision

```text
decision: proceed-to-candidate-preflight-implementation
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 277
status: qualified-red-tests
safe to continue to Phase 278: yes
```
````

- [ ] **Step 4: Verify Task 2**

Run:

```bash
nice -n 10 python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 3: Phase 278 Candidate Preflight Implementation

**Files:**
- Create: `script/zh_public_rc_evidence_candidate.py`
- Modify: `docs/zh-Hans-localization-phase277.md` only if the actual red-test output wording differs.
- Create: `docs/zh-Hans-localization-phase278.md`

- [ ] **Step 1: Implement candidate preflight helper**

Create `script/zh_public_rc_evidence_candidate.py`:

```python
#!/usr/bin/env python3
"""Preflight redacted zh-Hans public-RC evidence candidate artifacts."""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path
from typing import Any

from zh_public_rc_evidence_lint import DEFAULT_BLOCKERS, DEFAULT_EVIDENCE, blocker_index, has_sensitive_metadata, load_toml


REQUIRED_FIELDS = (
    "row_id",
    "profile",
    "visible_anchors",
    "redaction",
    "cleanup_proof",
    "safety_confirmation",
    "artifact_kind",
)

DISPOSABLE_OBJECT_NAMES = {
    "GUI-SET-06": "zh-smoke-delete-environment",
    "GUI-WS-04": "zh-smoke-delete-secret",
    "GUI-WS-07": "zh-smoke-public-rc-team",
}


@dataclasses.dataclass(frozen=True)
class CandidateResult:
    ok: bool
    row_id: str
    category: str
    artifact_path: str
    decision: str
    fields_present: tuple[str, ...]
    errors: tuple[str, ...]


def parse_candidate_text(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    current_key: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_key, current_lines
        if current_key is not None:
            fields[current_key] = "\n".join(line for line in current_lines).strip()
        current_key = None
        current_lines = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if ":" in line and not line.startswith(("-", " ")):
            flush()
            key, value = line.split(":", 1)
            current_key = key.strip()
            current_lines = [value.strip()]
            continue
        if current_key is not None:
            current_lines.append(line.strip())
    flush()
    return fields


def _evidence_status(evidence_doc: dict[str, Any], row_id: str) -> str:
    rows = evidence_doc.get("evidence", [])
    if not isinstance(rows, list):
        return "missing"
    for row in rows:
        if isinstance(row, dict) and str(row.get("row_id", "")) == row_id:
            return str(row.get("status", "missing"))
    return "missing"


def _candidate_errors(blocker: dict[str, Any], evidence_doc: dict[str, Any], row_id: str, fields: dict[str, str], text: str) -> list[str]:
    errors: list[str] = []
    if has_sensitive_metadata(text):
        errors.append("sensitive-looking text in candidate artifact")
    if _evidence_status(evidence_doc, row_id) == "provided":
        errors.append("row already has provided evidence; use strict evidence lint instead")

    for field in REQUIRED_FIELDS:
        if not fields.get(field):
            errors.append(f"{field} is required")

    if fields.get("row_id") and fields["row_id"] != row_id:
        errors.append("candidate row_id does not match requested row")

    if fields.get("artifact_kind") and fields["artifact_kind"] != "redacted-text":
        errors.append("artifact_kind must be redacted-text")

    anchors = fields.get("visible_anchors", "")
    if anchors and not any("\u4e00" <= char <= "\u9fff" for char in anchors):
        errors.append("visible_anchors must include at least one Chinese anchor")

    expected_object = DISPOSABLE_OBJECT_NAMES.get(row_id)
    if expected_object:
        object_name = fields.get("object_name", "")
        if object_name != expected_object:
            errors.append(f"object_name must be {expected_object}")

    safety = fields.get("safety_confirmation", "")
    if safety and "main account" not in safety and "主账号" not in safety:
        errors.append("safety_confirmation must state that the main account was not used")

    cleanup = fields.get("cleanup_proof", "")
    if cleanup and not any(marker in cleanup.lower() for marker in ("cleanup", "reset", "absent", "restored", "清理", "重置", "不存在", "恢复")):
        errors.append("cleanup_proof must describe cleanup, reset, absence, or restore proof")

    if not blocker.get("public_rc_required"):
        errors.append("row is not public-RC required")

    return errors


def preflight_candidate(
    blockers: dict[str, Any],
    evidence_doc: dict[str, Any],
    *,
    row_id: str,
    artifact_path: Path,
) -> CandidateResult:
    blockers_by_id = blocker_index(blockers)
    blocker = blockers_by_id.get(row_id)
    if blocker is None:
        return CandidateResult(
            ok=False,
            row_id=row_id,
            category="unknown",
            artifact_path=str(artifact_path),
            decision="candidate-rejected",
            fields_present=(),
            errors=(f"unknown row_id: {row_id}",),
        )

    errors: list[str] = []
    if artifact_path.suffix.lower() not in (".txt", ".md"):
        errors.append("candidate artifact must be .txt or .md")
    if not artifact_path.exists():
        errors.append("candidate artifact does not exist")
        return CandidateResult(
            ok=False,
            row_id=row_id,
            category=str(blocker["category"]),
            artifact_path=str(artifact_path),
            decision="candidate-rejected",
            fields_present=(),
            errors=tuple(errors),
        )

    text = artifact_path.read_text(encoding="utf-8", errors="replace")
    fields = parse_candidate_text(text)
    errors.extend(_candidate_errors(blocker, evidence_doc, row_id, fields, text))
    ok = not errors
    return CandidateResult(
        ok=ok,
        row_id=row_id,
        category=str(blocker["category"]),
        artifact_path=str(artifact_path),
        decision="candidate-ready-for-human-review" if ok else "candidate-rejected",
        fields_present=tuple(sorted(fields)),
        errors=tuple(errors),
    )


def result_to_json_data(result: CandidateResult) -> dict[str, Any]:
    return dataclasses.asdict(result)


def render_json(result: CandidateResult) -> str:
    return json.dumps(result_to_json_data(result), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_text(result: CandidateResult) -> str:
    lines = [
        "zh-Hans public-RC evidence candidate preflight",
        f"row_id: {result.row_id}",
        f"category: {result.category}",
        f"artifact_path: {result.artifact_path}",
        f"decision: {result.decision}",
        f"errors: {len(result.errors)}",
    ]
    for error in result.errors:
        lines.append(f"error: {error}")
    return "\n".join(lines) + "\n"


def render_markdown(result: CandidateResult) -> str:
    lines = [
        "# zh-Hans Public-RC Evidence Candidate Preflight",
        "",
        "This preflight checks a redacted text candidate only. It does not collect evidence, edit the ledger, or clear blockers.",
        "",
        f"- Row ID: `{result.row_id}`",
        f"- Category: `{result.category}`",
        f"- Artifact path: `{result.artifact_path}`",
        f"- Decision: `{result.decision}`",
        f"- Fields present: `{', '.join(result.fields_present)}`",
        "",
    ]
    if result.errors:
        lines.append("## Errors")
        lines.append("")
        for error in result.errors:
            lines.append(f"- {error}")
        lines.append("")
    else:
        lines.append("## Next Review Gate")
        lines.append("")
        lines.append("- Human reviewer must inspect the raw evidence outside Git.")
        lines.append("- The ledger must not be updated until redaction, cleanup proof, row match, and safety boundaries are approved.")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Preflight a redacted zh-Hans public-RC evidence candidate.")
    parser.add_argument("--blockers", type=Path, default=DEFAULT_BLOCKERS)
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--row-id", required=True)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args(argv)

    result = preflight_candidate(
        load_toml(args.blockers),
        load_toml(args.evidence),
        row_id=args.row_id,
        artifact_path=args.artifact,
    )
    if args.json:
        print(render_json(result), end="")
    elif args.markdown:
        print(render_markdown(result), end="")
    else:
        print(render_text(result), end="")
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run candidate preflight tests**

Run:

```bash
nice -n 10 python3 -m unittest script/test_zh_public_rc_evidence_candidate.py
```

Expected:

```text
Ran 7 tests
OK
```

- [ ] **Step 3: Run existing public-RC tests together**

Run:

```bash
nice -n 10 python3 -m unittest \
  script/test_zh_public_rc_evidence_lint.py \
  script/test_zh_public_rc_evidence_report.py \
  script/test_zh_public_rc_evidence_queue.py \
  script/test_zh_public_rc_evidence_candidate.py
```

Expected:

```text
OK
```

- [ ] **Step 4: Create Phase 278 record**

Create `docs/zh-Hans-localization-phase278.md`:

````markdown
# zh-Hans Localization Phase 278

Date: 2026-06-03

## Scope

Phase 278 implements offline redacted evidence candidate preflight.

The helper does not collect evidence, edit the evidence ledger, clear blockers,
launch GUI, use accounts, create fixtures, or write files under artifacts/redacted/.

## Verification

```text
candidate preflight tests: passed
public-RC lint/report/queue/candidate tests: passed
```

## Decision

```text
decision: candidate-preflight-helper-ready
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 278
status: qualified-candidate-preflight-helper
safe to continue to Phase 279: yes
```
````

- [ ] **Step 5: Verify Task 3**

Run:

```bash
nice -n 10 python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 4: Phase 279 Candidate Preflight Documentation

**Files:**
- Create: `docs/zh-Hans-public-rc-evidence-candidate-preflight-rc38.md`
- Create: `docs/zh-Hans-localization-phase279.md`

- [ ] **Step 1: Generate sample outputs from temporary candidate files**

Run:

```bash
tmp_candidate="$(mktemp /tmp/zh-rc38-candidate.XXXXXX.txt)"
cat > "$tmp_candidate" <<'EOF'
row_id: GUI-SET-05
profile: zh-rc38-fixture-profile
visible_anchors:
- 设置
- AI
- AWS Bedrock
- 无效凭据
redaction: account identifiers, callback URLs, endpoint URLs, tokens, cookies, API keys, and secrets removed
cleanup_proof: fixture reset proof captured and no production state was touched
safety_confirmation: no main account, real credential, billing state, cloud capacity, team ownership, or production object was used
artifact_kind: redacted-text
EOF
nice -n 10 python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-05 --artifact "$tmp_candidate"
nice -n 10 python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-05 --artifact "$tmp_candidate" --json
nice -n 10 python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-05 --artifact "$tmp_candidate" --markdown
rm -f "$tmp_candidate"
```

Expected:

```text
text output decision: candidate-ready-for-human-review
JSON output decision: candidate-ready-for-human-review
Markdown output contains GUI-SET-05 and no raw URL/token/account data
```

- [ ] **Step 2: Create RC38 candidate preflight docs**

Create `docs/zh-Hans-public-rc-evidence-candidate-preflight-rc38.md`:

````markdown
# zh-Hans Public-RC Evidence Candidate Preflight RC38

Date: 2026-06-03

## Purpose

RC38 adds an offline preflight step for reviewed redacted public-RC evidence
candidate text files. The preflight helps reject unsafe or incomplete candidate
artifacts before anyone edits `resources/localization/zh-Hans-public-rc-evidence.toml`.

The preflight does not collect evidence, does not review raw screenshots, does
not update the ledger, and does not clear blockers.

## Candidate File Format

```text
row_id: GUI-SET-05
profile: zh-rc38-fixture-profile
visible_anchors:
- 设置
- AI
- AWS Bedrock
- 无效凭据
redaction: account identifiers, callback URLs, endpoint URLs, tokens, cookies, API keys, and secrets removed
cleanup_proof: fixture reset proof captured and no production state was touched
safety_confirmation: no main account, real credential, billing state, cloud capacity, team ownership, or production object was used
artifact_kind: redacted-text
```

Disposable-object rows must include the exact allowlisted object name:

```text
GUI-SET-06 object_name: zh-smoke-delete-environment
GUI-WS-04 object_name: zh-smoke-delete-secret
GUI-WS-07 object_name: zh-smoke-public-rc-team
```

## Commands

```bash
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-05 --artifact /path/to/redacted-candidate.txt
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-05 --artifact /path/to/redacted-candidate.txt --json
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-05 --artifact /path/to/redacted-candidate.txt --markdown
```

## Decision Semantics

```text
candidate-ready-for-human-review: candidate text passed machine preflight only
candidate-rejected: candidate text is unsafe, incomplete, mismatched, or not row-specific
```

## Safety Boundary

```text
raw evidence stays outside Git
candidate text must not contain emails, callback URLs, endpoint URLs, tokens,
cookies, API keys, secret values, team IDs, billing IDs, or private object names
candidate-ready-for-human-review does not update the ledger
ledger promotion requires human review, approved redaction, cleanup proof, and strict artifact lint
```
````

- [ ] **Step 3: Create Phase 279 record**

Create `docs/zh-Hans-localization-phase279.md`:

````markdown
# zh-Hans Localization Phase 279

Date: 2026-06-03

## Scope

Phase 279 documents RC38 evidence candidate preflight commands and safety rules.

No real evidence is collected. Sample candidate files are temporary `/tmp` files
only and are removed after command checks.

## Verification

```text
sample text candidate preflight: passed
sample JSON candidate preflight: passed
sample Markdown candidate preflight: passed
temporary candidate removed: yes
```

## Decision

```text
decision: candidate-preflight-docs-ready
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 279
status: qualified-candidate-preflight-docs
safe to continue to Phase 280: yes
```
````

- [ ] **Step 4: Verify Task 4**

Run:

```bash
nice -n 10 python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 5: Phase 280 Runbook Preflight Refresh

**Files:**
- Modify: `docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md`
- Modify: `docs/zh-Hans-backend-fixture-contract-rc19.md`
- Create: `docs/zh-Hans-localization-phase280.md`

- [ ] **Step 1: Append isolated-account preflight commands**

Append this section to `docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md`:

````markdown
## RC38 Candidate Preflight Commands

After raw evidence is reviewed and converted to a redacted text candidate
outside Git, run preflight before proposing any ledger update:

```bash
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-AUTH-01 --artifact /path/to/gui-auth-01-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-SET-03 --artifact /path/to/gui-set-03-candidate.txt --markdown
python3 script/zh_public_rc_evidence_candidate.py --row-id GUI-WS-06 --artifact /path/to/gui-ws-06-candidate.txt --markdown
```

These commands do not create evidence and do not clear blockers. Keep candidate
files outside Git until human redaction review approves a committed
`artifacts/redacted/<row-id>.txt` path.
````

- [ ] **Step 2: Append backend/disposable preflight commands**

Append this section to `docs/zh-Hans-backend-fixture-contract-rc19.md`:

````markdown
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
````

- [ ] **Step 3: Create Phase 280 record**

Create `docs/zh-Hans-localization-phase280.md`:

````markdown
# zh-Hans Localization Phase 280

Date: 2026-06-03

## Scope

Phase 280 refreshes isolated-account, backend-fixture, and disposable-object
runbooks with RC38 candidate preflight commands.

The runbooks remain handoff documents only.

## Verification

```text
isolated-account preflight commands documented: yes
backend-fixture preflight commands documented: yes
disposable-object exact object-name rule documented: yes
```

## Decision

```text
decision: runbook-preflight-handoff-ready
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 280
status: qualified-runbook-preflight-refresh
safe to continue to Phase 281: yes
```
````

- [ ] **Step 4: Verify Task 5**

Run:

```bash
nice -n 10 python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 6: Phase 281 Lane Readiness Refresh

**Files:**
- Create: `docs/zh-Hans-public-rc-lane-readiness-rc38.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`
- Create: `docs/zh-Hans-localization-phase281.md`

- [ ] **Step 1: Capture lane readiness command outputs**

Run:

```bash
nice -n 10 python3 script/zh_public_rc_status.py
nice -n 10 python3 script/zh_public_rc_evidence_report.py --json
nice -n 10 python3 script/zh_public_rc_evidence_queue.py --json
```

Expected:

```text
public-RC blockers: 11
ready evidence rows: 0
queue total_rows: 11
```

- [ ] **Step 2: Create RC38 lane readiness doc**

Create `docs/zh-Hans-public-rc-lane-readiness-rc38.md`:

````markdown
# zh-Hans Public-RC Lane Readiness RC38

Date: 2026-06-03

## Summary

RC38 adds candidate preflight readiness but does not clear any public-RC row.

```text
public-RC blockers: 11
ready evidence rows: 0
queue rows: 11
candidate preflight helper: available
ledger promotions in RC38: 0
```

## Lane Status

```text
isolated_account: blocked until isolated account evidence exists and candidate preflight passes
backend_fixture: blocked until fixture-owner evidence exists and candidate preflight passes
disposable_object: blocked until exact disposable object evidence exists and candidate preflight passes
```

## Promotion Boundary

```text
candidate-ready-for-human-review is not public-RC verified
strict evidence lint must pass after approved ledger/artifact updates
raw evidence review remains outside Git
```
````

- [ ] **Step 3: Append RC38 section to GUI smoke matrix**

Append this section to `docs/zh-Hans-gui-smoke-matrix.md`:

````markdown
## RC38 Evidence Candidate Preflight

RC38 adds `script/zh_public_rc_evidence_candidate.py` so redacted text
candidates can be machine-checked before any ledger update is proposed.

```text
candidate preflight: available
public-RC blockers: 11
ready evidence rows: 0
rows promoted in RC38: 0
GUI launch in RC38: not run unless separately approved
```

Candidate preflight does not collect evidence and does not replace GUI, account,
fixture, cleanup, or strict artifact-lint requirements.
````

- [ ] **Step 4: Create Phase 281 record**

Create `docs/zh-Hans-localization-phase281.md`:

````markdown
# zh-Hans Localization Phase 281

Date: 2026-06-03

## Scope

Phase 281 refreshes lane readiness after candidate preflight planning.

## Verification

```text
public-RC status: 11 blockers
evidence report JSON: ready rows 0
queue JSON: total rows 11
```

## Decision

```text
decision: lane-readiness-updated-with-candidate-preflight
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 281
status: qualified-lane-readiness-refresh
safe to continue to Phase 282: yes
```
````

- [ ] **Step 5: Verify Task 6**

Run:

```bash
nice -n 10 python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 7: Phase 282 Heat-Safe Heavy Validation Retry

**Files:**
- Create: `docs/zh-Hans-localization-phase282.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md`

- [ ] **Step 1: Run low-load gate**

Run:

```bash
nice -n 10 python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
```

Expected if the machine is busy:

```text
decision: defer-heavy-gate
```

Expected if the machine is cool enough:

```text
decision: run-heavy-gate
```

- [ ] **Step 2: Run heavy commands only if allowed**

If and only if Step 1 prints `decision: run-heavy-gate`, run:

```bash
CARGO_BUILD_JOBS=1 nice -n 10 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 nice -n 10 ./script/run --dont-open
```

If Step 1 prints `decision: defer-heavy-gate`, do not run Rust compile or bundle commands.

- [ ] **Step 3: Create Phase 282 record**

If deferred, create `docs/zh-Hans-localization-phase282.md`:

````markdown
# zh-Hans Localization Phase 282

Date: 2026-06-03

## Scope

Phase 282 checks whether heavy validation can run safely.

GUI launch remains out of scope unless separately approved.

## Verification

```text
low-load gate: defer-heavy-gate
cargo check -j 1 -p warp: skipped-with-heat-safety
script/run --dont-open: skipped-with-heat-safety
fresh bundle: not refreshed in Phase 282
GUI launch: not run
```

## Decision

```text
decision: proceed-to-rc38-freeze-with-qualified-heavy-defer
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 282
status: qualified-heavy-validation-deferred
safe to continue to Phase 283: yes
```
````

If heavy validation runs, replace the verification block with the exact passing command outputs and keep `GUI launch: not run` unless a GUI launch was separately approved.

- [ ] **Step 4: Append heavy validation status to GUI matrix**

Append this section to `docs/zh-Hans-gui-smoke-matrix.md`:

````markdown
## RC38 Heavy Validation Retry

```text
low-load gate: defer-heavy-gate
cargo check -j 1 -p warp: skipped-with-heat-safety
script/run --dont-open: skipped-with-heat-safety
GUI launch: not run
```

When the low-load gate returns `decision: run-heavy-gate`, rerun the heavy gate
with `CARGO_BUILD_JOBS=1` and record exact outputs in the RC38 release record.
````

- [ ] **Step 5: Verify Task 7**

Run:

```bash
nice -n 10 python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 8: Phase 283 RC38 Freeze And Final Review

**Files:**
- Create: `docs/zh-Hans-localization-phase283.md`
- Create: `docs/zh-Hans-release-candidate-2026-06-03-rc38.md`
- Modify: `README.md`
- Modify: `docs/zh-Hans-localization.md`

- [ ] **Step 1: Run final lightweight validation**

Run:

```bash
set -e
nice -n 10 python3 script/zh_apply_localization.py --validate-manifest
nice -n 10 python3 script/zh_apply_localization.py --check-glossary
nice -n 10 python3 script/zh_apply_localization.py --metadata-summary
nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
nice -n 10 python3 script/zh_localization_inventory.py --preset release --coverage
nice -n 10 python3 script/zh_public_rc_status.py
nice -n 10 python3 script/zh_public_rc_evidence_report.py --json
nice -n 10 python3 script/zh_public_rc_evidence_queue.py --json
nice -n 10 python3 -m unittest \
  script/test_zh_apply_localization.py \
  script/test_zh_localization_inventory.py \
  script/test_zh_export_locale.py \
  script/test_zh_public_rc_status.py \
  script/test_zh_low_load_gate.py \
  script/test_zh_public_rc_evidence_lint.py \
  script/test_zh_public_rc_evidence_report.py \
  script/test_zh_public_rc_evidence_queue.py \
  script/test_zh_public_rc_evidence_candidate.py
set +e
nice -n 10 python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
lint_code=$?
set -e
printf 'strict_evidence_lint_exit_code=%s\n' "$lint_code"
test "$lint_code" -eq 1
nice -n 10 python3 script/privacy_guard.py --all-tracked
nice -n 10 cargo fmt --check
git diff --check
```

Expected:

```text
manifest/glossary/metadata/dry-run checks pass
release coverage remains 100.0%
public-RC blocker total remains 11
queue total_rows remains 11
Python tests pass
strict evidence lint exits 1 until real evidence exists
privacy guard exits 0
cargo fmt --check exits 0
git diff --check exits 0
```

- [ ] **Step 2: Create RC38 release record**

Create `docs/zh-Hans-release-candidate-2026-06-03-rc38.md`:

````markdown
# zh-Hans Release Candidate 2026-06-03 RC38

Date: 2026-06-03

## Scope

RC38 covers Phases 276 through 283. It adds offline redacted evidence candidate
preflight, candidate JSON/Markdown output, candidate tests, RC38 preflight docs,
runbook preflight command refreshes, lane readiness refresh, heat-safe heavy
validation gating, and the next local-use/public-RC decision freeze.

RC38 does not add manifest translations, change PNG assets, provide GUI
evidence, log in, create backend fixtures, touch billing/cloud state, create or
delete managed secrets/endpoints, mutate team state, mutate Git refs, stage,
commit, push, merge, or rebase.

## Candidate Preflight

```text
candidate helper: script/zh_public_rc_evidence_candidate.py
candidate JSON output: available
candidate Markdown output: available
public-RC rows tracked: 11
queue rows: 11
ready rows: 0
rows promoted in RC38: 0
```

## Manifest And Coverage

```text
manifest entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
release coverage: 100.0%
```

## Public-RC Blocker Registry

```text
total: 11
blocked-no-backend-fixture: 5
blocked-no-disposable-object: 3
blocked-no-isolated-account: 3
```

No blocker was cleared in RC38.

## Heavy Gate And GUI Status

```text
low-load gate: defer-heavy-gate
cargo check -j 1 -p warp: skipped-with-heat-safety
script/run --dont-open: skipped-with-heat-safety
fresh bundle: not refreshed in RC38
GUI launch: not run
```

## Command-Line Gates

Passed:

```text
manifest validation
glossary check
metadata summary
dry-run summary
release inventory coverage
public-RC blocker summary
public-RC evidence JSON report
public-RC prioritized queue JSON
public-RC candidate preflight tests
privacy guard
Python localization, public-RC, report, queue, candidate, lint, and gate tests
cargo fmt --check
git diff --check
```

Expected blocker signal:

```text
python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
exit_code: 1
decision: fail
reason: 11 rows still missing evidence
```

## Release Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

RC38 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until strict evidence lint passes with real
matching redacted artifacts, raw evidence is reviewed, current-cycle GUI
evidence exists, onboarding PNG visual status is approved or regenerated, and
publication is explicitly approved by the user.
````

- [ ] **Step 3: Create Phase 283 record**

Create `docs/zh-Hans-localization-phase283.md`:

````markdown
# zh-Hans Localization Phase 283

Date: 2026-06-03

## Scope

Phase 283 freezes the RC38 record after Phases 276 through 282.

This phase does not add translations, create GUI evidence, create fixtures,
publish a tag, stage, commit, push, merge, or rebase.

## Verification

```text
manifest validation: passed
glossary check: passed
metadata summary: passed
dry-run entries: 7943
dry-run files: 552
already_applied: 5690
would_change: 0
missing: 0
release coverage: 8574 covered, 2 candidates, 100.0%
public-RC blocker total: 11
ready evidence rows: 0
public-RC prioritized queue rows: 11
candidate preflight tests: passed
strict evidence lint: expected failure, exit_code 1, 11 rows missing evidence
privacy guard: passed
cargo fmt --check: passed
git diff --check: passed
```

## Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: still blocked by 11 evidence rows
```

## Qualification Review

```text
phase: 283
status: accepted-with-public-rc-evidence-blockers
safe to close goal: yes
```
````

- [ ] **Step 4: Update README and localization index**

Update `README.md`:

```text
当前版本：`0.18`
最后核验记录：`2026-06-03 RC38`

当前结论：`ready-for-local-use-with-fixture-evidence`。也就是说，本仓库已经适合本地工程使用和继续验证，但还不是公开 RC。RC38 继续保持源码级汉化和低负载验证干净，并新增 public-RC redacted evidence candidate preflight 的 text/JSON/Markdown 输出；远端 stable tag retarget 已确认与本地 stable 目标源码树一致，但不能声称当前分支包含远端 stable commit。公开 RC 仍需要补齐 GUI、隔离账号、后端 fixture、一次性对象和静态图证据。

| `script/zh_public_rc_evidence_candidate.py` | 预检 public-RC 脱敏候选证据文本，输出 text/JSON/Markdown 审查结果 |

- `docs/zh-Hans-release-candidate-2026-06-03-rc38.md`：当前 RC38 记录。
- `docs/zh-Hans-release-candidate-2026-06-02-rc37.md`：上一轮 RC37 记录。

现在不建议。`0.18 / RC38` 可以作为本地工程使用和继续验证的版本，但公开 RC 仍需要清掉 11 个 blocker，补齐 GUI、账号、后端 fixture、一次性对象和静态图证据；上游 stable retarget 目前只能按源码树等价表述，不能按 commit ancestry 表述。
```

Update `docs/zh-Hans-localization.md`:

```text
Last verified release audit: 2026-06-03 RC38, generated on 2026-06-03 Asia/Shanghai.

- RC38 decision: `ready-for-local-use-with-fixture-evidence`; public RC remains evidence-gated. RC38 adds `docs/zh-Hans-localization-phase276.md` through `docs/zh-Hans-localization-phase283.md`, `docs/zh-Hans-release-candidate-2026-06-03-rc38.md`, offline redacted evidence candidate preflight, candidate JSON/Markdown renderers, RC38 candidate docs, runbook preflight-command refresh, lane readiness refresh, and a heat-safe heavy validation defer. Current public-RC blocker total is 11, and ready evidence rows remain 0.

For RC38 and later, `script/zh_public_rc_evidence_candidate.py` can preflight a reviewed redacted evidence candidate with `--row-id`, `--artifact`, `--json`, and `--markdown` before any evidence ledger update is proposed.

The current RC38 record is `docs/zh-Hans-release-candidate-2026-06-03-rc38.md`. RC38 planning is tracked in `docs/superpowers/plans/2026-06-03-zh-Hans-post-rc37-roadmap.md`.
```

- [ ] **Step 5: Run post-doc final verification**

Run:

```bash
nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
nice -n 10 python3 script/zh_public_rc_status.py
nice -n 10 python3 script/zh_public_rc_evidence_queue.py --json --row-id GUI-SET-05
nice -n 10 python3 -m unittest script/test_zh_public_rc_evidence_candidate.py script/test_zh_public_rc_evidence_queue.py
set +e
nice -n 10 python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
lint_code=$?
set -e
printf 'strict_evidence_lint_exit_code=%s\n' "$lint_code"
test "$lint_code" -eq 1
nice -n 10 python3 script/privacy_guard.py --all-tracked
nice -n 10 cargo fmt --check
git diff --check
git status --short --branch
```

Expected:

```text
dry-run still has would_change: 0 and missing: 0
public-RC blockers remain 11
row queue JSON still returns GUI-SET-05
candidate and queue tests pass
strict evidence lint exits 1 as expected
privacy guard exits 0
cargo fmt --check exits 0
git diff --check exits 0
no stage/commit/push/tag/merge/rebase performed
```

## Self-Review Checklist

```text
Spec coverage: phases 276-283 cover baseline, red tests, implementation, docs, runbooks, lane readiness, heat-safe gate, and RC38 freeze.
Placeholder scan: no forbidden placeholder terms remain; replace expected-output lines with observed outputs during execution.
Type consistency: CandidateResult fields are ok, row_id, category, artifact_path, decision, fields_present, and errors across tests and implementation.
Safety boundary: no real account, fixture, GUI, billing, cloud, team, endpoint, managed secret, PNG, Git ref, or publication mutation is part of this plan.
Heat boundary: Rust compile and bundle run only if zh_low_load_gate.py prints decision: run-heavy-gate.
```
