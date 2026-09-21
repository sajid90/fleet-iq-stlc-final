---
name: "speckit-test"
description: "STLC Phase 5 — Test Execution & Closure. Run the automation suite, report results in Allure, and give a Go/No-Go verdict."
argument-hint: "Optional scope (e.g. 'smoke', 'p1', 'automation/tests/ui/test_login.py', '--browser firefox')"
compatibility: "Requires spec-kit project structure with .specify/ directory and an automation suite under automation/"
metadata:
  author: "github-spec-kit"
  adapted-for: "STLC (Software Testing Life Cycle)"
  stlc-phase: "5 — Test Execution & Cycle Closure"
user-invocable: true
disable-model-invocation: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are performing **STLC Phase 5 — Test Execution and Cycle Closure**. You
run the suite, interpret what happened, and produce a defensible verdict.

**Report what actually happened.** If tests fail, say so and quote the output.
A summary that reads better than the run did is a false report.

**QA perspective, not product design.** Triage against what the test case
says should happen, not against an assumption of what would be nicer. A
failure that reveals real product behaviour is a **product defect** to report
(Step 5) — never a reason to soften the assertion or the verdict.

### Step 1: Resolve scope and context

Determine what to run from the user input:

| Input | Invocation |
|-------|-----------|
| *(empty)* | Full suite |
| `smoke`, `p1`, `regression`… | `-m <marker>` |
| A path or node id | `-k <path>` |
| `--browser firefox` etc. | passed through |

**Step 0 — Convergence gate.** If `tasks.md` has ever recorded a
`## Phase N: Convergence` section, check its most recent findings. A full
execution cycle on an unconverged suite reports symptoms of a known,
unaddressed gap as if they were fresh news. If a CRITICAL or HIGH finding is
still open, halt and say so — run `/speckit-converge` first, or proceed with
`--force-gate` and record the override in the execution report. Skip this
check quietly if `tasks.md` has no convergence section yet (nothing to check).

**Post-approval change check (constitution XIII).** Also check `spec.md` and
`plan.md`'s `## Change Log` sections for a **Scope change**/**New
requirement** entry with no fresh `Approved by`/`Approved on` on or after it.
If found, halt: a Go/No-Go verdict built while an upstream gate stands
bypassed is not defensible evidence, whatever the suite reports.

Then load context (skip quietly if a feature is not yet initialised):

- `.specify/scripts/bash/check-prerequisites.sh --json --paths-only` for `FEATURE_DIR`
- `FEATURE_DIR/test-cases.json` — to map results back to `TC-xxx`
- `FEATURE_DIR/spec.md` — the exit criteria in §10 and requirements for coverage
- `FEATURE_DIR/plan.md` — the quality gate in §B6
- `.specify/memory/constitution.md`

### Step 2: Preflight

Confirm the suite can run before blaming the product for a failure:

```bash
python3 -m pytest --collect-only -q
```

If collection fails, that is an environment or framework problem. Report it as
such — do not present it as a test result. Common causes: dependencies not
installed (`pip install -r requirements.txt`), browsers missing
(`playwright install chromium`), `.env` not configured.

### Step 3: Execute

```bash
.specify/scripts/bash/run-tests.sh [-m MARKER] [-k PATH] [-b BROWSER] [-n auto] --json
```

The script writes Allure results to `reports/allure-results`, generates HTML
into `reports/allure-report` when the `allure` CLI is available, and returns a
JSON summary line with `PYTEST_EXIT`, `VERDICT` and `REPORT_STATUS`.

- `REPORT_STATUS: allure-cli-missing` means results were captured but no HTML
  was built. Tell the user how to install the CLI
  (`npm install -g allure-commandline`) rather than silently skipping it.
- Do **not** add `--reruns` on a normal cycle. Retries are a flake-triage tool
  (Step 5), not a way to turn a red run green.

### Step 4: Read the results

Parse the pytest output and `reports/allure-results/*-result.json` for:

- Totals: passed, failed, skipped, errors, duration
- Per-test status, with each failure's actual error message
- Attachments captured for each failure (screenshot, DOM, console, trace)

Map every result back to its `TC-xxx` using the `@allure.testcase` id or the
test function name, and roll up by priority and by scenario.

**Before rolling up requirement coverage**, confirm each mapped `TC-xxx`
cites at least one `TR-xxx` that actually exists in `spec.md` §3. A result
mapping to no `TR-xxx`, or to one absent from `spec.md`, is an
**orphan/unsupported test** (Step 5) — exclude it from requirement-coverage
rollups. Its pass or fail proves something ran; it proves nothing about
product requirement coverage (constitution I).

### Step 5: Triage every failure

For each failure, decide and record which it is:

