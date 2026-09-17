#!/usr/bin/env bash
# Execute the automation suite and produce an Allure report.
# STLC Phase 5 helper, invoked by /speckit-test.

set -euo pipefail

SCRIPT_DIR="$(CDPATH="" cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(CDPATH="" cd "$SCRIPT_DIR/../../.." && pwd)"

MARKERS=""
TEST_PATH=""
BROWSER=""
HEADED=false
PARALLEL=""
RERUNS=""
SERVE=false
GENERATE=true
JSON_MODE=false
EXTRA_ARGS=()

usage() {
    cat <<'USAGE'
Usage: run-tests.sh [OPTIONS] [-- extra pytest args]

OPTIONS:
  -m, --markers EXPR    pytest marker expression (e.g. "smoke", "p1 and not slow")
  -k, --path PATH       Limit to a test path or node id
  -b, --browser NAME    chromium | firefox | webkit  (default: from .env / chromium)
      --headed          Run with a visible browser
  -n, --parallel N      Run with pytest-xdist (e.g. 4, or "auto")
      --reruns N        Retry failed tests N times (flake triage only)
      --no-report       Skip Allure HTML generation (results are still written)
      --serve           Open the Allure report in a browser after generating
      --json            Emit a machine-readable summary line
  -h, --help            Show this help

EXAMPLES:
  ./run-tests.sh -m smoke
  ./run-tests.sh -m p1 -b firefox -n auto
  ./run-tests.sh -k automation/tests/ui/test_<feature>.py --headed
USAGE
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -m|--markers)  MARKERS="${2:?--markers requires a value}"; shift 2 ;;
        -k|--path)     TEST_PATH="${2:?--path requires a value}"; shift 2 ;;
        -b|--browser)  BROWSER="${2:?--browser requires a value}"; shift 2 ;;
        --headed)      HEADED=true; shift ;;
        -n|--parallel) PARALLEL="${2:?--parallel requires a value}"; shift 2 ;;
        --reruns)      RERUNS="${2:?--reruns requires a value}"; shift 2 ;;
        --no-report)   GENERATE=false; shift ;;
        --serve)       SERVE=true; shift ;;
        --json)        JSON_MODE=true; shift ;;
        -h|--help)     usage; exit 0 ;;
        --)            shift; EXTRA_ARGS+=("$@"); break ;;
        *)             echo "ERROR: unknown option '$1' (use -- to pass args to pytest)" >&2; exit 1 ;;
    esac
done

cd "$REPO_ROOT"

RESULTS_DIR="$REPO_ROOT/reports/allure-results"
REPORT_DIR="$REPO_ROOT/reports/allure-report"
mkdir -p "$RESULTS_DIR"

# --- Preflight -------------------------------------------------------------
if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 not found" >&2; exit 1
fi
if ! python3 -c "import pytest" >/dev/null 2>&1; then
    echo "ERROR: pytest is not installed. Run: pip install -r requirements.txt" >&2; exit 1
fi
if ! python3 -c "import allure_pytest" >/dev/null 2>&1; then
    echo "ERROR: allure-pytest is not installed. Run: pip install -r requirements.txt" >&2; exit 1
fi
if [[ -n "$PARALLEL" ]] && ! python3 -c "import xdist" >/dev/null 2>&1; then
    echo "ERROR: --parallel needs pytest-xdist. Run: pip install -r requirements.txt" >&2; exit 1
fi

# --- Build the pytest invocation -------------------------------------------
PYTEST_ARGS=("--alluredir=$RESULTS_DIR" "--clean-alluredir")
[[ -n "$TEST_PATH" ]] && PYTEST_ARGS+=("$TEST_PATH")
[[ -n "$MARKERS"   ]] && PYTEST_ARGS+=("-m" "$MARKERS")
[[ -n "$BROWSER"   ]] && PYTEST_ARGS+=("--browser" "$BROWSER")
[[ "$HEADED" == true ]] && PYTEST_ARGS+=("--headed")
[[ -n "$PARALLEL"  ]] && PYTEST_ARGS+=("-n" "$PARALLEL")
[[ -n "$RERUNS"    ]] && PYTEST_ARGS+=("--reruns" "$RERUNS")
[[ ${#EXTRA_ARGS[@]} -gt 0 ]] && PYTEST_ARGS+=("${EXTRA_ARGS[@]}")

echo "Running: pytest ${PYTEST_ARGS[*]}"
echo "----------------------------------------------------------------------"

set +e
python3 -m pytest "${PYTEST_ARGS[@]}"
PYTEST_EXIT=$?
set -e

echo "----------------------------------------------------------------------"

# --- Allure report ----------------------------------------------------------
REPORT_STATUS="skipped"
if [[ "$GENERATE" == true ]]; then
    if command -v allure >/dev/null 2>&1; then
        allure generate "$RESULTS_DIR" -o "$REPORT_DIR" --clean >/dev/null
        REPORT_STATUS="generated"
        echo "Allure report: $REPORT_DIR/index.html"
        if [[ "$SERVE" == true ]]; then
            allure open "$REPORT_DIR" &
        fi
    else
        REPORT_STATUS="allure-cli-missing"
        echo "NOTE: the 'allure' CLI is not on PATH, so no HTML report was generated." >&2
        echo "      Raw results are in: $RESULTS_DIR" >&2
        echo "      Install it with one of:" >&2
        echo "        npm install -g allure-commandline" >&2
        echo "        brew install allure" >&2
        echo "        # or download from https://github.com/allure-framework/allure2/releases" >&2
    fi
fi

# --- Summary ----------------------------------------------------------------
case "$PYTEST_EXIT" in
    0) VERDICT="all tests passed" ;;
    1) VERDICT="tests failed" ;;
    2) VERDICT="execution interrupted" ;;
    3) VERDICT="internal error" ;;
    4) VERDICT="pytest usage error" ;;
    5) VERDICT="no tests collected" ;;
    *) VERDICT="pytest exited with $PYTEST_EXIT" ;;
esac

if [[ "$JSON_MODE" == true ]]; then
    printf '{"PYTEST_EXIT":%d,"VERDICT":"%s","RESULTS_DIR":"%s","REPORT_DIR":"%s","REPORT_STATUS":"%s"}\n' \
        "$PYTEST_EXIT" "$VERDICT" "$RESULTS_DIR" "$REPORT_DIR" "$REPORT_STATUS"
else
    echo "Result: $VERDICT (pytest exit $PYTEST_EXIT)"
fi

exit "$PYTEST_EXIT"
