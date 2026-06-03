# zh-Hans Post-RC36 Evidence Queue Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move Warp CN from RC36 to RC37 by turning the 11 public-RC evidence blockers into a prioritized, machine-readable collection queue without collecting or approving real evidence.

**Architecture:** Keep the blocker registry and evidence ledger as the source of truth. Add a small `script/zh_public_rc_evidence_queue.py` helper that imports existing blocker/evidence parsing and emits safe queue rows with category, priority, approval gate, artifact path, and blocked-by fields. Keep real evidence, GUI launch, backend fixtures, PNG assets, and heavy validation behind explicit approval and `script/zh_low_load_gate.py`.

**Tech Stack:** Python `unittest`, dataclasses, JSON serialization, Markdown queue output, existing TOML subset parser, existing zh-Hans validation scripts, `nice` for lightweight checks, low-concurrency Rust gates only after the low-load helper allows them.

---

## Current Baseline

RC36 status:

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
filtered missing-action text: available
filtered missing-action JSON: available
filtered Markdown action packet: available
fresh bundle: not refreshed in RC36
GUI launch: not run
PNG changes: none
```

Next-cycle priority:

```text
1. Keep public-RC blocked until real reviewed evidence exists.
2. Add a queue helper that ranks missing evidence rows by category and risk.
3. Expose queue output as JSON and Markdown for operators and future dashboards.
4. Preserve row/category filters so operators can request a scoped queue.
5. Document RC37 queue usage without creating evidence or changing the ledger.
6. Retry heavy validation only if script/zh_low_load_gate.py returns decision: run-heavy-gate.
7. Do not stage, commit, push, merge, rebase, tag, launch GUI, create accounts, create backend fixtures, or mutate external state unless explicitly approved.
```

## File Structure

- Create `script/zh_public_rc_evidence_queue.py` to render prioritized public-RC evidence collection queues.
- Create `script/test_zh_public_rc_evidence_queue.py` to test queue row fields, filtering, JSON output, Markdown output, and ready-row omission.
- Create `docs/zh-Hans-public-rc-evidence-queue-rc37.md` to document queue commands and safety boundaries.
- Create `docs/zh-Hans-public-rc-lane-readiness-rc37.md` to record lane status after queue planning.
- Create `docs/zh-Hans-localization-phase268.md` through `docs/zh-Hans-localization-phase275.md`.
- Create `docs/zh-Hans-release-candidate-2026-06-02-rc37.md` only during Phase 275.
- Modify `docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md` to point isolated-account operators to filtered RC37 queue commands.
- Modify `docs/zh-Hans-backend-fixture-contract-rc19.md` to point backend-fixture and disposable-object operators to filtered RC37 queue commands.
- Modify `docs/zh-Hans-localization.md` during Phase 268 and Phase 275.
- Modify `README.md` only during Phase 275 to point to RC37 and the evidence queue helper.
- Modify `docs/zh-Hans-gui-smoke-matrix.md` only when heavy, GUI, asset, or queue status changes.
- Do not modify `resources/localization/zh-Hans-public-rc-evidence.toml` unless reviewed redacted evidence is provided and explicit approval is given.
- Do not modify `resources/localization/zh-Hans-public-rc-blockers.toml` unless a blocker is genuinely cleared with reviewed evidence and explicit approval is given.
- Do not create files under `artifacts/redacted/` except temporary files inside tests.
- Do not modify `app/assets/async/png/onboarding/**/*.png` without explicit asset approval.
- Do not stage, commit, push, merge, rebase, or mutate tags without explicit user approval.

## Phase Map

| Phase | Purpose | Qualification Gate |
| --- | --- | --- |
| 268 | Post-RC36 baseline and scope lock | RC36 status confirmed; privacy/diff checks pass |
| 269 | Evidence queue helper tests | failing tests define queue row fields and output contracts |
| 270 | Evidence queue helper implementation | JSON and Markdown queue output pass tests |
| 271 | RC37 queue documentation | docs explain queue usage without creating evidence |
| 272 | Runbook queue-command refresh | isolated/backend/disposable operators have exact queue commands |
| 273 | RC37 lane readiness refresh | lane boundaries remain explicit; no blockers are cleared |
| 274 | Low-load heavy validation retry | heavy commands run only after `decision: run-heavy-gate`; otherwise record defer |
| 275 | RC37 freeze and final review | validation passes; public-RC decision remains honest |

### Task 1: Phase 268 Post-RC36 Baseline

**Files:**
- Create: `docs/zh-Hans-localization-phase268.md`
- Modify: `docs/zh-Hans-localization.md`

- [ ] **Step 1: Inspect current branch and RC36 evidence state**

Run:

```bash
git status --short --branch
nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
nice -n 10 python3 script/zh_public_rc_status.py
nice -n 10 python3 script/zh_public_rc_evidence_report.py --json
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-actions-json --row-id GUI-SET-05
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category backend_fixture
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
filtered row JSON returns total_actions: 1 for GUI-SET-05
filtered category Markdown returns backend_fixture rows
strict evidence lint exits 1 because real evidence is still missing
privacy_guard.py exits 0
git diff --check exits 0
```

- [ ] **Step 2: Create Phase 268 record**

Create `docs/zh-Hans-localization-phase268.md`:

```markdown
# zh-Hans Localization Phase 268

