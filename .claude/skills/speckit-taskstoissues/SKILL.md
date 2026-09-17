---
name: "speckit-taskstoissues"
description: "STLC support — turn automation tasks in tasks.md into tracker issues (Jira via Atlassian MCP, or GitHub), with test-case traceability."
argument-hint: "Optional filter, label, or target (e.g. 'phase 3 only', 'github', 'jira')"
compatibility: "Requires spec-kit project structure with .specify/ directory and a connected tracker MCP server"
metadata:
  author: "github-spec-kit"
  adapted-for: "STLC (Software Testing Life Cycle)"
  stlc-phase: "3b — Work tracking handoff"
user-invocable: true
disable-model-invocation: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before tasks-to-issues conversion)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_taskstoissues` key
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

Turn the automation tasks in `tasks.md` into tracker issues so the testing work
is visible alongside the development work, with each issue carrying the test
cases it covers.

**QA perspective, not product design.** These issues track *testing* work
(automating a case) — never rephrase a task as a product change request or
infer product behaviour that isn't already stated in `test-cases.json` or
`spec.md`.

> **Creating issues writes to a shared tracker and is not cleanly reversible.**
> You MUST show the user the full list of issues you intend to create and get an
> explicit "yes" before creating any of them. Approval for one run never carries
> to the next.

### 1. Load context

Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks`
from the repo root; parse `FEATURE_DIR` and `AVAILABLE_DOCS`. All paths
absolute. For single quotes in args like "I'm Groot", use `'I'\''m Groot'`.

Then load:

- `tasks.md` — the tasks to convert
- `test-cases.json` (if present) — so each issue can carry its case titles,
  priorities and expected results
- `spec.md` (if present) — for the ticket key and requirement ids
- **IF EXISTS** `.specify/memory/constitution.md`

### 2. Choose the target tracker

| Signal | Target |
|--------|--------|
| User says "jira", or `spec.md` carries a Jira ticket key | **Jira** via the Atlassian MCP server |
| User says "github" | **GitHub** via the GitHub MCP server |
| Neither stated | Prefer Jira when a Jira key exists in `spec.md`, otherwise GitHub |

Locate the tracker's tools with `ToolSearch` — they are usually deferred. Try
`jira issue atlassian` or `github issue` as keyword queries and use whatever
tool names come back.

If the chosen tracker's MCP server is not available, say so plainly, name the
other option if it is available, and stop. Do not fall back silently to a
different tracker than the user expects.

### 3. Parse the tasks

Task lines start with a markdown checkbox. Strip the leading `- [ ]` and any
`[P]` / `[S#]` markers to recover the id and description. Each id is a `T`
followed by **at least** three digits (`T001`) — `/speckit-converge` assigns new
ids with `T{M+1:03d}`, which is a floor rather than a cap, so a file with more
than 999 tasks has four-digit ids.

For each task also capture:

- Its phase heading (Setup / Foundation / Scenario N / Polish / Convergence)
- The file path in the description
- The `(covers: TC-xxx)` clause, if present
- Whether it is already `[X]` — **skip completed tasks** unless the user asks
  for all of them

Apply any filter the user gave (a phase, an id range, a priority).

### 4. Deduplicate against existing issues

Before creating anything, build the set of task ids you are about to process,
then check which already have issues.

**Jira**: search the project with JQL for the feature's ticket key or a task-id
token in the summary, e.g. `project = FLEETIQ AND summary ~ "T001"`. Prefer one
broader query over many narrow ones — search for the feature key and match
locally.

**GitHub**: use the `list_issues` tool. Do **not** pass a `state`, so both open
and closed issues come back. Request `perPage: 100`, and page with the `after`
parameter using the previous response's `endCursor`.

Match each issue title against the task-id pattern `\bT\d{3,}\b`. The `{3,}`
accepts four-digit and longer ids — with `\d{3}` a title containing `T1000`
would not match at all, because the trailing `\b` cannot fall between two
digits, so that task would be silently neither deduplicated nor created. The
word boundaries also stop a token like `ST001` from matching and force the whole
digit run to be consumed, so `T100` can never match inside `T1000`. This
recognises titles written as `T001 ...`, `T001: ...` and `[T001] ...`.

Stop paginating once every task id is matched, or when there are no more pages,
so you do not walk the tracker's whole history unnecessarily.

### 5. Compose the issues

For each task without an existing issue:

**Title**: `T001: <description>` — the id once, then the description.
So `- [ ] T001 Create project structure` becomes `T001: Create project structure`.

**Body**:

```markdown
**Automation task** from `specs/<feature-dir>/tasks.md`

**Phase**: Scenario 1 — Driver signs in
**File**: `automation/tests/ui/test_login.py`

**Test cases covered**:
| TC | Title | Priority |
|----|-------|----------|
| TC-001 | Valid credentials land the driver on the dashboard | P1 |

**Requirements**: TR-001
**Feature ticket**: FLTIQ-1234

**Definition of done**
- [ ] Test implemented following the POM rules in `plan.md` §B4
- [ ] Carries its `@allure.testcase` id and priority marker
- [ ] Passes in parallel with no order dependence
- [ ] `test-cases.json` updated: `automation_status` and `test_file`
```

Pull the case titles and priorities from `test-cases.json` — do not invent them.
Omit any section whose source data is absent rather than filling it with
placeholders.

**Labels / fields**:

- GitHub: label with the phase (`setup`, `foundation`, `scenario-1`, `polish`)
  and the highest priority among the covered cases (`p1`/`p2`/`p3`), plus any
  label the user asked for
- Jira: issue type `Task` (or `Sub-task` under the feature ticket when the user
  wants that), priority mapped from the covered cases, and a link to the feature
  ticket

### 6. Confirm, then create

Present the full list before creating anything:

```text
About to create N issues in <tracker> <project/repo>:

  T009: Automate valid login in automation/tests/ui/test_login.py       [P1, covers TC-001]
  T010: Automate invalid password in automation/tests/ui/test_login.py  [P1, covers TC-002, TC-003]

Skipping 2 tasks that already have issues: T001, T002
Skipping 4 completed tasks: T003-T006

Proceed?
```

Create issues **only after an explicit yes**. Then create them one at a time and
report each result as it lands.

> **Never create issues in a project or repository that does not match the
> resolved target.** For GitHub, resolve the target from
> `git config --get remote.origin.url` and proceed only if it is a GitHub URL.
> For Jira, use the project derived from the feature's ticket key, and confirm
> the project key with the user if it cannot be derived.

### 7. Report

- Tracker and project/repository used
- Issues created, with their keys/numbers and titles
- Tasks skipped because an issue already existed
- Tasks skipped because they are complete
- Any task that failed to create, and why
- Test cases now tracked, and any automatable case with **no** task and
  therefore no issue — that gap belongs back in `/speckit-tasks`

## Post-Execution Checks

**Check for extension hooks (after tasks-to-issues conversion)**:
Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.after_taskstoissues` key
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

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Mandatory hook** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session (the invocation may differ from the literal `{command}` id shown above, e.g. a skills-mode agent runs it as `/skill:speckit-...` or `$speckit-...`). Emitting the block alone does not run the hook.
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently
