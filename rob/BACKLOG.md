# RoB Meetings — backlog

What has not been designed yet, and why it is worth designing.
[CHANGELOG.md](CHANGELOG.md) is what has.

## Where a thing goes

Three files, and an item belongs to exactly one of them:

| | Holds | Tense |
|---|---|---|
| **This file** | work not started — a gap, an idea, a question worth a screen | future |
| `CHANGELOG.md` › **Open, and worth revisiting** | decisions taken, built, then parked, each with the commit that still holds the work | past, paused |
| `CHANGELOG.md` › **History** | what was built and why | past |

An item **leaves** this file when it is built: delete it here, and write the
history entry there. Nothing is in both.

## What does not belong here

- **Anything about the repo.** A rename, a lint pass, a tooling change, a
  re-bake. Real work, and `git log` is where someone looks for it.
- **A bug in the prototype.** Fix it, or it is not worth writing down.
- **A deviation in the product.** The oracle already tracks those, with ids.
  Cite one here only as the *reason* an item is interesting.
- **A design that is already decided but unbuilt.** That is *Open, and worth
  revisiting* — it has a commit behind it; these do not.

## How to write an item

An `###` heading, then these lines in this order. Every one of them, even when
the answer is short — a missing line reads as an oversight rather than a
deliberate blank.

```markdown
### A short title, as a noun phrase

**Status** · Idea — one sentence, where there is anything to add.
**Added** · 2026-11-16
**Source** · where this came from: a rule, a screenshot, a conversation.
**Rule** · `ROB-PREREAD-010`, `B-206` — or: the spec does not cover this.

Two or three paragraphs: what is missing, what the product does, and what the
interesting decision is. If there is no interesting decision, it is a chore,
not a backlog item.
```

**Four statuses, and an item is in exactly one:**

- **Idea** — noticed, not yet looked into. May turn out to be nothing.
- **Researched** — checked against the oracle, with ids; the scope is understood.
- **Ready** — we know what we would build and could start.
- **Dropped** — decided against. The item stays, under *Dropped*, because why it
  was dropped is the useful part.

---

## Open

### A RoB with no host in the room

**Status** · Researched — the product has one safeguard for this and three documented ways it does not reach. The proposal is a separate item.
**Added** · 2026-11-16
**Source** · raised as a red flag: if the owner is away, participants wait in a waiting room and the meeting does not happen.
**Rule** · `ROB-ZOOM-009`, `ROB-ZOOM-001`, `ROB-OWNER-020`, `ROB-OCC-096`, `ROB-OCC-106`, deviation `B-014`

The product does have an answer, and it is not a host at all: every Zoom meeting
linked to an upcoming RoB occurrence is **forced to "join before host" ON**,
along with authenticated-join and a recording mode, and anything changed by hand
in Zoom is overwritten at the next enforcement (`ROB-ZOOM-009`). When that
enforcement reaches the room, the owner being away costs the meeting its host,
not its start.

**It does not always reach the room.** Four cases. The first three were written
here on 2026-11-16; the fourth was found on 2026-11-20 and is the one ops is
actually working around.

