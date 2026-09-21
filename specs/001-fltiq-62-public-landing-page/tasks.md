# Test Case Development & Automation Tasks: FLTIQ-62 — Build the public landing page

**Test Basis**: [spec.md](./spec.md) | **Test Plan**: [plan.md](./plan.md) | **Date**: 2026-09-19
**Test-case gate** (constitution XI.a): `test-cases.xlsx` reviewed for adequacy of coverage and approved by Sajid Mohammad on 2026-09-21, covering all 43 cases as they stand after the TR-018/TR-020 updates above.

> STLC Phase 3 — Test Case Development. Produced by `/speckit-tasks`.
> The **test cases** themselves live in `test-cases.json` (canonical) and
> `test-cases.xlsx` (deliverable). This file is the **work breakdown** that
> turns those cases into runnable automation, ordered by dependency.

## Test Case Summary

| Metric | Count |
|--------|-------|
| Total test cases | 43 |
| P1 / P2 / P3 | 22 / 16 / 5 |
| Automated (target) | 41 |
| Manual | 1 (TC-035, TR-015) |
| Blocked | 1 (TC-043/EC-003) |
| Scenarios covered | 5 of 5 |
| Requirements covered | 20 of 20 `TR-xxx` — **all with real coverage now**; TR-018 and TR-020 (both resolved 2026-09-21) are no longer Blocked placeholders |

*(TC-013/T018 and TC-040/T015 were removed 2026-09-21 -- see Change Log. Ids
are not renumbered/reused; they simply no longer exist. TC-044/T046 added the
same day: TR-003 requires the header render the "Capabilities"/"Hierarchy"
section-anchor links, and no case asserted their presence. TC-045/T047 added
the same day too: each link must navigate to its own correct, distinct
section — not guaranteed by the browser, unlike the generic scroll mechanism
EC-004 still correctly waives. Both found from a design/screenshot review,
both distinct from TC-040's removed click-scroll test. TC-042/T049 unblocked
the same day too, once §13b Q2 was answered ("skeleton loader") and TR-020
created — the last of the four originally-open questions to resolve.)*

**Deliverables**: `test-cases.json`, `test-cases.xlsx`, `test-cases.md`

## Change Log

*(Constitution XIII, Post-Approval Change Control. `tasks.md`/`test-cases.json`
don't carry a `Status:` header, but the same discipline applies once this
file has been through the test-case gate — constitution XI.a. No edit has
been made since this file was first written; the row below is the template
this file will use once one occurs.)*

