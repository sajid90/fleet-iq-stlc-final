# Test Cases: FLTIQ-62 — Build the public landing page

**Generated**: 2026-09-21T20:45:00 | **Total**: 43

> Generated from `test-cases.json`. Do not edit by hand — edit the JSON and re-export.

## TC-001 — Unauthenticated visitor sees the landing page with no sign-in prompt

**Priority**: P1 | **Type**: Functional | **Scenario**: S1 | **Requirements**: TR-001 | **Jira AC**: unbracketed-1

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc001_unauthenticated_visitor_sees_landing_page`)

**Preconditions**:
- No session cookie/token present (fresh browser context)

| # | Action | Expected |
|---|--------|----------|
| 1 | Navigate to the root URL (`BASE_URL`) | The public landing page renders |
| 2 | Inspect the page for any sign-in prompt, redirect, or auth wall | No sign-in prompt or redirect occurs |

**Expected result**: The landing page renders fully with no sign-in requirement of any kind

---

## TC-002 — Header "Create account" navigates to the sign-up screen

**Priority**: P1 | **Type**: Functional | **Scenario**: S1 | **Requirements**: TR-004 | **Jira AC**: unbracketed-2

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc002_header_create_account_navigates_to_signup`)

**Preconditions**:
- No active session
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Click "Create account" in the header | The browser navigates to the sign-up screen (FLTIQ-33) |

**Expected result**: The visitor lands on the real sign-up screen; no intercepting modal appears

---

## TC-003 — Hero "Create account" navigates to the sign-up screen

**Priority**: P1 | **Type**: Functional | **Scenario**: S1 | **Requirements**: TR-004 | **Jira AC**: unbracketed-2

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc003_hero_create_account_navigates_to_signup`)

**Preconditions**:
- No active session
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Click "Create account" in the hero section | The browser navigates to the sign-up screen (FLTIQ-33) |

**Expected result**: The visitor lands on the real sign-up screen; no intercepting modal appears

---

## TC-004 — Closing-section "Create account" navigates to the sign-up screen

**Priority**: P1 | **Type**: Functional | **Scenario**: S1 | **Requirements**: TR-004 | **Jira AC**: unbracketed-2

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc004_closing_create_account_navigates_to_signup`)

**Preconditions**:
- No active session
- Landing page loaded, scrolled to the closing section

| # | Action | Expected |
|---|--------|----------|
| 1 | Click "Create account" in the closing section | The browser navigates to the sign-up screen (FLTIQ-33) |

**Expected result**: The visitor lands on the real sign-up screen; no intercepting modal appears

---

## TC-005 — Header product mark scrolls the page back to the top when clicked

**Priority**: P2 | **Type**: UI | **Scenario**: S1 | **Requirements**: TR-003

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc005_header_product_mark_scrolls_to_top`)

**Preconditions**:
- Landing page loaded
- Visitor has scrolled down (e.g. to the Hierarchy section)

| # | Action | Expected |
|---|--------|----------|
| 1 | Inspect the header product mark's square icon | The square icon contains the letter "F" beside the "FleetIQ" wordmark |
| 2 | Click the "FleetIQ" product mark (icon + wordmark) in the header | The page scrolls back to the top (`#top`) |
| 3 | Scroll down again and click the same product mark a second time | The page scrolls back to the top again — the behaviour is not limited to the first click |

**Expected result**: The mark renders as a square "F" icon beside the wordmark, and the page returns to its topmost scroll position every time the mark is clicked, not only on the first click

---

## TC-006 — Footer "Back to top" link scrolls the page back to the top when clicked

**Priority**: P3 | **Type**: UI | **Scenario**: S1 | **Requirements**: TR-010

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc006_footer_back_to_top_scrolls_to_top`)

**Preconditions**:
- Landing page loaded
- Visitor has scrolled to the footer

| # | Action | Expected |
|---|--------|----------|
| 1 | Click the "Back to top" link in the footer | The page scrolls back to the top (`#top`) |
| 2 | Scroll down again and click "Back to top" a second time | The page scrolls back to the top again — the behaviour is not limited to the first click |

