---
name: "speckit-converge"
description: "STLC support — assess the automation suite against the test cases, plan and tasks, then append the remaining test work to tasks.md."
argument-hint: "Optional focus (e.g. 'P1 only', 'constitution compliance')"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  adapted-for: "STLC (Software Testing Life Cycle)"
  stlc-phase: "4b — Automation gap closure"
user-invocable: true
disable-model-invocation: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before convergence)**:

- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_converge` key
- If the YAML cannot be parsed or is invalid, do not skip silently: tell the user that `.specify/extensions.yml` could not be read (include the parser error) and that no hooks were checked, including any mandatory (`optional: false`) hooks registered there, then continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- When constructing command invocations from hook command names, replace dots (`.`) with hyphens (`-`). For example, `speckit.git.commit` → `/speckit-git-commit`.
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):

    ```text
    ## Extension Hooks

    **Optional Pre-Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```

  - **Mandatory hook** (`optional: false`):

    ```text
    ## Extension Hooks

    **Automatic Pre-Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}

    Wait for the result of the hook command before proceeding to the Goal.
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session (the invocation may differ from the literal `{command}` id shown above, e.g. a skills-mode agent runs it as `/skill:speckit-...` or `$speckit-...`). Emitting the block alone does not run the hook.

- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## Goal

Close the gap between the testing the artifacts call for and the testing that
actually exists. Read `spec.md`, `plan.md`, `test-cases.json` and `tasks.md` as
the **sole source of intent** (with the constitution as governing constraints),
assess the current state of `automation/`, determine which test cases, coverage
obligations, plan decisions and design rules are unmet, incomplete or only
partially satisfied, and **append each remaining piece of work as a new,
traceable task** at the bottom of `tasks.md` so `/speckit-implement` can finish it.

Run after `/speckit-implement` has worked through the current `tasks.md`.

This is **not** a diff tool. It assesses the present state of the test suite
against the feature's artifacts — no git, no branch comparison, no history.

**QA perspective, not product design.** The artifacts (`spec.md`, `plan.md`,
`test-cases.json`, `tasks.md`) define what "correct" means here — never
substitute your own idea of what the product should do when judging a gap or
a contradiction.

## Operating Constraints

**APPEND-ONLY, NEVER REWRITE**. The only write is a new
`## Phase N: Convergence` section at the end of `tasks.md`. It MUST NOT:

- modify `spec.md`, `plan.md` or `test-cases.json`;
- rewrite, renumber, reorder or delete any existing task (including tasks from a
  prior Convergence phase);
- modify, create or delete any test code — completing the appended tasks is
  `/speckit-implement`'s job;
- modify application code under any circumstances. The product under test is
  not this command's to change.

When everything is already satisfied, leave `tasks.md` **byte-for-byte
unchanged** (no empty Convergence header) and report a clean result.

**Constitution Authority**: `.specify/memory/constitution.md` is
non-negotiable. Test code violating a MUST principle is the highest-severity
finding and produces a remediation task. If the constitution is still an
unfilled template, skip those checks gracefully rather than failing.

## Execution Steps

### 1. Initialize

Run `.specify/scripts/bash/check-prerequisites.sh --json --require-spec --require-tasks --include-tasks`
once from the repo root; parse `FEATURE_DIR` and `AVAILABLE_DOCS`. Derive:

- `SPEC` = `FEATURE_DIR/spec.md`
- `PLAN` = `FEATURE_DIR/plan.md`
- `TASKS` = `FEATURE_DIR/tasks.md`
- `CASES` = `FEATURE_DIR/test-cases.json`
- `CONSTITUTION` = `.specify/memory/constitution.md` (if present)

If `spec.md`, `plan.md` or `tasks.md` is missing, STOP with an actionable
message naming the prerequisite command (`/speckit-specify`, `/speckit-plan`,
`/speckit-tasks`). Do not produce partial output. For single quotes in args like
"I'm Groot", use `'I'\''m Groot'`.

### 2. Load artifacts (progressive disclosure)

**From `spec.md`**: testable requirements (`TR-xxx`) with priority; scenarios
and their acceptance scenarios (`S1/AC2`); edge cases (§5); NFRs (§8); exit
criteria (§10).

**From `plan.md`**: the manual scope (§A3); automation candidacy rules and
target coverage (§B1); framework structure (§B3); design rules (§B4); test data
strategy (§B5); the quality gate (§B6).

**From `test-cases.json`**: every case with its priority, `automatable` flag,
`automation_status` and `test_file`.

**From `tasks.md`**: task ids (to compute the next id and phase number), phase
grouping, file paths, `covers:` clauses.

**From `automation/`**: which test functions exist, the `TC-xxx` each declares,
the page objects and locators present, and the markers applied.

**From the constitution** (unless it is an unfilled template): principle names
and MUST/SHOULD statements.

### 3. Build the intent inventory

Internal model only:

- **Obligation inventory** — one stable key per `TC-xxx` that should be
  automated, per acceptance scenario (`S1/AC2`), per NFR needing verification,
  plus the plan decisions and constitution principles that impose work.
- **Suite-scope map** — from the file paths named in `plan.md` §B3 and in
  `tasks.md`, plus a search for the concepts each case describes, derive the set
  of test files, page objects and locator modules in scope. Bound the assessment
  to these — do not infer scope beyond the artifacts. If a named path does not
  exist on disk, try resolving it by filename against the current automation
  tree before treating the obligation as `missing` — a feature planned before a
  framework restructure will name pre-restructure paths.

### 4. Assess the suite and classify findings

For each obligation, inspect the current test code and produce a `Finding` only
where a gap exists. Classify by **gap type**:

