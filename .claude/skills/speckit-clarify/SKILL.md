---
name: "speckit-clarify"
description: "STLC support — resolve ambiguity in the test basis by asking up to 5 targeted questions and encoding the answers back into spec.md."
argument-hint: "Optional areas to clarify (e.g. 'boundary values', 'test data', 'browser matrix')"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  adapted-for: "STLC (Software Testing Life Cycle)"
  stlc-phase: "1b — Requirement Analysis refinement (before Test Planning)"
user-invocable: true
disable-model-invocation: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before clarification)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_clarify` key
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

**Goal**: find the ambiguities in the test basis (`spec.md`) that would produce
the wrong tests, resolve them with the user, and write the answers back into the
spec.

An ambiguous requirement does not block coding — a developer will pick
something. It blocks **testing**, because there is no defensible expected
result. That is what this command exists to catch.

Run this **before** `/speckit-plan`. If the user chooses to skip it (a spike, a
throwaway cycle), proceed but warn that test cases built on an ambiguous basis
will need rework.

**QA perspective, not product design.** This command clarifies the *test
basis*, not the product. Apply the **Observation Rule** (constitution II):
where the gap is only the concrete *form* of a behaviour an approved source
already mandates, and the system is running, resolve it by observation and
record it as OBSERVED with its evidence. Where the gap is the behaviour's
*existence or intent* and no approved source settles it, it stays UNDEFINED and
goes to the requester — **never convert it into an assumption to continue**.
Never put a product-design decision to the user as if they were the developer
deciding how the app should work; a question about an undefined requirement
asks *who defines this*, not *what would you like*.

### Execution steps

1. Run `.specify/scripts/bash/check-prerequisites.sh --json --paths-only` from
   the repo root **once**. Parse `FEATURE_DIR` and `FEATURE_SPEC` (optionally
   `IMPL_PLAN`, `TASKS` for chained flows). If JSON parsing fails, abort and tell
   the user to re-run `/speckit-specify`.
   For single quotes in args like "I'm Groot", use `'I'\''m Groot'`.

2. **IF EXISTS**: load `.specify/memory/constitution.md` for the QA principles.

**Post-approval change note (constitution XIII).** Check `spec.md`'s `Status`.
If it already reads `Approved` (this run is resolving an open §13a/§13b
question the team answered after the original analysis — the common case for
a re-run, not the exception), every answer integrated in step 6 below is a
post-approval edit and needs the same treatment: classify it (an answer that
only supplies the concrete form of something already DEFINED/OBSERVED is a
**Clarification**; an answer that changes what the product actually does, or
resolves a conflict by picking a side no source had adjudicated, is a **Scope
change**), add the row to `spec.md`'s `## Change Log`, and — for a Scope
change — revert `Status` to `In Review` and say plainly that re-approval is
needed before `/speckit-plan` proceeds. Do not leave `Status: Approved`
standing on a spec that just had its scope changed underneath it.