| Date | Classification | What changed | Blast radius | Re-reviewed? |
|------|-----------------|--------------|---------------|----------------|
| 2026-09-21 | Correction | Removed TC-013 (session-expiry-on-reload) and its task T018. The underlying `spec.md` Scenario 2 negative-flow item was found, on a user question, to describe behaviour ("redirected to sign-in") that neither TR-001 nor TR-002 state and that belongs to FLTIQ-31/session-lifecycle scope, not this page -- see `spec.md` Change Log, same date. | Neither TC-013 nor T018 had been implemented -- zero automation code affected. TR-002's remaining case (TC-009) and task (T016) are unaffected. Phase 4's test-case list and the Traceability table updated below. | No re-review needed -- caught before implementation |
| 2026-09-21 | Correction | Removed TC-040 (anchor-link scroll behaviour) and its task T015. `spec.md` §12 already classified the underlying EC-004 as INFERRED, "not a distinct product requirement" -- a user question caught that a full asserting test case had been written for it anyway, in violation of constitution II, and that its TR-003 citation didn't hold up either (TR-003 covers presence/order, not scroll behaviour). EC-004 now carries an explicit waiver in `spec.md` §5 instead of a case. | Neither TC-040 nor T015 had been implemented. TR-003's remaining cases (TC-005, TC-028) and tasks (T012, T032) are unaffected. Phase 3's test-case list and the Traceability table updated below. | No re-review needed -- caught before implementation |
| 2026-09-21 | New requirement (coverage gap, not a spec change) | Added TC-044 and its task T046. A design-screenshot review found that TR-003's own text -- "the header renders ... the section anchors (Capabilities, Hierarchy) ..." -- had zero test coverage; the two prior TR-003 cases (TC-005, TC-028) cover the product mark's behaviour and the Sign-in/Create-account order, not the presence of these two links. Distinct from the correctly-removed TC-040: this covers presence, which TR-003 already requires; TC-040 covered click-scroll behaviour, which no source requires. | TR-003's other cases/tasks (TC-005/T012, TC-028/T032) unaffected. `spec.md` §14 Traceability Seed's TR-003 row updated to add TC-044. No `TR-xxx` wording changed -- this closes a coverage gap against existing text, not a new product decision. | No re-review needed -- caught before implementation |
| 2026-09-21 | New requirement (coverage gap, not a spec change) | Added TC-045 and its task T047. A further requester screenshot walkthrough (clicking both links, showing each lands on its own distinct section) caught that EC-004's waiver had swept in more than the generic scroll mechanism -- link/section *correctness* (this link wired to this section's id, not swapped) is not browser-guaranteed and is verifiable against the design source's explicit href/id pairing, same basis as TC-005's product-mark check. `spec.md` EC-004 row narrowed to state the distinction explicitly; §4 Scenario 1 gained acceptance items 7-8. | TR-003's other cases/tasks unaffected. `spec.md` §14 updated to add TC-045. No `TR-xxx` wording changed -- closes a correctness gap against TR-003's existing text (a real bug class: mismatched navigation), not a new product decision. | No re-review needed -- caught before implementation |
| 2026-09-21 | New requirement | The team answered `spec.md` §13a Q1 (CF-002): TR-018 resolved DEFINED, ships as designed. TC-039 converted from a Blocked placeholder to a real asserting case; task T048 added (Phase 7). TC-043's Blocked entry narrowed to match the related §13b Q3 partial answer -- the shared-JS-bundle risk to the CTAs it originally flagged is resolved, only the explorer's own fallback UI remains unanswered. Test Case Summary and Traceability table updated (Blocked 3 -> 2, Automated 39 -> 40). | No other case/task affected. This mirrors `spec.md`'s own classification -- see its Change Log, same date, for the full resolution and blast-radius reasoning. | Re-review needed once `spec.md`/`plan.md` are re-approved -- this file has no `Status:` gate of its own, but its content now assumes TR-018 is DEFINED |
| 2026-09-21 | Correction | A user question ("we have six edge cases in spec.md, and have 4 in tasks.md, why?") caught that the Traceability table only ever listed 4 of `spec.md` §5's 6 edge cases (EC-001, EC-003, EC-004, EC-005) -- EC-002 and EC-006 were always covered (TC-014/T019 and TC-019/T023 respectively) but never got their own row, so a reviewer scanning this table alone would have missed that they existed at all. Added both rows. | No coverage changed -- both were already tested; this closes a table-completeness gap, not a testing gap. | Stayed as-is -- no content assertion changed, just a missing row |
| 2026-09-21 | New requirement | §13b Q2 answered ("skeleton loader") -- the last of the original 4 open questions. `spec.md` created TR-020 (wholly new, not previously named by any source). TC-042 converted from Blocked to a real case; task T049 added (Phase 3). Blocked table down to 1 (TC-043 only). Traceability table's EC-001 row updated from Blocked to real, and a new TR-020 row added. | No other case/task affected. Mirrors `spec.md`'s own classification -- see its Change Log, same date. | Re-review needed once `spec.md`/`plan.md` are re-approved, same as the TR-018 entry above -- this adds to the same pending batch |
| 2026-09-21 | Correction (coverage gap, not a spec change) | TC-005 and TC-034 extended to assert the product mark's square icon contains "F", after a requester screenshot comparison against the design asked whether the icon matched and whether anything covered it. It did not: TR-003 ("a square icon containing \"F\" beside the \"FleetIQ\" wordmark") and TR-010 ("the same square \"F\" icon") both state the glyph, but every existing case asserted only behaviour (TC-005/TC-008) or the wordmark text (TC-034). No new `TC-xxx` added, per the standing preference to extend existing cases. | Both now **fail**: the icon renders as an empty square (no text node, no `::before` content, no background image) — header 11x11px, footer 9x9px, `rgb(11,63,168)`. Logged as defect **D8** in `reports/test-report-cycle-1.md`. `landing_page.py` gained `header_mark_icon_text()`/`footer_mark_icon_text()`, which return the glyph text so the test owns the assertion (constitution VII). `spec.md` §14's TR-003/TR-010 rows updated. | No requirement re-review needed — no `TR-xxx` text changed |
| 2026-09-21 | Correction (coverage gap, not a spec change) | TC-005 and TC-006 extended to exercise a **second** scroll-and-click cycle, after a user question asked why repeating the sequence failed. Both cases previously asserted a single click on a freshly-loaded page, which is all their steps described — so both passed while the real behaviour was broken. TR-003 and TR-010 state the scroll-to-top behaviour with no first-click-only qualifier, and a control experiment (a plain `<a href="#top">` page) re-scrolled on every click, confirming the app is breaking standard browser behaviour rather than the requirement being over-read. No new `TC-xxx` added — the existing cases now cover what their requirements always required. | Both cases now **fail** on attempt 2 (`scrollY=850`, `url=…/#top`), exposing a Product Defect: once the fragment is `#top`, any further `href="#top"` click is a same-fragment navigation the app no-ops. Confirmed to affect *both* elements and to cross between them (clicking the header mark also disables the footer link). `spec.md` §14's TR-003/TR-010 Automation column updated; `landing_page.py`'s `wait_for_scroll_top()` replaced by `scrolled_to_top_within()`, which returns data so the test owns the assertion (constitution VII). | No re-review of requirements needed — no `TR-xxx` text changed; this is coverage of existing text plus a defect finding |
| 2026-09-21 | Correction | `/speckit-implement` executed all 39 non-blocked, non-manual tasks against the actual running dev server (not just the design mockup). All checkboxes above updated to `[X]` with a pass/fail note per task, except T038, left unchecked: `test-cases.json` (authoritative) records TC-035 as `automatable: false`/Manual, contradicting T038's own "automated half only" premise -- writing a partial automated audit would have silently overridden that record rather than corrected it first. 16 of 41 implemented cases fail against the real build (Product Defects, not test defects -- see the Completion Report for the full list); tests were kept as spec'd, not weakened, per constitution VI. | `test-cases.json`'s `automation_status`/`test_file` fields and `spec.md` §14's Automation column updated to match (same date, their own records). No `TR-xxx` or `TC-xxx` content changed -- this is execution evidence, not a scope edit. | No re-review needed -- this is a status update, not a change to what any case asserts |

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