**Expected result**: The page returns to its topmost scroll position every time the link is clicked, not only on the first click of a page load

---

## TC-007 — No intercepting modal appears when "Create account" is clicked

**Priority**: P1 | **Type**: Functional | **Scenario**: S1 | **Requirements**: TR-004

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc007_no_intercepting_modal_on_create_account`)

**Preconditions**:
- No active session
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Click "Create account" in the header, hero, and closing section, one at a time | Navigation to the sign-up screen occurs each time |
| 2 | Inspect the page for any modal dialog appearing before navigation | No modal dialog is shown at any point |

**Expected result**: No intercepting modal is ever shown -- the design's own modal is explicitly non-production scaffolding

---

## TC-008 — Footer FleetIQ mark is plain text and does not navigate when clicked

**Priority**: P3 | **Type**: UI | **Scenario**: S1 | **Requirements**: TR-010

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc008_footer_mark_is_non_interactive`)

**Preconditions**:
- Landing page loaded
- Visitor has scrolled to the footer

| # | Action | Expected |
|---|--------|----------|
| 1 | Attempt to click the "FleetIQ" mark (icon + wordmark) in the footer | No navigation, scroll, or focus change occurs -- the element is not a link |

**Expected result**: The footer mark is confirmed as plain, non-interactive text, unlike the header's mark (TR-003)

---

## TC-009 — Authenticated visitor is redirected to the home page; the landing page is not shown

**Priority**: P1 | **Type**: Functional | **Scenario**: S2 | **Requirements**: TR-002 | **Jira AC**: unbracketed-4

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc009_authenticated_visitor_redirected_home`)

**Preconditions**:
- A valid authenticated session exists (real UI sign-in via FLTIQ-35, research.md R5)

| # | Action | Expected |
|---|--------|----------|
| 1 | With an active session, navigate to the root URL | The browser is redirected to the visitor's home page |
| 2 | Inspect the rendered page | The public landing page content is never rendered, not even briefly |

**Expected result**: The visitor lands on their home page; the landing page's content never appears

---

## TC-010 — Header "Sign in" navigates to the sign-in screen

**Priority**: P1 | **Type**: Functional | **Scenario**: S2 | **Requirements**: TR-005 | **Jira AC**: unbracketed-3

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc010_header_sign_in_navigates_to_signin`)

**Preconditions**:
- No active session
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Click "Sign in" in the header | The browser navigates to the sign-in screen (FLTIQ-35) |

**Expected result**: The visitor lands on the real sign-in screen; no intercepting modal appears

---

## TC-011 — Hero "Sign in" navigates to the sign-in screen

**Priority**: P1 | **Type**: Functional | **Scenario**: S2 | **Requirements**: TR-005 | **Jira AC**: unbracketed-3

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc011_hero_sign_in_navigates_to_signin`)

**Preconditions**:
- No active session
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Click "Sign in" in the hero section | The browser navigates to the sign-in screen (FLTIQ-35) |

**Expected result**: The visitor lands on the real sign-in screen; no intercepting modal appears

---

## TC-012 — Closing-section "Sign in" navigates to the sign-in screen

**Priority**: P1 | **Type**: Functional | **Scenario**: S2 | **Requirements**: TR-005 | **Jira AC**: unbracketed-3

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc012_closing_sign_in_navigates_to_signin`)

**Preconditions**:
- No active session
- Landing page loaded, scrolled to the closing section

| # | Action | Expected |
|---|--------|----------|
| 1 | Click "Sign in" in the closing section | The browser navigates to the sign-in screen (FLTIQ-35) |

**Expected result**: The visitor lands on the real sign-in screen; no intercepting modal appears

---

## TC-014 — Hierarchy explorer pre-selects "Floor 1" on first render

