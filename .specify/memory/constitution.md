# FleetIQ QA Constitution

> The governing principles for every STLC phase in this repository. Each
> `/speckit-*` command checks its output against this file. A violation must be
> justified in the plan's Complexity Tracking table or the work does not proceed.

## Core Principles

### I. Source Authority & Traceability

Every artifact carries its lineage. A Jira acceptance criterion becomes a
requirement `TR-xxx` in `spec.md`, which is covered by one or more `TC-xxx`
test cases, which are automated by a `Txxx` task, which becomes a named test
function tagged with its test case id.

No test exists without a requirement. No requirement ships untested or
explicitly waived in writing. Any orphan on either side is a defect in the
process and must be resolved before the exit gate.

**Every requirement names the source that authorised it.** The resolved source
set for a feature is recorded in `source-manifest.json` — what was retrieved,
from where, when, and with what authority. A source that could not be retrieved
is recorded as a missing source with its impact, never omitted and never
substituted with a plausible guess.

**Source conflicts are surfaced; they are never silently reconciled.** Where two
approved sources disagree, both statements are recorded with their authority,
and a clarification is raised. The single exception is a conflict that a source
*itself* adjudicates in writing — then the adjudication and its citation are
recorded, not merely the winner.

#### Precedence policy

Authority is assigned **by domain**, not by flat rank. Determine which domain a
claim belongs to and the source owning that domain governs:

| # | Source | Authority token | Governs |
|---|--------|-----------------|---------|
| 1 | Jira User Story / MVP ticket | `scope-and-story-acceptance` | Scope of this cycle; story acceptance criteria |
| 2 | Parent Jira Epic | `feature-context` | Feature context, conventions, dependencies |
| 3 | Feature / Product PRD | `detailed-requirements` | Detailed functional and non-functional requirements |
| 4 | Approved Decision Logs | `decision` | Settled decisions |
| 5 | Approved UX/UI designs | `presentation-and-interaction` | Layout, labels, interaction detail |
| 6 | MVP / Product Proposal / Roadmap | `product-context` | Product, architecture and delivery context |
| 7 | Existing implementation | `observed-implementation` | **OBSERVED behaviour only — may never redefine intent** |
| 8 | Technical documentation | `technical-documentation` | Mechanics, contracts |
| 9 | Technical inference | `inference` | **Testing craft only — never product behaviour** |

The ordered list is a **tie-break and labelling device**. It names which side of
a recorded conflict carries higher authority, and it may select a provisional
working position only where doing so does not change expected product
behaviour. It is never used to silently pick a winner on a behavioural conflict.

### II. Requirement Testability & Evidence Classification

The Requirement Analysis phase exists to find ambiguity, not to restate the
ticket. Untestable, contradictory, or missing acceptance criteria are raised in
the Testability Review section — never silently guessed.

**The Observation Rule.** Observation answers *"what does this system do?"* It
can never answer *"what should this system do?"*

Classify every material statement by asking two questions in order:

**Q1 — Does an approved source establish that this behaviour must exist?**

**Q2 — Is the unresolved part the behaviour's *existence/intent*, or only its
*concrete form*?** Existence/intent means whether it happens at all, under which
conditions, what the business outcome is, what the threshold is, who is
authorised. Form means the exact copy of an error message, field order, redirect
target, response shape, observed latency.

| Q1 | Q2 | Class | What may be written |
|----|----|-------|---------------------|
| Yes | form unresolved, system reachable and verified now | **OBSERVED** | A concrete expected result, citing both the observation evidence and the approved source that mandates the behaviour |
| Yes | fully specified | **DEFINED** | A concrete expected result, citing the source id and its authority |
| No | form only, following deterministically from a standard, the framework or the environment | **INFERRED** | Test *mechanics* only — waits, fixtures, selectors, environment config. **Never an expected result.** |
| No | existence/intent unresolved | **UNDEFINED** | Nothing. Record the requirement with `Expected result: UNDEFINED`, raise a blocking clarification, and write no test case that asserts an outcome. |

