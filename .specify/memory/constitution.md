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

**The chain runs in both directions, and both are checked at creation time,
not only at the exit gate.** A requirement traces down to a source — one of
the nine authorities in the precedence table below. A test case traces up
through its requirement to that same source:

```
Test Case  ->  Requirement (TR-xxx)  ->  Source  ->  Jira Story / Epic / PRD /
                                                      Decision Log / Design /
                                                      linked or sub-task issue
```

A test case, scenario, or requirement that cannot complete this chain is an
orphan by definition — not a defect to fix later, but one to **reject before
it is written**. **Never create a `TR-xxx` — however plausible-sounding —
solely to give an already-imagined test case something to cite, and never
attach an existing `TR-xxx` merely because it is nearby or sounds related.** A
citation is valid only when the cited requirement's own text establishes the
exact behaviour the test asserts, not merely a neighbouring or thematically
similar one.

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

**Five hard stops:**

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
5. **Only the nine sources in principle I's precedence table can establish a
   product behaviour.** Industry or QA best practice, a security convention
   (OWASP or otherwise) not adopted in writing by an approved source, generic
   UX/navigation/session/error-handling convention, common web or framework
   behaviour, another application's behaviour, a previous FleetIQ ticket,
   feature, or test suite, a template's example content, or a "reasonable
   default" the analysis judged sensible are never a source, however
   plausible or well-established the behaviour is elsewhere. Where none of
   the nine applies, the behaviour is UNDEFINED — recorded as an open
   question, never quietly written into a spec, scenario, or test case on the
   reasoning that it "would be a useful test." Usefulness is not authority.

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

**VII.a — Static UI text is asserted exactly, never semantically
(NON-NEGOTIABLE).** Every button label, link text, heading, and static body
copy that an approved source (design, `spec.md`, PRD) states as a literal
string is verified with an exact, case-sensitive string comparison —
`==` against the full, isolated text of the correct element. Never a
substring check (`in`), a lowercased comparison, a regex, or `exact=False`
used to decide whether the text is *correct*. A tolerant match answers "is
something there," not "is it right," and three separate defects on FLTIQ-62
shipped as passing tests because of exactly this: `"Create account"` shipped
as `"Create an account"` behind a lowercased substring check; `"tenant
owner"` shipped as `"Tenant Owner"` behind the same; a footer attribution
string was checked with `"ACL Digital" in <whole footer's text>`, which
would have passed even if the actual text were wrong, malformed, or
duplicated elsewhere in that block.

This does not ban tolerant matching outright — it separates two different
jobs that a semantic match quietly conflates:

- **Locating** an element to interact with it (click, navigate) may use a
  tolerant locator (`get_by_role` with a partial or case-insensitive name,
  `get_by_text(..., exact=False)`) when the test's purpose is confirming
  *where the control leads*, not *what it says*. `page_object.method()` may
  return the element via a tolerant locator.
- **Asserting** what that element's text actually is is a separate step,
  using the element's own isolated, full text with `==`. If a whole block of
  text contains other elements' content too (e.g. a footer with three
  children), isolate the one element that carries the literal string before
  comparing — never assert against the concatenated block with `in`.

**Narrowing the locating carve-out (1.5.0): when the element's own
accessible content *is* the literal string and nothing else, locate it
exactly too.** The tolerant-locating carve-out above was written for
elements whose accessible content legitimately combines the literal string
with other content an approved source places there too (e.g. an icon glyph
beside a wordmark) — forcing exact match there fails for a reason unrelated
to the string, and breaks the moment that sibling content changes for any
reason, including a fix. It was never meant to cover a standalone link or
button whose full content is nothing but the static string — a "Create
account" link, a "Back to top" link. There, a tolerant locator
(`get_by_role(..., name="create account")` case-insensitive, no `exact=True`)
doesn't just risk over-matching: it makes the click **succeed** even when the
shipped label is wrong, so a live defect ships invisibly through every test
that only clicks through, and only a separate, easy-to-forget assertion
elsewhere ever catches it. `CREATE_ACCOUNT_NAME`'s original
`re.compile(r"create.*account", re.IGNORECASE)` did exactly this on
FLTIQ-62 — TC-002/003/004/007/010-012 clicked straight through
`"Create an account"` and reported nothing wrong; only TC-029/030/033's
separate text assertions ever caught D5. A standalone static control is
therefore located with the same exact string/`exact=True` used to assert it
— one identifier, one place it's spelled correctly, both jobs use it. State
in a comment which case applies whenever it isn't obvious from the DOM
alone (e.g. why a wordmark-plus-icon element stays tolerant).