3. Load `spec.md` and run a structured ambiguity scan against the taxonomy
   below. Mark each category **Clear / Partial / Missing**. Keep the coverage map
   internal unless no questions will be asked.

   **Source Conflicts** *(highest priority — jumps the queue)*
   - Two approved sources making incompatible claims, recorded in §11a or the
     manifest's `conflicts[]` and still `unresolved`
   - A conflict recorded but with no matching §13a blocking question

   **Undefined Expected Results** *(highest priority — jumps the queue)*
   - A requirement classed UNDEFINED with no observable outcome from any source
   - An in-scope obligation with no acceptance criterion covering it

   These two categories are **exempt from the 5-question budget** below. They
   are findings, not elective precision, and suppressing one to fit a quota is
   the failure constitution II exists to prevent.

   **Expected Results & Oracles** *(highest priority — no oracle, no test)*
   - Is the expected outcome of each acceptance scenario observable and stated?
   - For error paths: the exact message, state or code expected
   - Tolerances for anything numeric, timed or rounded
   - What "success" looks like when the system is asynchronous

   **Requirement Testability**
   - Requirements observable only through internal state
   - Requirements with a verb but no measurable object
   - Vague adjectives — "fast", "intuitive", "robust", "seamless", "user-friendly"
   - Conflicting requirements across sections

   **Boundaries & Data Ranges**
   - Field limits: min, max, length, precision, allowed character set
   - What happens at the boundary versus one past it
   - Empty, null, zero and whitespace-only handling
   - Equivalence classes that genuinely behave differently

   **Test Data**
   - Which personas/roles are needed, and their permissions
   - Whether data is pre-seeded, self-created, or must be requested
   - Whether data can be reused across runs, or must be unique per run
   - Cleanup expectations and whether the environment is shared
   - Any data that is sensitive and must be masked or synthesised

   **Environment & Platform**
   - Which environment this is verified on
   - Browser and viewport matrix, and where behaviour is allowed to differ
   - Feature flags, toggles and their required state
   - Third-party integrations: live, sandbox, or stubbed

   **Non-Functional Verification**
   - Performance: the metric, the percentile, the load, the threshold
   - Accessibility: which standard and which level
   - Security: session, authorisation and data-protection expectations
   - How each of these is actually measured, and by whom

   **Negative & Failure Behaviour**
   - Expected handling of invalid input, timeouts, and lost connectivity
   - Concurrency and conflict resolution
   - Rate limiting and throttling
   - Whether a failure should be silent, logged, or surfaced to the user

   **Scope & Regression Impact**
   - Explicit out-of-scope declarations
   - Existing behaviour at risk of regression from this change
   - Whether prior test cases need retiring or updating

   **Manual vs Automation Intent**
   - Anything the team already knows must stay manual, and why
   - Missing test hooks (stable ids) that would block automation
   - Whether this feature is expected to enter the regression suite

   **Defect & Exit Expectations**
   - Severity and priority scale in use
   - What blocks release versus what ships as known issues
   - The pass-rate or coverage threshold for sign-off

   **Terminology**
   - The same concept named differently across sections
   - Domain terms used without definition

   For each **Partial** or **Missing** category, first apply the Observation
   Rule's own Q1 (constitution II): does an approved source already establish
   that this behaviour must exist? Only if yes — and only the concrete *form*
   is unresolved — may you resolve it yourself, by observing the live system
   (record it as OBSERVED, citing both the observation and the source that
   mandates it) or from a genuine framework/environment default that is pure
   test mechanics (record it as INFERRED). **A "well-known convention for the
   platform," an industry-standard behaviour, or a "documented default" is
   never itself grounds to resolve a Partial/Missing category** — none of
   those is a source (constitution II hard stop 5), and writing one in as if
   it were an observed or assumed behaviour is exactly the invented-scenario
   failure this command exists to catch, not create. Where Q1's answer is no,
   the gap is a genuine candidate question — create one, don't paper over it.
   Only skip creating a question for what is answerable this way, is not a
   product-design choice you'd be asking the user to make on the developer's
   behalf, and would not be better resolved at `/speckit-plan`.

   **Legitimate vs. not, concretely**: *"Should an expired session redirect to
   the login page?"* is a legitimate clarification question when no source
   answers it — that's Q1 failing, genuinely UNDEFINED. *"What does the Jira
   acceptance criterion mean?"* when the AC already states the answer is not
   a clarification question at all — that's Q1 already satisfied; read the
   source again rather than asking the user to restate it.

4. Build an internal, prioritised queue. The **budget of 5** applies to
   *elective* precision questions; unresolved source conflicts and UNDEFINED
   business requirements are uncapped and asked first, in batches of at most 3
   so the exchange stays answerable. Say how many remain unasked. Do not output
   them all at once.
   - Each must be answerable as a 2–5 option multiple choice, **or** a short
     answer of ≤5 words
   - Include only questions whose answers change **test cases, expected results,
     test data, environment setup, or the manual/automation split**
   - Prefer breadth across high-impact categories over depth in one
   - Exclude anything already answered, purely stylistic, or better resolved at
     planning time
   - If more than 5 categories are unresolved, rank by (Impact × Uncertainty).
     Expected Results and Boundaries outrank everything else — a wrong oracle
     produces a test that is confidently incorrect.

