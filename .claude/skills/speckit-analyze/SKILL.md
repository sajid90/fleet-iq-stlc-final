---
name: "speckit-analyze"
description: "STLC support — read-only consistency and coverage analysis across spec.md, plan.md, test-cases.json, tasks.md and the automation code."
argument-hint: "Optional focus areas (e.g. 'coverage only', 'automation drift')"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  adapted-for: "STLC (Software Testing Life Cycle)"
  stlc-phase: "Cross-phase — quality gate before automation"
user-invocable: true
disable-model-invocation: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before analysis)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_analyze` key
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

    Wait for the result of the hook command before proceeding to the Goal.
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session (the invocation may differ from the literal `{command}` id shown above, e.g. a skills-mode agent runs it as `/skill:speckit-...` or `$speckit-...`). Emitting the block alone does not run the hook.
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## Goal

Find the breaks in the traceability chain before anyone writes automation code:

```text
Jira AC → TR-xxx (spec.md) → TC-xxx (test-cases.json) → Txxx (tasks.md) → test function
```

A break at any link means something ships untested or something is tested for no
stated reason. Both are defects in the process.

**QA perspective, not product design.** You judge the artifacts against each
other and against the constitution — never against your own opinion of how
the product should behave. An ambiguous requirement is a Testability/Ambiguity
finding to raise, not something to silently resolve one way or another.

Run this after `/speckit-tasks` has produced a complete `tasks.md`. It also runs
usefully after `/speckit-implement`, when the code layer can be checked too.

## Operating Constraints

**STRICTLY READ-ONLY**. Do not modify any file. Output a structured report and
offer a remediation plan the user must explicitly approve.

**Constitution Authority**: `.specify/memory/constitution.md` is non-negotiable
here. A conflict with a MUST principle is automatically CRITICAL and requires
changing the spec, plan, cases or tasks — never diluting or reinterpreting the
principle. Amending a principle happens in `/speckit-constitution`, not here.

## Execution Steps

### 1. Initialize

Run `.specify/scripts/bash/check-prerequisites.sh --json --require-spec --require-tasks --include-tasks`
once from the repo root; parse `FEATURE_DIR` and `AVAILABLE_DOCS`. Derive:

- `SPEC` = `FEATURE_DIR/spec.md`
- `PLAN` = `FEATURE_DIR/plan.md`
- `TASKS` = `FEATURE_DIR/tasks.md`
- `CASES` = `FEATURE_DIR/test-cases.json`
- `WORKBOOK` = `FEATURE_DIR/test-cases.xlsx`

Abort with a clear message naming the missing prerequisite command if a required
file is absent. For single quotes in args like "I'm Groot", use `'I'\''m Groot'`.

### 2. Load artifacts (progressive disclosure)

Load only what each pass needs.

**From `spec.md`**: testable requirements (`TR-xxx`) with type/priority/risk,
`Authority` and `Class`; test scenarios and their acceptance scenarios; edge
cases (§5); test data (§6); environment matrix (§7); NFRs (§8); risk analysis
(§9); exit criteria (§10); testability review (§11); the acceptance-criteria
index (§3a); source conflicts (§11a); evidence classification (§12); blocking
questions (§13a); source inventory (§15); the `Status` header and, if present,
`## Change Log`.

**From `source-manifest.json`** *(schema 2.0 only, if present)*: resolved
sources and their authority, `conflicts[]` with status, `missing_sources[]` with
impact, `dependencies[]`. Verify that every source `spec.md` cites is
represented here, and that no downstream artifact introduces a requirement
absent from the approved source set.

**From `plan.md`**: automation candidacy rules and target coverage (§B1); stack
(§B2); framework structure (§B3); design rules (§B4); test data strategy (§B5);
reporting and quality gate (§B6); the manual scope decided in §A3; the
`Status` header and, if present, `## Change Log`.

**From `test-cases.json`**: every case's id, title, scenario, requirements,
type, priority, automatable, automation_status, test_file, steps.

