# Assessment Builder — prototype plan

Planning doc for the **builder** half of the Performance Reviews prototype: the
admin UI that replaces today's "file a ticket → engineer runs a script" process.
The reviewer-facing half (Assessments hub + Give Assessment) is already built in
`index.html`.

## Why this exists

v2.1 spec, *Launching Review Cycle*:

> Starting a cycle is **programmatic**: a backend engineer runs a script (in the
> future, this will be possible in the UI via a dedicated Admin page). For that,
> **4 CSV files are required**.

This prototype designs that "dedicated Admin page". Gated on the
**`Administer Performance Reviews`** permission (v2.1: *"All assessments are always
visible to users with the special permission"*).

## Source material — and what governs

| Source | Status |
|---|---|
| `Assessments … Version 2.1.md` | **Governing spec.** The 4-CSV model is the contract. |
| `Assessments … Version 2.0.md` | Historical only — superseded ("we've reworked…"). |
| Figma `hMZ8Nw27ub8PaIgPa0fgJf` node `33498:80831` | **No builder design exists.** All 10 frames are results/reporting screens. The newest canvas item (added 2026-08-19 21:11) is a *screenshot of the Vercel prototype*, pasted as reference. |
| `perf-review-proto-1.vercel.app` | **The v2.0 legacy tool** — its own sidebar says "legacy tool — static prototype". Shows what's being replaced, not the target. |

So: **designed fresh** against the icarus design system, with IA cues borrowed
from the prototype where they're genuinely good.

### What the prototype gets right (worth porting)

- **"Choose an existing one or type a new name"** — one control that either picks
  a library competency or creates one inline. Title + short description + Add.
- Competency rows as cards with name + description + a destructive action.
- `required` badges on questions.

### What the prototype has that v2.1 does NOT

> ⚠️ **Reversed 2026-08-19.** These were dropped in Phase 1 as v2.0-only, then
> deliberately reinstated for Phase 2 on Matt's call. See *Roles* and
> *Templates* below. Kept visible here so the reintroduction reads as a decision
> rather than drift.

- **Templates + Base Template inheritance** and the `inherited` badge
- **Regular / Newcomer** template variants
- Per-org-unit / per-job-level competency definitions (a v2.0 concept)

## Locked decisions

- ~~**Reuse model: persistent library, no inheritance.**~~ **Superseded
  2026-08-19** — templates are in. The library still exists underneath
  (individual competencies are shared across templates); templates sit *on top*
  of it as named, taggable bundles. See *Templates* below.
- **Questions ARE included** — Review Questions (asked of reviewers) and Goal
  Questions, each with a `required` flag. ⚠️ **This extends beyond v2.1**: no CSV
  column carries questions, so this is a *proposed* capability needing backend
  support, not a spec'd one. Called out as such in the UI review step.
- **Anchor flow:** admin launches a cycle end-to-end (the happy path below).
- **One competency set per cycle** — see Deliberate simplifications.

## Data model (from the 4 CSVs)

```
CompetencyGroup   id, name, description
Competency        id, name, description, group_id?
RatingScale       id(name), rows[{ id, value, label, color? }]
Participant       reviewer, reviewee, starts_on, ends_on,
                  competency_ids[], rating_scale_ids[],
                  available_for_reviewee_on?, available_for_managers_on?
Question   ⚠️ex   text, type(review|goal), required   ← extension, not in CSVs
```

Visibility semantics (v2.1, both date fields): submitted after the date → visible
immediately · **blank → never visible** · same as `Starts_on` → visible on submit.
The blank-means-never case needs to be unmistakable in the UI — it's the one
setting that silently hides results forever.

## Happy path — Launch an assessment cycle

Entry: **Assessments** hub → `New assessment cycle`. A 5-step `.stepper`.

**Step 1 · Setup**
- Cycle name (e.g. "H2 2026 — Engineering")
- Assessment window: `Starts_on` / `Ends_on` (defaults for every pair)
- Visibility: `Available_for_reviewee_on`, `Available_for_managers_on`, each with
  an explicit *"Never visible"* choice rather than an empty field

**Step 2 · Competencies**
- Pick from the library, grouped by competency group; or add inline via the
  choose-or-type control (name + description + group)
- Manage groups inline (name + description)
- Running count: "6 competencies across 2 groups"

**Step 3 · Scale & questions**
- Rating scale: pick a saved named scale, or build one — rows of value + label +
  optional colour swatch. Preview renders the scale as the reviewer will see it.
- Questions ⚠️: Review Questions and Goal Questions, each row text + `required`
  toggle. Empty is valid — the whole section is optional.

**Step 4 · Participants**
- Add reviewer → reviewee pairs manually, **and/or** bulk-upload a CSV
  (reuse the upload → preview → confirm pattern from `features/csv-export`)
- Table shows relationship type(s) *derived* per pair (v2.1: derived from org
  structure, not authored) — Self / Manager / Direct Report / Indirect Report /
  Teammate / Peer / RACI Member / Custom, multiple allowed per pair
- Per-row override of dates + visibility for the exceptions
- Guard the obvious own-goal: a reviewer/reviewee duplicate pair

**Step 5 · Review & launch**
- Summary: N participants · M competencies · scale name · window · visibility,
  with questions flagged as a proposed extension
- `Launch` → success confirmation. This is the moment that replaces the ticket.

## Deliberate simplifications (call these out, don't hide them)

- **One competency set + one scale for the whole cycle.** v2.1's `Competency_IDs`
  and `Rating_scale` are *per row*, so pairs could in principle differ (the spec's
  own sample does exactly this — Michael assesses John on 6 competencies where
  Alice and Jack use 4). The happy path picks one set for all; per-pair variation
  is left to the per-row override in Step 4 rather than designed as a first-class
  flow. **Open question — is per-pair variation a real need?**
- Relationship types are shown as derived but hardcoded per mock row (no org data).
- No persistence: library "saves" live in-page only.

## Roles (added 2026-08-19)

Three roles, plus one surface the three don't name.

| Role | Scope | Spec backing |
|---|---|---|
| **Admin** | Builds templates, runs cycles, sees everything | **Strong.** v2.1: *"All assessments are always visible to users with the special permission 'Administer Performance Reviews'."* The Admin page is v2.1's own stated future. |
| **Reviewer** | Gives assessments on assigned pairs | **Strong.** v2.1: *"anyone can review anyone."* |
| **Manager** | Sees how their team is faring; reads what peers said | **Access: yes. Analysis: no.** v2.0: *"Managers can access assessments and peer feedbacks for their reports."* v2.1 date-gates it via `Available_for_managers_on` → *"the direct manager and all managers up the reporting chain."* The roll-up/analytics layer is net-new. |

**Reviewer is not a permission.** Relationship type is derived *per pair*, so the
same person is reviewer in one row and reviewee in another. It's a hat worn per
assessment, not a role held — so it must not gate navigation the way Admin does.

**Manager scope = report chain.** The legacy tool confirms the mechanic: an
`Enable admin view` toggle with *"By default only people in your report chain are
shown."* Same model here — manager sees their chain, admin toggles to all.

**The unnamed fourth surface: reviewee receiving results.** Date-gated by
`Available_for_reviewee_on`, plus self-assessment (`Self` is a relationship
type). "My Results" was removed from the nav on 2026-08-19; if roles are being
formalised this needs a decision rather than staying dropped.

## Templates (added 2026-08-19)

Reinstated from v2.0 / the legacy tool. **Rationale:** v2.1's free-form model is
maximally flexible but unusable at scale — with no templates an admin
hand-assigns `Competency_IDs` per row for hundreds of pairs, which is exactly why
launching still needs a CSV and an engineer. v2.1's own sample already varies
competency sets per pair (Michael gets 6, Alice and Jack get 4), so per-pair
variation is the reality; templates are how it gets managed. **This also resolves
open question 1.**

Structure, per the reference:

- A template is a **named bundle of competencies + questions**, drawn from the
  shared library.
- **Tags/labels** on each: `base` (merged into every other template) and
  `universal` (no per-cycle-type variants).
- **Base Template** — *"define global values or culture areas all team members
  are evaluated on. Items here are combined with each employee's role-specific
  template."* Its items show an `inherited` badge in child templates, and can be
  hidden/revealed (`Show 4 inherited`) but not deleted from the child.
- **Role templates** — Design, Engineering, Management, Marketing, etc.
- **Variants** — non-universal templates split `Regular` / `Newcomer`, each with
  its own competency subset (Engineering Newcomer drops System Design and
  Mentorship).
- Templates carry **questions** too (review + goal, each with `required` and
  `inherited` flags) — which is where the questions already built into the wizard
  belong.

**Cycle mechanic:** each reviewee resolves to Base + their role template (+
variant). That's what replaces per-row competency picking. ⚠️ *How* the role
template is chosen — once per cycle or per participant — is still open; see
*Splitting templates out of the cycle wizard* below.

## Splitting templates out of the cycle wizard (added 2026-08-20)

Matt's call: **the template builder is a separate flow.** An admin creates
templates; a *different* act picks one and runs a cycle. Today's 5-step wizard
conflates the two — steps 2 and 3 are template authoring wearing a wizard's
clothes, which is why the same competencies have to be re-picked for every cycle.

### The split

| Today (5 steps) | Moves to |
|---|---|
| 1 · Setup — name, window, visibility | **Cycle** |
| 2 · Competencies | **Template** |
| 3 · Scale & questions | **Template** |
| 4 · Participants | **Cycle** |
| 5 · Review | **Cycle** |

**Template = what is being assessed.** Competencies (+ groups), rating scale,
review questions, goal questions. Reusable, versioned by editing, tagged.

**Cycle = who, when, and who may see it.** Name, type, window, visibility,
template selection, participants.

### Template builder

Lives on the **Review cycle** page (the admin surface) as a second tab —
`Cycles` | `Templates` — rather than a fourth nav item, keeping the
one-item-per-role read. Matches the reference's `Admin / Review Templates`
breadcrumb.

- **List:** Name (+ `base` / `universal` tags) · competencies summary (per
  variant where present) · Edit / Delete · `New review template`.
- **Editor:** name, tags, variant tabs (`Custom` / `Regular` / `Newcomer`),
  competency picker with `inherited` badges + `Show N inherited`, the rating
  scale editor, and the two question lists — i.e. today's steps 2 and 3, lifted
  wholesale.

### Cycle wizard, after the split

4 steps: **1 Setup → 2 Template → 3 Participants → 4 Review**

Step 1 gains a **cycle type** (`Regular` / `Newcomer`). That is what resolves a
template's variant, and it explains the legacy tool's cycle names ("Active
Regular Review: Aug 1, 2026", "Newcomer Review: Jun 20, 2026"). Without it,
variants have nothing to select them.

Step 2 shows the chosen template read-only — competencies grouped, scale
preview, questions — so the admin can see what they are committing to without
being able to edit it mid-launch. Editing is a template action, not a cycle one.

### ⚠️ Unresolved: one template per cycle, or one per participant?

Matt's wording is "selecting **one of** the templates" — one per cycle. That is
much simpler, and Base + template + variant fully determines the assessment.

But the reference cuts the other way: its cycle *"Active Regular Review: Aug 1,
2026"* spans **Engineering (Platform), Engineering (Web) and Design** in one
roster (Elena Park, Product Designer). A single template can't produce that. And
v2.1 carries `Competency_IDs` **per row**, so per-participant sets are the format's
native shape — see open question 6.

Three options:

1. **One template per cycle.** Simplest; mixed-team reviews mean running one
   cycle per team. Matches Matt's words, contradicts the reference.
2. **Template per participant row**, auto-suggested from the person's team and
   overridable. Exactly mirrors `Competency_IDs` per row. Most build.
3. **Cycle selects N templates; each participant resolves to one** by team.
   Closest to v2.0's org-unit cascade; the middle cost.

**Decided 2026-08-20: (3) — many templates per cycle.** The cycle selects a set
of templates; each participant resolves to one of them (by team), plus Base. This
reproduces the reference's mixed Engineering + Design roster, keeps the admin's
choice at cycle level rather than row level, and leaves (2)'s per-row override as
a later addition if it's ever needed.

Consequences to build against:
- Step 2 of the wizard is a **multi-select** of templates, not a single pick.
- The review step must show *which* template each participant resolved to, since
  a mixed cycle no longer has one answer.
- A participant whose team matches **no** selected template is an error state the
  wizard has to surface — the closest thing to a launch blocker in this flow.

### Migration risk (this is a refactor, not an addition)

Steps 2 and 3 are working code with real state — `STATE.selected`,
`STATE.scaleRows`, `STATE.reviewQs`, `STATE.goalQs`, plus `renderLibrary()`,
`renderScale()`, `renderQs()` and the inline add/remove handlers. Moving them
means:

- The library (`GROUPS`, `COMPETENCIES`, `SCALES`) stops being wizard-local and
  becomes template-scoped data with a `TEMPLATES` collection over it.
- The review step's summary currently reads competencies/scale/questions straight
  off `STATE`; it must read them off the resolved template instead.
- The stepper drops from 5 to 4, so `LAST`, `goToStep()` and the step markup all
  shift — and the compact page-head stepper's labels change with them.

Sequence it as: build the Templates list + editor alongside the existing wizard,
then cut the wizard down once the editor owns that state. Not the reverse — the
wizard is the only working demo of the flow right now.

## Manager views (added 2026-08-19)

Deliberately **lightweight** — a roll-up, not an analytics product.

**1. Team roster** (`Review results`)
- Cycle selector · `Summarized` / `Detailed` toggle · `Enable admin view`
- Rating-scale legend
- Row per reviewee: avatar/name/role/team · **Overall performance** (score +
  radial) · **Best performing in** (top 3 competencies + scores) · **Worst
  performing in** (bottom 3) · **Reviews** (`2 / 4 completed`, plus skipped
  count) · **Answers** (`3 / 3`) · **View Breakdown**

**2. Individual breakdown**
- Person header: name, role · team · cycle, overall score + label
- **Competency scores** — card per competency: score, radial, label, and the
  peer comments attributed by name (`Carla Ruiz · 5 "Great collaboration…"`), or
  an explicit *No comments.*
- **Competency trend** — score across recent cycles (bar chart)
- **Notes** — manager's own private notes (`Add note`)

⚠️ **Beyond spec, needs flagging in-UI:** averaged scores, best/worst ranking,
cross-cycle trend, and manager notes have no basis in either doc. The trend also
assumes competencies are stable across cycles, which templates make likely but
nothing guarantees. Attribution of comments to named peers is the most sensitive
piece — v2.1's visibility model is per-pair dates and says nothing about
surfacing who said what.

## Build sequence

- **Phase 1** — the 5-step wizard, happy path only, populated states
- **Phase 2** — edge states via the existing `?states=1` switcher (`pr-`
  prefixed): empty library, CSV with errors, blank-visibility warning,
  single-participant cycle, long competency lists
- **Phase 3** — the library as a browsable screen in its own right (`Competencies`
  nav item), if it earns a place beyond inline management

### Phase 2 order (roles · templates · manager views)

Revised 2026-08-20 for the template/cycle split. Steps 1–2 add the new surface
while the 5-step wizard keeps working; step 3 is the cut-over.

1. **Templates list** — `Cycles` | `Templates` tabs on Review cycle: table +
   tags, New / Edit / Delete.
2. **Template editor** — lift today's steps 2 and 3 (competency picker with
   `inherited` badges, scale editor, question lists) + name, tags, variant tabs.
3. ~~**Cut the wizard to 4 steps**~~ — **done 2026-08-20.** 1 Setup (+ cycle
   type) → 2 Templates (multi-select + resolved preview) → 3 Participants
   (+ team, showing which template each resolves to) → 4 Review. The old steps
   2 and 3 are gone; competencies, scale and questions now live only in the
   template editor, so the two competency libraries that briefly disagreed are
   one again.
   - Participants carry a **team**; `tplForTeam()` matches it to a template
     **by name** — the stand-in for real org data (open question 6).
   - A participant on a team no selected template covers is flagged inline as
     *No match* and raises a launch warning. That is the closest thing this
     flow has to a launch blocker, and it is surfaced rather than silent.
4. **Manager roster** — the roll-up table.
5. **Manager breakdown** — competency cards, peer comments, trend, notes.

## NB-59 revisions (2026-08-21)

Five sub-issues landed together. Two of them **reverse decisions recorded above**,
so they're noted here rather than left to look like drift.

| Issue | Change |
|---|---|
| NB-62 | `Create cycle` CTA and the Cycles tab move to **My direct reports** — the manager owns launching, and can launch whenever. |
| NB-63 | `Review cycle` → **Templates** (sidebar + page head), tab strip dropped; it only holds templates now. |
| NB-64 | Step 1's **cycle type selector removed** ("that's part of the templates"); each template row now shows its rating scale; the "What reviewers will see" card removed as duplicative. |
| NB-65 | Step 3's **reviewee team dropdown removed** — "not needed". |
| NB-66 | Page-head divider suppressed when a page-level tab strip follows it, kept otherwise. |

### ⚠️ Consequence: nothing resolves a template per participant any more

NB-64 removed the cycle type and NB-65 removed the team. Those were the **only two
inputs** to per-participant resolution, so with both gone:

- `tplForTeam()` is deleted, along with the Participants table's Team and
  Template columns and the *No match* launch warning.
- The Review step no longer reports `3 → Engineering · 0 → Design`; it states
  that every participant is assessed on all selected templates.
- **Newcomer variants are unreachable from the cycle flow.** `compsFor()` now
  always resolves to a template's `regular` set. The variants still exist and are
  still editable in the template editor, but no cycle can select one.

This supersedes the "many templates per cycle, each participant resolves to one"
decision above. It's a coherent simpler model — a cycle's templates apply to
everyone in it — but two things need a decision before this ships further:

1. **How does a Newcomer cycle happen?** Either the cycle picks the variant, or
   "newcomer" becomes a property of the person (tenure), resolved per participant.
   **Still open after NB-67.**
2. ~~**What does selecting two templates mean** if everyone gets both?~~ —
   **resolved by NB-67**: one template per cycle. See below.

## NB-67 — the cycle form (2026-08-21)

"Lets minimize the cycle creation flow. No need for all these steps." The
four-step wizard became **one form with three numbered sections**:

| | Section | Holds |
|---|---|---|
| 1 | Review template | Cycle name · template picker · read-only competencies + rating scale for the picked template |
| 2 | Schedule | Start date · End date · visibility to the reviewee · visibility to managers |
| 3 | Participants | Reviewer / Reviewee rows, add-a-pair, CSV upload |

What went, and why:

- **The steps.** Nothing in the form depends on an earlier answer — a cycle is a
  name, a template, a schedule and a list of people — so paging only hid the
  whole from the person filling it in.
- **The stepper** in the page head, and the compact-label CSS that made it fit.
- **The Review & launch step.** The form is short enough to be its own summary.
  Its blocking checks moved next to the Launch button as a validation read-out
  (no name / no template / no participants / end before start); its *soft*
  warnings were dropped — "reviewees never see their results" is a choice, and
  it now reads directly off Section 2.

### Revisions after review

- **Visibility is two options, not three.** NB-67 asked to keep "as soon as it's
  submitted"; on seeing it built, it went. It was a third way of saying "from
  today", so the choice is now *when?* rather than *which kind of when?* —
  **From a date** (the default) or **Never**.
- **The "N assessments will be created" read-out** in the Participants head was
  removed; the table already says how many rows there are.
- **Removing a participant toasts with Undo**, restoring the row at its original
  index. There's no confirm step before the delete, so the recovery sits after
  it rather than a dialog asking first.

### The template picker answers open question 2

**One template per cycle**, chosen from a dropdown, labelled `Engineering
(extends Base Template)`. Multi-select had nothing left to resolve against once
NB-64 and NB-65 removed cycle type and team, so a set of templates could only
ever mean "union everything" — which was the ambiguity. Picking one is the
honest model.

Selecting a template reveals a read-only block: competencies grouped
General / Skills (unioned with the Base Template's, which always apply), the
rating scale as swatches with labels, and the open-question count. It answers
"what will reviewers actually score?" without making any of it editable here —
that stays in Templates.

Newcomer variants are **still unreachable** (question 1 above): with no cycle
type, `compsFor()` resolves to `regular`.

## Template model, extended (2026-08-24)

Design review on the built screens pushed three changes into the template model
itself. All three are in the editor; everything that renders templates reads
from the same source, so the cycle form follows automatically.

**Description.** Optional, 180 chars, shown as a sub-line under the name in the
Templates list. Says who a template is for and when to reach for it — the name
already identifies it.

**Inherits from.** Inheritance used to be hardwired: *every non-Base template
inherits Base*. No control could express that, so a template with no parent was
impossible. It's now an explicit `parentId`:

- Resolution walks the whole chain, not one level — competencies, questions and
  the counts that derive from them.
- The three seeded templates point at Base, so nothing regressed; **new
  templates default to no parent**.
- Base can't have one (it's the root); a template can't pick itself or one of
  its own descendants, so the picker can't build a loop. The walk carries a
  `seen` guard anyway, since saved data could.
- A deleted parent resolves to no parent and clears the stored link.

**Competency groups: General / Hard skills / Soft skills.** v2.0 had one
undifferentiated *Skills* bucket, which said nothing about whether a competency
was a craft or a behaviour. The seeded set is now v2.1's split — the 13 former
Skills items were re-filed as 7 hard (Design Systems, Prototyping, UX &
Interaction, Visual Design, Code Quality, System Design, Technical Proficiency)
and 6 soft (Mentorship, Problem Solving, Delivery & Execution, Leadership,
People Development, Strategic Thinking).

**Custom competency groups.** The set is no longer fixed at all — admins can add
their own — a Contractor group with its own skills.
The Group control is a combobox: typing filters the list, and a query matching
nothing offers to create it. Two deliberate constraints:

- A group is only committed when Add resolves it with a competency. The library
  skips empty groups, so one created by browsing would be invisible.
- Re-typing an existing name reuses that group rather than duplicating it.

Each group header carries a plus that points the shared add row at that group,
rather than an inline form per group — one control, one code path.

**Inheritance is editable, not read-only.** Inherited competencies used to sit
in a separate collapsible list above the library, unticked-able. They now sit
*in* the library, ticked and badged `inherited`, and can be unticked — which
records an **exclusion** rather than editing the parent:

- `excludes` is keyed by variant, like the `variants` it modifies, so Regular
  can drop something Newcomer keeps.
- Resolution everywhere is *(inherited − excluded) ∪ own*. The cycle form reads
  the same rule through `PR_TPL.excluded()`, so it can't disagree with the
  editor.
- Rationale: a parent is a starting point, not a contract. Base still owns the
  competency; a child simply doesn't use it.

**The library shows only what's picked.** Each group lists its selected
competencies and offers **Show N unselected** / **Hide unselected** beside the
group name. The library is long and most of it isn't in any one template, so
what's picked leads and the rest is one click away. Unticking a row removes it
immediately when its group is collapsed — otherwise the list disagreed with its
own heading until some later re-render. The reveal state is per group and lives
outside the draft: it's a view preference, not part of the template.

**Not carried through:** the Give Assessment screen's section headers are static
markup from the Figma build, not driven by `GROUPS`, so it still shows v2.0's
General / Skills split and won't show a custom group either. Worth wiring if the
reviewer side should reflect the new grouping.

## Templates are archived, never deleted (2026-08-26)

A running cycle is tied to its template and resolves competencies, questions and
rating scale through it. Deleting one mid-cycle would leave those assessments
pointing at nothing, so the templates list offers **Edit** and **Archive** only —
no Delete.

- Archiving sets a flag. The template leaves the list and the cycle form's
  picker; the record stays, so an existing cycle's reference still resolves.
- A template picked for a *draft* cycle and then archived is un-picked, and
  Launch blocks until another is chosen. A cycle that already launched is
  untouched.
- Archived templates are still **inherited from** — archiving stops a template
  being chosen for new cycles, not being a parent.
- Archived templates **stay listed**, tagged `archived`, with Restore in the same
  menu. They were hidden at first; that's what made archiving the Base Template
  dangerous, since Base feeds every other template and a hidden-but-still-
  applying Base would have been unreachable to see or edit. Listed and
  reversible, the exception isn't needed — **every template can be archived,
  Base included.** (A status filter is the next thing this needs at scale.)

## Naming (2026-08-24)

| Was | Now | Note |
|---|---|---|
| My direct reports | **Review cycles** | sidebar, page head and the cycle form's breadcrumb |
| Overview (tab) | **Reviews** | the manager roll-up |
| Review template (section 1) | **Cycle setup** | it holds the cycle name too |
| 5-point standard / 3-point (legacy 2.0) | **5-point** / **3-point** | |

⚠️ *Review cycles* is the name NB-63 took **away** from the admin page (renamed
to Templates). Reusing it for the manager surface is deliberate, but the two are
easy to confuse when reading those tickets back. The page's own tabs are now
Reviews · Individual reviews · Individual goals · Cycles, so "review" carries
three meanings in one strip — worth a second look if it reads ambiguously.

## Detailed matrix — grouped, with group averages

The manager's Detailed view had thirteen unlabelled competency columns, giving
no clue which skill sat in which group. It now renders a group band across the
top spanning that group's competencies plus an **Avg** column at its right edge.

- **Columns derive from the shared library**, not a frozen list — the old
  hardcoded `General / Skills` would have kept showing v2.0's split and would
  never pick up a custom group. Only competencies somebody was scored on get a
  column; an "Other" bucket catches a score whose competency has left the
  library.
- The footer's group average is computed **across every score in the group**,
  not as the mean of the per-person averages — otherwise someone scored on one
  competency would weigh as much as someone scored on five.
- The final column is **Overall**, not "Average", now that "average" means
  something more specific in the same table.
- The per-group Avg cells take their row's own colour. Tinting them fought the
  table's row striping — the same grey sat visibly on a white row and vanished
  into a striped one, so the column read as a rendering fault. The header and
  the group band carry the distinction instead.

**Answers open a modal**, like the Reviews cell beside them. It lists every open
question with its answer, and keeps unanswered ones visible as *Not answered
yet* — the gap is why a manager opens the cell. `ansDone` / `ansOf` were
separate fields that could disagree with what the modal listed, so both counts
now derive from the answer list itself.

## Breakdown screen (2026-08-27)

The manager's `View` button toasted "screen not built yet" since the manager
views landed. It now opens a per-reviewee breakdown for the selected cycle —
reference: `perf-review-proto-1 /reviews/4/roles/25`. Competency cards
best-first with the peer comments behind each score, plus a trend chart and
private notes.

**Derived, not duplicated.** Scores, band labels, reviewer names and the cycle
all come from the same `PEOPLE` rows the Reviews tables read, so the breakdown
can't contradict the row that was clicked to reach it. Reachable from both the
Summarised and Detailed tables.

**Comments** are the one thing those rows don't hold. They're drawn from a pool
and attributed only to that person's *submitted, non-self* reviewers, keyed off
a hash of name + competency so a person always shows the same comments. Nobody
is quoted who hasn't reviewed.

Two states the reference has no equivalent for, both reachable in the seed data:

- **One cycle only** → no trend. Alice appears in a single cycle; one bar
  pretending to be a trend is worse than saying "First cycle on record".
- **No peer assessments yet** → one callout, not nine "No comments." rows.
  Carla is 1 of 5 submitted and that one is her self-assessment, so the callout
  says so: an average over a lone self-assessment *is* a self-assessment, and
  the screen shouldn't present it as team feedback.

Notes are session-only — enough to show the interaction, with an empty state.

## One assessment (Figma 33986:136076)

A Peer reviews row *is* one reviewer's assessment of one reviewee, so the row
opens that assessment — not the reviewee's aggregate breakdown, which the report
tables already reach. Redesigned against the Figma reference; ported with
designmd parts (`.avatar avatar-lg`, `.tag tag-light`, `#i-quote`,
`#i-arrow-long-right`, `modal-lg` = the reference's 800px) rather than new
equivalents.

**The disabled button is muted with colours, not `opacity`.** `opacity: 0.5` on
the button broke its own tooltip two ways at once, from one root cause: group
opacity multiplies into `::after`, so the tooltip painted at half strength; and
any opacity below 1 creates a stacking context, which trapped the tooltip's
`z-index: 1000` inside the button and let later-painting rows cover it. Explicit
`--color-text-subtle` on `--color-surface` gives the same muted read with no
stacking context and no bleed into the pseudo-element. Hover feedback is also
suppressed — the tooltip is the only thing hovering a dead button should produce.

**The dead row action.** An unsubmitted row keeps a **View**, disabled, with a
tooltip naming the reason in the Status column's own words ("Outstanding —
nothing has been submitted to view yet." / "Skipped — this reviewer will not be
submitting an assessment."). A bare `—` said *nothing here* without saying *why*,
and cost the column its scannability. It carries `aria-disabled` rather than the
`disabled` attribute on purpose: a genuinely disabled button is not focusable, so
the tooltip — the only thing explaining the state — would never reach a keyboard
user. It has no `data-cd-assess`, so the delegated click handler cannot reach it.
designmd ships no disabled `.btn` style at all, so the 0.5 opacity is local.

**From → To.** The reference puts identity in the body, not the title, so the
title is just "Assessment". The reviewer's second line is their **relationship**
(Manager / Peer / Teammate), not a job title: the capacity they reviewed in is
what matters here, and it's the one descriptor always present — most reviewers
are not themselves reviewees in the cycle, so their title is unknown data.

**The two numbers.** The reference gives each side an "Overall Score" slot. Used
for the comparison that justifies opening a single assessment: *Score given*
(this reviewer's average) on the From side, *Overall score* (everyone's) on the
To side, with the gap as the From side's tag (`+0.2 vs team`, or "in line with
the team").

No band label on those two — they're **averages**, and rounding 4.5 to
"Outstanding" invents a verdict the numbers don't support; it also made 4.7 and
4.5 wear the same tag. The per-competency rows *do* carry a band, because there
the score is a whole point and the band is exact.

**Self-assessments** get one block labelled "Self-assessment" carrying both
numbers, instead of the same face mirrored across the arrow — that reads like a
bug. (The Peer reviews tab still lists Self rows, because it doubles as the
progress view. The content is right; the label is the loose part.)

**Groups.** `GROUPS` gained a `d` description, which the reference shows under
each group name. Runtime-added groups have none and render without one rather
than with placeholder text. A score whose group has since been removed lands in
an "Ungrouped" card rather than being dropped silently.

**Same source as the breakdown.** Every score and quote comes from the shared
`takeOf(reviewee, reviewer, competency)`, so the aggregate breakdown's quotes and
this modal cannot disagree about what a reviewer said. Verified: every quote
attributed to a reviewer in the breakdown appears identically here.

### designmd bug found, not fixed here

`.modal` caps its height with `calc(100vh - var(--ic-space-9))`, but the space
scale has **no `--ic-space-9`** (it runs 0–8, then 10, 12, 16). The calc is
invalid, so the cap is dropped and *any* modal taller than the viewport grows off
the top of the screen — this one did, at 1308px. Capped locally with
`--ic-space-6`; `.modal-body` already scrolls. Affects every modal in the system,
not just this prototype.

## Peer assessments on the Give Assessment screen (Figma 34655:39160)

A card directly below the reviewee's self-assessment, listing what the other
reviewers have already said: who they are and in what relationship, the band they
gave, and their comment. Left column is designmd's own `.cell-user` (avatar +
name + role) rather than a restatement of it; the badge counts the rows it sits
above rather than being typed a second time.

**Adapts to its own width, not the viewport's.** The reference's two-column split
(180px name column, 24px gap) was drawn against an 800px card. On this screen the
competency nav leaves ~480px, where a fixed 180px hands 40% of the row to a name
and stretches a two-line comment to five. So `.assess-peers` is a container and
the row stacks below 520px, giving the comment the full width; above that it is
the reference layout exactly. Measured: 2 lines at 956px, 3 at 449px.

**The dot is grey-violet, not the reference's blue.** Blue is this system's
interactive colour, and the card directly above already establishes green =
Overperforming — a blue "On Track" beside it reads as a different kind of signal
rather than the middle of the same scale. So the dot uses the same `#9999BB` the
score rings use for that band. Literal for the same reason as the nav gradient:
the scale's colours live in the data, not in tokens.

**Anchoring, unresolved.** Peer ratings sit *above* the rating input, as the
reference places them, which means a reviewer reads what everyone else concluded
before forming their own view. That is the classic reason review tools withhold
peer input until submission. Built as designed; the cheap mitigation, if wanted,
is to collapse the card by default using the rubric's existing pattern, or to
move it below the rating.

**Not built:** the empty state ("no peer assessments submitted yet"), because
this screen is static markup for a single competency and has no data behind it.

## Maintaining a template's competencies

Building a template was smooth; revising one was not — seventeen competencies
across three groups, each ticked and unticked one row at a time. Each group head
now carries the three things revising needs.

**A tri-state group checkbox.** All in / some in / none in, using designmd's own
indeterminate checkbox (`checkbox-mark-dash`, set as a DOM property after render
since `indeterminate` is not an attribute). It moves in one direction from
wherever it is: **any missing → take all in; all present → drop all**. Reading
`e.target.checked` instead would make the first click on an indeterminate box
depend on what the browser decided that click meant.

Crucially it routes through the same `setComp(id, on)` the individual rows use.
That matters because "in this template" has two shapes: an inherited competency
is held out by being **excluded**, anything else by being **selected**. One
function owns that, so a group can't come to mean something different from
ticking its rows one at a time. Verified on Engineering, which inherits Base's
four: mixed → all in → all out (via exclusions) → back.

**A count, `4 of 7`.** The state of a group without expanding it.

**A collapse.** Distinct from the existing "Show N unselected" reveal, which is a
different question — that one asks *what else could be here*, this one asks *get
this out of my way*. Both view preferences, both kept out of the draft. A
collapsed group hides its reveal link, since there is nothing to reveal into.

**The plus drops a card into the group.** It used to point the single add row at
the foot of the section at that group and move the cursor there; the trip down and
back was the expensive part of adding several competencies to one group. The card
sits where the row will, in accent-bordered form to say it isn't saved, and after
Add it reopens empty in place — adding one competency to a group is usually adding
several. Enter commits, Escape abandons. Collapsing a group mid-draft closes the
card rather than hiding what was typed.

Both ways in — the card and the bottom add row — go through one `createComp()`,
so they can't drift into producing different library entries. The bottom row keeps
its group combobox, because it is still the only way to create a *new* group.

## Questions column on Templates

A **Questions** column between Competencies and Actions, showing a count that
opens a modal listing what the template actually asks.

**The count is own + inherited** — the total a reviewer will see — computed by the
same rule the cycle builder's template detail uses, so the two can't report
different numbers for the same template. Verified they agree for all four
templates (4 / 4 / 5 / 4).

This *differs* from the Competencies column beside it, which shows **own-only** on
purpose: Base's four competencies would otherwise repeat as tag chips on every
row. A single digit has no such problem, so the number is the total and the modal
splits it — the meta line reads "5 questions — 1 on this template, 4 inherited."
Worth a decision if the inconsistency bothers you; the alternative is own-only in
the cell, which makes Design and Management both read 0 while they do ask four.

**The modal groups by kind, in the editor's own words** — "Review questions —
asked of reviewers" and "Goal questions — answered by the reviewee about
themselves" — so the list and the authoring screen describe the same thing the
same way. Each row carries `required` and `inherited from <parent>` as tags.

**Zero is not a link.** A template with no parent and no questions of its own
shows a plain `0` with a tooltip saying so, rather than a link to an empty modal.
Reachable: a newly created template starts with no parent and no questions.

The count reuses `.mv-reviews-btn`, the same "reads as text, not a control"
treatment the Reviews and Goals counts already use in the report tables.

One layout fix: at 8% the column heading rendered as "Quest". Widened to 13% —
the column has to fit its own header word, not just a single digit.

## Breakdown: one view, two filters

**This cycle** and **All cycles** were two tabs holding two different shapes — a
list of competencies with their comments, and a cycle-by-cycle matrix. They are
one view now, in the list's shape, with **cycle** and **reviewer** as filters on
it. "Which cycle" and "who said it" are questions about scope, not different
screens.

**A cycle is always selected — there is no All.** It opens on the one the page
was reached from. Averaging across cycles made the headline number a lifetime
average (Alice read 3.8 rather than 4.5) and put six identical quotes on one card,
because scores from different cycles are measurements of a moving target. With
one cycle at a time the mixed-scale refusal also disappears — every score on
screen is against one template's scale — and quotes no longer need to say which
cycle they came from. Reviewer still defaults to All.

**Everything derives from one list of takes** — one row per reviewer per
competency per cycle, from the same shared `takeOf()` the assessment modal reads.
So the card scores, the quotes and the counts cannot disagree.

**Two meanings for the card's score, deliberately.** With *All reviewers* it is
the cycle's own aggregate (averaged across the cycles in scope) — the same number
the report tables and the rings show. Recomputing it from individual takes would
put a slightly different number on this page than on every other one. With one
reviewer picked, their own score is the honest answer, and the hint above the list
changes to say so.

**The page-head overall follows the filters.** It used to be the opening cycle's
overall, which would contradict a list showing every cycle. Same for the meta
line, which dropped the cycle name — role and team are true whichever cycle is in
scope.

**Quotes carry their cycle only when more than one is in scope.** Inside a single
cycle that would just repeat the filter above them.

**A rating filter, third of the three.** Where they struggle and where they do
well. One entry per point on the scale — rendered as the same coloured chip a
score wears everywhere else, so the menu reads by colour — built from `SCALE`
rather than hardcoded to five.

Every option carries a count, so **the open menu is the distribution** — usually
the answer without filtering at all. The counts are computed over the cycle and
reviewer scope but ignore the rating filter itself; counting against its own
result would zero every other option the moment you picked one.

It deliberately does **not** move the page-head overall. The overall answers "how
is this person doing", which is a property of the person over a scope of cycles
and reviewers; the band filter is a view on the competency list, not a change of
scope. An overall computed from only the competencies you filtered to would be a
different question wearing the same label.

**Refusals kept.** A scope spanning two rating scales can't be averaged, so it
says so rather than producing a number — the same refusal the matrix made about
its Change column. An empty list names *which* filter emptied it. And when a
cycle has no peer assessments, the alert still says the score above is the
reviewee's own self-assessment; without that sentence the head shows a number
with nothing visibly behind it.

Narrowing to one cycle can drop the reviewer that was picked, so the reviewer
resets to All rather than showing an empty list under a name nobody in scope has.
(Unreachable with the current seed: the historical cycles mark every reviewer
submitted, so every reviewer appears in every past cycle.)

**Parked, not deleted:** `renderMatrix`. It is the only view that shows change
*per competency* rather than in aggregate — the trend card beside the list only
shows the overall — so it is worth keeping recoverable.

Swept all five reviewees × every cycle option (24 combinations): nothing throws,
and every empty result carries an explanation.

## Cycles moved out of Reports

The Cycles tab became its own page and its own nav item, sitting between Reports
and Templates: **My assessments · Reports · Cycles · Templates** — your own work,
your team's results, the cycles you run, what they ask.

The reason is that creating a cycle is not reporting on one. Three of those tabs
read results; the fourth ran the thing that produces them, and **Create cycle**
sat as the primary action on a page otherwise about numbers. Reports keeps the
cycle *picker*, because a cycle is still the scope those tables are read through —
what moved is the list and the authoring, not the scoping.

Consequences handled rather than left to rot:

- The tab badge became a **count beside the page heading** (designmd's documented
  `count-badge` next to a title). It still counts what the table is showing, so
  the search and the All / Created-by-me switch drive it.
- **`prSelectCycle` is now a navigation.** Its comment used to say the opposite —
  correctly, while the list was a tab on the same page. From a separate page,
  the kebab's View cycle has to travel to Reports or it would scope tables the
  person can't see.
- The builder's breadcrumb reads **Cycles** and returns there, and launching or
  re-launching lands back on the list it was opened from rather than on Reports.
- `syncToolbar` is gone. It existed to hide the report toolbar on the Cycles tab;
  every remaining tab is a report scoped by the picker, so it had nothing left to
  hide from.

## Export CSV

Replaces Create cycle as the Reports CTA, and it exports rather than toasting an
apology: the **tab you are looking at**, including whatever the search and the
cycle picker have narrowed it to, with the cycle in the filename because every
one of those tables is scoped to one.

Two details that matter for the output:

- Cells are read with `innerText`, not `textContent`. `textContent` glues an
  avatar's initials onto the name behind it ("ACAlice Chen"); `innerText` keeps
  the browser's own line breaks, which become ` · ` separators. The avatar line is
  then dropped, since initials aren't data.
- The **Actions column is dropped** — "View" in a spreadsheet is a button that
  isn't there. Matched per cell rather than by column index, because the detailed
  matrix's rowspans mean its two header rows don't share an index space. Both of
  those header rows are kept: the group row above the competency row is how that
  table is meant to be read.

## Cycles list toolbar

Search plus a two-segment scope switch (**All cycles** / **Created by me**),
inside `#rc-cycles-panel` rather than beside the report tabs' toolbar — it acts on
this table only, so it appears and disappears with the tab instead of needing to
be hidden by hand the way `#rc-toolbar` is.

**Search covers the three text columns on screen** — name, creator and the status
word — so what you can read, you can search for. Dates are deliberately out:
nobody types "Sep 15, 2026" to find a row.

**"Me" is one constant.** `window.PR_ME = 'Matt Vella'` (the MV in the topbar),
so "the ones I created" can't drift from anything else that needs to tell mine
from everyone's. A real app reads it from the session.

**The tab badge counts what the table shows**, matching how the report tabs'
badges already follow their search. This also replaced a stale comment claiming
there was "no tab to count into any more" — there is, and it was only ever set by
the load-time pass, so it would have frozen at 8 while the table filtered.

**The empty state names the control that caused it**, not just the emptiness:
with a search and a scope both live, "no results" leaves you guessing which one to
undo. Four cases — search-and-scope, search alone, scope alone, and genuinely no
cycles.

`role="group"` with `aria-pressed` rather than designmd's documented
`role="tablist"` for `.segmented`: these two segments switch a filter, not a
panel, and there are no tabpanels for a tablist to control.

Verified that archiving a row and re-launching a cycle both keep the filter —
each goes through the same `render()`, which reads the filter state rather than
resetting it.

## Editing a launched cycle

Clicking a cycle's name opens the builder filled in from that cycle — name,
schedule dates, template, participants — with the CTA reading **Re-launch
cycle**. The kebab keeps **View cycle** for the report and gains **Edit cycle**
so the action is discoverable without knowing the name is clickable. This
partly answers open question 3 ("should a launched cycle be editable after the
fact?"): yes, editable.

**The edit lands on the record.** `name`, `template`, `start` and `due` are
written back to the cycle in `PR_CYCLES`, and both the cycles table and the
results cycle-picker are re-rendered — otherwise you would return to the list
and see the old name, an edit that silently didn't happen.

**The warning painted empty at first.** `.alert` is `display: flex` in
components.css, which outranks the UA stylesheet's `[hidden] { display: none }`,
so setting `hidden` on it left an empty banner on screen for every active cycle.
This is the fourth component in this file needing the same one-line guard
(`.btn`, `.toolbar`, `.cb-vis-date`, now `.alert`) — the trap belongs fixed
upstream, not patched a fifth time here.

**Status is derived, not assumed.** A cycle re-launched with a start date in the
future becomes `scheduled`; otherwise `active`. Re-launching a closed or archived
cycle therefore reopens it, so the form shows a warning saying so before the
button is pressed, naming that the recorded assessments stay attached.

**Participants are read, not copied.** `pairsOf()` derives the roster from the
assessments recorded against the cycle (`PR_PEOPLE[c.data]`), so the builder's
table cannot disagree with the Peer reviews tab. Consequence: the three cycles
with no `data` (H2 Company-wide, Q4 Company-wide, H1 Design) open with an empty
roster and cannot be re-launched until someone is added — which is the truth
about them in this prototype, and the existing "launch empty" check already says
it in the right place.

Two things this exposed and fixed:

- **`chosen()` only looked in `pickable()`**, which excludes the Base Template.
  Five of eight seeded cycles run on Base, so editing them showed "Choose a
  template…" over a cycle that plainly has one. It now looks in the full list;
  a *new* cycle can still only set the template from the menu, so Base stays
  unreachable there.
- **The New-cycle form shipped pre-filled** with `H2 2026 — Engineering` — the
  name of a cycle that actually exists in the list. Harmless before; now that
  clicking that cycle opens a filled form, it read as though Create cycle were
  editing it. Create cycle now opens blank, with no participants (a new cycle
  genuinely has none — the three seeded pairs were filler).

**Not carried over:** visibility dates. The cycle model doesn't record them, so
an edited cycle shows the form's defaults rather than what it was launched with.

## Skipping an assessment

Skip opens a modal naming the row, with a **required** reason, Cancel (secondary)
and Continue (primary). The reason is required because the manager's Reviews
column already flags "Includes N skipped", and that count only means something if
each skip says why. It rides as a tooltip on the Date Skipped cell — the Skipped
table has five fixed columns and none of them is Reason. **A Reason column is the
better home** if skips are something anyone reviews.

**Overdue rows leave Pending on their own** (asked for directly, 2026-09-01):
once the due date passes, the assessment moves to Skipped without anyone pressing
Skip. Its reason is written by the system and says so — "Auto-skipped — not
submitted by Aug 21, 2026." — and the row carries `data-skip-auto`, so a chosen
skip and a lapsed one are not merged into one fact. One summary toast announces
it, because a row silently absent from Pending is worse than one that explains
where it went.

**The tension this creates, unresolved.** Everywhere else in this feature overdue
is a *flag on* a state, not a state: an Outstanding peer review that passes its
date stays Outstanding and turns red; a past-due cycle stays Active. This is the
one place a deadline changes state. Two consequences worth a decision:

1. Skipped now mixes "I decided not to" with "the clock ran out". They read
   differently in the tooltip but look identical in the table, and the manager's
   skipped count no longer distinguishes them.
2. The red overdue date in Pending was the thing that prompted a late reviewer to
   act. Moving the row out removes that nudge — the deadline now closes the
   review rather than chasing it.

If either matters, the alternative is to leave overdue rows in Pending (red, as
they were) and surface them as their own filter or count instead.

### A bug this uncovered

`skipRow` wrote the skip date into `children[2]` with a comment claiming that
slot was Date Received — stale from before the Review cycle and Due columns were
added. So skipping a row overwrote its cycle name with the date and left a 6-cell
row in a 5-column table, shifting every column after Relationship by one. It now
writes into the Date Skipped cell, keeps the cycle, and drops the Due cell that
Skipped has no column for.

## Open questions

1. ~~Per-pair competency/scale variation~~ — **resolved 2026-08-19** by templates
   (Base + role template + variant, resolved per reviewee).
2. Do questions survive contact with the backend, or stay a design proposal?
3. ~~Should a launched cycle be editable after the fact, or immutable?~~ —
   **partly resolved 2026-08-31**: editable, via the cycles list. Still open:
   whether re-launching a *closed* cycle should reopen it (what it does now) or
   duplicate it into a new one.
4. Does the library need archive-vs-delete? (Past assessments reference
   competencies by ID, so hard delete would orphan them.)
5. **Does the reviewee get a results surface?** ("My Results" was removed from the
   nav; the three roles don't name the reviewee-as-reader.)
6. ~~How is a role template bound to a person?~~ — **partly resolved
   2026-08-20**: a cycle carries *many* templates and each participant resolves
   to one. Still open: what the resolution keys on. Team is the assumption here
   (the reference's roster shows a Team column); v2.0 cascaded by **org unit**
   and also varied definitions by **job level**, neither of which this prototype
   models.
7. **Are peer comments attributed or anonymous to the manager?** The reference
   shows names; v2.1 says nothing, and v2.0's Peer Feedback was a separate
   always-on channel. Highest-sensitivity open item.
8. **Does editing a template affect cycles already launched?** Templates are
   mutable, assessments reference competencies by ID — same orphaning risk as 4,
   one level up.
