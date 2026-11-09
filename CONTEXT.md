# Operationalize — what the product is

Context for anyone, person or model, building a prototype here. It answers the
question a prototype cannot: **what is this feature for, who opens it, when, and
why does it work the way it does.**

It is deliberately static. Decisions about how a particular screen is built live
in that feature's own `PLAN.md`; this file is the background those decisions are
made against, and it should change only when the product does.

## Three sources, in this order

Two different things are true about Operationalize, and they disagree in places.
**The software enforces one set of rules; Toptal's Operating Framework asks
people to follow another.** Both are real. Confusing them is how a prototype ends
up blocking something the product allows, or allowing something the framework
discourages without saying so.

| | Answers | Where | Authority |
|---|---|---|---|
| **1. The test oracle** | what the product **does** | `topteam/test-oracle/` | the source of truth for behaviour and for what things are called on screen |
| **2. Framework policy** | what people are **asked** to do | Part 2 of this file, labelled *Policy* | shapes defaults, empty states, guidance and copy — never a rule the screen enforces |
| **3. Our prototypes** | what we have **designed** | Part 3 of this file, and each `PLAN.md` | a proposal, not a description of the business |

**Where policy and product differ, design for the product and let policy set the
default.** If the product allows monthly RoBs and the framework prefers weekly,
the form defaults to weekly and still offers monthly — it does not remove it.

### Asking the oracle

`toptal/topteam` is the real platform. In Toptal's working layout a read-only
clone sits beside `icarus/`, and its `test-oracle/` folder is the product's
behaviour spec: about 4,500 cards across 29 modules — rules, known bugs and open
questions, each cited to code, tickets or a PO decision.

```bash
topteam/test-oracle/search/spec search "who is invited when an item is linked to a RoB"
topteam/test-oracle/search/spec rule ROB-LINK-001
```

The same index is available to Claude as an MCP server (`search_oracle`,
`get_rule`, `rules_for_code_path`) where it is configured. The global glossary
is §7 of `test-oracle/00-system-overview.md`.

- **A rule card states intended behaviour.** When the code deviates today it
  says so in an *Observed today* line — design for the rule, and know the bug
  is there.
- **Cards are pinned to a baseline** (`f488203`, Oct 30, 2026). Where it matters,
  check `front-end/src/` for what ships now.
- **It knows nothing about our prototypes**, and its README asks that it stay
  inside the team: cite rule IDs here, don't copy its prose in.

> **Marked `TO FILL`** means nobody has written it down yet. Do not fill a gap by
> inferring from a prototype — ask the oracle, or leave it.

---

# Part 1 — Product facts prototypes keep getting wrong

Checked against the oracle on 2026-11-09. Not a summary of the product — just
the facts that earlier versions of this file, or earlier prototypes, stated
differently. Each row cites the rule to re-check before relying on it.

| Topic | The product does | Rule |
|---|---|---|
| **Linking a RoB** | Each work item (Initiative, Project, Sub-project, Process, Activity, Sub-activity) links to **at most one** RoB. One RoB links to **any number** of items, regular and Process mixed. | `ROB-LINK-001` |
| **Recurrence** | Every RoB is a recurring series — there is **no "Does not repeat"**. The create form **defaults to Every weekday**. Quick options: Every day, Every weekday, weekly on the date's weekday, monthly on the Nth or last weekday, yearly, and **Custom**. | `ROB-SCHED-001`, `-002`, `-004` |
| **Kinds of RoB** | "Initiative RoB" and "Process RoB" are **not chosen** — the kind is derived from the linked items, and only the meeting deck uses it. A RoB linked only to Projects or Activities, or to nothing, is neither. | `ROB-LINK-004` |
| **Who is invited** | Linking an item auto-invites its RACI, by the **item's own auto-invite settings** (which RACI kinds, on or off). Per a PO decision of 2026-11-02 the default kinds are Accountable, Responsible and Consulted. Auto-invite only ever adds people; attendees are edited on the RoB itself. | `ROB-LINK-024`, `-027`, `Q-028`, `ROB-HIST-010` |
| **Creating from an item** | Intended: start a RoB from an Initiative or Process item, pre-named *"[RoB] <item name>"* and pre-linked. *Observed today:* only the RoB page opens the create form. | `ROB-CREATE-004` |
| **Slack channels** | A RoB inherits the Slack channels of all its linked, non-archived items. | `ROB-SLACK-002` |
| **What the levels are called** | On Operationalize-branded tenants the top level is **"Process"**, then **"Activity"**, **"Sub-activity"**. Only Toptal's own TopTeam-branded tenant shows **"BAU"**. Code and the RoB glossary say *BAU* and *Focus area* — never on screen here. | `BAU-TERM-001` |
| **"RoB"** | The product calls them **RoBs** on screen — *"Label RoBs only"*, *"[RoB] <item name>"*. | `ROB-VIEW-133`, `ROB-CREATE-004` |

