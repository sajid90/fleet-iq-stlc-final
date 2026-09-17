---
name: "speckit-implement"
description: "STLC Phase 4 — Test Automation. Implement the test cases as Python/pytest/Playwright POM code."
argument-hint: "Optional filter (e.g. 'phase 3 only', 'T009-T012')"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  adapted-for: "STLC (Software Testing Life Cycle)"
  stlc-phase: "4 — Test Automation Development"
user-invocable: true
disable-model-invocation: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before implementation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_implement` key
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

You are performing **STLC Phase 4 — Test Automation Development**. You turn the
tasks in `tasks.md` into working Python + pytest + Playwright code following the
Page Object Model.

You are writing **tests**, not application code. The product under test is not
yours to change.

**QA perspective, not product design.** Assert against what `test-cases.json`
and `spec.md` say the product actually does — never adjust an assertion
because you assume the product "should" behave differently. A test failing
against real behaviour is evidence for Step 6's defect report, not a cue to
redesign the check.

### Step 1: Prerequisites

Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks`
and parse `FEATURE_DIR` and `AVAILABLE_DOCS`. All paths are absolute.

If `tasks.md` is missing or has no tasks, stop and tell the user to run
`/speckit-tasks` first.

**Step 0 — Entry gate.** Test cases must have been reviewed and approved before
automation starts. If `test-cases.json` has not been through the test-case gate,
halt and say so. `--force-gate` proceeds and records the override in `tasks.md`.

### Step 2: Load context

- **Required** `tasks.md` — the work breakdown, phases, dependencies, `[P]` markers
- **Required** `plan.md` — stack, framework structure, design rules (§B3, §B4)
- **Required** `test-cases.json` — the exact steps and expected results each
  test must verify. Implement what the case says, not what you would have tested.
- **Required** `spec.md` — the requirements behind the cases
- **IF EXISTS** `source-manifest.json` — the approved source set. Do not
  implement behaviour that contradicts it, and do not resolve a recorded
  conflict by choosing a side in test code.
- **IF EXISTS** `data-model.md`, `research.md`, `quickstart.md`, `contracts/`
- **IF EXISTS** `.specify/memory/constitution.md`

### Step 3: Verify the framework

Confirm the automation skeleton exists before writing feature tests. The
table below is the repo default; `plan.md` §B3 is authoritative for this
feature's exact paths.

| Path | Purpose |
|------|---------|
| `requirements.txt` | pinned dependencies |
| `pytest.ini` | markers, Allure results dir, artifact settings, `testpaths` |
| `automation/conftest.py` | settings, context args, failure evidence — global fixtures only |
| `automation/utils/` | `base_page.py` (POM base), `config.py`, `logger.py`, `data_loader.py` |
| `automation/pages/` | page objects — one file per feature |
| `automation/locators/` | locator constants |
| `automation/test_data/` | static test data |
| `automation/tests/ui/` | UI tests, with `automation/tests/ui/conftest.py` for page-object fixtures |
| `automation/tests/api/` | API tests (only if the feature has an API surface — see `contracts/`) |

If a **layer** in the table is absent, **stop and report it — do not
scaffold it.** Creating or renaming a framework layer is a framework change
requiring a human decision and a foundation task in `tasks.md`. Only files
*inside* an existing layer are yours to create. Never create a second
automation root. Then verify the toolchain:

```bash
pip install -r requirements.txt
playwright install chromium
python3 -m pytest --collect-only -q
```

Collection must succeed before you write a single feature test.

### Step 4: Implement, phase by phase

Work through `tasks.md` in order. Complete each phase before starting the next.

- **Never implement a case whose `automation_status` is `Blocked`.** It waits
  on a clarification and has no approved expected result; report it and move on.
- Respect dependencies: sequential tasks in order; `[P]` tasks may proceed together
- Tasks touching the same file are always sequential
- **Mark each finished task `[X]` in `tasks.md` as you go** — not in a batch at the end
- Report progress after each task

### Step 5: Code rules

These are enforced by the constitution. Violating one is a defect even if the
test passes.

**Layering**

- **One feature owns exactly one file per layer.** A feature named
  `<feature>` gets `automation/pages/<feature>_page.py`,
  `automation/locators/<feature>_locators.py`,
  `automation/test_data/<feature>.json`, and
  `automation/tests/ui/test_<feature>.py` (or `tests/api/` for an API-level
  feature). Never split one feature's page object, locators or test data
  across multiple files, and never let two features share one.
- **Locators** live in `automation/locators/<feature>_locators.py` as class
  constants *(illustrative — `plan.md` §B3 gives this feature's exact
  path)*. Never inline a selector in a test or a page object method body.
- **Page objects** live in `automation/pages/<feature>_page.py`, extend
  `BasePage` (`automation.utils.base_page`), expose user intent
  (`checkout_page.apply_coupon(code)`), and return page objects or plain
  data. **A page object never asserts.**
