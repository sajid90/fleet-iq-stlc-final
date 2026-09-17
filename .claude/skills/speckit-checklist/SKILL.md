---
name: "speckit-checklist"
description: "STLC support — generate a review checklist that validates the quality of the test artifacts (basis, plan, cases, automation readiness)."
argument-hint: "Domain or focus (e.g. 'coverage', 'automation readiness', 'release exit')"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  adapted-for: "STLC (Software Testing Life Cycle)"
  stlc-phase: "Cross-phase — artifact quality review"
user-invocable: true
disable-model-invocation: false
---

## Checklist Purpose: "Unit Tests for the Test Artifacts"

**CRITICAL CONCEPT**: these checklists review **the quality of your testing
artifacts** — the requirement analysis, the test plan, the test cases, the
automation design. They are not test cases, and they do not verify the product.

**NOT product verification** (that is what `test-cases.json` and `/speckit-test` are for):

- ❌ NOT "Verify the login button works"
- ❌ NOT "Test that invalid passwords are rejected"
- ❌ NOT "Confirm the dashboard loads in under 2s"

**FOR test-artifact quality**:

- ✅ "Does every P1 requirement have at least one P1 test case?" (coverage)
- ✅ "Is the expected result of TC-014 observable, or does it assume internal state?" (testability)
- ✅ "Are boundary values defined for every field with a stated limit?" (completeness)
- ✅ "Does the plan state why each manual case stays manual?" (justification)
- ✅ "Do all automated tests carry a TC id so the Allure report is traceable?" (traceability)
- ✅ "Is the pass-rate threshold for sign-off quantified?" (measurability)

**The distinction**: a test case asks "does the product behave correctly?" A
checklist item asks "is our testing of it well-designed, complete, and
defensible?" If an item could pass or fail by running the application, it is a
test case and belongs in `/speckit-tasks` — not here.

**QA perspective, not product design.** This is QA of a product that already
exists or is being built elsewhere. The dynamic clarify-intent questions below
are about *reviewing testing artifacts* (scope, audience, rigor) — never about
deciding how the product itself should behave. If a candidate question would
ask the user to make a product-design call, drop it; that is out of scope for
a checklist command.

**Ownership and checkbox lifecycle**:

- These checklists are reviewer-owned artifacts.
- `[x]` means a reviewer judged the artifact-quality criterion satisfied.
- `[x]` does **not** mean any testing was executed.
- This command generates or appends items; it MUST NOT mark them `[x]`.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before checklist generation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_checklist` key
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

    Wait for the result of the hook command before proceeding to the Execution Steps.
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session (the invocation may differ from the literal `{command}` id shown above, e.g. a skills-mode agent runs it as `/skill:speckit-...` or `$speckit-...`). Emitting the block alone does not run the hook.
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## Execution Steps

1. **Setup**: run `.specify/scripts/bash/check-prerequisites.sh --json --template checklist-template`
   from the repo root; parse `FEATURE_DIR`, `AVAILABLE_DOCS` and `TEMPLATE_CONTENT`.
   All paths absolute. For single quotes in args like "I'm Groot", use `'I'\''m Groot'`.

2. **IF EXISTS**: load `.specify/memory/constitution.md`.

3. **Clarify intent (dynamic)** — derive up to THREE contextual questions. They MUST:
   - Come from the user's phrasing plus signals in `spec.md` / `plan.md` /
     `test-cases.json` / `tasks.md`
   - Only ask what materially changes the checklist's content
   - Be skipped individually when `$ARGUMENTS` already settles them

   **Generation algorithm**:
   1. Extract signals: which STLC phase the user is reviewing (basis / plan /
      cases / automation / release), risk indicators ("critical", "compliance",
      "regulated"), audience hints ("QA lead", "peer review", "release board"),
      explicit deliverables ("coverage", "a11y", "cross-browser", "exit criteria").
   2. Cluster into candidate focus areas (max 4), ranked by relevance.
   3. Identify the audience and the moment of use (author self-check, peer
      review, phase gate, release sign-off) if not explicit.
   4. Detect missing dimensions: which artifact is under review, depth/rigor,
      risk emphasis, exclusions, what "done" means for this review.
   5. Draw questions from these archetypes:
      - Artifact scope (e.g. "Should this review the test cases only, or also the automation code that implements them?")
      - Phase gate depth (e.g. "Is this a quick self-check before planning, or the formal gate before automation starts?")
      - Risk prioritisation (e.g. "Which risk areas must have mandatory gating items?")
      - Audience framing (e.g. "Will the QA lead use this to sign off, or is it an author self-check?")
      - Boundary exclusion (e.g. "Should performance and accessibility be excluded from this round?")
      - Coverage-class gap (e.g. "No negative-path cases detected — should the checklist gate on their absence?")

   **Formatting**: if presenting options, use a compact table with columns
   Option | Candidate | Why It Matters. Maximum A–E; omit the table when
   free-form is clearer. Never ask the user to restate what they already said.
   Do not invent categories — if uncertain, ask "Confirm whether X is in scope."

   **Defaults when interaction is impossible**: Depth = Standard;
   Audience = Reviewer (peer review); Focus = the top 2 relevance clusters.

   Label them Q1/Q2/Q3. After the answers, if ≥2 coverage classes (Negative /
   Boundary / Non-Functional / Recovery) remain unclear, you MAY ask up to TWO
   more (Q4/Q5) with a one-line justification each. Never exceed five. Skip
   escalation if the user declines.

4. **Understand the request**: combine `$ARGUMENTS` with the answers to derive
   the checklist theme, consolidate the user's explicit must-have items, map
   focus areas to category scaffolding, and infer missing context from the
   artifacts — never hallucinate it.