- [x] T001 Install automation dependencies from `requirements.txt`
- [x] T002 Install Playwright browsers (`playwright install --with-deps`)
- [x] T003 Configure `.env` from `.env.example` — `BASE_URL=http://localhost:3000`, `TEST_ENV=local` (test account credentials left blank — none was provisioned; TC-009 conditional-skips per research.md R5)
- [x] T004 Verify `automation/tests/test_framework_wiring.py` passes (browserless self-check, no `.env`/browser needed)
- [x] T005 Verify the local dev server responds at `http://localhost:3000` (root URL reachable, smoke-passable) before feature work begins — spec.md §10 Entry Criteria

---

## Phase 2: Framework Foundation

**Purpose**: shared building blocks every scenario depends on. **Blocking** —
no scenario phase starts until this completes.

- [x] T006 [P] Add locators for every header/hero/capabilities/hierarchy/closing/footer element in `automation/locators/landing_locators.py`
- [x] T007 Add `LandingPage` page object in `automation/pages/landing_page.py`, extending `BasePage` — exposes intent only (`click_create_account(location)`, `click_sign_in(location)`, `select_hierarchy_node(label)`, etc.), never asserts (plan.md B4)
- [x] T008 [P] Add the five-record `HierarchyNode` fixture (data-model.md) to `automation/test_data/landing.json`
- [x] T009 [P] Register a `landing_page` fixture (constructing `LandingPage(page, settings)`) in `automation/tests/ui/conftest.py`, following the existing `example_page` pattern
- [x] T010 Pin an axe-core-based accessibility package in `requirements.txt` (`axe-playwright-python>=0.1.8`, plan.md B2) and verify it imports cleanly

