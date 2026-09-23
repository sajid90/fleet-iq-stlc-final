"""FLTIQ-62 — public landing page.

Every test traces to a TC-xxx in test-cases.json and a TR-xxx in spec.md
(tasks.md's Traceability table has the full chain). Each test navigates
fresh (constitution VI) — no shared session/state between tests.

TC-035 (manual, `automatable: false` in test-cases.json) and TC-043
(Blocked — EC-003 unanswered) are intentionally not automated here, per
constitution II ("never implement a case whose automation_status is
Blocked") and per test-cases.json being the authoritative record over
tasks.md's T038 note (see the Completion Report).
"""

from __future__ import annotations

import re

import allure
import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import expect

from automation.locators.landing_locators import LandingLocators as L
from automation.pages.landing_page import LandingPage
from automation.utils.config import Settings
from automation.utils.data_loader import load_json

ANALYTICS_HOST_PATTERN = re.compile(
    r"google-analytics\.com|googletagmanager\.com|segment\.(io|com)|mixpanel\.com|"
    r"hotjar\.com|fullstory\.com|amplitude\.com|intercom\.io|doubleclick\.net",
    re.IGNORECASE,
)


@pytest.fixture
def nodes() -> dict:
    return load_json("landing.json")["nodes"]


def _has_horizontal_scroll(page) -> bool:
    return page.evaluate(
        "() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1"
    )


# ===========================================================================
# Phase 3 — Scenario 1: unauthenticated visitor discovers FleetIQ (P1)
# ===========================================================================

