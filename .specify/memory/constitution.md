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

**Design sources are enumerated, not read.** A `presentation-and-interaction`
source (a design mockup or prototype) carries most of its requirements through
attributes, sequence, repetition and data fields — a link's `href` target,
the same label appearing in three places, a field that looks like another
field but is not — not through prose a reader would naturally notice while
reading top to bottom. Reading such a source as a document rather than
inventorying it as a structure is a named failure mode: it reliably passes
over exactly this content. `/speckit-specify` enumerates a design source
structurally (text, interactive behaviour and its resulting effect, repeated
labels compared across their locations, data values, conditionals, semantic
attributes) before drafting any requirement from it, per its own procedure —
never derives requirements from a design source by reading it as narrative.

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

### XIII. Post-Approval Change Control

An approved artifact does not become mutable by default. A gap found later,
or a source that turns out to say something different than first recorded, is
handled as a **change**, never as a silent correction — the same discipline
that governs source conflicts (principle I) and undefined requirements
(principle II) applies equally to editing something already signed off.

**Step 1 — Classify the edit before making it.**

| Classification | Definition | Does it change a decision a human already approved? |
|---|---|---|
| **Clarification** | A source-verified detail that was always true, newly captured | No |
| **Correction** | The artifact stated something wrong about a source that has not itself changed | No |
| **Scope change** | An approved source's own content changed (a Jira field edited, a decision reversed, a design revised) | Yes |
| **New requirement** | Content enters scope that no approved source's previously-resolved content covered | Yes |

**Step 2 — Apply the matching rule.**

- **Clarification / Correction** — the artifact's `Status` may remain
  `Approved`. No new `Approved by`/`Approved on` is required. A dated entry in
  the artifact's `## Change Log` is still mandatory (Step 3).
- **Scope change / New requirement** — the artifact's `Status` reverts to
  `In Review` immediately, and every phase downstream of it halts at its own
  Step 0 entry gate until a human re-approves with a fresh `Approved by`/
  `Approved on`. This is the same gate as the first approval, not a lesser
  one — the Quality Gate criteria in §XI.b apply exactly as they did then.

**Step 3 — Every post-approval edit is logged, never silent.** Every artifact
carrying a `Status:` header maintains a `## Change Log` section: date,
classification, what changed and why, and the blast-radius statement from
Step 4. An edit to an approved artifact with no matching Change Log entry is
itself a defect, regardless of how small the edit was.

**Step 4 — Blast radius is checked, not assumed.** Before reporting a
post-approval edit complete, run `/speckit-analyze` (or, when the drift is at
the automation layer rather than the requirement layer, `/speckit-converge`)
against the changed artifact and record what it found: which downstream
`TR-xxx` / `TC-xxx` / task / test already encodes the pre-change content, and
whether each is now stale, still valid, or unaffected. "Nothing downstream
exists yet" is itself a valid, statable finding from that check — not a step
to skip because the answer seems obvious.

**Step 5 — Downstream updates are targeted, not wholesale.** A changed
`TR-xxx` requires updating only the `TC-xxx` / tasks / tests that Step 4
actually found referencing it — never a full re-run of the phase that
produced them by default. A full phase re-run is warranted only when the
blast radius genuinely spans most of that artifact, and that judgment is
stated, not assumed.

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

**Version**: 1.1.0 | **Ratified**: 2026-09-17 | **Last Amended**: 2026-09-19

### Amendment history

- **1.1.0** (2026-09-19, MINOR): Added principle XIII, Post-Approval Change
  Control. Prompted by FLTIQ-62's own `spec.md` needing a real post-approval
  edit (the §15a retrofit's one new finding) with no written rule for how to
  classify it, whether it needed re-approval, or how to check what it might
  affect downstream — that call had been made ad hoc, in conversation, twice
  in a row. Adds a classification step, a matching re-gate/lightweight-note
  rule, a mandatory `## Change Log` on every `Status`-bearing artifact, and a
  required blast-radius check via `/speckit-analyze`/`/speckit-converge`
  before any post-approval edit is reported complete.
- **1.0.1** (2026-09-19, PATCH): Clarified principle II — design and
  presentation sources are consumed by enumeration, not by reading as prose.
  Prompted by FLTIQ-62's requirement analysis missing eight design-sourced
  facts (section headings, link behaviour, repeated controls, CTA order, and
  two data fields that looked alike) on the first pass, all caught only by
  manual re-review. Changes no principle; states explicitly what "first-class
  input" already implied about how a design source must be consumed.
