"""Page Object Model base class.

Contract (constitution principle V):
  - Page objects expose *user intent*, not mechanics.
  - They return page objects or plain data — they never assert.
  - Every interaction is an Allure step so the report reads like a manual script.
  - Playwright auto-waiting and web-first assertions only. `time.sleep` is banned.
"""

from __future__ import annotations

from typing import Any

import allure
from playwright.sync_api import Locator, Page

from automation.utils.config import Settings
from automation.utils.logger import get_logger


class BasePage:
    """Shared behaviour for every page object."""

    #: Path appended to base_url by :meth:`open`. Override in subclasses.
    path: str = "/"

    def __init__(self, page: Page, settings: Settings) -> None:
        self.page = page
        self.settings = settings
        self.log = get_logger(type(self).__name__)

    # -- navigation ---------------------------------------------------------

    def open(self, url: str | None = None) -> "BasePage":
        """Navigate to this page. Pass `url` to override (e.g. a file:// fixture)."""
        target = url or f"{self.settings.base_url}{self.path}"
        if not target:
            raise RuntimeError(
                f"{type(self).__name__}.open() has no URL: BASE_URL is unset and no "
                "explicit url was passed."
            )
        with allure.step(f"Open {target}"):
            self.log.info("navigating to %s", target)
            self.page.goto(target, wait_until="domcontentloaded")
        return self

    def current_url(self) -> str:
        return self.page.url

    def title(self) -> str:
        return self.page.title()

    # -- element access -----------------------------------------------------

    def find(self, selector: str) -> Locator:
        """Resolve a selector to a Locator. Prefer the semantic helpers below."""
        return self.page.locator(selector)

    def by_test_id(self, test_id: str) -> Locator:
        return self.page.get_by_test_id(test_id)

    def by_role(self, role: str, name: str | None = None, **kwargs: Any) -> Locator:
        return self.page.get_by_role(role, name=name, **kwargs)  # type: ignore[arg-type]

    def by_label(self, text: str, **kwargs: Any) -> Locator:
        return self.page.get_by_label(text, **kwargs)

    def by_text(self, text: str, **kwargs: Any) -> Locator:
        """For elements with no accessible role/label bound to them."""
        return self.page.get_by_text(text, **kwargs)

    # -- interactions -------------------------------------------------------

    def click(self, target: str | Locator, name: str | None = None) -> None:
        locator = self._resolve(target)
        with allure.step(f"Click {name or self._describe(target)}"):
            locator.click()

    def fill(self, target: str | Locator, value: str, name: str | None = None,
             secret: bool = False) -> None:
        locator = self._resolve(target)
        shown = "********" if secret else value
        with allure.step(f"Enter {shown!r} into {name or self._describe(target)}"):
            locator.fill(value)

    def select_option(self, target: str | Locator, value: str, name: str | None = None) -> None:
        locator = self._resolve(target)
        with allure.step(f"Select {value!r} in {name or self._describe(target)}"):
            locator.select_option(value)

    def check(self, target: str | Locator, name: str | None = None) -> None:
        locator = self._resolve(target)
        with allure.step(f"Check {name or self._describe(target)}"):
            locator.check()

    def press(self, target: str | Locator, key: str, name: str | None = None) -> None:
        locator = self._resolve(target)
        with allure.step(f"Press {key} on {name or self._describe(target)}"):
            locator.press(key)

    # -- state queries (return data; the test does the asserting) -----------

    def text_of(self, target: str | Locator) -> str:
        return (self._resolve(target).inner_text() or "").strip()

    def value_of(self, target: str | Locator) -> str:
        return self._resolve(target).input_value()

    def attribute_of(self, target: str | Locator, attribute: str) -> str | None:
        return self._resolve(target).get_attribute(attribute)

    def is_visible(self, target: str | Locator, timeout: int | None = None) -> bool:
        """True if the element becomes visible within the timeout, else False.

        Use for branching, not for assertions — assert with `expect()` in the test.
        """
        try:
            self._resolve(target).wait_for(
                state="visible", timeout=timeout or self.settings.default_timeout
            )
            return True
        except Exception:  # playwright TimeoutError and friends
            return False

    def count_of(self, target: str | Locator) -> int:
        return self._resolve(target).count()

    def wait_for_url(self, pattern: str, timeout: int | None = None) -> None:
        with allure.step(f"Wait for URL matching {pattern}"):
            self.page.wait_for_url(pattern, timeout=timeout or self.settings.default_timeout)

    # -- evidence -----------------------------------------------------------

    def attach_screenshot(self, name: str = "screenshot") -> None:
        allure.attach(
            self.page.screenshot(full_page=True),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )

    # -- internals ----------------------------------------------------------

    def _resolve(self, target: str | Locator) -> Locator:
        return self.page.locator(target) if isinstance(target, str) else target

    @staticmethod
    def _describe(target: str | Locator) -> str:
        return target if isinstance(target, str) else repr(target)
