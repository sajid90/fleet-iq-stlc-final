# Test Data Model: FLTIQ-62 — Build the public landing page

STLC Phase 2, Phase 1 output. This is the **test data model**, not a product
data model — every entity below exists to be asserted against, not to be
created/mutated by the tests (this page has no write path at all).

## Entity: HierarchyNode

The static fixture the hierarchy explorer renders, confirmed verbatim in the
Claude Design source (`FleetIQ Landing.dc.html`) and mirrored in
`spec.md` §6.

| Field | Type | Notes |
|---|---|---|
| `id` | string | Internal key (`a`, `a1`, `a2`, `b`, `un`) — not visible to the user, used only to select the fixture row in `automation/test_data/landing.json` |
| `label` | string | Visible name (e.g. "Floor 1") — the stable substring used for locator matching (R6) |
| `prefix` | string | The ASCII tree-art string rendered before the label in the tree row (`├─ `, `│  ├─ `, `│  └─ `, `└─ `, or blank for the un-nested "Unassigned" row) — this is what makes exact-name locator matching brittle (R6) |
| `meta` | string | The right-aligned text shown **in the tree row itself**. **Not the same field as `devices`** — see note below |
| `devices` | integer (as string in source) | Device count shown **only in the detail panel**, once a node is selected |
| `type` | string | Device type shown in the detail panel |
| `source` | string | Config source shown in the detail panel |
| `status` | enum: `healthy` \| `caution` \| `decommissioned` \| `warning` | Drives the status badge |
| `statusLabel` | string | Human-readable status text ("Healthy", "3 pending", "Empty", "Needs placing") |
| `note` | string | Free-text note shown under the detail-panel fields |

**`meta` vs. `devices` — a distinction easy to miss and worth testing
explicitly**: for the two "Building" nodes, the tree row's `meta` text is a
**subgroup count**, not a device count (`"2 subgroups"` for Building A,
`"0 subgroups"` for Building B) — while Building A's *detail panel* still
shows `79` under "Devices" once selected. For the two "Floor" nodes and
"Unassigned", `meta` happens to read as a device count (`"41 devices"`), but
it is still a distinct string field, not a derived display of `devices`. A
test that only asserts the detail panel's `devices` value would never catch
a regression in the tree row's `meta` text for Building A/B.

**Concrete instances (the full fixture, no others exist)**:

| id | label | prefix | meta (tree row) | devices (detail panel) | type | source | status | statusLabel | note |
|---|---|---|---|---|---|---|---|---|---|
| `a` | Building A | `├─ ` | "2 subgroups" | 79 | Mixed — 2 types | Organisation default | healthy | Healthy | "Subgroups may override the organisation default. Two do." |
| `a1` | Floor 1 | `│  ├─ ` | "41 devices" | 41 | Gateway XR-2 | Building A | healthy | Healthy | "A change applied here reaches 41 devices. Nothing is applied until you review the diff." |
| `a2` | Floor 2 | `│  └─ ` | "38 devices" | 38 | Gateway XR-2 | Overridden here | caution | 3 pending | "Three devices have not acknowledged the last push. They keep their previous configuration until they do." |
| `b` | Building B | `└─ ` | "0 subgroups" | 0 | — | Organisation default | decommissioned | Empty | "Devices appear here the moment they claim a provisioning token." |
| `un` | Unassigned | *(blank)* | "501 devices" | 501 | Mixed — 4 types | None — inherits nothing | warning | Needs placing | "Unassigned devices report telemetry but receive no configuration. Place them in a group to give them one." |

Each `note` is not filler — it ties directly back to a capability claim in
TR-007: Floor 1's note ("Nothing is applied until you review the diff")
demonstrates capability card 03 ("Review before it applies"); Building A's
("Subgroups may override the organisation default") demonstrates card 02
("A hierarchy that holds"). A test asserting `note` text is therefore
verifying the demo actually backs up the marketing claim next to it, not
just checking arbitrary copy.

**Boundary values worth testing** (constitution V — every scenario carries
boundary cases):
- `b` (Building B) — the **zero-devices** boundary; confirms the detail panel
  renders correctly with a `0` count and a `—` type rather than blank/error
  (EC-006, Scenario 3 negative flow)
- `un` (Unassigned) — the **largest count** in the fixture (501); confirms no
  truncation/overflow in the device-count display at 360px (ties to TR-011)
- `a1` (Floor 1) — the **default-selected** instance on first render, with no
  visitor interaction yet (TR-008)

**Relationships**: none in the data model's own terms — the tree hierarchy
(Building A → Floor 1/Floor 2) is expressed only through the `prefix` display
string in the design source (`├─`, `│  ├─`, etc.), not through a parent-id
field. Tests assert the *displayed* tree shape (which labels appear, in what
visual nesting) rather than a data relationship, since no such relationship
exists to assert against.

**Lifecycle**: fully static, bundled with the build. Tests neither create nor
delete any `HierarchyNode` — read-only fixture, sourced once into
`automation/test_data/landing.json` from the table above so the suite has one
canonical copy to assert against rather than each test hard-coding values.

**State transitions worth exercising**: exactly one transition exists —
`selected` (which single node is currently shown in the detail panel).
Initial state: `a1` (Floor 1). Transition: clicking any node's `<button>`
moves `selected` to that node's `id`; exactly one node is selected at a time
(no multi-select, no deselection to "none"). Both the initial state and at
least one transition (to a different node, and to the zero-devices boundary
node `b`) are exercised in Scenario 3.

## Entity: AuthSession

Not a page-specific entity — the redirect behavior (TR-002) needs to know
whether *any* valid session exists, not any detail of what it contains.

| Field | Type | Notes |
|---|---|---|
| `authenticated` | boolean | The only fact this page's logic depends on |

**Lifecycle**: created via a real UI sign-in (R5) immediately before the
Scenario 2 test navigates to the root URL; the test's own teardown ends the
browser context, which discards the session — no explicit logout call is
needed since Playwright's `context` fixture is function-scoped and each test
gets a fresh one (constitution VI: every test creates and cleans up its own
state).

**No other entity exists for this feature** — there is no form, no
user-entered data, and no write path anywhere on this page.