@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Unauthenticated visitor discovers FleetIQ and reaches sign-up")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("TC-001: Unauthenticated visitor sees the landing page with no sign-in prompt")
@allure.testcase("TC-001")
@pytest.mark.smoke
@pytest.mark.p1
def test_tc001_unauthenticated_visitor_sees_landing_page(landing_page: LandingPage):
    landing_page.open()
    expect(landing_page.page).to_have_url(re.compile(r"^http.*"))
    assert landing_page.is_visible(landing_page.page.get_by_role("heading", level=1)), (
        "landing page heading did not render"
    )
    assert not landing_page.is_modal_visible(timeout=1_000), "no sign-in prompt/modal should appear"


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Unauthenticated visitor discovers FleetIQ and reaches sign-up")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title('TC-002: Header "Create account" navigates to the sign-up screen')
@allure.testcase("TC-002")
@pytest.mark.smoke
@pytest.mark.p1
def test_tc002_header_create_account_navigates_to_signup(landing_page: LandingPage):
    landing_page.open()
    landing_page.click_create_account("header")
    expect(landing_page.page).to_have_url(re.compile(r"/create-account"))


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Unauthenticated visitor discovers FleetIQ and reaches sign-up")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title('TC-003: Hero "Create account" navigates to the sign-up screen')
@allure.testcase("TC-003")
@pytest.mark.p1
def test_tc003_hero_create_account_navigates_to_signup(landing_page: LandingPage):
    landing_page.open()
    landing_page.click_create_account("hero")
    expect(landing_page.page).to_have_url(re.compile(r"/create-account"))


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Unauthenticated visitor discovers FleetIQ and reaches sign-up")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title('TC-004: Closing-section "Create account" navigates to the sign-up screen')
@allure.testcase("TC-004")
@pytest.mark.p1
def test_tc004_closing_create_account_navigates_to_signup(landing_page: LandingPage):
    landing_page.open()
    landing_page.scroll_to_bottom()
    landing_page.click_create_account("closing")
    expect(landing_page.page).to_have_url(re.compile(r"/create-account"))


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Unauthenticated visitor discovers FleetIQ and reaches sign-up")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-005: Header product mark scrolls the page back to the top when clicked")
@allure.testcase("TC-005")
@pytest.mark.p2
def test_tc005_header_product_mark_scrolls_to_top(landing_page: LandingPage):
    landing_page.open()
    # TR-003: the mark is "a square icon containing 'F' beside the 'FleetIQ'
    # wordmark" — the glyph is part of the requirement, not decoration.
    assert landing_page.header_mark_icon_text() == "F", (
        "the header product mark's square icon does not contain 'F' "
        f"(got {landing_page.header_mark_icon_text()!r})"
    )
    # Exercised twice: TR-003 puts no "first click only" qualifier on this
    # behaviour, and a plain <a href="#top"> re-scrolls on every click in any
    # browser. The second pass is where a same-fragment no-op would surface.
    for attempt in (1, 2):
        landing_page.scroll_to_bottom()
        assert landing_page.scroll_y() > 0, f"attempt {attempt}: page did not scroll down"
        landing_page.click_product_mark()
        assert landing_page.scrolled_to_top_within(), (
            f"attempt {attempt}: clicking the product mark did not return the page to "
            f"the top (scrollY={landing_page.scroll_y()}, url={landing_page.current_url()})"
        )


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Unauthenticated visitor discovers FleetIQ and reaches sign-up")
@allure.severity(allure.severity_level.MINOR)
@allure.title('TC-006: Footer "Back to top" link scrolls the page back to the top when clicked')
@allure.testcase("TC-006")
@pytest.mark.p3
def test_tc006_footer_back_to_top_scrolls_to_top(landing_page: LandingPage):
    landing_page.open()
    # Exercised twice for the same reason as TC-005: TR-010 requires the link
    # to scroll the page to the top, with no first-click-only qualifier.
    for attempt in (1, 2):
        landing_page.scroll_to_bottom()
        assert landing_page.scroll_y() > 0, f"attempt {attempt}: page did not scroll down"
        landing_page.click_back_to_top()
        assert landing_page.scrolled_to_top_within(), (
            f'attempt {attempt}: "Back to top" did not return the page to the top '
            f"(scrollY={landing_page.scroll_y()}, url={landing_page.current_url()})"
        )


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Unauthenticated visitor discovers FleetIQ and reaches sign-up")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('TC-007: No intercepting modal appears when "Create account" is clicked')
@allure.testcase("TC-007")
@pytest.mark.p1
@pytest.mark.negative
def test_tc007_no_intercepting_modal_on_create_account(landing_page: LandingPage):
    for location in ("header", "hero", "closing"):
        landing_page.open()
        if location == "closing":
            landing_page.scroll_to_bottom()
        assert not landing_page.is_modal_visible(timeout=500), f"modal shown before {location} click"
        landing_page.click_create_account(location)
        assert not landing_page.is_modal_visible(timeout=500), f"modal shown after {location} click"
        expect(landing_page.page).to_have_url(re.compile(r"/create-account"))


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Unauthenticated visitor discovers FleetIQ and reaches sign-up")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC-008: Footer FleetIQ mark is plain text and does not navigate when clicked")
@allure.testcase("TC-008")
@pytest.mark.p3
@pytest.mark.negative
def test_tc008_footer_mark_is_non_interactive(landing_page: LandingPage):
    landing_page.open()
    landing_page.scroll_to_bottom()
    assert not landing_page.footer_mark_is_link(), "footer mark must not be a link (unlike the header's, TR-003)"
    url_before = landing_page.current_url()
    landing_page.attempt_click_footer_mark()
    landing_page.page.wait_for_timeout(300)
    assert landing_page.current_url() == url_before, "clicking the footer mark must not navigate"


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Page content and structure match the approved scope")
@allure.severity(allure.severity_level.NORMAL)
@allure.title('TC-044: Header displays "Capabilities" and "Hierarchy" as section-anchor links')
@allure.testcase("TC-044")
@pytest.mark.p2
def test_tc044_header_has_capabilities_and_hierarchy_anchors(landing_page: LandingPage):
    landing_page.open()
    assert landing_page.header_nav_anchor_count("Capabilities") == 1, (
        "header must render a 'Capabilities' section-anchor link (TR-003)"
    )
    assert landing_page.header_nav_anchor_count("Hierarchy") == 1, (
        "header must render a 'Hierarchy' section-anchor link (TR-003)"
    )


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Unauthenticated visitor discovers FleetIQ and reaches sign-up")
@allure.severity(allure.severity_level.NORMAL)
@allure.title('TC-045: Header "Capabilities" and "Hierarchy" links each navigate to their own correct, distinct section')
@allure.testcase("TC-045")
@pytest.mark.p2
def test_tc045_header_anchors_navigate_to_correct_section(landing_page: LandingPage):
    landing_page.open()
    landing_page.click_header_nav_anchor("Capabilities")
    landing_page.page.wait_for_timeout(300)
    expect(landing_page.page.locator("section[aria-label='Capabilities'] h2")).to_be_in_viewport()

    landing_page.open()
    landing_page.click_header_nav_anchor("Hierarchy")
    landing_page.page.wait_for_timeout(300)
    expect(landing_page.page.locator("section[aria-label='Hierarchy example'] h2")).to_be_in_viewport()


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Unauthenticated visitor discovers FleetIQ and reaches sign-up")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC-042: Skeleton loader displays while auth state resolves at first paint")
@allure.testcase("TC-042")
@pytest.mark.p3
def test_tc042_skeleton_loader_during_auth_resolution(landing_page: LandingPage):
    # Test-mechanics note (INFERRED, per research.md R4's precedent): the
    # current build makes zero XHR/fetch requests on load (confirmed by
    # network probing during implementation), so there is no async auth
    # check request to intercept-and-delay as TC-042's own note describes.
    # This checks the earliest observable frame directly instead.
    landing_page.page.goto(f"{landing_page.settings.base_url}/", wait_until="commit")
    seen_skeleton = landing_page.is_skeleton_loader_visible(timeout=1_000)
    landing_page.page.wait_for_load_state("networkidle")
    assert seen_skeleton, "no skeleton loader was observed during the auth-resolution window (TR-020)"
    assert not landing_page.is_skeleton_loader_visible(timeout=500), (
        "skeleton loader should be replaced once auth state resolves"
    )


