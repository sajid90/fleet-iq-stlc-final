# Test Plan: [TICKET-ID] — [FEATURE NAME]

**Feature Dir**: `[specs/###-name]` | **Date**: [DATE] | **Test Basis**: [link to spec.md]
**Plan ID**: TP-[TICKET-ID] | **Owner**: [NAME] | **Status**: Draft | Approved

> STLC Phase 2 — Test Planning. Produced by `/speckit-plan`.
> Part A is the **manual test strategy**. Part B is the **technical design for
> automation**. Both must be filled: the split between them is a decision, not
> an oversight.

## Change Log

<!--
  Required once Status first becomes Approved -- constitution XIII,
  Post-Approval Change Control. Same rule as spec.md's Change Log: Clarification
  /Correction may keep Status: Approved with just this row; Scope change/New
  requirement reverts Status to In Review until re-approved. Also log here
  when an upstream spec.md change (its own Change Log) turns out to affect
  this plan's A0 table, coverage targets, or design rules -- state the
  blast-radius finding even when the answer is "this plan is unaffected."
-->

| Date | Classification | What changed | Blast radius | Status impact |
|------|-----------------|--------------|---------------|----------------|
| [DATE] | [Clarification/Correction/Scope change/New requirement] | [What changed and why] | [What /speckit-analyze found downstream (test-cases.json, tasks.md, automation), or "none yet"] | [Stayed Approved / Reverted to In Review, re-approved DATE by NAME] |

## Summary

