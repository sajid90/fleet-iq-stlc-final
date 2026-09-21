"""Page object for the public landing page (FLTIQ-62).

Exposes user intent and returns data or page objects; every assertion lives
in the test (constitution VII). Destination pages (sign-up, sign-in, home)
belong to FLTIQ-33/35/46's own future page objects - this page's methods
return only the resulting URL for the caller to assert against, per
plan.md B3.
"""

from __future__ import annotations

import allure

from automation.locators.landing_locators import LandingLocators as L
from automation.utils.base_page import BasePage


class LandingPage(BasePage):
    path = "/"

    def open(self, url: str | None = None) -> "LandingPage":
        """Wait past client hydration, not just `domcontentloaded`.

        This is a client-rendered Next.js app: `BasePage.open()`'s
        `domcontentloaded` wait fires before the header/hero JS has
        hydrated, so an action immediately after it can race an empty DOM.
        Waiting for a stable, always-present element (the header's product
        mark) is a test-mechanics fix (INFERRED), not a product change.
        """
        super().open(url)
        self.page.locator(L.HEADER).get_by_role("link", name=L.PRODUCT_MARK_NAME).wait_for(state="visible")
        return self

    # -- header ---------------------------------------------------------------

    @allure.step("Click the FleetIQ product mark in the header")
    def click_product_mark(self) -> None:
        self.click(
            self.page.locator(L.HEADER).get_by_role("link", name=L.PRODUCT_MARK_NAME),
            name="header product mark",
        )

    @allure.step("Click {name} in the header nav")
    def click_header_nav_anchor(self, name: str) -> None:
        self.click(
            self.page.locator(L.HEADER).get_by_role("link", name=name, exact=True),
            name=f"header {name} anchor",
        )

    def header_nav_anchor_count(self, name: str) -> int:
        return self.count_of(self.page.locator(L.HEADER).get_by_role("link", name=name, exact=True))

    def header_cta_order(self) -> list[str]:
        return self._section_cta_order(L.HEADER)

    # -- section-scoped Sign in / Create account -------------------------------

    def _section(self, location: str):
        return {
            "header": L.HEADER,
            "hero": L.HERO_SECTION,
            "closing": L.CLOSING_SECTION,
        }[location]

    def _section_cta_order(self, scope_selector: str) -> list[str]:
        scope = self.page.locator(scope_selector)
        links = scope.get_by_role("link").all()
        names = [link.inner_text().strip() for link in links]
        return [n for n in names if n]

    @allure.step("Click Create account in the {location}")
    def click_create_account(self, location: str) -> None:
        scope = self.page.locator(self._section(location))
        self.click(
            scope.get_by_role("link", name=L.CREATE_ACCOUNT_NAME),
            name=f"{location} Create account",
        )

    @allure.step("Click Sign in in the {location}")
    def click_sign_in(self, location: str) -> None:
        scope = self.page.locator(self._section(location))
        self.click(
            scope.get_by_role("link", name=L.SIGN_IN_NAME, exact=True),
            name=f"{location} Sign in",
        )

    # -- hero -------------------------------------------------------------------

    def hero_badge_text(self) -> str:
        wrapper = self.page.locator(f"{L.HERO_SECTION} > div")
        return self.text_of(wrapper.locator("> div").nth(0))

    def hero_headline_text(self) -> str:
        return self.text_of(self.page.locator(L.HERO_SECTION).get_by_role("heading", level=1))

    def hero_subhead_text(self) -> str:
        wrapper = self.page.locator(f"{L.HERO_SECTION} > div")
        return self.text_of(wrapper.locator("> p").nth(0))

    def hero_free_line_text(self) -> str:
        wrapper = self.page.locator(f"{L.HERO_SECTION} > div")
        return self.text_of(wrapper.locator("> p").nth(1))

    def hero_stats_texts(self) -> list[str]:
        wrapper = self.page.locator(f"{L.HERO_SECTION} > div")
        stats = wrapper.locator("> div").nth(1).locator("> div")
        return [stats.nth(i).inner_text().strip() for i in range(stats.count())]

    def hero_cta_order(self) -> list[str]:
        return self._section_cta_order(L.HERO_SECTION)

    # -- capabilities -------------------------------------------------------------

    def capabilities_heading_text(self) -> str:
        return self.text_of(self.page.locator(L.CAPABILITIES_SECTION).get_by_role("heading", level=2))

    def capability_cards(self) -> list[dict]:
        cards = self.page.locator(L.CAPABILITY_CARD)
        result = []
        for i in range(cards.count()):
            card = cards.nth(i)
            number = card.locator("span").first.inner_text().strip()
            title = card.get_by_role("heading", level=3).inner_text().strip()
            body = card.locator("p").first.inner_text().strip()
            result.append({"number": number, "title": title, "body": body})
        return result

    # -- hierarchy explorer ---------------------------------------------------------

    def hierarchy_heading_text(self) -> str:
        return self.text_of(self.page.locator(L.HIERARCHY_SECTION).get_by_role("heading", level=2))

    def hierarchy_intro_text(self) -> str:
        return self.text_of(self.page.locator(L.HIERARCHY_SECTION).locator("p").first)

    def hierarchy_row(self, label: str):
        return self.page.locator(L.HIERARCHY_ROW).filter(has_text=label)

    def hierarchy_row_meta_text(self, label: str) -> str:
        return self.text_of(self.hierarchy_row(label))

    @allure.step("Select hierarchy node {label}")
    def select_hierarchy_node(self, label: str) -> None:
        self.click(self.hierarchy_row(label), name=f"hierarchy row {label}")

    def hierarchy_row_aria_pressed(self, label: str) -> str | None:
        return self.attribute_of(self.hierarchy_row(label), "aria-pressed")

    def detail_panel_devices(self) -> str:
        return self.text_of(L.DETAIL_PANEL_DEVICES)

    def detail_panel_type(self) -> str:
        return self.text_of(L.DETAIL_PANEL_TYPE)

    def detail_panel_source(self) -> str:
        return self.text_of(L.DETAIL_PANEL_SOURCE)

    def detail_panel_note(self) -> str:
        return self.text_of(L.DETAIL_PANEL_NOTE)

    def detail_panel_status(self) -> str:
        return self.text_of(L.DETAIL_PANEL_STATUS)

    def detail_panel_label(self) -> str:
        return self.text_of(L.DETAIL_PANEL_LABEL)

    def is_detail_panel_visible(self, timeout: int = 5_000) -> bool:
        return self.is_visible(L.DETAIL_PANEL_LABEL, timeout=timeout)

    # -- closing section ---------------------------------------------------------

    def closing_heading_text(self) -> str:
        return self.text_of(self.page.locator(L.CLOSING_SECTION).get_by_role("heading", level=2))

    def closing_body_text(self) -> str:
        return self.text_of(self.page.locator(L.CLOSING_SECTION).locator("p").first)

    def closing_cta_order(self) -> list[str]:
        return self._section_cta_order(L.CLOSING_SECTION)

    # -- footer -------------------------------------------------------------------

    def _mark_icon_text(self, scope_selector: str) -> str:
        """Text inside the square glyph preceding the FleetIQ wordmark.

        TR-003/TR-010 require a square icon *containing "F"*. Returns the
        glyph's own text so the test can assert it; an empty string means the
        square renders with no letter in it.
        """
        mark = self.page.locator(scope_selector).get_by_text("FleetIQ", exact=False).first
        return (mark.locator("div").first.inner_text() or "").strip()

    def header_mark_icon_text(self) -> str:
        return self._mark_icon_text(L.HEADER)

    def footer_mark_icon_text(self) -> str:
        return self._mark_icon_text(L.FOOTER)

    def footer_mark_text(self) -> str:
        return self.text_of(self.page.locator(L.FOOTER).get_by_text("FleetIQ", exact=False))

    def footer_mark_is_link(self) -> bool:
        return self.count_of(self.page.locator(L.FOOTER).get_by_role("link", name=L.PRODUCT_MARK_NAME)) > 0

    def footer_copyright_text(self) -> str:
        return self.text_of(self.page.locator(L.FOOTER))

    @allure.step("Click Back to top in the footer")
    def click_back_to_top(self) -> None:
        self.click(
            self.page.locator(L.FOOTER).get_by_role("link", name=L.BACK_TO_TOP_NAME),
            name="footer Back to top",
        )

    @allure.step("Attempt to click the footer FleetIQ mark")
    def attempt_click_footer_mark(self) -> None:
        self.page.locator(L.FOOTER).get_by_text("FleetIQ", exact=False).first.click()

    def is_back_to_top_visible(self) -> bool:
        return self.is_visible(self.page.locator(L.FOOTER).get_by_role("link", name=L.BACK_TO_TOP_NAME))

    # -- page-wide queries --------------------------------------------------------

    def full_page_text(self) -> str:
        return self.page.locator("body").inner_text()

    def scroll_y(self) -> int:
        return self.page.evaluate("() => window.scrollY")

    def scroll_to_bottom(self) -> None:
        self.page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_function("() => window.scrollY > 0", timeout=self.settings.default_timeout)

    def scrolled_to_top_within(self, timeout: int = 5_000) -> bool:
        """True if the page reaches the top within the timeout, else False.

        Polls the real condition rather than sleeping a fixed amount, which
        proved flaky under parallel load. Returns data instead of raising so
        the test owns the assertion (constitution VII) and a failure reads as
        the test's own message rather than a Playwright timeout stack.
        """
        try:
            self.page.wait_for_function("() => window.scrollY === 0", timeout=timeout)
            return True
        except Exception:  # playwright TimeoutError and friends
            return False

    def is_modal_visible(self, timeout: int = 2_000) -> bool:
        return self.is_visible(self.page.get_by_role("dialog"), timeout=timeout)

    def is_skeleton_loader_visible(self, timeout: int = 2_000) -> bool:
        return self.is_visible(self.page.locator(".MuiSkeleton-root").first, timeout=timeout)
