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

from automation.utils.config import PROJECT_ROOT, REPORTS_DIR, Settings, get_settings

ALLURE_RESULTS = REPORTS_DIR / "allure-results"
ARTIFACTS_DIR = REPORTS_DIR / "test-artifacts"


# --------------------------------------------------------------------------
# Report paths
# --------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """Resolve relative report paths against the repo root, not the cwd.

    `pytest.ini`'s `--alluredir`/`--output` are relative, and the option
    parser resolves them against the *current working directory*. Running
    `pytest` from inside `automation/` would otherwise scatter results into
    `automation/automation/reports/` and silently produce a partial Allure
    report. Absolute paths (what `run-tests.sh` passes) are left untouched.

    `tryfirst` matters: allure-pytest reads `allure_report_dir` in its own
    `pytest_configure`, and as an entry-point plugin it is registered before
    this conftest.
    """
    for option_name in ("allure_report_dir", "output"):
        value = getattr(config.option, option_name, None)
        if value and not Path(value).is_absolute():
            setattr(config.option, option_name, str(PROJECT_ROOT / value))

    _validate_maximize_options(config)


def _validate_maximize_options(config: pytest.Config) -> None:
    """Warn when `--no-maximize` was passed to a run that has no window.

    Headless never maximizes — it always uses VIEWPORT_WIDTH/HEIGHT — so the
    flag is a silent no-op there. Saying so beats letting someone believe
    they changed the viewport when they did not.
    """
    if config.getoption("maximize", default=None) is not False:
        return
    if config.getoption("headed", default=False):
        return
    if not get_settings().headless:
        return  # headed via HEADLESS=false, so the flag is meaningful

    config.issue_config_time_warning(
        pytest.PytestConfigWarning(
            "--no-maximize has no effect on a headless run: headless never "
            "maximizes and always uses VIEWPORT_WIDTH/HEIGHT. Add --headed "
            "(or set HEADLESS=false) if you meant to watch a browser window."
        ),
        stacklevel=2,
    )


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


def pytest_addoption(parser: pytest.Parser) -> None:
    """CLI opt-out for the env-driven maximize setting (the CLI wins).

    A `--headed` run maximizes by default (MAXIMIZE in .env), so the only
    flag needed is the bypass. There is deliberately no `--maximize`: it
    would just restate the default.
    """
    parser.getgroup("fleetiq").addoption(
        "--no-maximize",
        action="store_false",
        dest="maximize",
        default=None,
        help="Keep the fixed VIEWPORT_WIDTH/HEIGHT viewport on a --headed run "
             "instead of maximizing. Overrides MAXIMIZE in .env.",
    )


def _maximize_enabled(settings: Settings, config: pytest.Config, headless: bool) -> bool:
    """Resolve the effective maximize setting for this run.

    `--no-maximize` beats the environment; the option defaults to None (not
    passed) rather than a boolean, so an unset flag stays distinguishable
    from an explicit `--no-maximize`.

    MAXIMIZE is required only when it can actually change something. A
    headless run never maximizes, so an unset value there is irrelevant, not
    an error — demanding it anyway would contradict "headless ignores it".
    """
    override = config.getoption("maximize", default=None)
    if override is not None:
        return bool(override)
    if headless:
        return False  # never applies; the value is moot for this run
    if settings.maximize is None:
        raise RuntimeError(
            "MAXIMIZE is not set, and this is a headed run where it decides "
            "whether the browser window is maximized. Set MAXIMIZE in .env "
            "(cp .env.example .env), or pass --no-maximize for this run."
        )
    return settings.maximize


@pytest.fixture(scope="session")
def browser_type_launch_args(
    browser_type_launch_args: dict, settings: Settings, pytestconfig: pytest.Config
) -> dict:
    """Apply HEADLESS / SLOW_MO from the environment, plus --start-maximized.

    pytest-playwright populates `headless`/`slow_mo` here only when `--headed`
    (or `HEADED=1`) and `--slowmo` are passed, otherwise leaving Playwright's
    own defaults — so `HEADLESS` and `SLOW_MO` were previously read into
    `Settings` and never actually used. `setdefault` fills them from `.env`
    while leaving any CLI-supplied value untouched, so command-line flags still
    win exactly as `.env`'s own comment promises.

    MAXIMIZE is on by default but headed-only: headless has no window to
    maximize, so it keeps the fixed VIEWPORT_WIDTH/HEIGHT viewport, which is
    what keeps layout assertions reproducible across machines and in CI
    (constitution VI).
    """
    args = {**browser_type_launch_args}
    args.setdefault("headless", settings.headless)
    if settings.slow_mo:
        args.setdefault("slow_mo", settings.slow_mo)

    if _maximize_enabled(settings, pytestconfig, args["headless"]):
        selected = pytestconfig.getoption("browser", default=None) or ["chromium"]
        if "chromium" in selected:  # Chrome-only flag; others ignore/reject it
            args["args"] = [*args.get("args", []), "--start-maximized"]
    return args


@pytest.fixture(scope="session")
def browser_context_args(
    browser_context_args: dict,
    settings: Settings,
    pytestconfig: pytest.Config,
    browser_type_launch_args: dict,
) -> dict:
    """Extend pytest-playwright's context defaults instead of replacing them.

    Headedness is read back off the resolved launch args rather than
    recomputed, so `--headed` and `HEADLESS=false` behave identically here.
    """
    args = {
        **browser_context_args,
        "viewport": settings.viewport,
        "ignore_https_errors": True,
        "locale": "en-US",
    }
    if _maximize_enabled(
        settings, pytestconfig, browser_type_launch_args.get("headless", True)
    ):
        # Playwright rejects viewport and no_viewport together. Dropping the
        # fixed viewport lets the page fill the real window; a test that calls
        # page.set_viewport_size() still overrides this for its own duration,
        # so the responsive cases (TC-021/022/026/041) are unaffected.
        args.pop("viewport", None)
        args["no_viewport"] = True
    return args


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