**Priority**: P1 | **Type**: Functional | **Scenario**: S3 | **Requirements**: TR-008 | **Jira AC**: unbracketed-5

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc014_hierarchy_default_selection_floor1`)

**Preconditions**:
- Landing page loaded fresh
- No node has been clicked yet

| # | Action | Expected |
|---|--------|----------|
| 1 | Load the landing page and locate the hierarchy explorer's detail panel | The detail panel shows "Floor 1"'s information (label, status, devices, type, source, note) with no visitor interaction |

**Expected result**: "Floor 1" (node `a1`) is pre-selected by default, matching the design source's `state = { selected: 'a1' }`

---

## TC-015 — Selecting a different node updates the detail panel without a full page reload

**Priority**: P1 | **Type**: Functional | **Scenario**: S3 | **Requirements**: TR-008 | **Jira AC**: unbracketed-5

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc015_selecting_node_updates_detail_panel`)

**Preconditions**:
- Landing page loaded
- Hierarchy explorer visible with "Floor 1" selected

| # | Action | Expected |
|---|--------|----------|
| 1 | Click a different node's row, e.g. "Floor 2" | The detail panel updates to Floor 2's label, status badge, device count, device type, config source and note |
| 2 | Confirm no full page navigation/reload occurred | The page's navigation entry and header/footer remain unchanged; only the detail panel content changed |

**Expected result**: The detail panel reflects the newly selected node's data with no page reload

---

## TC-016 — No FleetIQ API request fires while interacting with the hierarchy explorer

**Priority**: P1 | **Type**: Functional | **Scenario**: S3 | **Requirements**: TR-008 | **Jira AC**: unbracketed-5

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc016_no_api_call_during_hierarchy_interaction`)

**Preconditions**:
- Landing page loaded
- Network request listener attached (research.md R4)

| # | Action | Expected |
|---|--------|----------|
| 1 | Attach a request listener, then select a sequence of different nodes in the hierarchy explorer | No `xhr`/`fetch` request fires at any point during the interaction |

**Expected result**: Zero network requests are observed while interacting with the hierarchy explorer, confirming it is a static, local-data-only component (NFR-002)

---

## TC-017 — Building A and Building B tree rows show a subgroup count distinct from the detail panel's device count

**Priority**: P1 | **Type**: Data | **Scenario**: S3 | **Requirements**: TR-008 | **Jira AC**: unbracketed-5

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc017_meta_distinct_from_devices`)

**Preconditions**:
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Inspect Building A's tree row (without selecting it) | The row's right-aligned text reads "2 subgroups" |
| 2 | Select Building A | The detail panel's "Devices" field reads "79" -- a different value/meaning from the tree row's "2 subgroups" |
| 3 | Inspect Building B's tree row (without selecting it) | The row's right-aligned text reads "0 subgroups" |
| 4 | Select Building B | The detail panel's "Devices" field reads "0" |

**Expected result**: The tree row's `meta` text and the detail panel's `devices` field are confirmed as two distinct fixture fields, never derived from one another

---

## TC-018 — Selecting a node visually highlights that node's own tree row

**Priority**: P1 | **Type**: UI | **Scenario**: S3 | **Requirements**: TR-008

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc018_selected_row_visually_highlighted`)

**Preconditions**:
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Select a node other than the default (e.g. "Floor 2") | That node's row shows `aria-pressed="true"` and a distinguishing background/left-edge style; the previously selected row no longer does |

**Expected result**: Exactly one tree row is visually marked as selected at any time, independent of and in addition to the detail panel updating

---

## TC-019 — Selecting the zero-device node (Building B) updates the detail panel without error

**Priority**: P1 | **Type**: Functional | **Scenario**: S3 | **Requirements**: TR-008

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc019_zero_device_boundary_node`)

**Preconditions**:
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Select "Building B" | The detail panel renders with Devices "0", Type "—", status "Empty", and its note text -- no blank fields, no console error |

**Expected result**: The zero-devices boundary renders correctly rather than blank or erroring

---

## TC-020 — Each of the five hierarchy nodes displays its own exact note text when selected

