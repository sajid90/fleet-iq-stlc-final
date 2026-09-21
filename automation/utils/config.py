"""Environment-driven configuration.

Every value comes from the environment (`.env` locally, secret store in CI).
Nothing sensitive is ever hard-coded here — see constitution principle
"Data & Security Standards".
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

AUTOMATION_ROOT = Path(__file__).resolve().parents[1]  # .../automation
PROJECT_ROOT = AUTOMATION_ROOT.parent  # repo root
DATA_DIR = AUTOMATION_ROOT / "test_data"
REPORTS_DIR = AUTOMATION_ROOT / "reports"  # generated output — gitignored


def _bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _optional_bool(name: str) -> bool | None:
    """Read a boolean that has no in-code default — `None` when unset.

    Nothing is substituted here, so `.env` stays the single source of truth,
    but the value is also not *demanded* at import time. The caller decides
    whether it is actually needed: see `_maximize_enabled` in
    `automation/conftest.py`, which requires MAXIMIZE only for a headed run,
    since a headless run never maximizes and the value is moot.
    """
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return None
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer, got {raw!r}") from exc


@dataclass(frozen=True)
class Settings:
    """Resolved run configuration."""

    base_url: str
    environment: str
    browser: str
    headless: bool
    slow_mo: int
    default_timeout: int
    viewport_width: int
    viewport_height: int
    maximize: bool | None  # None when MAXIMIZE is unset; only needed if headed
    username: str | None
    password: str | None

    @property
    def viewport(self) -> dict[str, int]:
        return {"width": self.viewport_width, "height": self.viewport_height}

    def require_credentials(self) -> tuple[str, str]:
        """Fail loudly rather than testing with empty credentials."""
        if not self.username or not self.password:
            raise RuntimeError(
                "TEST_USERNAME / TEST_PASSWORD are not set. "
                "Copy .env.example to .env and fill them in."
            )
        return self.username, self.password


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    load_dotenv(PROJECT_ROOT / ".env", override=False)
    return Settings(
        base_url=os.getenv("BASE_URL", "").rstrip("/"),
        environment=os.getenv("TEST_ENV", "local"),
        browser=os.getenv("BROWSER", "chromium"),
        headless=_bool("HEADLESS", True),
        slow_mo=_int("SLOW_MO", 0),
        default_timeout=_int("DEFAULT_TIMEOUT", 10_000),
        viewport_width=_int("VIEWPORT_WIDTH", 1920),
        viewport_height=_int("VIEWPORT_HEIGHT", 1080),
        maximize=_optional_bool("MAXIMIZE"),
        username=os.getenv("TEST_USERNAME") or None,
        password=os.getenv("TEST_PASSWORD") or None,
    )
