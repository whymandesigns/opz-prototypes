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

**Status** · Researched — the product has one safeguard for this and three documented ways it does not reach.
**Added** · 2026-11-16
**Source** · raised as a red flag: if the owner is away, participants wait in a waiting room and the meeting does not happen.
**Rule** · `ROB-ZOOM-009`, `ROB-ZOOM-001`, `ROB-OWNER-020`, deviation `B-014`

The product does have an answer, and it is not a host at all: every Zoom meeting
linked to an upcoming RoB occurrence is **forced to "join before host" ON**,
along with authenticated-join and a recording mode, and anything changed by hand
in Zoom is overwritten at the next enforcement (`ROB-ZOOM-009`). When that
enforcement reaches the room, the owner being away costs the meeting its host,
not its start.

**It does not always reach the room.** Three cases, all in the spec:

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

So the proposal is not "add a host field". It is: **what does a RoB look like
when its owner is not in it?** A standing second name on the series, a
per-occurrence stand-in, or something that is not a Zoom concept at all — the
agenda and action items do not need a host, and the meeting that matters is the
working session, not the call. Worth deciding which of those we are proposing
before any of it is drawn.

### What else Zoom could carry

**Status** · Idea — the integration uses a few of Zoom's capabilities; nobody has looked at the rest.
**Added** · 2026-11-16
**Source** · a standing interest in what the RoB feature could get from Zoom beyond what it uses today.
**Rule** · `ROB-ZOOM-001`, `-005`, `-009`, `-011`, `-073` — the baseline; the rest is not covered because the product does not do it.

What the product already takes from Zoom is narrow and worth writing down before
asking for more: it creates the room, enforces three settings on it, pulls cloud
recordings and gates who may watch them, and reads attendance. That is
provisioning, compliance and evidence — all of it after the fact, none of it in
the meeting.

The question is which of Zoom's other capabilities would actually serve a RoB,
given what a RoB is for: a quick round of status, then a working session that
ends in decisions and actions. Candidates worth checking rather than assuming —
transcripts and summaries against the agenda, in-meeting polls for the decisions
a RoB is supposed to produce, breakout rooms for a working session, chat as a
source of action items, registration or webinar mode for the large ones,
scheduling privilege for the item above. Which of these Zoom's API actually
exposes, and on which plan, is the research — not a list to design from.

Two constraints that are already known and should bound it. Enforcement
overwrites settings changed by hand (`ROB-ZOOM-009`), so anything we propose has
to be something the product sets, not something a user configures in Zoom. And
recording access is already decided and does not follow the Zoom host
(`ROB-ZOOM-073`), so a proposal that re-derives access from Zoom is arguing with
a settled rule.

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