# ===========================================================================
# Phase 4 — Scenario 2: authenticated visitor is routed past the landing page (P1)
# ===========================================================================

@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Existing user returns and is routed past the landing page")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("TC-009: Authenticated visitor is redirected to the home page; the landing page is not shown")
@allure.testcase("TC-009")
@pytest.mark.smoke
@pytest.mark.p1
def test_tc009_authenticated_visitor_redirected_home(landing_page: LandingPage, settings: Settings):
    try:
        settings.require_credentials()
    except RuntimeError as exc:
        pytest.skip(f"research.md R5: {exc}")
    # FLTIQ-35's sign-in page object doesn't exist yet (owned by that
    # feature, per plan.md B3) — best-effort generic sign-in, matching R5's
    # "real UI sign-in" approach.
    landing_page.page.goto(f"{settings.base_url}/sign-in")
    username, password = settings.require_credentials()
    landing_page.page.get_by_label(re.compile("email|username", re.I)).fill(username)
    landing_page.page.get_by_label(re.compile("password", re.I)).fill(password)
    landing_page.page.get_by_role("button", name=re.compile("sign in|log in", re.I)).click()
    landing_page.page.wait_for_load_state("networkidle")

    landing_page.open()
    expect(landing_page.page).not_to_have_url(re.compile(r"^http://[^/]+/?$"))
    assert not landing_page.is_visible(
        landing_page.page.get_by_role("heading", name="Every device in your fleet, in one hierarchy.", exact=True),
        timeout=1_000,
    ), "the landing page must never render for an authenticated visitor"


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Existing user returns and is routed past the landing page")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title('TC-010: Header "Sign in" navigates to the sign-in screen')
@allure.testcase("TC-010")
@pytest.mark.smoke
@pytest.mark.p1
def test_tc010_header_sign_in_navigates_to_signin(landing_page: LandingPage):
    landing_page.open()
    landing_page.click_sign_in("header")
    expect(landing_page.page).to_have_url(re.compile(r"/sign-in"))


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Existing user returns and is routed past the landing page")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title('TC-011: Hero "Sign in" navigates to the sign-in screen')
@allure.testcase("TC-011")
@pytest.mark.p1
def test_tc011_hero_sign_in_navigates_to_signin(landing_page: LandingPage):
    landing_page.open()
    landing_page.click_sign_in("hero")
    expect(landing_page.page).to_have_url(re.compile(r"/sign-in"))


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Existing user returns and is routed past the landing page")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title('TC-012: Closing-section "Sign in" navigates to the sign-in screen')
@allure.testcase("TC-012")
@pytest.mark.p1
def test_tc012_closing_sign_in_navigates_to_signin(landing_page: LandingPage):
    landing_page.open()
    landing_page.scroll_to_bottom()
    landing_page.click_sign_in("closing")
    expect(landing_page.page).to_have_url(re.compile(r"/sign-in"))


# ===========================================================================
# Phase 5 — Scenario 3: hierarchy explorer, no backend call (P1)
# ===========================================================================