**Four hard stops:**

1. Observation may never *create* a requirement. If no approved source says the
   behaviour must exist, observing that it happens produces a note, not a
   requirement with an expected result.
2. Observation may never *override* a DEFINED statement. Observed behaviour that
   contradicts an approved source is a **Product Defect candidate** plus a
   recorded conflict — not a re-specification.
3. A system **not yet built, or being built by this very ticket**, yields no
   legitimate OBSERVED for expected results. Anything read from an in-progress
   branch is INFERRED at best and carries no authority.
4. **Assumptions are restricted to test-execution assumptions** — environment,
   data provisioning, tooling, scheduling. A statement of product intent may
   never be recorded as an assumption. **Never convert an undefined business
   requirement into an assumption just to continue.**

**The designated-observation exception.** Where a system has *no* approved
requirement source and the running application is the agreed source of record
(third-party demo portals, undocumented legacy), declare that explicitly in
`source-manifest.json` with authority `de-facto-requirement`. Statements derived
from it are then DEFINED by that designated source. The distinction is honesty
about where authority comes from: a source designated up front and recorded,
versus an observation quietly promoted mid-analysis to avoid asking a question.

**QA perspective, not product design.** No phase command decides how the product
*should* behave. Do not ask the user a question an approved source already
answers. Do not answer from observation a question only an approved source can
settle. A user-facing question is reserved for what only the requester can
decide: scope, priority, business intent, or an undefined requirement.

### III. Context Flows Forward

Each phase carries forward the resolved context of the phase before it, so a
reviewer can judge an artifact without re-reading the whole chain. Requirement
classification and source authority established in `spec.md` are restated in
`plan.md`; acceptance-criterion ids survive into `test-cases.json`; test case
ids survive into task and test-function names. A phase that silently introduces
a source, requirement or expectation absent from its input is drifting, and
`/speckit-analyze` treats it as such.

### IV. Risk Drives Test Depth

Coverage is allocated by risk, not spread evenly. P1 paths — those where
failure costs money, data, or trust — get exhaustive positive, negative, and
boundary coverage and are automated first. P3 paths may be smoke-only or
manual. The allocation is stated in the plan and defended, not assumed.

### V. Negative, Boundary & Security Testing

Positive coverage alone is not coverage. Every scenario carries negative and
boundary cases: invalid input, rejected states, missing permissions, minimum,
maximum, empty, zero, and maximum length. Security and privacy expectations —
authorisation, session handling, data exposure, enumeration resistance — are
identified during requirement analysis, not discovered at execution. Timing,
concurrency and idempotency requirements are named explicitly where the feature
has them; their absence from the source is a finding, not a silence to fill.

### VI. Deterministic Automation (NON-NEGOTIABLE)

A test that fails intermittently is worse than no test: it trains the team to
ignore red. Therefore:

- Playwright auto-waiting and web-first assertions only. `time.sleep` is banned.
- Every test creates its own state and cleans up after itself.
- Tests pass in any order and under parallel execution, or they are broken.
- No test depends on another test, on execution order, or on leftover data.
- A quarantined flaky test is a tracked defect with an owner, not a permanent
  `rerun` flag.

### VII. Page Objects Own Interaction, Tests Own Assertion

The Page Object Model boundary is strict. Page objects expose user intent
(`login_page.sign_in(user)`), return page objects or data, and never assert.
Tests read as the scenario they verify and hold every assertion. Locators live
in the locator layer, never inline in test bodies. Selector priority is
role → label → `data-testid` → CSS; XPath requires a comment justifying it.

### VIII. Manual and Automated Testing Are Both First-Class

Automation is a means, not the goal. Exploratory testing, visual judgement, and
usability review find classes of defect no script will. Every test plan states
what stays manual and why. Conversely, anything run every regression cycle
against a stable interface gets automated — repeating it by hand is waste.

### IX. Data & Security

