# Test Execution Report: FLTIQ-62 — Build the public landing page

**Cycle**: 1 | **Date**: 2026-09-21 | **Environment**: Local dev server (`http://localhost:3000`)
**Executed by**: QA (automated suite) | **Test Plan**: [plan.md](../plan.md)

> STLC Phase 5 — Test Execution & Cycle Closure.
> **Audience: the FleetIQ development team.** Section 4 is grouped by root
> cause rather than by test id, so each block is one fix.

## 1. Execution Summary

| Metric | Value |
|--------|-------|
| Total test cases | 43 |
| Executed (automated) | 42 |
| Passed | 19 |
| Failed | 22 |
| Blocked (not executed) | 1 (TC-043) |
| Manual (not executed) | 0 -- TC-035 partially automated 2026-09-21 (see D9); pixel-fidelity half stays manual per plan.md A3 |
| Skipped | 1 (TC-009 — no test account provisioned) |
| Pass rate | **45%** (19 of 42 executed) |
| Duration | 2m 56s (Chromium, serial) |

**Allure report**: `automation/reports/allure-report/index.html`
**Raw results**: `automation/reports/allure-results/`
**Jira-format defect records** (shareable, one per root cause):
https://claude.ai/artifact/8uzunsp6Qf2CWozuaCyHWP

22 failures resolve to **10 distinct defects**. All were verified as product
behaviour rather than test defects: every assertion was checked against the
approved requirement text, D3 was additionally confirmed against a
control experiment, every copy string was compared against the design
source itself rather than a transcription of it, D9 (styling) was found only
after implementing the token-audit task (T038) that an earlier pass had
incorrectly treated as unautomatable, and D10 was found only after tracing a
requirement citation through to its actual resolution instead of trusting an
older note that said it was still open.

## 2. Results by Priority

| Priority | Total | Passed | Failed | Skipped | Pass rate |
|----------|-------|--------|--------|---------|-----------|
| P1 | 22 | 12 | 9 | 1 | 55% |
| P2 | 15 | 5 | 10 | 0 | 33% |
| P3 | 5 | 2 | 3 | 0 | 40% |

## 3. Results by Scenario

| Scenario | Cases | Passed | Failed | Status |
|----------|-------|--------|--------|--------|
| S1 — Unauthenticated visitor reaches sign-up | 10 | 6 | 4 | **Fail** |
| S2 — Existing user routed past landing page | 4 | 3 | 0 (1 skipped) | Pass |
| S3 — Hierarchy explorer, no backend call | 8 | 1 | 7 | **Fail** |
| S4 — Accessibility & responsive baseline | 7 | 5 | 2 | **Fail** |
| S5 — Content & structure match scope | 13 | 4 | 9 | **Fail** |

## 4. Defects — grouped by root cause

### D1 — Hierarchy explorer is static markup; no detail panel exists

**Severity: Critical** | **Requirements: TR-008 (P1), TR-012 (P1)**
**Fails 8 cases: TC-014, TC-015, TC-017, TC-018, TC-019, TC-020, TC-021, TC-027**

The explorer renders as a `<pre>` block of plain tree-art text. There are no
`<button>` elements, no `aria-pressed`, no click handlers, and **no detail
panel anywhere in the DOM**.

Expected per TR-008: selecting a node updates a detail panel (label, status
badge, device count, device type, config source, note) without a page reload;
"Floor 1" is pre-selected on first render; and the selected row is visually
distinguished from the others.

```
TC-014  AssertionError: no default-selection detail panel is rendered for 'Floor 1'
TC-018  AssertionError: the selected tree row does not expose aria-pressed='true'
TC-015/017/019/020/021  TimeoutError: Locator.inner_text: Timeout 10000ms exceeded
        waiting for [data-testid="hierarchy-detail-*"]
TC-027  AssertionError: hierarchy node did not become selected via keyboard Enter
```

**Accessibility impact**: because the rows are not buttons, the control is not
keyboard-operable at all. That fails TR-012 (WCAG 2.1 AA) independently of the
missing panel.

**Testability request still outstanding** (raised during planning): please add
`data-testid` to the four detail-panel value fields — device count, device
type, config source, note. They are plain `<span>` pairs with no ARIA
semantics, so role- and label-based selectors cannot tell them apart.

---

### D2 — Header renders no "Capabilities" / "Hierarchy" section-anchor links

