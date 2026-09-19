# Test Plan: FLTIQ-62 — Build the public landing page

**Feature Dir**: `specs/001-fltiq-62-public-landing-page` | **Date**: 2026-09-18 | **Test Basis**: [spec.md](./spec.md)
**Plan ID**: TP-FLTIQ-62 | **Owner**: Sajid Mohammad | **Status**: Approved
**Approved by**: Sajid Mohammad | **Approved on**: 2026-09-19

> STLC Phase 2 — Test Planning. Produced by `/speckit-plan`.
> Part A is the **manual test strategy**. Part B is the **technical design for
> automation**. Both must be filled: the split between them is a decision, not
> an oversight.

## Change Log

*(Added on approval, 2026-09-19, per constitution XIII — Post-Approval Change
Control. Empty for now: no edit has been made to this plan since approval.)*

| Date | Classification | What changed | Blast radius | Status impact |
|------|-----------------|--------------|---------------|----------------|
| — | — | No post-approval edits yet | — | — |

## Summary

FLTIQ-62 adds FleetIQ's public, unauthenticated landing page — the entry
point ahead of sign-up/sign-in. 18 of `spec.md`'s 19 testable requirements
are DEFINED and ready to plan against; TR-018 (the contested "Free while you
set up your first fleet. No card required." line) is UNDEFINED, blocked on an
open source conflict (CF-002 / §13a Q1), and gets no test strategy here. Of
the remaining 18: **8 P1 requirements automate at 100%** (the auth-redirect
gate, both primary CTAs, the hierarchy explorer's core interaction, and the
full WCAG/responsive baseline); **9 of 10 P2/P3 requirements automate** as
deterministic content/structure checks; one (TR-015, design-system-token
compliance) is only partially automatable and is backed by a manual
visual-regression review. Five things stay manual: visual/brand fidelity
against the Keel design, marketing-copy business-accuracy sign-off, one-off
verification of however CF-002 resolves, a screen-reader exploratory pass
(axe-core catches roughly a third to half of real WCAG issues), and a
real-device sanity check beyond the emulated 360px viewport.

---

# Part A — Manual Test Strategy

## A1. Test Objectives

- Confirm the authentication-based routing gate is airtight in both
  directions — unauthenticated visitors see the landing page, authenticated
  ones never do (TR-001, TR-002; risk RA-004).
- Confirm every "Create account" / "Sign in" control, everywhere it appears
  on the page, reaches the real destination screen with no intercepting
  modal (TR-004, TR-005; risk RA-001 — this is the entire reason the page
  exists).
- Confirm the hierarchy explorer behaves as a safe, self-contained demo: no
  network dependency on an API that doesn't have an agreed contract yet
  (TR-008; risk RA-005).
- Confirm the page meets the epic's WCAG 2.1 AA and 360px responsive
  baseline, since this is explicitly called out as the most visible screen
  in the product (TR-011–TR-014; risk RA-002).
- Confirm every piece of content matches the approved design exactly and
  makes no capability claim MVP1 doesn't support (TR-003, TR-006, TR-007,
  TR-009, TR-010, TR-015, TR-016, TR-017, TR-019; risks RA-003, RA-006).

## A2. Test Levels & Types

| Level | In Use | Rationale |
|-------|--------|-----------|
| Unit | No | Frontend component-level testing is owned by development; out of this suite's scope |
| System / E2E (UI) | Yes | The only level that matters here — a static marketing/interaction page with no API surface of its own |
| Regression | Yes | Folded into the `regression` pytest marker; re-run whenever the shared Keel design system (FLTIQ-60) or a sibling epic screen changes, since this page inherits both |
| UAT | Yes | Product-owner sign-off specifically on marketing copy and CF-002's resolution — everything else is objectively checkable and doesn't need a subjective business sign-off |

*(Integration/API deleted — this feature has no API surface at all, per
`spec.md` TR-008/NFR-002; nothing to test at that level.)*

**Test types in scope**: Smoke, Sanity, Functional, Regression, Negative,
Boundary, Cross-browser, Accessibility.

*(Performance deleted — no NFR was defined by any source for this ticket,
per `spec.md` §8; nothing to test against. Security deleted as a standalone
type — the one security-adjacent concern, no-analytics/no-tracking, is
folded into Functional via TR-017 rather than warranting its own test type
for a page with no auth boundary of its own and no data input.)*