5. **Sequential questioning loop** — exactly ONE question at a time.

   **Question quality** (every question, MC or short answer):
   - Lead with `**Question:**` followed by a full interrogative ending in `?`.
     The text before the `?` must stand on its own.
   - NEVER use a topic label or requirement id as the question.
     `Boundary values (TR-004)` is INVALID — it is a label.
     Permitted: `**Question:** <interrogative>?` or
     `**Question:** <interrogative>? (TR-004)`. The id only ever follows the `?`.
   - Immediately after the question, add one plain sentence of
     **"Why it matters"** — what test would be wrong without this answer.
   - Everyday wording. A reader who has not seen the spec must be able to answer
     from the question line alone.

   **Multiple choice**:
   - Analyse the options and pick the **most suitable** based on testing best
     practice, risk reduction, and what the spec already implies
   - Lead with `**Recommended:** Option [X] - <1-2 sentence reasoning>`
   - Then a table:

     | Option | Description | Testing Implication |
     |--------|-------------|---------------------|
     | A | <description> | <what it means for coverage> |
     | B | <description> | <what it means for coverage> |
     | C | <description> (up to E) | <what it means for coverage> |
     | Short | Provide a different short answer (≤5 words) | — |

   - Close with: `You can reply with the option letter (e.g., "A"), accept the recommendation by saying "yes" or "recommended", or provide your own short answer.`

   **Short answer**:
   - Lead with `**Suggested:** <proposed answer> - <brief reasoning>`
   - Then: `Format: Short answer (≤5 words). You can accept the suggestion by saying "yes" or "suggested", or provide your own answer.`

   **After each answer**:
   - "yes" / "recommended" / "suggested" → use your stated recommendation
   - Otherwise validate it maps to an option or fits ≤5 words
   - If ambiguous, ask once for disambiguation (same question, not a new one)
   - Record in working memory, then move to the next question

   **Stop** when all critical ambiguities are resolved, the user signals
   completion ("done", "good", "no more"), or you have asked 5. Never reveal
   queued questions in advance. If there are no valid questions at the start,
   say so immediately.

