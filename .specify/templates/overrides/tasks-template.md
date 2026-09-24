# Test Case Development & Automation Tasks: [TICKET-ID] — [FEATURE NAME]

**Test Basis**: [spec.md] | **Test Plan**: [plan.md] | **Date**: [DATE]

> STLC Phase 3 — Test Case Development. Produced by `/speckit-tasks`.
> The **test cases** themselves live in `test-cases.json` (canonical) and
> `test-cases.xlsx` (deliverable). This file is the **work breakdown** that
> turns those cases into runnable automation, ordered by dependency.

## Test Case Summary

| Metric | Count |
|--------|-------|
| Total test cases | [N] |
| P1 / P2 / P3 | [n] / [n] / [n] |
| Automated | [n] |
| Manual | [n] |
| Scenarios covered | [n of n] |

**Deliverables**: `test-cases.json`, `test-cases.xlsx`

## Change Log

<!--
  Constitution XIII, Post-Approval Change Control. tasks.md/test-cases.json
  don't carry a Status: header the way spec.md/plan.md do, but the same
  discipline applies once test cases have been through the test-case gate
  (constitution XI.a): a Clarification/Correction to a case may be made in
  place with a row here; a Scope change/New requirement (the case now
  asserts something different, or a new case is needed) requires the case's
  owner to re-review it before /speckit-implement/-converge treats it as
  trustworthy again. Also log here whenever a spec.md/plan.md Change Log
  entry's blast-radius check found a TC-xxx/task here that needed updating.
-->

| Date | Classification | What changed | Blast radius | Re-reviewed? |
|------|-----------------|--------------|---------------|----------------|
| [DATE] | [Clarification/Correction/Scope change/New requirement] | [Which TC-xxx/task changed and why] | [What /speckit-converge or /speckit-analyze found in automation, or "none yet"] | [No re-review needed / Re-reviewed DATE by NAME] |

## Task Format (REQUIRED)

```text
- [ ] [TaskID] [P?] [Story?] Description with file path (covers: TC-xxx)
```

- **Checkbox**: always `- [ ]`; mark `[X]` when done
- **TaskID**: `T001`, `T002`… in execution order
- **[P]**: include only if parallel-safe (different files, no unmet dependency)
- **[Story]**: `[S1]`, `[S2]`… mapping to scenarios in spec.md — required in
  scenario phases only, omitted in Setup/Foundation/Polish
- **covers**: the test case IDs the task automates — required for every task in
  a scenario phase, so traceability survives into the code

---

## Phase 1: Test Environment Setup

**Purpose**: make the suite runnable before any test is written.

- [ ] T001 Install automation dependencies from `requirements.txt`
- [ ] T002 Install Playwright browsers (`playwright install --with-deps`)
- [ ] T003 Configure environment in `.env` from `.env.example` (base URL, credentials source)
- [ ] T004 Verify the smoke test passes against [environment]

---

## Phase 2: Framework Foundation

**Purpose**: shared building blocks every scenario depends on. **Blocking** —
no scenario phase starts until this completes.

- [ ] T005 [P] Add locators for [feature] in `automation/locators/[feature]_locators.py`
- [ ] T006 Add `[Feature]Page` page object in `automation/pages/[feature]_page.py`
- [ ] T007 [P] Add test data in `automation/test_data/[feature]_data.json`
- [ ] T008 [P] Register the `[feature]_page` fixture in `automation/tests/ui/conftest.py`

---

## Phase 3: Scenario 1 — [Title] (Priority: P1)

**Goal**: [What this scenario proves]
**Test cases**: TC-001 … TC-00n
**Independent verification**: [How to confirm this phase alone is green]

- [ ] T009 [P] [S1] Automate happy path in `automation/tests/ui/test_[feature].py` (covers: TC-001)
- [ ] T010 [P] [S1] Automate negative flow in `automation/tests/ui/test_[feature].py` (covers: TC-002, TC-003)
- [ ] T011 [S1] Automate boundary cases in `automation/tests/ui/test_[feature].py` (covers: TC-004)

**Checkpoint**: Scenario 1 suite green in [browser] — deliverable on its own.

---

## Phase 4: Scenario 2 — [Title] (Priority: P2)

**Goal**: [What this scenario proves]
**Test cases**: TC-0nn …

- [ ] T012 [P] [S2] Automate [behaviour] in `automation/tests/ui/test_[feature].py` (covers: TC-0nn)

**Checkpoint**: Scenario 2 suite green.

---

## Phase 5: Cross-Cutting & Polish

- [ ] T0nn [P] Add Allure metadata (epic/feature/story/severity, `@allure.testcase`) to all new tests
- [ ] T0nn [P] Add cross-browser markers for [browsers] per the plan
- [ ] T0nn Add accessibility checks for [pages] per NFR-002
- [ ] T0nn Verify the full suite passes in parallel (`-n auto`) with no order dependence
- [ ] T0nn Update the traceability matrix in `spec.md` §14

---

## Manual Test Cases (not automated)

| TC ID | Title | Priority | Why manual |
|-------|-------|----------|------------|
| TC-0nn | [Title] | P2 | [Subjective / one-off / blocked] |

---

## Dependencies

```text
Phase 1 (Environment)
   └─> Phase 2 (Foundation) ── blocking for all scenarios
          ├─> Phase 3 (Scenario 1, P1)   ← MVP: ship this first
          ├─> Phase 4 (Scenario 2, P2)   ← independent of Phase 3
          └─> Phase 5 (Polish)           ← after scenarios land
```

## Parallel Execution Opportunities

- Phase 2: T005, T007, T008 run together (different files)
- Phase 3 vs Phase 4: independent once Foundation is done
- Within a scenario: only tasks touching different files carry `[P]`

## Execution Strategy

1. **MVP**: Phase 1 → Phase 2 → Phase 3. A green P1 suite is a shippable
   regression gate on its own.
2. **Incremental**: add one scenario phase at a time; each must stay green.
3. **Verify continuously**: run `/speckit-test` after every phase, not just at
   the end.

## Traceability

<!--
  One row per TR-xxx AND one row per EC-xxx from spec.md -- both lists,
  exhaustively, built now rather than added one at a time whenever an item
  happens to need a fix later. An edge case that never needs fixing still
  needs a row; that's precisely the kind of row a reactive table forgets.
-->

| Requirement | Scenario | Test Cases | Automation Task | Test File |
|-------------|----------|------------|-----------------|-----------|
| TR-001 | S1 | TC-001, TC-002 | T009, T010 | `automation/tests/ui/test_[feature].py` |
| EC-001 | S1 | TC-004 | T011 | `automation/tests/ui/test_[feature].py` |
