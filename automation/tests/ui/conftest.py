"""Fixtures shared by every browser-driven UI test.

pytest registers a conftest for items at or below its directory, so fixtures
defined here are visible to every test under `tests/ui/`. Register a new
feature's page-object fixture here — never in the root `automation/conftest.py`,
which holds only global, browser-agnostic fixtures.
"""

from __future__ import annotations

import pytest
from playwright.sync_api import expect

from automation.pages.landing_page import LandingPage
from automation.utils.config import Settings


# --------------------------------------------------------------------------
# Browser-only fixtures
# --------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _apply_timeouts(page, settings: Settings) -> None:
    """One place to set waiting behaviour — no per-test timeout constants.

    Playwright's `expect()` assertion timeout is tracked separately from the
    action/navigation timeouts above and otherwise silently defaults to
    5000ms regardless of DEFAULT_TIMEOUT — too tight for a live, externally
    hosted environment under load. Align it here so every `expect()` call in
    the suite honours the same configured budget.

    Deliberately scoped to `tests/ui/` rather than the root conftest: it is
    `autouse=True` and requests `page` directly, so it would launch a browser
    for every API test if it lived at the automation root.
    """
    page.set_default_timeout(settings.default_timeout)
    page.set_default_navigation_timeout(settings.default_timeout)
    expect.set_options(timeout=settings.default_timeout)


# --------------------------------------------------------------------------
# FLTIQ-62 — public landing page
# --------------------------------------------------------------------------

@pytest.fixture
def landing_page(page, settings: Settings) -> LandingPage:
    return LandingPage(page, settings)
