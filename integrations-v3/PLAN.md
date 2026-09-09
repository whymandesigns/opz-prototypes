# Integrations (Admin Settings) — prototype plan

The Integrations screen under **Admin Settings** in the Operationalize app shell,
built against the Figma reference and the designmd system.

## HireGlobal MVP scope

The whole integration is **one card on this page**. Nothing else.

| # | Step | Status |
|---|---|---|
| 1 | Admin sees a HireGlobal card alongside the others and clicks **Connect** | **Built** |
| 2 | They link their Operationalize tenant to their HireGlobal tenant, as the customer/owner account | **Built** — sign-in embed |
| 3 | Once connected, push people data one way: full name, email, position, reporting relationships | **Built** — share screen |
| 4 | HireGlobal ingests it and builds a plain list of people | **Built** — people screen |

Everything after step 4 happens on HireGlobal's side.

### The job to be done

> Someone already runs their org in Operationalize and likes it. They go
> *"Operationalize is so great, but I want to manage my payments too — oh, they
> have HireGlobal! I want to pay my people through HireGlobal!"* They go to
> Integrations, connect HireGlobal, and their HireGlobal account gets prefilled
> with the people they already have in Operationalize. Then they go to
> HireGlobal and manage payments there.

That's the whole job.

### Explicitly out of scope

No OKRs, no RoB meetings, no Initiative connections, no process diagrams. The
data flow is **one way, people only** — full name, email, position, reporting
relationships. Operationalize does not read anything back from HireGlobal, and
nothing about payments surfaces in Operationalize.

### Still open

- ~~**One-shot or ongoing?**~~ **Decided 2026-09-09: ongoing.** The connection
  is a standing sync, not a one-off prefill — people join, change position and
  move under a new manager, and HireGlobal follows. This makes the card's
  `Last synced` row load-bearing rather than decorative, and the copy across the
  share and people screens now says so. See *Ongoing sync* below for what it
  opens up.
- **Who is excluded** — contractors, inactive people, anyone without an email.
  The share list currently shows all 12 with no exclusions.
- **What happens when a person fails to ingest** — no partial-failure state.
- **Disconnect.** The connected card offers it; nothing is behind it, and it is
  undecided whether disconnecting removes the people from HireGlobal.

## Where it lives

```
features/integrations-v3/
├── index.html   ← the prototype (design system inlined, logos as data URIs)
├── assets/      ← third-party brand logos exported from Figma (sources)
└── PLAN.md      ← this file
```

Naming: `integrations/` and `integrations-v2/` (both Jun 2026) are earlier,
unrelated passes. design.md §7 says a feature folder is never reused, so this is
`-v3` rather than an edit of either.

Served at `/features/integrations-v3/` by the root `.claude/launch.json` dev server.

## Source of truth