## A3. Manual Scope — What Stays Manual and Why

| Area | Why manual | Effort |
|------|------------|--------|
| Visual/brand fidelity against the Keel design (spacing, exact colours, typography rendering) | Subjective visual judgement — pixel-level fidelity to a design isn't a boolean automation can assert cleanly, and TR-015's "every token from the design system" claim is better served by a human comparing rendered output to the design plus a visual-regression baseline than a single Playwright assertion (already flagged in `spec.md` §11) | 2h |
| Marketing-copy business-accuracy sign-off | TR-016 asserts the *literal* copy makes no unsupported claim per the story's own checklist; whether "500+ devices onboarded in a single import" (§13b Q1) is actually true is a business fact only the Device Registrar epic owner can confirm, not something a test can derive | 1h, blocked on §13b Q1 response |
| One-off verification of CF-002's resolution | Whatever the team decides for the "Free... No card required." line (ship/cut/revise, §13a Q1), a single manual check confirms it shipped as decided before the automated suite is updated to assert it going forward | 0.5h, blocked on §13a Q1 response |
| Screen-reader exploratory pass (NVDA / VoiceOver) | Automated axe-core scanning (research.md R3) catches roughly a third to half of real-world WCAG issues; the hierarchy explorer's custom tree control in particular needs a human listening to what actually gets announced, not just that ARIA attributes are present | 2h |
| Real-device sanity check beyond the emulated 360px viewport | Playwright's viewport emulation is not identical to a real phone's touch behaviour and rendering; a quick manual pass on at least one real Android/iOS device catches what emulation can't | 1h |

## A4. Exploratory Test Charters

| Charter | Explore | With | To discover |
|---------|---------|------|--------------|
| CH-001 | The hierarchy explorer's custom tree control | NVDA (Windows) and VoiceOver (macOS) | Whether node selection, status, and detail-panel updates are actually announced usefully — the risk automated axe scanning and Tab-order assertions alone can't rule out (risk RA-002) |
| CH-002 | The page's behaviour under a throttled/degraded network (DevTools "Slow 3G", and blocking the shared design-system JS bundle outright) | Chrome DevTools network conditions | What currently happens if the shared JS bundle (which both the hierarchy explorer and the primary CTAs depend on) fails to load — directly informs the pending answer to §13b Q3, and surfaces whether RA-001's CTA risk is theoretical or real today |
| CH-003 | Every capability claim and hero statistic against actual MVP1-shipped behaviour, with the product owner | The approved design's copy plus a walkthrough of what MVP1 actually supports | Any overclaiming beyond the five claims already verified in `spec.md`'s "Note on the copy" (risk RA-003, RA-006) |

## A5. Test Execution Approach

- **Cycles**: Cycle 1 — smoke (root URL loads, auth-redirect gate, both CTAs
  route correctly). Cycle 2 — full functional, accessibility and responsive
  pass. Cycle 3 — regression, re-run whenever FLTIQ-60 (design system) or any
  sibling Tenant/Identity screen changes, since this page inherits both.
- **Defect workflow**: Logged in Jira against FLTIQ-62, triaged into the
  constitution's five failure classes (Product Defect / Test Defect /
  Requirement Defect / Environment Issue / Flaky Behaviour) before any fix is
  attempted — never weaken an assertion to clear a failure.
- **Suspension criteria**: The smoke subset (TR-001, TR-002, TR-004, TR-005)
  fails → suspend further execution until fixed; a broken entry point makes
  every other result meaningless.
- **Resumption criteria**: Smoke subset green again.

## A6. Test Environment

| Item | Value |
|------|-------|
| Environments | QA / Staging, per `BASE_URL` in `.env` |
| Test accounts | One purpose-created, least-privileged account with an existing tenant, for Scenario 2's authenticated-redirect check — credentials sourced from `.env` (`TEST_USERNAME`/`TEST_PASSWORD`), never written into any test file |
| Data seeding | None — the hierarchy explorer's data is a static fixture bundled with the build (`spec.md` §6); no product data exists for this page to seed |
| Integrations | None live — this page explicitly makes no API call (TR-008/NFR-002). FLTIQ-33 (sign-up) and FLTIQ-35 (sign-in) are external dependencies for full-journey verification; `spec.md` §10 already documents the fallback (route-level verification only) if they're not yet deployed |