| Verdict | Meaning | Action |
|---------|---------|--------|
| **Product defect** | The application behaves wrongly | Raise a defect; keep the test |
| **Test defect** | The test or locator is wrong | Fix the test; do not blame the product |
| **Requirement defect** | The approved requirement/source set is contradictory or untestable | Return to `/speckit-clarify`; do not weaken the test |
| **Environment issue** | Data, config, deployment, network | Fix the environment; re-run and say the result changed |
| **Flaky** | Passes and fails without a code change | Investigate the race; quarantine only with an owner and a ticket |
| **Orphan/unsupported test** | The test's `TC-xxx` has no `TR-xxx`, cites one absent from `spec.md`, or `spec.md` traces that `TR-xxx` to no authoritative source (constitution I) | A process/test-artifact defect, not a product or test-logic defect — its result is reported separately and never counted toward requirement coverage; recommend `/speckit-analyze` (category I) or `/speckit-tasks` to remove or properly trace it |

Never classify a failure as flaky just because a rerun passed — confirm the
non-determinism and name its cause. Never weaken an assertion to clear a
failure.

For each **product defect**, draft a report the team can act on:

- Title, severity (Critical/High/Medium/Low) and priority
- The `TC-xxx` and `TR-xxx` it violates
- Environment and build
- Steps to reproduce, taken from the test case
- Expected vs actual, quoting the assertion output
- Evidence: point at the Allure attachments

If an Atlassian MCP server is connected and the user asks you to file them,
create the Jira issues — **confirm the list with the user before creating
anything**, since that writes to their tracker.

### Step 6: Write the execution report

Use `.specify/templates/test-report-template.md`. Write it to
`FEATURE_DIR/reports/test-report-cycle-<N>.md` (create the directory; `<N>` is
the next cycle number in that folder, starting at 1).

Fill every section: summary counts, results by priority and scenario, each
failure with its triage verdict, defects raised, flaky tests, coverage against
requirements, the exit criteria assessment, and the recommendation.

### Step 7: Update test case status

In `FEATURE_DIR/test-cases.json`, record this cycle's outcome on each executed
case by setting `last_result` to `Pass`, `Fail`, `Blocked` or `Skipped` and
`last_run` to the run's date **and time** (`YYYY-MM-DDTHH:MM:SS`, from the
actual execution — e.g. the earliest `start` timestamp in this cycle's Allure
results — not just today's date). A bare date cannot distinguish between
multiple cycles run on the same day. **Do not touch the top-level `generated`
field here** — it tracks when the test-case *content* was last written by
`/speckit-tasks` or `/speckit-implement`, not when the suite was last
executed; bumping it on every test run would make it indistinguishable from
`last_run` and lose its meaning. Then regenerate the workbook:

```bash
python3 .specify/scripts/python/export_testcases.py <FEATURE_DIR> --markdown
```

### Step 8: Assess exit criteria and give a verdict

Compare the run against `spec.md` §10 exit criteria and the `plan.md` §B6
quality gate. State each criterion, its target, the actual value, and whether
it was met.

**Requirement coverage counts only executed tests whose `TC-xxx` traces to a
real, source-backed `TR-xxx`** — an orphan/unsupported test's result (Step 5)
is reported separately and never inflates the coverage percentage, even if it
passed. A Go verdict built on inflated coverage is not defensible evidence.

Then give one verdict:

- **Go** — every exit criterion met
- **No-Go** — a criterion failed; name exactly which and what it would take
- **Conditional Go** — met apart from named, accepted risks; state the
  conditions and who owns them
- **No-Go (requirement)** — a P1 requirement is still classed UNDEFINED, or a
  source conflict affecting a P1 requirement is unresolved. A Go is not
  available in this state: the suite cannot demonstrate a requirement nobody
  has defined. The remedy is `/speckit-clarify`, not another test cycle — which
  is why this is a distinct verdict from a defect-driven No-Go.

The verdict follows from the criteria. Do not soften a No-Go because the
failures look minor, and do not withhold a Go that the evidence supports.

## Completion Report

Report:

- The command that ran and its scope
- Pass/fail/skip counts and duration, quoted from the actual output
- Results by priority, and coverage of `TR-xxx`
- Every failure with its triage verdict, in one line each
- Defects raised or drafted
- Path to the Allure report and the execution report
- Exit criteria assessment and the Go / No-Go / Conditional Go verdict
- If the run was red: the shortest path to green

## Done When

- [ ] Suite executed and results captured in `reports/allure-results`
- [ ] Allure HTML generated, or its absence explained with the fix
- [ ] Every failure triaged into product / test / environment / flaky / orphan-unsupported
- [ ] Requirement coverage excludes any orphan/unsupported test result
- [ ] Execution report written to `FEATURE_DIR/reports/`
- [ ] `test-cases.json` updated with this cycle's results and the workbook regenerated
- [ ] Exit criteria assessed and a Go/No-Go verdict given
- [ ] Actual results reported without softening
