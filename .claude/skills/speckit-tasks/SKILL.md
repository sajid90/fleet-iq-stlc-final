---
name: "speckit-tasks"
description: "STLC Phase 3 — Test Case Development. Derive test cases from the test basis and export them to Excel."
argument-hint: "Optional constraints (e.g. 'API cases only', 'skip P3')"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  adapted-for: "STLC (Software Testing Life Cycle)"
  stlc-phase: "3 — Test Case Development"
user-invocable: true
disable-model-invocation: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before tasks generation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_tasks` key
- If the YAML cannot be parsed or is invalid, do not skip silently: tell the user that `.specify/extensions.yml` could not be read (include the parser error) and that no hooks were checked, including any mandatory (`optional: false`) hooks registered there, then continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- When constructing command invocations from hook command names, replace dots (`.`) with hyphens (`-`). For example, `speckit.git.commit` → `/speckit-git-commit`.
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Pre-Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Mandatory hook** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Pre-Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}

    Wait for the result of the hook command before proceeding to the Outline.
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session (the invocation may differ from the literal `{command}` id shown above, e.g. a skills-mode agent runs it as `/skill:speckit-...` or `$speckit-...`). Emitting the block alone does not run the hook.
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## Outline

You are performing **STLC Phase 3 — Test Case Development**. You produce three
artifacts:

| Artifact | Role |
|----------|------|
| `test-cases.json` | **Canonical** test cases — the single source of truth |
| `test-cases.xlsx` | The Excel deliverable, **generated** from the JSON |
| `tasks.md` | The automation work breakdown that turns cases into code |

The workbook is always regenerated from the JSON. Never hand-write the `.xlsx`
and never edit it as the source — a divergence between the two is a defect.

**QA perspective, not product design.** Derive every case from what `spec.md`
already states the product does or must do — do not invent new product
behaviour or silently resolve an ambiguity yourself. If a scenario's expected
result is unclear enough that you cannot write a defensible case, that is a
gap in the test basis; send the user back to `/speckit-clarify` rather than
guessing what the product should do.

### Step 1: Setup

Run `.specify/scripts/bash/setup-tasks.sh --json` from the repo root and parse
`FEATURE_DIR`, `TASKS_TEMPLATE_CONTENT`, `TASKS_TEMPLATE` and `AVAILABLE_DOCS`.
`FEATURE_DIR` and `TASKS_TEMPLATE` are absolute paths. Older setup scripts may
omit `TASKS_TEMPLATE_CONTENT` — read `TASKS_TEMPLATE` in that case.

For single quotes in args like "I'm Groot", use escape syntax: `'I'\''m Groot'`.

**Step 0 — Entry gate.** Read `plan.md`'s `Status:` header, or the approval
note the planning gate recorded. If the test plan has not been approved, halt
and say which artifact is waiting and what setting `Status: Approved` means.
`--force-gate` proceeds and records the override in `tasks.md`.

