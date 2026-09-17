"""EXAMPLE page object — a template showing the Page Object Model pattern.

This is not a real feature. It exists only to show the shape a page object
takes: it extends BasePage, exposes user intent (never mechanics), returns a
page object or plain data from every method, and never asserts — that is the
test's job.

Delete or replace this once the first real feature lands. The naming
convention for a real feature is:

    automation/pages/<feature>_page.py
    automation/locators/<feature>_locators.py
    automation/test_data/<feature>.json
    automation/tests/ui/test_<feature>.py

One feature owns exactly one file per layer.
"""

from __future__ import annotations

import allure

from automation.locators.login_locators import ExampleLocators
from automation.utils.base_page import BasePage


class ExamplePage(BasePage):
    """Template page object. Replace with a real feature page object."""

    path = "/PLACEHOLDER-replace-with-real-path"

    @allure.step("Submit example form as {username}")
    def submit(self, username: str, password: str) -> "ExampleResultPage":
        self.fill(ExampleLocators.USERNAME_INPUT, username, name="username field")
        self.fill(ExampleLocators.PASSWORD_INPUT, password, name="password field", secret=True)
        self.click(ExampleLocators.SUBMIT_BUTTON, name="Submit button")
        return ExampleResultPage(self.page, self.settings)

    def error_message(self) -> str:
        return self.text_of(ExampleLocators.ERROR_MESSAGE)

    def is_error_shown(self, timeout: int = 5_000) -> bool:
        return self.is_visible(ExampleLocators.ERROR_MESSAGE, timeout=timeout)

    def is_loaded(self) -> bool:
        return self.is_visible(ExampleLocators.FORM)


class ExampleResultPage(BasePage):
    """Template result page object. Replace with a real feature page object."""

    path = "/PLACEHOLDER-replace-with-real-path"

    def heading(self) -> str:
        return self.text_of(ExampleLocators.RESULT_HEADING)

    def is_loaded(self, timeout: int = 10_000) -> bool:
        return self.is_visible(ExampleLocators.RESULT_HEADING, timeout=timeout)
