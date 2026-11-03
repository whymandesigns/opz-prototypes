# Operationalize — what the product is

Context for anyone, person or model, building a prototype here. It answers the
question a prototype cannot: **what is this feature for, who opens it, when, and
why does it work the way it does.**

It is deliberately static. Decisions about how a particular screen is built live
in that feature's own `PLAN.md`; this file is the background those decisions are
made against, and it should change only when the product does.

**Where the sections come from.** The side nav is the product's own map, so this
file follows it: one section per nav item. A nav item with no prototype yet still
gets a section, because knowing nothing has been designed is itself worth knowing.

> **Marked `TO FILL`** means nobody has written it down yet. Everything else is
> traceable to something in the repo — a `PLAN.md`, a spec quoted in one, or the
> prototypes themselves. Do not fill a gap by inferring from the UI: a prototype
> is a proposal, not a description of how the business works.

---

## Processes

**What it is** — the workflow / planning-cycle machinery: setting up a process,
running it, and watching it progress.

**Who uses it** — TO FILL
**When** — TO FILL
**Why it works this way** — TO FILL

**Prototypes** — the largest group, seven of them:
`operationalize-web-app` (the main app shell), `workflow-view`, `meeting-grid`
(planning-cycle meetings as week / month / calendar), `empty-states` (an empty
state per page), `admin`, `template-preview`, and `experiments/spotlight`
(help docs and feature launches).

---

## Initiatives

**What it is** — initiative definition, set-up and tracking, plus the live
dashboard for the Core Strategy forum.

**Who uses it** — Core Strategy leaders and initiative owners.
*(Source: `toptrack/PLAN.md`.)*

**When** — the dashboard is read in the Core Strategy forum; set-up and edit
happen outside it, when an initiative is defined or changes.

**Why it works this way** — from the TopTrack initiative definition (Sep 2026),
workstream **SP3 — Launch a Live Initiative Dashboard**. The four problems it
traces back to, quoted in `toptrack/PLAN.md`:

1. Initiative execution is inconsistent and manual.
2. Success depends on the owner's familiarity with Toptal's systems and standards.
3. Initiative management feels like a burden, not a driver of progress.
4. Core Strategy leaders run off Google Sheets that drift from TopTeam.

The MVP must be *"usable for Core Strategy forum with a focus on Core Strategy
initiatives, while retaining visibility to all remaining Initiatives"* — which is
why the dashboard splits Core Strategy from everything else rather than showing
one flat list.

**Prototypes** — `toptrack` (the dashboard; has a full `PLAN.md` — **read it
first**), `initiatives/` (set-up, edit and view across v1 drawer, v2 full screen,
v3 breadcrumb + People, with a version switcher), `csv-export` (bulk import from
a spreadsheet), `workspaces` (multi-tenant kick-off, shown over Initiatives).

---

## RoB Meetings

**What it is** — Rhythm of Business meetings: agendas, action items, follow-ups
and the connection between a meeting and the work it governs.

**Who uses it** — TO FILL
**When** — TO FILL
**Why it works this way** — TO FILL

**Prototypes** — `rob` (meeting action items, respond-via-menu), `action-trace`
(connects ActionTrace processes to an RoB meeting, then reviews worker recordings
with timeline annotations), `test` (a 34-board design canvas of the master
calendar: week view, propose / respond / decline, drag-to-move, custom Zoom
links), and five older flows under `archive/`.

---

## OKRs

**What it is** — objectives and key results, and the performance attributes
attached to them.

**Who uses it** — TO FILL
**When** — TO FILL
**Why it works this way** — TO FILL

**Prototypes** — `performance-attributes/` (OKR performance attributes, ticket
**TOP-7764**, across v1 Icarus rebuild and v2 master prompt, with a version
switcher).

---

## People

**What it is** — TO FILL
**Who uses it** — TO FILL
**When** — TO FILL
**Why it works this way** — TO FILL

**Prototypes** — none yet. The closest is `initiatives/v3-breadcrumb`, which adds
People to the initiative view, and `performance-reviews` (below), which is about
people but sits under its own nav item.

---

## Team

**What it is** — TO FILL
**Who uses it** — TO FILL
**When** — TO FILL
**Why it works this way** — TO FILL

**Prototypes** — none yet.

---

# Beyond the six

These have prototypes and their own nav items, so an agent will meet them.

## Performance reviews / My assessments

**What it is** — giving an assessment, and building a review cycle.

**Why it works this way** — from the v2.1 spec, *Launching Review Cycle*:
starting a cycle is **programmatic** — a backend engineer runs a script, and four
CSV files are required. The prototype designs the Admin page that replaces that
script. It is gated on the **`Administer Performance Reviews`** permission, since
v2.1 states all assessments are always visible to users with it.
*(Source: `performance-reviews/PLAN.md`, which has the data model from the 4 CSVs.)*

**Who uses it** — administrators with that permission, for cycle set-up;
everyone, for giving an assessment.

**When** — per review cycle.

**Prototypes** — `performance-reviews` (has a full `PLAN.md` — **read it first**).

## Integrations and Admin Settings

**What it is** — connecting external systems, and workspace-wide settings.

**Who uses it** — TO FILL
**When** — TO FILL
**Why it works this way** — TO FILL

**Prototypes** — `integrations/` (Connectors, Tableau streams, Admin Settings +
HireGlobal, API token management), `admin-toc` (workspace settings with a
contents rail), `admin`.

Two deliberate non-designmd rebuilds of the Admin Settings page live in
`experiments/`: one in stock Tailwind v4, one in shadcn/ui. They are custom-themed
UI kept for comparison — **leave them as they are** and do not migrate them onto
the kit.

---

## Keeping this honest

- A section's **Prototypes** list is the only part that goes stale. When you add a
  prototype, add it to the right section — that is how the next agent finds the
  reference implementation instead of rebuilding one.
- `PLAN.md` beats this file. Where a feature has one, it is the governing
  document for how that screen is built; this file only says why the feature
  exists at all.
- The side nav varies between prototypes — some use `Dashboard`, `Settings` or
  `My assessments` where others use the six above. The template's nav is the
  intended set; treat anything else as that prototype's own choice.