- **`missing`** — no test implements this case at all
- **`partial`** — a test exists but does not fully verify the case: steps
  skipped, only the happy path asserted, an assertion weaker than the stated
  expected result, or a marker/`TC-xxx` id absent
- **`contradicts`** — the code conflicts with stated intent or a MUST
  principle: a page object that asserts, a `time.sleep`, an inline locator, a
  hard-coded credential, a test depending on another test's state, an assertion
  that contradicts the case's expected result
- **`unrequested`** — test code not called for by any case, task or plan
  decision (surfaced for awareness — converge never deletes; it appends a task
  to justify or remove it)

Each `Finding` records a stable id, its `source-ref`, the `gap-type`, a
severity, and a short description with the evidence observed.

**Suite-specific checks worth running explicitly**:

- A case marked `Automated` in `test-cases.json` whose `test_file` resolves to nothing
- A test function with no `@allure.testcase` id — invisible in traceability
- A scenario with a positive test but no negative test
- A boundary listed in `spec.md` §5 with no corresponding assertion anywhere
- Coverage below the target stated in `plan.md` §B1
- Tests that cannot pass in parallel or depend on execution order

**Blocked obligations are not gaps.** A requirement classed `UNDEFINED` in
`spec.md` §3, or a test case whose `automation_status` is `Blocked`, has no
approved expected result. It is a **blocked obligation**: list it under
*Blocked (pending clarification)* with the §13a question it waits on, and
**do not append a task to automate it**. Appending such a task would ask the
next phase to invent the expectation that requirement analysis deliberately
refused to invent (constitution II). Blocked obligations are excluded from the
coverage denominator.

**Edge cases**:

- **Little or no test code yet** — treat the whole specified scope as `missing`
  remaining work rather than failing
- **Nothing remains** — produce zero findings and follow the converged branch

### 5. Assign severity

- **CRITICAL** — violates a constitution MUST principle, or a
  `missing`/`contradicts` gap on a **P1** test case
- **HIGH** — a `missing` or `partial` gap on a core test case or acceptance
  scenario; automation coverage below the plan's P1 target
- **MEDIUM** — a `partial` gap on a secondary case, a missing marker or Allure
  id, or an `unrequested` test with unclear justification
- **LOW** — minor partial gaps, polish, low-risk unrequested additions

### 6. Present the findings summary

Before appending anything, output a severity-graded summary — no file writes yet:

## Convergence Findings

| ID | Gap Type | Severity | Source | Evidence | Remaining Work |
|----|----------|----------|--------|----------|----------------|
| F1 | missing | CRITICAL | TC-004 (P1) | No test found for the invalid-password path | Automate TC-004 in automation/tests/ui/test_login.py |
| F2 | contradicts | CRITICAL | Constitution V | `LoginPage.sign_in` asserts on the dashboard heading | Move the assertion into the test |

**Summary metrics**:

- Test cases checked / automatable / automated
- Acceptance scenarios checked
- Plan decisions checked
- Constitution principles checked (or "skipped — template")
- Findings by gap type (missing / partial / contradicts / unrequested)
- Findings by severity
- Automation coverage: actual % vs the `plan.md` §B1 target

### 7. Append convergence tasks (or report converged)

**If there are actionable findings** (`tasks_appended`):

1. Scan all existing task ids; let `M` be the maximum. Determine the next phase
   number `N` (highest existing + 1).
2. Write a single header `## Phase N: Convergence`.
3. Emit one checklist item per actionable finding, CRITICAL/HIGH first, with
   zero-padded ids `T{M+1:03d}, T{M+2:03d}, …`:

   ```markdown
   - [ ] T042 <imperative description> in <file path> per <source-ref> (<gap-type>) (covers: TC-xxx)
   ```

   `<source-ref>` traces the task: `TC-004`, `TR-003`, `S1/AC2`,
   `plan: §B1 coverage target`, `Constitution V`.
   `<gap-type>` is `missing`, `partial`, `contradicts` or `unrequested`.
   Include `(covers: TC-xxx)` whenever the task maps to a case.
   Constitution-violation tasks come first, described as `CRITICAL`.
4. Never reuse or renumber existing ids. If a prior Convergence phase exists,
   add a new, separately-numbered one below it — do not touch the old one.

**If there are no actionable findings** (`converged`):

- Do **not** modify `tasks.md` at all — no empty phase header
- Report: **"✅ Converged — the test suite satisfies the test cases, plan and tasks."**
- Include the summary counts that justify that claim

### 8. Next actions

- On `tasks_appended`: state how many tasks were appended under which phase,
  recommend `/speckit-implement`, and note that a follow-up converge run will
  find fewer or no remaining items.
- On `converged`: recommend `/speckit-test` for a full execution cycle and the
  Go/No-Go verdict. No further implement pass is needed for this scope.

### 9. Check for extension hooks

After producing the result, check if `.specify/extensions.yml` exists in the project root.

- If it exists, read it and look for entries under the `hooks.after_converge` key
- If the YAML cannot be parsed or is invalid, do not skip silently: tell the user that `.specify/extensions.yml` could not be read (include the parser error) and that no hooks were checked, including any mandatory (`optional: false`) hooks registered there, then continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- Report the convergence outcome (`converged` or `tasks_appended`) in-session before listing
  any hooks, so users can decide whether to run optional follow-up commands.
- When constructing command invocations from hook command names, replace dots (`.`) with hyphens (`-`). For example, `speckit.git.commit` → `/speckit-git-commit`.
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):

    ```text
    ## Extension Hooks

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```

  - **Mandatory hook** (`optional: false`):

    ```text
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session (the invocation may differ from the literal `{command}` id shown above, e.g. a skills-mode agent runs it as `/skill:speckit-...` or `$speckit-...`). Emitting the block alone does not run the hook.

- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently
