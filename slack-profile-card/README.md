# Slack profile card

Design canvas for the Operationalize profile link preview in Slack. It holds
the card in several layouts: the original, photo right, photo left, a split
row, and two new layout ideas (full-bleed photo, fact columns).

The canvas lives as a Design artifact on claude.ai
(https://claude.ai/artifact/KGej9EpiVX6ZBLJ7SqWPdt). This folder is a snapshot of it.

## Files

- `project/canvas.json`: board titles, positions and order on the canvas.
- `project/*.dc.html`: one file per board.
  - `Main`: Normal (original)
  - `Hover`, `Mobile`, `ManagerIcon`: the other original boards
  - `PhotoRight`, `PhotoLeft`, `PhotoLeftSplit`: photo-position variants
  - `LayoutPanel` (Idea A) and `LayoutFacts` (Idea B): new layout ideas
- `project/ds/opz/tokens.json`: Operationalize design system tokens.
- `assets/`: the images the boards use.

## Image references

The boards point at images as `/_blob/<id>`, which only resolve inside the
artifact. The same files are in `assets/`:

| `/_blob/` id | File | What it is |
| --- | --- | --- |
| `f9e20eef...` | `f9e20eef9ce671843f4a8f97b41ac057.jpg` | Lucas Ferreira photo |
| `7d24c9cd...` | `7d24c9cdfb9236d07822df8e741bf872.jpg` | Elena Petrova avatar |
| `881ab08b...` | `881ab08be326006871e03a7fd753d88d.jpg` | Dana Whitfield avatar |
| `c5ac8b8e...` | `c5ac8b8ef7e305346b96c853322b9172.svg` | Operationalize banner |

Outside the artifact, point each `src` at the matching file in `assets/`.
