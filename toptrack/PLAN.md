# TopTrack Dashboard — prototype plan

Planning doc for the **TopTrack Dashboard** prototype (`index.html`): the live
initiative dashboard for the Core Strategy forum, built on the icarus design system.

## Why this exists

From the TopTrack initiative definition (Sep 2026), workstream **SP3 — Launch a
Live Initiative Dashboard**:

> MVP: Must produce a live dashboard, usable for Core Strategy forum with a focus
> on Core Strategy initiatives, while retaining visibility to all remaining
> Initiatives.

The four problems it traces back to:

1. Initiative execution is inconsistent and manual.
2. Success depends on the owner's familiarity with Toptal's systems and standards.
3. Initiative management feels like a burden, not a driver of progress.
4. Core Strategy leaders run off Google Sheets that drift from TopTeam.

## Source material — and what governs

| Source | Status |
|---|---|
| `[RoB] [Initiative] TopTrack _ Sep 2026` (deck export) | **Governing requirement.** Objective, workstreams, charter fields, automations. |
| Concept v1 (screenshot) | Superseded. Two scope cards + tree table. |
| Concept v2 (screenshot, 2026-09-26) | **Governing layout.** Page-head toggle, one insights card, table grouped by objective. Treated as a wireframe — polished, not copied. |

## How this fits with `features/initiatives`

Decided 2026-10-01: **two linked prototypes, not one merged file.**

| Prototype | Owns |
|---|---|
| `features/toptrack` | The TopTrack Dashboard (this plan). |
| `features/initiatives` | Initiatives list + the **New initiative drawer** — the "current UI" that roadmap row 1 says to keep for MVP. **All P1 Set-Up / Edit work lands there.** |