**Note (not a code task)**: raise the `data-testid` request for the hierarchy
detail panel's four value fields (device count, device type, config source,
note) with development per research.md R6 / plan.md B4 — role/label locators
cannot disambiguate these plain `<span>` pairs. Track this outside `tasks.md`
(e.g. a dev-facing ticket); it blocks nothing here since T007's locators use
the plain-label regex approach in the meantime (R6).

---

## Phase 3: Scenario 1 — Unauthenticated visitor discovers FleetIQ and reaches sign-up (Priority: P1)

**Goal**: the entry point and every "Create account" path are airtight; the
header/footer scroll-to-top elements behave correctly and independently.
**Test cases**: TC-001 … TC-008, TC-042, TC-045
**Independent verification**: run this phase alone against a fresh browser
context with no session — all ten cases pass with no dependency on any
other phase.

- [x] T011 [P] [S1] Automate unauthenticated landing-page render and all three "Create account" CTA destinations (header/hero/closing) in `automation/tests/ui/test_landing.py` (covers: TC-001, TC-002, TC-003, TC-004) — all passing
- [x] T012 [P] [S1] Automate the header product-mark and footer "Back to top" independent scroll-to-top behaviours in `automation/tests/ui/test_landing.py` (covers: TC-005, TC-006) — **both FAILING: Product Defect, each element scrolls to the top only on the first click of a page load (see Completion Report / Change Log)**
- [x] T013 [P] [S1] Automate the no-intercepting-modal negative check across all three "Create account" locations in `automation/tests/ui/test_landing.py` (covers: TC-007) — passing
- [x] T014 [P] [S1] Automate the footer-mark non-interactivity negative check in `automation/tests/ui/test_landing.py` (covers: TC-008) — passing
- [x] T047 [P] [S1] Automate the "Capabilities"/"Hierarchy" link-to-correct-section navigation check in `automation/tests/ui/test_landing.py` (covers: TC-045) — **FAILING: Product Defect, links don't exist (see Completion Report)**
- [x] T049 [P] [S1] Automate the skeleton-loader-during-auth-resolution check in `automation/tests/ui/test_landing.py` (covers: TC-042) — **FAILING: Product Defect (or test-technique limitation — see Completion Report); no interceptable auth-check request exists to delay as originally planned, checked the earliest observable frame directly instead**

**Checkpoint**: Scenario 1 suite green in Chromium — a shippable smoke gate on its own (plan.md A5 Cycle 1).

---

## Phase 4: Scenario 2 — Existing user returns and is routed past the landing page (Priority: P1)

**Goal**: the authentication-based routing gate is airtight in both
directions.
**Test cases**: TC-009 … TC-012
**Independent verification**: run this phase alone with one authenticated
test account — all four cases pass without depending on Scenario 1's code.

- [x] T016 [P] [S2] Automate the authenticated-visitor redirect-to-home gate in `automation/tests/ui/test_landing.py` (covers: TC-009) — conditional-skip, no test account provisioned (research.md R5)
- [x] T017 [P] [S2] Automate all three "Sign in" CTA destinations (header/hero/closing) in `automation/tests/ui/test_landing.py` (covers: TC-010, TC-011, TC-012) — all passing

**Checkpoint**: Scenario 2 suite green — the redirect gate holds for both unauthenticated and authenticated visitors.

---

## Phase 5: Scenario 3 — Visitor explores the hierarchy explorer without triggering a backend call (Priority: P1)

