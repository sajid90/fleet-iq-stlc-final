# Research: FLTIQ-62 — Build the public landing page

STLC Phase 2, Phase 0 output. Every unknown a test plan for this feature
needs is resolved below before Part A/B are designed. None of these are
product-behavior questions — those stay in `spec.md` §13 and are not
relitigated here.

## R1 — Desktop viewport for non-360px testing

**Decision**: Use the repository's existing default desktop viewport,
1920×1080.

**Rationale**: `automation/utils/config.py::Settings` already defaults
`VIEWPORT_WIDTH`/`VIEWPORT_HEIGHT` to 1920×1080, and `.env.example` mirrors
it. `spec.md` §7 explicitly leaves the desktop breakpoint as INFERRED test
mechanics with no source-stated value — using the framework's existing
default avoids introducing a second, competing convention.

**Alternatives considered**: A feature-specific override (e.g. 1440×900) —
rejected; nothing in any source calls for a different desktop size than what
every other test in this repo already runs at, and a one-off override would
fragment the viewport matrix for no stated reason.

**Classification**: Resolved by repository.

## R2 — Emulating 200% browser zoom (TR-014)

**Decision**: Emulate 200% zoom by halving the desktop viewport (1920×1080 →
960×540), run at the standard 360px mobile viewport unchanged (halving that
further is not meaningful), and assert the same "no content/function lost"
outcome Scenario 4 already defines.

**Rationale**: Playwright's sync API has no cross-browser "browser zoom"
control. Chromium exposes `Page.setPageScaleFactor` only via a raw CDP
session, and CSS `zoom` (`page.evaluate("document.body.style.zoom=...")`) is
Chromium/WebKit-only — Firefox does not implement it. Halving the viewport is
the standard, browser-agnostic technique for approximating "what fits at 200%
zoom" (twice the content must occupy the same physical space, which is
equivalent to testing half the CSS-pixel viewport), and it runs identically
across the project's Chromium/Firefox/WebKit triad (pytest.ini's default
browsers).

**Alternatives considered**: CDP `setPageScaleFactor` — rejected, Chromium
-only, breaks cross-browser parity the suite otherwise has. Real OS-level
browser zoom via `page.keyboard.press("Control+Plus")` repeated — rejected,
unreliable step count across browsers/OS and not scriptable deterministically.

**Classification**: INFERRED (test mechanics only, per constitution II — this
is how to verify TR-014, not a restatement of what TR-014 requires).

## R3 — Automated WCAG 2.1 AA tooling (TR-012, TR-013, TR-014)

**Decision**: Add an axe-core-based Python package (exact package/version to
be pinned in `requirements.txt` at implementation time — not invented here,
per the rule against fabricating versions) for automated contrast and
common-violation scanning (TR-013, and a broad sweep supporting TR-011/014).
Keyboard operability (TR-012) is **not** delegated to axe — it is verified
directly with Playwright's own keyboard API (`page.keyboard.press("Tab")`
sequences plus `expect(locator).to_be_focused()`), which needs no new
dependency.

**Rationale**: `requirements.txt` currently has no accessibility-scanning
library at all — this is a real gap, not a hidden capability. Axe-core is the
de facto standard automated WCAG engine and is what FLTIQ-53 (the epic-wide
accessibility story whose pipeline gate RA-002 references) is virtually
certain to standardize on; adopting it here avoids inventing a second tool
that story would have to reconcile later. Keyboard-trap and focus-order
checks are only partially covered by axe's static analysis — genuine
tab-order verification requires actually driving the keyboard, which
Playwright already does natively.

**Alternatives considered**: Hand-rolled contrast calculation (WCAG's own
relative-luminance formula against computed styles) — rejected, reinventing
a well-tested wheel for no benefit and no source calls for a bespoke
implementation. `pa11y`/Node-based tooling — rejected, this is a Python
project; introducing a Node toolchain for one check is disproportionate.

**Residual gap, not fully closed here**: axe-core-class tools catch roughly
a third to half of real WCAG issues (industry consensus, not a project
figure) — screen-reader announcement quality for the hierarchy explorer's
custom tree control is explicitly carried into Part A as exploratory charter
CH-001, not claimed as automated.

**Classification**: INFERRED (tooling choice; the WCAG requirements
themselves are DEFINED in `spec.md`, this is only how they get measured).

## R4 — Verifying "no FleetIQ API call" (TR-008, NFR-002)

