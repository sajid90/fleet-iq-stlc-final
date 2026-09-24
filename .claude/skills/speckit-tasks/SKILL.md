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
| Edge cases | Every row of `spec.md` §5, unless §12 classifies it INFERRED with no distinct product requirement — see the waiver rule below |
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
- **Every case cites at least one `TR-xxx` that actually establishes the
  behaviour being asserted** — not merely a nearby or thematically related
  one. A case testing X may cite only a `TR-xxx` whose own text states X; if
  no requirement does, the case doesn't belong in this file (see the waiver
  rule below), and reaching for the closest-sounding `TR-xxx` to satisfy the
  citation rule is exactly the failure this note exists to prevent. Where the
  source provides an acceptance-criterion id, the case also cites it in
  `acceptance_criteria` — that is what makes the chain start at the Jira AC
  rather than at `TR-xxx`. An untraced case violates constitution principle I;
  either trace it properly or delete it.
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
- **An edge case in `spec.md` §5 that §12 classifies INFERRED with "not a
  distinct product requirement" produces no case at all — not even a boundary
  or negative one.** Constitution II is explicit: INFERRED means test
  mechanics only, never an expected result. Writing a full asserting case for
  one anyway is fabricating a requirement nobody stated — indistinguishable
  from testing the browser/framework rather than the product (e.g. asserting
  that an `<a href="#section">` scrolls to its anchor, which is guaranteed by
  the HTML standard, not a FleetIQ decision). If the row is genuinely a
  boundary/combination of an *already-DEFINED* requirement (e.g. two existing
  P1 requirements' boundary values combined), it still earns a real case,
  citing those requirements — the bar is whether a source establishes the
  behaviour at all, not whether the row happens to sit in the Edge Cases
  table. Where it doesn't, add one sentence to that row of `spec.md` §5 itself
  stating the waiver and why, and move on — do not manufacture a citation to
  an unrelated `TR-xxx` just to make the coverage checklist pass.

### Step 3.5: Pre-write validation gate (mandatory, per case and as a final sweep)

This is the last hard stop before anything reaches `test-cases.json`
(constitution I). For **every** candidate case, before it is added, confirm
each of the following in order:

1. Identify the scenario it belongs to.
2. Identify the `TR-xxx` it cites.
3. Read that `TR-xxx`'s **exact text** in `spec.md` §3 — not a memory of it.
4. Identify the source that `TR-xxx` itself cites (its Authority/source id).
5. Identify the acceptance-criterion id, if the source provides one.
6. Confirm the case's `expected_result` is explicitly supported by that
   `TR-xxx`'s own text — not adjacent to it, not a plausible extension of it.
7. Confirm the case does not rely on a nearby or thematically similar
   `TR-xxx` that doesn't actually establish this behaviour.
8. Confirm the behaviour is not merely inferred, assumed, or "generally how
   this kind of page/flow works" — if it is, it belongs in the INFERRED
   test-mechanics bucket at most, never as an expected result (constitution
   II).

**If any step fails, do not generate the test case.** Specifically:

- Do **not** solve the gap by attaching a nearby or thematically similar `TR-xxx`.
- Do **not** create a new `TR-xxx` to justify the test.
- Do **not** silently reclassify an UNDEFINED requirement as DEFINED to make
  the case writable.
- Do **not** add the case to `test-cases.json`.

Instead, report it as an **untraceable test candidate**:

```markdown
## Untraceable Test Candidate: [proposed title]

**Why it looked worth testing**: [one sentence]
**Missing link**: [no TR-xxx covers this / TR-xxx exists but doesn't state this / no source backs the cited TR-xxx]
**Classification**: UNDEFINED
**Next step**: raise as a clarification/open question in spec.md §13, via /speckit-clarify — not written here
```

**Final sweep — no orphan tests.** Before writing `test-cases.json`, walk every
case one more time and confirm the full chain:

```
TC-xxx  ->  TR-xxx  ->  Source  ->  Jira / Epic / PRD / Decision / Design / Linked Issue
```

Any case where a link is missing is **rejected** at this point, not patched
with a borrowed citation — remove it and report it as above.

**Clause-level coverage, not just row-level.** Before treating any `TR-xxx`
as covered, decompose its own §3 text into every distinct element or clause
it names — a list ("the product mark, the section anchors, and the Sign in /
Create account controls") or a compound sentence joined by "and" is naming
**more than one thing**, not one. Confirm each named element has at least one
case citing this `TR-xxx` — not just that the `TR-xxx` as a whole has *a*
case. A `TR-xxx` with cases covering 2 of its 3 named elements is **partially
covered**, which reads identically to "covered" in every existing check
(constitution I's "no test without a requirement" is satisfied technically,
while a named element has zero coverage) — this is exactly how FLTIQ-62's
"Capabilities"/"Hierarchy" nav links went missing: TR-003 had cases, just not
one for every element TR-003 itself names. Where a named element has no case
and no explicit waiver in `spec.md` (e.g. it was folded into an edge case's
INFERRED waiver without its own DEFINED facts split out first), report it the
same way as an untraceable candidate — but phrased as a **gap**, not an
invention: `**Missing element coverage**: TR-xxx names "[element]" with no
case asserting it` — and add the case, since the source already establishes it.

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

**The traceability table lists every `TR-xxx` *and* every `EC-xxx` from
`spec.md` §5 — exhaustively, in one pass, not one row at a time as each
happens to come up later.** A table that only grows when something is being
fixed will under-represent everything that was already correct from the
start — this is exactly how FLTIQ-62's table ended up listing 4 of its 6
edge cases: the two that never needed a fix never got a row, even though
both had real coverage from day one. Build the full row set now, in this
step, from the complete list of `TR-xxx`/`EC-xxx` ids in `spec.md` — never
defer a row to "whenever that item next comes up."

### Step 7: Validate coverage

Before reporting, verify and state the result of each:

- [ ] Every `TR-xxx` in `spec.md` maps to at least one test case
- [ ] Every distinct element/clause a `TR-xxx` names in its own text has a case, not just the `TR-xxx` as a whole (clause-level coverage)
- [ ] Every **P1** requirement has at least one **P1** case
- [ ] Every scenario has positive **and** negative coverage
- [ ] Every edge case in `spec.md` §5 has a case, or — for one §12 classifies INFERRED with no distinct product requirement — an explicit waiver written into that row instead
- [ ] Every NFR in `spec.md` §8 has a case or an explicit written waiver
- [ ] No case is untraced (the exporter reported zero warnings)
- [ ] Every case passed the Step 3.5 pre-write gate — none cites a borrowed/unrelated `TR-xxx`, none rests on an unsupported assumption, and any untraceable candidate was reported and excluded, not written in anyway
- [ ] Every automatable case has a task in `tasks.md`
- [ ] `tasks.md`'s own Traceability table lists every `TR-xxx` *and* every `EC-xxx` from `spec.md` — not only the ones a fix happened to touch (count both lists and compare, don't eyeball it)
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
- Untraceable test candidates found and excluded (Step 3.5), if any, with the
  missing link named for each
- Next phase: `/speckit-implement`

`tasks.md` must be immediately executable — each task specific enough to
complete without re-reading this conversation.

## Done When

- [ ] Every case passed the Step 3.5 pre-write gate; no orphan or borrowed-`TR-xxx` case reached `test-cases.json`
- [ ] `test-cases.json` written and passing the exporter's validation
- [ ] `test-cases.xlsx` and `test-cases.md` generated with zero warnings
- [ ] `tasks.md` generated with every task in the strict format
- [ ] Coverage validation run and any gap reported
- [ ] `spec.md` §14 traceability updated with test case ids
- [ ] Extension hooks dispatched or skipped per the rules above
- [ ] Completion reported with counts, coverage and next phase