## A note on the word: Processes, not BAU

Older source material — the training material, the code, the oracle's own rule
IDs (`BAU-*`) — says **BAU** (business as usual). Operationalize's screens say
**Process** (`BAU-TERM-001`), so **write Processes everywhere** in prototypes:
copy, headings, comments, class names.

One trap: a few prototypes say "the designmd BAU toolbar", meaning the standard
or default toolbar. That is an unrelated use of the abbreviation and must not be
swept into "Processes".

---

# Part 2 — The operating framework *(Policy)*

> **Everything in this part is policy**: Toptal's Operating Framework training
> material, supplied 2026-11-03 and 2026-11-04. It says what people are asked to
> do, not what the software prevents. Use it for defaults, empty states, helper
> text and the shape of a flow — and check Part 1 or the oracle before turning
> any of it into a constraint.

Every feature here hangs off one model. Toptal **runs** the business through
Processes and **changes** it through Initiatives, and RoB meetings are what move
both forward. A screen that does not serve one of those three is probably in the
wrong place.

| | Processes | Initiatives |
|---|---|---|
| Purpose | run the business | change the business |
| Shape | a Process (the training material says *Focus Area* — typically a sub-function within a function) and its Activities and Sub-activities | a group of Projects, sometimes Sub-projects |
| Ownership | defined by RACI | a **Beneficiary Function**, which gains from the outcome, and an **Accountable Function**, which owns and drives it |
| OKRs | may or may not support one | supports an OKR, with specific Key Results as targets |
| Measured by | KPIs showing day-to-day performance | its Key Results |
| Time | ongoing | start and end dates |
| Delivered as | Activities and Sub-activities | Projects and Sub-projects |
| RoB, by policy | at the **lowest** level — each Sub-activity, or the Activity if it has none | one, at the **Initiative** — its Projects and Sub-projects link to it |
| Cadence, by policy | weekly or bi-weekly; monthly by approved exception | weekly or bi-weekly |
| RoB drives | business KPIs | the Initiative's OKRs |

Three things make the framework work, and all three show up in the product:

**Accountability.** Roles are assigned with **RACI**, across Functions,
Divisions, Processes, Initiatives and RoB meetings alike:

- **R — Responsible**: carries out the activity or assignment.
- **A — Accountable**: holds decision authority, and is the *singular* owner.
- **C — Consulted**: asked before a decision is made or an assignment completed.
- **I — Informed**: kept in the loop on decisions, outcomes and status.

Anywhere the UI shows ownership, Accountable is one person.

RACI is also how **working teams** are formed. A team either drives an Initiative
by delivering its Projects and Sub-projects, or runs a Process by delivering its
Activities and Sub-activities — and its RoB meeting is where that team works.

The **Accountable Owner** is the A for an Initiative or a Process: the sole owner,
responsible for setting up the Initiative or Process *and its RoB* so the working
team is ready to succeed, and for leading that RoB. The Initiative cannot progress
unless its Accountable Owner runs an effective RoB — the source is that blunt.

**RoB meetings.** Structured recurring meetings on a set cadence, tied to
important areas of the business. They exist to drive continuous progress on
Process Activities and Sub-activities, or on Initiatives, Projects and
Sub-projects. They are the mechanism, not a side feature.

