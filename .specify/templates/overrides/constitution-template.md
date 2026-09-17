# [PROJECT_NAME] QA Constitution
<!-- Example: FleetIQ QA Constitution -->

> The governing testing principles for this repository. Every `/speckit-*`
> phase command validates its output against this file. A violation must be
> justified in the plan's Complexity Tracking table, or the work does not proceed.

## Core Principles

### [PRINCIPLE_1_NAME]
<!-- Example: I. Traceability Is Non-Negotiable -->
[PRINCIPLE_1_DESCRIPTION]
<!-- Example: Every Jira AC becomes a TR-xxx, covered by a TC-xxx, automated by a Txxx, implemented as a named test function. No test without a requirement; no requirement untested or unwaived in writing. Any orphan is a process defect resolved before the exit gate. -->

### [PRINCIPLE_2_NAME]
<!-- Example: II. Requirements Are Verified Before They Are Tested -->
[PRINCIPLE_2_DESCRIPTION]
<!-- Example: Requirement analysis finds ambiguity, it does not restate the ticket. Untestable or contradictory ACs are raised in the Testability Review, never silently guessed. Assumptions applied in place of a missing detail are recorded so a reviewer can overturn them. -->

### [PRINCIPLE_3_NAME]
<!-- Example: III. Risk Drives Test Depth -->
[PRINCIPLE_3_DESCRIPTION]
<!-- Example: Coverage is allocated by risk, not spread evenly. P1 paths get exhaustive positive, negative and boundary coverage and are automated first. P3 may be smoke-only or manual. The allocation is stated in the plan and defended. -->

### [PRINCIPLE_4_NAME]
<!-- Example: IV. Deterministic Tests Only (NON-NEGOTIABLE) -->
[PRINCIPLE_4_DESCRIPTION]
<!-- Example: A test that fails intermittently trains the team to ignore red. Auto-waiting and web-first assertions only; time.sleep banned. Every test creates and cleans its own state. Tests pass in any order and in parallel or they are broken. A quarantined flaky test is a tracked defect with an owner, not a permanent rerun flag. -->

### [PRINCIPLE_5_NAME]
<!-- Example: V. Page Objects Own Interaction, Tests Own Assertion -->
[PRINCIPLE_5_DESCRIPTION]
<!-- Example: Page objects expose user intent, return page objects or data, and never assert. Locators live in the locator layer. Selector priority: role → label → data-testid → CSS; XPath requires a justifying comment. Other candidates: Manual and Automated Testing Are Both First-Class; Evidence Over Assertion. -->

## [SECTION_2_NAME]
<!-- Example: Data & Security Standards -->

[SECTION_2_CONTENT]
<!-- Example: No real customer data in the repository. Credentials come from the environment, never a tracked file — a committed secret is a Critical defect fixed before anything else. Test accounts are purpose-created and least-privileged. Reports and traces are scrubbed before leaving the team boundary. -->

## [SECTION_3_NAME]
<!-- Example: Quality Gates -->

[SECTION_3_CONTENT]
<!-- Example: a table of gate | what it blocks | criterion. Requirement analysis approved blocks /speckit-plan (no open NEEDS CLARIFICATION on P1). Test plan approved blocks /speckit-tasks (manual/automation split justified). Test cases reviewed blocks /speckit-implement (every P1 requirement has a P1 case). Suite green blocks sign-off (100% of P1 executed, zero open Critical/High). -->

## Governance
<!-- Example: how this constitution is amended and enforced -->

[GOVERNANCE_RULES]
<!-- Example: This constitution supersedes convention and convenience. Amendments go through /speckit-constitution, require a stated rationale, and bump the version semantically: MAJOR to remove or redefine a principle, MINOR to add one, PATCH for clarification. Every phase command validates its output against these principles and reports compliance. Warranted deviations are recorded in the plan's Complexity Tracking table with the rejected simpler alternative. Undocumented deviation is not permitted. -->

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
<!-- Example: Version: 1.0.0 | Ratified: 2026-09-10 | Last Amended: 2026-09-10 -->
