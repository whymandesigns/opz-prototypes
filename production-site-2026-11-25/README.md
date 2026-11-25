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
approximated: `_src/elements.css` holds twenty of them (`ps-*` classes, kit
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