## A7. Schedule, Effort & Roles

*(Estimates for planning purposes; not a resourcing commitment — no source
gave a schedule for this ticket, and none is invented here.)*

| Activity | Owner | Estimate | Dependency |
|----------|-------|----------|------------|
| Test case development (`/speckit-tasks`) | QA | 0.5d | This plan approved |
| Automation implementation (`/speckit-implement`) | QA/SDET | 2d | Framework files listed in B3 |
| Manual/exploratory execution (A3, A4) | QA | 1d (6.5h across A3 + CH-001..003) | Build deployed to QA/Staging |
| Execution cycle 1 (smoke) | QA | 0.5d | Build deployed, smoke-passable |

## A8. Test Deliverables

- [x] Requirement analysis (`spec.md`) — Approved
- [x] This test plan (`plan.md`)
- [ ] Test cases (`test-cases.json` + `test-cases.xlsx`) — `/speckit-tasks`
- [ ] Automation code (`automation/`) — `/speckit-implement`
- [ ] Allure execution report — `/speckit-test`
- [ ] Test closure / summary report — `/speckit-test`

---

# Part B — Automation Technical Plan

## A0. Carry-Forward and Blocked Requirements

| TR-xxx | Class | Authority | Source id |
|--------|-------|-----------|-----------|
| TR-001 | DEFINED | scope-and-story-acceptance | unbracketed-1 |
| TR-002 | DEFINED | scope-and-story-acceptance | unbracketed-4 |
| TR-003 | DEFINED | scope-and-story-acceptance + presentation-and-interaction | Story §Scope bullet 2 + design source |
| TR-004 | DEFINED | scope-and-story-acceptance | unbracketed-2 |
| TR-005 | DEFINED | scope-and-story-acceptance + presentation-and-interaction | unbracketed-3 + design source |
| TR-006 | DEFINED | scope-and-story-acceptance + presentation-and-interaction | Story §Scope bullet 3 + design source |
| TR-007 | DEFINED | scope-and-story-acceptance + presentation-and-interaction | Story §Scope bullet 4 + design source |
| TR-008 | DEFINED | scope-and-story-acceptance + presentation-and-interaction | unbracketed-5 + design source |
| TR-009 | DEFINED | scope-and-story-acceptance + presentation-and-interaction | Story §Scope bullet 6 + design source |
| TR-010 | DEFINED | scope-and-story-acceptance + presentation-and-interaction | Story §Scope bullet 7 + design source |
| TR-011 | DEFINED | detailed-requirements | [TIA-AC-74] |
| TR-012 | DEFINED | detailed-requirements | [TIA-AC-77] |
| TR-013 | DEFINED | detailed-requirements | [TIA-AC-80] |
| TR-014 | DEFINED | detailed-requirements | [TIA-AC-81] |
| TR-015 | DEFINED | scope-and-story-acceptance + presentation-and-interaction | unbracketed-6, [FLTIQ-60] |
| TR-016 | DEFINED | scope-and-story-acceptance | unbracketed-7 |
| TR-017 | DEFINED | scope-and-story-acceptance | Story §Scope, Out of scope |
| TR-019 | DEFINED | scope-and-story-acceptance + presentation-and-interaction | Story §Scope bullet 5 + design source |

### Blocked requirements register

| TR-xxx | Blocked on | Reason |
|--------|-----------|--------|
| TR-018 | `spec.md` §13a Q1 (CF-002) | Existence disputed — the story's own pricing exclusion vs. the approved design both speak to this line without either settling whether it ships. **No test approach is designed for it.** Excluded from the §B1 coverage denominator. Revisit once §13a Q1 is answered; at that point this is a `spec.md` update (TR-018's Class changes to DEFINED or the row is removed), not a `plan.md` patch. |

## B1. Automation Candidacy

| Criterion | Threshold |
|-----------|-----------|
| Executed every regression cycle | Automate |
| Stable UI / contract | Automate |
| High business risk (P1) | Automate first |
| One-off, subjective, or exploratory | Keep manual (A3, A4) |
| Blocked by missing testability hooks | Defer — raised in B7 as a request to development |