**Severity: High** | **Requirement: TR-003 (P2)** | **Fails: TC-044, TC-045**

TR-003 requires the header to render the product mark, **the section anchors
(Capabilities, Hierarchy)**, and the Sign in / Create account controls. The
build has only the mark and the two CTAs. The words "Capabilities" and
"Hierarchy" appear solely as `aria-label` values on `<section>` elements —
there are no nav links, so nothing scrolls to those sections.

```
TC-044  AssertionError: header must render a 'Capabilities' section-anchor link
TC-045  TimeoutError: Locator.click: waiting for
        locator("header").get_by_role("link", name="Capabilities", exact=True)
```

---

### D3 — Scroll-to-top works only on the first click of a page load

**Severity: Medium** | **Requirements: TR-003, TR-010** | **Fails: TC-005, TC-006**

Both the header product mark and the footer "Back to top" link return the page
to the top **once**, then stop working for the rest of the session.

Root cause: after the first click the URL is already `…/#top`, so every
subsequent `href="#top"` click is a same-fragment navigation that the app
no-ops. The two controls share the fault — clicking the header mark also
disables the footer link.

```
TC-005  attempt 2: clicking the product mark did not return the page to the top
        (scrollY=850, url=http://localhost:3000/#top)
TC-006  attempt 2: "Back to top" did not return the page to the top
        (scrollY=850, url=http://localhost:3000/#top)
```

**This is not standard browser behaviour.** A control page using a plain
`<a href="#top">` re-scrolled on every click (verified 3 of 3), so a router or
handler in the app is swallowing the repeat navigation. Reproduced
deterministically on Chromium and Firefox, serially and in parallel.

**To reproduce by hand**: scroll to the bottom → click the FleetIQ logo (page
goes up) → scroll down again → click the logo → nothing happens.

---

### D4 — Nine colour-contrast violations (WCAG 2.1 AA)

**Severity: High** | **Requirement: TR-013 (P1)** | **Fails: TC-025**

An axe-core scan reports **9 `color-contrast` violations at impact "serious"**.
TR-013 requires at least 4.5:1 for normal text and 3:1 for large text and
control boundaries.

```
TC-025  AssertionError: contrast violations found: color-contrast (serious) : 9
```

Per-element detail (selector, measured ratio, expected ratio) is in the Allure
attachment for this test. This is contractual under the epic's accessibility
baseline (FLTIQ-53), not a nice-to-have.

---

### D5 — Marketing copy does not match the approved design

**Severity: Low–Medium** | **Requirements: TR-006, TR-007, TR-009**
**Fails: TC-028, TC-029, TC-030, TC-031, TC-033**

Shipped text differs from the approved copy — mostly contractions where the
design uses full forms, plus one substantive rewrite of the hero subhead.

| Where | Approved | Shipped |
|---|---|---|
| **CTA label — all 6 instances** (TR-003/006/009) | "Create account" | "Create an account" |
| Hero subhead (TR-006) | "One place to define device types, organise thousands of units into groups, and review a configuration change before it lands." | "FleetIQ gives you one place to define device types, organise thousands of units into groups, and push configuration changes you can review before they land." |
| Hero stat 3 (TR-006) | "4 roles, from tenant owner to read-only viewer" | "4 roles, from Tenant Owner to read-only Viewer" |
| Card 02 (TR-007) | "…nobody builds a tree the next person **cannot** read." | "…the next person **can't** read." |
| Card 03 (TR-007) | "…then apply — or **do not**." | "…then apply — or **don't**." |
| Card 06 (TR-007) | "**It is not** a filter — **it is** the boundary." | "**It isn't** a filter — **it's** the boundary." |
| Closing body (TR-009) | "**You will** be adding device types the same afternoon." | "**You'll** be adding device types the same afternoon." |

Cards 01, 04 and 05 match exactly. Verified by reading the design source directly and sweeping all 32 design-sourced strings against the build: 20 match exactly, 12 differ (case-sensitive comparison). The hierarchy panel label (`XYZ` vs `XYZ — organisation`) also differs and **is** now raised, as its own defect below (D10) — see the correction there for why it was initially left out. Please confirm which side is authoritative for the seven strings above:
if the shipped wording is intentional, the design source and `spec.md` should
be updated instead of the code.

---

### D10 — Hierarchy panel header text truncated, missing "— organisation"

