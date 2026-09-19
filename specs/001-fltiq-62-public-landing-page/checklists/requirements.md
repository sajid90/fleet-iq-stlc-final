# Requirement Analysis Quality Checklist: Build the public landing page

**Purpose**: Validate the test basis before test planning
**Created**: 2026-09-18
**Ticket**: FLTIQ-62

## Source Fidelity

- [x] Every requirement traces to a named source id (acceptance criterion, PRD section, or ticket field)
- [x] Every requirement carries an Authority and a Class
- [x] `source-manifest.json` exists and is valid JSON
- [x] `field_map` records how each custom field was resolved, with `matched_by`
- [x] No `customfield_NNNNN` literal appears anywhere in the spec
- [x] The parent Epic was resolved, or its absence is recorded with a reason
- [x] Every cited-but-unretrieved source is in `missing_sources` with its impact
- [x] Every source conflict appears in both §11a and `conflicts[]`
- [x] Ticket URL and fetch datetime recorded

## UI Element Enumeration

*(Added 2026-09-19 along with the skill's §15a retrofit — see spec.md Change Log)*

- [x] Pass 0 lists every file in the design project, each with an in-scope decision and a reason — 12 files, 1 in scope (`FleetIQ Landing.dc.html`), 11 excluded by name (spec.md §15a)
- [x] Every pass in §15a states its count and how that count was derived
- [x] Every UI element in every in-scope screen appears in §15a with a disposition
- [x] Every interactive-element row names a behaviour, not a presence
- [x] §3a states the acceptance-criterion count per source and how it was derived

## Testability

- [x] Every TR is independently verifiable from outside the system
- [x] Every TR has a Type, Priority and Risk rating
- [x] Ambiguous or unmeasurable source ACs are listed in the Testability Review
- [x] NFRs state measurable targets, not adjectives

## Evidence Integrity

- [x] No TR classed UNDEFINED carries a concrete expected result — TR-018 is the only UNDEFINED item and carries none
- [x] Every UNDEFINED TR has a matching §13a blocking question — TR-018 ↔ §13a Q1
- [x] §12 *Test-execution assumptions* contains no statement of product intent
- [x] Every OBSERVED statement cites both its evidence and the source mandating the behaviour — *(vacuously true: no OBSERVED statement exists — system not yet built)*
- [x] No business rule, threshold or contract was invented to keep the workflow moving

## Coverage

- [x] Every TR is covered by at least one scenario
- [x] Every acceptance criterion in §3a maps to a TR, or is recorded as uncovered
- [x] Each scenario has both positive and negative/alternate flows
- [x] Edge cases and boundary conditions identified
- [x] Security/privacy and timing/concurrency/idempotency concerns addressed or marked N/A
- [x] Test data requirements identified for every scenario
- [x] Environment and platform matrix defined

## Readiness

- [ ] No unresolved §13a blocking item on a P1 requirement — **one blocking item is open (Q1), but it blocks TR-018 (P2), not a P1 requirement — does not block the requirement-analysis gate per constitution XI.b, but must be resolved before TR-018 is automated or before this page ships**
- [x] Risk analysis complete, with test focus per risk
- [x] Entry and exit criteria are concrete and checkable
- [x] No implementation detail has leaked into the spec

## Notes

- **Dependency resolution gate**: all pre-execution checks passed on this run — constitution, source-manifest template, and jira-field-map present; Atlassian MCP connected; a design link was found on FLTIQ-62 and the Claude Design MCP connection was verified live (via `DesignSync`) before any content was written, per the new 1F.2 gate added to this skill after an earlier session hit this gap mid-analysis.
- This story is a late backlog addition (S-25) with no dedicated PRD section, but its own acceptance criteria and scope statement are unusually complete. The tension between "no PRD requirement" and three PRD-bracketed ACs in its own AC field (CF-001) was investigated and resolved in-source — see spec.md §11a.
- **New finding from the design source**: the hero contains "Free while you set up your first fleet. No card required." — a line with no counterpart in the Story, Epic, or PRD, and in tension with the Story's own "no pricing content" exclusion. Recorded as CF-002 / TR-018, raised to the requester as a genuine blocking question (§13a Q1) rather than silently included or excluded.
- **Requester screenshot cross-check (post-initial-draft)**: the requester supplied two screenshots of the rendered design and asked for a cross-check against `spec.md`. This surfaced two omissions — the capabilities section heading and the hierarchy section heading+intro, both now folded into TR-007/TR-019.
- Four elective (non-blocking) questions remain open — cross-epic statistic accuracy, auth-loading state, hierarchy-explorer failure fallback, and static-data permanence. None blocks a P1 requirement.
- **All 4 open questions (§13a Q1 blocking + §13b Q2/Q3/Q4 elective) were sent to the team on 2026-09-18; answers are pending.** Per constitution §XI.b, this does not block moving to `/speckit-plan` — the sole blocking item affects TR-018 (P2), and every P1 requirement is fully DEFINED with no open blocking clarification.
- Items left incomplete must be resolved before `/speckit-clarify` or `/speckit-plan`. *(Note: per the point above, this project's own gate does not require these specific items resolved before `/speckit-plan`, since none blocks a P1 — the standard checklist language is retained here as the general rule, with the exception noted explicitly.)*
