---
name: designmd
description: Build or change an HTML prototype in this repo using the designmd design system. Use when creating a screen, page or feature under features/, adding or editing UI markup, reaching for a component (button, table, modal, drawer, top bar, side nav, sheet, field, badge, tag, toast, tooltip), styling anything with tokens, or when asked to inline, lint or ship a prototype.
---

# designmd

A plain HTML/CSS system. Three stylesheets, no build step, no React. Prototypes are
single self-contained files.

designmd is a **sibling checkout** of this one, and every path below is written from the
folder holding them both — `icarus/`, with `designmd/` and `features/` inside it. From
inside `features/`, reach the system as `../designmd/`.

## Before writing markup

Read `designmd/dist/kit.json`. It is the generated inventory — 368 classes grouped by
component, the attribute-driven components, and the classes you must not use. Find the
class there; do not guess one, and do not copy markup out of `designmd/example.html`
(see Traps).

For a new screen, start from the skeleton rather than assembling one:

```bash
cp -r designmd/starter features/my-feature
```

It already has the top bar, page head, table, modal and search wired correctly, and it
lints clean.

## The rules

1. Every class must be in `kit.json`. A class nothing defines renders as nothing. If the
   kit lacks a component, say so rather than approximating it.
2. Semantic tokens only — `var(--color-bg)`, `var(--type-h1)`, `var(--spacing-4)`. Never
   `var(--color-blue-500)`. The one exception is `--color-graphite-800`, the top bar
   chrome, which does not change with the theme.
3. One `.btn-primary` per page; every other CTA is `.btn-secondary`.
4. No component CSS in a prototype. Add the variant to `designmd/components.css` and
   re-inline, so the next screen inherits it.
5. Status colours signal state, never decoration. Type carries the hierarchy — try a
   different size or weight before adding a border, divider or fill.

## Check and ship

```bash
python3 designmd/lint.py features/my-feature/index.html
python3 designmd/inline.py features/my-feature/index.html
```

The linter catches invented classes, showcase classes, dead icon slugs, retired Phosphor,
raw hex and primitives used past the semantic layer. Run it before saying a prototype is
done. `inline.py` bakes the CSS, the icon sprite and the fonts into one file; it refuses
a prototype still using retired tokens.

## Traps

These fail silently, and each has cost someone a debugging session:

- **`example.html` is not a source of markup.** 88 of its classes are the showcase's own
  chrome, styled in its `<style>` block alone and identical-looking in markup.
  `.btn-cta-icon` is one and is already shipped in a prototype. Browse the file to see
  what a component looks like; take the class name from `kit.json`.
- **Icons are blank until `inline.py` runs.** The stylesheets do not carry the sprite.
  The starter fetches it at dev time; a hand-built page will not.
- **Don't copy the `example.html` script block whole.** 2,286 lines, and its tail renders
  the showcase's palette swatches against elements no prototype has — it throws, and
  every handler after it never attaches. Take only the handlers you need.
- **`.topbar-title`, `.topbar-menu` and `.topbar-cta` are the collapsed layout.** The top
  bar is a container query; they appear below 768px and show nothing on a wide screen.
  Include all three from the start.
- **Some classes carry no CSS and are still right.** `.dropdown-trigger` is how the
  delegated script finds a dropdown's button. `kit.json` lists these under
  `behaviourHooks`, and the attribute-driven components under `attributes` — a tooltip
  is `[data-tooltip]`, never `.tooltip`.
- **Phosphor is retired.** `<i class="ph …">` renders nothing. Some CSS comments still
  show it; they are stale.

## When the system itself changes

Editing a stylesheet means regenerating the packages, or `dist/` goes stale and the
linter checks against an old inventory:

```bash
python3 designmd/tools/build-packages.py          # after any stylesheet change
python3 designmd/tools/build-packages.py --check  # fails if dist/ is behind
```

`designmd/design.md` is the full written system (~15k tokens) — read the section you
need, not the file. Upstream is **Picasso**, Toptal's production React system; where
designmd and Picasso disagree, Picasso is right and designmd has a bug.