**Post-approval change check (constitution XIII).** Apply the same check to
**both** `spec.md` and `plan.md`: if either's `Status` reads `Approved` but
its `## Change Log` has a **Scope change**/**New requirement** entry with no
fresh `Approved by`/`Approved on` dated on or after it, halt and name the
specific entry — proceeding would build test cases on a basis whose own gate
was bypassed. A `Clarification`/`Correction` entry does not block. If test
cases already exist for a `TR-xxx` that a logged change touched, this run's
job is the targeted update Step 5 of constitution XIII describes, not a
wholesale re-generation — record the update in `tasks.md`'s own Change Log.

### Step 2: Load context

From `FEATURE_DIR`:

- **Required** `spec.md` — testable requirements (`TR-xxx`), scenarios,
  acceptance scenarios, edge cases, NFRs, risks
- **Required** `plan.md` — the manual/automated split, automation candidacy
  rules, target coverage, framework structure
- **Optional** `data-model.md` (test data), `research.md` (decisions),
  `quickstart.md`, `contracts/` (API contracts)
- **IF EXISTS** `.specify/memory/constitution.md`

### Step 3: Derive the test cases

For **every** scenario in `spec.md`, generate cases across these dimensions —
skipping a dimension is a decision you must be able to defend:

| Dimension | What to cover |
|-----------|---------------|
| Positive | Each acceptance scenario's happy path |
| Negative | Invalid input, wrong credentials, missing permissions, rejected states |
| Boundary | Min, min−1, max, max+1, empty, zero, maximum length |
| Data variation | Each equivalence class that behaves differently |
| Edge cases | Every row of `spec.md` §5 |
| NFR | Each measurable target in `spec.md` §8 |
| Compatibility | The browser/viewport matrix from `spec.md` §7, where behaviour can differ |

**Rules for each case**:

- **One case verifies one thing.** If the expected result needs the word "and"
  twice, split it.
- **Steps are actions a human could follow**, numbered, each with its own
  expected observation where meaningful.
- **The expected result is observable** — a state the tester can see, not an
  internal assumption.
- **Preconditions are explicit**, including the required data and role.
- **Every case cites at least one `TR-xxx`.** Where the source provides an
  acceptance-criterion id, the case also cites it in `acceptance_criteria` —
  that is what makes the chain start at the Jira AC rather than at `TR-xxx`.
  An untraced case violates
  constitution principle I; either trace it or delete it.
- **Priority is inherited from its requirement**, raised where risk justifies it.
- **Automatable** is decided using the candidacy rules in `plan.md` §B1, not by
  guesswork.
- **No secrets.** Reference a data alias (`example_user`), never a real
  credential.
- **A requirement classed UNDEFINED produces no asserting case.** It has no
  approved expected result, so writing one would fabricate the expectation that
  requirement analysis deliberately refused to invent (constitution II).
  Emit a placeholder instead: `automation_status: "Blocked"`, a
  `blocked_reason` naming the §13a question, and no `expected_result`. The
  requirement stays visible and uncovered, with the reason attached, rather
  than silently vanishing from the coverage matrix.

### Step 4: Write `test-cases.json`

Write `FEATURE_DIR/test-cases.json` in exactly this schema:

```json
{
  "ticket": "FLTIQ-1234",
  "feature": "Driver login",
  "generated": "YYYY-MM-DDTHH:MM:SS",
  "test_cases": [
    {
      "id": "TC-001",
      "title": "Valid credentials land the driver on the dashboard",
      "scenario": "S1",
      "requirements": ["TR-001"],
      "acceptance_criteria": ["TIA-AC-04"],
      "type": "Functional",
      "priority": "P1",
      "preconditions": ["An active driver account exists"],
      "steps": [
        {"action": "Open the login page", "expected": "Login form is visible"},
        {"action": "Enter valid credentials and submit", "expected": "Dashboard loads"}
      ],
      "expected_result": "Driver dashboard is displayed with the driver's name",
      "test_data": "example_user",
      "automatable": true,
      "automation_status": "Not Started",
      "test_file": "",
      "notes": ""
    }
  ]
}
```

Field rules:

- `generated` — the date and time this file's **content** was last written,
  not just first authored. Refresh it to the current timestamp whenever this
  file's test cases actually change — here, and in `/speckit-implement`
  Step 7 (which sets `automation_status`/`test_file`). **Do not** refresh it
  in `/speckit-test` — running the suite is a separate concern, tracked by
  each case's own `last_run`, and bumping `generated` on every execution
  would make the two fields indistinguishable.
- `id` — `TC-001` upward, unique, never reused across a feature
- `priority` — exactly `P1`, `P2` or `P3`
- `type` — Functional | UI | API | Data | Performance | Security | Accessibility | Compatibility
- `automation_status` — `Not Started` | `In Progress` | `Automated` | `Manual` | `Blocked`.
  Use `Manual` for cases the plan deliberately keeps manual.
- `acceptance_criteria` — the source acceptance-criterion ids this case covers
  (e.g. `["TIA-AC-04"]`). Use `[]` only when the source genuinely provides no
  explicit ids.
- `blocked_reason` — present only when `automation_status` is `Blocked`; names
  the §13a question the case waits on
- `test_file` — left empty here; `/speckit-implement` fills it in
- `steps` — non-empty; every step needs an `action`

### Step 5: Export to Excel

```bash
python3 .specify/scripts/python/export_testcases.py <FEATURE_DIR> --markdown
```

This validates the JSON, then writes `test-cases.xlsx` (sheets: Summary, Test
Cases, Steps, Traceability) and `test-cases.md`.

- The script **exits non-zero on invalid data** — fix the JSON and re-run; do
  not work around it.
- It **warns** about untraced cases. Treat every warning as a defect in your
  own output and resolve it.
- If it reports `openpyxl` missing, run `pip install -r requirements.txt` and
  retry.

### Step 6: Generate `tasks.md`

Use `TASKS_TEMPLATE_CONTENT` as the structure. This file is the **automation
work breakdown**, not a second copy of the test cases.

- **Phase 1 — Test Environment Setup**: dependencies, browsers, `.env`, a
  verified smoke run
- **Phase 2 — Framework Foundation** *(blocking)*: locators, page objects,
  test data files, fixtures this feature needs
- **Phase 3+ — One phase per scenario**, in priority order, each listing its
  goal, its `TC-xxx` ids and how the phase is independently verified
- **Final phase — Cross-cutting**: Allure metadata, cross-browser markers,
  accessibility checks, parallel-safety verification, traceability update
- **Manual Test Cases table**: every case with `automation_status: Manual`,
  with the reason

Every task follows the strict format:

```text
- [ ] [TaskID] [P?] [Story?] Description with file path (covers: TC-xxx)
```

- `- [ ]` checkbox, always
- `T001`, `T002`… sequential in execution order
- `[P]` only when parallel-safe (different files, no unmet dependency)
- `[S1]`, `[S2]`… on scenario-phase tasks only — never on Setup, Foundation or Polish
- An exact file path
- `(covers: TC-xxx)` on every scenario-phase task

Correct: `- [ ] T009 [P] [S1] Automate valid login in automation/tests/ui/test_login.py (covers: TC-001)`
Wrong: `- [ ] Automate login` — no id, no path, no coverage.

Finish `tasks.md` with the dependency graph, parallel opportunities, execution
strategy and the traceability table.

### Step 7: Validate coverage

Before reporting, verify and state the result of each:

- [ ] Every `TR-xxx` in `spec.md` maps to at least one test case
- [ ] Every **P1** requirement has at least one **P1** case
- [ ] Every scenario has positive **and** negative coverage
- [ ] Every edge case in `spec.md` §5 has a case
- [ ] Every NFR in `spec.md` §8 has a case or an explicit written waiver
- [ ] No case is untraced (the exporter reported zero warnings)
- [ ] Every automatable case has a task in `tasks.md`
- [ ] `test-cases.xlsx` regenerated from the current JSON

Any gap is reported to the user — never silently accepted.

### Step 8: Update the traceability seed

Fill the Test Cases column of `spec.md` §14, and the Jira AC column where the
source supplied acceptance-criterion ids. Update §3a's Status column so an
uncovered acceptance criterion is visible. Leave the Automation column for
`/speckit-implement`.

## Mandatory Post-Execution Hooks

**You MUST complete this section before reporting completion to the user.**

Check if `.specify/extensions.yml` exists in the project root.
- If it does not exist, or no hooks are registered under `hooks.after_tasks`, skip to the Completion Report.
- If it exists, read it and look for entries under the `hooks.after_tasks` key.
- If the YAML cannot be parsed or is invalid, do not skip silently: tell the user that `.specify/extensions.yml` could not be read (include the parser error) and that no hooks were checked, including any mandatory (`optional: false`) hooks registered there, then continue to the Completion Report.
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- When constructing command invocations from hook command names, replace dots (`.`) with hyphens (`-`). For example, `speckit.git.commit` → `/speckit-git-commit`.
- For each executable hook, output the following based on its `optional` flag:
  - **Mandatory hook** (`optional: false`) — **You MUST emit `EXECUTE_COMMAND:` for each mandatory hook**:
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session (the invocation may differ from the literal `{command}` id shown above, e.g. a skills-mode agent runs it as `/skill:speckit-...` or `$speckit-...`). Emitting the block alone does not run the hook.
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```

## Completion Report

Report:

- Paths: `test-cases.json`, `test-cases.xlsx`, `test-cases.md`, `tasks.md`
- Totals: cases overall, per priority, automated vs manual
- Cases per scenario
- Requirement coverage: n of n `TR-xxx` covered; name any that are not
- Automation task count and the MVP scope (usually Phase 1 → 2 → 3)
- Format validation: confirm every task has a checkbox, id, path and `covers:`
- Next phase: `/speckit-implement`

`tasks.md` must be immediately executable — each task specific enough to
complete without re-reading this conversation.

## Done When

- [ ] `test-cases.json` written and passing the exporter's validation
- [ ] `test-cases.xlsx` and `test-cases.md` generated with zero warnings
- [ ] `tasks.md` generated with every task in the strict format
- [ ] Coverage validation run and any gap reported
- [ ] `spec.md` §14 traceability updated with test case ids
- [ ] Extension hooks dispatched or skipped per the rules above
- [ ] Completion reported with counts, coverage and next phase