**From `tasks.md`**: task ids, phases, `[P]` markers, file paths, `covers:` ids.

**From the code** *(only if `automation/` exists)*: test function names, their
`@allure.testcase` ids and markers, page-object and locator files.

**From the constitution**: principle names and MUST/SHOULD statements.

### 3. Build the traceability model

Internal only — do not echo raw artifacts.

- **Requirement inventory** keyed by `TR-xxx`, with priority and risk
- **Scenario inventory** keyed by `S<n>`, with the `TR-xxx` each claims to cover
- **Case inventory** keyed by `TC-xxx`, with requirements, priority, automatable
  flag and status
- **Task inventory** keyed by `Txxx`, with the `TC-xxx` from its `covers:` clause
- **Code inventory** keyed by test node id, with the `TC-xxx` it declares
- **Constitution rule set**

### 4. Detection passes

High-signal findings only. Cap at 50; summarise the overflow.

#### A. Coverage gaps *(the core pass)*

- `TR-xxx` with **zero** test cases
- **P1** requirement with no **P1** case
- **A `TR-xxx` naming more than one distinct element/clause in its own text (a
  list, or a compound sentence joined by "and") where at least one named
  element has no case referencing it, even though the `TR-xxx` overall has
  some coverage.** `TR-xxx` with *zero* cases is caught above; this catches
  the harder case — *partial* coverage that reads as complete because the
  requirement isn't orphaned, it's just incompletely decomposed. Check by
  reading the `TR-xxx`'s row in `spec.md` §3 clause by clause against every
  case citing it, not by confirming a citation count > 0. This is precisely
  how FLTIQ-62's "Capabilities"/"Hierarchy" nav links went uncovered for two
  full review cycles: TR-003 had cases, just not one per named element.
- Scenario with positive coverage but **no negative** case
- Edge case in §5 with no case
- NFR in §8 with no case and no written waiver
- Test case with **no** `TR-xxx` — an orphan with no stated reason to exist
- `automatable: true` case with no task in `tasks.md`
- Task with a `covers:` id that does not exist in `test-cases.json`
- Scenario-phase task missing its `covers:` clause entirely
- **An `EC-xxx` from `spec.md` §5 with real, existing test coverage
  (confirmed via a `test-cases.json` note or `requirements`/citation) that
  has no row of its own in `tasks.md`'s Traceability table.** Count `spec.md`
  §5's edge cases and `tasks.md`'s Traceability table's `EC-xxx` rows
  separately and compare — do not assume they match because most of them do.
  This is a documentation-completeness gap, not a coverage gap (the test
  itself is fine) — but it is exactly how FLTIQ-62's table under-reported 4
  of its 6 edge cases: rows were added only when that edge case needed a fix,
  never as a systematic sweep once the others were already correct.

#### B. Automation drift *(when `automation/` exists)*

- Case marked `Automated` whose `test_file` does not resolve to a real test.
  If it does not resolve at the literal path recorded, try resolving it by
  filename against the current automation tree before reporting drift — the
  path may predate a framework restructure.
- Test function carrying a `TC-xxx` that is absent from `test-cases.json`
- Test function with **no** `@allure.testcase` id — untraceable in the report
- `automation_status` disagreeing with what the code actually contains
- `test-cases.xlsx` older than `test-cases.json` — the deliverable has drifted
  from the source of truth

#### C. Constitution alignment

- Page object containing an assertion (principle V)
- `time.sleep` anywhere in `automation/` (principle IV)
- Locator inline in a test body rather than the locator layer (principle V)
- A literal credential or real customer data in a tracked file (Data & Security)
- Test depending on another test's state or on execution order (principle IV)
- Any requirement, plan element or task conflicting with a MUST principle
- A quality gate mandated by the constitution that the plan omits

#### D. Ambiguity

- Vague adjectives in requirements or expected results — fast, scalable, secure,
  intuitive, robust — with no measurable criterion