6. **Integrate after EACH accepted answer** (incremental, saved each time):

   - On the first answer, ensure a `## Clarifications` section exists (just after
     the Requirement Summary), with a `### Session YYYY-MM-DD` subheading.
   - Append `- Q: <question> → A: <final answer>` immediately on acceptance.
   - Then apply the answer to the right STLC section of `spec.md`:

     | Answer type | Target section |
     |-------------|----------------|
     | Requirement wording or testability | §3 Testable Requirements — rewrite the `TR-xxx` row |
     | Expected result / oracle | §4 Test Scenarios — the relevant Given/When/**Then** |
     | Negative or error behaviour | §4 Negative / Alternate Flows |
     | Boundary or range | §5 Edge Cases & Boundary Conditions |
     | Test data | §6 Test Data Requirements |
     | Environment, browser, flag | §7 Environment & Platform Matrix |
     | Performance, a11y, security target | §8 Non-Functional Requirements — as a measurable number |
     | Risk or impact | §9 Risk Analysis |
     | Exit threshold, severity scale | §10 Entry & Exit Criteria |
     | Resolution of a flagged ambiguity | §11 Testability Review — move the row to resolved with the answer |
     | A default the user confirmed | §12 Evidence Classification — under the correct class |
     | An answer defining a previously UNDEFINED requirement | §3 — change `Class` to DEFINED, cite the answer as its source; remove the §13a item |
     | Resolution of a source conflict | §11a **and** `source-manifest.json` `conflicts[].status`/`resolution` |

   - If the answer resolves a `[NEEDS CLARIFICATION]` marker in §13, **delete the
     marker** and write the resolved content in place.
   - If it invalidates an earlier statement, **replace** it — never leave
     contradictory text behind.
   - **If `spec.md`'s `Status` was already `Approved`** (per the post-approval
     change note above), add the corresponding row to `## Change Log` in the
     same write — classification, what changed, and the blast-radius result
     (run `/speckit-analyze` once at the end of step 6 rather than per-answer,
     and back-fill each row's blast-radius column from that single pass). Set
     `Status: In Review` if any accepted answer this session classified as a
     Scope change.
   - Save `spec.md` after each integration (atomic overwrite). Preserve heading
     hierarchy and do not reorder unrelated sections.
   - Keep each insertion minimal and testable.

7. **Validate** after each write and once at the end:
   - Exactly one Clarifications bullet per accepted answer, no duplicates
   - Total accepted questions ≤ 5
   - No lingering vague placeholder the answer was meant to resolve
   - No contradictory earlier statement remains
   - Only these new headings introduced: `## Clarifications`, `### Session YYYY-MM-DD`
   - Terminology consistent across every section touched
   - Every `TR-xxx` still has an observable, testable statement

8. Write the updated spec back to `FEATURE_SPEC`.

9. **Re-validate the requirement checklist** if `FEATURE_DIR/checklists/requirements.md` exists:
   1. Read it. If absent, skip silently.
   2. Find every task-list checkbox line — `- [ ]`, `- [x]`, `- [X]` (tolerant of
      leading whitespace, outside code fences). Ignore all other content.
   3. Snapshot each item's current state and text.
   4. Re-evaluate each item against the **updated** spec from step 8.
   5. Toggle only the items whose state actually changed: `[ ]`→`[x]` when now
      passing, `[x]`→`[ ]` when now failing. Leave unchanged items exactly as
      they are, preserving case.
   6. Save. **Only the `[ ]`/`[x]` marker of changed lines may differ** — all
      headings, notes, ordering and whitespace stay byte-identical.
   7. Compute three lists for the report: newly passing, regressions, still unchecked.
   8. Record before/after counts (e.g. "12/16 → 15/16 items passing").

### Behaviour rules

- No meaningful ambiguities → "No critical ambiguities detected worth formal
  clarification." and suggest proceeding to `/speckit-plan`.
- `spec.md` missing → tell the user to run `/speckit-specify`; never create one here.
- Never exceed 5 asked questions (retries on one question do not count).
- Do not ask automation-tooling questions — framework choices belong in
  `/speckit-plan`. Ask only if the absence blocks knowing *what* to verify.
- Do not ask the user to decide how an already-existing/live product should
  behave **when an approved source already requires the behaviour and only its
  concrete form is unclear** — determine the form from the real system
  instead (OBSERVED). This is never license to resolve *whether* a behaviour
  exists, or *what* it should be, from the system alone — that is
  observation overriding intent (constitution II hard stop 1/2), and stays a
  question. Ask the user only about QA scope, priority, or business intent
  that only they can decide.
- Respect early termination ("stop", "done", "proceed").
- If the quota is reached with high-impact categories unresolved, flag them
  explicitly under **Deferred** with the risk each one carries.

Context for prioritization: $ARGUMENTS

## Mandatory Post-Execution Hooks

**You MUST complete this section before reporting completion to the user.**

Check if `.specify/extensions.yml` exists in the project root.
- If it does not exist, or no hooks are registered under `hooks.after_clarify`, skip to the Completion Report.
- If it exists, read it and look for entries under the `hooks.after_clarify` key.
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

- Questions asked and answered
- Path to the updated spec
- Sections touched, by name
- `[NEEDS CLARIFICATION]` markers resolved and how many remain
- Requirement checklist status if re-validated: before/after counts, items that
  changed state in either direction, and any still unchecked
- Coverage summary: each taxonomy category as **Resolved** / **Deferred** /
  **Clear** / **Outstanding**
- For anything Deferred or Outstanding, the concrete testing risk it leaves
- Whether to proceed to `/speckit-plan` or clarify again

## Done When

- [ ] Test basis scanned against the full ambiguity taxonomy
- [ ] Up to 5 questions asked one at a time and answered
- [ ] Every answer integrated into the correct `spec.md` section and saved
- [ ] Resolved `[NEEDS CLARIFICATION]` markers removed, contradictions cleared
- [ ] Requirement checklist re-validated if present
- [ ] Extension hooks dispatched or skipped per the rules above
- [ ] Completion reported with coverage summary and remaining testing risk
