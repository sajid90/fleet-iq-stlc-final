#!/usr/bin/env python3
"""Export canonical test cases (test-cases.json) to an Excel deliverable.

The JSON file is the single source of truth, written by /speckit-tasks.
This script renders it as test-cases.xlsx (and optionally test-cases.md) so the
workbook is always regenerable and never hand-edited.

Usage:
    python3 .specify/scripts/python/export_testcases.py <feature-dir> [--markdown]
    python3 .specify/scripts/python/export_testcases.py --json <path> --out <path.xlsx>

Schema of test-cases.json:
{
  "ticket": "FLTIQ-1234",
  "feature": "Driver login",
  "generated": "2026-09-10T14:30:00",
  "test_cases": [
    {
      "id": "TC-001",
      "title": "Valid credentials land on the dashboard",
      "scenario": "S1",
      "requirements": ["TR-001"],
      "acceptance_criteria": ["TIA-AC-04"],
      "type": "Functional",
      "priority": "P1",
      "preconditions": ["An active driver account exists"],
      "steps": [{"action": "Open the login page", "expected": "Login form is visible"}],
      "expected_result": "Dashboard is shown with the driver's name",
      "test_data": "example_user",
      "automatable": true,
      "automation_status": "Not Started",
      "test_file": "automation/tests/ui/test_login.py::test_valid_login",
      "notes": ""
    }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_CASE_FIELDS = ("id", "title", "priority", "steps", "expected_result")
VALID_PRIORITIES = {"P1", "P2", "P3"}
VALID_AUTOMATION_STATUS = {"Not Started", "In Progress", "Automated", "Manual", "Blocked"}

HEADER_FILL = "1F4E78"
HEADER_FONT = "FFFFFF"
PRIORITY_FILL = {"P1": "FFC7CE", "P2": "FFEB9C", "P3": "C6EFCE"}

CASE_COLUMNS = [
    ("id", "TC ID", 12),
    ("title", "Title", 45),
    ("scenario", "Scenario", 12),
    ("requirements", "Requirement(s)", 18),
    ("acceptance_criteria", "Jira AC", 18),
    ("type", "Type", 16),
    ("priority", "Priority", 10),
    ("preconditions", "Preconditions", 35),
    ("steps_text", "Steps", 50),
    ("expected_result", "Expected Result", 40),
    ("test_data", "Test Data", 20),
    ("automatable", "Automatable", 12),
    ("automation_status", "Automation Status", 18),
    ("test_file", "Test Reference", 40),
    ("notes", "Notes", 25),
]

STEP_COLUMNS = [
    ("case_id", "TC ID", 12),
    ("case_title", "Test Case", 40),
    ("step_no", "Step #", 8),
    ("action", "Action", 55),
    ("expected", "Expected", 55),
]


class ValidationError(Exception):
    pass


def load(json_path: Path) -> dict:
    if not json_path.is_file():
        raise ValidationError(f"test cases file not found: {json_path}")
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{json_path} is not valid JSON: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("test_cases"), list):
        raise ValidationError(f"{json_path} must be an object with a 'test_cases' list")
    if not data["test_cases"]:
        raise ValidationError(f"{json_path} contains no test cases")
    return data


def validate(data: dict) -> list[str]:
    """Return a list of warnings; raise ValidationError on anything fatal."""
    warnings: list[str] = []
    seen: set[str] = set()
    for index, case in enumerate(data["test_cases"], start=1):
        if not isinstance(case, dict):
            raise ValidationError(f"test case #{index} is not an object")
        missing = [f for f in REQUIRED_CASE_FIELDS if not case.get(f)]
        if missing:
            raise ValidationError(
                f"test case #{index} ({case.get('id', 'no id')}) is missing: {', '.join(missing)}"
            )
        case_id = str(case["id"])
        if case_id in seen:
            raise ValidationError(f"duplicate test case id: {case_id}")
        seen.add(case_id)

        if case["priority"] not in VALID_PRIORITIES:
            raise ValidationError(
                f"{case_id}: priority {case['priority']!r} must be one of {sorted(VALID_PRIORITIES)}"
            )
        if not isinstance(case["steps"], list) or not case["steps"]:
            raise ValidationError(f"{case_id}: 'steps' must be a non-empty list")
        for step_no, step in enumerate(case["steps"], start=1):
            if not isinstance(step, dict) or not step.get("action"):
                raise ValidationError(f"{case_id} step {step_no}: 'action' is required")

        status = case.get("automation_status", "Not Started")
        if status not in VALID_AUTOMATION_STATUS:
            warnings.append(
                f"{case_id}: automation_status {status!r} is not one of {sorted(VALID_AUTOMATION_STATUS)}"
            )
        if not case.get("requirements"):
            warnings.append(f"{case_id}: no requirement traced — violates traceability principle I")

    # Acceptance-criterion tracing is warned on only when this feature actually
    # declares AC ids. Not every source provides discrete AC identifiers (a
    # narrative PRD or an informally written story may not), so this is opt-in
    # per feature rather than a blanket requirement.
    feature_uses_acs = any(c.get("acceptance_criteria") for c in data["test_cases"])
    if feature_uses_acs:
        for case in data["test_cases"]:
            if not case.get("acceptance_criteria"):
                warnings.append(
                    f"{case.get('id', 'no id')}: no acceptance criterion traced, but this "
                    "feature declares AC ids on other cases"
                )
    return warnings


def as_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (list, tuple)):
        return "\n".join(f"{i}. {v}" for i, v in enumerate(value, 1)) if len(value) > 1 else str(value[0]) if value else ""
    return str(value)


def flatten_case(case: dict) -> dict:
    steps = case.get("steps", [])
    steps_text = "\n".join(
        f"{i}. {s.get('action', '')}" + (f"\n   → {s['expected']}" if s.get("expected") else "")
        for i, s in enumerate(steps, 1)
    )
    row = dict(case)
    row["steps_text"] = steps_text
    row["requirements"] = ", ".join(case.get("requirements", []) or [])
    row["acceptance_criteria"] = ", ".join(case.get("acceptance_criteria", []) or [])
    row["preconditions"] = as_text(case.get("preconditions"))
    row["automatable"] = as_text(case.get("automatable"))
    row["automation_status"] = case.get("automation_status", "Not Started")
    return row


def write_xlsx(data: dict, out_path: Path) -> None:
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
        from openpyxl.utils import get_column_letter
    except ImportError:
        raise ValidationError(
            "openpyxl is required for Excel export.\n"
            "  Install it with:  pip install openpyxl\n"
            "  (it is already listed in requirements.txt)"
        )

    cases = [flatten_case(c) for c in data["test_cases"]]
    wb = Workbook()

    header_font = Font(bold=True, color=HEADER_FONT, size=11)
    header_fill = PatternFill("solid", fgColor=HEADER_FILL)
    thin = Side(style="thin", color="BFBFBF")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    top_wrap = Alignment(vertical="top", wrap_text=True)

    def style_header(ws, columns):
        for col_index, (_, label, width) in enumerate(columns, start=1):
            cell = ws.cell(row=1, column=col_index, value=label)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)
            cell.border = border
            ws.column_dimensions[get_column_letter(col_index)].width = width
        ws.row_dimensions[1].height = 26
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = f"A1:{get_column_letter(len(columns))}1"

    # --- Sheet 1: Test Cases -------------------------------------------------
    ws = wb.active
    ws.title = "Test Cases"
    style_header(ws, CASE_COLUMNS)
    for row_index, case in enumerate(cases, start=2):
        for col_index, (key, _, _) in enumerate(CASE_COLUMNS, start=1):
            cell = ws.cell(row=row_index, column=col_index, value=as_text(case.get(key)))
            cell.alignment = top_wrap
            cell.border = border
        priority = case.get("priority")
        if priority in PRIORITY_FILL:
            ws.cell(row=row_index, column=6).fill = PatternFill("solid", fgColor=PRIORITY_FILL[priority])

    # --- Sheet 2: Steps (step-level detail) ----------------------------------
    ws_steps = wb.create_sheet("Steps")
    style_header(ws_steps, STEP_COLUMNS)
    row_index = 2
    for case in data["test_cases"]:
        for step_no, step in enumerate(case.get("steps", []), start=1):
            values = {
                "case_id": case["id"],
                "case_title": case["title"],
                "step_no": step_no,
                "action": step.get("action", ""),
                "expected": step.get("expected", ""),
            }
            for col_index, (key, _, _) in enumerate(STEP_COLUMNS, start=1):
                cell = ws_steps.cell(row=row_index, column=col_index, value=values[key])
                cell.alignment = top_wrap
                cell.border = border
            row_index += 1

    # --- Sheet 3: Traceability ------------------------------------------------
    ws_trace = wb.create_sheet("Traceability")
    trace_columns = [("req", "Requirement", 18), ("ac", "Jira AC", 18),
                     ("cases", "Test Cases", 45),
                     ("count", "Count", 10), ("auto", "Automated", 12)]
    style_header(ws_trace, trace_columns)
    by_req: dict[str, list[dict]] = {}
    for case in data["test_cases"]:
        for req in case.get("requirements") or ["(untraced)"]:
            by_req.setdefault(req, []).append(case)
    for row_index, (req, req_cases) in enumerate(sorted(by_req.items()), start=2):
        automated = sum(1 for c in req_cases if c.get("automation_status") == "Automated")
        acs = sorted({a for c in req_cases for a in (c.get("acceptance_criteria") or [])})
        values = [req, ", ".join(acs), ", ".join(c["id"] for c in req_cases),
                  len(req_cases), f"{automated}/{len(req_cases)}"]
        for col_index, value in enumerate(values, start=1):
            cell = ws_trace.cell(row=row_index, column=col_index, value=value)
            cell.alignment = top_wrap
            cell.border = border

    # --- Sheet 4: Summary -----------------------------------------------------
    ws_sum = wb.create_sheet("Summary", 0)
    ws_sum.column_dimensions["A"].width = 28
    ws_sum.column_dimensions["B"].width = 50
    counts = {p: sum(1 for c in cases if c.get("priority") == p) for p in sorted(VALID_PRIORITIES)}
    automatable = sum(1 for c in data["test_cases"] if c.get("automatable"))
    rows = [
        ("Ticket", data.get("ticket", "")),
        ("Feature", data.get("feature", "")),
        ("Generated", data.get("generated", "")),
        ("", ""),
        ("Total test cases", len(cases)),
        ("P1", counts.get("P1", 0)),
        ("P2", counts.get("P2", 0)),
        ("P3", counts.get("P3", 0)),
        ("", ""),
        ("Automatable", automatable),
        ("Manual", len(cases) - automatable),
        ("Requirements covered", len([r for r in by_req if r != "(untraced)"])),
        ("Untraced cases", len(by_req.get("(untraced)", []))),
    ]
    title = ws_sum.cell(row=1, column=1, value=f"Test Cases — {data.get('ticket', '')} {data.get('feature', '')}".strip())
    title.font = Font(bold=True, size=14)
    for row_index, (label, value) in enumerate(rows, start=3):
        label_cell = ws_sum.cell(row=row_index, column=1, value=label)
        label_cell.font = Font(bold=True)
        ws_sum.cell(row=row_index, column=2, value=value)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)


def write_markdown(data: dict, out_path: Path) -> None:
    lines = [
        f"# Test Cases: {data.get('ticket', '')} — {data.get('feature', '')}".rstrip(" —"),
        "",
        f"**Generated**: {data.get('generated', '')} | **Total**: {len(data['test_cases'])}",
        "",
        "> Generated from `test-cases.json`. Do not edit by hand — edit the JSON and re-export.",
        "",
    ]
    for case in data["test_cases"]:
        lines += [
            f"## {case['id']} — {case['title']}",
            "",
            f"**Priority**: {case['priority']} | **Type**: {case.get('type', '-')} "
            f"| **Scenario**: {case.get('scenario', '-')} "
            f"| **Requirements**: {', '.join(case.get('requirements', [])) or '-'}"
            + (f" | **Jira AC**: {', '.join(case['acceptance_criteria'])}"
               if case.get("acceptance_criteria") else ""),
            "",
            f"**Automation**: {case.get('automation_status', 'Not Started')}"
            + (f" (`{case['test_file']}`)" if case.get("test_file") else ""),
            "",
        ]
        if case.get("preconditions"):
            lines.append("**Preconditions**:")
            lines += [f"- {p}" for p in case["preconditions"]]
            lines.append("")
        lines += ["| # | Action | Expected |", "|---|--------|----------|"]
        for step_no, step in enumerate(case["steps"], start=1):
            action = str(step.get("action", "")).replace("|", "\\|")
            expected = str(step.get("expected", "")).replace("|", "\\|")
            lines.append(f"| {step_no} | {action} | {expected} |")
        lines += ["", f"**Expected result**: {case['expected_result']}", "", "---", ""]
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export test-cases.json to Excel.")
    parser.add_argument("feature_dir", nargs="?", help="Feature directory containing test-cases.json")
    parser.add_argument("--json", dest="json_path", help="Explicit path to test-cases.json")
    parser.add_argument("--out", dest="out_path", help="Explicit output .xlsx path")
    parser.add_argument("--markdown", action="store_true", help="Also write test-cases.md")
    args = parser.parse_args()

    if args.json_path:
        json_path = Path(args.json_path)
    elif args.feature_dir:
        json_path = Path(args.feature_dir) / "test-cases.json"
    else:
        parser.error("provide a feature directory or --json")

    out_path = Path(args.out_path) if args.out_path else json_path.with_suffix(".xlsx")

    try:
        data = load(json_path)
        warnings = validate(data)
        write_xlsx(data, out_path)
        if args.markdown:
            write_markdown(data, json_path.with_suffix(".md"))
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    print(f"Exported {len(data['test_cases'])} test cases -> {out_path}")
    if args.markdown:
        print(f"Exported markdown -> {json_path.with_suffix('.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