A page object method that returns a composite, multi-element string (for
locating or debugging) must say so in its docstring and must not be used for
an exact-match assertion; add a dedicated method that isolates the single
element instead. Every literal string asserted this way is verified against
the approved source directly — the design file itself, not a transcription
of it in `spec.md`, when the two could disagree (constitution I).

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

**Step 4a — Prose citations of the changed item's status are found and
fixed too, not just structured references (NON-NEGOTIABLE).** Resolving a
clarification question, closing an open item, or changing a requirement's
class does not only create downstream `TR-xxx`/`TC-xxx` links to check — it
can leave *other sections describing that same item's old status in prose*
uncorrected, and `/speckit-analyze`'s structured-id check does not read
prose for this. Before reporting the resolution complete, search every
artifact in `FEATURE_DIR` (and the constitution and skills themselves, when
one of them is what changed) for the item's own identifier (its `§`
section/question number, `TR-xxx`, `EC-xxx`, `CF-xxx`, defect id) and read
each hit — not just the section where it was first raised — to confirm it
still states the *current* resolution, not the state before this edit. A
citation that itself asserts a status ("still-open", "unanswered",
"pending", "blocked", "excluded") is exactly the failure mode this step
exists to catch: it must be re-verified against the section it names, never
trusted on its own wording, before it is used to justify a decision (such as
excluding something from a defect report). FLTIQ-62's own history is the
named case: `spec.md` §11 called §13b Q4 "still-open" a full day after §13b
itself recorded Q4 as closed, and that stale sentence was then cited to
exclude a real defect from a report — twice, in two different artifacts —
before a direct question caught it.

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

**Version**: 1.5.0 | **Ratified**: 2026-09-17 | **Last Amended**: 2026-09-24

### Amendment history

- **1.5.0** (2026-09-24, MINOR): Narrowed VII.a's tolerant-locating
  carve-out. It had permitted a tolerant locator whenever a test only cared
  about a control's destination, not its label — but `CREATE_ACCOUNT_NAME`'s
  `re.compile(r"create.*account", re.IGNORECASE)` used that carve-out on a
  *standalone* link (no other content sharing its accessible name), so it
  matched `"Create an account"` (D5's wrong label) just as happily as the
  correct string: every routing test clicked straight through the defect and
  reported nothing wrong, leaving only the separate copy-assertion tests to
  ever catch it. The carve-out now applies only where the element's
  accessible content legitimately combines the literal string with other
  approved-source content (e.g. an icon glyph beside a wordmark) — a
  standalone static control is located with the same exact string used to
  assert it.
- **1.4.0** (2026-09-22, MINOR): Added principle XIII Step 4a, closing a gap
  in Step 4's own blast-radius check: it scoped "downstream" to structured
  `TR-xxx`/`TC-xxx`/task/test links, never to prose elsewhere that describes
  the changed item's status. On FLTIQ-62, `spec.md` §11 called §13b Q4
  "still-open" a full day after §13b itself recorded Q4 as closed; that
  stale sentence was then cited — unverified against §13b — to exclude a
  real defect from a report, in two separate artifacts, before a direct
  question caught it. Step 4a requires searching every artifact for the
  changed item's own identifier and re-verifying each hit against the
  current resolution, and names "a citation asserting a status" as the
  specific pattern to distrust on its own wording.

- **1.3.0** (2026-09-22, MINOR): Added principle VII.a, Static UI text is
  asserted exactly, never semantically. Prompted by three FLTIQ-62 findings
  in one cycle: a CTA label ("Create account" shipped as "Create an
  account"), a hero statistic's case ("tenant owner" shipped as "Tenant
  Owner"), and a footer attribution string, all hidden from the suite by
  substring/lowercased assertions that answered "is something there"
  instead of "is it right." Separates tolerant *locating* (permitted, when
  the point is confirming a destination) from exact *asserting* (mandatory
  `==` on the correct element's isolated text, for every literal string an
  approved source states), and requires verifying against the design source
  directly rather than a transcription of it when the two could disagree.
- **1.2.0** (2026-09-21, MINOR): Strengthened principle I (the bidirectional
  `Test Case -> Requirement -> Source` chain, made explicit; an incomplete
  chain is rejected at creation, not fixed later; never invent or borrow a
  `TR-xxx` for traceability) and principle II (fifth hard stop: only the nine
  precedence-table sources establish a product behaviour — industry practice,
  security/UX/navigation convention, another application, a prior ticket or
  test suite, and "reasonable defaults" are never one). Prompted by two
  concrete invented-scenario incidents on FLTIQ-62 found only by user
  question — a session-expiry redirect with no supporting requirement, and an
  anchor-scroll test built on generic browser behaviour with a borrowed
  `TR-003` citation. Neither the requirement-authority chain nor the
  evidence-classification rule changes; both are stated more explicitly so
  the same class of invention is caught before it is written, not after.
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