Date: 2026-06-02

## Scope

Phase 268 audits the post-RC36 baseline before adding prioritized evidence queue
output.

This phase does not stage, commit, push, merge, rebase, mutate tags, launch GUI,
use accounts, create backend fixtures, touch billing/cloud state, create real
evidence artifacts, run Rust compile, build a bundle, or modify PNG assets.

## Findings

```text
branch: codex/zh-Hans-post-rc26-execution
dry-run: would_change 0, missing 0
public-RC blockers: 11
evidence ready rows: 0
filtered row JSON: passed
filtered category Markdown: passed
strict evidence lint: expected fail, exit_code 1
privacy guard: passed
git diff --check: passed
```

## Decision

```text
decision: proceed-to-prioritized-evidence-queue
public RC: still blocked by evidence
publication/integration: requires explicit user approval
```

## Qualification Review

```text
phase: 268
status: qualified-post-rc36-baseline
safe to continue to Phase 269: yes
```
```

- [ ] **Step 3: Update localization index**

Add this line near the RC36 status in `docs/zh-Hans-localization.md`:

```markdown
- Phase 268 records the post-RC36 baseline before adding prioritized evidence queue output.
```

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

### Task 2: Phase 269 Evidence Queue Tests

**Files:**
- Create: `script/test_zh_public_rc_evidence_queue.py`
- Create: `docs/zh-Hans-localization-phase269.md`

- [ ] **Step 1: Write failing queue tests**

Create `script/test_zh_public_rc_evidence_queue.py`:

```python
#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_public_rc_evidence_lint import load_toml
from zh_public_rc_evidence_queue import (
    build_queue,
    filter_queue,
    render_json,
    render_markdown,
)


