# Requirement Analysis: [TICKET-ID] — [FEATURE NAME]

**Ticket**: `[TICKET-ID]` | **Source**: [Jira URL or PRD path]
**Analysed**: [DATE] | **Analyst**: [NAME]
**Source manifest**: `source-manifest.json`
**Status**: Draft | In Review | Approved
**Approved by**: *(set at the requirement-analysis gate)* | **Approved on**: —
**Input**: "$ARGUMENTS"

> STLC Phase 1 — Requirement Analysis. This document is the **test basis**.
> Everything downstream (test plan, test cases, automation) traces back to a
> `TR-xxx` identifier defined here. No implementation detail belongs in this file.

## 1. Requirement Summary

[2-4 sentences in plain business language: what changes for the user, and why.
Derived from the resolved sources — not invented.]

## 2. Scope

### In Scope

- [Capability that will be tested]

### Out of Scope

- [Explicitly excluded area — state why, e.g. "covered by TICKET-999"]

### Deferred

<!--
  Distinct from Out of Scope. A deferred requirement IS part of this feature's
  intent but is scheduled elsewhere. Name where it went — an unexplained
  deferral is indistinguishable from an omission.
-->

- [Requirement deferred to another ticket — name the ticket and the reason]

## 3. Testable Requirements

<!--
  Every row must be independently verifiable. If a source acceptance criterion
  is vague, split it or raise it in section 11 (Testability Review) — do not
  silently invent the missing half.

  Class is governed by the Observation Rule (constitution II). A row classed
  UNDEFINED has no expected result: state the obligation, cite the §13a
  question, and write no test case that asserts an outcome for it.
-->

| ID | Requirement | Source (AC / PRD ref) | Authority | Class | Type | Priority | Risk |
|----|-------------|-----------------------|-----------|-------|------|----------|------|
| TR-001 | System MUST [observable behaviour] | TIA-AC-04 | detailed-requirements | DEFINED | Functional | P1 | High |
| TR-002 | System MUST [observable behaviour] | AC-2 | scope-and-story-acceptance | DEFINED | Functional | P2 | Medium |
| TR-003 | [Obligation stated, outcome not defined by any approved source] — **Expected result: UNDEFINED, see §13a Q1** | PRD §4.12 | detailed-requirements | UNDEFINED | Functional | P1 | High |

**Type**: Functional | UI | API | Data | Performance | Security | Accessibility | Compatibility
**Priority**: P1 (critical path) | P2 (important) | P3 (nice to have)
**Risk**: High | Medium | Low — drives test depth in the plan phase.
**Authority**: the token of the source that governs this requirement (constitution I).
**Class**: DEFINED | OBSERVED | INFERRED | UNDEFINED (constitution II).

## 3a. Acceptance Criteria Index

<!--
  The anchor of the traceability chain: Jira AC → TR → TC → task → test function.
  Origin distinguishes an AC that came from the PRD from one the backlog added,
  where a source states such a convention (see source-manifest provenance_rules).
  A row with no TR is an uncovered acceptance criterion — a gap, not a rounding error.
-->

| AC id | Origin | Statement (summary) | Source ref | TR(s) | Status |
|-------|--------|---------------------|-----------|-------|--------|
| [TIA-AC-04] | prd | [Given/When/Then, summarised] | PRD §7 | TR-001 | covered |
| *(unbracketed)* | backlog | [Given/When/Then, summarised] | Story AC field | TR-002 | covered |

## 4. Test Scenarios *(mandatory)*

<!--
  Prioritised user journeys. Each scenario must be INDEPENDENTLY TESTABLE — if
  only this one is executed it still yields a meaningful verdict on the feature.
-->

### Scenario 1 - [Brief Title] (Priority: P1)

[The user journey in plain language.]

**Why this priority**: [Business impact / usage frequency / risk exposure]

**Covers**: TR-001, TR-002

**Independent Test**: [How this is exercised end to end on its own]

**Acceptance Scenarios**:

1. **Given** [precondition], **When** [action], **Then** [observable expected result]
2. **Given** [precondition], **When** [action], **Then** [observable expected result]

**Negative / Alternate Flows**:

1. **Given** [precondition], **When** [invalid action], **Then** [expected error handling]

---

### Scenario 2 - [Brief Title] (Priority: P2)

[Repeat the structure above. Add scenarios as needed.]

---

## 5. Edge Cases & Boundary Conditions

| ID | Condition | Expected Handling |
|----|-----------|-------------------|
| EC-001 | [Boundary value, e.g. field at max length] | [Expected behaviour] |
| EC-002 | [Empty / null / zero state] | [Expected behaviour] |
| EC-003 | [Concurrency, timeout, idempotency, or network failure] | [Expected behaviour] |

## 6. Test Data Requirements

| Data Set | Description | Source | Sensitivity |
|----------|-------------|--------|-------------|
| [e.g. example_user] | [Attributes needed] | [Seeded / fixture / prod-like] | [None / PII — must be masked] |

**Note**: Never place real customer data, credentials, or tokens in this file.

## 7. Environment & Platform Matrix

| Dimension | Values |
|-----------|--------|
| Environments | [e.g. QA, Staging] |
| Browsers | [e.g. Chromium, Firefox, WebKit] |
| Viewports | [e.g. 1920x1080 desktop, 390x844 mobile] |
| Prerequisites | [Feature flags, roles, integrations that must be live] |

