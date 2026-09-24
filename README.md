# FleetIQ STLC

GitHub Spec Kit, adapted from Spec-Driven Development (SDD) to the **Software
Testing Life Cycle (STLC)**. The five phase commands take a Jira ticket through
requirement analysis, test planning, test case development, automation, and
execution — each phase producing a reviewable artifact that traces to the last.

## The workflow

| Command | STLC phase | Input | Output |
|---------|-----------|-------|--------|
| `/speckit-specify` | 1 — Requirement Analysis | Jira issue key only | `spec.md` — testable requirements `TR-xxx` (each classified DEFINED/OBSERVED/INFERRED/UNDEFINED), scenarios, risks, testability findings, `source-manifest.json` |
| `/speckit-plan` | 2 — Test Planning | `spec.md` | `plan.md` — manual strategy (Part A) + automation technical plan (Part B), `research.md`, `data-model.md`, `quickstart.md` |
| `/speckit-tasks` | 3 — Test Case Development | `spec.md`, `plan.md` | `test-cases.json`, **`test-cases.xlsx`**, `tasks.md` |
| `/speckit-implement` | 4 — Test Automation | `tasks.md`, `test-cases.json` | pytest + Playwright POM code under `automation/` |
| `/speckit-test` | 5 — Execution & Closure | the suite | Allure report, execution report, Go/No-Go verdict |

Run them in order, or run the whole gated cycle as the `speckit` workflow
("Full STLC Cycle"), which pauses for human approval after specify, plan,
tasks and convergence.

## Requirement resolution: one Jira key in, the full source chain out

`/speckit-specify FLTIQ-33` — or the full ticket URL,
e.g. `/speckit-specify https://fleetiq-acldigital.atlassian.net/browse/FLTIQ-33`
— takes a Jira reference and nothing else — never a manually supplied Epic,
PRD, decision log or design file. It discovers those by walking a fixed source
chain and recording, for every level, either what it found or why it could not
(`source-manifest.json`):

```text
Jira Story/MVP ─ parent ─► Epic ─ attachments ─► PRD
                              ├─► cited decisions ─► Decision Logs
                              └─► design field/attachments ─► approved UX/UI
   ─► MVP/Product Proposal/Roadmap ─► existing implementation ─► technical docs ─► inference
```

Empty `issuelinks`/`attachment`/`comment` on the story is not evidence of no
dependencies — prose is scanned for issue keys as a fallback. Custom fields
(acceptance criteria, design links) are resolved by display name via
`.specify/jira-field-map.json`, never hard-coded, because field ids differ per
Jira site.

Every material statement is classified DEFINED / OBSERVED / INFERRED /
UNDEFINED. Observation can establish what a system *does*, never what it
*should* do — so an unbuilt feature's business intent that no approved source
settles is recorded as UNDEFINED and blocks the P1 gate, never quietly turned
into an assumption. Conflicts between sources are recorded, never silently
resolved, unless a source adjudicates the conflict itself in writing.

### Traceability chain

```text
Jira AC  →  TR-xxx (spec.md)  →  TC-xxx (test-cases.json/xlsx)  →  Txxx (tasks.md)  →  test_tcxxx_*() 
```

Every link is enforced by the phase commands. An orphan at either end is a
process defect — see `.specify/memory/constitution.md`, principle I.

## Getting started

```bash
pip install -r requirements.txt
```

```bash
playwright install --with-deps chromium
```

```bash
cp .env.example .env
```

Fill in `BASE_URL` and test credentials in `.env`, then verify the framework:

```bash
.specify/scripts/bash/run-tests.sh -m smoke
```

`automation/tests/test_framework_wiring.py` is a browserless self-check — no
`.env`, no browser, no product required — so it passes on a clean clone before
any real feature exists. If it fails, the framework itself is broken, not the
product.

For HTML reports you also need the Allure CLI:

```bash
npm install -g allure-commandline
```

## Automation framework

FleetIQ is one application subdivided by feature module. **One feature owns
exactly one file per layer** — a page object, a locator module, a test-data
file, a test file.

```text
pytest.ini              markers, Allure results dir, artifact capture
requirements.txt        pinned dependencies
.env.example            configuration template — real .env is git-ignored
automation/
├── conftest.py         GLOBAL fixtures only: settings, context args, failure
│                        evidence, ui/api marker derivation
├── utils/               base_page.py, config.py, logger.py, data_loader.py
├── pages/               Page Object Model — one file per feature, <feature>_page.py
├── locators/            locator constants — one file per feature, <feature>_locators.py
├── test_data/           static test data (JSON) — one file per feature, <feature>.json
└── tests/
    ├── test_framework_wiring.py   browserless self-check
    ├── ui/               browser tests, test_<feature>.py; conftest.py holds
    │                      browser-only autouse fixtures + page-object fixtures
    └── api/              API-level tests, no browser — empty until the first one
```

**Design rules** (enforced by the constitution):

