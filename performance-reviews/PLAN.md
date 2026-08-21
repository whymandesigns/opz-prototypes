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

## Open questions

1. ~~Per-pair competency/scale variation~~ — **resolved 2026-08-19** by templates
   (Base + role template + variant, resolved per reviewee).
2. Do questions survive contact with the backend, or stay a design proposal?
3. Should a launched cycle be editable after the fact, or immutable?
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