**Goal**: the hierarchy explorer proves out as a safe, self-contained,
fully-data-driven demo.
**Test cases**: TC-014 … TC-021
**Independent verification**: run this phase alone with a network listener
attached — all eight cases pass with zero backend dependency.

- [x] T019 [P] [S3] Automate default-selection ("Floor 1" pre-selected) and node-selection detail-panel update in `automation/tests/ui/test_landing.py` (covers: TC-014, TC-015) — **FAILING: Product Defect, no detail panel exists (see Completion Report)**
- [x] T020 [P] [S3] Automate the no-FleetIQ-API-call network assertion during hierarchy interaction in `automation/tests/ui/test_landing.py` (covers: TC-016) — passing
- [x] T021 [P] [S3] Automate the `meta`-vs-`devices` field distinction for Building A/B in `automation/tests/ui/test_landing.py` (covers: TC-017) — **FAILING: same detail-panel defect**
- [x] T022 [P] [S3] Automate the selected-row visual-highlight assertion via `aria-pressed` in `automation/tests/ui/test_landing.py` (covers: TC-018) — **FAILING: same detail-panel defect (no aria-pressed at all)**
- [x] T023 [P] [S3] Automate the zero-device node (Building B) boundary render in `automation/tests/ui/test_landing.py` (covers: TC-019) — **FAILING: same detail-panel defect**
- [x] T024 [P] [S3] Automate the all-five-nodes exact-`note`-text data-variation sweep in `automation/tests/ui/test_landing.py` (covers: TC-020) — **FAILING: same detail-panel defect**
- [x] T025 [P] [S3] Automate the largest-value node ("Unassigned", 501 devices) render at 360px in `automation/tests/ui/test_landing.py` (covers: TC-021) — **FAILING: same detail-panel defect**

**Checkpoint**: Scenario 3 suite green — confirmed no unplanned coupling to the not-yet-agreed FLTIQ-59 API contract.

---

## Phase 6: Scenario 4 — The landing page meets the epic's accessibility and responsive baseline (Priority: P1)

**Goal**: WCAG 2.1 AA and the 360px responsive baseline hold across the
page, including the custom hierarchy-explorer control.
**Test cases**: TC-022 … TC-027, TC-041
**Independent verification**: run this phase alone at 360px, keyboard-only,
and 200%-zoom-equivalent viewports — all seven cases pass independently of
Scenarios 1–3.

- [x] T026 [P] [S4] Automate the 360px no-horizontal-scroll/no-truncation check in `automation/tests/ui/test_landing.py` (covers: TC-022) — passing
- [x] T027 [P] [S4] Automate the full keyboard-reachability and focus-indicator sweep in `automation/tests/ui/test_landing.py` (covers: TC-023) — passing (excludes the Next.js dev-tools overlay and end-of-document focus loss as non-page-content, test mechanics)
- [x] T028 [P] [S4] Automate the no-keyboard-trap forward/backward Tab sweep in `automation/tests/ui/test_landing.py` (covers: TC-024) — passing
- [x] T029 [P] [S4] Integrate the axe-core contrast scan (needs T010) and assert WCAG 2.1 AA thresholds in `automation/tests/ui/test_landing.py` (covers: TC-025) — **FAILING: Product Defect, 9 serious color-contrast violations (see Completion Report)**
- [x] T030 [P] [S4] Automate the 200%-zoom-equivalent (halved-viewport) usability check, including the combined 360px+200%-zoom boundary variant, in `automation/tests/ui/test_landing.py` (covers: TC-026, TC-041) — both passing
- [x] T031 [P] [S4] Automate hierarchy-explorer keyboard operability (Enter/Space selection, matching focus indicator) in `automation/tests/ui/test_landing.py` (covers: TC-027) — **FAILING: same hierarchy-explorer defect as TR-008 (no interactive semantics to operate via keyboard)**

**Checkpoint**: Scenario 4 suite green — the epic's most-visible-page accessibility bar is met.