- Real customer data never enters this repository — not in test data, not in
  fixtures, not in screenshots committed to git.
- Credentials, API tokens, and connection strings come from the environment
  (`.env`, CI secret store). A secret in a tracked file is a Critical defect,
  fixed before anything else.
- Test accounts are purpose-created and least-privileged.
- Reports and traces are scrubbed before leaving the team boundary.

### X. Evidence & Defect Integrity

A phase is complete when its artifact exists and is reviewable, not when
someone reports it done. Execution results are Allure reports with screenshots,
traces, and videos on failure. "Tests pass" without a report attached is not a
result. Failures are reported with their actual output, never summarised away.

Every failure is triaged into exactly one class:

| Class | Meaning | Action |
|-------|---------|--------|
| **Product Defect** | The application behaves wrongly | Raise a defect; keep the test |
| **Test Defect** | The test or locator is wrong | Fix the test; do not blame the product |
| **Requirement Defect** | The approved source set is contradictory or untestable | Return to `/speckit-clarify`; do not weaken the test |
| **Environment Issue** | Data, config, deployment, network | Fix the environment; re-run and say the result changed |
| **Flaky Behaviour** | Passes and fails without a code change | Investigate the race; quarantine only with an owner and a ticket |

Never weaken an assertion to clear a failure.

### XI. Phase Gates

#### XI.a Phase approval gates (human)

| Gate | Blocks | Minimum condition |
|------|--------|-------------------|
| Requirement analysis approved | `/speckit-plan` | A human has reviewed `spec.md` and `source-manifest.json` — conflicts, missing sources and UNDEFINED items included — and set `Status: Approved` |
| Test plan approved | `/speckit-tasks` | A human has reviewed the manual/automated split and target coverage |
| Test cases approved | `/speckit-implement` | A human has reviewed `test-cases.xlsx` for adequacy of coverage |
| Convergence | `/speckit-test` | `/speckit-converge` reports no outstanding CRITICAL or HIGH gap, or each is accepted in writing |
| Closure | Sign-off | A human accepts the Go / No-Go verdict and its evidence |

A gate is a decision by a person. Approving a gate whose machine criteria below
have failed requires recording the override and its reason.

#### XI.b Quality gate criteria (machine-checkable)

| Gate | Blocks | Criterion |
|------|--------|-----------|
| Requirement analysis approved | `/speckit-plan` | No open blocking clarification on a P1 requirement |
| Source resolution complete | `/speckit-plan` | `source-manifest.json` exists; every conflict has a status; every missing source names its impact |
| Test plan approved | `/speckit-tasks` | Manual/automation split decided and justified |
| Test cases reviewed | `/speckit-implement` | Every P1 requirement has at least one P1 test case |
| No fabricated expectations | `/speckit-implement` | No test case carries a concrete expected result for an UNDEFINED requirement |
| Suite green | Sign-off | 100% of P1 cases executed; zero open Critical/High defects |

### XII. Continuous Traceability & Drift Control

Traceability is verified, not assumed. `/speckit-analyze` audits the chain
read-only at any point; `/speckit-converge` reconciles the automation suite
against the approved test cases and tasks; `/speckit-test` reports coverage
actually executed. A break anywhere in
`Jira AC → TR-xxx → TC-xxx → Txxx → test function` is a defect in the process
and is reported rather than closed over.

## Governance

This constitution supersedes convention, habit, and convenience. Amendments are
made through `/speckit-constitution`, require a stated rationale, and bump the
version below using semantic versioning: MAJOR for removing or redefining a
principle, MINOR for adding one or materially expanding guidance, PATCH for
clarification that changes no behaviour.

Every phase command validates its output against these principles and reports
compliance. Where a deviation is genuinely warranted, it is recorded in the
plan's Complexity Tracking table with the simpler alternative that was rejected
and why. Undocumented deviation is not permitted.

**Version**: 1.0.0 | **Ratified**: 2026-09-17 | **Last Amended**: 2026-09-17