**TopTeam.** The training material calls TopTeam the central hub for company
operations — planning, tracking and managing Processes, Initiatives and their
RoB meetings. In product terms TopTeam is the name Toptal's own tenant of this
same platform carries; Operationalize is the brand everyone else sees. Where a
prototype implies data comes from somewhere, that somewhere is this platform.

---

# Part 3 — The features, and what we have prototyped

The side nav is the product's own map, so this part follows it: one section per
nav item. A nav item with no prototype yet still gets a section, because knowing
nothing has been designed is itself worth knowing. Lines marked *Policy* come
from Part 2; everything else is traceable to the oracle, a `PLAN.md`, or the
prototypes themselves.

## Processes

**What it is** — the day-to-day activities that run the business: a **Process**,
and beneath it the **Activities** and sometimes **Sub-activities** that make it
up. In the product this is also the workflow and planning-cycle machinery:
setting a process up, running it, and watching it progress.

**How it is measured** — specific **KPIs** that show the day-to-day performance
of the business. Unlike an Initiative, a Process has no end date; it is ongoing,
and the question is how well it is running rather than how far along it is.

**Relationship to OKRs** — a Process *may or may not* support one. Do not build
screens that assume it does.

**Its RoB** — any Process, Activity or Sub-activity can link to one RoB
(`ROB-LINK-001`). *Policy:* set it up at the **lowest level** of the tree, so each
Sub-activity has its own recurring RoB, or the Activity if it has none, and every
review, decision and assignment about that item happens there.

**Who uses it** — the working team, which is the Process's RACI, set up and led
by its Accountable Owner. *(Which of them opens which screen, and how often, is
not yet written down.)*
**When** — continuously. *Policy:* the team meets weekly or bi-weekly in its RoB.

**Prototypes** — the largest group, seven of them:
`operationalize-web-app` (the main app shell), `workflow-view`, `meeting-grid`
(planning-cycle meetings as week / month / calendar), `empty-states` (an empty
state per page), `admin`, `template-preview`, and `experiments/spotlight`
(help docs and feature launches).

---

## Initiatives

**What it is** — a group of projects, and sometimes sub-projects, that together
achieve a "change the business" goal. Every Initiative has a **Beneficiary
Function** that gains from the outcome and an **Accountable Function** that owns
and drives it, **supports an OKR** with specific Key Results as its targets, and
has **start and end dates**. In the product: initiative definition, set-up and
tracking, plus the live dashboard for the Core Strategy forum.

**Who uses it** — Core Strategy leaders and initiative owners
*(source: `toptrack/PLAN.md`)*, and the working team — the RACI of the Initiative
and its Projects — led by the Accountable Owner.

**Its RoB** — the item form's Meetings block links an Initiative, Project or
Sub-project to one RoB (`INIT-ROB-001`, `ROB-LINK-001`). *Policy:* one RoB, at
the Initiative level. Projects and Sub-projects link to it, and discussion about
them happens there and in the Initiative's Slack channel. A Project-level RoB is
reserved for exceptionally large, complex projects, with approval from the leader
of the Accountable Function — the product does not check for that approval.

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

**What it is** — Rhythm of Business meetings: recurring meeting series, each
linked to the work it governs. Agendas, action items, follow-ups, recordings and
the connection between a meeting and its Initiatives and Processes. The oracle's
`rob` module is the largest in the spec — query it before designing any of this.

**What the product enforces** — see Part 1. In short: always recurring, default
Every weekday, monthly and custom available (`ROB-SCHED-001/002/004`); a RoB can
cover many items, an item has at most one RoB (`ROB-LINK-001`); the kind is
derived, not chosen (`ROB-LINK-004`); invitees come from each linked item's RACI
by its auto-invite settings (`ROB-LINK-024`).

**What the framework asks** *(Policy)*

- **Purpose.** A RoB exists to drive continuous progress on Process Activities
  and Sub-activities, or on an Initiative and its Projects. A meeting is always
  *about* something in one of those two trees.
- **Who.** The working team — the RACI of the Initiative and its Projects, or of
  the Process item. The **Accountable Owner leads it**.
