"""EXAMPLE locators — a template showing the locator-layer pattern.

This is not a real feature. Selector priority (constitution principle V):
    get_by_role  >  get_by_label  >  data-testid  >  CSS
XPath only as a last resort, with a comment explaining why.

Keeping locators here (never inline in a page object or a test) means a UI
change is a one-file edit. Delete or replace this once the first real feature
lands — see automation/pages/login_page.py for the naming convention.
"""


class ExampleLocators:
    # Placeholders — replace with real selectors for the actual feature,
    # preferring get_by_role/get_by_label where the UI has one.
    USERNAME_INPUT = "[data-testid='PLACEHOLDER-username']"
    PASSWORD_INPUT = "[data-testid='PLACEHOLDER-password']"
    SUBMIT_BUTTON = "[data-testid='PLACEHOLDER-submit']"
    ERROR_MESSAGE = "[data-testid='PLACEHOLDER-error-message']"
    FORM = "[data-testid='PLACEHOLDER-form']"
    RESULT_HEADING = "[data-testid='PLACEHOLDER-result-heading']"