- A test case whose expected result is not observable
- Unresolved `[NEEDS CLARIFICATION]`, TODO, TKTK, `???`, `<placeholder>`
- An acceptance scenario whose **Then** clause states no verifiable outcome

#### E. Duplication and redundancy

- Near-duplicate requirements
- Test cases that verify the same behaviour with the same data
- Cases differing only in wording — consolidate and keep the clearer one

#### F. Consistency

- Case priority contradicting its requirement's priority
- A case marked `automatable: false` that the plan's §B1 rules say should be automated
- The manual list in `tasks.md` disagreeing with `plan.md` §A3
- Terminology drift — the same concept named differently across files
- An entity in the test data model absent from the spec, or the reverse
- Task ordering contradictions — a scenario task before its Foundation dependency
  with no dependency note
- Browser or environment named in a case but absent from the §7 matrix

#### G. Evidence integrity *(schema 2.0 only)*

- A test case carrying a concrete `expected_result` that traces **only** to a
  requirement classed `UNDEFINED` — a fabricated expectation. Always CRITICAL:
  it is the failure mode constitution II exists to prevent.
- An unresolved entry in `conflicts[]` with no corresponding §13a blocking
  question — a conflict that was recorded and then quietly dropped.
- An entry under §12 *Test-execution assumptions* that states product intent
  rather than an environment/data/tooling assumption (look for "shall", "must",
  "will" applied to system behaviour).
- A `Class` or `Authority` value outside the enum in constitution I and II.
- A requirement classed `OBSERVED` that cites no observation evidence, or no
  approved source mandating the behaviour.

#### H. Post-approval change control *(constitution XIII)*

