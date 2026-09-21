# Test Execution Report: [TICKET-ID] — [FEATURE NAME]

**Cycle**: [N] | **Date**: [DATE] | **Environment**: [QA/Staging] | **Build**: [version/commit]
**Executed by**: [NAME] | **Test Plan**: [link to plan.md]

> STLC Phase 5 — Test Execution & Cycle Closure. Produced by `/speckit-test`.

## 1. Execution Summary

| Metric | Value |
|--------|-------|
| Total test cases | [N] |
| Executed | [N] |
| Passed | [N] |
| Failed | [N] |
| Blocked | [N] |
| Skipped | [N] |
| Pass rate | [N%] |
| Duration | [Xm Ys] |

**Allure report**: `automation/reports/allure-report/index.html`
**Raw results**: `automation/reports/allure-results/`

## 2. Results by Priority

| Priority | Total | Passed | Failed | Blocked | Pass rate |
|----------|-------|--------|--------|---------|-----------|
| P1 | | | | | |
| P2 | | | | | |
| P3 | | | | | |

## 3. Results by Scenario

| Scenario | Test Cases | Passed | Failed | Status |
|----------|-----------|--------|--------|--------|
| S1 — [Title] | | | | Pass / Fail |

## 4. Failed Test Cases

<!-- One block per failure. No failure is omitted or softened. -->

### FAIL: TC-xxx — [Title]

- **Test**: `automation/tests/ui/test_x.py::test_name`
- **Requirement**: TR-xxx
- **Error**: `[actual assertion / exception message]`
- **Evidence**: screenshot, trace, video attached in Allure
- **Verdict**: Product defect | Test defect | Environment issue | Flaky
- **Defect raised**: [TICKET-ID or "not raised — reason"]

## 5. Defects Raised This Cycle

| Defect ID | Title | Severity | Priority | Test Case | Status |
|-----------|-------|----------|----------|-----------|--------|
| [KEY-123] | [Title] | Critical/High/Medium/Low | P1..P3 | TC-xxx | Open |

## 6. Flaky / Quarantined Tests

| Test | Observed behaviour | Owner | Action |
|------|--------------------|-------|--------|
| [test id] | [passes on rerun N/M] | [NAME] | [Fix / quarantine ticket] |

## 7. Coverage Against Requirements

| Requirement | Test Cases | Executed | Result |
|-------------|-----------|----------|--------|
| TR-001 | TC-001, TC-002 | Yes | Pass |

**Uncovered requirements**: [list, or "none"]

## 8. Exit Criteria Assessment

| Criterion | Target | Actual | Met |
|-----------|--------|--------|-----|
| P1 cases executed | 100% | [N%] | Yes/No |
| Open Critical/High defects | 0 | [N] | Yes/No |
| Overall pass rate | [target] | [actual] | Yes/No |

**Exit criteria met**: Yes / No — [if No, state precisely what is outstanding]

## 9. Recommendation

**Verdict**: Go / No-Go / Conditional Go

[One paragraph. If Conditional, state the exact conditions and who owns them.]

## 10. Observations & Improvements

- [What slowed the cycle, what should change next time — coverage gaps, missing
  test hooks, environment instability, data setup friction]