**Priority**: P1 | **Type**: Data | **Scenario**: S3 | **Requirements**: TR-008

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc020_each_node_exact_note_text`)

**Preconditions**:
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Select "Building A" | Note reads "Subgroups may override the organisation default. Two do." |
| 2 | Select "Floor 1" | Note reads "A change applied here reaches 41 devices. Nothing is applied until you review the diff." |
| 3 | Select "Floor 2" | Note reads "Three devices have not acknowledged the last push. They keep their previous configuration until they do." |
| 4 | Select "Building B" | Note reads "Devices appear here the moment they claim a provisioning token." |
| 5 | Select "Unassigned" | Note reads "Unassigned devices report telemetry but receive no configuration. Place them in a group to give them one." |

**Expected result**: Each node's exact note text renders verbatim, per data-model.md's captured fixture

---

## TC-021 — Selecting "Unassigned" (501 devices, the largest fixture value) renders without truncation at 360px

**Priority**: P1 | **Type**: Compatibility | **Scenario**: S3 | **Requirements**: TR-008, TR-011 | **Jira AC**: unbracketed-5, TIA-AC-74

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc021_largest_value_at_360px`)

**Preconditions**:
- Landing page loaded at a 360px viewport

| # | Action | Expected |
|---|--------|----------|
| 1 | Select the "Unassigned" node | The detail panel renders "501" in the Devices field with no truncation, overflow, or horizontal scroll introduced |

**Expected result**: The largest count in the fixture displays fully at the mandatory minimum viewport width

---

## TC-022 — Page renders with no horizontal scroll or truncation at a 360px viewport

**Priority**: P1 | **Type**: Accessibility | **Scenario**: S4 | **Requirements**: TR-011 | **Jira AC**: TIA-AC-74

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc022_no_horizontal_scroll_at_360px`)

**Preconditions**:
- Browser viewport set to 360px width

| # | Action | Expected |
|---|--------|----------|
| 1 | Load the landing page at 360px width | No horizontal scrollbar appears |
| 2 | Inspect every section (header, hero, capabilities, hierarchy, closing, footer) | No content is truncated or overlapping |

**Expected result**: The page is fully usable at the mandatory minimum viewport width

---

## TC-023 — Every link, section anchor, and hierarchy-explorer node is reachable and operable via keyboard with a visible focus indicator

**Priority**: P1 | **Type**: Accessibility | **Scenario**: S4 | **Requirements**: TR-012 | **Jira AC**: TIA-AC-77

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc023_keyboard_reachability_and_focus_indicator`)

**Preconditions**:
- Landing page loaded
- No pointing device used

| # | Action | Expected |
|---|--------|----------|
| 1 | Press Tab repeatedly from the top of the page | Focus moves through the header links, hero CTAs, capability cards (if focusable), hierarchy nodes, closing CTAs, and footer links, each showing a visible focus indicator |

**Expected result**: Every interactive element is reachable and operable by keyboard alone, with a visible focus indicator at each step

---

## TC-024 — No keyboard trap exists anywhere on the page

**Priority**: P1 | **Type**: Accessibility | **Scenario**: S4 | **Requirements**: TR-012 | **Jira AC**: TIA-AC-77

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc024_no_keyboard_trap`)

**Preconditions**:
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Tab forward through every focusable element to the end of the page, then Shift+Tab back to the start | Focus always advances/retreats; it never becomes stuck on one element |

**Expected result**: No element traps keyboard focus in either direction

---

## TC-025 — Text and control-boundary contrast meets WCAG 2.1 AA thresholds

**Priority**: P1 | **Type**: Accessibility | **Scenario**: S4 | **Requirements**: TR-013 | **Jira AC**: TIA-AC-80

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc025_contrast_meets_wcag_aa`)

**Preconditions**:
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Run the axe-core-based contrast scan (research.md R3) across the full page | Normal text measures at least 4.5:1; large text and control boundaries measure at least 3:1 |

**Expected result**: No contrast violation is reported anywhere on the page

---

## TC-026 — Page remains usable at 200% browser zoom with no content or function lost

