---
name: artifact-sync
description: Sync a Claude artifact with its folder in this repo via GitHub. "publish <folder>" = git pull, then publish the folder as a Claude artifact. "save <folder>" = read the artifact back into the folder, commit and push. Use for "publish the artifact", "save my artifact changes", "pull and open as artifact".
---

Each artifact lives in a repo folder (e.g. `test/`). The folder is the source of truth; the Claude artifact is its published view. The artifact URL is stored in `<folder>/.artifact-url` (one line, per person, gitignored).

## publish <folder>
1. `git pull`.
2. Load the `artifact-design` skill is NOT needed: the folder is already a finished page.
3. Call the Artifact tool: `file_path` = `<folder>/index.html`, `root` = `<folder>`, `files` = every other file in the folder at its relative path (exclude `.artifact-url`). If `.artifact-url` exists pass it as `url` (read it first with action "read"); otherwise publish new and write the returned URL to `.artifact-url`.
4. Reply with the artifact link only.

## save <folder>
1. Read the artifact (`action: "read"`, URL from `.artifact-url`), then read every published path with `paths` and `out_dir` = `<folder>`.
2. `git add <folder>`, commit, `git pull --rebase`, `git push`.
3. Reply with one line.
