---
name: "speckit-plan"
description: "STLC Phase 2 — Test Planning. Produce the manual test strategy and the technical plan for automation."
argument-hint: "Optional planning guidance (e.g. 'API only', 'cross-browser matters here')"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  adapted-for: "STLC (Software Testing Life Cycle)"
  stlc-phase: "2 — Test Planning"
user-invocable: true
disable-model-invocation: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before planning)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_plan` key
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

You are performing **STLC Phase 2 — Test Planning**. You produce one document
with two halves that are equally mandatory:

- **Part A — Manual Test Strategy**: levels, types, what stays manual and why,
  exploratory charters, cycles, environment, schedule, deliverables.
- **Part B — Automation Technical Plan**: the engineering design for the
  Python + pytest + Playwright + POM suite that will implement the automatable
  portion.

A plan that fills only one half is incomplete. The split between manual and
automated is a **decision you must make and defend**, not an omission.

**QA perspective, not product design.** `spec.md` is the resolved test basis —
treat its requirements and observed/assumed behaviours as fact, not as open
product questions to relitigate here. This plan decides how to *test* the
product, never how the product should *behave*; if something about actual
behaviour is still unclear, that belongs back in `/speckit-clarify`, not a
design call made mid-plan.

### Step 1: Setup

Run `.specify/scripts/bash/setup-plan.sh --json` from the repo root and parse
`FEATURE_SPEC`, `IMPL_PLAN`, `FEATURE_DIR`, `BRANCH`. The script copies the
STLC plan template into place.

For single quotes in args like "I'm Groot", use escape syntax: `'I'\''m Groot'`
(or double-quote when possible).

### Step 2: Load context

- **Required**: `FEATURE_SPEC` (`spec.md`) — the test basis. Read every `TR-xxx`,
  scenario, edge case, NFR and risk, **plus each requirement's Class and
  Authority** (schema 2.0).
- **IF EXISTS** `source-manifest.json` — the approved source set. The plan may
  not silently introduce a source the spec never approved, and may not
  contradict a resolved conflict.
- **IF EXISTS** the approved design artifact — it drives UI, responsive and
  accessibility coverage planning.
- **Required**: `.specify/memory/constitution.md` — the QA principles this plan
  is graded against.
- The `IMPL_PLAN` template already copied by the setup script.
- **IF EXISTS**: the existing `automation/` framework — read `pytest.ini`,
  `automation/conftest.py`, `automation/utils/base_page.py` so the plan
  reflects what is actually there rather than proposing a parallel structure.

**Step 0 — Entry gate.** Read `spec.md`'s `Status:` header. If it is not
`Approved`, halt and say:
> `<FEATURE_DIR>/spec.md` is `<Status>`. Test planning is gated on human
> approval of the requirement analysis. Review `spec.md` and
> `source-manifest.json`, then set `Status: Approved` (adding `Approved by` and
> `Approved on`), or re-run me with `--force-gate` to proceed and record the
> override.

With `--force-gate`, add a `## Gate Overrides` block to `plan.md` naming the
gate, the date and the reason. An audited override beats an unenforceable rule.

If `spec.md` still contains an unresolved §13a blocking item against a P1
requirement, stop and tell the user to run `/speckit-clarify` first.

### Step 3: Phase 0 — Research and decisions

Resolve every unknown before designing. Produce `FEATURE_DIR/research.md`.

Research tasks come from:

- Any `NEEDS CLARIFICATION` in the Technical Context you are filling
- Each technology or integration the feature touches (auth mechanism, third
  party sandbox, file upload, websockets, payment provider)
- Each NFR that needs a measurement approach (how do we actually measure p95?
  which accessibility ruleset?)
- Each testability gap raised in `spec.md` §11 (does the UI expose stable
  hooks, or must we request `data-testid` attributes from development?)

Classify each unknown by how it was settled:

- **Resolved by source** — an approved source answers it; cite the source
- **Resolved by repository** — the existing framework or a running system
  answers it; cite the evidence
- **Needs clarification** — nothing settles it; it stays open and, if it
  affects a P1 requirement, it blocks

Record each finding as:

- **Decision**: what was chosen
- **Rationale**: why
- **Alternatives considered**: what else was evaluated and why it lost

**Output**: `research.md` with no unresolved unknowns.

### Step 4: Part A — Manual test strategy

Fill sections A1–A8 of the template:

- **A1 Objectives** — each tied to a `TR-xxx` or a risk from `spec.md` §9.
- **A2 Test levels & types** — which levels are in play and who owns them.
  Delete rows that do not apply rather than marking them N/A.
- **A3 Manual scope** — what stays manual and *why*, with effort estimates.
  Legitimate reasons: subjective/visual judgement, one-off migration checks,
  exploratory discovery, blocked by a missing test hook, cost exceeds value.
  "We ran out of time" is a schedule note, not a strategy.
- **A4 Exploratory charters** — explore *what*, with *what*, to discover *what
  risk*. Derive them from the high-risk rows in `spec.md` §9.
