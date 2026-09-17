# Source Authority & Resolution

How `/speckit-specify` turns a Jira issue key into a complete, classified test
basis. This is the reference for the mechanism; the constitution
(`.specify/memory/constitution.md`, principles I and II) is the governing
policy — this document explains how the skill implements it.

## Why a Jira key alone

`/speckit-specify FLTIQ-33` is deliberately minimal input. Requiring a person to
separately gather and hand over the Epic, PRD, decision logs and design files
defeats the point: those artifacts already exist in the tracker, linked or
attached, and asking a human to re-collect them is where drift enters — a
PRD version pasted once and never refreshed, a decision log nobody remembers
to attach next time. The skill discovers them instead.

## The resolution chain

```text
Jira Story / MVP ticket                   authority 1  scope + story ACs
   └─ parent ─► Parent Epic               authority 2  context, conventions, dependencies
   └─ sub-tasks (story)  ─┐
   └─ issue links (story) ─┤
   └─ prose-mentioned issues ┤
   Epic's own sub-tasks, issue links and prose-mentioned issues ┤
                             │
                             ▼
   the full issue set — story + Epic + every sub-task + every linked
   or prose-discovered issue — each checked for attachments, comments
   and custom fields. No document type is assumed to live on a
   particular ticket type.
                             │
             ┌───────────────┼────────────────┐
             ▼                ▼                ▼
   PRD (wherever attached)  Decision Logs   approved UX/UI design
   authority 3               authority 4      authority 5
     ├─ identifier convention
     ├─ requirements + acceptance criteria
     └─ open-questions section  ← an approved doc can carry UNDEFINED items of its own
   └─ MVP / Product Proposal / Roadmap              authority 6  product + delivery context
   └─ existing implementation             authority 7  OBSERVED only, never redefines intent
   └─ technical documentation             authority 8
                                          authority 9  inference — testing craft only
   ═► test basis: spec.md + source-manifest.json
```

Every level is attempted on every run. A level that resolves to nothing is not
a failure — it is a `missing_sources` entry naming what was sought, where it
was cited, and what it affects. That is a correct, informative result: it is
how a decision log nobody attached, or a design batch still in progress,
becomes visible to a reviewer instead of silently absent.

### Document location is not fixed — check the whole issue set

A PRD, decision log or design file can be attached to the story, the parent
Epic, a sub-task of either, or a linked issue — there is no reliable rule for
which. Attaching a shared PRD once to the parent Epic and letting every story
inherit it is a common pattern, but "common" is not "guaranteed": a team just
as easily attaches a requirements document to a dedicated sub-task, or to a
linked spike ticket, or to the story itself.

Because of this, resolution never stops at the first place a document is
found and never assumes a document type belongs on a particular issue type.
It builds the **full issue set** first — the story, its parent Epic, every
sub-task of both, and every issue reachable through `issuelinks[]` or through
an issue key mentioned in prose — and only then checks every member of that
set for attachments, comments and custom-field content. A document is recorded
as missing only after every issue in the set has been checked, and the
manifest records exactly which issue each artifact was actually found on
(`found_on`), not just the artifact's type.

### Why prose scanning matters

`issuelinks`, `attachment` and `comment` being empty on a story is not
evidence that the story has no dependencies — it commonly means the author
wrote "Depends on FLTIQ-15" in the description instead of creating a formal
Jira link. The resolution regex-scans all prose for issue-key patterns as a
fallback channel, and separately captures non-Jira references (backlog ids,
decision-log ids) that cannot be fetched at all, recording them as
unresolvable rather than dropping them.

### Why custom fields are resolved by name

Acceptance criteria frequently live in a custom field rather than in
`description` — and that field's id is specific to one Jira site. A skill that
hard-codes `customfield_10133` breaks the moment it runs against a different
project. `.specify/jira-field-map.json` holds synonym lists per semantic field
(`acceptance_criteria`, `design_link`, …); the skill matches a field's display
name against them, caches the resolution, and only a human-supplied
`overrides` entry may pin an id directly.

## Authority is scoped by domain, not by flat rank

The nine-level order above says which source *wins a tie when two sources
agree on which domain governs*. It is not a flat "higher number always loses"
rule: a design mockup outranks the PRD on layout and labels, but loses to the
PRD on a functional rule. See constitution I's Precedence Policy table for the
authority tokens and the domains each governs.

**A conflict is recorded, never silently resolved** — the one exception being
a conflict a source adjudicates in writing itself (e.g. a PRD note saying "the
requirement takes precedence over the wireframe label"), in which case the
adjudication and its citation are recorded, not merely the outcome.

## Classification: DEFINED / OBSERVED / INFERRED / UNDEFINED

See constitution II for the full rule and its four hard stops. The short
version: an approved source settles DEFINED and OBSERVED; a testing-craft
choice with no product consequence is INFERRED; everything else — a business
requirement no approved source defines — is UNDEFINED, and UNDEFINED is never
converted into an assumption to keep the workflow moving. It is recorded, a
clarification is raised, and it blocks the gate on a P1 requirement.