---

## Phase 7: Scenario 5 — Page content and structure match the approved scope (Priority: P2)

**Goal**: every section's copy, order, and structural presence matches the
approved design exactly, and no MVP1-unsupported claim ships.
**Test cases**: TC-028 … TC-039, TC-044 (TR-018/CF-002 resolved 2026-09-21 — TC-039 is a real case now, not excluded)
**Independent verification**: run this phase alone as a static DOM/content
review — all thirteen cases pass independently of any interaction flow.

- [x] T032 [P] [S5] Automate the header CTA-order assertion (Sign in before Create account) in `automation/tests/ui/test_landing.py` (covers: TC-028) — passing
- [x] T033 [P] [S5] Automate the hero exact-copy and CTA-order assertions (Create account before Sign in) in `automation/tests/ui/test_landing.py` (covers: TC-029, TC-030) — TC-030 passing; **TC-029 FAILING: Product Defect, subhead/stats copy diverges from spec (see Completion Report)**
- [x] T034 [P] [S5] Automate the capabilities section's exact heading and six-card copy assertion in `automation/tests/ui/test_landing.py` (covers: TC-031) — **FAILING: Product Defect, cards 02/03/06 use contractions not in spec**
- [x] T035 [P] [S5] Automate the hierarchy section's exact heading and intro-paragraph copy assertion in `automation/tests/ui/test_landing.py` (covers: TC-032) — passing
- [x] T036 [P] [S5] Automate the closing section's exact copy and CTA-order assertion in `automation/tests/ui/test_landing.py` (covers: TC-033) — **FAILING: Product Defect, body uses "You'll" not spec's "You will"**
- [x] T037 [P] [S5] Automate the footer presence assertion (mark, copyright, Back to top) in `automation/tests/ui/test_landing.py` (covers: TC-034) — **FAILING: Product Defect, no "©ACL Digital" text anywhere in the footer**
- [ ] T038 [P] [S5] Automate the partial design-system token/component usage audit for TR-015 (covers: TC-035) — **not implemented.** `test-cases.json` (authoritative, per CLAUDE.md) records TC-035 as `automatable: false` / `automation_status: "Manual"`, which this task's own premise ("automated half only") contradicts. Writing a partial automated audit without first correcting that record would silently override the case's own classification, so no test was added — see the Completion Report.
- [x] T039 [P] [S5] Automate the MVP1-capability-claim checklist comparison in `automation/tests/ui/test_landing.py` (covers: TC-036) — passing
- [x] T040 [P] [S5] Automate the no-analytics/no-tracking network assertion in `automation/tests/ui/test_landing.py` (covers: TC-037) — passing
- [x] T041 [P] [S5] Automate the excluded-content-category absence assertion (pricing/docs/blog/contact/demo, explicitly excluding TR-018's line) in `automation/tests/ui/test_landing.py` (covers: TC-038) — passing
- [x] T046 [P] [S5] Automate the "Capabilities"/"Hierarchy" section-anchor link presence assertion in `automation/tests/ui/test_landing.py` (covers: TC-044) — **FAILING: Product Defect, links don't exist (see Completion Report)**
- [x] T048 [P] [S5] Automate the hero "Free while you set up your first fleet. No card required." presence assertion in `automation/tests/ui/test_landing.py` (covers: TC-039) — passing

**Checkpoint**: Scenario 5 suite green — content/structure matches scope, including TR-018 (resolved 2026-09-21, no longer excluded).

---

## Phase 8: Cross-Cutting & Polish

- [x] T042 [P] Add Allure metadata (epic/feature/story/severity, `@allure.testcase("TC-xxx")`) to every test added in Phases 3–7, in `automation/tests/ui/test_landing.py`
- [x] T043 [P] Add `@pytest.mark.p1/p2/p3`, `a11y`, `boundary`, `negative` markers per each case's actual priority/type from `test-cases.json`, in `automation/tests/ui/test_landing.py`
- [x] T044 Verify the full landing-page suite passes in parallel (`-n auto`) across the Chromium/Firefox/WebKit triad with no order dependence — **verified with a caveat.** Chromium `-n auto`: 24 passed / 16 failed / 1 skipped, identical to serial — no order dependence. WebKit serial: the same 24/16/1 split exactly. Firefox: identical 16 genuine failures at `-n 4`, but the full-suite `-n auto` default (12 workers on this machine) saturated the single dev server and produced 3 additional transient timeouts (TC-007/010/012) that passed cleanly in isolation and at `-n 4` — an environment/CI-capacity limit (too many concurrent browsers against one dev-mode Next.js server), not a test-order or product defect. Recorded here rather than silently rerun until green. **Amendment, 2026-09-21**: these counts predate the TC-005/TC-006 repeat-click extension; the split is now 22 passed / 18 failed / 1 skipped. The parallel and cross-browser conclusions are unchanged — both newly-failing cases were re-verified as deterministic under `-n 2` and on Firefox, failing identically (`scrollY=850`, `url=…/#top`).
- [x] T045 Confirm every automated test's `@allure.testcase` id matches its `TC-xxx`, then update `spec.md` §14's Automation column and `test-cases.json`'s `test_file`/`automation_status` fields — done

---

## Manual Test Cases (not automated)

| TC ID | Title | Priority | Why manual |
|-------|-------|----------|------------|
| TC-035 | Every visual element resolves to a shared design-system token or component | P2 | Pixel-level fidelity to the Keel design isn't a boolean a single Playwright assertion can cleanly cover (spec.md §11); T038 automates the component/token-usage half, a human visual-regression review (plan.md A3, 2h) covers the rest |

Plan.md A3 also keeps three further areas manual that have no individual
`TC-xxx` of their own (they are strategy-level activities, not single
assertions): marketing-copy business-accuracy sign-off (§13b Q1, closed
2026-09-21 without a literal accuracy confirmation — see spec.md Testability
Review), a screen-reader exploratory pass (charter CH-001, also now covering
the script-failure check per CH-002), and a real-device sanity check beyond
the emulated 360px viewport. *(The one-off CF-002/TR-018 verification is no
longer needed — TC-039 asserts it directly now.)*

## Blocked Test Cases (excluded from automation, not silently dropped)

| TC ID | Title | Requirement/Edge Case | Blocked on |
|-------|-------|------------------------|------------|
| TC-043 | Hierarchy explorer's own fallback UI if its client-side script fails to load | EC-003 | `spec.md` §13b Q3 — narrowed 2026-09-21 (rest-of-page risk resolved, explorer's own fallback still unanswered) |