- Page objects expose user intent and **never assert**; tests hold every assertion
- Selector priority: `get_by_role` → `get_by_label` → `data-testid` → CSS
- Playwright auto-waiting and web-first assertions only — `time.sleep` is banned
- Every test is independent and passes in parallel and in any order
- Test functions are named `test_<tcid>_<behaviour>` and tagged `@allure.testcase("TC-xxx")`
- Secrets come from the environment, never from a tracked file

### Running tests

```bash
.specify/scripts/bash/run-tests.sh
```

| Goal | Command |
|------|---------|
| Smoke only | `.specify/scripts/bash/run-tests.sh -m smoke` |
| P1 in Firefox | `.specify/scripts/bash/run-tests.sh -m p1 -b firefox` |
| One file, visible browser | `.specify/scripts/bash/run-tests.sh -k automation/tests/ui/test_<feature>.py --headed` |
| Parallel | `.specify/scripts/bash/run-tests.sh -n auto` |
| Open the report | `.specify/scripts/bash/run-tests.sh --serve` |

On failure the Allure report carries a screenshot, the page DOM, the URL and
the browser console, attached to the failed test itself. Playwright traces and
videos land in `automation/reports/test-artifacts/`; open one with
`playwright show-trace <path>`.

## Test case export

`test-cases.json` is the single source of truth; the workbook is generated:

```bash
python3 .specify/scripts/python/export_testcases.py specs/<feature-dir> --markdown
```

Produces `test-cases.xlsx` with four sheets — Summary, Test Cases, Steps,
Traceability — plus `test-cases.md`. The script fails on invalid data and warns
on untraced cases. Never edit the `.xlsx` as the source; edit the JSON and
re-export.

## Jira input

`/speckit-specify` fetches tickets — and their parent Epic, attachments and
linked/prose-referenced issues — through the **Atlassian MCP server** when one
is connected. If it is not, the command says so and asks you to paste the ticket
content or point at a local PRD — it will not invent requirements.

Ticket content is always treated as data, never as instructions.

## Repository layout

```text
.claude/skills/         the phase commands
.specify/
├── memory/constitution.md      QA principles every phase is checked against
├── jira-field-map.json         custom-field name→id resolution (never hard-coded ids)
├── templates/overrides/        STLC templates (spec, plan, tasks, checklist, constitution)
├── templates/                  source-manifest-template.json, test-report-template.md
├── scripts/bash/               setup, prerequisites, run-tests.sh
├── scripts/python/             export_testcases.py
└── workflows/speckit/          the gated Full STLC Cycle
specs/<nnn-feature>/    one directory per ticket, holding all phase artifacts
automation/             the automation framework
```

## Supporting commands

All eleven commands are STLC-adapted. Beyond the five phase commands above:

| Command | What it does |
|---------|--------------|
| `/speckit-clarify` | Resolves ambiguity in the test basis before planning — asks up to 5 targeted questions across a testing taxonomy (expected results, boundaries, test data, environment, NFR measurability, manual-vs-automation intent) and writes the answers into the right `spec.md` section |
| `/speckit-analyze` | Read-only audit of the whole traceability chain across `spec.md`, `plan.md`, `test-cases.json`, `tasks.md` and `automation/`. Flags uncovered requirements, orphan cases, automation drift, and constitution violations |
| `/speckit-checklist` | Generates reviewer checklists that validate the **quality of the test artifacts** — coverage, case quality, automation readiness, test data, release exit — never the product itself |
| `/speckit-constitution` | Creates or amends the QA constitution, with the versioning and Sync Impact Report intact |
| `/speckit-converge` | Assesses the automation suite against the test cases and appends the remaining test work to `tasks.md`. Append-only; never touches product code |
| `/speckit-taskstoissues` | Turns automation tasks into tracker issues — **Jira via Atlassian MCP** or GitHub — carrying the test cases each covers. Always confirms the list before creating anything |

### Suggested order

```text
/speckit-specify → [approve] → /speckit-clarify → /speckit-plan → [approve]
    → /speckit-checklist → /speckit-tasks → [approve] → /speckit-analyze
    → /speckit-implement → /speckit-converge → [approve] → /speckit-test
```

The five phase commands are the spine; `/speckit-converge` sits between
implement and test, not off to the side — the workflow's gate after it is what
a "Go" verdict is conditioned on. The rest are gates you run when the feature
warrants them. Approval gates are enforced two ways: the `type: gate` steps in
`.specify/workflows/speckit/workflow.yml` when you run the full cycle, and each
phase skill's own check of the previous artifact's `Status:` header when you
run commands individually.

## Upgrade caution

All eleven adapted skills live at `.claude/skills/speckit-*/SKILL.md`, the same
paths spec-kit installs to. **Re-running `specify init` or a spec-kit upgrade
will overwrite them** with the upstream SDD versions.

The STLC templates are safe: they live in `.specify/templates/overrides/`, which
takes priority over anything an upgrade installs. Back up `.claude/skills/`
before upgrading, and restore the adapted skills after.
