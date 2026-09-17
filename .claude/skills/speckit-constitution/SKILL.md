---
name: "speckit-constitution"
description: "STLC support — create or amend the QA constitution: the testing principles every phase command is checked against."
argument-hint: "Testing principles or values to add or amend"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  adapted-for: "STLC (Software Testing Life Cycle)"
  stlc-phase: "Governance — applies to every phase"
user-invocable: true
disable-model-invocation: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Scope Guard

This command's work is limited to `.specify/memory/constitution.md`. The phase
commands read it at runtime; they are not modified here.

**QA perspective, not product design.** This constitution governs how
*testing* is done (traceability, risk depth, determinism, POM boundaries) — it
is not a place to specify product behaviour or feature requirements. If the
user's input tries to define how the product should work, that is a
non-governance intent to defer to `/speckit-specify`, not content for this file.

- Classify every part of the user input as either constitution content or a
  separate, non-governance intent.
- If the input includes writing test cases, automating a scenario, running the
  suite, or fixing a defect, you **MUST NOT** execute it. Extract it as a
  deferred intent instead.
- You **MUST NOT** create, modify or delete test code, page objects, test data,
  feature specs, or any artifact outside the constitution workflow.
- If it is unclear whether an instruction is constitution content, ask before
  changing anything.
- After the update, add a `Next Actions` section for each deferred intent,
  naming the original intent and the appropriate follow-up command
  (`/speckit-specify`, `/speckit-tasks`, `/speckit-implement`, `/speckit-test`)
  without invoking it.
- Omit `Next Actions` when there are no non-governance intents.

## Pre-Execution Checks

**Check for extension hooks (before constitution update)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_constitution` key
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

You are updating the **QA constitution** at `.specify/memory/constitution.md` —
the testing principles that `/speckit-specify`, `/speckit-plan`,
`/speckit-tasks`, `/speckit-implement` and `/speckit-test` all validate their
output against. A principle here is not advice; it is a gate.

Follow this flow:

1. Run `.specify/scripts/bash/resolve-template.sh constitution-template --json`
   from the repository root and parse `TEMPLATE_CONTENT` as the active scaffold.
   - The resolver applies project overrides, preset layers and extension layers
     before the core fallback. It MUST succeed before you continue.
   - If it fails, stop and report the resolution error. Do not continue with
     only one contributing layer.
   - If `.specify/memory/constitution.md` exists, load it as the source of
     current values and amendments, and preserve everything still applicable.
   - If it does not exist, use the resolved template as the initial document.
   - Never write back to a versioned template layer.
   - Identify every `[ALL_CAPS_IDENTIFIER]` placeholder.

   **IMPORTANT**: the user may want more or fewer principles than the template
   carries. If they name a number, respect it and follow the general structure.

2. Collect or derive values for the placeholders:
   - Use the user's input where it supplies a value.
   - Otherwise infer from repository context — `README.md`, the existing
     constitution, `plan.md` design rules, the actual conventions in `automation/`.
   - `RATIFICATION_DATE` is the original adoption date (ask, or mark TODO, if
     unknown). `LAST_AMENDED_DATE` is today when anything changed, else keep the
     previous value.
   - `CONSTITUTION_VERSION` increments by semantic versioning:
     - **MAJOR** — a principle removed or redefined in a backward-incompatible way
     - **MINOR** — a new principle or section added, or guidance materially expanded
     - **PATCH** — clarification, wording, typo, non-semantic refinement
   - If the bump type is ambiguous, state your reasoning before finalising.

3. Draft the updated constitution using the resolved template as the required
   structure:
   - Replace every placeholder with concrete text. Leave no bracketed token
     unless the project has deliberately deferred it — and justify each one.
   - Preserve heading hierarchy. Remove template comments once replaced, unless
     they still add clarifying guidance.
   - Each principle needs: a succinct name line, the non-negotiable rule stated
     in MUST/SHOULD terms, and an explicit rationale where it is not obvious.
   - The Governance section must state the amendment procedure, the versioning
     policy, and the compliance review expectation.

   **Principles worth covering in a QA constitution** — offer these when the
   user is starting from the template and has not specified their own:

   | Area | The kind of rule it carries |
   |------|-----------------------------|
   | Traceability | Every test traces to a requirement; every requirement is tested or waived in writing |
   | Requirement verification | Ambiguity is raised, not guessed; assumptions are recorded |
   | Risk-based depth | Coverage is allocated by risk, not spread evenly |
   | Test determinism | No `sleep`, no order dependence, no permanently-rerun flaky test |
   | Page Object boundary | Page objects expose intent and never assert; tests own assertions |
   | Manual and automated parity | Both are first-class; the split is decided and justified |
   | Evidence | A phase is done when its artifact exists and is reviewable |
   | Data and security | No real customer data, no secrets in tracked files |
   | Defect handling | Severity scale, triage cadence, what blocks release |
   | Quality gates | The concrete criteria that block each phase transition |

   Keep principles **declarative and checkable**. "Tests should be reliable" is
   not a principle. "Tests pass in any order and under parallel execution, or
   they are broken" is.

4. Produce a **Sync Impact Report** as an HTML comment at the top of the file.
   It is scratch material for human review of this amendment, not governance
   content, and is expected to be removed before the file is committed.
   - Version change: old → new
   - Modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Follow-up TODOs for any deliberately deferred placeholder
   - **Downstream impact**: which phase commands are affected by this change —
     e.g. a new determinism rule changes what `/speckit-implement` must enforce
     and what `/speckit-analyze` will flag as CRITICAL

5. Validate before writing:
   - No unexplained bracket tokens remain
   - The version line matches the report
   - Dates are ISO `YYYY-MM-DD`
   - Every principle is declarative, checkable, and free of vague language
     (replace bare "should" with MUST/SHOULD plus rationale)
   - No principle contradicts another
   - Every principle could actually be evaluated by a phase command against a
     real artifact — if it could not, it is a value statement, not a principle

6. Write the completed constitution back to `.specify/memory/constitution.md`
   (overwrite).

7. Output a final summary:
   - The new version and the reasoning for the bump
   - Any TODO placeholders or deferred items needing manual follow-up
   - Which phase commands' behaviour changes as a result
   - A suggested commit message, e.g.
     `docs: amend QA constitution to vX.Y.Z (determinism principle + exit gate)`
   - A `Next Actions` section for any deferred non-governance intents

**Formatting**:

- Use Markdown headings exactly as in the template — do not promote or demote levels
- Wrap long rationale lines around 100 characters, without awkward breaks
- One blank line between sections; no trailing whitespace

If the user supplies a partial update (one principle revision), still run the
validation and version-decision steps.

If critical information is genuinely unknown (a ratification date, say), insert
`TODO(<FIELD_NAME>): explanation` and list it in the Sync Impact Report under
deferred items.

Write only `.specify/memory/constitution.md`. Do not create or modify template
source files.

## Post-Execution Checks

**Check for extension hooks (after constitution update)**:
Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.after_constitution` key
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
