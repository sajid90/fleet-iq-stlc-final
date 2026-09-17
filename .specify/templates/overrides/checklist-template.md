# [CHECKLIST TYPE] Checklist: [TICKET-ID] — [FEATURE NAME]

**Purpose**: [What quality dimension of the test artifacts this reviews]
**Created**: [DATE]
**Reviews**: [Which artifacts — spec.md / plan.md / test-cases.json / tasks.md / automation/]
**Reviewer**: [NAME]

**What this is**: a review of the **quality of our testing**, not a run of the
tests. Every item is answered by reading the artifacts. If an item could only be
answered by running the application, it is a test case and belongs in
`test-cases.json` via `/speckit-tasks`.

**Review Ownership**: reviewer-owned. Mark an item `[x]` only when you have
judged the criterion satisfied.
**Marker Semantics**: `[x]` means the test artifacts meet this quality
criterion. It does **not** mean any testing was executed, nor that the product
passed.

<!--
  ============================================================================
  IMPORTANT: the items below are SAMPLE ITEMS for illustration only.

  /speckit-checklist MUST replace them with real items derived from:
  - the user's specific review request
  - the test basis in spec.md (TR-xxx, scenarios, edge cases, NFRs)
  - the strategy and design rules in plan.md
  - the cases in test-cases.json
  - the automation breakdown in tasks.md and the code in automation/

  DO NOT keep these samples in the generated file.
  ============================================================================
-->

## [Category 1 — e.g. Coverage Completeness]

- [ ] CHK001 Does every `TR-xxx` in spec.md §3 map to at least one test case? (traceability)
- [ ] CHK002 Does every P1 requirement have at least one P1 test case? (completeness)
- [ ] CHK003 Does every scenario have both positive and negative coverage? (coverage)

## [Category 2 — e.g. Test Case Quality]

- [ ] CHK004 Is each expected result observable without inspecting internal state? (testability)
- [ ] CHK005 Are preconditions explicit, including the required role and data? (completeness)
- [ ] CHK006 Do steps reference a data alias rather than a literal credential? (security)

## Findings

<!-- Record what a failed item actually revealed, and where it was fixed. -->

| Item | Finding | Resolution |
|------|---------|------------|
| CHK00n | [What was missing or unclear] | [Artifact updated / raised as a question] |

## Notes

- Mark `[x]` only after review confirms the criterion is satisfied
- Leave unchecked when the artifact still needs clarification or correction
- `/speckit-implement` reads checkbox state as a gate and must not change markers
- `checklists/requirements.md` has its own lifecycle, maintained by
  `/speckit-specify` and `/speckit-clarify`
- Items are numbered sequentially for reference in review comments
