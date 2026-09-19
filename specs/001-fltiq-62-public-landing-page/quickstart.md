# Quickstart: FLTIQ-62 — Build the public landing page

How to run this feature's suite once it exists (`/speckit-implement` writes
the actual test files this refers to — this document describes how to run
them, not their content).

## Prerequisites

- Python 3.10+ (per `requirements.txt`'s header comment)
- `pip install -r requirements.txt`
- `playwright install --with-deps chromium` (add `firefox webkit` too if
  running the full cross-browser matrix locally)
- Allure CLI, for the HTML report: `npm install -g allure-commandline`

## Environment configuration

Copy `.env.example` to `.env` and fill in:

| Key | Required for this feature | Notes |
|---|---|---|
| `BASE_URL` | Yes | The landing page is served at the root of this URL |
| `TEST_ENV` | Yes (informational) | Recorded in the Allure environment block |
| `TEST_USERNAME` / `TEST_PASSWORD` | Yes, for Scenario 2 only | A purpose-created, least-privileged QA account with an existing tenant — used to sign in via the real sign-in screen (FLTIQ-35) before testing the authenticated-redirect behavior. Every other scenario runs with no session at all. |
| `BROWSER` / `HEADLESS` / `VIEWPORT_WIDTH` / `VIEWPORT_HEIGHT` | No | Framework defaults (1920×1080, headless Chromium) match this feature's desktop test viewport (research.md R1); no override needed |
| `API_BASE_URL` | No | This feature has no API surface; leave commented out |

No other secrets are needed — the hierarchy explorer's data is a static
fixture bundled with the test suite (`automation/test_data/landing.json`),
not fetched from anywhere.

## Running the suite

All commands use `.specify/scripts/bash/run-tests.sh` from the repo root.

```bash
# Framework self-check (always run this first on a fresh clone)
.specify/scripts/bash/run-tests.sh -k automation/tests/test_framework_wiring.py

# Smoke subset for this feature (once /speckit-implement lands it)
.specify/scripts/bash/run-tests.sh -m smoke -k automation/tests/ui/test_landing.py

# Full landing-page suite, headed (visible browser), for local debugging
.specify/scripts/bash/run-tests.sh -k automation/tests/ui/test_landing.py --headed

# A single test case by name
.specify/scripts/bash/run-tests.sh -k "automation/tests/ui/test_landing.py::test_tc001_unauthenticated_visitor_sees_landing_page"

# Full landing-page suite across the browser triad, in parallel
.specify/scripts/bash/run-tests.sh -k automation/tests/ui/test_landing.py -b firefox -n auto
```

## Opening the Allure report

```bash
.specify/scripts/bash/run-tests.sh -k automation/tests/ui/test_landing.py --serve
```

Opens the generated HTML report in a browser. On any failure, the report
carries a screenshot, the page's DOM, its URL, and the browser console log —
already wired globally in `automation/conftest.py`, nothing feature-specific
to configure.

## Expected outcome of a healthy run

- `test_framework_wiring.py` always collects and passes, with no `.env` and
  no browser (browserless self-check).
- The landing-page suite: all P1 cases (TR-001, TR-002, TR-004, TR-005,
  TR-008, TR-011, TR-012, TR-013) green. TR-018's line item stays out of the
  suite entirely until `spec.md` §13a Q1 is answered (see `plan.md` §A0
  Blocked requirements register) — its absence is expected, not a gap to
  chase.
- If `TEST_USERNAME`/`TEST_PASSWORD` point to an account whose tenant no
  longer exists, or if FLTIQ-35 (sign-in) is not yet deployed to the target
  environment, the Scenario 2 test reports **skipped**, with the reason
  printed in the test output and the Allure report — not a failure, and not
  silently absent (see `research.md` R5).
