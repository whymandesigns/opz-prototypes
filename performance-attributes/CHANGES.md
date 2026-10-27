# Performance attributes (TOP-7764) · on Icarus

A rebuild of the "Performance attributes" sandbox artifact
(<https://claude.ai/artifact/7AKTZ9sAm75GVhzzrv8VXE>) using only the Icarus library. The original
renders 18 screens from a compiled bundle of the real app components (namespace `Opz`). This copy
uses Icarus classes, tokens and icons. Where Icarus has no component, the part is built from Icarus
tokens in the prototype's own style block and listed under "Library gaps" below.

| File | What it is |
|---|---|
| `index.html` | The clickable prototype. `?state=<key>` opens a state. `?states=1` adds the state switcher. |
| `canvas.html` | All 18 states as live screens, laid out like the original canvas. Screen 02 stays clickable. `?states=1&state=<key>` zooms to a screen. |

Rebuild after a library change with `python3 ../icarus/inline.py performance-attributes/index.html`
(and the same for `canvas.html`).

## What the feature adds to the OKRs page

These items come from the original's canvas titles and the bundle's source comments. The original
has no written brief: its Handoff tab is generated from the code.

- **Eight performance attributes.** Brand, Growth, Dynamic/Process, Growth/Revenue, People,
  Organization, Speed and Quality. Each has one icon and a draft description.
- **"Performance attributes" button** in the page head, next to Export as CSV. It opens the list of
  attributes with how many objectives and key results support each one in the selected year.
- **One attribute.** A row in the list opens the attribute: everything that supports it that year,
  grouped by OKR level. A row there opens that OKR on its level, period and org unit, searched by
  name and highlighted, like global search. With nothing linked it says so for that year.
- **One attribute per key result.** The icon leads the key result's connection pill, before a
  divider, so the counters stay aligned. Hover shows "Performance attribute: <name>". Clicking the
  icon opens that attribute.
- **One attribute per objective.** The same icon in its own pill, next to Draft / Signed Off.
- **Key result menu.** It has one item: "Add performance attribute" when none is set, or "Change
  performance attribute" when one is. Removing happens in the dialog.
- **Objective menu.** The same item, between Sign Off and Clone.
- **Add / Change dialog.** Eight options in two columns, each with a radio, a tile, the name and the
  description. The current attribute is marked "Current". The Change dialog has "Remove attribute"
  on the left, where Delete sits in edit footers. Saving shows a toast: added, changed or removed.
- **Attribute filter** in the toolbar, after the org unit filter: "All attributes" plus the eight,
  each with its icon. A filtered list keeps an OKR when its objective or any key result supports
  the attribute.
- **Read-only levels.** Company Vision and Company Objective show the icons and open the attribute,
  with no menus.
- **Icon board (screen 18).** The eight glyphs for approval, each with its pill, tile, icon name and
  description.

## The 18 states

| # | Key | State |
|---|---|---|
| 01 | `main` | OKRs page, what's new |
| 02 | `prototype` | Clickable prototype |
| 03 | `catalog` | Performance attributes list, Speed row hovered |
| 04 | `detail` | One attribute: Speed |
| 05 | `detail-empty` | One attribute: Quality, nothing in 2027 |
| 06 | `kr-menu-add` | Key result menu with "Add performance attribute" |
| 07 | `picker-add` | Add performance attribute, People picked |
| 08 | `toast` | Added: icon in the pill, toast shown |
| 09 | `kr-menu-pa` | Key result menu with "Change performance attribute" |
| 10 | `picker-change` | Change performance attribute, Growth picked, People current |
| 11 | `card-menu` | Objective menu |
| 12 | `picker-objective` | Change performance attribute for the objective |
| 13 | `obj-tip` | Objective icon with its tooltip |
| 14 | `pa-tip` | Key result icon with its tooltip |
| 15 | `filter-menu` | Attribute filter open |
| 16 | `filtered` | Filtered by Speed |
| 17 | `read-only` | Company Objective, read-only |
| 18 | `icons` | The eight icons |

## Designer edits from the sandbox (`design/state`, version 437)

Carried over:

- Every green (positive) button became secondary. Only "Create OKR" on screen 01 stays the primary
  CTA, as in the sandbox.
- The NEW markers on screen 01 are hidden.
- A highlighted card's head is tighter (8px top and bottom) and fully rounded.

Not carried over, because they are free drags or test values rather than design decisions:

- Card 1 on every screen: the org unit chip dragged 110px left and the objective's attribute pill
  dragged 582px right, onto the "+" button.
- Screen 01: the Function Yearly tab moved first, the status tag dragged next to the org unit, the
  first key result's pill and owner offset, all cards highlighted.
- Screen 02: 48px padding on one key result row.
- Screen 04: "xxx" appended to an objective.
- Screen 05: the title changed to "Quality Hello Testing" and a stray "Button" added.
- Screen 09: the top bar dragged 88px left.

## Library gaps

Icarus had no component for these. Each is built in the prototype's own style block from semantic
tokens, with a `pa-` class. `lint.py` reports them as local classes.

- **OKR card and key result row** (`pa-okr*`, `pa-kr*`): objective head with level stripe, rows,
  drag handle, title truncation.
- **Connection counter pill** (`pa-cnt*`, `pa-sep`): three counters plus the attribute slot.
- **Owner chip** (`pa-owner*`): avatar and name on a muted fill, with a pending variant.
- **Labelled compact select** (`pa-unit*`): the org unit field on the card, with a caption label.
- **Progress value** (`pa-pct`): coloured percentage as a button.
- **Icon tile** (`pa-tile`): a 32px square holding a 16px glyph.
- **Radio card** (`pa-opt*`): an option tile around the kit's `.radio`.
- **List rows** (`pa-row*`, `pa-item*`, `pa-group-h`): attribute row with tile, count and chevron;
  linked result row with meta line; uppercase group heading.
- **Danger text button** (`pa-remove`): "Remove attribute". Icarus has a filled `.btn-danger` only.
- **Tooltip held open** (`pa-tip-on`): `[data-tooltip]` opens only on hover or focus, so a designed
  "tooltip open" state needs a modifier.
- **Empty state** (`pa-empty`) and **pagination** (`pa-pager`).
- **Top bar parts**: business-line switcher (`pa-bl`) and the account's notification dot (`pa-dot`).
- **Shared key results list** (`pa-shared*`, `pa-person`).
- **Icons**: no plain dollar glyph. Growth/Revenue uses `billing-2`, a dollar on a document. No
  small "performance" bars glyph either, so Growth uses `bar-chart`.
- **Menus**: `.dropdown-item` wraps long labels, so the card menus set a wider minimum and
  `nowrap`.
- **App shell**: `.app-shell` is sized for the showcase frame. It is overridden to fill the
  viewport, as the other prototypes do.

## Visual differences from the original

These remain because the prototype uses the Icarus component as it is:

- **Brand.** The Icarus logo (Operationalize) replaces the TopTeam tenant logo.
- **Top bar.** The padding is 24px instead of 32px, and the search is narrower.
- **Sidebar.** Items are 36px tall with an 8px icon gap, instead of 38px and 12px. The collapse
  toggle is always visible on the edge.
- **Status pill.** The neutral `.badge` has a near-white gray-100 border and regular 12px muted
  text. The original has a gray-400 border and semibold text.
- **Selects.** These are `.input-select` with a chevron and 13px text. The original has 14px text
  with an up/down caret.
- **Sort direction.** The button is round (`.btn-icon-only`), not square and attached.
- **Kebab and "+" buttons.** These are 24px round ghost buttons, not 16px bare icons.
- **Menus.** The kit dropdown has 8px padding, an 8px radius and a 12px icon gap.
- **Tooltips.** These are the kit's dark caption pills: graphite-900 with 12px text, not
  graphite-800 with 13px.
- **Avatars.** These have the kit's chamfered corner instead of a 4px radius.
- **Modals.** Titles are 16px, not 20px, and padding is 24px, not 32–40px. The kit's backdrop is
  graphite at 50%.
- **Toast.** The kit's success toast is lighter and smaller: a bordered green-100 card with a 16px
  icon. It sits under the top bar.
- **Colours.** Progress at 75% and above uses `--color-success` (green-500), not green-600.
  Secondary text uses `--color-text-muted` (gray-700), not graphite-700. Body text uses
  `--color-text` (graphite-900), not black.

## Interactions

These work as in the original:

- the Performance attributes button, list, detail and back
- opening an OKR from the detail
- the key result and objective attribute icons
- both menus
- the add, change and remove dialogs with their toasts
- the attribute and org unit filters
- level tabs, quarters, year, sort and direction
- search, pagination, Sign Off, the org unit change and Export as CSV

These existing app controls are drawn but do nothing, because they are not part of this feature:

- add key result and inline renaming
- the progress slider and the connection drawers
- add, remove and cancel owner
- Clone, Remove and drag to reorder
- Accept and Reject on shared key results