class PublicRcEvidenceQueueTests(unittest.TestCase):
    def test_current_queue_contains_all_missing_rows_with_priority(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        queue = build_queue(blockers, evidence)

        self.assertEqual(len(queue), 11)
        self.assertEqual(queue[0].row_id, "GUI-BILL-01")
        self.assertEqual(queue[0].category, "backend_fixture")
        self.assertEqual(queue[0].priority, 10)
        self.assertEqual(queue[0].approval_gate, "fixture-owner-approval")
        self.assertEqual(queue[0].artifact_path, "artifacts/redacted/gui-bill-01.txt")

    def test_filter_queue_by_category_and_row_id(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        queue = build_queue(blockers, evidence)
        backend_queue = filter_queue(queue, categories=("backend_fixture",))
        row_queue = filter_queue(queue, row_ids=("GUI-SET-05",))

        self.assertEqual(len(backend_queue), 5)
        self.assertTrue(all(row.category == "backend_fixture" for row in backend_queue))
        self.assertEqual([row.row_id for row in row_queue], ["GUI-SET-05"])

    def test_json_output_has_stable_counts_and_no_ready_rows(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        data = json.loads(render_json(build_queue(blockers, evidence)))

        self.assertEqual(data["total_rows"], 11)
        self.assertEqual(data["decision"], "blocked-until-queue-cleared")
        self.assertEqual(data["category_counts"]["backend_fixture"], 5)
        self.assertEqual(data["rows"][0]["row_id"], "GUI-BILL-01")
        self.assertEqual(data["rows"][0]["approval_gate"], "fixture-owner-approval")

    def test_markdown_output_is_safe_and_scoped(self) -> None:
        blockers = load_toml(Path("resources/localization/zh-Hans-public-rc-blockers.toml"))
        evidence = load_toml(Path("resources/localization/zh-Hans-public-rc-evidence.toml"))

        markdown = render_markdown(filter_queue(build_queue(blockers, evidence), row_ids=("GUI-SET-05",)))

        self.assertIn("# zh-Hans Public-RC Evidence Collection Queue", markdown)
        self.assertIn("## GUI-SET-05", markdown)
        self.assertIn("artifacts/redacted/gui-set-05.txt", markdown)
        self.assertIn("fixture-owner-approval", markdown)
        self.assertNotIn("GUI-AUTH-01", markdown)
        self.assertNotIn("@", markdown)
        self.assertNotIn("https://", markdown)

    def test_ready_rows_are_omitted_from_queue(self) -> None:
        blockers = {
            "blocker": [
                {
                    "id": "GUI-SET-05",
                    "category": "backend_fixture",
                    "status": "blocked-no-backend-fixture",
                    "handoff_doc": "docs/zh-Hans-backend-fixture-contract-rc19.md",
                    "safety_rule": "Use safe invalid marker values only.",
                    "required_evidence": ["invalid credential fixture"],
                    "public_rc_required": True,
                    "local_fixture_allowed": True,
                }
            ]
        }
        evidence = {
            "evidence": [
                {
                    "row_id": "GUI-SET-05",
                    "status": "provided",
                    "evidence_paths": ["artifacts/redacted/gui-set-05.txt"],
                    "cleanup_proof": "fixture reset proof captured",
                    "redaction": "identifiers removed",
                    "notes": "safe marker only",
                }
            ]
        }

        queue = build_queue(blockers, evidence)

        self.assertEqual(queue, ())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
nice -n 10 python3 -m unittest script/test_zh_public_rc_evidence_queue.py
```

Expected:

```text
FAIL because script/zh_public_rc_evidence_queue.py does not exist yet
```

- [ ] **Step 3: Create Phase 269 record**

Create `docs/zh-Hans-localization-phase269.md`:

```markdown
# zh-Hans Localization Phase 269

Date: 2026-06-02

## Scope

Phase 269 defines failing tests for prioritized public-RC evidence queue output.

No implementation exists yet, no evidence rows are promoted, and no evidence
artifacts are created.

## Verification

```text
script/test_zh_public_rc_evidence_queue.py: expected fail because queue helper is not implemented
```

## Decision

```text
decision: proceed-to-evidence-queue-helper-implementation
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 269
status: qualified-red-test-for-evidence-queue
safe to continue to Phase 270: yes
```
```

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

### Task 3: Phase 270 Evidence Queue Helper Implementation

**Files:**
- Create: `script/zh_public_rc_evidence_queue.py`
- Modify: `script/test_zh_public_rc_evidence_queue.py` only if the red tests reveal exact import or formatting adjustments.
- Create: `docs/zh-Hans-localization-phase270.md`

- [ ] **Step 1: Implement queue helper**

Create `script/zh_public_rc_evidence_queue.py`:

```python
#!/usr/bin/env python3
"""Render prioritized zh-Hans public-RC evidence collection queues."""

from __future__ import annotations

import argparse
import collections
import dataclasses
import json
import sys
from pathlib import Path
from typing import Any

from zh_public_rc_evidence_lint import DEFAULT_BLOCKERS, DEFAULT_EVIDENCE, blocker_index, load_toml
from zh_public_rc_evidence_report import evidence_by_id, redacted_path


CATEGORY_PRIORITY = {
    "backend_fixture": 10,
    "isolated_account": 20,
    "disposable_object": 30,
}

CATEGORY_APPROVAL_GATE = {
    "backend_fixture": "fixture-owner-approval",
    "isolated_account": "isolated-account-approval",
    "disposable_object": "disposable-object-approval",
}

CATEGORY_RISK = {
    "backend_fixture": "medium",
    "isolated_account": "high",
    "disposable_object": "high",
}

CATEGORY_BLOCKERS = {
    "backend_fixture": ("fixture_owner", "fixture_reset_proof", "redacted_fixture_evidence"),
    "isolated_account": ("isolated_account", "logout_or_profile_cleanup", "redacted_gui_evidence"),
    "disposable_object": ("disposable_object", "explicit_delete_approval", "cleanup_absence_proof"),
}


@dataclasses.dataclass(frozen=True)
class QueueRow:
    row_id: str
    category: str
    status: str
    priority: int
    risk: str
    approval_gate: str
    artifact_path: str
    handoff_doc: str
    blocked_by: tuple[str, ...]
    required_evidence: tuple[str, ...]
    safety_rule: str


def _priority_for(category: str, row_id: str) -> int:
    base_priority = CATEGORY_PRIORITY.get(category, 90)
    if category == "disposable_object":
        return base_priority + 5
    if row_id.startswith("GUI-BILL"):
        return base_priority + 2
    return base_priority


def build_queue(blockers: dict[str, Any], evidence_doc: dict[str, Any]) -> tuple[QueueRow, ...]:
    evidence = evidence_by_id(evidence_doc)
    rows: list[QueueRow] = []
    for row_id, blocker in sorted(blocker_index(blockers).items()):
        evidence_row = evidence.get(row_id, {})
        evidence_status = str(evidence_row.get("status", "missing"))
        if evidence_status == "provided":
            continue
        category = str(blocker["category"])
        rows.append(
            QueueRow(
                row_id=row_id,
                category=category,
                status=evidence_status,
                priority=_priority_for(category, row_id),
                risk=CATEGORY_RISK.get(category, "unknown"),
                approval_gate=CATEGORY_APPROVAL_GATE.get(category, "manual-approval"),
                artifact_path=redacted_path(row_id),
                handoff_doc=str(blocker["handoff_doc"]),
                blocked_by=tuple(CATEGORY_BLOCKERS.get(category, ("manual_review",))),
                required_evidence=tuple(str(item) for item in blocker.get("required_evidence", [])),
                safety_rule=str(blocker["safety_rule"]),
            )
        )
    return tuple(sorted(rows, key=lambda row: (row.priority, row.row_id)))


def filter_queue(
    rows: tuple[QueueRow, ...],
    *,
    row_ids: tuple[str, ...] = (),
    categories: tuple[str, ...] = (),
) -> tuple[QueueRow, ...]:
    row_filter = {row_id.strip() for row_id in row_ids if row_id.strip()}
    category_filter = {category.strip() for category in categories if category.strip()}
    selected: list[QueueRow] = []
    for row in rows:
        if row_filter and row.row_id not in row_filter:
            continue
        if category_filter and row.category not in category_filter:
            continue
        selected.append(row)
    return tuple(selected)


def queue_to_json_data(rows: tuple[QueueRow, ...]) -> dict[str, Any]:
    category_counts = collections.Counter(row.category for row in rows)
    risk_counts = collections.Counter(row.risk for row in rows)
    return {
        "total_rows": len(rows),
        "category_counts": dict(sorted(category_counts.items())),
        "risk_counts": dict(sorted(risk_counts.items())),
        "rows": [
            {
                **dataclasses.asdict(row),
                "blocked_by": list(row.blocked_by),
                "required_evidence": list(row.required_evidence),
            }
            for row in rows
        ],
        "decision": "ready" if not rows else "blocked-until-queue-cleared",
    }


def render_json(rows: tuple[QueueRow, ...]) -> str:
    return json.dumps(queue_to_json_data(rows), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_text(rows: tuple[QueueRow, ...]) -> str:
    lines = [
        "zh-Hans public-RC evidence collection queue",
        f"total_rows: {len(rows)}",
    ]
    for row in rows:
        lines.append(
            f"{row.row_id}: priority={row.priority} category={row.category} risk={row.risk} approval={row.approval_gate}"
        )
    lines.append(f"decision: {'ready' if not rows else 'blocked-until-queue-cleared'}")
    return "\n".join(lines) + "\n"


def render_markdown(rows: tuple[QueueRow, ...]) -> str:
    lines = [
        "# zh-Hans Public-RC Evidence Collection Queue",
        "",
        "This queue is planning metadata only. It does not provide evidence and does not clear public-RC blockers.",
        "",
        "## Safety Boundary",
        "",
        "- Keep raw screenshots, recordings, callback URLs, cookies, tokens, account identifiers, endpoint URLs, team IDs, and private object names outside Git.",
        "- Do not mutate accounts, billing, cloud state, teams, secrets, endpoints, or environments without explicit approval.",
        "- Promote a row only after reviewed raw evidence, approved redacted artifact text, cleanup proof, and strict artifact lint pass.",
        "",
    ]
    if not rows:
        lines.extend(["## Empty Queue", "", "No missing public-RC evidence rows matched the supplied filters.", ""])
        return "\n".join(lines)

    for row in rows:
        lines.extend(
            [
                f"## {row.row_id}",
                "",
                f"- Priority: `{row.priority}`",
                f"- Category: `{row.category}`",
                f"- Risk: `{row.risk}`",
                f"- Approval gate: `{row.approval_gate}`",
                f"- Current status: `{row.status}`",
                f"- Expected redacted artifact: `{row.artifact_path}`",
                f"- Handoff doc: `{row.handoff_doc}`",
                f"- Blocked by: `{', '.join(row.blocked_by)}`",
                f"- Safety rule: {row.safety_rule}",
                "",
                "Required evidence:",
            ]
        )
        for item in row.required_evidence:
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render zh-Hans public-RC evidence collection queue.")
    parser.add_argument("--blockers", type=Path, default=DEFAULT_BLOCKERS)
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--json", action="store_true", help="Print queue as JSON")
    parser.add_argument("--markdown", action="store_true", help="Print queue as Markdown")
    parser.add_argument("--row-id", action="append", default=[], help="Limit queue output to a public-RC row ID")
    parser.add_argument("--category", action="append", default=[], help="Limit queue output to a blocker category")
    args = parser.parse_args(argv)

    rows = filter_queue(
        build_queue(load_toml(args.blockers), load_toml(args.evidence)),
        row_ids=tuple(args.row_id),
        categories=tuple(args.category),
    )
    if args.json:
        print(render_json(rows), end="")
        return 0
    if args.markdown:
        print(render_markdown(rows), end="")
        return 0
    print(render_text(rows), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Verify queue helper tests**

Run:

```bash
nice -n 10 python3 -m unittest script/test_zh_public_rc_evidence_queue.py
nice -n 10 python3 script/zh_public_rc_evidence_queue.py --json --row-id GUI-SET-05
nice -n 10 python3 script/zh_public_rc_evidence_queue.py --markdown --category backend_fixture
```

Expected:

```text
5 tests pass
row JSON returns total_rows: 1 and GUI-SET-05
backend_fixture Markdown returns five backend fixture rows and no isolated/disposable rows
```

- [ ] **Step 3: Create Phase 270 record**

Create `docs/zh-Hans-localization-phase270.md`:

```markdown
# zh-Hans Localization Phase 270

Date: 2026-06-02

## Scope

Phase 270 implements prioritized public-RC evidence queue output.

No evidence rows are promoted, and no evidence artifacts are created.

## Verification

```text
script/test_zh_public_rc_evidence_queue.py: passed
--json --row-id GUI-SET-05: total_rows 1
--markdown --category backend_fixture: backend fixture rows only
```

## Decision

```text
decision: proceed-to-rc37-queue-documentation
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 270
status: qualified-evidence-queue-helper
safe to continue to Phase 271: yes
```
```

- [ ] **Step 4: Verify Task 3**

Run:

```bash
nice -n 10 python3 script/privacy_guard.py --all-tracked
git diff --check
```

Expected:

```text
both commands exit 0
```

### Task 4: Phase 271 RC37 Evidence Queue Docs

**Files:**
- Create: `docs/zh-Hans-public-rc-evidence-queue-rc37.md`
- Create: `docs/zh-Hans-localization-phase271.md`

- [ ] **Step 1: Generate queue outputs for documentation**

Run:

```bash
nice -n 10 python3 script/zh_public_rc_evidence_queue.py
nice -n 10 python3 script/zh_public_rc_evidence_queue.py --json
nice -n 10 python3 script/zh_public_rc_evidence_queue.py --json --row-id GUI-SET-05
nice -n 10 python3 script/zh_public_rc_evidence_queue.py --markdown --category backend_fixture
```

Expected:

```text
text queue reports total_rows: 11
full JSON reports total_rows: 11
row JSON reports total_rows: 1
backend_fixture Markdown reports five backend fixture rows
```

- [ ] **Step 2: Create RC37 queue doc**

Create `docs/zh-Hans-public-rc-evidence-queue-rc37.md`:

```markdown
# zh-Hans Public-RC Evidence Queue RC37

Date: 2026-06-02

## Purpose

RC37 adds prioritized public-RC evidence queue output. The queue helps operators
choose safe evidence work by row, category, risk, priority, and approval gate.

The queue is planning metadata only. It does not provide evidence, does not
change `resources/localization/zh-Hans-public-rc-evidence.toml`, and does not
clear blockers.

## Commands

```bash
python3 script/zh_public_rc_evidence_queue.py
python3 script/zh_public_rc_evidence_queue.py --json
python3 script/zh_public_rc_evidence_queue.py --markdown
python3 script/zh_public_rc_evidence_queue.py --json --row-id GUI-SET-05
python3 script/zh_public_rc_evidence_queue.py --markdown --category backend_fixture
python3 script/zh_public_rc_evidence_queue.py --markdown --category isolated_account
python3 script/zh_public_rc_evidence_queue.py --markdown --category disposable_object
```

## Queue Semantics

```text
priority 10-19: backend fixture lane
priority 20-29: isolated account lane
priority 30-39: disposable object lane
approval_gate fixture-owner-approval: requires fixture owner and reset proof
approval_gate isolated-account-approval: requires isolated account and cleanup proof
approval_gate disposable-object-approval: requires explicit object mutation approval
```

## Current Queue

```text
total_rows: 11
backend_fixture: 5
isolated_account: 3
disposable_object: 3
ready rows: 0
decision: blocked-until-queue-cleared
```

## Safety Boundary

```text
raw evidence stays outside Git
redacted artifact text requires explicit approval before adding to artifacts/redacted/
ledger promotion requires reviewed raw evidence and strict artifact lint pass
blocker promotion requires accepted evidence row and explicit approval
queue output alone cannot promote any row
```
```

- [ ] **Step 3: Create Phase 271 record**

Create `docs/zh-Hans-localization-phase271.md`:

```markdown
# zh-Hans Localization Phase 271

Date: 2026-06-02

## Scope

Phase 271 documents RC37 prioritized public-RC evidence queue output.

No evidence rows are promoted, and no evidence artifacts are created.

## Verification

```text
text queue: total_rows 11
JSON queue: total_rows 11
row JSON queue: total_rows 1
backend_fixture Markdown queue: five backend fixture rows
```

## Decision

```text
decision: proceed-to-runbook-queue-command-refresh
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 271
status: qualified-evidence-queue-docs
safe to continue to Phase 272: yes
```
```

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

### Task 5: Phase 272 Runbook Queue-Command Refresh

**Files:**
- Modify: `docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md`
- Modify: `docs/zh-Hans-backend-fixture-contract-rc19.md`
- Create: `docs/zh-Hans-localization-phase272.md`

- [ ] **Step 1: Update isolated-account runbook**

Append this section to `docs/zh-Hans-public-rc-isolated-account-runbook-rc19.md`:

```markdown
## RC37 Evidence Queue Commands

Use these commands to inspect isolated-account queue order before collecting
evidence:

```bash
python3 script/zh_public_rc_evidence_queue.py --markdown --category isolated_account
python3 script/zh_public_rc_evidence_queue.py --json --row-id GUI-AUTH-01
python3 script/zh_public_rc_evidence_queue.py --json --row-id GUI-SET-03
python3 script/zh_public_rc_evidence_queue.py --json --row-id GUI-WS-06
```

These commands do not create evidence. They print queue metadata only. Do not
use the user's main account, and do not store account identifiers, callback
URLs, cookies, tokens, or magic links in repository files.
```

- [ ] **Step 2: Update backend/disposable fixture contract**

Append this section to `docs/zh-Hans-backend-fixture-contract-rc19.md`:

```markdown
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
```

- [ ] **Step 3: Create Phase 272 record**

Create `docs/zh-Hans-localization-phase272.md`:

```markdown
# zh-Hans Localization Phase 272

Date: 2026-06-02

## Scope

Phase 272 refreshes the isolated-account and backend/disposable-object runbooks
with RC37 evidence queue commands.

No evidence rows are promoted, and no evidence artifacts are created.

## Verification

```text
isolated-account runbook: RC37 queue commands added
backend/disposable runbook: RC37 queue commands added
privacy guard: passed
git diff --check: passed
```

## Decision

```text
decision: proceed-to-rc37-lane-readiness-refresh
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 272
status: qualified-runbook-queue-command-refresh
safe to continue to Phase 273: yes
```
```

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

### Task 6: Phase 273 RC37 Lane Readiness Refresh

**Files:**
- Create: `docs/zh-Hans-public-rc-lane-readiness-rc37.md`
- Create: `docs/zh-Hans-localization-phase273.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md` only if lane status text needs a current RC37 entry.

- [ ] **Step 1: Recheck lane counts, queue counts, and asset status**

Run:

```bash
nice -n 10 python3 script/zh_public_rc_status.py
nice -n 10 python3 script/zh_public_rc_evidence_report.py --json
nice -n 10 python3 script/zh_public_rc_evidence_queue.py --json
git status --short -- '*.png' 'app/assets/async/png/onboarding/**/*.png'
git diff --name-only -- '*.png' 'app/assets/async/png/onboarding/**/*.png'
```

Expected:

```text
public-RC blocker total remains 11
ready evidence rows remain 0
queue total_rows remains 11
PNG commands produce no onboarding asset changes unless explicitly approved
```

- [ ] **Step 2: Create RC37 lane readiness doc**

Create `docs/zh-Hans-public-rc-lane-readiness-rc37.md`:

```markdown
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
```

- [ ] **Step 3: Update GUI smoke matrix only if needed**

If `docs/zh-Hans-gui-smoke-matrix.md` lacks a current RC37 lane entry, add:

```markdown
## RC37 Evidence Queue Planning

```text
evidence queue: available
backend_fixture queue rows: 5
disposable_object queue rows: 3
isolated_account queue rows: 3
GUI launch: pending explicit GUI smoke approval
PNG assets: unchanged
```
```

- [ ] **Step 4: Create Phase 273 record**

Create `docs/zh-Hans-localization-phase273.md`:

```markdown
# zh-Hans Localization Phase 273

Date: 2026-06-02

## Scope

Phase 273 refreshes RC37 lane readiness after prioritized evidence queue
planning.

No evidence rows are promoted, no GUI is launched, and no PNG assets are changed.

## Verification

```text
public-RC blocker status: 11 blockers
evidence report JSON: blocked, ready rows 0
evidence queue JSON: total_rows 11
PNG asset status: unchanged
```

## Decision

```text
decision: proceed-to-low-load-heavy-validation-retry
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 273
status: qualified-lane-readiness-refresh
safe to continue to Phase 274: yes
```
```

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

### Task 7: Phase 274 Low-Load Heavy Validation Retry

**Files:**
- Create: `docs/zh-Hans-localization-phase274.md`
- Modify: `docs/zh-Hans-gui-smoke-matrix.md` only to record heavy validation result.

- [ ] **Step 1: Run low-load gate**

Run:

```bash
nice -n 10 python3 script/zh_low_load_gate.py --probes 2 --wait-seconds 60 --max-load 2.50 --max-hot-process-percent 25
```

Expected:

```text
If output contains decision: run-heavy-gate, continue to Step 2.
If output contains decision: defer-heavy-gate, skip Step 2 and record skipped-with-heat-safety.
```

- [ ] **Step 2: Run heavy validation only if allowed**

Run only if Step 1 prints `decision: run-heavy-gate`:

```bash
CARGO_BUILD_JOBS=1 cargo check -j 1 -p warp
TERM=xterm-256color WARP_SKIP_COMMON_SKILLS_INSTALL=1 ./script/run --dont-open
```

Expected:

```text
cargo check passes
bundle generation passes
GUI is not launched
```

- [ ] **Step 3: Record heavy validation result**

Create `docs/zh-Hans-localization-phase274.md` with one of these result blocks.

If heavy validation ran:

```markdown
# zh-Hans Localization Phase 274

Date: 2026-06-02

## Scope

Phase 274 retries heavy validation only after the low-load gate allows it.

GUI launch remains out of scope.

## Verification

```text
low-load gate: run-heavy-gate
cargo check -j 1 -p warp: passed
script/run --dont-open: passed
fresh bundle: passed
GUI launch: not run
```

## Decision

```text
decision: proceed-to-rc37-freeze
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 274
status: qualified-heavy-validation-passed
safe to continue to Phase 275: yes
```
```

If heavy validation was deferred:

```markdown
# zh-Hans Localization Phase 274

Date: 2026-06-02

## Scope

Phase 274 checks whether heavy validation can run safely.

GUI launch remains out of scope.

## Verification

```text
low-load gate: defer-heavy-gate
cargo check -j 1 -p warp: skipped-with-heat-safety
script/run --dont-open: skipped-with-heat-safety
fresh bundle: not refreshed in Phase 274
GUI launch: not run
```

## Decision

```text
decision: proceed-to-rc37-freeze-with-qualified-heavy-defer
public RC: still blocked by evidence
```

## Qualification Review

```text
phase: 274
status: qualified-heavy-validation-deferred
safe to continue to Phase 275: yes
```
```

- [ ] **Step 4: Update GUI smoke matrix**

Add a short RC37 heavy validation entry to `docs/zh-Hans-gui-smoke-matrix.md` matching the Phase 274 result:

```markdown
## RC37 Heavy Validation Retry

```text
low-load gate: run-heavy-gate or defer-heavy-gate
fresh bundle: passed or skipped-with-heat-safety
GUI launch: pending explicit GUI smoke approval
```
```

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

### Task 8: Phase 275 RC37 Freeze And Final Review

**Files:**
- Create: `docs/zh-Hans-release-candidate-2026-06-02-rc37.md`
- Create: `docs/zh-Hans-localization-phase275.md`
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
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-actions-json --row-id GUI-SET-05
nice -n 10 python3 script/zh_public_rc_evidence_report.py --missing-action-markdown --category backend_fixture
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
nice -n 10 python3 -m unittest script/test_zh_apply_localization.py script/test_zh_localization_inventory.py script/test_zh_export_locale.py script/test_zh_public_rc_status.py script/test_zh_low_load_gate.py script/test_zh_public_rc_evidence_lint.py script/test_zh_public_rc_evidence_report.py script/test_zh_public_rc_evidence_queue.py
nice -n 10 cargo fmt --check
git diff --check
```

Expected:

```text
manifest and glossary pass
dry-run reports would_change 0 and missing 0
release coverage remains 100.0%
public-RC blocker total remains 11
JSON evidence report remains blocked
filtered missing-action outputs pass
queue JSON reports total_rows 11
row queue JSON reports total_rows 1 for GUI-SET-05
backend_fixture queue Markdown returns backend fixture rows
strict evidence lint exits 1 because evidence is still missing
Python tests pass; expected total is 56 tests if no unrelated tests changed
cargo fmt --check exits 0
git diff --check exits 0
```

- [ ] **Step 2: Create RC37 release candidate record**

Create `docs/zh-Hans-release-candidate-2026-06-02-rc37.md`:

```markdown
# zh-Hans Release Candidate 2026-06-02 RC37

Date: 2026-06-02

## Scope

RC37 covers Phases 268 through 275. It adds prioritized public-RC evidence queue
output, queue JSON and Markdown renderers, RC37 queue docs, runbook queue-command
refresh, lane readiness refresh, low-load heavy validation retry, and the next
local-use/public-RC decision freeze.

RC37 does not add manifest translations, change PNG assets, provide GUI
evidence, log in, create backend fixtures, touch billing/cloud state, create or
delete managed secrets/endpoints, mutate team state, mutate Git refs, stage,
commit, push, merge, or rebase.

## Evidence Queue

```text
text queue: script/zh_public_rc_evidence_queue.py
JSON queue: script/zh_public_rc_evidence_queue.py --json
Markdown queue: script/zh_public_rc_evidence_queue.py --markdown
row queue: script/zh_public_rc_evidence_queue.py --json --row-id GUI-SET-05
category queue: script/zh_public_rc_evidence_queue.py --markdown --category backend_fixture
public-RC rows tracked: 11
queue rows: 11
ready rows: 0
rows promoted in RC37: 0
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

No blocker was cleared in RC37.

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
public-RC filtered missing-action outputs
public-RC evidence queue text/JSON/Markdown outputs
privacy guard
Python localization, public-RC, report, queue, and gate tests
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

RC37 is acceptable for local engineering use and continued verification. It is
not acceptable as a public RC until strict evidence lint passes with real
matching redacted artifacts, raw evidence is reviewed, current-cycle GUI
evidence exists, onboarding PNG visual status is approved or regenerated, and
publication is explicitly approved by the user.
```

- [ ] **Step 3: Create Phase 275 record**

Create `docs/zh-Hans-localization-phase275.md`:

```markdown
# zh-Hans Localization Phase 275

Date: 2026-06-02

## Scope

Phase 275 freezes RC37 after prioritized evidence queue planning and final
lightweight validation.

No evidence rows are promoted, and no integration or publication action is
performed.

## Verification

```text
manifest validation: passed
glossary check: passed
dry-run: would_change 0, missing 0
release coverage: 100.0%
public-RC blockers: 11
ready evidence rows: 0
evidence queue rows: 11
filtered row queue: passed
filtered category queue: passed
strict evidence lint: expected fail, exit_code 1
privacy guard: passed
Python test suite: passed
cargo fmt --check: passed
git diff --check: passed
```

## Decision

```text
decision: ready-for-local-use-with-fixture-evidence
public RC: not ready
```

## Qualification Review

```text
phase: 275
status: qualified-rc37-freeze
safe to stop: yes
```
```

- [ ] **Step 4: Update README and localization index**

Update `README.md` and `docs/zh-Hans-localization.md` so they point to RC37:

```text
Last verified release audit: 2026-06-02 RC37
RC37 adds prioritized public-RC evidence queue output with JSON and Markdown renderers.
Current public-RC blocker total remains 11, and ready evidence rows remain 0.
```

Also add a helper description:

```text
For RC37 and later, use script/zh_public_rc_evidence_queue.py with --json,
--markdown, --row-id, and --category to inspect prioritized evidence collection
queues.
```

- [ ] **Step 5: Run final post-doc verification**

Run:

```bash
set -e
nice -n 10 python3 script/zh_apply_localization.py --dry-run --summary
nice -n 10 python3 script/zh_public_rc_status.py
nice -n 10 python3 script/zh_public_rc_evidence_queue.py --json --row-id GUI-SET-05
nice -n 10 python3 script/zh_public_rc_evidence_queue.py --markdown --category backend_fixture
set +e
nice -n 10 python3 script/zh_public_rc_evidence_lint.py --strict-artifacts
lint_code=$?
set -e
printf 'strict_evidence_lint_exit_code=%s\n' "$lint_code"
test "$lint_code" -eq 1
nice -n 10 python3 script/privacy_guard.py --all-tracked
nice -n 10 python3 -m unittest script/test_zh_public_rc_evidence_lint.py script/test_zh_public_rc_evidence_report.py script/test_zh_public_rc_evidence_queue.py
nice -n 10 cargo fmt --check
git diff --check
git status --short --branch
```

Expected:

```text
dry-run remains clean
public-RC remains blocked with 11 blockers
queue outputs pass
strict lint expected-fails with exit code 1
targeted tests pass
cargo fmt --check exits 0
git diff --check exits 0
git status shows changes only from planned files and earlier uncommitted project work
```

## Final Review Checklist

Before marking the RC37 goal complete:

```text
all Phase 268-275 records exist
script/test_zh_public_rc_evidence_queue.py includes queue field/filter/JSON/Markdown tests
script/zh_public_rc_evidence_queue.py text, JSON, and Markdown output works
strict evidence lint still blocks missing evidence
no resources/localization/zh-Hans-public-rc-evidence.toml promotion happened without approved evidence
no artifacts/redacted/ files were created outside tests
no GUI launch happened without explicit approval
no heavy command ran unless low-load gate allowed it
no stage/commit/push/merge/rebase/tag action happened
```
