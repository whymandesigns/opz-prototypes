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

The boards reference images as `/_blob/<id>`, which only resolve inside the
artifact, so locally they show as broken images. The same files are in
`assets/`:

| `/_blob/` id | File | What it is |
| --- | --- | --- |
| `f9e20eef...` | `f9e20eef9ce671843f4a8f97b41ac057.jpg` | Lucas Ferreira photo |
| `7d24c9cd...` | `7d24c9cdfb9236d07822df8e741bf872.jpg` | Elena Petrova avatar |
| `881ab08b...` | `881ab08be326006871e03a7fd753d88d.jpg` | Dana Whitfield avatar |
| `c5ac8b8e...` | `c5ac8b8ef7e305346b96c853322b9172.svg` | Operationalize banner |