- **Where it sits.** One per Initiative; for a Process, one per lowest-level
  item. Project-level RoBs only for exceptionally large projects, with approval.
- **Cadence.** Weekly or bi-weekly. A Process RoB may run monthly by exception,
  with approval from the Accountable Function's leader. The source states that
  exception for Process RoBs only.

**How a RoB runs** *(Policy)* — the same for both kinds:

1. A **quick** round of status updates — the prelude, not the point.
2. Then a **working session**: robust discussion that ends in **decisions and
   actions**. For an Initiative those serve its OKRs; for a Process they drive
   its business KPIs.
3. Discussion stays on the **agenda**, and true to the meeting's purpose — which
   is defined by its **name and description**.
4. Each kind follows its own **format and template**, designed to make that kind
   of RoB effective. *(The templates themselves are not yet written down here.)*

**What follows for a screen** — where the two layers meet:

- **Default to the policy; don't remove what the product allows.** The create
  form can start at *weekly*, but monthly, daily and Custom stay available —
  the product offers them (`ROB-SCHED-004`). Today's product
  default is Every weekday (`ROB-SCHED-002`); a prototype that proposes a
  different default is proposing a product change, and should say so.
- **Never offer "Does not repeat".** A RoB is a recurring series in both layers
  (`ROB-SCHED-001`).
- **Linking is many-to-one.** A RoB picker on an item selects one RoB; a RoB's
  connections list can hold many items, mixed (`ROB-LINK-001`). A design that
  forces one parent per RoB is stricter than the product.
- **Guide toward the right level, don't block the others.** Offering "Create
  RoB" from an Initiative is the policy's happy path; a Project can link to a RoB
  too, and the screen can say that is the exception rather than hide it.
- **Don't ask the user to choose a RoB "kind".** It follows from what is linked
  (`ROB-LINK-004`).
- **Invitees are seeded from the RACI**, through the linked item's auto-invite
  settings (`ROB-LINK-024`) — show where they came from, and let the list be
  edited. Removing a RACI role does not remove the attendee (`ROB-LINK-027`).
- **The output of a meeting is decisions and actions.** Status is the short
  prelude; a design that centres the status update has the emphasis backwards.
- **Name and description carry the purpose**, and the agenda keeps the
  discussion on it — they are load-bearing fields, not optional metadata.

**Prototypes** — `rob` (meeting action items, respond-via-menu), `action-trace`
(connects ActionTrace processes to a RoB meeting, then reviews worker recordings
with timeline annotations — the oracle covers this as *label RoBs*,
`ROB-LINK-046`), `test` (a 34-board design canvas of the master calendar: week
view, propose / respond / decline, drag-to-move, custom Zoom links), and five
older flows under `archive/`.

---

## OKRs

**What it is** — objectives and key results, and the performance attributes
attached to them.

**How it connects** — an Initiative supports an OKR, and that OKR's **Key
Results** are the Initiative's targets. A Process may or may not support one. So
OKRs are not a separate reporting layer bolted on top: they are what makes an
Initiative measurable, and the link runs Initiative → OKR → Key Results.

**Who uses it** — TO FILL
**When** — TO FILL

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

## Beyond the six

These have prototypes and their own nav items, so an agent will meet them.

### Performance reviews / My assessments

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

### Integrations and Admin Settings

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

- **Before stating how the product behaves, ask the oracle and cite the rule.**
  A claim here without a rule ID is policy or inventory, and should read like it.
- **Policy stays labelled.** When adding framework material, put it in Part 2 or
  mark it *Policy* where it appears — never as a constraint the screen enforces.
- A section's **Prototypes** list goes stale fastest. When you add a prototype,
  add it to the right section — that is how the next agent finds the reference
  implementation instead of rebuilding one.
- `PLAN.md` beats this file for how a screen is built; this file only says why
  the feature exists at all.
- The side nav varies between prototypes — some use `Dashboard`, `Settings` or
  `My assessments` where others use the six above. The template's nav is the
  intended set; treat anything else as that prototype's own choice.