**Severity: Medium** | **Requirement: TR-008 (P1)** | **Fails: TC-032**

The tree panel's own header line, above the node rows, renders `"XYZ"` where
the design specifies `"XYZ — organisation"` verbatim — the em dash and the
word "organisation" are both missing.

```
TC-032  AssertionError: assert 'XYZ' == 'XYZ — organisation'
```

**Correction, stated plainly.** This report initially excluded this string
from D5, citing `spec.md` §13b Q4 as still open. That citation was stale:
Q4 closed on 2026-09-21 ("today's exact static values are what ships now"),
but nothing acted on that closure for this specific line, and `spec.md` §11
was never updated to say so — so it stayed both untested and mis-cited as
open for a full day. Caught only by a requester screenshot comparison
against the design, not by this report's own review. `spec.md` §11 now
carries a dated correction note, and TR-008 has been amended to name this
line explicitly.

---

### D8 — Product mark renders an empty square; the "F" glyph is missing

**Severity: Medium** | **Requirements: TR-003, TR-010** | **Fails: TC-005, TC-034**

Both requirements describe the mark as a **square icon containing "F"** beside
the "FleetIQ" wordmark. The build renders the square, but it is empty — there
is no letter in it, in either the header or the footer.

```
header icon: iconText='' iconTextContent='' ::before=none background-image=none
             backgroundColor=rgb(11,63,168)  size=11px x 11px
footer icon: same, 9px x 9px
TC-005  AssertionError: the header product mark's square icon does not contain 'F' (got '')
TC-034  AssertionError: the footer mark's square icon does not contain 'F' (got '')
```

The glyph is absent by every mechanism checked — no text node, no `::before`
content, no background image. Visually it reads as a small blue diamond rather
than the design's rounded square with a white "F", and it is also considerably
smaller relative to the wordmark than the design shows.

**Requirement text**: TR-003 — "the product mark (a square icon containing
"F" beside the "FleetIQ" wordmark)"; TR-010 — "the same square "F" icon +
"FleetIQ" wordmark as the header".

---

### D6 — Footer is missing the "©ACL Digital" attribution

**Severity: Low** | **Requirement: TR-010 (P3)** | **Fails: TC-034**

TR-010 requires the footer to show the FleetIQ mark, an "©ACL Digital"
attribution line, and a "Back to top" link. The attribution is absent — the
footer contains only "FleetIQ" and "Back to top".

```
TC-034  AssertionError: assert 'ACL Digital' in 'FleetIQ\nBack to top'
```

---

### D7 — No skeleton loader during authentication resolution

**Severity: Low** | **Requirement: TR-020 (P3)** | **Fails: TC-042**

TR-020 requires a skeleton loader while the visitor's authentication state
resolves at first paint, regardless of the eventual outcome.

```
TC-042  AssertionError: no skeleton loader was observed during the
        auth-resolution window (TR-020)
```

**Caveat, stated plainly**: the build issues **zero** XHR/fetch requests on
load, so there is no async auth-check for the test to intercept and delay; it
samples the earliest observable frame instead. If authentication is resolved
server-side, a client-side loader may never be observable at all — in which
case TR-020 needs revisiting with QA rather than a code change. Happy to pair
on this one before any work starts.

### D9 — Design-system tokens applied to the wrong surfaces

**Severity: High** | **Requirement: TR-015 (P2)** | **Fails: TC-035**

Five of eight checked surfaces render the wrong Keel token, and capability
cards, the hierarchy panel and the header header/border treatment are missing
entirely. This was found only after fixing a gap in the suite itself, not
from a code change -- see the note at the end of this entry.

| Surface | Design token | Design value | Build renders |
| --- | --- | --- | --- |
| Capabilities grid | *(no background)* | transparent | `#E2E5EB` -- **`--keel-border` painted as a background fill** |
| Capability card | `--keel-surface` | `#FFFFFF` | `#F7F8FA` (`--keel-bg`, the *page* background) |
| Hierarchy panel | `--keel-surface` | `#FFFFFF` | transparent (no background at all) |
| Closing section | `--keel-deck-navy` | `#000D35` | `#141922` (`--keel-n-900`, a generic dark neutral) |
| Footer | `--keel-surface` | `#FFFFFF` | `#F7F8FA` (`--keel-bg`) |

