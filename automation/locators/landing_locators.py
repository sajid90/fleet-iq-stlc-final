"""Locators for the public landing page (FLTIQ-62).

Selector priority (constitution VII): get_by_role -> get_by_label ->
data-testid -> CSS. Landmark/section scopes below are CSS (the page has no
data-testid hooks yet - B7/research.md R6 already raised that as a
testability request to development); every element *within* a scope is then
located by role/text, never by a hashed MUI classname.

Scope selectors are structural (HTML5 landmark tags, `id`, `aria-label`) so
they survive a CSS-module class-hash rebuild. Confirmed against the actual
rendered DOM, not just the design mockup - see plan.md B7's own warning that
the real DOM may differ from the Claude Design prototype.
"""

class LandingLocators:
    # -- landmark scopes (CSS, structural) -----------------------------------
    HEADER = "header"
    HERO_SECTION = "section#top"
    CAPABILITIES_SECTION = 'section[aria-label="Capabilities"]'
    HIERARCHY_SECTION = 'section[aria-label="Hierarchy example"]'
    CLOSING_SECTION = 'section[aria-label="Get started"]'
    FOOTER = "footer"

    # -- accessible names (role + name) --------------------------------------
    PRODUCT_MARK_NAME = "FleetIQ"
    NAV_CAPABILITIES_NAME = "Capabilities"
    NAV_HIERARCHY_NAME = "Hierarchy"
    SIGN_IN_NAME = "Sign in"
    BACK_TO_TOP_NAME = "Back to top"
    # Exact static string per constitution VII.a - no wildcard/regex for a
    # known, spec-defined label, same as SIGN_IN_NAME below. Locating call
    # sites pass exact=True. Note the trade-off this reverses: if the build
    # ever ships a wrong label again (e.g. "Create an account"), a click
    # against this locator now fails as "element not found" rather than
    # succeeding and letting TC-029/030/033 report the copy defect on its
    # own - i.e. a label typo now surfaces as a routing-test failure too.
    CREATE_ACCOUNT_NAME = "Create account"

    # -- capability cards ------------------------------------------------------
    CAPABILITIES_GRID = 'section[aria-label="Capabilities"] > div'
    CAPABILITY_CARD = 'section[aria-label="Capabilities"] > div > div'
    HIERARCHY_PANEL = 'section[aria-label="Hierarchy example"] pre'

    # -- hierarchy explorer ----------------------------------------------------
    # The real build renders the tree as static `<pre>` text (no <button>,
    # no aria-pressed - see plan.md B7 / the Completion Report's defect
    # list). These CSS locators are the best available fallback per
    # constitution VII's own documented case for it; a per-node data-testid
    # was already requested from development (research.md R6) and remains
    # outstanding.
    HIERARCHY_TREE = f"{HIERARCHY_SECTION} pre"
    HIERARCHY_ROW = f"{HIERARCHY_SECTION} pre > div"
    # The tree's own header line (design: "XYZ — organisation"), the first
    # child of the <pre> block and structurally distinct from a node row —
    # it carries no node label and is never a click target.
    HIERARCHY_ORG_LABEL = f"{HIERARCHY_SECTION} pre > div:first-child"
    # Detail panel fields the design specifies but the current build has not
    # implemented (no detail panel exists in the DOM at all). Referenced via
    # the data-testid names already requested in research.md R6 so the
    # locators are ready the moment development adds them, rather than
    # guessing at a CSS shape that doesn't exist yet.
    DETAIL_PANEL_DEVICES = '[data-testid="hierarchy-detail-devices"]'
    DETAIL_PANEL_TYPE = '[data-testid="hierarchy-detail-type"]'
    DETAIL_PANEL_SOURCE = '[data-testid="hierarchy-detail-source"]'
    DETAIL_PANEL_NOTE = '[data-testid="hierarchy-detail-note"]'
    DETAIL_PANEL_STATUS = '[data-testid="hierarchy-detail-status"]'
    DETAIL_PANEL_LABEL = '[data-testid="hierarchy-detail-label"]'