- **A5 Execution approach** — cycles, defect workflow and severity scale,
  suspension and resumption criteria.
- **A6 Environment** — URLs, roles, data seeding, integration stubs. Reference
  where secrets live; never write a credential into this file.
- **A7 Schedule, effort, roles**.
- **A8 Deliverables** — the checklist of artifacts this feature will produce.

### Step 5: Part B — Automation technical plan

Fill sections B1–B7:

- **A0 Carry-forward and blocked requirements** — a compact table of
  `TR-xxx | Class | Authority | source id` copied from `spec.md` §3, so a
  reviewer can judge this plan without re-reading the spec (constitution III).
  Below it, a **Blocked requirements register**: every requirement classed
  UNDEFINED, with the §13a question it waits on. **A blocked requirement gets
  no test approach** — designing a strategy for an undefined requirement is the
  same defect as inventing the requirement. It is excluded from the coverage
  denominator in §B1 and named in the completion report.
- **B1 Automation candidacy** — the explicit rule set deciding what gets
  automated, plus target coverage per priority band (e.g. 100% of P1).
- **B2 Technology stack** — confirm the versions actually present in
  `requirements.txt`. Do not invent versions; read the file.
- **B3 Framework structure** — the real tree, including the new files this
  feature adds (`automation/pages/<feature>_page.py`,
  `automation/locators/<feature>_locators.py`,
  `automation/test_data/<feature>.json`,
  `automation/tests/ui/test_<feature>.py`, plus
  `automation/tests/api/test_<feature>.py` only if the feature has an API
  surface). One feature owns exactly one file per layer — never split a
  feature's page object, locators or test data across files, and never share
  one file between two features. This is the authoritative path definition
  later phases and `/speckit-implement` follow; do not introduce a new
  top-level layer here — if one seems needed, raise it as a framework change
  first.
- **B4 Design rules** — locator priority, waiting strategy, page-object
  boundary, test independence, naming, traceability tags. These restate the
  constitution for this feature; call out any feature-specific exception.
- **B5 Test data strategy** — static vs generated vs API-seeded, and teardown.
- **B6 Reporting & CI** — Allure results path, what is attached on failure, the
  quality gate that blocks a merge.
- **B7 Risks to automation** — flaky surfaces, dynamic ids, unstable third
  parties, and the concrete mitigation for each.

### Step 6: Phase 1 — Design artifacts

Generate alongside `plan.md`:

1. **`FEATURE_DIR/data-model.md`** — the **test data model**:
   - Each entity the tests create, read or mutate
   - Required fields, valid ranges, and the boundary values worth testing
   - Relationships and setup order (what must exist before what)
   - Lifecycle: how each entity is created and cleaned up
   - State transitions worth exercising

2. **`FEATURE_DIR/quickstart.md`** — how a new engineer runs this suite:
   - Prerequisites (Python version, `playwright install`, Allure CLI)
   - Environment configuration (which `.env` keys, where secrets come from)
   - The exact commands to run the full suite, the smoke subset, and a single
     test, using `.specify/scripts/bash/run-tests.sh`
   - How to open the Allure report
   - Expected outcome of a healthy run

3. **`FEATURE_DIR/contracts/`** *(only if the feature has API surface under
   test)* — the request/response contracts the API tests assert against.
   Skip entirely for pure UI features.

### Step 7: Constitution check

Re-read `.specify/memory/constitution.md` and evaluate this plan against each
principle. Record the result in the Constitution Check section. Any deviation
goes in the Complexity Tracking table with the simpler alternative that was
rejected and why. An unjustified violation is an ERROR — fix the plan.

## Mandatory Post-Execution Hooks

**You MUST complete this section before reporting completion to the user.**

Check if `.specify/extensions.yml` exists in the project root.
- If it does not exist, or no hooks are registered under `hooks.after_plan`, skip to the Completion Report.
- If it exists, read it and look for entries under the `hooks.after_plan` key.
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

- `IMPL_PLAN` path and every artifact generated (`research.md`,
  `data-model.md`, `quickstart.md`, `contracts/` if present)
- The manual/automated split with counts and the reasoning in one line
- Target automation coverage per priority band
- New framework files this feature will add
- Constitution check result, including any tracked deviation
- Next phase: `/speckit-tasks`

## Key Rules

- Use absolute paths for filesystem operations; project-relative paths in prose.
- Read `requirements.txt` and the existing `automation/` tree before
  describing the stack — report what is there, not what you would have chosen.
- ERROR on unresolved clarifications or unjustified constitution violations.
- No test case content here. Cases are Phase 3 (`/speckit-tasks`).

## Done When

- [ ] `research.md` produced with every unknown resolved
- [ ] Part A complete: manual scope decided and justified, charters written
- [ ] Part B complete: stack confirmed against `requirements.txt`, structure and design rules stated
- [ ] `data-model.md` and `quickstart.md` generated (`contracts/` if API surface exists)
- [ ] Constitution check passed or deviations tracked
- [ ] Extension hooks dispatched or skipped per the rules above
- [ ] Completion reported with artifacts and the manual/automated split
