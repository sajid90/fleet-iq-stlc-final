# Requirement Analysis: FLTIQ-62 — Build the public landing page

**Ticket**: `FLTIQ-62` | **Source**: https://fleetiq-acldigital.atlassian.net/browse/FLTIQ-62
**Analysed**: 2026-09-18 | **Analyst**: Claude (speckit-specify)
**Source manifest**: `source-manifest.json`
**Status**: Approved
**Approved by**: Sajid Mohammad | **Approved on**: 2026-09-18
**Re-confirmed**: 2026-09-18, after design-source cross-check additions (button order, header click-to-top, hierarchy tree-row `meta` vs. detail-panel `devices`, exact `note` text, and Sign-in's third location) made during `/speckit-plan` — reviewed and accepted by Sajid Mohammad without requiring a new approval cycle, since every addition is a source-verified clarification, not a new product decision
**Re-confirmed**: 2026-09-19, after a full §15a UI Element Enumeration retrofit (Pass 0 + six structural passes over the entire Claude Design project, run per the updated `/speckit-specify` 1F.3 procedure) — reconciled cleanly against every existing requirement with exactly one new finding (the hierarchy tree row's own selected-state highlight, added to TR-008 and Scenario 3 below); see §15a for the full enumeration and its counts
**Input**: "FLTIQ-62"

> STLC Phase 1 — Requirement Analysis. This document is the **test basis**.
> Everything downstream (test plan, test cases, automation) traces back to a
> `TR-xxx` identifier defined here. No implementation detail belongs in this file.

## Change Log

Formalized retroactively 2026-09-19 per constitution XIII (Post-Approval
Change Control), added after this ticket's own history showed the same
"was this a real change or just a note" judgment being made ad hoc, in
conversation, more than once. Both entries below were already summarized in
the `Re-confirmed` header lines above; this table is their structured record.

| Date | Classification | What changed | Blast radius | Status impact |
|------|-----------------|--------------|---------------|----------------|
| 2026-09-18 | Clarification | Design-source cross-check additions made during `/speckit-plan`: button order per section (TR-003/006/009), header click-to-top behaviour (TR-003), footer's plain-text mark and "Back to top" behaviour (TR-010), hierarchy tree-row `meta` vs. detail-panel `devices` distinction (TR-008), exact `note` text for all five nodes (data-model.md), Sign-in's third location (TR-005), and TR-019 (hierarchy section heading/body). Every item verified verbatim against the design source already resolved at Approval — no new source, no new product decision. | `plan.md` A0 table needed its TR-003/TR-005 Authority rows updated to add `presentation-and-interaction` (done same day). No `test-cases.json`/`tasks.md`/automation existed yet to check. | Stayed Approved — reviewed and accepted by Sajid Mohammad without a new approval cycle |
| 2026-09-19 | Clarification | §15a UI Element Enumeration retrofit (Pass 0 + six structural passes over the full Claude Design project, per the updated `/speckit-specify` 1F.3 procedure). One new finding: the hierarchy tree row's own selected-state highlight was never asserted — added to TR-008's wording and as Scenario 3 item 5. Everything else enumerated reconciled cleanly against existing TRs. | Ran `/speckit-analyze`-equivalent reasoning manually (no `test-cases.json`/`tasks.md` exist yet): TR-008's Class/Authority/Priority are unchanged, so `plan.md`'s A0 row for TR-008 needed no edit. `plan.md` itself is still `Status: Draft`, so nothing downstream was consuming the old TR-008 wording as approved. | Stayed Approved — source-verified clarification, no new product decision; not yet reviewed by Sajid Mohammad in this form (see Completion Report) |
| 2026-09-19 | Clarification | §3a Acceptance Criteria Index gained a "count per source, and how derived" statement (7 from the Story AC field, 4 from PRD 1) — closing a gap against a Step 8 checklist item added to `/speckit-specify` in the same change-control update. No AC row, TR, or source changed; only a summary statement was added. | None — §3a's row content is unchanged, only a summary added above the table. No downstream artifact references this statement directly. | Stayed Approved |

## 1. Requirement Summary

FleetIQ's root URL currently serves nothing — a prospective customer who hears
about the product has nowhere to land before sign-up or sign-in. This story
builds a public, unauthenticated marketing/landing page at the root URL that
explains what FleetIQ does, gives an interactive preview of its device
hierarchy model, and gets a visitor to "Create account" in one click. An
already-authenticated visitor is redirected past it to their own home page.
The page is explicitly a late backlog addition (S-25) with no dedicated PRD
section of its own, but it still inherits the epic's cross-cutting
accessibility and responsive requirements like every other screen in the
Tenant, Identity & Access layer.

## 2. Scope

### In Scope

- Public, unauthenticated page served at the FleetIQ root URL (React app)
- Header: product mark, section anchors (Capabilities, Hierarchy), Sign in / Create account
- Hero: positioning line, both calls to action, three supporting statistics
- Six capability cards: device types first; a hierarchy that holds; review before it applies; roles people understand; a complete audit trail; tenant isolation
- Interactive hierarchy explorer: selectable node tree + detail panel, static local data, no API call
- Closing section: restates the three-step setup, repeats both CTAs
- Footer: ACL Digital attribution, back-to-top link
- Redirect of an already-authenticated visitor to their home page
- Responsive to 360px width and WCAG 2.1 AA, consistent with the rest of the Tenant, Identity & Access epic

### Out of Scope

- The sign-up and sign-in screens themselves — covered by FLTIQ-33 and FLTIQ-35. The design's own intercept-modal behaviour is explicitly prototype scaffolding, verified verbatim in the design source ("This prototype covers the landing page only" / "not part of this prototype yet"); the real app must navigate to the real screens with no modal (see FLTIQ-62's own "Note on the design prototype")
- Pricing, documentation, blog, contact form, demo request, and **analytics** — none is in MVP1 (see TR-017). **Caveat**: the design source itself contains one line that reads as pricing-adjacent microcopy — see TR-018 and CF-002, unresolved.
- Content management — copy ships with the application; changing it requires a release
- SEO beyond a page title and meta description

### Deferred

- None identified. No requirement in this story's approved sources was flagged as "part of this feature, scheduled elsewhere."

## 3. Testable Requirements

| ID | Requirement | Source (AC / PRD ref) | Authority | Class | Type | Priority | Risk |
|----|-------------|-----------------------|-----------|-------|------|----------|------|
| TR-001 | The FleetIQ root URL serves the public landing page to an unauthenticated visitor; no sign-in is required to view it | unbracketed-1 | scope-and-story-acceptance | DEFINED | Functional | P1 | High |
| TR-002 | An already-authenticated visitor who opens the root URL is redirected to their home page; the landing page is not shown | unbracketed-4 | scope-and-story-acceptance | DEFINED | Functional | P1 | High |
| TR-003 | The header renders the product mark (a square icon containing "F" beside the "FleetIQ" wordmark), the section anchors (Capabilities, Hierarchy), and the Sign in / Create account controls **in that order — Sign in first, then Create account**. The header's product mark is a link that scrolls the page back to the top (`href="#top"`). | Story §Scope bullet 2; icon, order and click-to-top behaviour all verified verbatim in the design source | scope-and-story-acceptance + presentation-and-interaction | DEFINED | UI | P2 | Medium |
| TR-004 | Clicking "Create account" from the header, the hero, or the closing section navigates to the real sign-up screen (FLTIQ-33) — never to an intercepting modal. All three instances must be verified independently. | unbracketed-2 + "Note on the design prototype", confirmed verbatim in the design's own modal-copy ("This prototype covers the landing page only") | scope-and-story-acceptance | DEFINED | Functional | P1 | High |
| TR-005 | Clicking "Sign in" from the header, the hero, or the closing section navigates to the real sign-in screen (FLTIQ-35) — never to an intercepting modal. All three instances must be verified independently, on the same basis as TR-004: the design confirms "Sign in" appears in all three locations, even though the story's own AC field only enumerated this explicitly for "Create account" (see §11 finding). | unbracketed-3 + "Note on the design prototype", confirmed verbatim in the design's own modal-copy ("not part of this prototype yet"); location count corroborated by the design source (all three CTA groups pair Sign in with Create account) | scope-and-story-acceptance + presentation-and-interaction | DEFINED | Functional | P1 | High |
| TR-006 | The hero section renders the badge "Multi-tenant device management," the headline "Every device in your fleet, in one hierarchy.", the subhead "One place to define device types, organise thousands of units into groups, and review a configuration change before it lands.", three supporting statistics: "500+ devices onboarded in a single import," "3 levels of grouping, enforced by the platform," "4 roles, from tenant owner to read-only viewer," and both calls to action **in the order Create account, then Sign in** | Story §Scope bullet 3; exact copy and button order verified verbatim against the Claude Design source (`FleetIQ Landing.dc.html`) | scope-and-story-acceptance + presentation-and-interaction | DEFINED — one statistic flagged, see §11 | Functional/UI | P2 | Medium |
| TR-007 | The capabilities section renders the heading "Built for fleets that outgrew the spreadsheet." followed by six capability cards with this exact title/body copy: "01 Device types first — Describe a model once — its telemetry, its settings, its identifiers — and every unit you add inherits it."; "02 A hierarchy that holds — Organisation, group, subgroup. Three levels, no deeper, so nobody builds a tree the next person cannot read."; "03 Review before it applies — Configuration changes queue up as a diff. See which devices are affected, then apply — or do not."; "04 Roles people understand — Four roles, each described in a line. Invite a colleague without reading a permissions matrix."; "05 A complete audit trail — Who changed what, when, and what the value was before. Shown in your own time zone."; "06 Tenant isolation — One tenant never sees another's devices, members, or history. It is not a filter — it is the boundary." | Story §Scope bullet 4 + "Note on the copy"; exact copy verified verbatim against the design source (the five claims in "Note on the copy" match this copy word-for-sense exactly) | scope-and-story-acceptance + presentation-and-interaction | DEFINED | UI/Content | P2 | Medium |
| TR-008 | Selecting a node in the hierarchy explorer updates the detail panel (label, status badge, device count, device type, config source, note) without a page reload and without any call to a FleetIQ API; on first render, before any visitor interaction, "Floor 1" is pre-selected. Each tree row also displays its own right-aligned text independent of the detail panel — for Building A and Building B this is a **subgroup count** ("2 subgroups" / "0 subgroups"), not a device count, even though the detail panel's "Devices" field for those same nodes shows 79 and 0 respectively. The selected node's own tree row is also visually distinguished from the other rows (a background highlight and a left-edge accent), independent of and in addition to the detail panel updating. | unbracketed-5; default-selection behaviour, the tree-row/detail-panel field distinction, and the row's own selected-state styling (`rowStyle`, driven by `node.isSelected`/`aria-pressed`) all confirmed verbatim in the design source (`state = { selected: 'a1' }`; the `meta` field is separate from `devices` — see data-model.md) | scope-and-story-acceptance + presentation-and-interaction | DEFINED | Functional | P1 | Medium |
| TR-009 | The closing section renders the heading "Set up your organisation in three steps." and the body "Sign up, verify your email, name your organisation. You will be adding device types the same afternoon.", and repeats both calls to action | Story §Scope bullet 6; exact copy verified verbatim against the design source | scope-and-story-acceptance + presentation-and-interaction | DEFINED | UI/Content | P2 | Medium |
| TR-010 | The footer displays the same square "F" icon + "FleetIQ" wordmark as the header, but as **plain, non-interactive text** (not a link — unlike the header's mark, see TR-003), followed by an "©ACL Digital" attribution line, and a separate "Back to top" link that **scrolls the page to the top when clicked** (`href="#top"`, same destination as the header's product mark, but a distinct element) | Story §Scope bullet 7; icon, the header/footer asymmetry (link vs. plain text), and the "Back to top" click behaviour all verified verbatim in the design source | scope-and-story-acceptance + presentation-and-interaction | DEFINED | UI | P3 | Low |
| TR-011 | At a 360px viewport, the page requires no horizontal scrolling and no content is truncated or overlapping | [TIA-AC-74] | detailed-requirements | DEFINED | UI/Accessibility | P1 | High |
| TR-012 | With a keyboard and no pointing device, every link, the section anchors, and the hierarchy explorer are reachable and operable, with a visible focus indicator throughout and no keyboard trap | [TIA-AC-77] | detailed-requirements | DEFINED | Accessibility | P1 | High |
| TR-013 | Contrast measures at least 4.5:1 for normal text and at least 3:1 for large text and control boundaries, across the page | [TIA-AC-80] | detailed-requirements | DEFINED | Accessibility | P1 | High |
| TR-014 | The page is usable at 200% browser zoom with no content or function lost | [TIA-AC-81] (epic-wide, see §11 finding — not individually cited in FLTIQ-62's own AC field) | detailed-requirements | DEFINED | Accessibility | P2 | Medium |
| TR-015 | Every design token, component, and layout rule on the page comes from the shared design system (FLTIQ-60) rather than page-specific styling | unbracketed-6, cites [FLTIQ-60]; corroborated structurally — the design source is built entirely on `var(--keel-*)` tokens and `KeelACLDigitalDesignSystem_3fda8b.*` component imports, with no inline colour/spacing literals | scope-and-story-acceptance + presentation-and-interaction | DEFINED | UI | P2 | Medium |
| TR-016 | No copy on the page claims a capability the product does not yet support in MVP1 | unbracketed-7 | scope-and-story-acceptance | DEFINED | Content/Compliance | P3 | Medium |
| TR-017 | The page makes no calls to analytics or tracking services, and contains no pricing, documentation, blog, contact-form, or demo-request content | Story §Scope, Out of scope | scope-and-story-acceptance | DEFINED (negative assertion) | Functional/Security-Privacy | P2 | Medium |
| TR-018 | The hero displays the line "Free while you set up your first fleet. No card required." beneath the calls to action | Claude Design source (`FleetIQ Landing.dc.html`) | presentation-and-interaction — **contested by scope-and-story-acceptance**, see CF-002 | **Expected result: UNDEFINED, see §13a Q1** | Content/Compliance | P2 | Medium |
| TR-019 | The hierarchy section (§4.3 of the page) renders the heading "Group once. Configure the group." and the body "Devices inherit configuration from the group they sit in, so a change to a floor reaches forty units without touching one of them individually. Unassigned devices stay visible until someone places them." | Story §Scope bullet 5 (interactive hierarchy explorer); exact copy verified verbatim against the design source — found during a requester screenshot cross-check, not captured on the first pass | scope-and-story-acceptance + presentation-and-interaction | DEFINED | UI/Content | P2 | Medium |

**Type**: Functional | UI | API | Data | Performance | Security | Accessibility | Compatibility
**Priority**: P1 (critical path) | P2 (important) | P3 (nice to have)
**Risk**: High | Medium | Low — drives test depth in the plan phase.
**Authority**: the token of the source that governs this requirement (constitution I).
**Class**: DEFINED | OBSERVED | INFERRED | UNDEFINED (constitution II).

TR-018 carries no expected result pending resolution of an unresolved source
conflict (CF-002). Every other requirement is fully DEFINED. See §12 and §13a.

## 3a. Acceptance Criteria Index

**Count per source, and how derived**: 7 acceptance criteria from the Story's
own AC field (`customfield_10133`, resolved by display name per 1D) — 6
unbracketed plus the one bracketed `[FLTIQ-60]` dependency citation — read
via `getJiraIssue(fields=["*all"])` on FLTIQ-62 itself; 4 from PRD 1 (3
bracketed `[TIA-AC-NN]` ids read directly from FLTIQ-62's own AC field content
plus `[TIA-AC-81]`, not present on FLTIQ-62 but added as TR-014 on FLTIQ-53's
epic-wide scope statement — see the uncovered-but-applicable note below).
11 total; 10 appear in the table (the 11th, `[TIA-AC-81]`, is the
uncovered-but-applicable addition noted separately since it wasn't found *on*
this ticket).

| AC id | Origin | Statement (summary) | Source ref | TR(s) | Status |
|-------|--------|---------------------|-----------|-------|--------|
| *(unbracketed)* | backlog | Unauthenticated visitor, root URL → landing page served, no sign-in required | Story AC field | TR-001 | covered |
| *(unbracketed)* | backlog | Click Create account (header/hero/closing) → sign-up screen | Story AC field | TR-004 | covered |
| *(unbracketed)* | backlog | Click Sign in → sign-in screen | Story AC field | TR-005 | covered |
| *(unbracketed)* | backlog | Already-authenticated visitor, root URL → home page, not landing page | Story AC field | TR-002 | covered |
| *(unbracketed)* | backlog | Hierarchy explorer node selection → detail panel updates, no reload, no API call | Story AC field | TR-008 | covered |
| [TIA-AC-74] | prd | 360px viewport → no horizontal scroll, no truncation/overlap | PRD 1 §8; verbatim in FLTIQ-52 | TR-011 | covered |
| [TIA-AC-77] | prd | Keyboard only → every control (incl. hierarchy explorer) reachable/operable, visible focus, no trap | PRD 1 §8; verbatim in FLTIQ-53 | TR-012 | covered |
| [TIA-AC-80] | prd | Contrast ≥4.5:1 normal, ≥3:1 large/control boundaries | PRD 1 §8; verbatim in FLTIQ-53 | TR-013 | covered |
| [FLTIQ-60] | backlog *(dependency citation, not a [TIA-AC-NN] PRD marker — see provenance note below)* | Every token/component/rule from the shared design system | Story AC field | TR-015 | covered |
| *(unbracketed)* | backlog | No claim made that the product does not yet support in MVP1 | Story AC field | TR-016 | covered |

**Provenance note**: per FLTIQ-29's stated convention, a bracketed id of the
form `[TIA-AC-NN]` marks PRD origin. The one AC bracketed `[FLTIQ-60]` does not
match that pattern — it is a backlog-added AC that cites its governing
dependency ticket, not a PRD marker. Classified `origin: backlog` accordingly.

**Uncovered-but-applicable criterion**: `[TIA-AC-81]` (200% zoom) is not
present in FLTIQ-62's own AC field, but is scoped epic-wide by FLTIQ-53
("each screen is opened"). Added as TR-014 on that basis — see §11.

**Design-sourced content not in any AC field**: the design source
(`FleetIQ Landing.dc.html`) is itself a resolved requirement source
(authority 5, `presentation-and-interaction`) independent of the AC field —
constitution I does not require every material statement to originate from an
acceptance criterion. It settled the exact copy for TR-006/007/009/010, the
default-selection behaviour for TR-008, and surfaced one line with no
counterpart in any Jira/PRD source (TR-018, see CF-002).

## 4. Test Scenarios

### Scenario 1 - Unauthenticated visitor discovers FleetIQ and reaches sign-up (Priority: P1)

A prospective customer opens the FleetIQ root URL, reads the pitch, and
converts to sign-up without needing to understand the platform first.

**Why this priority**: This is the entry point to the entire self-service
onboarding path the epic depends on; the Epic states this layer "blocks every
other MVP1 stream."

**Covers**: TR-001, TR-003, TR-004, TR-009, TR-010

**Independent Test**: Load the root URL with no session cookie/token present;
verify the page renders and every "Create account" control routes to the
sign-up screen.

**Acceptance Scenarios**:

1. **Given** no active session, **When** the visitor opens the FleetIQ root URL, **Then** the landing page renders without any sign-in prompt
2. **Given** the landing page, **When** the visitor clicks "Create account" in the header, **Then** they arrive at the sign-up screen
3. **Given** the landing page, **When** the visitor clicks "Create account" in the hero, **Then** they arrive at the sign-up screen
4. **Given** the landing page, **When** the visitor clicks "Create account" in the closing section, **Then** they arrive at the sign-up screen
5. **Given** the visitor has scrolled down the page (e.g. to the Hierarchy section), **When** they click the "FleetIQ" product mark in the header, **Then** the page scrolls back to the top
6. **Given** the visitor has scrolled down to the footer, **When** they click "Back to top," **Then** the page scrolls back to the top — the same destination (`href="#top"`) as the header's product mark (Scenario 1, item 5), verified independently since it is a separate element

**Negative / Alternate Flows**:

1. **Given** the landing page, **When** the visitor clicks "Create account" anywhere on the page, **Then** no intercepting modal is shown (the design's own modal is explicitly non-production behaviour, per its own copy: "This prototype covers the landing page only")
2. **Given** the landing page, **When** the visitor clicks the "FleetIQ" product mark in the **footer**, **Then** nothing navigates — the footer's mark is plain text, not a link, unlike the header's (TR-010)

---

### Scenario 2 - Existing user returns and is routed past the landing page (Priority: P1)

An already-authenticated visitor should never see marketing content meant for
prospects; they belong in their own workspace.

**Why this priority**: Explicit acceptance criterion; a regression here would
put every returning user through an irrelevant page on every visit to the root.

**Covers**: TR-002, TR-005

**Independent Test**: Load the root URL with a valid authenticated session;
verify the redirect target, not the landing page, renders.

**Acceptance Scenarios**:

1. **Given** an authenticated session, **When** the visitor opens the FleetIQ root URL, **Then** they are taken to their home page and the landing page is not rendered
2. **Given** no active session, **When** the visitor clicks "Sign in" in the header, **Then** they arrive at the sign-in screen
3. **Given** no active session, **When** the visitor clicks "Sign in" in the hero, **Then** they arrive at the sign-in screen
4. **Given** no active session, **When** the visitor clicks "Sign in" in the closing section, **Then** they arrive at the sign-in screen

**Negative / Alternate Flows**:

1. **Given** an authenticated session that expires while the landing page happens to be open in another tab, **When** the root URL is reloaded, **Then** the visitor is redirected to sign-in rather than shown stale home content *(test-mechanics note: exact expiry-detection behaviour is owned by the session-lifecycle story, S-02; this scenario only re-confirms the landing-page redirect gate itself)*

---

### Scenario 3 - Visitor explores the hierarchy explorer without triggering a backend call (Priority: P1)

The interactive hierarchy preview is a static demonstration, not a live data
view, and must not create an unintended dependency on a backend that does not
yet have an agreed API contract (FLTIQ-59 is still open).

**Why this priority**: An explicit, testable architectural constraint; a
violation here is an unplanned coupling to an unstable/nonexistent API.

**Covers**: TR-008

**Independent Test**: Intercept/monitor all network requests while interacting
with the hierarchy explorer; assert none target a FleetIQ API host.

**Acceptance Scenarios**:

1. **Given** the hierarchy explorer on first render, **When** no node has been selected by the visitor, **Then** "Floor 1" is shown pre-selected in the detail panel
2. **Given** the hierarchy explorer, **When** the visitor selects a different node, **Then** the detail panel updates to that node's information (including its exact `note` text — see data-model.md) without a full page reload
3. **Given** the hierarchy explorer, **When** the visitor selects a series of different nodes, **Then** no request to a FleetIQ API endpoint is observed at any point
4. **Given** the tree view, **When** Building A's and Building B's rows are inspected, **Then** each shows a subgroup count ("2 subgroups" / "0 subgroups") in the tree row, not a device count — distinct from what the detail panel shows once that node is selected (79 / 0 devices respectively)
5. **Given** the hierarchy explorer, **When** a node is selected (whether the default "Floor 1" or after a click), **Then** that node's own tree row is visually distinguished from the other rows (a background highlight and a left-edge accent), independently of and in addition to the detail panel updating — found via the §15a UI Element Enumeration retrofit (2026-09-19), not on the original pass

**Negative / Alternate Flows**:

1. **Given** the hierarchy explorer, **When** a node with zero devices is selected (e.g. the design's "Building B" example), **Then** the detail panel still updates without error *(boundary condition, not a distinct source requirement)*

---

### Scenario 4 - The landing page meets the epic's accessibility and responsive baseline (Priority: P1)

Every screen in the Tenant, Identity & Access epic — and this is called out as
its most visible page — must meet the same responsive and WCAG 2.1 AA bar.

**Why this priority**: Contractually significant per the PRD's own background
(FLTIQ-53), and this page is explicitly the one "most visible" screen the
design-system dependency (FLTIQ-60) singles out.

**Covers**: TR-011, TR-012, TR-013, TR-014

**Independent Test**: Run the page through a 360px viewport pass, a
keyboard-only navigation pass, an automated contrast check, and a 200%-zoom
pass, independently of any other scenario.

**Acceptance Scenarios**:

1. **Given** a 360px viewport, **When** the landing page is opened, **Then** no horizontal scrolling is required and no content is truncated or overlapping
2. **Given** a keyboard and no pointing device, **When** the page is navigated, **Then** every link, the section anchors, and the hierarchy explorer are reachable and operable with a visible focus indicator
3. **Given** the page, **When** contrast is measured, **Then** normal text meets 4.5:1 and large text/control boundaries meet 3:1
4. **Given** the browser at 200% zoom, **When** the page is opened, **Then** no content or function is lost

**Negative / Alternate Flows**:

1. **Given** a keyboard-only pass over the hierarchy explorer specifically, **When** a node is focused, **Then** it is selectable via keyboard (Enter/Space) with the same visible focus indicator as the rest of the page — no separate exemption for the explorer's custom tree control (the design implements each node as a native `<button>`, which is a favourable implementation signal, not itself a requirement)

---

### Scenario 5 - Page content and structure match the approved scope (Priority: P2)

**Why this priority**: Structural/content correctness supports the page's
purpose but a defect here is recoverable copy work, not a blocked user journey.

**Covers**: TR-003, TR-006, TR-007, TR-010, TR-015, TR-016, TR-017, TR-019

**Independent Test**: Static review of rendered DOM content and structure
against the approved scope list, independent of any interaction flow.

**Acceptance Scenarios**:

1. **Given** the landing page, **When** the header is inspected, **Then** the "Sign in" control appears before "Create account" (TR-003)
2. **Given** the landing page, **When** the hero section is inspected, **Then** the badge, headline, subhead and three supporting statistics render with the exact copy in TR-006, and "Create account" appears before "Sign in"
3. **Given** the landing page, **When** the capability section is inspected, **Then** the section heading and all six capability cards render with the exact copy in TR-007
4. **Given** the landing page, **When** the hierarchy section is inspected, **Then** its heading and intro paragraph render with the exact copy in TR-019
5. **Given** the landing page, **When** the closing section is inspected, **Then** "Create account" appears before "Sign in" (TR-009), the same order as the hero and opposite the header
6. **Given** the landing page, **When** the footer is inspected, **Then** the FleetIQ mark, "©ACL Digital," and "Back to top" are present
7. **Given** the page, **When** it is rendered, **Then** every visual element resolves to a shared design-system token or component (no page-specific styling)
8. **Given** the page's copy, **When** compared against the MVP1-supported capability list (three levels of grouping, four roles, diff-based review, viewer-timezone audit, tenant isolation as a boundary), **Then** no claim exceeds what MVP1 supports

**Negative / Alternate Flows**:

1. **Given** the rendered page, **When** its outbound network activity is inspected, **Then** no analytics or tracking request is present
2. **Given** the rendered page, **When** its content is inspected, **Then** no pricing, documentation, blog, contact-form, or demo-request element is present *(pending TR-018/CF-002 resolution — the hero's "Free ... No card required" line is inspected under this scenario and reported against whatever CF-002's resolution decides)*

## 5. Edge Cases & Boundary Conditions

| ID | Condition | Expected Handling |
|----|-----------|-------------------|
| EC-001 | Visitor's authentication state is still resolving at first paint | No source specifies fallback UI; flagged as elective §13b Q2. Do not assert a specific "flash of content" behaviour without a source. |
| EC-002 | Hierarchy explorer opened with no node yet selected | **Resolved via the design source**: "Floor 1" (`a1`) renders pre-selected — see TR-008 and Scenario 3 |
| EC-003 | Hierarchy explorer's client-side script fails to load | Fallback behaviour unspecified by any source — elective §13b Q3; test mechanics only (no unhandled console error), no expected-result assertion |
| EC-004 | Visitor opens a deep link to a section anchor (e.g. `#capabilities`), **or clicks the header's own "Capabilities"/"Hierarchy" nav link** (mechanically the same `<a href="#...">` behaviour, confirmed in the design source) | INFERRED test mechanics: anchor scroll-to-section is standard anchor-link behaviour in both cases, not a distinct product requirement |
| EC-005 | 360px viewport combined with 200% zoom simultaneously | INFERRED test mechanics: a boundary combination of TR-011 and TR-014, not a new expected result |
| EC-006 | A node with zero devices is selected in the hierarchy explorer (design's "Building B" example: 0 subgroups, 0 devices) | Detail panel still renders correctly with zero-value fields — see Scenario 3 negative flow |

## 6. Test Data Requirements

| Data Set | Description | Source | Sensitivity |
|----------|-------------|--------|-------------|
| hierarchy-explorer-fixture | Static local node tree: Building A (79 devices, 2 subgroups), Floor 1 (41 devices, default-selected), Floor 2 (38 devices, 3 pending), Building B (0 devices), Unassigned (501 devices) — exact fixture confirmed in the design source | Fixture, shipped with the build | None |
| authenticated-test-account | One pre-provisioned account with a valid session, for Scenario 2 | `.env` (`TEST_USERNAME` / `TEST_PASSWORD`), per repo convention | None — test account, least-privileged |

**Note**: No real customer data, credentials, or tokens are placed in this file.

## 7. Environment & Platform Matrix

| Dimension | Values |
|-----------|--------|
| Environments | QA / Staging (per `BASE_URL` in `.env`) |
| Browsers | Chromium, Firefox, WebKit (repo's Playwright default triad). No PRD-specified minimum browser matrix was found for this ticket; the "clear message on an unsupported browser" requirement belongs to FLTIQ-52, not this story |
| Viewports | 360px width (mandatory, TR-011); a representative desktop width (INFERRED test mechanics — no explicit desktop breakpoint value found in any source) |
| Prerequisites | Design-system component library (FLTIQ-60) integrated into the build (Done); one authenticated test account for Scenario 2; FLTIQ-33/FLTIQ-35 deployed for full-journey verification of TR-004/TR-005 (see §10 Entry Criteria for the fallback if not yet deployed) |

## 8. Non-Functional Requirements

- **NFR-001**: WCAG 2.1 AA — contrast (TR-013), full keyboard operability (TR-012), 360px responsive layout (TR-011), 200% zoom (TR-014). Source: PRD 1 §8 / FLTIQ-53.
- **NFR-002**: No FleetIQ API call originates from the hierarchy explorer interaction. Source: FLTIQ-62 AC field (TR-008).
- No performance/latency target (e.g. page-load time) was stated by any approved source for this ticket. Not invented — if one is needed, it is an open question for the requester, not an assumption.

## 9. Risk Analysis

| ID | Risk | Likelihood | Impact | Mitigation / Test Focus |
|----|------|------------|--------|-------------------------|
| RA-001 | Broken or misdirected CTAs prevent prospective customers from self-serve sign-up, undermining the MVP1 pilot's core self-service premise | Low | High | Full positive + negative coverage on TR-004/TR-005; automate first |
| RA-002 | Accessibility regressions on "the most visible page in the product" — WCAG 2.1 AA is often contractually required for enterprise/public-sector procurement | Medium | High | TR-011 through TR-014, automated checks per FLTIQ-53's pipeline gate |
| RA-003 | Marketing copy overstates MVP1 capability, creating trust or support exposure | Low-Medium | Medium | TR-016, content-review checklist (see §11) |
| RA-004 | Authentication-redirect defect shows marketing content to an already-onboarded user instead of their workspace | Low | Medium | TR-002 |
| RA-005 | Hierarchy explorer is inadvertently wired to a real API in a later iteration, before the API contract (FLTIQ-59) is agreed | Low | Medium | TR-008, automated network-call assertion |
| RA-006 | "Free while you set up your first fleet. No card required." ships unreviewed, either contradicting the story's own no-pricing-content exclusion or committing to a commercial policy (free tier, no payment collection) nobody outside this design has agreed | Medium | Medium-High | Resolve CF-002/TR-018 with the requester before this build reaches production; do not let a design-only line become de facto commercial policy |

## 10. Entry & Exit Criteria

**Entry criteria** (before test execution starts):

- [ ] This requirement analysis (`spec.md`) is Approved
- [ ] Design-system component library (FLTIQ-60) is available in the build under test — already Done
- [ ] Build deployed to the QA/Staging environment; root URL reachable and smoke-passable
- [ ] One authenticated test account provisioned (Scenario 2)
- [ ] FLTIQ-33 and FLTIQ-35 deployed to the test environment for full-journey verification of TR-004/TR-005; **if not yet deployed**, those two are verified at the routing/target-URL level only, per the story's own note that they "need not exist before this page is built" — not treated as a P1 blocker for this story
- [ ] CF-002 / TR-018 resolved with the requester (see §13a Q1) before the automation suite asserts a concrete outcome for the "Free ... No card required" line

**Exit criteria** (before sign-off):

- [ ] 100% of P1 test cases executed (TR-001, TR-002, TR-004, TR-005, TR-008, TR-011, TR-012, TR-013)
- [ ] Zero open Critical/High defects
- [ ] Automated accessibility checks integrated per FLTIQ-53's pipeline gate (cross-referenced, owned by that story — not re-implemented here)
- [ ] TR-018 no longer carries `Expected result: UNDEFINED`

## 11. Testability Review

| Source AC | Issue | Proposed Resolution |
|-----------|-------|---------------------|
| "No claim is made that the product does not yet support in MVP1" | Open-ended claim-checking is not independently machine-verifiable | Maintain a short "MVP1-supported capabilities" checklist derived from the story's own "Note on the copy" (three levels of grouping, four roles, diff-based review, viewer-timezone audit, tenant isolation as a boundary) — confirmed to match the design's card copy word-for-sense — and test literal copy against that checklist |
| `[FLTIQ-60]` "every token/component/rule from the shared design system" | Not verifiable via a single functional/behavioural assertion | Cover via a component-usage audit or visual-regression baseline against Keel components in the plan phase, alongside/instead of a Playwright assertion. The design source's own structure (100% `var(--keel-*)` tokens, zero literal colour/spacing values) gives the plan phase a concrete baseline to diff against. |
| `[TIA-AC-81]` (200% zoom) | Applies epic-wide per FLTIQ-53 ("each screen is opened") but is not individually cited in FLTIQ-62's own AC field | **Confirmed by the requester (2026-09-18): keep as a requirement.** TR-014 stays DEFINED via FLTIQ-53's epic-wide scope statement. Still recommend the AC field on FLTIQ-62 itself be updated to cite `[TIA-AC-81]` explicitly, so future readers don't have to reconstruct this cross-reference. |
| `[TIA-AC-78]` (dialog focus) and `[TIA-AC-79]` (form-error announcement), both epic-wide per FLTIQ-53 | Neither applies: this page's approved scope has no dialogs (the design's own intercept-modal is explicitly non-production) and no forms | Marked **Not Applicable** for this story so a future reviewer does not mistake the omission for a coverage gap |
| Hero statistic "500+ devices onboarded in a single import" | This is a capability claim about bulk device import — a Device Registrar epic concern, not Tenant/Identity. No source in this ticket's resolved set (Story, Epic, PRD 1, sibling stories) corroborates or contradicts it. | Recorded in `missing_sources` (Device Registrar PRD, not fetched — out of this ticket's epic). Not blocking: the claim is structurally present and testable (TR-006 covers its presence), but its factual accuracy should be confirmed with whoever owns the Device Registrar epic before launch — elective §13b Q1. |
| The original Jira AC enumerates "header, hero, or closing section" for "Create account" but not for "Sign in" ("Given the landing page, when the visitor clicks Sign in..." — no locations named) | Found via a detailed design cross-check (2026-09-18): the design confirms "Sign in" physically appears in all three locations too, paired with "Create account" in every case, so the same regression risk (RA-001) applies equally to both controls. Testing only a generic, unlocated "Sign in" click would have left two of its three instances unverified. | **Resolved, not left open**: TR-005 and Scenario 2 updated to explicitly test all three "Sign in" locations, matching TR-004/Scenario 1's existing treatment of "Create account." Not raised as a question to the requester — the design source itself settles the location count; this is a testability gap in the *test basis's own thoroughness*, not a product-intent ambiguity. |
| CTA button order per section, and the header/footer product-mark asymmetry (header's mark is a link back to `#top`; the footer's is plain text) | Neither the Story's AC field nor its Scope bullets mention button order or that the header mark is interactive — both are only visible in the design source's markup, not in any prose description | **Resolved, not left open**: added to TR-003 (header order + click-to-top), TR-006 (hero order), TR-009 (closing order), and TR-010 (footer's mark is explicitly non-interactive, for contrast) — each verified verbatim against the design. New acceptance scenarios added to Scenario 1 (click-to-top; footer mark does *not* navigate) and Scenario 5 (order assertions per section). |
| Hierarchy tree row's `meta` text vs. the detail panel's `devices` field | Easy to conflate as the same value — for Floor 1/Floor 2/Unassigned they happen to read alike ("41 devices"), but for Building A/Building B the tree row shows a **subgroup count** ("2 subgroups" / "0 subgroups"), not the device count (79 / 0) the detail panel shows for the same node. Neither the Story's AC field nor its Scope bullets distinguish these; only the design source's underlying `meta` vs. `devices` fields do. | **Resolved, not left open**: added to TR-008 and a dedicated acceptance scenario in Scenario 3; full per-node values (including the exact `note` text for all five nodes, also previously only described structurally rather than quoted) captured verbatim in `data-model.md`. |
| Full re-read of the design source's remaining script-level artifacts (2026-09-18 diligence pass, prompted by a request to re-verify nothing was missed) | The design file exposes a `theme` prop (light/dark, default light), a `showStats` prop (boolean, default true), and a third, unused modal variant (`flow`, tied to an `openFlow` handler) | **Checked and confirmed not requirements, not silently skipped**: (1) `theme` — no Jira/Epic/PRD source anywhere mentions dark mode; this is Claude Design/Keel authoring scaffolding for previewing a page in either theme, not a FleetIQ product capability. (2) `showStats` — the Story's own scope text states the hero unconditionally includes "the three supporting statistics," with no conditional language, resolving this as scaffolding rather than a real feature flag; TR-006 correctly treats the stats as always-present. (3) The `flow` modal / `openFlow` handler is defined in the script but **not referenced by any element anywhere in the rendered markup** — confirmed dead prototype code, not a feature this page exposes. None of the three is elevated to a TR. |
| Footer's "Back to top" link — functionality, not just presence | TR-010 only stated it "is a link," and Scenario 5 only checked it was structurally present. Its actual click behaviour (scroll to top) was never asserted anywhere, mirroring the same gap already found and fixed for the header's product mark (TR-003). | **Resolved, not left open**: TR-010 now states the click-to-top behaviour explicitly, and Scenario 1 gained a dedicated acceptance scenario (item 6) verifying it independently of the header's mark, since they are two distinct elements sharing the same `href="#top"` destination. |
| Hierarchy explorer load-failure fallback | Unspecified by any source, including the design (no error boundary or fallback UI is defined in the design's script) | Elective §13b Q3 — asked to the team 2026-09-18, awaiting response |
| Hierarchy tree row's own selected-state visual styling (2026-09-19, found during the §15a UI Element Enumeration retrofit — Pass 5, Visibility & conditionals) | TR-008 and Scenario 3 asserted the detail panel's update on selection, but never the tree row's own highlight (`rowStyle`, driven by `node.isSelected`/`aria-pressed`) — a directly observable consequence of the same selection state, not a new product decision | **Resolved, not left open**: TR-008 and Scenario 3 (new acceptance scenario item 5) updated to assert the selected row's own visual distinction, verified verbatim against the design source's per-row style logic |
| Visitor auth-state resolution flash (EC-001) | Unspecified by any source | Elective §13b Q2 — asked to the team 2026-09-18, awaiting response |
| Hierarchy explorer example data — permanent content vs. illustrative placeholder | Confirmed static/no-API (TR-008), but no source says whether the exact figures (79/41/38/0/501 devices, "XYZ — organisation") must ship as-is or may be swapped for different static example values | Elective §13b Q4 — asked to the team 2026-09-18, awaiting response |

### 11a. Source Conflicts

| ID | Source A (authority) | Source B (authority) | Contested statement | Domain | Outcome | Status |
|----|----------------------|----------------------|---------------------|--------|---------|--------|
| CF-001 | FLTIQ-62 description: "Covers: no PRD requirement — this page was missing from the PRD" (scope-and-story-acceptance) | FLTIQ-62's own AC field carries three PRD-bracketed ids, `[TIA-AC-74]`, `[TIA-AC-77]`, `[TIA-AC-80]` (detailed-requirements) | Whether this page has any PRD-sourced requirement at all | Source classification (page-specific vs. cross-cutting requirement) | Not a genuine conflict — PRD 1 and its epic-wide children (FLTIQ-52, FLTIQ-53) state these three criteria apply to "each screen/flow in this document/epic," a scope that includes the landing page even without a dedicated PRD section for it | resolved-in-source |
| CF-002 | FLTIQ-62 description, Scope: "Out of scope: Pricing, documentation, blog, contact form, demo request, and analytics — none is in MVP1" (scope-and-story-acceptance) | Design source hero: "Free while you set up your first fleet. No card required." (presentation-and-interaction) | Whether pricing/commercial-terms microcopy ships on this page | Scope | Unresolved. Per the constitution's domain-based precedence policy, scope-and-story-acceptance — not presentation-and-interaction — governs "scope of this cycle." Whether this line counts as the "pricing" the story excludes, or is incidental copy the exclusion never meant to reach, is a business-intent question neither source settles. **Raised to the requester, not decided here** (§13a Q1). | unresolved |

## 12. Evidence Classification

### DEFINED

- TR-001 through TR-017 — each cites its Story AC field, PRD-verified bracketed id, and/or the design source, per §3. TR-006, TR-007, TR-008, TR-009, TR-010 and TR-015 are corroborated with exact, verbatim copy/behaviour from the retrieved Claude Design source.

### OBSERVED

- None. The landing page does not yet exist ("The FleetIQ root URL currently has no page behind it" — FLTIQ-62 background). Per constitution II hard-stop 3, a system not yet built yields no legitimate OBSERVED for expected results. (The *design* is a first-class DEFINED source per authority 5 — this is not observation of a running system, it is reading an approved artifact.)

### INFERRED

- Choice of a representative desktop viewport width for testing (no explicit desktop breakpoint value is stated by any source)
- The network-call-monitoring technique used to verify TR-008 ("no FleetIQ API call")
- EC-004 (anchor-link scroll behaviour), EC-005 (combined 360px + 200%-zoom boundary), and EC-006 (zero-device node) — test mechanics only, no new expected result

### UNDEFINED

- TR-018 ("Free while you set up your first fleet. No card required.") — existence disputed by CF-002. Two approved sources speak to this line's domain (scope exclusion vs. design content) without either settling whether it should ship. No expected result is written; see §13a Q1.

### Test-execution assumptions

- The QA/Staging build under test already integrates the FLTIQ-60 design-system component library
- An authenticated test account is available via `.env` (`TEST_USERNAME`/`TEST_PASSWORD`), never hard-coded
- FLTIQ-33/FLTIQ-35 may or may not be deployed in the test environment when this suite runs; where absent, TR-004/TR-005 are verified at the routing/target level only (see §10)

## 13. Open Questions

### 13a. Blocking

- **Q1** [NEEDS CLARIFICATION: Should the hero's "Free while you set up your first fleet. No card required." line ship as designed, be removed as excluded pricing content, or be revised? The story's own scope explicitly excludes pricing/commercial-terms content from MVP1 (out-of-scope bullet), but the approved design includes this line with no corresponding product decision on file.] — *Blocks*: TR-018 (P2); also affects the completeness of Scenario 5's negative flow and TR-017's "no pricing content" assertion, which cannot be marked fully verified while this line's status is undecided. **Status: asked to the team 2026-09-18, awaiting response.** Does not block progression to `/speckit-plan` per constitution §XI.b — the quality gate requires no open blocking clarification on a *P1* requirement, and this blocks TR-018, which is P2.

### 13b. Elective

- **Q1** [NEEDS CLARIFICATION: Is "500+ devices onboarded in a single import" (hero statistic) an accurate, agreed capability claim? It concerns bulk device import, which belongs to the Device Registrar epic — outside this ticket's own resolved source set.] Non-blocking: the statistic's presence is testable regardless (TR-006); only its factual accuracy is in question.
- **Q2** [NEEDS CLARIFICATION: What should the page show, if anything, while the visitor's authentication state is still resolving at first paint?] **Status: asked to the team 2026-09-18, awaiting response.**
- **Q3** [NEEDS CLARIFICATION: If the hierarchy explorer's client-side script fails to load, should the rest of the page still function, and what (if anything) should appear in its place? The design itself defines no fallback. Note: the header/hero/closing-section CTAs are built from the same shared design-system JS bundle as the explorer — a failure there could plausibly affect the CTAs too, not just the explorer.] **Status: asked to the team 2026-09-18, awaiting response.**
- **Q4** [NEEDS CLARIFICATION: The hierarchy explorer's example data (Building A/Floor 1/Floor 2/Building B/Unassigned with their device counts, and the "XYZ — organisation" label) is confirmed static with no API call. Is this exact data meant to ship as permanent content, or is it illustrative placeholder that the real implementation can replace with different static example values?] **Status: asked to the team 2026-09-18, awaiting response.**

**All 4 questions above (§13a Q1, §13b Q2–Q4) were sent to the team on
2026-09-18; answers are pending.** Per constitution §XI.b, this does not
block moving to `/speckit-plan` — the only blocking item (§13a Q1) affects a
P2 requirement (TR-018), not a P1, and every P1 requirement in this spec is
fully DEFINED with no open blocking clarification.

## 14. Traceability Seed

| Jira AC | Requirement | Scenario(s) | Test Cases | Automation |
|---------|-------------|-------------|------------|------------|
| unbracketed-1 | TR-001 | Scenario 1 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| unbracketed-4 | TR-002 | Scenario 2 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| Story §Scope + design source | TR-003 | Scenario 1, Scenario 5 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| unbracketed-2 | TR-004 | Scenario 1 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| unbracketed-3 | TR-005 | Scenario 2 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| Story §Scope + design source | TR-006 | Scenario 5 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| Story §Scope + design source | TR-007 | Scenario 5 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| unbracketed-5 + design source | TR-008 | Scenario 3 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| Story §Scope + design source | TR-009 | Scenario 1 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| Story §Scope + design source | TR-010 | Scenario 1, Scenario 5 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| Story §Scope + design source | TR-019 | Scenario 5 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| [TIA-AC-74] | TR-011 | Scenario 4 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| [TIA-AC-77] | TR-012 | Scenario 4 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| [TIA-AC-80] | TR-013 | Scenario 4 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| [TIA-AC-81] | TR-014 | Scenario 4 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| [FLTIQ-60] | TR-015 | Scenario 5 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| unbracketed-6/7 | TR-016 | Scenario 5 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| Story §Scope (out of scope) | TR-017 | Scenario 5 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |
| design source only | TR-018 | Scenario 5 (pending §13a Q1) | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |

## 15. Source Inventory

| Type | Id / filename | Version | Found on | Retrieved | Authority | Relationship |
|------|---------------|---------|----------|-----------|-----------|--------------|
| jira-story | FLTIQ-62 | — | FLTIQ-62 (self) | 2026-09-18 | scope-and-story-acceptance | primary |
| jira-epic | FLTIQ-29 | — | FLTIQ-29 (self) | 2026-09-18 | feature-context | parent |
| prd | FleetIQ_PRD_1_Tenant_Identity_and_Access_v1.2.docx | 1.2 | FLTIQ-29 (attachment) | 2026-09-18 | detailed-requirements | parent (metadata only; not parsed) |
| prd | PRD 1 Tenant, Identity & Access (Confluence 14057474) | 1.2, Draft for Review | Confluence space FM | 2026-09-18 | detailed-requirements | prose-dependency (content read in full) |
| jira-issue-context | FLTIQ-53 (Meet WCAG 2.1 AA across the identity layer) | — | Epic child (JQL) | 2026-09-18 | feature-context | prose-dependency |
| jira-issue-context | FLTIQ-52 (Make the identity layer work on a phone) | — | Epic child (JQL) | 2026-09-18 | feature-context | prose-dependency |
| jira-issue | FLTIQ-60 (design system, Done) | — | FLTIQ-62 description (prose) | 2026-09-18 | feature-context | prose-dependency |
| jira-issue | FLTIQ-33 (Sign up) | — | FLTIQ-62 description (prose) | 2026-09-18 | feature-context | prose-dependency |
| jira-issue | FLTIQ-35 (Sign in) | — | FLTIQ-62 description (prose) | 2026-09-18 | feature-context | prose-dependency |
| process-documentation | Design handoff process (Confluence 13533185) | — | FLTIQ-60 (comment) | 2026-09-18 | technical-documentation | prose-dependency |
| presentation-and-interaction | FleetIQ Landing.dc.html (Claude Design project "Keel Design Wireframe Prototype") | — | FLTIQ-62 (Design/Mockup Links field) | 2026-09-18 | presentation-and-interaction | primary — **full content retrieved** via the Claude Design MCP, per this skill's dependency resolution gate (1F.2) |

### 15a. UI Element Enumeration

Retrofit pass, 2026-09-19, run per the updated `/speckit-specify` 1F.3
procedure (added after this spec's original analysis missed eight
design-sourced facts, all caught only by manual re-review — see the
2026-09-18 "Re-confirmed" line above and `plan.md`'s A0 table). This is the
enumeration's receipt: covered rows carry a bare `TR-xxx`; only the one
uncovered row found quotes its content.

**Pass 0 — Screens in scope.** The Claude Design project ("Keel Design
Wireframe Prototype") holds 12 screen files (`.dc.html`) plus non-screen
infrastructure (a shared design-system library under `_ds/`, reference
screenshots for other tickets under `uploads/`, a project `.thumbnail`, and a
shared `support.js`) — the infrastructure is excluded as "not a screen," not
silently omitted.

| File | In scope? | Reason |
|------|-----------|--------|
| `FleetIQ Landing.dc.html` | **Yes** | Named in FLTIQ-62's Design/Mockup Links field; this is the page this story builds |
| `FleetIQ Signup.dc.html` | No | FLTIQ-33 (Sign up) — different ticket |
| `Step 1 - Sign up.dc.html` | No | FLTIQ-33 flow step — different ticket |
| `Step 2 - Verify email.dc.html` | No | FLTIQ-33 flow step — different ticket |
| `Step 3 - Create organisation.dc.html` | No | Onboarding flow step — different ticket |
| `Step 4 - Land on Home.dc.html` | No | Onboarding flow step — different ticket |
| `Home day zero.dc.html` | No | Post-authentication home page — different ticket, out of this page's scope by definition (TR-002 only tests the redirect target, not that page's content) |
| `Sign in - failed attempts.dc.html` | No | FLTIQ-35 (Sign in) — different ticket |
| `Password recovery.dc.html` | No | Different ticket, auth flow |
| `Members and roles.dc.html` | No | Different ticket |
| `Organisation settings.dc.html` | No | Different ticket |
| `Your account.dc.html` | No | Different ticket |
| `uploads/FleetIQ Landing.dc.html` | No (not a screen) | Duplicate upload of the in-scope file, not a distinct screen |
| `_ds/**` (11 files) | No (not a screen) | Shared design-system token/component library the landing page consumes — infrastructure, not a UI screen |
| `uploads/*.png` (13 files) | No (not a screen) | Reference screenshots for other tickets' flows (member/role management, account, org settings) |
| `.thumbnail`, `support.js` | No (not a screen) | Project thumbnail and shared runtime script — not screens |

Six passes over the one in-scope screen (`FleetIQ Landing.dc.html`):

**1. Text elements** — 51 static/chrome text elements found, derived from
every `<h1>/<h2>/<h3>`, paragraph, span-label, badge, caption and
button/link text node in the header, hero, stats, capabilities, hierarchy
and closing sections plus the footer (6 + 6 + 6 + 19 + 6 + 4 + 4 = 51).
Disposition: all 51 map to TR-003, TR-006, TR-007, TR-008, TR-009, TR-010 or
TR-019, except the hierarchy panel's "XYZ — organisation" label, which is not
itself a requirement — it is the subject of the still-open §13b Q4 (whether
the hierarchy example data, including this label, is permanent or
illustrative placeholder). A further 9 text elements (3 modal titles, 3
modal bodies, 3 modal CTA labels) were found and are **excluded**: they
belong to the prototype-only intercept modal already established as
non-production scaffolding (TR-004/TR-005's "Note on the design prototype"
finding).

**2. Interactive elements** — 14 found, derived from every `<a>`, `<button>`
and `x-import ... Button` occurrence in the markup. 12 map to TR-003 (header
mark, click-to-top), TR-004/TR-005 (the six Sign in/Create account
instances), TR-008 (5 tree-row buttons), TR-010 (footer "Back to top"), and
EC-004 (2 nav anchor links). The remaining 2 (the design-system Modal
component's own internal close control and footer CTA button) are
**excluded**: they are generic chrome belonging to the shared Modal
component, not page-specific behaviour, and the modal itself is
non-production scaffolding.

**3. Repeated labels** — 5 distinct labels found with 2+ instances, derived
from a text-content diff across all 51 Pass-1 elements: "Sign in" (3 —
header, hero, closing), "Create account" (3 — header, hero, closing),
"FleetIQ" wordmark (2 — header, footer), "F" icon glyph (2 — header,
footer), and "Continue" (2, both inside the excluded prototype modal). The
first four map to TR-003/TR-004/TR-005/TR-010, each already asserting every
instance and its order — this is the exact class of gap the original
analysis missed (§11's asymmetry finding) and it reconciles cleanly on
retrofit. "Continue" is excluded with the rest of the modal scaffolding.

**4. Data fixtures** — 79 values found, derived from the source's three
inline data structures: `NODES` (5 records × 10 fields = 50), `CAPABILITIES`
(6 records × 3 fields = 18), `MODALS` (3 records × 3 fields = 9), plus 2
top-level props (`theme`, `showStats`). `NODES` and `CAPABILITIES` map to
TR-008/`data-model.md` and TR-007 respectively, with every value already
captured verbatim. `MODALS.signup`/`MODALS.signin` bodies are already quoted
in TR-004/TR-005 as prototype-only copy. `MODALS.flow` (title "The setup
flow", body "Three steps: create an account, verify your email, name your
organisation. Device types come after that.", cta "Close") is **excluded**:
it is reachable only via the `openFlow` handler, which — confirmed again on
this pass — no element in the markup ever calls (dead prototype code, per
the existing Testability Review finding). `theme` and `showStats` are
**excluded** as authoring scaffolding, per the same existing finding.

**5. Visibility & conditionals** — 5 found: `theme` (light/dark toggle),
`showStats` (stats-section visibility), the modal's own open/close state,
`aria-pressed`/`node.isSelected` (tree-row selection state), and the
selected row's own style conditional (`rowStyle`, background + box-shadow
inset when `node.isSelected`). The first three are **excluded**, already
classified as authoring scaffolding (Testability Review). The fourth
(selection state) maps to TR-008. **The fifth is the one new finding this
retrofit surfaced**: the row's own selected-state highlight was never
asserted by any existing TR or scenario, though it follows directly from
TR-008's own selection behaviour and required no new product decision —
**resolved**, not left open: added to TR-008 and Scenario 3 (item 5) above.

**6. Semantic attributes** — found: `aria-label` on 4 landmark sections
("Platform overview", "Capabilities", "Hierarchy example", "Get started"),
`aria-pressed` on the 5 tree-row buttons, `type="button"` on 7 raw
`<button>` elements (5 tree rows + 2 closing-section CTAs), and **zero**
`alt`/`<img>` elements anywhere on the page (confirmed, not silently
assumed — there are no images on this page, only CSS-styled marks). The
landmark `aria-label`s and `aria-pressed` are supporting evidence for
TR-012/TR-013 (bare reference, no new TR needed); `type="button"` is
INFERRED test mechanics (standard, prevents accidental form submission); the
absence of images means no `alt`-text requirement applies to this page.

### Missing Sources

| Ref | Kind | Cited by | Reason | Impact |
|-----|------|----------|--------|--------|
| FleetIQ Decision Log — Platform UI/UX (UX-D1 to UX-D51) | decision-log | PRD 1, Related Documents | Cited by name; no retrievable page found under this or a similar title | Low — no FLTIQ-62 statement cites a UX-D decision directly |
| FleetIQ Decision Log — Pre-Onboarding and Device Registrar (D1 to D27) | decision-log | PRD 1, Related Documents | Cited by name; not retrievable | None identified — out of this story's domain |
| FleetIQ Architecture and MVP1 (PDF) | technical-documentation | PRD 1, Related Documents | Cited by name; not retrievable | None identified — no backend/architecture behaviour in this story |
| FleetIQ MVP Proposal 1 (PDF) | product-context | PRD 1, Related Documents | Cited by name; not retrievable | Low — story's own scope statement is self-sufficient |
| fleetiq-tenant-first-run-two-track-flow (HTML diagram) | technical-documentation | PRD 1, Related Documents | Cited by name; not retrievable | None — the design source's own closing-section copy independently settles the three-step wording (TR-009) |
| FleetIQ Device Registrar PRD (or equivalent) | detailed-requirements | The design source's hero statistic "500+ devices onboarded in a single import" | Out of scope for this ticket's source resolution (a different epic); not fetched | Low-Medium — see §11 and §13b Q1 |

### Dependencies

| Ref | Kind | Discovered in | Status |
|-----|------|---------------|--------|
| FLTIQ-60 | jira-issue | FLTIQ-62 description (prose) | resolved — Done |
| FLTIQ-33 | jira-issue | FLTIQ-62 description (prose) | resolved — need not exist before this page is built (see §10) |
| FLTIQ-35 | jira-issue | FLTIQ-62 description (prose) | resolved — same caveat as FLTIQ-33 |
| FLTIQ-45 | jira-issue | FLTIQ-60 description (prose) | resolved — informational only, not applicable (post-auth navigation shell) |
| FLTIQ-15 | jira-issue | FLTIQ-29 (Epic) description (prose) | resolved — informational only, not applicable (this page makes no API/data calls) |
| FLTIQ-19 | jira-issue | FLTIQ-29 (Epic) description (prose) | resolved — informational only, not applicable |