@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Visitor explores the hierarchy explorer without triggering a backend call")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('TC-014: Hierarchy explorer pre-selects "Floor 1" on first render')
@allure.testcase("TC-014")
@pytest.mark.p1
def test_tc014_hierarchy_default_selection_floor1(landing_page: LandingPage, nodes: dict):
    landing_page.open()
    assert landing_page.is_detail_panel_visible(timeout=3_000), (
        "no default-selection detail panel is rendered for 'Floor 1' (TR-008/EC-002)"
    )
    assert landing_page.detail_panel_label() == nodes["a1"]["label"]


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Visitor explores the hierarchy explorer without triggering a backend call")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC-015: Selecting a different node updates the detail panel without a full page reload")
@allure.testcase("TC-015")
@pytest.mark.p1
def test_tc015_selecting_node_updates_detail_panel(landing_page: LandingPage, nodes: dict):
    landing_page.open()
    url_before = landing_page.current_url()
    landing_page.select_hierarchy_node("Floor 2")
    assert landing_page.detail_panel_devices() == str(nodes["a2"]["devices"])
    assert landing_page.detail_panel_note() == nodes["a2"]["note"]
    assert landing_page.current_url() == url_before, "selecting a node must not cause a full page reload"


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Visitor explores the hierarchy explorer without triggering a backend call")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC-016: No FleetIQ API request fires while interacting with the hierarchy explorer")
@allure.testcase("TC-016")
@pytest.mark.p1
def test_tc016_no_api_call_during_hierarchy_interaction(landing_page: LandingPage):
    xhr_fetch: list[str] = []
    landing_page.page.on(
        "request",
        lambda r: xhr_fetch.append(r.url) if r.resource_type in ("xhr", "fetch") else None,
    )
    landing_page.open()
    for label in ("Floor 1", "Floor 2", "Building A", "Building B", "Unassigned"):
        landing_page.select_hierarchy_node(label)
    assert xhr_fetch == [], f"unexpected network request(s) during hierarchy interaction: {xhr_fetch}"


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Visitor explores the hierarchy explorer without triggering a backend call")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-017: Building A/B tree rows show a subgroup count distinct from the detail panel's device count")
@allure.testcase("TC-017")
@pytest.mark.p1
def test_tc017_meta_distinct_from_devices(landing_page: LandingPage, nodes: dict):
    landing_page.open()
    # Exact match on the isolated meta node, not a substring of the whole
    # row's text (constitution VII.a) — the row's prefix/label text must not
    # be able to mask a wrong meta value.
    assert landing_page.hierarchy_row_meta_value("Building A") == nodes["a"]["meta"]
    landing_page.select_hierarchy_node("Building A")
    assert landing_page.detail_panel_devices() == str(nodes["a"]["devices"])

    assert landing_page.hierarchy_row_meta_value("Building B") == nodes["b"]["meta"]
    landing_page.select_hierarchy_node("Building B")
    assert landing_page.detail_panel_devices() == str(nodes["b"]["devices"])


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Visitor explores the hierarchy explorer without triggering a backend call")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-018: Selecting a node visually highlights that node's own tree row")
@allure.testcase("TC-018")
@pytest.mark.p1
def test_tc018_selected_row_visually_highlighted(landing_page: LandingPage):
    landing_page.open()
    landing_page.select_hierarchy_node("Floor 2")
    assert landing_page.hierarchy_row_aria_pressed("Floor 2") == "true", (
        "the selected tree row does not expose aria-pressed='true' (TR-008)"
    )
    assert landing_page.hierarchy_row_aria_pressed("Floor 1") in (None, "false"), (
        "the previously selected row should no longer be marked pressed"
    )


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Visitor explores the hierarchy explorer without triggering a backend call")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-019: Selecting the zero-device node (Building B) updates the detail panel without error")
@allure.testcase("TC-019")
@pytest.mark.p1
@pytest.mark.boundary
def test_tc019_zero_device_boundary_node(landing_page: LandingPage, nodes: dict):
    console_errors: list[str] = []
    landing_page.page.on("pageerror", lambda err: console_errors.append(str(err)))
    landing_page.open()
    landing_page.select_hierarchy_node("Building B")
    assert landing_page.detail_panel_devices() == "0"
    assert landing_page.detail_panel_type() == nodes["b"]["type"]
    assert console_errors == [], f"page errors on zero-device selection: {console_errors}"


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Visitor explores the hierarchy explorer without triggering a backend call")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-020: Each of the five hierarchy nodes displays its own exact note text when selected")
@allure.testcase("TC-020")
@pytest.mark.p1
def test_tc020_each_node_exact_note_text(landing_page: LandingPage, nodes: dict):
    landing_page.open()
    for node in nodes.values():
        landing_page.select_hierarchy_node(node["label"])
        assert landing_page.detail_panel_note() == node["note"], f"note mismatch for {node['label']}"


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Visitor explores the hierarchy explorer without triggering a backend call")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-021: Selecting \"Unassigned\" (501 devices) renders without truncation at 360px")
@allure.testcase("TC-021")
@pytest.mark.p1
@pytest.mark.boundary
def test_tc021_largest_value_at_360px(landing_page: LandingPage, nodes: dict):
    landing_page.page.set_viewport_size({"width": 360, "height": 800})
    landing_page.open()
    landing_page.select_hierarchy_node("Unassigned")
    assert landing_page.detail_panel_devices() == str(nodes["un"]["devices"])
    assert not _has_horizontal_scroll(landing_page.page), "horizontal scroll introduced at 360px"


