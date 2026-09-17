"""Load static test data from automation/test_data.

Test data is versioned JSON so a case's inputs are reviewable in a diff.
Never put real customer data or credentials in these files — real values
come from the environment (.env). `filename` may be a relative path to reach
a feature's own fixtures, e.g. get_user("example_user", filename="<feature>.json").
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from automation.utils.config import DATA_DIR


@lru_cache(maxsize=None)
def _read_text(filename: str) -> str:
    """Cache the raw file text, not the parsed object.

    Caching a parsed dict would hand every caller the same mutable object —
    one test mutating a loaded persona would corrupt every later test,
    order-dependently and invisibly under `-n auto`.
    """
    path = DATA_DIR / filename
    if not path.is_file():
        directory = path.parent
        available = ", ".join(sorted(p.name for p in directory.glob("*.json"))) or "none"
        raise FileNotFoundError(f"test data file not found: {path} (available in {directory}: {available})")
    return path.read_text(encoding="utf-8")


def load_json(filename: str) -> Any:
    return json.loads(_read_text(filename))


def get_user(alias: str, filename: str = "users.json") -> dict[str, str]:
    """Look up a named test persona, e.g. get_user("example_user")."""
    users = load_json(filename)
    if alias not in users:
        raise KeyError(f"unknown user alias {alias!r}; known aliases: {sorted(users)}")
    return users[alias]
