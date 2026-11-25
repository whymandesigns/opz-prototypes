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
- **What is missing:** only each screen's basic state is built. Tabs other than
  the first, drawers, modals and the areas listed under "Still to build" on
  `index.html` come later.

Where the kit has no component, the nearest kit one stands in, and says so here
rather than in invented CSS:

| In the app | Here |
|---|---|
| Dashboard status bar chart | stat cards, one per status |
| RoB month calendar grid | a five-column table with the meetings as list rows |
| Profile location map | a card with the city |

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