- **The waiting room, which the product does not manage.** Enforcement sets
  three settings and `settings.waiting_room` is not one of them — and in Zoom
  **the waiting room overrides join-before-host**. A room the product manages
  correctly, on the right host, with a live integration, still strands everyone
  if the waiting room is on at the account, group or user level. This is why
  owners are told by hand to turn it off, and it means join-before-host being ON
  is not evidence that anyone can get in. Drawn up as
  [Hold the waiting room off](#hold-the-waiting-room-off).
- **Webinars.** Join-before-host is explicitly not touched for them — only
  authentication and recording mode are.
- **No active Zoom integration.** Enforcement is conditioned on one, and a
  tenant without it gets none of these settings.
- **`B-014`, open.** Only links on `zoom.us` and `toptal.zoom.us` are
  recognised, so a room on any other host is never linked — and the notes on
  `ROB-ZOOM-009` say unlinked rooms are not enforced. A regional host such as
  `us02web.zoom.us` is enough to lose the protection.

**And there is no way to name a second host.** No alternative host, no co-host,
no per-occurrence delegation anywhere in the spec. The room is created with the
owner as host and `ROB-ZOOM-001` is explicit that an existing room is never
reused or chosen by the user. The only lever is a full ownership transfer, which
creates a **new** Zoom meeting and rewrites the join link across every current
and future occurrence (`ROB-OWNER-020`) — the right tool for "someone else runs
this RoB now", the wrong one for "I am away next Tuesday".

**The product had the right tool and dropped it**, which is worth knowing before
anyone proposes building one: the legacy temporary ownership transfer was
exactly "hold this for me while I am away", and it was deprecated on
2026-10-29 with Role Inheritance — a permanent handover — named as its
replacement. See
[The temporary ownership transfer the product dropped](#the-temporary-ownership-transfer-the-product-dropped).

**Since 2026-11-12 something does tell people in advance, and it stops short of
the owner.** `TOP-7503` (topteam#6899) added a per-occurrence **Decline** with
an optional comment (`ROB-OCC-097`), a comment the owner and RoB admins can read
(`ROB-OCC-098`), and a red ✕ on the upcoming occurrence (`ROB-OCC-067`, where a
future occurrence used to show no response at all). But `ROB-OCC-096` says the
actions are **not offered to the owner** — the one person whose absence costs
the meeting its Zoom host has no way to say so in the product. A decline made
in Google Calendar does surface, so the signal exists; what is missing is
anyone reading it as "this meeting now has no host".

Out-of-office is still invisible in advance: `ROB-OCC-025` computes it only from
an hour after the occurrence ends. The planned absence, with a named stand-in
attached, is recorded elsewhere — see
[Carry "who is covering" from time off into the RoB](#carry-who-is-covering-from-time-off-into-the-rob).

**And there is now a second answer to "the owner is away", which is to move the
meeting.** `ROB-OCC-096` and `ROB-OCC-102` let a participant propose another
time for one occurrence, with a comment; `ROB-OCC-106` lets anyone who can edit
accept it with **Move meeting**, which edits that occurrence only and leaves
everyone's response alone. It is a real alternative to a stand-in — and it is
not offered to the owner either, so an owner who knows they are away cannot
propose their own move.

**Zoom has two mechanisms for this, and the product uses neither** (checked
2026-11-16, see *What else Zoom could carry* for the sources):

- **`settings.alternative_hosts`** on the meeting object — a semicolon-separated
  list of e-mails, settable when the room is created or updated. An alternative
  host can start the meeting. Both the host and the alternative host must be
  **Licensed users on the same Zoom account**, which for a company-account RoB
  is the normal case. This is the direct answer, and it is one field on a call
  the product already makes (`ROB-ZOOM-001` creates the room).
- **Scheduling privilege** (`POST /users/{userId}/assistants`) — a standing
  delegation, one person scheduling and managing on another's behalf. The API
  adds assistants; the scheduling privilege itself is granted in Zoom's web
  portal, so it is not fully programmable, and it is a per-person relationship
  rather than a per-meeting one.

There is also a way to **see** the problem happening:
`meeting.participant_jbh_waiting` fires when someone has waited at least 30
seconds for a host, and `meeting.participant_joined_waiting_room` when someone
lands in a waiting room. Either is a signal the RoB could act on.

So the question was never "add a host field". It was: **what does a RoB look
like when its owner is not in it?** A standing second name on the series, a
per-occurrence stand-in, or something that is not a Zoom concept at all — the
agenda and action items do not need a host, and the meeting that matters is the
working session, not the call.

**Decided 2026-11-16: the standing second name.** Built on 2026-11-20 — see
the history entry in `CHANGELOG.md`. The other two are not ruled out, but
nobody is holding them; if the first goes to review badly, this item is where
they come back.

**This item stays open** because the backup host does not close it. Two things
it does not reach:

- **Ownership transfer mints a new Zoom room** (`ROB-OWNER-020`), and nothing
  carries a backup host across it. The transfer modal should say so; the honest
  answer today is that it does not come along.
- **Seeing it happen.** `meeting.participant_jbh_waiting` and
  `meeting.participant_joined_waiting_room` are still unused, and a RoB that
  stranded its room is worth knowing about afterwards even once it stops
  happening.

### The temporary ownership transfer the product dropped

**Status** · Researched — the history is established; what to do with it is a decision for review, not a build.
**Added** · 2026-11-20
**Source** · looking up what the product offers an owner who will be absent, and finding that it used to offer this.
**Rule** · `ROB-OWNER-042`, `ROB-OWNER-043`, `ROB-OWNER-044`, `PEOP-ACCESS-007`, `PEOP-TEMP-003`, deviation `PEOP-B-016`

**The product once modelled "hold this for me while I am away", and retired it
without a replacement.** The legacy temporary ownership transfer took a
snapshot of a person's owned RoBs, handed them to someone else, and gave them
back on return — which is the shape of the problem the backup host answers.

`ROB-OWNER-042` (Confirmed, PO 2026-10-29) says it is deprecated: no screen
creates one and `createUserOwnershipTransfer` refuses every performer.
Transfers that are still active can only be returned (`ROB-OWNER-043`), which
is why a profile can still show **Return Temporary Ownership** with no way to
start one. `PEOP-B-016` notes the API path still works — the capability is in
the code with nothing calling it.

**What replaced it is not a replacement.** Role Inheritance hands a person's
items over for good: it is built for someone leaving or changing role, and
`ROB-OWNER-037` shows the shape — one ongoing request per person, a terminated
recipient rejected, a pending termination blocking it. Nobody files a role
inheritance request to go on holiday for a week. `TOP-6180`, "Clean up the Temp
Ownership Transfer concept", was closed **Abandoned** on 2026-10-26, so the
half-removed state is where it stops.

**Why this is worth carrying rather than filing as trivia.** It changes how the
backup host reads at review. The proposal is not a new idea arriving from
outside the product — it is a smaller, cheaper answer to a problem the product
already recognised and then stopped answering. A standing name on one series
costs a field on a call that is already made; the thing it replaces was a
snapshot, a background job, a return flow and four open deviations.

**The decision to take:** whether to say any of that out loud. Reviving a
deprecated concept and proposing a field that quietly does its job are
different conversations, and the second one is easier to win.

### Carry "who is covering" from time off into the RoB

**Status** · Researched — both halves exist and neither knows about the other; the join is the open question.
**Added** · 2026-11-20
**Source** · the early-warning alert, which needs to know the owner will be away — and the discovery that the product already stores that.
**Rule** · `TOFF-SLACK-009`, `TOFF-PROF-003`, `TOFF-EDGE-001`, `TOFF-SLACK-005`, `ROB-OCC-025`, `ROB-OCC-067`, `ROB-OCC-038` — checked against the oracle at topteam `6805064` (2026-11-20)

**RoB can see a decline in advance since 2026-11-12, but not an absence — and
an absence is the one somebody planned.**

Declines reach an upcoming occurrence now: `ROB-OCC-067`, changed by `TOP-7503`
(topteam#6899), draws a red ✕ on a future occurrence where there used to be no
response at all. Out-of-office does not. `ROB-OCC-025` is the hard edge there: a
participation status — Present, OOO, Declined, Missing — **exists only from 1
hour after the occurrence ends**, and OOO has no equivalent of the decline
marker. So RoB reads the approved out-of-office day once, afterwards, to score
attendance, and never before the meeting it explains. The only other
forward-looking signal is `ROB-OCC-038`, which counts calendar overlaps and says
*may not attend* — about double-booking, not about leave.

This is the sharper version of the gap: the product will tell you someone
**said** they are not coming, and not that the company already **knows** they
are away.

**Time off has the other half.** `TOFF-SLACK-009`: an employee assigns coverage
roles on their own absence, naming a co-worker or a Slack channel, and the
assignee is notified. `TOFF-PROF-003` and `TOFF-EDGE-001`: the profile shows
**Who Is Covering**, or *"No one is covering this time off"*. `TOFF-SLACK-005`:
mention someone who is out and the bot replies in-thread with who is covering.

So the company already models *this person is out, here is the stand-in*, and a
RoB meeting — the one place where an absent owner has a concrete cost — is the
one place that cannot read it.

**The interesting decision is how far the join goes**, and there are three
rungs, each a real option rather than a step toward the next:

- **Read it.** The occurrence knows the owner has an approved absence covering
  its date, and says so. This is the cheapest and it is what the early-warning
  alert actually needs.
- **Suggest from it.** If that absence names a coverage role whose assignee is
  on the roster, offer them as the backup host rather than asking the owner to
  pick from scratch.
- **Follow it.** The backup host tracks the coverage role. This is the one to
  be suspicious of: coverage roles are free text with a title and a type, not a
  statement about who can host a Zoom call, and `TOFF-VAL-009` allows a Slack
  channel as the assignee — which cannot host anything.

**What to check before any of it:** whether time off is on for the tenants that
have RoB. `TOFF-PROF-003` is conditioned on the time-off feature, and the Slack
coverage roles are TopTeam-only. A RoB that reads an absence has to behave when
there is no time-off module at all, which is the same shape as the no-Zoom
state the backup host already draws.

### Hold the waiting room off

**Status** · Ready — the mechanism is a known field on a call the product already makes, and the screen that depends on it is built.
**Added** · 2026-11-20
**Source** · the second half of the manual fix ops hands RoB owners: turn the waiting room off for the meeting.
**Rule** · `ROB-ZOOM-009`, `ROB-ZOOM-011`, `ROB-ZOOM-013`

**What it is.** A fourth setting on the enforcement pass: every Zoom meeting
linked to an upcoming RoB occurrence is held at `settings.waiting_room = false`,
beside the join-before-host, authenticated-join and recording mode that pass
already holds.

**Why it is not a preference.** The product decided in 2023 that a RoB room
takes join-before-host (TOP-2826, `ROB-ZOOM-009`), and a waiting room overrides
it. So a waiting room on a RoB is not a configuration of the decision, it is a
silent reversal of it. The product does not offer a toggle for the other three
and should not offer one for this.

**No screen.** This is enforcement, not UI. The meeting view already states the
result — *Anyone can join before the host* — and that line is a promise the
product has to keep rather than a control.

**What it touches:**

- **Webinars.** `ROB-ZOOM-009` does not touch join-before-host for them, so this
  should follow the same line and leave webinar waiting rooms alone until
  somebody decides what a webinar RoB wants.
- **Shared rooms.** `ROB-ZOOM-011` already resolves a conflict between two RoBs
  sharing a room by taking the stricter value. A waiting room has the same
  shape: if any RoB on the room wants it off, off wins, because the alternative
  is a RoB that cannot start.
- **Enforcement reads from Zoom** since topteam#6534 (`ROB-ZOOM-013`), so a
  waiting room switched on by hand would be switched back on the next pass,
  which is the behaviour this needs.
- **`B-014` is upstream.** On a room the product never recognises, none of this
  is enforced — the same hole the other three settings fall down.

**One thing to check before building:** whether Toptal's Zoom account locks the
waiting room at the account or group level. A locked setting cannot be turned
off per meeting by the API, and if that is the case this item becomes a Zoom
admin change rather than a code one.

### What else Zoom could carry

**Status** · Researched — what the API offers, checked 2026-11-16; which of it a RoB should use is still a design call.
**Added** · 2026-11-16
**Source** · a standing interest in what the RoB feature could get from Zoom beyond what it uses today.
**Rule** · `ROB-ZOOM-001`, `-005`, `-009`, `-011`, `-073` — the baseline; the rest is not covered, because the product does not do it.

What the product takes from Zoom today is narrow: it creates the room, enforces
three settings on it, pulls cloud recordings and gates who may watch them, and
reads attendance. Provisioning, compliance and evidence — all after the fact,
none of it in the meeting.

**What the API offers that a RoB could use.** Each of these is a published
endpoint or field, not a guess; what none of them is yet is a decision.

| Capability | Where | What it would give a RoB | Gate |
|---|---|---|---|
| **Alternative hosts** | `settings.alternative_hosts` on the meeting object | someone who can start the meeting when the owner is away — **used**, as the backup host, 2026-11-20 | both users Licensed, same account |
| **Scheduling privilege** | `POST /users/{userId}/assistants`, `GET /users/{userId}/schedulers` | a standing stand-in for a person rather than a meeting | Licensed; the privilege itself is granted in Zoom's portal, not by API |
| **AI Companion summary** | `GET` meeting summary, `meeting.summary_completed` webhook with `summary_content` as Markdown | the written record a RoB is supposed to leave, next to the agenda it was meant to follow | Pro+, AI Companion summary on, not E2EE |
| **Transcript** | `TRANSCRIPT` / `CC` cloud-recording files; `meeting.aic_transcript_completed` | what was said under each agenda item, if the timing can be matched | cloud recording on |
| **Polls** | `POST /meetings/{id}/polls`, `batch_polls`, past-results and report scopes | a RoB's output is decisions — a poll is the one place Zoom records one | Pro+, polling enabled, **not instant meetings** |
| **Breakout rooms** | `settings.breakout_room.rooms[]`, pre-assigned by e-mail | a working session split by workstream, pre-assigned from the RACI we already hold | pre-assign only; live control is SDK, not REST |
| **In-meeting chat** | `CHAT` (text) and `CHAT_MESSAGE` (JSON, incl. waiting-room and deleted) recording files | action items people type instead of saying | cloud recording on |
| **Waiting-room / join-before-host signals** | `meeting.participant_jbh_waiting`, `meeting.participant_joined_waiting_room` | the absent-owner problem, observable instead of reported | webhook subscription |

**Where the value is, on this reading.** The summary and transcript are the ones
that touch what a RoB is *for* — it exists to produce decisions and actions, and
those are the only Zoom artefacts that contain them. Polls are the narrow,
unglamorous version of the same thing and are the easiest to act on, because a
poll result is structured where a summary is prose. Breakout rooms are a real
fit for the working session and the cheapest to try, since the RACI already
tells us who goes where. Chat is a long shot: people do type actions into it,
but separating those from "can you hear me" is the whole problem.

**Three constraints that bound any of it.**

- **The product sets it, not the user.** Enforcement overwrites settings changed
  by hand in Zoom at the next pass (`ROB-ZOOM-009`), so a proposal that asks
  someone to configure something in Zoom is a proposal that will be undone.
- **Recording access is already decided** and deliberately does not follow the
  Zoom host (`ROB-ZOOM-073`). A design that re-derives who may read a summary or
  transcript from Zoom is arguing with a settled rule — summaries and
  transcripts should inherit the recording rules, not invent their own.
- **`B-014` is upstream of all of it.** A room on a host other than `zoom.us` or
  `toptal.zoom.us` is never linked, so nothing here reaches it. Anything built
  on this list inherits that hole.

**Not checked in this pass**, and worth knowing before committing: the plan tier
Toptal is actually on, whether AI Companion summaries are enabled on the
account, and the live in-meeting surfaces (Zoom Apps and the Meeting SDK), which
are a different kind of integration from everything above — an app running
inside the call rather than a server reading it afterwards. That is the obvious
next question if any of this looks worth having.

### Pre-reads

**Status** · Researched — the one thing a participant is meant to be able to add, and there is nowhere to add it.
**Added** · 2026-11-16
**Source** · the prototype has no pre-reads section at all (`grep -c pre-read` on `index.html` is 0).
**Rule** · `ROB-PREREAD-010`, deviation `B-206`, `ROB-PREREAD-014`

A RoB carries pre-read links per occurrence, and the participant role — which
otherwise reads everything and writes almost nothing — is supposed to be able
to add one. Our meeting view has no section for them, so the participant's one
intended contribution has nowhere to go.

The decision worth having is **whose "Add link" shows.** A PO decision of
2026-10-29 says participants may add links; the shipped code still refuses them
and only the owner and RoB admins can (`B-206`, open). So the two roles in this
prototype would be designed against the rule rather than against the app, which
puts it in *We follow the spec where the product does not* when it is built.
Whether a participant may also **remove** a link — their own, or anyone's — is
not decided; removal stays with the owner and admins today (`ROB-PREREAD-014`).

### The attendance summary

**Status** · Researched — the only admin-only read in the whole rights table, and it is not built.
**Added** · 2026-11-16
**Source** · absent from the meeting view; the rights table on `rights.html` already promises it.
**Rule** · `ROB-OCC-032`, `ROB-OCC-023`, `Q-050` (resolved 2026-10-28)

Per-occurrence attendance is readable by anyone who can open the RoB — that
much the roster already shows. The **aggregate** summary is the exception:
owner and RoB admins only, and it needs active integrations. It is the single
row in *What each role can do* where an admin sees something a participant
cannot and there is no screen behind it.

`Q-050` asked whether per-occurrence attendance should be restricted too and
was answered **no** — today's split is the intended one. So the design question
is not who sees it but what it says: over what span, counting what, and whether
a person's own record reads differently from everyone else's.

### Multi-select filters

**Status** · Researched — closing this retires two rows from the departures table.
**Added** · 2026-11-16
**Source** · [Where it departs from the product](CHANGELOG.md#where-it-departs-from-the-product).
**Rule** · `ROB-VIEW-019`, `-025`, `-026`, `-027`, `ROB-VIEW-030`

All five directory filters are multi-select in the product; all five are
single-select here. That is the oldest departure in the file and the only one
nobody chose — it was never a proposal, just what got built first.

Two things come with it rather than after it. The tags read differently when a
filter holds several values — `Divisions: <names>`, and "<N> users selected"
past five people or while names load (`ROB-VIEW-030`). And the
clear-by-reselect gesture we added when the **All** row came out exists only
because the selection is single; multi-select would retire it, which is the
cleanest kind of backlog item — one that deletes code rather than adding it.

### Action-item comments: keep them or cut them

**Status** · Idea — we have a feature the product deliberately removed.
**Added** · 2026-11-16
**Source** · `openCommentPop` in `index.html` — a threaded comment popover on every action item.
**Rule** · `ROB-ACTION-008`

Action items here carry threaded comments. The product carries none, and not by
omission: notes shipped in late June 2026 and were taken out again within a
week, data dropped with them (`TOP-7168`, `TOP-7169`). The spec is flat about
it — discussion about an action item happens outside the product.

So this is a proposal we never made deliberately, and it is now a row in the
departures table. Two honest endings: cut it, and the prototype stops promising
something the product dropped on purpose; or keep it and say why it should come
back, which means knowing why it went — and that is the research this item
needs before it can move past Idea.

### The roster's own-row is fixed in markup

**Status** · Idea — needs a look before it is worth more than this line.
**Added** · 2026-11-16
**Source** · `.md-person.is-me[data-md-me]` is one hard-coded row; the viewer role only changes its CSS.
**Rule** · the spec does not cover this — it is a fixture problem, not a behaviour one.

"You" in the roster is always the same person, and switching to the participant
role restyles that row rather than moving it. It reads correctly in both roles
today because the fixture happens to line up. Worth confirming it still does
before anything else is built on the roster.

---

## Dropped

*Nothing yet. When something is dropped it moves here with the reason, not out
of the file.*

---

## For an agent adding to this file

These are rules, not suggestions. An item that breaks one is worse than no item,
because someone will act on it.

- **Read before writing.** `CHANGELOG.md` — all of it, including *History*,
  *Open, and worth revisiting* and *Where it departs from the product* — and
  every item here. An idea already recorded in one of those is not new, and a
  second copy is how two people end up designing the same screen differently.
- **Never state what the product does without a rule id.** Query the oracle
  (`search_oracle`, then `get_rule` for the full card before asserting). If
  nothing covers it, write *the spec does not cover this*. Do not infer product
  behaviour from this prototype — it is a proposal, not a description.
- **Never paste the oracle's prose into this repo.** It is public and the
  oracle is not. Ids are the way back to it; a short restatement in your own
  words is fine, a quotation is not. The same goes for internal ticket text.
- **Check the card's status and date.** A rule can be `Inferred`, a question can
  be `resolved` with the opposite answer to the one you expected, and an
  `observed_today` line can mean the shipped app does not do what the rule says.
  Any of those changes what the item is about, so read them before writing.
- **Append under *Open*.** Do not reorder, rewrite or re-status an existing item
  — someone else's judgement is in it. Say so in the chat instead.
- **Start at Idea.** `Researched` requires ids you actually read. `Ready`
  requires knowing what you would build, which is a design call, not a research
  one — leave it to a person.
- **One item per thing.** If the title needs "and", it is two items.
- **An item needs a decision in it.** "Build the pre-reads section" is a chore.
  "Whose *Add link* shows, given the PO said participants and the code says
  otherwise" is a backlog item. If you cannot find the decision, the honest
  outcome is not to add the item.
