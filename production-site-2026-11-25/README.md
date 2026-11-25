# Production site · 2026-11-25

The product as it ran on 25 November 2026, rebuilt on the designmd kit. It is a
reference: start an update, or a new version of a screen, from its copy here
instead of from memory.

- **What matches the app:** layout, labels, order and structure of each screen,
  at desktop width and at phone width. Lists are tables on a wide screen and
  cards on a phone, as in the app.
- **What does not:** the people and the records are made up. The app's own
  tenant says "Business as Usual"; these screens say "Processes", as every
  Operationalize prototype does (`BAU-TERM-001`). The top bar and side nav are
  the kit's, so the business-line switcher is not there.
- **States:** tabs switch panels, and the Processes list opens its drawer,
  create drawer, RACI and query panel. Add `#tab-2` to a screen's address to
  open its third tab, or `#open-<id>` to open a drawer or modal. `STATES` in
  `_src/screens.py` lists every state built, `STATES_2` the second round
  (view modes with `#show-view-1`, filter and query panels, calendar views,
  the account menu). The Initiatives filters follow the Processes ones by
  analogy; they were not opened on staging. Drawers and modals on Initiatives,
  OKRs and RoB Meetings are not built yet.

`index.html` is our own list, not a product screen, so it has no app shell. It
shows every primary screen with a tick when built, when it was built and
updated, and how long each took. The times come from `BATCHES` and `UPDATES`
in `_src/screens.py`: add an entry there after every build or update pass.

Where the kit has no component, the element is built here rather than
approximated: `_src/elements.css` holds twenty-six of them (`ps-*` classes, kit
tokens only, no media queries), and `elements/index.html` shows each one live
as a candidate for `components.css`. The linter reports them as `local-class`
warnings, which is the point: they are the list of what the kit is missing.

Three things still differ from the product on purpose:

| In the product | Here |
|---|---|
| A real map on People › Geography and on a profile | a placeholder panel with pins; a map needs a map provider |
| Curved lines in the reporting-relationships graph | the same tree with straight lines |
| Illustrated badges and empty-state pictures | an icon in a ring |

## Rebuilding

The screens are generated from `_src/`, so a change to the shell reaches all of
them:

```bash
python3 production-site-2026-11-25/_src/build.py     # write every screen
python3 ../designmd/lint.py production-site-2026-11-25/index.html production-site-2026-11-25/*/index.html
for f in production-site-2026-11-25/index.html production-site-2026-11-25/*/index.html; do python3 ../designmd/inline.py "$f"; done
```

`_src/screens.py` holds each screen's content as kit markup; `_src/build.py`
wraps it in designmd's `template/index.html`, the same shell
`tools/new-prototype.py` copies.

## Phone versions

Every screen is one file that changes layout under 1024px. On staging, a phone
is sent from Processes, Initiatives and OKRs to RoB Meetings: the product has
no phone layout for those three lists. The reference keeps a phone layout for
them anyway, built from the same cards as the dashboard.

## Adding an element to the library

On the elements page every element has **Add to library**. It copies a request
with the command behind it:

    python3 production-site-2026-11-25/_src/promote.py ps-bars

The script moves that element's rules from `_src/elements.css` into designmd's
`components.css`, regenerates `dist/kit.json` and rebuilds the reference. The
element stays on the elements page with an "Added to library" badge and the
date (recorded in `_src/promoted.json`), the linter stops flagging it as
local, and the next screen picks it up from the kit. The filter at the top of
the page (`elements/#added`) lists just the added ones: that is the list to
hand to developers, who do not have them in their library yet. `--list` shows what can be moved,
`--dry-run` shows the change without making it. Nothing is committed: review
and commit the designmd change as any other.

## Icons the kit lacks

Twelve icons and drawings the product has and the kit's sprite does not were
drawn for the reference and kept in `_src/icons.svg`: open in new tab, Slack
in colour, the eight recognition badges and the two empty-state drawings. They
are coloured with the kit's tokens. `icons/index.html` lists them with the
same See it in place, Add to library, badge and filter as the elements page;
`promote.py i-external-link` moves one into designmd's `icons.svg`. The badges
are redrawn, not copied: the Culture Ambassador flag is plain where the
product's carries the company mark.

## Comparing with staging

Every screen carries a floating **Open on staging** link (bottom right) that
opens the same view on the staging server in a new tab. It is ours, not part
of the product. Three screens need a record id the reference does not keep
(an initiative, a meeting, a talent; and the self-review): their link opens
the nearest list instead and says so. The paths are in `STAGING` in
`_src/screens.py`. Staging needs a login. On eight screens the link follows
the open tab (`STAGING_TABS`); RoB Meetings and OKRs tabs have no stable
address on staging, so there it opens the screen.

## Side menu

The menu ends as staging does for a non-admin account: a group holding
Confluence, Watercooler and TopTaste, then the Learning hub. The group is
labelled "Team Fun" here; the product names it after the company.