[What is being tested, the chosen approach in 3-5 sentences, and the headline
split — e.g. "38 test cases: 26 automated as Playwright e2e, 12 manual
exploratory/visual."]

---

# Part A — Manual Test Strategy

## A1. Test Objectives

- [Objective tied to a TR/risk from spec.md]

## A2. Test Levels & Types

| Level | In Use | Rationale |
|-------|--------|-----------|
| Unit | [Yes/No] | [Owned by dev / covered elsewhere] |
| Integration / API | [Yes/No] | [Which contracts] |
| System / E2E (UI) | [Yes/No] | [Which journeys] |
| Regression | [Yes/No] | [Which existing suite] |
| UAT | [Yes/No] | [Who signs off] |

**Test types in scope**: Smoke, Sanity, Functional, Regression, Negative,
Boundary, Cross-browser, Accessibility, Performance, Security
*(delete those not applicable — do not leave as N/A)*

## A3. Manual Scope — What Stays Manual and Why

| Area | Why manual | Effort |
|------|------------|--------|
| [e.g. Visual layout / brand review] | [Subjective judgement needed] | [Xh] |
| [e.g. First-run exploratory] | [Unknown unknowns before automating] | [Xh] |

## A4. Exploratory Test Charters

| Charter | Explore | With | To discover |
|---------|---------|------|-------------|
| CH-001 | [area] | [tooling/personas] | [risk being probed] |

## A5. Test Execution Approach

- **Cycles**: [e.g. Cycle 1 smoke → Cycle 2 full functional → Cycle 3 regression]
- **Defect workflow**: [Tool, severity/priority scale, triage cadence]
- **Suspension criteria**: [When testing stops, e.g. smoke suite fails]
- **Resumption criteria**: [What must be true to restart]

## A6. Test Environment

| Item | Value |
|------|-------|
| Environments | [QA / Staging URLs — no credentials in this file] |
| Test accounts | [Roles needed; where secrets live, e.g. `.env` / vault] |
| Data seeding | [How state is created and cleaned] |
| Integrations | [Stubs, sandboxes, or live third parties] |

## A7. Schedule, Effort & Roles

| Activity | Owner | Estimate | Dependency |
|----------|-------|----------|------------|
| Test case development | [NAME] | [Xd] | Requirement analysis approved |
| Automation implementation | [NAME] | [Xd] | Framework ready |
| Execution cycle 1 | [NAME] | [Xd] | Build deployed |

## A8. Test Deliverables

- [ ] Requirement analysis (`spec.md`)
- [ ] This test plan (`plan.md`)
- [ ] Test cases (`test-cases.json` + `test-cases.xlsx`)
- [ ] Automation code (`automation/`)
- [ ] Allure execution report
- [ ] Test closure / summary report

---

# Part B — Automation Technical Plan

## B1. Automation Candidacy

Cases are automated when they are **repeatable, deterministic, and
business-valuable**. Record the decision explicitly:

| Criterion | Threshold |
|-----------|-----------|
| Executed every regression cycle | Automate |
| Stable UI / contract | Automate |
| High business risk (P1) | Automate first |
| One-off, subjective, or exploratory | Keep manual |
| Blocked by missing testability hooks | Defer — raise with dev |

**Target automation coverage**: [e.g. 100% of P1, 70% of P2, 0% of P3]

## B2. Technology Stack

| Concern | Choice | Version | Notes |
|---------|--------|---------|-------|
| Language | Python | [3.11+] | |
| Test runner | pytest | [8.x] | |
| Browser driver | Playwright (sync API) | [1.4x] | via `pytest-playwright` |
| Design pattern | Page Object Model | — | Pages expose intent, never raw locators |
| Reporting | Allure | [allure-pytest 2.x] | |
| Parallelism | pytest-xdist | [3.x] | [`-n auto` / disabled and why] |
| Flake control | pytest-rerunfailures | [15.x] | [max reruns policy] |
| Config | python-dotenv | — | secrets from env only |

## B3. Framework Structure

```text
automation/
├── conftest.py            # GLOBAL fixtures only: settings, browser context, Allure hooks
├── utils/                 # base_page.py, config.py, logger.py, data_loader.py
├── pages/                 # Page Object Model — one class per feature
│   └── [feature]_page.py
├── locators/              # locator constants, kept out of page logic
│   └── [feature]_locators.py
├── test_data/             # static test data (JSON) — no secrets
│   └── [feature].json
└── tests/
    ├── ui/                # browser-driven UI tests, named test_*.py
    │   ├── conftest.py    # page-object fixtures + browser-only autouse fixtures
    │   └── test_[feature].py
    └── api/               # API-level tests, no browser
```

**Structure decision**: [Confirm or amend the tree above with the real paths
this feature adds. One feature owns exactly one file per layer — a page
object, a locator module, a test-data file, a test file. Do not introduce a
new top-level layer — if one seems needed, raise it as a framework change
first.]

## B4. Design Rules

- **Locator strategy**: [Priority order, e.g. `get_by_role` → `get_by_label` →
  `data-testid` → CSS. XPath only as a last resort, with a comment explaining why.]
- **Waiting**: Playwright auto-waiting and web-first assertions (`expect`) only.
  No `time.sleep`, no hard-coded timeouts outside config.
- **Page objects**: return page objects or data, never assertions. Assertions
  live in tests.
- **Test independence**: every test creates and cleans its own state; tests must
  pass in any order and in parallel.
- **Naming**: `test_<TCID>_<behaviour>` so the report links back to the test case.
- **Traceability**: each test carries `@allure.testcase` / marker with its `TC-xxx` id.

## B5. Test Data Strategy

| Approach | Used for | Mechanism |
|----------|----------|-----------|
| Static fixtures | [stable reference data] | `automation/test_data/*.json` |
| Generated | [unique per-run entities] | [faker / timestamped ids] |
| Seeded via API | [preconditions] | [endpoint + teardown] |

**Secrets**: sourced from environment (`.env`, CI secret store). Never committed.

## B6. Reporting & CI

- **Local run**: `.specify/scripts/bash/run-tests.sh`
- **Results**: `reports/allure-results` → HTML in `reports/allure-report`
- **Attachments on failure**: screenshot, page HTML, Playwright trace, video
- **CI trigger**: [PR / nightly / on-demand]
- **Quality gate**: [e.g. P1 suite must be 100% green to merge]

## B7. Risks to Automation

| Risk | Mitigation |
|------|------------|
| [e.g. Dynamic ids break locators] | [Request `data-testid` from dev — raise as ticket] |
| [e.g. Third-party sandbox instability] | [Stub at network layer] |

---

## Constitution Check

*GATE: must pass before test case development. Re-check after design.*

[Evaluate this plan against `.specify/memory/constitution.md`. List each
principle and whether the plan complies.]

## Complexity Tracking

> Fill ONLY if the Constitution Check has violations that need justification.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g. XPath locators] | [legacy app, no test ids] | [role selectors unavailable] |

## Artifacts Produced by This Phase

```text
specs/[###-feature]/
├── spec.md              # Requirement analysis (/speckit-specify)
├── plan.md              # This file (/speckit-plan)
├── research.md          # Tooling/approach decisions (/speckit-plan)
├── data-model.md        # Test data model (/speckit-plan)
├── quickstart.md        # Environment setup & how to run (/speckit-plan)
├── test-cases.json      # Canonical test cases (/speckit-tasks)
├── test-cases.xlsx      # Excel deliverable (/speckit-tasks)
├── tasks.md             # Automation work breakdown (/speckit-tasks)
└── reports/             # Execution results (/speckit-test)
```