**Decision**: Attach a Playwright request listener (`page.on("request", ...)`
or `page.expect_event`) during hierarchy-explorer interaction and assert zero
requests of type `xhr`/`fetch` fire after the initial page load, rather than
filtering by a specific API host.

**Rationale**: `.env.example` has `API_BASE_URL` commented out — no API
surface is configured for this suite yet, so a host-based filter would be
guessing at a value nothing has defined. Asserting "no XHR/fetch fires at all
during this interaction" is a stronger, not weaker, check and needs no
invented configuration.

**Alternatives considered**: Filtering by a hypothetical `API_BASE_URL` —
rejected, would require inventing an unconfigured value.

**Classification**: Resolved by repository (uses `.env.example`'s actual,
current state rather than a guessed one).

## R5 — Establishing an authenticated session for Scenario 2 (TR-002)

**Decision**: Authenticate via a real UI sign-in (FLTIQ-35's sign-in screen)
before navigating to the root URL, using `TEST_USERNAME`/`TEST_PASSWORD` from
`.env`. If FLTIQ-35 is not yet deployed to the target environment, this test
is skipped with an explicit, visible reason (`pytest.mark.skip(reason=...)`),
never silently — mirroring the exact conditionality `spec.md` §10 already
documents for TR-004/TR-005's full-journey checks.

**Rationale**: There is no API-based session-seeding path available (no
`API_BASE_URL`/auth-token configuration exists), and injecting a forged
session cookie/token would test nothing about the real authentication flow
and could mask a genuine redirect defect. A real sign-in is the only
approach that proves TR-002's actual claim.

**Alternatives considered**: `context.add_cookies()` with a hand-crafted
session token — rejected, no source describes this app's session/cookie
format, and forging one is guessing at an implementation detail this repo's
constitution (never invent) forbids. Skipping Scenario 2 outright until
FLTIQ-35 ships — rejected as the default; the conditional-skip approach keeps
the test ready to go green the moment the dependency lands, rather than
requiring someone to remember to write it later.

**Classification**: Resolved by repository/environment-dependency precedent
already set in `spec.md` §10.

## R6 — Stable selectors for the hierarchy explorer

**Decision**: Locate each tree node with `get_by_role("button", name=re.compile(...))`
using a regex that matches the node's plain label (e.g. `"Floor 1"`) rather
than its full accessible name, since the real DOM's button text concatenates
the label with tree-drawing characters (`├─`, `│`, `└─`) and a metadata
string. Detail-panel fields (device count, device type, config source) have
no ARIA semantics distinguishing them — **flag to development as a
testability request**: add `data-testid` to the four detail-panel value
elements, per constitution VII's own selector-priority fallback (role → label
→ `data-testid` → CSS) for exactly the case where role/label cannot
disambiguate.

**Rationale**: The design source's node rows are rendered as native
`<button>` elements (a good sign — genuinely keyboard-operable by default),
but their full text includes ASCII tree art that regex/partial matching
avoids being fragile against. The detail panel's `<span>` pairs (label +
value) have no accessible role of their own, which is exactly constitution
VII's documented case for falling back to `data-testid` rather than XPath.

**Alternatives considered**: Full-string exact-name matching — rejected,
brittle against any whitespace/character change in the tree-art rendering.
XPath text-contains selectors for the detail panel — rejected without
justification per constitution VII ("XPath requires a comment justifying
it") when a `data-testid` request is the correct, non-brittle fix.

**Classification**: INFERRED for the node-matching technique (test mechanics
only); the `data-testid` request is a testability gap carried into B7 Risks
to Automation, not a requirement change.

## R7 — TR-018 and the three pending elective questions

**Decision**: TR-018 (UNDEFINED, blocked on `spec.md` §13a Q1) gets **no**
test approach and is excluded from B1's coverage denominator, per the
Outline's explicit rule that a blocked requirement gets no strategy — that
would be inventing an expected result. The three pending elective questions
(§13b Q2–Q4: loading-state UI, script-failure fallback, static-data
permanence) already have no expected result written in `spec.md` (EC-001,
EC-003, and TR-006/§11's flagged statistic) — nothing new is invented here
either; they surface as exploratory charters in Part A instead of automated
assertions.

**Classification**: Needs clarification (already tracked; does not newly
block this plan per constitution §XI.b, since none affects a P1 requirement).

## Summary — no unresolved unknowns

Every technical unknown this feature's test design depends on is settled
above. No `NEEDS CLARIFICATION` marker remains unaddressed in this document.