**Target automation coverage**:
- **P1 (8 requirements: TR-001, 002, 004, 005, 008, 011, 012, 013): 100%.**
  Every P1 requirement is DEFINED with no blocking gap.
- **P2 (8 requirements: TR-003, 006, 007, 009, 014, 015, 017, 019): ~90%.**
  All automate except TR-015, which gets a supplementary manual
  visual-regression review (A3) alongside a partial automated check (a
  component-usage/token audit, not a single Playwright assertion — per
  `spec.md` §11's own proposed resolution).
- **P3 (2 requirements: TR-010, 016): 100%.** Both are deterministic
  structural/content checks (footer presence; literal-copy-against-checklist
  comparison) with no subjective element.
- **TR-018: excluded** (blocked requirements register above).

## B2. Technology Stack

Confirmed against the repository's actual `requirements.txt` — no version
invented:

| Concern | Choice | Version (from `requirements.txt`) | Notes |
|---------|--------|---------|-------|
| Language | Python | 3.10+ | Per the file's own header comment |
| Test runner | pytest | >=8.0 | |
| Browser driver | Playwright (sync API) | >=1.44 | via `pytest-playwright>=0.5` |
| Design pattern | Page Object Model | — | `automation/utils/base_page.py`, already in place |
| Reporting | Allure | allure-pytest>=2.13 | HTML report needs the separate `allure` CLI (`npm install -g allure-commandline`, per `quickstart.md`) |
| Parallelism | pytest-xdist | >=3.5 | `-n auto` supported; this suite has no shared mutable state, so it is safe under full parallelism |
| Flake control | pytest-rerunfailures | >=14.0 | Triage tool only, never a permanent fix (constitution VI) |
| Config | python-dotenv | >=1.0 | Secrets from environment only |
| **New dependency** | An axe-core-based Python package | **Not yet in `requirements.txt` — version to be pinned at implementation time (`/speckit-implement`), not invented here** | Needed for automated WCAG/contrast scanning (research.md R3); this plan does not add it to `requirements.txt` itself — that edit belongs to the phase that actually writes the test code |

## B3. Framework Structure

```text
automation/
├── conftest.py                          # unchanged — global fixtures only
├── utils/                               # unchanged
├── pages/
│   └── landing_page.py                  # NEW — this feature's page object
├── locators/
│   └── landing_locators.py              # NEW — this feature's locators
├── test_data/
│   └── landing.json                     # NEW — the HierarchyNode fixture (data-model.md)
└── tests/
    ├── ui/
    │   ├── conftest.py                  # MODIFIED — add a `landing_page` fixture
    │   └── test_landing.py              # NEW — this feature's test file
    └── api/                             # untouched — this feature has no API surface
```

**Structure decision**: Exactly the pattern `automation/pages/login_page.py`
already demonstrates — one feature, one file per layer. No new top-level
directory is needed. `login_page.py`/`login_locators.py` are the existing
**template** files (`ExamplePage`/`ExampleLocators`); FLTIQ-62 does not reuse
or extend them — it adds its own `landing_page.py`/`landing_locators.py`
alongside, per "one feature owns exactly one file per layer, never shared
between two features."

`tests/ui/conftest.py` gets one addition — a `landing_page` fixture
(constructing `LandingPage(page, settings)`), following the same pattern as
the existing `example_page`/`example_result_page` fixtures. No fixtures are
needed for the sign-up/sign-in/home destination pages TR-002/004/005 route
to — those belong to FLTIQ-33/35/46's own future page objects; this
feature's tests assert only the resulting URL (`expect(page).to_have_url(...)`),
not the destination page's content, so no cross-feature file ownership is
created.

## B4. Design Rules

- **Locator strategy**: `get_by_role` → `get_by_label` → `data-testid` →
  CSS, per constitution VII. Hierarchy-explorer nodes use
  `get_by_role("button", name=re.compile(...))` against the node's plain
  label (research.md R6) rather than the full tree-art-decorated accessible
  name. XPath is not used anywhere in this feature.
- **Two distinct "scroll to top" elements, tested independently**: the
  header's product mark and the footer's "Back to top" link both navigate to
  `#top`, but are two separate DOM elements with distinct accessible names
  (`get_by_role("link", name="FleetIQ")` vs.
  `get_by_role("link", name="Back to top")`) — role+name matching already
  disambiguates them without any special handling, but a passing test for one
  must never be read as covering the other (TR-003, TR-010; Scenario 1 items
  5 and 6 in `spec.md`).
- **Testability request to development** (not a code change this plan makes):
  add `data-testid` to the hierarchy detail panel's four value fields
  (device count, device type, config source, note) — role/label cannot
  disambiguate plain `<span>` pairs with no ARIA semantics (research.md R6).
- **Waiting**: Playwright auto-waiting and `expect()` web-first assertions
  only. `time.sleep` is banned (constitution VI) — `tests/ui/conftest.py`
  already centralises timeout configuration via `_apply_timeouts`.
- **Page objects**: `LandingPage` returns data (e.g. `hero_statistics()` →
  `list[str]`) or another page object (e.g. `click_create_account()` → the
  caller asserts the resulting URL); it never asserts, per
  `automation/utils/base_page.py`'s existing contract.
- **Test independence**: every test navigates to the root URL fresh; the one
  stateful test (Scenario 2) signs in within its own test via a real UI
  flow and relies on Playwright's function-scoped `context` fixture for
  teardown — no shared session between tests.
- **Naming**: `test_<tcid>_<behaviour>()`, e.g.
  `test_tc001_unauthenticated_visitor_sees_landing_page` (exact `TC-xxx` ids
  assigned by `/speckit-tasks`).
- **Traceability**: every test tagged `@allure.testcase("TC-xxx")` plus the
  relevant `@pytest.mark.p1/p2/p3` and `@pytest.mark.a11y`/`boundary`/
  `negative` markers already defined in `pytest.ini`.

## B5. Test Data Strategy

| Approach | Used for | Mechanism |
|----------|----------|-----------|
| Static fixture | The five `HierarchyNode` instances (data-model.md) | `automation/test_data/landing.json`, loaded via `automation.utils.data_loader` (existing utility — pass `"landing.json"`) |
| Environment-sourced | The one authenticated test account (Scenario 2) | `.env` `TEST_USERNAME`/`TEST_PASSWORD` via `Settings.require_credentials()` — already implemented, fails loudly if unset rather than testing with blank credentials |

**Teardown**: None needed for the static fixture (read-only). The
authenticated session ends automatically with the test's browser context
(constitution VI: every test creates and cleans up its own state).

## B6. Reporting & CI

- **Local run**: `.specify/scripts/bash/run-tests.sh` (see `quickstart.md`
  for this feature's exact invocations).
- **Results**: `reports/allure-results` → HTML in `reports/allure-report`,
  already wired globally; no feature-specific reporting code needed.
- **Attachments on failure**: screenshot, page DOM, URL, browser console —
  already global via `automation/conftest.py`'s `pytest_runtest_call` hook.
- **CI trigger**: **none currently configured.** The repository's only
  GitHub Actions workflow (`qa-suite.yml`) was removed from this repo earlier
  in this feature's own work (unrelated cleanup, not a product decision).
  Until a CI workflow is re-established, this suite runs via `run-tests.sh`
  manually, or in whatever pipeline the team sets up separately — this is
  recorded honestly rather than assumed.
- **Quality gate** (once CI exists): 100% of the P1 suite green blocks merge,
  per constitution §XI.b's own "Suite green" criterion.

## B7. Risks to Automation

| Risk | Mitigation |
|------|------------|
| Hierarchy-node button accessible names include ASCII tree-art characters (`├─`, `│`, `└─`), making exact-name locators brittle | Regex/partial-text role matching on the plain label only (research.md R6) |
| Detail-panel value fields have no ARIA role/label to distinguish them | Request `data-testid` from development (B4); do not fall back to unjustified XPath |
| The design source is a static Claude Design prototype — the real React implementation's DOM may differ in structure even if visually identical | Verify locators against the first real deployed build before treating them as final, rather than assuming 1:1 fidelity to the prototype's markup |
| FLTIQ-33 (sign-up) / FLTIQ-35 (sign-in) may not be deployed when this suite first runs | Conditional skip with an explicit, visible reason (research.md R5); re-enable once those land — never a silent pass |
| No `API_BASE_URL` is configured, so "no API call" can only be asserted broadly (no XHR/fetch at all), not filtered to a specific host | Accepted as the stronger, not weaker, check (research.md R4); revisit if this page ever gains real network activity |
| axe-core-class tooling only catches roughly a third to half of real WCAG issues | Covered by exploratory charter CH-001 (screen-reader pass) in Part A — never claimed as fully automated |
| TR-018 is blocked/UNDEFINED | Excluded from automation entirely (A0); do not write a test asserting any outcome for it until `spec.md` is updated |
| The hierarchy tree row's `meta` text (e.g. Building A's "2 subgroups") is easy to conflate with the detail panel's `devices` count (Building A shows 79 there) — they read alike for three of the five nodes but diverge for the two "Building" nodes | Assert `meta` and `devices` as two distinct fixture fields from `data-model.md`, never derive one from the other in a test; the two Building nodes are the specific regression case to keep in the suite |
| The design source defines a third, unused modal variant (`flow`/`openFlow`) and two page-level props (`theme`, `showStats`) that are Claude Design/Keel authoring scaffolding, not real page behaviour (confirmed in `spec.md` §11) | Do not write a test for any of the three — there is nothing they gate in the real page. Flagged here so a future implementer skimming the source doesn't assume `openFlow` is a missed interaction to automate. |

---

## Constitution Check

*GATE: must pass before test case development. Re-check after design.*

| Principle | Compliance |
|---|---|
| I. Source Authority & Traceability | Pass — every TR carried forward from `spec.md` with its Class and Authority (A0); TR-018 correctly excluded rather than silently tested |
| II. Requirement Testability & Evidence Classification | Pass — no test approach designed for the one UNDEFINED requirement (TR-018); every INFERRED decision in `research.md` is explicitly test-mechanics only, never a restated product expectation |
| III. Context Flows Forward | Pass — `spec.md`'s Class/Authority reproduced verbatim in A0; nothing here introduces a source `spec.md` didn't already resolve |
| IV. Risk Drives Test Depth | Pass — P1 gets 100% automated coverage and runs first (B1); P3 still gets full automated coverage here since both P3 items are cheap, deterministic checks, not because risk was ignored |
| V. Negative, Boundary & Security Testing | Pass — boundary values identified (zero-device and max-count nodes, data-model.md); negative flows present in every `spec.md` scenario; the one privacy-adjacent concern (no analytics/tracking, TR-017) is covered |
| VI. Deterministic Automation | Pass — no `time.sleep` anywhere in this design; every fixture test-data-driven and stateless except the one explicitly-scoped authenticated test |
| VII. Page Objects Own Interaction, Tests Own Assertion | Pass — `LandingPage` returns data/page-objects only (B4); locator priority followed, with the one XPath-avoiding fallback (`data-testid` request) justified rather than silently reached for |
| VIII. Manual and Automated Testing Are Both First-Class | Pass — Part A names five genuinely manual areas with reasons, not schedule excuses |
| IX. Data & Security | Pass — no credential appears in any planning artifact; test account sourced from `.env` only |
| X. Evidence & Defect Integrity | Pass — reporting already wired globally; nothing new needed |
| XI. Phase Gates | Pass — this plan is gated on `spec.md`'s `Status: Approved` (confirmed at Step 0 entry); its own approval gates `/speckit-tasks` |
| XII. Continuous Traceability & Drift Control | Pass — A0's carry-forward table gives `/speckit-analyze` a direct chain to audit |

No violation found. No entry required below.

## Complexity Tracking

*(No violations — table intentionally left empty.)*

## Artifacts Produced by This Phase

```text
specs/001-fltiq-62-public-landing-page/
├── spec.md              # Requirement analysis (/speckit-specify) — Approved
├── plan.md              # This file (/speckit-plan)
├── research.md          # Tooling/approach decisions (/speckit-plan)
├── data-model.md        # Test data model (/speckit-plan)
├── quickstart.md        # Environment setup & how to run (/speckit-plan)
├── test-cases.json      # Canonical test cases — /speckit-tasks, not yet produced
├── test-cases.xlsx      # Excel deliverable — /speckit-tasks, not yet produced
├── tasks.md             # Automation work breakdown — /speckit-tasks, not yet produced
└── reports/             # Execution results — /speckit-test, not yet produced
```

*(No `contracts/` directory — this feature has no API surface under test.)*