5. **Load feature context** from `FEATURE_DIR`:
   - `spec.md` — requirements, scenarios, edge cases, NFRs, risks, exit criteria
   - `plan.md` (if present) — manual/automation split, candidacy rules, design rules
   - `test-cases.json` (if present) — the cases themselves
   - `tasks.md` (if present) — the automation breakdown
   - `automation/` (if present) — the implemented automation

   Load only the portions relevant to the active focus areas. Summarise long
   sections rather than embedding raw text. Use progressive disclosure.

6. **Generate the checklist** using `TEMPLATE_CONTENT` as the structure:
   - Create `FEATURE_DIR/checklists/` if needed
   - Name the file for its domain: `coverage.md`, `automation-readiness.md`,
     `test-data.md`, `release-exit.md`, `a11y.md`
   - **New file** → number items from `CHK001`. **Existing file** → append,
     continuing from the last id (last was `CHK015` → start at `CHK016`)
   - Never delete or replace existing content — always preserve and append
   - Leave every new item unchecked `[ ]`

   **Core principle — review the testing, not the product.** Every item
   evaluates the artifacts for:
   - **Completeness** — is every necessary requirement, case, or decision present?
   - **Clarity** — is it unambiguous and specific?
   - **Consistency** — do the artifacts agree with each other?
   - **Measurability** — can it be objectively judged?
   - **Coverage** — are all scenarios, paths and edge cases addressed?
   - **Traceability** — does every link in the chain hold?

   **Category structure** — group by quality dimension, choosing what fits the
   theme:
   - **Test Basis Quality** — are the requirements testable as written?
   - **Coverage Completeness** — does every requirement, path and edge case have a case?
   - **Test Case Quality** — are steps, data and expected results clear and observable?
   - **Traceability** — does `TR → TC → T → test function` hold end to end?
   - **Automation Readiness** — is the design sound, and are the test hooks there?
   - **Test Data & Environment** — is everything needed defined and obtainable?
   - **Exit Criteria** — is "done" quantified and agreed?

   **Item quality rules**:
   - Each item is a question a reviewer answers by reading the artifacts
   - Reference the specific artifact and id where possible: `(spec.md §3 TR-004)`
   - One judgement per item — split anything compound
   - No item may require running the application to answer

7. **Report** the checklist path, its theme, the item count, the categories
   covered, and whether the file was created or appended to.

## Example Checklist Types & Sample Items

**`coverage.md`** — is the test set complete?

- CHK001 Does every `TR-xxx` in spec.md §3 map to at least one test case? (traceability)
- CHK002 Does every P1 requirement have at least one P1 test case? (completeness)
- CHK003 Does every scenario have both a positive and a negative case? (coverage)
- CHK004 Is every edge case in spec.md §5 represented by a case? (completeness)
- CHK005 Does every NFR in spec.md §8 have a case, or a written waiver? (completeness)
- CHK006 Are boundary values defined for every field with a stated limit? (completeness)

**`test-case-quality.md`** — are the cases well written?

- CHK001 Is each expected result observable without inspecting internal state? (testability)
- CHK002 Does any case verify more than one behaviour and need splitting? (clarity)
- CHK003 Are preconditions explicit, including the required role and data? (completeness)
- CHK004 Do steps reference a data alias rather than a literal credential? (security)
- CHK005 Is the priority of each case consistent with its requirement? (consistency)

**`automation-readiness.md`** — can this actually be automated well?

- CHK001 Does the plan state the candidacy rule that decided each automate/manual call? (justification)
- CHK002 Does every manual case in tasks.md carry a stated reason? (justification)
- CHK003 Are stable test hooks (`data-testid` or roles) available for every element the cases touch? (feasibility)
- CHK004 Does the plan define how each test creates and cleans up its own state? (design)
- CHK005 Is the locator strategy stated and consistent with constitution principle V? (consistency)
- CHK006 Will every automated test carry a `TC-xxx` id for report traceability? (traceability)

**`test-data.md`** — is the data story complete?

- CHK001 Is the source of every data set defined (seeded, generated, requested)? (completeness)
- CHK002 Is it stated whether data can be reused across runs or must be unique? (clarity)
- CHK003 Is cleanup defined for every entity the tests create? (completeness)
- CHK004 Is any sensitive data identified and a masking approach stated? (security)

**`release-exit.md`** — can we sign off defensibly?

- CHK001 Are the exit criteria in spec.md §10 quantified rather than descriptive? (measurability)
- CHK002 Is the defect severity scale defined and agreed? (clarity)
- CHK003 Is the required pass rate stated as a number? (measurability)
- CHK004 Is it defined which defect severities block release? (clarity)

## Anti-Examples: What NOT To Do

These belong in `test-cases.json` via `/speckit-tasks`, never in a checklist:

- ❌ "Verify a valid user can log in" → a test case
- ❌ "Check the error message says 'Invalid credentials'" → a test case
- ❌ "Run the smoke suite on Firefox" → an execution step
- ❌ "Confirm the API returns 200" → a test case

The checklist equivalents:

- ✅ "Is there a test case covering successful login for each supported role?" (coverage)
- ✅ "Is the exact expected error message specified in the case, rather than 'an error'?" (clarity)
- ✅ "Does the browser matrix in spec.md §7 state which cases run on which browsers?" (completeness)
- ✅ "Do the API cases specify the expected status code and body shape?" (completeness)

Also avoid:

- ❌ Items answerable only by running code
- ❌ Compound items joining two judgements with "and"
- ❌ Items with no artifact reference, leaving the reviewer to hunt
- ❌ Marking generated items `[x]` — that is the reviewer's call

## Post-Execution Checks

**Check for extension hooks (after checklist generation)**:
Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.after_checklist` key
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