**Priority**: P2 | **Type**: Accessibility | **Scenario**: S4 | **Requirements**: TR-014 | **Jira AC**: TIA-AC-81

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc026_usable_at_200_percent_zoom`)

**Preconditions**:
- Viewport halved (1920x1080 -> 960x540) to emulate 200% zoom, per research.md R2

| # | Action | Expected |
|---|--------|----------|
| 1 | Load the landing page at the halved viewport | All content and functionality (CTAs, hierarchy explorer, nav anchors) remain visible and operable |

**Expected result**: No content or function is lost at the 200%-zoom-equivalent viewport

---

## TC-027 — Hierarchy explorer nodes are selectable via keyboard with the same visible focus indicator as the rest of the page

**Priority**: P1 | **Type**: Accessibility | **Scenario**: S4 | **Requirements**: TR-012 | **Jira AC**: TIA-AC-77

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc027_hierarchy_keyboard_operability`)

**Preconditions**:
- Landing page loaded
- No pointing device used

| # | Action | Expected |
|---|--------|----------|
| 1 | Tab to a hierarchy-explorer node | The node shows the same visible focus indicator as any other control |
| 2 | Press Enter or Space | The node becomes selected and the detail panel updates, identical to a mouse click |

**Expected result**: The hierarchy explorer's custom tree control has no keyboard exemption -- it behaves like any other control

---

## TC-028 — Header displays "Sign in" before "Create account"

**Priority**: P2 | **Type**: UI | **Scenario**: S5 | **Requirements**: TR-003

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc028_header_cta_order`)

**Preconditions**:
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Inspect the header's control group | "Sign in" appears before "Create account" in DOM/visual order |

**Expected result**: The header's CTA order matches the design source exactly

---

## TC-029 — Hero renders the exact badge, headline, subhead, and three supporting statistics

**Priority**: P2 | **Type**: UI | **Scenario**: S5 | **Requirements**: TR-006

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc029_hero_exact_copy`)

**Preconditions**:
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Inspect the hero badge | Reads exactly "Multi-tenant device management" |
| 2 | Inspect the headline | Reads exactly "Every device in your fleet, in one hierarchy." |
| 3 | Inspect the subhead | Reads exactly "One place to define device types, organise thousands of units into groups, and review a configuration change before it lands." |
| 4 | Inspect the three statistics | Read exactly "500+ devices onboarded in a single import", "3 levels of grouping, enforced by the platform", "4 roles, from tenant owner to read-only viewer" |

**Expected result**: All hero copy matches the approved design verbatim

---

## TC-030 — Hero displays "Create account" before "Sign in"

**Priority**: P2 | **Type**: UI | **Scenario**: S5 | **Requirements**: TR-006

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc030_hero_cta_order`)

**Preconditions**:
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Inspect the hero's CTA group | "Create account" appears before "Sign in" in DOM/visual order |

**Expected result**: The hero's CTA order matches the design source exactly -- the reverse of the header

---

## TC-031 — Capabilities section renders the exact heading and all six capability cards' copy

**Priority**: P2 | **Type**: UI | **Scenario**: S5 | **Requirements**: TR-007

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc031_capabilities_exact_copy`)

**Preconditions**:
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Inspect the section heading | Reads exactly "Built for fleets that outgrew the spreadsheet." |
| 2 | Inspect all six capability cards in order (01-06) | Each card's title and body match spec.md TR-007 verbatim, in the numbered order 01 through 06 |

**Expected result**: The capabilities section's heading and all six cards match the approved design verbatim

---

## TC-032 — Hierarchy section renders the exact heading and intro paragraph

**Priority**: P2 | **Type**: UI | **Scenario**: S5 | **Requirements**: TR-019

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc032_hierarchy_exact_copy`)

**Preconditions**:
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Inspect the hierarchy section's heading | Reads exactly "Group once. Configure the group." |
| 2 | Inspect the intro paragraph | Reads exactly "Devices inherit configuration from the group they sit in, so a change to a floor reaches forty units without touching one of them individually. Unassigned devices stay visible until someone places them." |

**Expected result**: The hierarchy section's heading and intro copy match the approved design verbatim

---

## TC-033 — Closing section displays "Create account" before "Sign in"

**Priority**: P2 | **Type**: UI | **Scenario**: S5 | **Requirements**: TR-009

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc033_closing_exact_copy_and_order`)

**Preconditions**:
- Landing page loaded, scrolled to the closing section

