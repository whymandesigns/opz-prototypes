---
name: artifact-sync
description: Sync a Claude artifact with its folder in this repo via GitHub. "publish <folder>" = git pull, then publish the folder to its shared Claude artifact. "save <folder>" = read the artifact back into the folder, commit and push. Use for "publish the artifact", "save my artifact changes", "pull and open as artifact".
---

Each artifact lives in a repo folder (e.g. `test/`). The folder is the source of truth; the Claude artifact is its published, editable view. Everyone works on ONE shared artifact per folder, recorded in `<folder>/artifact.json` (committed):

```json
{
  "url": "https://claude.ai/artifact/<id>",
  "capabilities": { "artifact": {}, "db": {}, "...": {} },
  "contract": "0.2.47"
}
```

- `url`: the shared artifact. `null` until the first publish.
- `capabilities` / `contract`: what the artifact is published with. Without them a page that edits itself (a Design canvas, a checklist) opens **read-only for everyone**, edit access or not. A Design canvas folder (it has `artifact-type/`) uses the Design type's set: `downloads`, `artifact`, `comments` (`composer_only`, `customAnchors`), `room`, `db` (rules `[{"path":"","write":"admin"}]`), `assets`, `user` (scopes `["profile"]`), `sample`, at contract `0.2.47`.

Edit access is granted per Claude account in the artifact's **Share** menu, never by GitHub. Repo access alone lets nobody edit.

Old per-person links in `<folder>/.artifact-url` (gitignored) are only a fallback when `artifact.json` has no `url`.

## publish <folder>
1. `git pull`.
2. Load the `artifact-design` skill is NOT needed: the folder is already a finished page.
3. Read `<folder>/artifact.json`. No file: create it with `url: null` and the capabilities above (Design canvas) or `{}`.
4. Call the Artifact tool: `file_path` = `<folder>/index.html`, `root` = `<folder>`, `files` = every other file in the folder at its relative path (exclude `artifact.json`, `.artifact-url`, `.DS_Store`, and `_files.json`: a local-only manifest for serving the folder over HTTP; names starting `_` are reserved by the artifact service).
   - **First publish** (`url` is null): also pass `capabilities` and `contract` from `artifact.json`, and an `icon`. Write the returned URL into `artifact.json`, commit it (`git add <folder>/artifact.json`, commit, `git pull --rebase`, `git push` — ask before pushing), and tell the user: open the link → **Share** → give the team / organization **Can edit**. Until that is done only the publisher can edit.
   - **Later publishes**: pass `url` (read it first with action "read" if this session hasn't). Omit `capabilities` and `contract` so the stored ones carry forward, unless `artifact.json` changed them.
   - Refused because someone edited the artifact since: run **save** first, then publish again.
   - Refused as not a writer: the user lacks edit access; the artifact's owner must grant it in **Share**.
5. Reply with the artifact link only (plus the Share reminder on a first publish).

## save <folder>
1. Read the artifact (`action: "read"`, `url` from `artifact.json`), then read every published path with `paths` and `out_dir` = `<folder>`.
2. `git add <folder>`, commit, `git pull --rebase`, `git push`.
3. Reply with one line.