- **Tests** live in `automation/tests/ui/test_<feature>.py` for a
  browser-driven UI journey, or `automation/tests/api/test_<feature>.py` for
  an API-level check with no browser — both hold every assertion. Register
  any new page-object fixture in `automation/tests/ui/conftest.py`, never in
  the root `automation/conftest.py`.

**Selectors** — priority order: `get_by_role` → `get_by_label` →
`data-testid` → CSS. XPath only as a last resort with a comment explaining why.
If the UI offers no stable hook, add a task to request `data-testid` from
development rather than writing a brittle selector.

**Waiting** — Playwright auto-waiting and web-first assertions (`expect(...)`)
only. `time.sleep` is banned. Timeouts come from settings, never hard-coded in
a test.

**Independence** — each test sets up and tears down its own state, and passes
in any order and in parallel. No shared mutable state between tests.

**Naming and traceability** — one test function per test case:

```python
@allure.epic("FleetIQ")
@allure.feature("Authentication")
@allure.story("Driver signs in")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("TC-001: Valid credentials land the driver on the dashboard")
@allure.testcase("TC-001")
@pytest.mark.smoke
@pytest.mark.p1
def test_tc001_valid_login(self, login_page):
    ...
```

- Function name: `test_<tcid>_<behaviour>`
- `@allure.title` carries the test case title verbatim
- `@allure.testcase` carries the `TC-xxx` id
- Priority marker matches the case's priority (`p1`/`p2`/`p3`)
- Type markers (`smoke`, `regression`, `negative`, `boundary`, `a11y`) match
  the case
- Every marker used must already be declared in `pytest.ini`

**Data** — from `automation/test_data/<feature>.json` via
`automation.utils.data_loader`, or generated for unique entities. Never a
literal credential in a test file.

**Steps** — the page-object calls should read in the same order as the case's
steps, so the Allure report mirrors the manual script.

### Step 6: Verify as you go

After each phase, run the tests you just wrote:

```bash
.specify/scripts/bash/run-tests.sh -k automation/tests/ui/test_<feature>.py
```

- A test that fails because the **product** is wrong is a finding: keep the
  test, report it, and raise it as a defect. **Never weaken an assertion to
  make a test pass.**
- A test that fails because the **test** is wrong: fix the test.
- A test that passes only sometimes is not done. Fix the determinism before
  moving on — do not paper over it with `--reruns`.

Then confirm parallel safety once the phase is complete:

```bash
.specify/scripts/bash/run-tests.sh -k automation/tests/ui/test_<feature>.py -n auto
```

### Step 7: Update traceability

When a case becomes automated, update `test-cases.json`:

- `automation_status` → `"Automated"`
- `test_file` → the node id, e.g. `"automation/tests/ui/test_login.py::TestLogin::test_tc001_valid_login"`
- `generated` → the current date and time (`YYYY-MM-DDTHH:MM:SS`) — this field
  tracks when the file was last written, not just first authored, so refresh
  it whenever you rewrite the file

Then regenerate the workbook so the deliverable does not drift:

```bash
python3 .specify/scripts/python/export_testcases.py <FEATURE_DIR> --markdown
```

Finally, fill the Automation column of `spec.md` §14.

### Step 8: Error handling

- If implementation evidence exposes a contradiction in the approved
  requirements or source artifacts, classify it as a **Requirement Defect**,
  stop the affected task, and return it to `/speckit-clarify`. Do not change
  the test expectation silently to make the contradiction go away.
- Halt on a failing non-parallel task; report the error with its actual output
- For `[P]` tasks, continue with the ones that succeeded and report the ones
  that failed
- Never mark a task `[X]` unless its tests actually run and behave as intended
- If you cannot proceed, say exactly what is blocking and what would unblock it

## Mandatory Post-Execution Hooks

**You MUST complete this section before reporting completion to the user.**

Check if `.specify/extensions.yml` exists in the project root.
- If it does not exist, or no hooks are registered under `hooks.after_implement`, skip to the Completion Report.
- If it exists, read it and look for entries under the `hooks.after_implement` key.
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

- Tasks completed vs total, per phase
- Test files created or modified
- Page objects, locators and fixtures added
- Test cases now `Automated`, and any still `Not Started` or `Blocked` with the reason
- Actual suite result from the last run — pass/fail counts, quoted, not summarised away
- Any product defect the new tests uncovered
- Any constitution deviation and its justification
- Next phase: `/speckit-test` for a full execution cycle and Allure report

## Done When

- [ ] Every task in scope completed and marked `[X]` in `tasks.md`
- [ ] Tests follow the POM boundary, selector priority and naming rules
- [ ] Every automated test carries its Allure metadata and `TC-xxx` id
- [ ] The suite passes, in parallel, with no order dependence — or failures are reported as findings
- [ ] `test-cases.json` updated and `test-cases.xlsx` regenerated
- [ ] `spec.md` §14 automation column filled
- [ ] Extension hooks dispatched or skipped per the rules above
- [ ] Completion reported with real test output