| # | Action | Expected |
|---|--------|----------|
| 1 | Inspect the closing section's heading and body | Heading reads exactly "Set up your organisation in three steps."; body reads exactly "Sign up, verify your email, name your organisation. You will be adding device types the same afternoon." |
| 2 | Inspect the closing section's CTA group | "Create account" appears before "Sign in", the same order as the hero and opposite the header |

**Expected result**: The closing section's copy and CTA order match the approved design verbatim

---

## TC-034 — Footer displays the FleetIQ mark, "©ACL Digital" attribution, and "Back to top" link

**Priority**: P3 | **Type**: UI | **Scenario**: S5 | **Requirements**: TR-010

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc034_footer_elements_present`)

**Preconditions**:
- Landing page loaded, scrolled to the footer

| # | Action | Expected |
|---|--------|----------|
| 1 | Inspect the footer | The "F" icon + "FleetIQ" wordmark, "©ACL Digital", and a "Back to top" link are all present |
| 2 | Inspect the footer mark's square icon | The square icon contains the letter "F", the same mark as the header |

**Expected result**: All three footer elements are present, with the mark rendering the same square "F" icon as the header, structurally distinct from it (TR-003)

---

## TC-035 — Every visual element resolves to a shared design-system token or component

**Priority**: P2 | **Type**: UI | **Scenario**: S5 | **Requirements**: TR-015 | **Jira AC**: unbracketed-6, FLTIQ-60

**Automation**: Manual

**Preconditions**:
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Perform a component-usage/token audit against the Keel design system (spec.md §11's proposed resolution) | No page-specific styling (inline colour/spacing literals) is found |
| 2 | Compare the rendered page against the approved design in a manual visual-regression review (plan.md A3) | Visual fidelity matches the design system's tokens and components |

**Expected result**: The page is built entirely on shared design-system tokens/components, with no page-specific styling

---

## TC-036 — Page copy makes no capability claim exceeding what MVP1 supports

**Priority**: P3 | **Type**: Functional | **Scenario**: S5 | **Requirements**: TR-016 | **Jira AC**: unbracketed-7

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc036_no_overclaiming_capability`)

**Preconditions**:
- Landing page loaded
- The MVP1-supported capabilities checklist (spec.md §11) is available

| # | Action | Expected |
|---|--------|----------|
| 1 | Compare every capability claim on the page against the checklist (three levels of grouping, four roles, diff-based review, viewer-timezone audit, tenant isolation as a boundary) | No claim on the page exceeds what is on the checklist |

**Expected result**: No overclaiming capability is found on the page

---

## TC-037 — No analytics or tracking request is observed during page load or interaction

**Priority**: P2 | **Type**: Security | **Scenario**: S5 | **Requirements**: TR-017

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc037_no_analytics_or_tracking`)

**Preconditions**:
- Network request listener attached

| # | Action | Expected |
|---|--------|----------|
| 1 | Load the page and interact with every CTA and the hierarchy explorer while monitoring outbound network activity | No request to a known analytics/tracking endpoint pattern is observed |

**Expected result**: The page makes no calls to analytics or tracking services

---

## TC-038 — No pricing, documentation, blog, contact-form, or demo-request content is present

**Priority**: P2 | **Type**: Functional | **Scenario**: S5 | **Requirements**: TR-017

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc038_no_out_of_scope_content`)

**Preconditions**:
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Inspect the full page for pricing tables, documentation links, a blog section, a contact form, or demo-request content | None of these elements are present anywhere on the page |

**Expected result**: The page contains none of the explicitly out-of-scope content categories

---

## TC-039 — Hero displays "Free while you set up your first fleet. No card required." beneath the calls to action

**Priority**: P2 | **Type**: UI | **Scenario**: S5 | **Requirements**: TR-018

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc039_hero_free_placeholder_line`)

**Preconditions**:
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Inspect the hero section beneath the calls to action | The line "Free while you set up your first fleet. No card required." is present, exactly as designed |

**Expected result**: The line renders verbatim beneath the hero CTAs, matching the design source -- authorized to ship as designed by the requester's decision resolving CF-002 (spec.md Clarifications, 2026-09-21)

---

## TC-041 — Page remains usable with no content loss at 360px combined with 200% zoom

**Priority**: P2 | **Type**: Accessibility | **Scenario**: S4 | **Requirements**: TR-011, TR-014 | **Jira AC**: TIA-AC-74, TIA-AC-81

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc041_360px_combined_with_200_percent_zoom`)