Capability cards and the hierarchy panel are also missing the 1px
`--keel-border` border, `--keel-radius-lg` corner radius and `--keel-shadow-sm`
drop shadow the design gives every raised surface; the header is missing its
1px bottom border. Header, stats section and page background are correct.

```
TC-035  AssertionError: design-system token application defects:
        - section[aria-label="Capabilities"] > div: background is rgb(226, 229, 235),
          design declares no background declared in the design (rgba(0, 0, 0, 0))
        - section[aria-label="Capabilities"] > div > div: background is
          rgb(247, 248, 250), design declares --keel-surface (rgb(255, 255, 255))
        - section[aria-label="Hierarchy example"] pre: background is
          rgba(0, 0, 0, 0), design declares --keel-surface (rgb(255, 255, 255))
        - section[aria-label="Get started"]: background is rgb(20, 25, 34),
          design declares --keel-deck-navy (rgb(0, 13, 53))
        - footer: background is rgb(247, 248, 250), design declares
          --keel-surface (rgb(255, 255, 255))
        - section[aria-label="Capabilities"] > div > div: no border, design
          declares 1px solid --keel-border
        - section[aria-label="Capabilities"] > div > div: no border-radius,
          design declares --keel-radius-lg
        - section[aria-label="Capabilities"] > div > div: no box-shadow,
          design declares --keel-shadow-sm
        - section[aria-label="Hierarchy example"] pre: no border, design
          declares 1px solid --keel-border
        - section[aria-label="Hierarchy example"] pre: no border-radius,
          design declares --keel-radius-lg
        - section[aria-label="Hierarchy example"] pre: no box-shadow, design
          declares --keel-shadow-sm
```

**How this was found, stated plainly.** TR-015/TC-035 was originally marked
`automatable: false` and left fully manual, on the reasoning that pixel-level
visual fidelity isn't a boolean a single assertion can cover. `tasks.md`'s own
T038 already called for automating the deterministic half -- a token/component
usage audit -- but that task was skipped, and no styling property was checked
by any test in this suite for the entire first cycle. A requester screenshot
comparison against the design caught a visibly grey block in the capabilities
section that should be a card grid on white; that specific instance led to
implementing the audit T038 always called for, which surfaced the other four.
The lesson generalises: earlier gaps in this cycle (the missing "F" glyph, the
"Create an account" vs "Create account" label) were also found by lenient test
coverage rather than no coverage; this one had no coverage at all.

Since these are shared-surface tokens (backgrounds, borders, radius, shadow),
please check whether the mistake sits in this page's own styles or in the
Keel component library (FLTIQ-60) -- if the latter, every screen in the epic
inherits it.

---

## 5. Not executed

| Case | Why |
|------|-----|
| TC-009 | **Skipped** — no authenticated test account provisioned (`TEST_USERNAME`/`TEST_PASSWORD` unset). The authenticated-redirect gate (TR-002, **P1**) is therefore **unverified**. Please provision a least-privileged QA account so this can run. |
| TC-043 | **Blocked** — the explorer's fallback when its client-side script fails to load is unspecified by any source (spec.md §13b Q3). Needs a product decision before a test can be written. |
| TC-035 | **Partially automated** — the token-application audit now runs (see D9) and fails; the pixel-fidelity/visual-regression half stays manual per plan.md A3. |

## 6. What passed

Worth stating, because it scopes the work: the primary conversion paths are
sound. All six "Create account" / "Sign in" CTAs route correctly (TR-004,
TR-005) with no intercepting modal; the footer mark is correctly
non-interactive; the 360px and 200%-zoom responsive baselines hold; keyboard
reachability and focus indicators pass with no keyboard trap; the page makes
no analytics or tracking calls and contains no out-of-scope content; and the
hierarchy section's own heading and intro paragraph match the design verbatim.

## 7. Verdict

**NO-GO for release.**

Blocking items: **D1** (a P1 requirement is essentially unimplemented), **D4**
(contractual accessibility baseline), **D2**, and **D9** (widespread token
misapplication, epic-scope risk if it sits in FLTIQ-60 rather than this page).
TR-002 also remains unverified for want of a test account.

Suggested order: D1 → D4 → D9 → D2 → D3 → D8 → D5 → D10 → D6 → D7.

Re-run after fixes with `.specify/scripts/bash/run-tests.sh`. The suite is
deterministic — it reproduces the same 18 failures on Chromium, Firefox and
WebKit, serially and in parallel — so any change in the numbers is a real
change in behaviour.