*(TC-042/EC-001 unblocked 2026-09-21 — see Change Log. TC-043/EC-003 is now
the sole remaining Blocked case.)*

None of these three gets a `Txxx` automation task — writing one would
automate an outcome no approved source has defined (constitution II). Revisit
once the corresponding question is answered; at that point `test-cases.json`
is updated (an `automation_status` change, not a `tasks.md` patch) and a new
`Txxx` is added here.

---

## Dependencies

```text
Phase 1 (Environment)
   └─> Phase 2 (Foundation) ── blocking for all scenarios
          ├─> Phase 3 (Scenario 1, P1)   ← MVP: ship this first
          ├─> Phase 4 (Scenario 2, P1)   ← independent of Phase 3
          ├─> Phase 5 (Scenario 3, P1)   ← independent of Phases 3-4
          ├─> Phase 6 (Scenario 4, P1)   ← independent of Phases 3-5 (T029 needs T010)
          ├─> Phase 7 (Scenario 5, P2)   ← independent of Phases 3-6
          └─> Phase 8 (Polish)           ← after all scenarios land
```

## Parallel Execution Opportunities

- Phase 2: T006, T008, T009 run together (different files); T007 depends on T006 (needs the locators it imports)
- Phases 3–7: fully independent of each other once Phase 2 completes — different scenarios, same test file, no shared state (constitution VI)
- Within each scenario phase: tasks are marked `[P]` since each targets a distinct, independent test function in `test_landing.py` with no unmet dependency, following this repo's own template convention — the one exception is T029, which needs T010's dependency pinned first
- Phase 8: T042/T043 can run together; T044 must run last (it verifies the combined result)