**Preconditions**:
- Viewport set to 360px width, further halved to emulate 200% zoom (180px-equivalent content area, per research.md R2)

| # | Action | Expected |
|---|--------|----------|
| 1 | Load the landing page at the combined boundary viewport | No horizontal scroll is introduced beyond what 360px alone requires, and no content or function is lost |

**Expected result**: The combined boundary of the two individually-required conditions still renders usably

---

## TC-042 — Skeleton loader displays while auth state resolves at first paint

**Priority**: P3 | **Type**: UI | **Scenario**: S1 | **Requirements**: TR-020

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc042_skeleton_loader_during_auth_resolution`)

**Preconditions**:
- The auth-check network request is intercepted and delayed (e.g. Playwright route handler) to create a reliably observable loading window

| # | Action | Expected |
|---|--------|----------|
| 1 | Navigate to the root URL with the auth-check request delayed | A skeleton loader is visible immediately, before either the landing page or an authenticated redirect renders |
| 2 | Allow the delayed auth-check to resolve | The skeleton loader is replaced by the correct outcome -- the landing page (TR-001) for an unauthenticated visitor, or the home-page redirect (TR-002) for an authenticated one |

**Expected result**: A skeleton loader is shown during the auth-resolution window, regardless of the eventual authenticated/unauthenticated outcome

---

## TC-043 — [BLOCKED] Hierarchy explorer behaviour if its client-side script fails to load

**Priority**: P2 | **Type**: Functional | **Scenario**: S3 | **Requirements**: -

**Automation**: Blocked

**Preconditions**:
- Not executed while blocked

| # | Action | Expected |
|---|--------|----------|
| 1 | Do not execute this case until spec.md §13b Q3 is answered and EC-003 states a fallback behaviour | N/A -- placeholder only, no assertion is made |

**Expected result**: BLOCKED -- narrowed 2026-09-21: the requester confirmed the rest of the page (header/hero/closing CTAs) functions independent of the explorer's script, resolving the shared-JS-bundle risk this note originally flagged. What appears in the explorer's own place on failure remains unspecified by any source; asserting one would fabricate a product behaviour no source defines. This row exists so that remaining half of EC-003 stays visible rather than silently vanishing.

---

## TC-044 — Header displays "Capabilities" and "Hierarchy" as section-anchor links

**Priority**: P2 | **Type**: UI | **Scenario**: S5 | **Requirements**: TR-003

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc044_header_has_capabilities_and_hierarchy_anchors`)

**Preconditions**:
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Inspect the header's nav area, between the product mark and the Sign in/Create account controls | "Capabilities" and "Hierarchy" both render as clickable links (`<a>` elements), not plain text |

**Expected result**: Both section-anchor links are present in the header, matching TR-003's explicit requirement that the header renders "the section anchors (Capabilities, Hierarchy)"

---

## TC-045 — Header "Capabilities" and "Hierarchy" links each navigate to their own correct, distinct section

**Priority**: P2 | **Type**: UI | **Scenario**: S1 | **Requirements**: TR-003

**Automation**: Automated (`automation/tests/ui/test_landing.py::test_tc045_header_anchors_navigate_to_correct_section`)

**Preconditions**:
- Landing page loaded

| # | Action | Expected |
|---|--------|----------|
| 1 | Click "Capabilities" in the header | The page scrolls to the Capabilities section -- confirmed by the heading "Built for fleets that outgrew the spreadsheet." (TR-007) becoming visible, not the Hierarchy section |
| 2 | From the top of the page, click "Hierarchy" in the header | The page scrolls to the Hierarchy section -- confirmed by the heading "Group once. Configure the group." (TR-019) becoming visible, not the Capabilities section |

**Expected result**: Each link navigates to its own correct, distinct section; neither lands on the other's destination

---
