# Slack profile card

Design canvas for the Operationalize profile link preview in Slack. It holds
the card in several layouts: the original (Normal, Hover, Mobile, Manager
icon), photo right, photo left, a split row, and two new layout ideas
(Idea A full-bleed photo, Idea B fact columns).

It is also one shared Claude artifact, recorded in `artifact.json`. The folder
is the source of truth: use the artifact-sync skill to publish or save it.

## Files

- `project/canvas.json`: board titles, positions and order.
- `project/*.dc.html`: one file per board.
- `project/ds/opz/tokens.json`: Operationalize design-system tokens.
- `assets/`: the images the boards use.
- Everything else (`index.html`, `SKILL.md`, `artifact-type/`) is the canvas
  viewer and its reference pages, as in `test/`.

## Images

The boards reference images as `/_blob/<id>`, the same addresses the Claude
artifact uses. On the deployed site those resolve to the repo-root `_blob/`
folder (file names are the ids, no extension; `vercel.json` sets their content
types), so the images show in the artifact and on the site without editing the
boards. Serve the repo root (not this folder) when running locally.

| `/_blob/` id | What it is |
| --- | --- |
| `f9e20eef...` | Lucas Ferreira photo |
| `7d24c9cd...` | Elena Petrova avatar |
| `881ab08b...` | Dana Whitfield avatar |
| `c5ac8b8e...` | Operationalize banner (SVG) |

`assets/` keeps the same files with their extensions.
