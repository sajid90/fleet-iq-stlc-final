# specs/

One directory per Jira ticket, created by `/speckit-specify`. Each holds that
ticket's phase artifacts as they accumulate: `spec.md`, `source-manifest.json`,
`plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `test-cases.json`,
`test-cases.xlsx`, `test-cases.md`, `tasks.md`, `checklists/`, and — once the
suite has run — `reports/`.

`test-cases.json` is authoritative; `test-cases.xlsx` and `test-cases.md` are
generated from it via `.specify/scripts/python/export_testcases.py` and must
never be hand-edited.

This directory is empty until the first feature is specified.
