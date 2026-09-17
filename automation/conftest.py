"""Global pytest fixtures for the FleetIQ automation suite.

Built on top of `pytest-playwright`, which already provides the `browser`,
`context` and `page` fixtures plus the `--browser` / `--headed` / `--base-url`
options. This file holds only fixtures and hooks that apply to *every* test,
UI or API — anything browser-specific (timeouts) or page-object-specific
(login_page, etc.) lives in `automation/tests/ui/conftest.py` or a more
specific subfolder's conftest, never here. This file adds:

  * `settings`           — environment-driven config (automation/utils/config.py)
  * context defaults     — viewport, locale, HTTPS handling
  * failure evidence     — screenshot, DOM and console log attached to Allure
  * Allure environment   — so every report records where it ran
"""

from __future__ import annotations

from pathlib import Path

import allure
import pytest

from automation.utils.config import PROJECT_ROOT, Settings, get_settings

ALLURE_RESULTS = PROJECT_ROOT / "reports" / "allure-results"
ARTIFACTS_DIR = PROJECT_ROOT / "reports" / "test-artifacts"


# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="session")
def base_url(request: pytest.FixtureRequest, settings: Settings) -> str | None:
    """Prefer an explicit --base-url, fall back to BASE_URL from the environment."""
    return request.config.getoption("base_url", default=None) or settings.base_url or None


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, settings: Settings) -> dict:
    """Extend pytest-playwright's context defaults instead of replacing them."""
    return {
        **browser_context_args,
        "viewport": settings.viewport,
        "ignore_https_errors": True,
        "locale": "en-US",
    }


# --------------------------------------------------------------------------
# Path-derived markers
# --------------------------------------------------------------------------

def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Apply `ui`/`api` from directory, so the marker can never drift from
    where a test actually lives — no need to tag every test by hand."""
    for item in items:
        parts = item.path.parts
        if "ui" in parts:
            item.add_marker(pytest.mark.ui)
        elif "api" in parts:
            item.add_marker(pytest.mark.api)


# --------------------------------------------------------------------------
# Failure evidence
# --------------------------------------------------------------------------

_EVIDENCE_ATTR = "_fleetiq_evidence"


@pytest.fixture(autouse=True)
def _capture_evidence(request: pytest.FixtureRequest):
    """Wire up console capture and expose the live page to the failure hook.

    Only engages for tests that actually use a browser — API tests never pay
    the cost of launching one.
    """
    console: list[str] = []
    page = None

    if "page" in request.fixturenames:
        try:
            page = request.getfixturevalue("page")
        except Exception:  # browser could not start — the test failure will say why
            page = None

    if page is not None:
        page.on("console", lambda msg: console.append(f"[{msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: console.append(f"[pageerror] {err}"))

    setattr(request.node, _EVIDENCE_ATTR, (page, console))
    yield
    # Attaching happens in pytest_runtest_call, not here: artifacts attached
    # during fixture teardown bind to the teardown container and get buried
    # under "Tear down" in the Allure report instead of showing on the failure.


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item: pytest.Item):
    """Attach failure evidence while the Allure test result is still the active context."""
    outcome = yield
    if outcome.excinfo is None:
        return

    page, console = getattr(item, _EVIDENCE_ATTR, (None, []))
    if page is None:
        return

    try:
        allure.attach(
            page.screenshot(full_page=True),
            name="failure-screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception as exc:
        allure.attach(str(exc), name="screenshot-failed", attachment_type=allure.attachment_type.TEXT)

    try:
        allure.attach(page.content(), name="page-dom", attachment_type=allure.attachment_type.HTML)
        allure.attach(page.url, name="page-url", attachment_type=allure.attachment_type.TEXT)
    except Exception:
        pass

    if console:
        allure.attach(
            "\n".join(console), name="browser-console", attachment_type=allure.attachment_type.TEXT
        )

    allure.attach(
        f"Playwright trace and video (when the run enabled them) are written to:\n{ARTIFACTS_DIR}\n"
        f"View a trace with:  playwright show-trace <path-to-trace.zip>",
        name="artifact-location",
        attachment_type=allure.attachment_type.TEXT,
    )


# --------------------------------------------------------------------------
# Allure environment metadata
# --------------------------------------------------------------------------

def pytest_sessionstart(session: pytest.Session) -> None:
    """Record where the run happened so a report is interpretable months later."""
    settings = get_settings()
    ALLURE_RESULTS.mkdir(parents=True, exist_ok=True)
    browser = session.config.getoption("browser", default=None) or [settings.browser]
    properties = {
        "Environment": settings.environment,
        "Base.URL": settings.base_url or "(not set)",
        "Browser": ",".join(browser) if isinstance(browser, (list, tuple)) else str(browser),
        "Headless": str(not session.config.getoption("headed", default=False)),
        "Viewport": f"{settings.viewport_width}x{settings.viewport_height}",
    }
    (ALLURE_RESULTS / "environment.properties").write_text(
        "\n".join(f"{k}={v}" for k, v in properties.items()), encoding="utf-8"
    )


def pytest_report_header(config: pytest.Config) -> list[str]:
    settings = get_settings()
    return [
        f"fleetiq: env={settings.environment} base_url={settings.base_url or '(not set)'} "
        f"timeout={settings.default_timeout}ms"
    ]