- **Roadmap ID 1 — resolved (2026-10-01): keep the current UI.** The existing
  New initiative drawer (`#in-drawer-new`, Figma `20307:80788`) *is* the MVP
  set-up / edit surface. No separate set-up page. Every Set-Up / Edit row is a
  change to this drawer.

  | Roadmap ID | Item | Prototype status |
  |---|---|---|
  | 1 | Keep current UI vs new set-up page | **Resolved — current drawer** |
  | 2 | Core strategy switch (optional), below Description | **Built** (Figma `37186:491383`) |
  | 3 | Company strategic objective — shown only when Core strategy is on | **Built** — 2 objectives, with owner |
  | 6 | Executive sponsor — required person select, above Accountable owner | **Built** — error on Create, cleared on pick |
  | 8 | Beneficiary function moved under Executive sponsor | **Built** — out of "More details", always visible |
  | 9 | Beneficiary function required | **Built** (required only). Slack-naming part **parked** — see open question 9 |
  | 10 | Start date defaults to today | **Built** — reset to today on every open (roadmap marked it "Already exists"; prototype had a hardcoded date) |
  | 7 | Working team — multi-select people, required (≥ 1), under Project manager | **Built** — searchable photo picker (shared with Executive sponsor), checkmarks, stays open while picking; trigger shows up to 3 stacked avatars + "Name +N". Counts for both draft and publish. RACI relationship + FTE counts still open (question 10) |
  | 11 | Estimated duration — required, above Start date, fills End date | **Built** — < 1 month = +2 wks · 1 mo · 1–4 qtrs = +3/6/9/12 mo · 1 year / Requires scoping = +12 mo (End date always required — ID 18 decision). Start change recalculates; manual End date → Custom |
  | 12 | Initial impact date — next 8 quarters | **Built** — optional, after End date; current quarter + 7. (Parked 2026-10-01, restored 2026-10-02) |
  | 13 | Full impact date — next 8 quarters | **Built** — optional; quarters before Initial hidden, cleared if now earlier. (Restored with ID 12) |
  | 18 | Save & publish — required list | **Partly built** — enforced now: Name, Executive sponsor, Beneficiary function, Accountable owner, Project manager, Estimated duration, Start date, End date (+ Description's 100-char minimum). Problem / Opportunity (19), Objective(s) (20) and Success Metrics (21) added. Working team (7) added. Still to add: Related Initiatives (22) |
  | 17 *(P3)* | Save as draft | **Built** — secondary button far left of the footer. **No validation** (2026-10-02): a draft saves at any point, even empty ("Untitled initiative"), and clears any errors on screen. Lands **pinned first** in the Initiatives table, greyed out, dark **Draft** tag; re-saving / publishing updates the same row. **Draft rows are clickable** (mouse or Enter): the drawer reopens with everything the draft had. "Create Initiative" always opens a blank form. Not built: hidden-by-default views |
  | 19 | Problem / Opportunity — required, 2–3 lines | **Built** — below Description, ⓘ carries the roadmap helper text, 500-char cap with counter |
  | 20 | Objective(s) — required, 3 boxes, add / remove / reorder | **Built** — reusable multi-entry list: numbered rows, sample placeholders, + Add, × (last row protected), drag handle + Alt+↑/↓, Enter adds a row. Required = ≥ 1 filled |
  | 21 | Success metrics — required, 3 boxes, add / remove | **Built** — same list as Objective(s), numbered for consistency (user call; roadmap sample is unnumbered) |
  | 5 | Duplicate / related notice | **Built (prototype rule)** — designmd `.alert-warning` (yellow, warning icon) above Health: "Sounds like this relates to another initiative already in TopTeam." Shows only when the name contains **"partner"** (any case), and points at **Partner Enablement Program** — a real seed row in the Initiatives table (Sales · In progress · Aisha Khan, 2 projects); the match line reads that row. Real fuzzy matching on name / description / objectives still to design with ID 22 |
  | 22 | Related & duplicate initiatives section | Not started |

  **Drawer → table (2026-10-02):** Create and Save as draft add the initiative to
  the Initiatives table as a **top-level row** — name, Beneficiary function,
  status (drawer stage, or *Draft*), health, Accountable owner, End date as
  roadmap, today as created. Saving a draft again or publishing it updates the
  same row (no duplicates). Count badge updates; the page scrolls to the row and
  it flashes once. Success toast on both. **Ordering:** everything added from the
  drawer (drafts and newly created) is pinned above the seed rows, most recent
  action first — the row you just saved is always first, whatever the sort.
  **Reopening:** every row the drawer made is clickable (mouse, or Enter / Space).
  Drafts reopen in draft mode; published ones reopen in edit mode — primary
  button reads **Save changes**, Save as draft is hidden, and saving updates the
  same row (toast: "… updated."). Seed rows aren't editable yet.

  **View mode (2026-10-02)** — Figma *Drawer / Regular* `20327:41665`, extended
  with the TopTrack fields. A second, read-only drawer:
  - Header: title, Initiative + stage tags, "Last edit was made … by …", copy-link
    and close.
  - **Overview** tab: label · value rows (Health tag, Executive sponsor /
    Accountable owner / Project manager as avatar + name + role, Beneficiary
    function, Working team stack + names, duration, dates, impact quarters,
    Core strategy + objective); Description, Problem / Opportunity, numbered
    Objective(s) and Success metrics; Connections, Documents, Projects sections
    (placeholders: "Not connected", "No documents yet", "Add project").
  - **Activity log** tab: created / published / edited / draft entries with times.
  - Footer CTA **Edit initiative** → edit drawer ("Save changes") → back to view.
  - Flow: a successful **Create** lands on the **table** (new row pinned first,
    toast) — clicking that row opens view mode. Saving an *edit* returns to
    view mode, where the edit started. Drafts still open straight into edit. Empty values show "—".

  **States switcher — `features/initiatives/?states=1`** (2026-10-02). Floating
  window, same look as toptrack's. Each state reloads with `&state=…` and
  replays the real UI steps, so every state starts clean:
  - *Table:* Default · Drafts + created rows · No initiatives · Search, no
    results · Long text
  - *Create drawer:* Blank · Required errors · Duplicate notice · Filled, ready
    to create
  - *Draft & edit:* Draft reopened · Edit (Save changes)
  - *View mode:* View — all fields · View — required only · View — activity log


  **ID 18 decisions (2026-10-01):** keep Health, Connections, More details and
  Core strategy (not in ID 18's list, but stay — optional). Keep Description
  *and* add Problem / Opportunity alongside it. End date is always required.

- Sidenavs are cross-linked: toptrack *Initiatives* → `../initiatives/`;
  initiatives *Dashboard* → `../toptrack/`. Each side only blocks its own
  decorative `href="#"` items.
- **Not yet:** dashboard-row → initiative-drawer deep links, and a shared mock
  dataset (toptrack has 48 initiatives, initiatives has 24). Data reconciliation
  is deferred.

## The core design change

**Core Strategy stops being a free-text tag.** Today owners tag initiatives
"Core Strategy" by hand, and a tag can be spelled anything. TopTrack asks the
owner at set-up: *is this a Core Strategy initiative?* The answer becomes a
yes/no metadata field that the dashboard filters on.

- Projects and sub-projects **inherit** the flag from their initiative.
- They also inherit the initiative's **company strategic objective**.

## Locked decisions

- **Shell is frozen.** Topbar, sidenav (with the *Dashboard* item) and page head
  stay as scaffolded. Content work only — except page-head changes the user asks
  for directly.
- **Page head:** "TopTrack Dashboard" + scope toggle + ⋮ menu. No subtitle, no action buttons.
- **Scope toggle:** `Core Strategy N | Other initiatives N` segmented control.
  Exactly one side is always active — there is no "all" view. Lives in the
  page head, left of the ⋮ menu.
- **Insights count every item in scope** — initiatives + projects + sub-projects.
  (Concept v2 superseded the earlier initiatives-only roll-up.)
- **Health % = On track ÷ all items**, Not active included, as designed.
- **Not active is neutral grey** everywhere — never blue, which is Execution.
- **Status → tag colour** follows designmd's sheet renderer: Execution blue,
  Impact assessment cyan, Complete green, everything else light grey.
- **Table columns:** Company strategic objectives · Area of work · Description ·
  Status · Health · Owner. No weekly-update columns in V1.
- **Initiatives start collapsed**; chevrons reveal projects and sub-projects.

## What's built

### Page head
- Title + scope toggle + ⋮ menu (Export as CSV, Copy link to this view, Dashboard settings) —
  menu items are visual only.

### Insights card
1. **Summary strip** (muted header row)
   - Hierarchy counts: `4 Objectives › 5 Initiatives › 14 Projects › 16 Sub-projects`.
     Carets read as "contains".
2. **Health pane**
   - Headline "Health" + "74% on track".
   - Thin 8px stacked bar, no text; segments are clickable filters.
   - Legend: designmd `.tag.tag-indicator` (Figma *Tag Rectangle*,
     `37361:265263`) — dot · bold count · label:
     `26 On track · 3 At risk · 0 Off track · 6 Not active`. Clickable filters;
     zero-count tags are disabled.
3. **Status pane**
   - Headline "Status" + "Select a bar to filter the table".
   - Column chart, all 8 statuses including zeros; On hold / Cancelled set
     slightly apart from the active pipeline.

### Toolbar + table
- Search (name, owner, function, objective), table-settings icon, view toggles
  (wide / narrow / sheet — visual only; sheet is the one built view).
- Filter chips for active status / health filters, with "Clear all".
- Read-only `.table-sheet` tree: objective cell spans its group; initiatives
  bold; header chevron expands / collapses everything.

### Interactions
| Action | Result |
|---|---|
| Switch scope | Counts tween, bars slide to new sizes, table re-cuts. |
| Click a health segment or pill | Filters table by health; others dim; chip appears. |
| Click a status column | Filters table by status; others dim; chip appears. |
| Status + health together | Filters combine. |
| Search | Keeps matches plus their ancestors (and subtree of matching parents). |
| Filtering | Ignores collapse so matches are always visible. |

Motion respects `prefers-reduced-motion`.

### States (`?states=1`)
Default · Loading · Load error · No initiatives · No Core Strategy initiatives ·
Long text · Search, no results.

## Mock data

- 48 initiatives — 5 Core Strategy, 43 other — 108 rows with projects and
  sub-projects. Fictional people.
- **Objectives are placeholders.** Seven invented company objectives; Core
  initiatives are mapped by name, others by function. Swap in the real list.

| Objective | Fed by |
|---|---|
| World-Class Talent Operations | Talent Operations |
| Services Strategy Execution | Customer Operations, Product |
| Enterprise Growth | Sales |
| Operational Excellence | Finance, Legal |
| Brand & Demand | Marketing |
| People & Culture | People Ops |
| Platform Reliability & Security | Engineering |

## designmd gaps (fixed locally, worth fixing at source)

| Component | Problem | Local fix |
|---|---|---|
| `.sidenav`, `.sidenav-item`, `.page-head` | Light primitives (gray-150/200) stay light in dark mode | Re-pointed at `--color-surface-muted` / `-sunken` / `--color-border` |
| `.tag-light` | gray-200 fill + `--color-text` → white on near-white in dark | `--tag-color: var(--color-surface-muted)` |
| `.segmented-item.is-active` | graphite-700 + text-inverse → label vanishes in dark | Inverted fill in dark |
| `.tag-indicator` | Figma's Tag Rectangle has a resting grey fill; designmd's is transparent until hover | `background: var(--color-surface-muted)` on the legend tags |
| `.alert`, `.btn` | `display: flex` beats `[hidden]` | `.alert[hidden] { display: none }` |
| `[data-tooltip]` | CSS-only `::after` is clipped by scrolling containers (`.drawer-body` has `overflow-y: auto`) and never wraps | In drawers: pseudo-element off, same compact tooltip drawn in a fixed layer on `<body>`, wraps at 260px, flips/clamps to viewport (features/initiatives) |
| `.cell-avatar` vs `.avatar` | Table rows still use the round `.cell-avatar`; the squared `.avatar` (radius 0) shares its `surface-muted` fill with `.table-wide`'s zebra stripe, so it vanishes on striped rows | Initiatives table uses `.avatar.avatar-md` with a `surface-sunken` fill (features/initiatives) |
| `.input-select-trigger` | No `.is-error` state (`.input` has one) | Local `.input-select-trigger.is-error` mirroring `.input.is-error` (in features/initiatives) |
| — | No meter / column chart component | Health bar + status chart are local, built on `--tag-color` / `--tag-text` |

## Open questions

1. **Who can set the Core Strategy flag?** Owner self-declares, admin-only, or
   owner suggests + approval? The deck has Jo/Dima tagging from an agreed list.
2. **Can a project differ from its initiative's flag?** Currently strict inheritance.
3. **Real objective list** — and does Strategic Pillar (Operationalize "Parent
   Name") map to it?
4. **Migration of existing tags** ("Core Strategy", "core strat", …) onto the field.
5. **Does the business-line switcher narrow the dashboard?** (Concept topbar has
   "All Business Lines".)
6. **Freshness** — "live" is undefined in the deck; should the dashboard show
   last-updated per row or overall?
7. **Weekly update** (Progress since last week / Next steps) — out of V1; where
   does it land in V2?
8. **What should the view toggles do** — wide vs narrow vs sheet?
9. **ID 9 Slack nomenclature** (`-c-init-gtm-crusade` for Customer) — does the
   Beneficiary function name a *newly created* Slack channel, or does it apply
   when *connecting an existing* channel (the drawer's Connections → Slack)?
   Also needs the function → code list (only Customer → `gtm` known), and
   "Customer" isn't in the drawer's function list (it has Customer Success).
10. **ID 7 Working Team** — how does it relate to RACI (separate list, drawn
    from RACI, or replacing part of it)? The row itself says "discuss before
    implementing". Also: picker design (proposed: multi-select of the sponsor
    picker + removable avatar row) and how it feeds FTE counts.
11. **IDs 12–13 Initial / Full impact date** — what do they relate to (impact
    on what — revenue, an OKR, the objective)? Restored in the drawer as
    optional fields while this is answered.

## Next

- Confirm open questions 1–3 with Joanna / Dima.
- **P1 Initiative Set-Up / Edit** — built in `features/initiatives`' New
  initiative drawer, per the roadmap CSV (`TopTrack Roadmap Data - Detailed Rows`).
- Reconcile the two datasets, then add dashboard-row → drawer deep links.
- Weekly update approval flow (Monday 9:00 EST owner review).
- Before sharing: `python3 inline.py ../features/toptrack/index.html` from `designmd/`.
