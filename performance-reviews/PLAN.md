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

### What the prototype has that v2.1 does NOT (deliberately dropped)

- **Templates + Base Template inheritance** and the `inherited` badge
- **Regular / Newcomer** template variants
- Per-org-unit / per-job-level competency definitions (a v2.0 concept)

## Locked decisions

- **Reuse model: persistent library, no inheritance.** Competency groups,
  competencies and rating scales persist and are reusable across cycles; the
  wizard picks from them or creates new ones inline. No template/inheritance
  concept — v2.1 dropped it and it's the prototype's most complex machinery.
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

## Build sequence

- **Phase 1** — the 5-step wizard, happy path only, populated states
- **Phase 2** — edge states via the existing `?states=1` switcher (`pr-`
  prefixed): empty library, CSV with errors, blank-visibility warning,
  single-participant cycle, long competency lists
- **Phase 3** — the library as a browsable screen in its own right (`Competencies`
  nav item), if it earns a place beyond inline management

## Open questions

1. Per-pair competency/scale variation — first-class flow, or override-only?
2. Do questions survive contact with the backend, or stay a design proposal?
3. Should a launched cycle be editable after the fact, or immutable?
4. Does the library need archive-vs-delete? (Past assessments reference
   competencies by ID, so hard delete would orphan them.)