**Figma:** [Operationalize → node `35846:262599`](https://www.figma.com/design/hMZ8Nw27ub8PaIgPa0fgJf/Operationalize?node-id=35846-262599)

Pulled via `get_design_context`. Code Connect mapping was declined — see
*Code Connect* below.

## What's built

Page head (title + subtitle), a rule, then three sections of integration cards:

| Section | Cards |
|---|---|
| **Core** | Google Workspace (Interrupted → Reconnect) · Zoom (Not Connected → Connect) · Slack (Connected → Disconnect) |
| **OKR connectors** | Tableau · BigQuery — both Not Connected, no meta rows |
| **Other integrations** | Jira · HireGlobal — both Not Connected |

**Connect on HireGlobal** opens the HireGlobal account-setup flow *in page* —
see *The HireGlobal embed* below.

Card anatomy: 44×44 logo + name · description · optional meta list
(Domain / Connected as / Last synced) · connection status · full-width CTA.
Each of the last three regions sits under its own hairline; the CTA is pinned
with `margin-top:auto` so a row of uneven cards still lines its buttons up.

## designmd components used

| Design element | designmd |
|---|---|
| Integration card | `.card` |
| Card / section title (16/24 semibold) | `.card-title` type role — `--type-h3` |
| Descriptions, meta rows (13/20) | `--type-body-sm` + `--color-text-muted` |
| Status label (11/16) | `--type-body-xxs` |
| Connect / Reconnect CTA | `.btn .btn-primary` |
| Disconnect CTA | `.btn .btn-secondary` |
| Connected / Not connected glyph | `#i-link` / `#i-unlink` |
| Domain · Connected as · Last synced | `#i-globe` · `#i-avatar` · `#i-update` |
| Interrupted warning | `#i-warning-solid` |
| Stale-sync red, CTA green | `--color-danger` · `--color-brand` |

**HireGlobal** comes from its own frame,
[node `35852:562831`](https://www.figma.com/design/hMZ8Nw27ub8PaIgPa0fgJf/Operationalize?node-id=35852-562831).

**Brand logos are the exception.** Google, Zoom, Slack, Tableau, BigQuery,
Jira and HireGlobal are third-party marks and are not in the designmd icon pack. They were
exported from Figma (HireGlobal supplied directly), kept in `assets/`, and
inlined as base64 data URIs so the prototype stays a single self-contained file.
`inline.py` doesn't touch them.

**Zoom** is the one wordmark rather than a square mark, so it takes a per-brand
width (`.ic-logo-zoom`, 89px) chosen so `object-fit: contain` lands its glyph at
a 20px optical height inside the shared 44px logo row.

**HireGlobal** uses the square app-icon tile, so it takes the standard 44x44
`.ic-logo` box with no extra rules — the frame draws it hard-edged, so the
rounding tried earlier was dropped. The unused wordmark is kept at
`assets/hireglobal-wordmark.svg`.

### The `Domain` row

Each card shows **its own tool's tenant/instance domain**, not the vendor's
marketing domain — `toptal.zoom.us`, `toptal.slack.com`,
`toptal.atlassian.net`. The Figma frame had every card reading `toptal.com`,
which is right only for Google Workspace (where the Workspace domain genuinely
is the company domain).

The reasoning: the logo already says which vendor it is, so a vendor domain in
this row is dead weight. Paired with `Connected as`, a tenant domain answers the
question the row exists for — *which account is wired up?*

HireGlobal keeps `hireglobal.com` as its frame draws it; its client portal has no
per-customer subdomain, so that is its instance domain too. Tableau and BigQuery
have no meta rows at all, so nothing to set.


## Deliberate deviations from the Figma frame

| Thing | Figma | Here | Why |
|---|---|---|---|
| Card radius | 8px | 12px (`--ic-radius-lg`) | designmd's `.card` radius. Composing beats overriding (design.md §6) — but worth confirming which is right. |
| Card inner divider | `#F3F4F6` (gray-150) | `--color-border` (gray-200) | Nearest semantic border token; one step darker, imperceptible at 1px. |
| Card shadow | Shadows/Level 2 `0 4px 4px /8%` | `--ic-shadow-md` `0 4px 12px /8%` | Same offset and alpha, nearest system token. |
| Card width | 369px | ~364px | Page padding is 32px per the frame; the remainder is the scrollbar. |
| `Domain` per card | every card `toptal.com` | each tool's tenant domain | See *The `Domain` row* above. |
| Status label colour | graphite-800 on the Core frame, graphite-700 on the HireGlobal frame | `--color-text` everywhere | The two frames disagree; one value across all cards beats matching each frame and looking like a bug. |

## Questions for the designer

1. ~~**Zoom and Jira show meta rows while disconnected.**~~ **Answered
   2026-09-09** by the HireGlobal frame: meta rows stay visible when
   disconnected, with `-` standing in for values that aren't known until the
   connection exists. So Zoom and Jira are right as drawn — but that leaves
   **three** treatments in the page: real values (Google, Zoom, Slack, Jira),
   `-` placeholders (HireGlobal), and no meta block at all (Tableau, BigQuery).
   Tableau and BigQuery now look like the outliers. Should they carry a
   `Domain` row with `-` for the other two?
2. **Card radius** — 8px in the frame vs the system's 12px. Which wins?
3. The frame contains extra cards hidden from the render (duplicate Slack /
   BigQuery with "Description of the connection will appear in this area"). Read
   as scaffolding and not built — confirm.
4. Those hidden cards use a **different connected treatment**: a "Disconnect"
   text link at the right of the status row plus a narrow (114px) button, rather
   than the full-width secondary button the visible Slack card uses. Two
   connected variants, or is one superseded?

### Ongoing sync — what the decision opens up

Ongoing rather than one-shot (decided 2026-09-09) settles the copy but raises
questions a one-off push never had to answer. None are designed:

- **What triggers a re-sync?** Event-driven as records change in Operationalize,
  or on a schedule? The people screen says "updated just now", which promises
  something fairly live.
- **Offboarding — the sharp one.** When someone is removed or deactivated in
  Operationalize, what happens in HireGlobal? This is a payroll system: silently
  leaving them behind means continuing to pay someone who left, and silently
  removing them may destroy pay history someone needs. Neither default is safe,
  so it needs a deliberate answer rather than falling out of the sync logic.
- **Who wins on conflict?** If someone edits a person's position in HireGlobal,
  does the next sync overwrite it? Operationalize being the source of truth for
  org data argues yes, but that makes the HireGlobal field quietly un-editable
  and should say so.
- **Where the admin sees sync health.** The card shows `Last synced`. There is no
  surface for "3 people failed to sync" or "sync paused". Worth deciding whether
  the card grows that or it lives on a detail page.
- **Turning it off.** Disconnect now means stopping a live sync, not just
  dropping a link — a heavier action than the current secondary button implies.


## The connect flow

Five screens, alternating between the two products. Which system owns a screen is
the load-bearing decision — see *Where the confirmation lives* below.

| # | Screen | Whose UI | Where |
|---|---|---|---|
| 1 | Integrations, HireGlobal card | Operationalize | `.page-view[data-page="integrations"]` |
| 2 | Sign in (+ 2s loader) | HireGlobal | iframe · `#hg-doc-signin` |
| 3 | Share people with HireGlobal | **Operationalize** | `.page-view[data-page="hireglobal-share"]` |
| 4 | Sync modal (~10s) | Operationalize | `#hg-sync-overlay` |
| 5 | Card Connected + success toast | Operationalize | rewritten in place |
| — | People synced | HireGlobal | iframe · `#hg-doc-people` — via the toast action |

Sign-in credentials are prefilled with a placeholder (`admin@toptal.com`) so the
flow can be walked without typing. The password value is a visible dummy string,
not a credential.

**Sign in holds on a loader for 2s**, then hands off and fires a success toast —
`Signed in to HireGlobal as admin@toptal.com`, timed, auto-dismissing. The word
"successfully" is deliberately left off: the success variant's green tick already
carries that, and the account is the part an admin cannot otherwise verify at a
glance.

The flow therefore raises **two** toasts at different moments — sign-in landed,
and sync finished. That is intentional; they confirm different things. The form is *replaced*
by the loader rather than dimmed behind a scrim — a light scrim over HireGlobal's
dark proof panel looked broken, and half-dimmed inputs invite clicking. A second
click is ignored so it cannot queue a second hand-off.

The loader is designmd's chase spinner (`.chase-cw`, `size-lg`), copied into the
frame with its two token references resolved to literals, because the frame
carries no designmd tokens by design:

| Token | Literal |
|---|---|
| `--ic-palette-graphite-300` (resting) | `#8F96AA` |
| `--color-accent` (12% flash) | `#204ECF` |

`--color-accent` resolving to `#204ECF` is the same blue HireGlobal uses — both
products sit on the Toptal palette — so the loader needed no recolouring for the
HireGlobal context. The 24 segment delays are staggered by a script inside the
frame using designmd's own formula, `((n - 1 - i) / n * 1.1)s`, since the frame
cannot reach the host's script block.

Note this is the one place designmd crosses into the embed. Justified on the
grounds that the wait *is* the Operationalize↔HireGlobal handshake and the user
is about to be returned to Operationalize — but it is a deliberate exception to
*None of them are built from designmd* below, not an oversight.

### Where the confirmation lives — and why

Screen 3 is **Operationalize's own screen in designmd**, not a page inside the
frame. This was a judgement call, so it is worth stating:

- It is the host's data leaving the host. The host should be the thing that asks.
- Rendering it inside the embed would mean HireGlobal drawing a list of people it
  has not been given yet — the wrong system holding the data at the wrong moment.
- The visual switch back to designmd is the signal. The admin sees Operationalize
  chrome for the decision, HireGlobal chrome for the result.

**It can be dropped.** The job-to-be-done reads as *"connect and it's prefilled"*
— magic, no friction. If that is the intent, delete the share screen and push on
sign-in success. The trade is that the admin never sees their org chart leave.
One click against an explicit moment of consent.

### The push

`Start syncing 12 people` opens a **blocking modal** that runs for ~10s, then
drops the admin back on Integrations with the card Connected and a success toast.

| Stage | Duration | Shows |
|---|---|---|
| Sending people | 7.6s | live counter, one tick per person |
| Building your people list | 1.6s | tick when done |
| (hold on 100%) | 0.8s | both ticked |

There is deliberately **no "Connecting to HireGlobal" step**: the connection is
already live by the time the admin reaches the share screen — they signed in to
get here — so that step would report work already done. Its 1.2s went to
`send`, keeping the total at ~10s.

The timings are theatre. The counter is the honest part — it is the thing
actually being sent, and it is what makes 10 seconds legible rather than a
stalled spinner. No spinner was added: designmd's loader is the chase mark, and
a second spinning thing here would compete with it, so a pulsing stage dot and
the progress bar carry it instead (sending owns 2→85%, building the rest).

**The modal has no close control.** A sync mid-flight should not be dismissable
into a half-sent state. The shared overlay handler closes any `.modal-overlay`
on Escape or a backdrop click, so both are swallowed in the capture phase while
`syncing` is true — cheaper than forking a bespoke overlay that would duplicate
`.modal-overlay`'s styling. Verified: the modal survives both.

⚠️ **Worth a second look.** A 10-second modal with no escape hatch is a real
commitment to make an admin sit through, and a live sync of a large org will not
take a fixed 10 seconds. A backgroundable version — start the sync, return to
Integrations immediately, let the card show `Syncing…` and toast on completion —
would scale better and is barely more work. Built as asked; flagged because the
blocking version is a decision rather than a default.

### Where the people screen went

The flow now ends on Integrations, which would leave HireGlobal's people screen
orphaned. It is reached from the success toast's **View in HireGlobal** action
(`behavior: 'action'`), which is also the only thing in the flow that models
"go and do your payroll now" — the actual next step in the job to be done.

Sample data is 12 people across a four-level reporting line, so the
`Reports to` column has something real to show.

The primary button reads **Start syncing 12 people**, not "Share" — the action
establishes a standing connection rather than performing a single transfer.


### designmd gap — `[hidden]` is inert under an author `display:`

Each frame document carries its own reset, and none of them neutralised
`[hidden]`. An author `display:` outranks the UA stylesheet's
`[hidden] { display: none }`, so the attribute silently did nothing on any
element given an explicit display — the sign-in loader rendered under the form
on load until `[hidden] { display: none !important; }` was added to all three
resets.

Worth knowing because `performance-reviews` already hit the same gap on `.btn`,
and a check of `el.hidden` reads the *attribute*, not whether the element is
actually invisible — which is how this survived a round of verification.


## The HireGlobal embed

Connect on the HireGlobal card swaps the content column for HireGlobal's own
screen. In page, not a modal: the topbar and sidenav stay put and the embed fills
the column beneath them.

### Three screens, one frame

| Screen | Template | Reached by |
|---|---|---|
| **Sign in** (default) | `#hg-doc-signin` | Connect on the HireGlobal card |
| **People imported** | `#hg-doc-people` | after the push on the share screen |
| **Sign up** (parked) | `#hg-doc-signup` | "Sign up" on the sign-in screen |

**Sign in is the default** — an Operationalize admin is assumed to already have a
HireGlobal account, so Connect is a *link-your-account* step, not a create-one
step. Sign up is kept rather than deleted: it is still where a genuine
first-time tenant has to land, and it is one link away.

**Sign up is a dead end, by decision** (2026-09-09). Its "Set up account" button
is inert — the branch is walked to that screen and stops. Not an omission to be
filled in later without a fresh decision.

Sources: sign-in is rebuilt from the live page at `client.hireglobal.com/login`
with values read off it (57.4/42.6 panel split, 28/42 semibold heading, 420px
controls at 48px, `#204ECF` submit, `#f3f4f6` panel, `#d8d9dc` borders). Sign-up
is [Figma node `35852:571546`](https://www.figma.com/design/hMZ8Nw27ub8PaIgPa0fgJf/Operationalize?node-id=35852-571546).

### How it's put together

- A sibling `.page-view[data-page="hireglobal-connect"]` holding one `<iframe>`.
- Each screen lives in a `<template>` pushed into the frame's `srcdoc` **on
  demand**, not at load. Keeping them in templates means the markup stays
  readable in source (no HTML-escaping) while the prototype stays one
  self-contained file, per design.md §7.
- `sandbox="allow-forms allow-popups allow-scripts"` — deliberately **no**
  `allow-same-origin`, so the frame runs its own code but stays an opaque origin
  the host cannot read into.
- Because of that, sign-in → sign-up crosses the boundary by **`postMessage`**,
  not by the host binding a listener inside the frame. That is the same channel
  the real integration will need to signal "tenant created" back to
  Operationalize, so the prototype models the actual seam.
- Assets inside the frame are data URIs: `srcdoc` has no base URL of its own.
- The frame is sized off its **container**, not the viewport
  (`height: calc(100% + padding*2)` against the negative margin that cancels the
  column padding). Viewport math (`100vh` minus a hardcoded topbar) was two
  pixels out and left the shell with a scrollbar behind a frame that already
  scrolls itself.

### None of them are built from designmd

Everything inside the frame uses HireGlobal's own tokens — its blue (`#204ECF`),
its 14/22 body scale, its `#d8d9dc` field borders. An embed that silently adopted
the host's design system would disguise the hand-off the admin is actually
making. The one thing borrowed from the host is the `@font-face` pair: both
products set in Proxima Nova, and the faces are already data-URI'd in this file.

Two asset substitutions, both to keep the file's weight sane:

- The live sign-in layers a **marketing photograph** under its gradients. That is
  approximated in CSS rather than embedding a third-party JPEG.
- The **HireGlobal · by Toptal** lockup shipped as a 65 KB Illustrator export,
  58 KB of which was an Adobe `<metadata>` dump. Stripped to 6 KB.

The US flag in the sign-up country select ships from Figma as four separate
layers rather than one flattened asset, so it is reassembled at the coordinates
Figma reports.

### Open question — the frame screens still have no way back

The share screen (Operationalize's own) has breadcrumbs and a Cancel button. The
three screens **inside the frame** have no back, cancel or breadcrumb control, and the embed covers the
whole content column. The only escape is noticing the sidenav is still live and
clicking **Integrations** again (which does work — verified).

That is a real gap rather than a prototype shortcut, so nothing was invented to
paper over it. Worth deciding: a slim host-owned bar above the frame carrying a
back control and the "you are leaving Operationalize" framing would fix it
without becoming a modal.

### Not built

- Forgot password, Remember me, and the three OAuth paths are inert.
- Anything past sign-up's **Set up account** — the agreed stopping point above.

### Verifying the bridge

The frame is an opaque origin, so the host cannot click into it and coordinate
clicks through the preview pane are unreliable. To exercise the real path under
the real sandbox, append a probe to the srcdoc that clicks the link from inside:

```js
const f = document.getElementById('hg-embed');
f.srcdoc = document.getElementById('hg-doc-signin').innerHTML +
  '<script>document.querySelector("[data-hg-signup]").click()<\/script>';
```

The parent should receive `{hg:'signup'}` and swap the frame to the sign-up
screen. Verified working on 2026-09-09.

## Conventions this prototype follows

- **Shell.** Topbar + `.app-shell` (`.sidenav` + `.app-shell-main`), same markup
  as `features/performance-reviews`. Nav items without a matching `.page-view`
  are decorative: they take active state but don't navigate.
- **Selectors are scoped.** Sidenav links and page views share `data-page`
  values, so anything targeting a view must be `.page-view[data-page="…"]`.
- **Shared handlers.** The first `<script>` block is the delegated component
  handler set, copied from `designmd/example.html` via `performance-reviews`.
  example.html's showcase-only code is excluded — it throws on load.
- **Re-inline after a system change:** from `designmd/`, run
  `python3 inline.py ../features/integrations-v3/index.html`. Idempotent, and it
  preserves the prototype-local `<style>` block.

## Code Connect

Declined for now. `designmd/figma-map.json` already records the designmd ↔ Figma ↔
Picasso binding (39 components, 33 with a Figma node), and design.md §9 treats
Code Connect as phase 2 — `.figma.ts` templates **generated from that file**, not
hand-authored, and published against the **Product Library v2.0** file
(`0zTTN9YKOABPGLQ4NsyEW5`), not this product file.

## Edge states to cover (design.md §9)

`?states=1` for the switcher, `?state=<key>` to deep-link one.

- [x] `default` — as designed
- [ ] Empty — no integrations available to this org
- [ ] Error — connection failed / token expired (partly covered by *Interrupted*)
- [ ] At scale — many integrations per section
- [ ] Long text — long integration names and descriptions
- [ ] Loading — while connection status resolves
- [ ] Permissions — what a non-admin sees
- [ ] Embed fails to load — HireGlobal down, or the frame blocked
- [ ] Sign-in failure — wrong credentials, locked account
- [ ] Already-linked — admin whose HireGlobal account is connected elsewhere
- [x] The people push — in-progress states covered by the sync modal
- [ ] Push failure — partway through, or refused outright
- [ ] Re-sync of an already-connected tenant (the flow assumes first connect)