# ===========================================================================
# Phase 6 — Scenario 4: accessibility & responsive baseline (P1)
# ===========================================================================

@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("The landing page meets the epic's accessibility and responsive baseline")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC-022: Page renders with no horizontal scroll or truncation at a 360px viewport")
@allure.testcase("TC-022")
@pytest.mark.p1
@pytest.mark.a11y
def test_tc022_no_horizontal_scroll_at_360px(landing_page: LandingPage):
    landing_page.page.set_viewport_size({"width": 360, "height": 800})
    landing_page.open()
    assert not _has_horizontal_scroll(landing_page.page), "horizontal scroll present at 360px"


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("The landing page meets the epic's accessibility and responsive baseline")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC-023: Every interactive element is reachable and operable via keyboard with a visible focus indicator")
@allure.testcase("TC-023")
@pytest.mark.p1
@pytest.mark.a11y
def test_tc023_keyboard_reachability_and_focus_indicator(landing_page: LandingPage):
    landing_page.open()
    focused_tags: set[str] = set()
    for _ in range(30):
        landing_page.page.keyboard.press("Tab")
        handle = landing_page.page.evaluate_handle("() => document.activeElement")
        tag = handle.get_property("tagName").json_value()
        if not tag or tag in ("NEXTJS-PORTAL", "BODY", "HTML"):
            # NEXTJS-PORTAL is the dev-server-only devtools overlay, never
            # present in production. BODY/HTML means focus fell off the end
            # of the document (no element actually focused) rather than a
            # genuine focusable target (test mechanics, not page content).
            continue
        focused_tags.add(tag)
        outline = landing_page.page.evaluate(
            "(el) => getComputedStyle(el).outlineStyle !== 'none' || getComputedStyle(el).boxShadow !== 'none'",
            handle,
        )
        assert outline, f"focused element <{tag}> has no visible focus indicator"
    assert "A" in focused_tags, "no links were reachable via keyboard"


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("The landing page meets the epic's accessibility and responsive baseline")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC-024: No keyboard trap exists anywhere on the page")
@allure.testcase("TC-024")
@pytest.mark.p1
@pytest.mark.a11y
def test_tc024_no_keyboard_trap(landing_page: LandingPage):
    landing_page.open()
    seen: list[str] = []
    for _ in range(25):
        landing_page.page.keyboard.press("Tab")
        seen.append(landing_page.page.evaluate("() => document.activeElement.outerHTML.slice(0, 60)"))
    for _ in range(25):
        landing_page.page.keyboard.press("Shift+Tab")
    assert len(set(seen)) > 1, "focus never advanced across Tab presses — possible keyboard trap"


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("The landing page meets the epic's accessibility and responsive baseline")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC-025: Text and control-boundary contrast meets WCAG 2.1 AA thresholds")
@allure.testcase("TC-025")
@pytest.mark.p1
@pytest.mark.a11y
def test_tc025_contrast_meets_wcag_aa(landing_page: LandingPage):
    landing_page.open()
    results = Axe().run(landing_page.page, options={"runOnly": {"type": "rule", "values": ["color-contrast"]}})
    violations = results.response["violations"]
    assert violations == [], f"contrast violations found: {results.generate_snapshot()}"


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("The landing page meets the epic's accessibility and responsive baseline")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-026: Page remains usable at 200% browser zoom with no content or function lost")
@allure.testcase("TC-026")
@pytest.mark.p2
@pytest.mark.a11y
def test_tc026_usable_at_200_percent_zoom(landing_page: LandingPage, settings: Settings):
    landing_page.page.set_viewport_size(
        {"width": settings.viewport_width // 2, "height": settings.viewport_height // 2}
    )
    landing_page.open()
    assert landing_page.is_visible(landing_page.page.get_by_role("heading", level=1))
    landing_page.click_create_account("hero")
    expect(landing_page.page).to_have_url(re.compile(r"/create-account"))


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("The landing page meets the epic's accessibility and responsive baseline")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC-027: Hierarchy explorer nodes are selectable via keyboard with the same visible focus indicator")
@allure.testcase("TC-027")
@pytest.mark.p1
@pytest.mark.a11y
def test_tc027_hierarchy_keyboard_operability(landing_page: LandingPage):
    landing_page.open()
    row = landing_page.hierarchy_row("Floor 2")
    row.focus()
    landing_page.page.keyboard.press("Enter")
    assert landing_page.hierarchy_row_aria_pressed("Floor 2") == "true", (
        "hierarchy node did not become selected via keyboard Enter"
    )


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("The landing page meets the epic's accessibility and responsive baseline")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-041: Page remains usable with no content loss at 360px combined with 200% zoom")
@allure.testcase("TC-041")
@pytest.mark.p2
@pytest.mark.a11y
@pytest.mark.boundary
def test_tc041_360px_combined_with_200_percent_zoom(landing_page: LandingPage):
    landing_page.page.set_viewport_size({"width": 180, "height": 320})
    landing_page.open()
    assert landing_page.is_visible(landing_page.page.get_by_role("heading", level=1))


# ===========================================================================
# Phase 7 — Scenario 5: content & structure match approved scope (P2)
# ===========================================================================

@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Page content and structure match the approved scope")
@allure.severity(allure.severity_level.NORMAL)
@allure.title('TC-028: Header displays "Sign in" before "Create account"')
@allure.testcase("TC-028")
@pytest.mark.p2
def test_tc028_header_cta_order(landing_page: LandingPage):
    landing_page.open()
    # Exact, case-sensitive and ordered: TR-003 fixes both the labels and
    # their order, so one comparison covers both. The product mark is
    # excluded — it is a link, but not one of the two controls.
    ctas = [t for t in landing_page.header_cta_order() if t != "FleetIQ"]
    assert ctas == ["Sign in", "Create account"], (
        f"header controls must read exactly ['Sign in', 'Create account'] in that order, got {ctas}"
    )


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Page content and structure match the approved scope")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-029: Hero renders the exact badge, headline, subhead, and three supporting statistics")
@allure.testcase("TC-029")
@pytest.mark.p2
def test_tc029_hero_exact_copy(landing_page: LandingPage):
    landing_page.open()
    assert landing_page.hero_badge_text() == "Multi-tenant device management"
    assert landing_page.hero_headline_text() == "Every device in your fleet, in one hierarchy."
    assert landing_page.hero_subhead_text() == (
        "One place to define device types, organise thousands of units into groups, "
        "and review a configuration change before it lands."
    )
    stats = landing_page.hero_stats_texts()
    assert stats == [
        "500+ devices onboarded in a single import",
        "3 levels of grouping, enforced by the platform",
        "4 roles, from tenant owner to read-only viewer",
    ]


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Page content and structure match the approved scope")
@allure.severity(allure.severity_level.NORMAL)
@allure.title('TC-030: Hero displays "Create account" before "Sign in"')
@allure.testcase("TC-030")
@pytest.mark.p2
def test_tc030_hero_cta_order(landing_page: LandingPage):
    landing_page.open()
    # Exact, case-sensitive and ordered — TR-006 fixes both (see TC-028).
    ctas = landing_page.hero_cta_order()
    assert ctas == ["Create account", "Sign in"], (
        f"hero CTAs must read exactly ['Create account', 'Sign in'] in that order, got {ctas}"
    )


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Page content and structure match the approved scope")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-031: Capabilities section renders the exact heading and all six capability cards' copy")
@allure.testcase("TC-031")
@pytest.mark.p2
def test_tc031_capabilities_exact_copy(landing_page: LandingPage):
    landing_page.open()
    assert landing_page.capabilities_heading_text() == "Built for fleets that outgrew the spreadsheet."
    expected = [
        ("01", "Device types first",
         "Describe a model once — its telemetry, its settings, its identifiers — and every unit you add inherits it."),
        ("02", "A hierarchy that holds",
         "Organisation, group, subgroup. Three levels, no deeper, so nobody builds a tree the next person cannot read."),
        ("03", "Review before it applies",
         "Configuration changes queue up as a diff. See which devices are affected, then apply — or do not."),
        ("04", "Roles people understand",
         "Four roles, each described in a line. Invite a colleague without reading a permissions matrix."),
        ("05", "A complete audit trail",
         "Who changed what, when, and what the value was before. Shown in your own time zone."),
        ("06", "Tenant isolation",
         "One tenant never sees another's devices, members, or history. It is not a filter — it is the boundary."),
    ]
    cards = landing_page.capability_cards()
    assert len(cards) == 6, f"expected 6 capability cards, found {len(cards)}"
    for (number, title, body), card in zip(expected, cards):
        assert card["number"] == number
        assert card["title"] == title
        assert card["body"] == body


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Page content and structure match the approved scope")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-032: Hierarchy section renders the exact heading and intro paragraph")
@allure.testcase("TC-032")
@pytest.mark.p2
def test_tc032_hierarchy_exact_copy(landing_page: LandingPage):
    landing_page.open()
    assert landing_page.hierarchy_heading_text() == "Group once. Configure the group."
    assert landing_page.hierarchy_intro_text() == (
        "Devices inherit configuration from the group they sit in, so a change to a floor "
        "reaches forty units without touching one of them individually. Unassigned devices "
        "stay visible until someone places them."
    )
    # TR-008/data-model.md: the tree panel's own header line — closed by
    # §13b Q4 (2026-09-21) as one of "today's exact static values" the
    # suite tests as shipped, not an open placeholder question.
    assert landing_page.hierarchy_org_label_text() == "XYZ — organisation"


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Page content and structure match the approved scope")
@allure.severity(allure.severity_level.NORMAL)
@allure.title('TC-033: Closing section displays "Create account" before "Sign in"')
@allure.testcase("TC-033")
@pytest.mark.p2
def test_tc033_closing_exact_copy_and_order(landing_page: LandingPage):
    landing_page.open()
    landing_page.scroll_to_bottom()
    assert landing_page.closing_heading_text() == "Set up your organisation in three steps."
    assert landing_page.closing_body_text() == (
        "Sign up, verify your email, name your organisation. You will be adding device "
        "types the same afternoon."
    )
    # Exact, case-sensitive and ordered — TR-009 fixes both (see TC-028).
    ctas = landing_page.closing_cta_order()
    assert ctas == ["Create account", "Sign in"], (
        f"closing CTAs must read exactly ['Create account', 'Sign in'] in that order, got {ctas}"
    )


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Page content and structure match the approved scope")
@allure.severity(allure.severity_level.MINOR)
@allure.title('TC-034: Footer displays the FleetIQ mark, "©ACL Digital" attribution, and "Back to top" link')
@allure.testcase("TC-034")
@pytest.mark.p3
def test_tc034_footer_elements_present(landing_page: LandingPage):
    landing_page.open()
    landing_page.scroll_to_bottom()
    # Exact match throughout (constitution VII.a) — "FleetIQ"/"©ACL Digital"
    # are literal strings TR-010 names, not fragments to search for.
    assert landing_page.footer_mark_text() == "FleetIQ"
    # TR-010: "the same square 'F' icon + 'FleetIQ' wordmark as the header"
    assert landing_page.footer_mark_icon_text() == "F", (
        "the footer mark's square icon does not contain 'F' "
        f"(got {landing_page.footer_mark_icon_text()!r})"
    )
    assert landing_page.footer_attribution_text() == "©ACL Digital"
    assert landing_page.is_back_to_top_visible()


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Page content and structure match the approved scope")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-035: Every visual element resolves to a shared design-system token or component")
@allure.testcase("TC-035")
@pytest.mark.p2
def test_tc035_design_system_token_application(landing_page: LandingPage):
    """Automated half of TC-035 (task T038) — the deterministic token audit.

    The manual visual-regression half stays in plan.md A3. This compares what
    the build renders against the Keel tokens the design source declares for
    each surface, so a token applied to the wrong property is caught. Every
    check is collected and reported together: these defects cluster, and
    failing on the first would hide the rest.
    """
    landing_page.open()
    BG, SURFACE, BORDER, NAVY = (
        "rgb(247, 248, 250)",  # --keel-bg      #F7F8FA
        "rgb(255, 255, 255)",  # --keel-surface #FFFFFF
        "rgb(226, 229, 235)",  # --keel-border  #E2E5EB
        "rgb(0, 13, 53)",      # --keel-deck-navy #000D35
    )
    expected_backgrounds = [
        ("body", BG, "--keel-bg"),
        (L.HEADER, SURFACE, "--keel-surface"),
        ('section[aria-label="Platform overview"]', SURFACE, "--keel-surface"),
        (L.CAPABILITIES_GRID, "rgba(0, 0, 0, 0)", "no background declared in the design"),
        (L.CAPABILITY_CARD, SURFACE, "--keel-surface"),
        (L.HIERARCHY_PANEL, SURFACE, "--keel-surface"),
        (L.CLOSING_SECTION, NAVY, "--keel-deck-navy"),
        (L.FOOTER, SURFACE, "--keel-surface"),
    ]
    problems: list[str] = []
    for selector, expected, token in expected_backgrounds:
        styles = landing_page.computed_styles(selector)
        if styles is None:
            problems.append(f"{selector}: element not found")
            continue
        if styles["background"] != expected:
            problems.append(
                f"{selector}: background is {styles['background']}, "
                f"design declares {token} ({expected})"
            )
    # The design gives cards and the hierarchy panel a 1px border, a radius
    # and a shadow; the header a bottom border.
    for selector in (L.CAPABILITY_CARD, L.HIERARCHY_PANEL):
        styles = landing_page.computed_styles(selector)
        if styles is None:
            continue
        if styles["borderTopWidth"] == "0px":
            problems.append(f"{selector}: no border, design declares 1px solid --keel-border")
        if styles["radius"] == "0px":
            problems.append(f"{selector}: no border-radius, design declares --keel-radius-lg")
        if styles["shadow"] == "none":
            problems.append(f"{selector}: no box-shadow, design declares --keel-shadow-sm")
    header = landing_page.computed_styles(L.HEADER)
    if header and header["borderBottomWidth"] == "0px":
        problems.append(f"{L.HEADER}: no bottom border, design declares 1px solid --keel-border")

    assert not problems, "design-system token application defects:\n  - " + "\n  - ".join(problems)


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Page content and structure match the approved scope")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC-036: Page copy makes no capability claim exceeding what MVP1 supports")
@allure.testcase("TC-036")
@pytest.mark.p3
def test_tc036_no_overclaiming_capability(landing_page: LandingPage):
    landing_page.open()
    text = landing_page.full_page_text().lower()
    overclaims = ["unlimited devices", "sso", "single sign-on", "custom roles", "api access", "white-label"]
    found = [term for term in overclaims if term in text]
    assert found == [], f"page claims capabilities not on the MVP1 checklist: {found}"


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Page content and structure match the approved scope")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-037: No analytics or tracking request is observed during page load or interaction")
@allure.testcase("TC-037")
@pytest.mark.p2
def test_tc037_no_analytics_or_tracking(landing_page: LandingPage):
    tracked: list[str] = []
    landing_page.page.on(
        "request", lambda r: tracked.append(r.url) if ANALYTICS_HOST_PATTERN.search(r.url) else None
    )
    landing_page.open()
    landing_page.click_product_mark()
    if landing_page.is_detail_panel_visible(timeout=1_000):
        landing_page.select_hierarchy_node("Floor 2")
    assert tracked == [], f"analytics/tracking request(s) observed: {tracked}"


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Page content and structure match the approved scope")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC-038: No pricing, documentation, blog, contact-form, or demo-request content is present")
@allure.testcase("TC-038")
@pytest.mark.p2
def test_tc038_no_out_of_scope_content(landing_page: LandingPage):
    landing_page.open()
    text = landing_page.full_page_text().lower()
    for term in ("pricing", "documentation", "blog", "contact us", "request a demo", "book a demo"):
        assert term not in text, f"out-of-scope content found: {term!r}"


@allure.epic("FleetIQ")
@allure.feature("Public landing page")
@allure.story("Page content and structure match the approved scope")
@allure.severity(allure.severity_level.NORMAL)
@allure.title('TC-039: Hero displays "Free while you set up your first fleet. No card required." beneath the CTAs')
@allure.testcase("TC-039")
@pytest.mark.p2
def test_tc039_hero_free_placeholder_line(landing_page: LandingPage):
    landing_page.open()
    assert landing_page.hero_free_line_text() == "Free while you set up your first fleet. No card required."