## 8. Non-Functional Requirements

- **NFR-001**: [Measurable target, e.g. "Search results render within 2 seconds at p95"]
- **NFR-002**: [Accessibility target, e.g. "All interactive controls reachable by keyboard, WCAG 2.1 AA"]
- **NFR-003**: [Security expectation, e.g. "Session expires after 30 minutes idle"]

## 9. Risk Analysis

| ID | Risk | Likelihood | Impact | Mitigation / Test Focus |
|----|------|------------|--------|-------------------------|
| RA-001 | [What could go wrong in production] | High/Med/Low | High/Med/Low | [Which tests reduce this risk] |

## 10. Entry & Exit Criteria

**Entry criteria** (before test execution starts):

- [ ] Requirement analysis approved
- [ ] Build deployed to [environment] and smoke-passable
- [ ] Test data and accounts provisioned

**Exit criteria** (before sign-off):

- [ ] 100% of P1 test cases executed
- [ ] Zero open Critical/High defects
- [ ] [Coverage or pass-rate threshold]

## 11. Testability Review

<!--
  Flag requirements that cannot be verified as written. This is the QA value-add
  of the analysis phase — do not skip it because the ticket "looked clear".
-->

| Source AC | Issue | Proposed Resolution |
|-----------|-------|---------------------|
| [AC-3] | [Ambiguous: "fast" is not measurable] | [Propose p95 < 2s] |

### 11a. Source Conflicts

<!--
  Mirrors source-manifest.json conflicts[]. Never silently pick a winner on a
  behavioural conflict. A conflict a source adjudicates in writing is recorded
  as resolved-in-source, citing the adjudication — not merely the outcome.

  A paraphrase or a boundary instance of the same rule is NOT a conflict.
-->

| ID | Source A (authority) | Source B (authority) | Contested statement | Domain | Outcome | Status |
|----|----------------------|----------------------|---------------------|--------|---------|--------|
| CF-001 | [PRD §4.1 requirement] | [PRD Figure 1 design] | [what differs] | presentation vs detailed-requirement | requirement governs | resolved-in-source |
| CF-002 | [Story "covers X"] | [Story "X out of scope"] | [what differs] | scope | — | **unresolved → §13a Q1** |

## 12. Evidence Classification

### DEFINED

- [Statement] — source, authority

### OBSERVED

- [Statement] — how verified, URL, date, **and** the approved source that mandates the behaviour

### INFERRED

- [Test-mechanics inference only]

### UNDEFINED

- [Obligation with no approved outcome] — cross-reference §13a

### Test-execution assumptions

<!--
  Environment, data provisioning, tooling and scheduling only.
  A statement of product intent must NEVER appear here — it belongs in §13a.
  Never convert an undefined business requirement into an assumption to continue.
-->

- [e.g. "The QA environment seeds the terms document before the suite runs"]

## 13. Open Questions

### 13a. Blocking

<!--
  UNDEFINED business requirements and unresolved source conflicts.
  UNCAPPED — truncating this list to fit a quota falsifies the analysis.
  Each item names what it blocks.
-->

- **Q1** [NEEDS CLARIFICATION: specific question] — *Blocks*: TR-003 (P1)

### 13b. Elective

<!-- Precision that would improve coverage but does not block. Maximum 3. -->

- [NEEDS CLARIFICATION: non-blocking question]

## 14. Traceability Seed

| Jira AC | Requirement | Scenario(s) | Test Cases | Automation |
|---------|-------------|-------------|------------|------------|
| TIA-AC-04 | TR-001 | Scenario 1 | *(filled by /speckit-tasks)* | *(filled by /speckit-implement)* |

## 15. Source Inventory

<!--
  Human-readable mirror of source-manifest.json, so the gate can be reviewed
  in Markdown. "Found on" names the actual issue key the artifact was located
  on -- never assumed from its type. A PRD is not always on the Epic; a
  decision log is not always cited-only. Every issue in the resolved set
  (story, Epic, every sub-task, every linked/prose-discovered issue) was
  checked for attachments before concluding a document is missing.
-->

| Type | Id / filename | Version | Found on | Retrieved | Authority | Relationship |
|------|---------------|---------|----------|-----------|-----------|--------------|
| jira-story | [KEY] | — | [KEY] (self) | [ISO datetime] | scope-and-story-acceptance | primary |
| jira-epic | [KEY] | — | [KEY] (self) | [ISO datetime] | feature-context | parent |
| prd | [filename] | [v1.2] | [issue key it was actually attached to] | [ISO datetime] | detailed-requirements | [parent / subtask-of-story / subtask-of-epic / issue-link] |

### Missing Sources

| Ref | Kind | Cited by | Reason | Impact |
|-----|------|----------|--------|--------|
| [UX-D28] | decision-log | [PRD §4.1] | [Log not supplied to this repository] | [TR-00n undefined] |

### Dependencies

| Ref | Kind | Discovered in | Status |
|-----|------|---------------|--------|
| [FLTIQ-15] | jira-issue | [Epic description (prose)] | resolved |
| [FLTIQ-40] | jira-issue | [Story sub-task] | resolved |
| [S-02] | backlog-ref | [Story description (prose)] | unresolvable — identifier only |
