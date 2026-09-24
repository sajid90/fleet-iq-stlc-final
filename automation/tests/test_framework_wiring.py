"""Framework self-check — no browser, no .env, no product under test.

Confirms the framework's own wiring (settings, test-data loading, the
Page Object Model base) is intact. If this fails, the framework itself is
broken, not a product under test. It exists so a clean clone always has at
least one green test before the first real feature lands.
"""

from __future__ import annotations

import pytest

from automation.utils.base_page import BasePage
from automation.utils.config import get_settings
from automation.utils.data_loader import load_json


@pytest.mark.smoke
def test_framework_wiring() -> None:
    settings = get_settings()
    assert settings.browser
    assert settings.default_timeout > 0

    # data_loader resolves a real feature's fixture under test_data/ and
    # returns its parsed content — proven against actual data, not a
    # template placeholder, so this stays valid however many features land.
    fixture = load_json("landing.json")
    assert fixture["nodes"]

    # BasePage exposes the Page Object Model contract every real page object
    # will extend — checked by introspection, since this test opens no browser.
    for method in ("open", "click", "fill", "text_of", "is_visible"):
        assert hasattr(BasePage, method), f"BasePage is missing '{method}'"