- An artifact whose `Status` reads `Approved` but whose `## Change Log` has a
  **Scope change**/**New requirement** entry with no fresh `Approved by`/
  `Approved on` dated on or after it — the gate was bypassed. Always CRITICAL:
  everything downstream is trusting an approval that no longer covers what
  the artifact currently says.
- A `## Change Log` entry with no classification, or no blast-radius
  statement — an incomplete change record, itself a defect per constitution
  XIII Step 3.
- A `## Change Log` entry whose blast-radius column claims "none" or "not
  affected," but the traceability model built in step 3 shows a `TC-xxx` /
  task / test that does in fact reference the changed `TR-xxx` — the blast
  radius was checked incorrectly, not skipped honestly.
- An artifact edited after `Approved` (its content disagrees with what an
  earlier `Change Log`-less version would have said, if inferable from
  context — e.g. a `TR-xxx` referenced in `tasks.md`/`test-cases.json` no
  longer matches its current text in `spec.md`) with **no** `## Change Log`
  section at all.

When this session is being run specifically to check the blast radius for a
named recent change (the user says something like "I just updated TR-008,
what does that affect"), treat this category as the primary pass: report,
per Change Log entry, exactly which `TC-xxx`/task/test the model shows
referencing that `TR-xxx`, and whether each still holds, needs a targeted
update, or is now orphaned — this *is* constitution XIII Step 4's check.

#### I. Invented / Unsupported Test Behaviour *(constitution I/II)*

- A test case citing a `TR-xxx` whose own text does not establish the
  specific behaviour the case asserts — a borrowed or nearby-sounding
  citation rather than one that actually matches. Check by reading the
  `TR-xxx`'s row in `spec.md` §3 against the case's `expected_result`
  directly, not by trusting that a citation exists.
- A `TR-xxx`, scenario, or test case whose only support (per `spec.md`'s own
  Source column, or `source-manifest.json`) is industry/QA best practice, a
  security convention not adopted in writing by an approved source, generic
  UX/navigation/session/error-handling convention, another application's
  behaviour, or a previous FleetIQ ticket/feature/test suite — none of these
  is one of the nine sources in constitution I.
- An expected result reflecting only `OBSERVED` implementation behaviour with
  no approved source establishing that it is *required* — observation
  redefining intent (constitution II hard stops 1–2).
- A requirement or edge case classed `INFERRED` that nonetheless carries a
  concrete expected result instead of test-mechanics-only content
  (constitution II).
- A test case, scenario, or requirement for a page, screen, or feature absent
  from the resolved source set entirely.

Found in `test-cases.json` → always **CRITICAL** (it is already
automation-adjacent, not a draft). Found only in `spec.md`'s Test Scenarios,
not yet a test case → **CRITICAL** if it would produce an executable
assertion as written, **HIGH** if it is already flagged in the Testability
Review pending clarification. The recommendation is always to **remove the
requirement/scenario/test case, or return it to `/speckit-clarify`** as an
open question — never to invent a source or reclassify it `DEFINED` to clear
the finding.

### 5. Severity

- **CRITICAL** — violates a constitution MUST; a P1 requirement with zero
  coverage; a case claiming `Automated` with no test behind it; a bypassed
  post-approval gate (category H); an invented/unsupported test behaviour
  found in `test-cases.json` (category I)
- **HIGH** — a requirement with no coverage; a missing negative path on a P1
  scenario; conflicting requirements; an untestable expected result; a
  Change Log blast-radius claim contradicted by the traceability model
- **MEDIUM** — terminology drift; missing NFR coverage; priority mismatch;
  duplicate cases; stale workbook; an incomplete Change Log entry
- **LOW** — wording, minor redundancy, cosmetic inconsistency

### 6. Report

Output Markdown only — no file writes.

## Test Artifact Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| C1 | Coverage | CRITICAL | spec.md §3 TR-004 | No test case covers TR-004 (P1) | Add a P1 case in `/speckit-tasks` |

One row per finding, with stable ids prefixed by category initial.

**Traceability matrix:**

| TR | Priority | Test Cases | Tasks | Automated | Status |
|----|----------|-----------|-------|-----------|--------|
| TR-001 | P1 | TC-001, TC-002 | T009, T010 | 1/2 | Partial |

**Orphans:** test cases with no requirement; tasks with no case; tests with no `TC-xxx`.

**Constitution alignment issues:** (if any)

**Metrics:**

- Requirements: total / covered / uncovered
- Requirement coverage %, and P1 coverage % separately
- Test cases: total, by priority, automatable vs manual
- Cases automated vs planned
- Tasks: total, with valid `covers:`, orphaned
- Ambiguity count, duplication count, CRITICAL count

### 7. Next actions

- CRITICAL present → resolve before `/speckit-implement`
- Coverage gaps → re-run `/speckit-tasks` to add the missing cases
- Ambiguity in the basis → run `/speckit-clarify`
- Automation drift → re-run the exporter, or fix `automation_status` in
  `test-cases.json`, then regenerate the workbook
- Bypassed gate (category H) → the artifact's owner re-classifies the Change
  Log entry, or re-approves it (fresh `Approved by`/`Approved on`) — no
  downstream phase should proceed in the meantime
- Invented/unsupported behaviour (category I) → remove the requirement/
  scenario/test case, or return to `/speckit-clarify` to raise it as an open
  question — never invent a source or reclassify it to clear the finding
- Only LOW/MEDIUM → safe to proceed, with the improvements listed

Give explicit commands, not general advice.

### 8. Offer remediation

Ask: "Would you like me to suggest concrete remediation edits for the top N
issues?" Do **not** apply them automatically.

### 9. Check for extension hooks

After reporting, check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.after_analyze` key
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

## Operating Principles

### Context efficiency

- Minimal high-signal tokens — actionable findings, not exhaustive documentation
- Progressive disclosure — load artifacts incrementally
- Cap the findings table at 50 rows; summarise the overflow
- Deterministic — a re-run without changes produces the same ids and counts

### Analysis guidelines

- **NEVER modify files** — this is read-only
- **NEVER hallucinate a missing section** — report its absence accurately
- **Constitution violations are always CRITICAL**
- Cite specific instances, not generic patterns
- Report a clean result gracefully, with the coverage statistics that prove it

## Context

$ARGUMENTS