## Execution Strategy

1. **MVP**: Phase 1 → Phase 2 → Phase 3. A green Scenario 1 suite is a
   shippable smoke gate on its own (plan.md A5 Cycle 1).
2. **Incremental**: add one scenario phase at a time (4 → 5 → 6 → 7); each
   must stay green before the next starts.
3. **Verify continuously**: run `/speckit-test` after every phase, not just
   at the end — per plan.md A5's three-cycle execution approach (smoke → full
   functional/accessibility/responsive → regression).

## Traceability

| Requirement | Scenario | Test Cases | Automation Task | Test File |
|-------------|----------|------------|-----------------|-----------|
| TR-001 | S1 | TC-001 | T011 | `automation/tests/ui/test_landing.py` |
| TR-002 | S2 | TC-009 | T016 | `automation/tests/ui/test_landing.py` |
| TR-003 | S1, S5 | TC-005, TC-028, TC-044, TC-045 | T012, T032, T046, T047 | `automation/tests/ui/test_landing.py` |
| TR-004 | S1 | TC-002, TC-003, TC-004, TC-007 | T011, T013 | `automation/tests/ui/test_landing.py` |
| TR-005 | S2 | TC-010, TC-011, TC-012 | T017 | `automation/tests/ui/test_landing.py` |
| TR-006 | S5 | TC-029, TC-030 | T033 | `automation/tests/ui/test_landing.py` |
| TR-007 | S5 | TC-031 | T034 | `automation/tests/ui/test_landing.py` |
| TR-008 | S3 | TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-020, TC-021 | T019, T020, T021, T022, T023, T024, T025 | `automation/tests/ui/test_landing.py` |
| TR-009 | S5 | TC-033 | T036 | `automation/tests/ui/test_landing.py` |
| TR-010 | S1, S5 | TC-006, TC-008, TC-034 | T012, T014, T037 | `automation/tests/ui/test_landing.py` |
| TR-011 | S3, S4 | TC-021, TC-022, TC-041 | T025, T026, T030 | `automation/tests/ui/test_landing.py` |
| TR-012 | S4 | TC-023, TC-024, TC-027 | T027, T028, T031 | `automation/tests/ui/test_landing.py` |
| TR-013 | S4 | TC-025 | T029 | `automation/tests/ui/test_landing.py` |
| TR-014 | S4 | TC-026, TC-041 | T030 (both) | `automation/tests/ui/test_landing.py` |
| TR-015 | S5 | TC-035 | T038 (partial) + manual (plan.md A3) | `automation/tests/ui/test_landing.py` |
| TR-016 | S5 | TC-036 | T039 | `automation/tests/ui/test_landing.py` |
| TR-017 | S5 | TC-037, TC-038 | T040, T041 | `automation/tests/ui/test_landing.py` |
| TR-018 | S5 | TC-039 | T048 | `automation/tests/ui/test_landing.py` |
| TR-019 | S5 | TC-032 | T035 | `automation/tests/ui/test_landing.py` |
| TR-020 | S1, S2 | TC-042 | T049 | `automation/tests/ui/test_landing.py` |
| EC-001 | S1 | TC-042 | T049 | `automation/tests/ui/test_landing.py` |
| EC-002 | S3 | TC-014 | T019 | `automation/tests/ui/test_landing.py` |
| EC-003 | — | TC-043 | **Blocked — no task** (§13b Q3, narrowed) | — |
| EC-004 | — | **Waived — no case** (2026-09-21, spec.md §5) | — | — |
| EC-005 | S4 | TC-041 | T030 | `automation/tests/ui/test_landing.py` |
| EC-006 | S3 | TC-019 | T023 | `automation/tests/ui/test_landing.py` |
