#!/usr/bin/env python3
"""Move an element from this reference into the Icarus library.

    python3 production-site-2026-11-25/_src/promote.py ps-bars [ps-health ...]
    python3 production-site-2026-11-25/_src/promote.py --dry-run ps-bars
    python3 production-site-2026-11-25/_src/promote.py i-external-link   (an icon)
    python3 production-site-2026-11-25/_src/promote.py --list

The element's rules leave _src/elements.css and are appended to designmd's
components.css; the kit packages are regenerated so dist/kit.json lists the
classes, and the reference is rebuilt. From then on the linter treats the
element as a kit class and the next screen takes it from the library instead
of building it again. The element stays on the elements page with an "Added
to library" badge and its date (kept in promoted.json), so developers can
filter the page to the library elements they still have to implement.

It edits the designmd checkout next to this one and commits nothing: review
the diff there and commit it as any other library change.
"""
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSS = HERE / 'elements.css'


def designmd():
    for up in (HERE.parents[2], HERE.parents[1]):
        if (up / 'designmd' / 'components.css').exists():
            return up / 'designmd'
    sys.exit('designmd not found beside this checkout')


def blocks():
    """elements.css is one block per element, blank line between them."""
    return [b for b in CSS.read_text().split('\n\n') if b.strip()]


def owns(block, cls):
    return re.search(r'\.' + re.escape(cls) + r'(?![a-z])', re.sub(r'/\*.*?\*/', '', block, flags=re.S)) is not None


def main(argv):
    dry = '--dry-run' in argv
    names = [a for a in argv if not a.startswith('--')]
    bl = blocks()
    if '--list' in argv or not names:
        for m in re.finditer(r'<symbol id="([^"]+)"', (HERE / 'icons.svg').read_text()):
            print(m.group(1), '- icon')
        for b in bl[1:]:
            first = re.search(r'\.(ps-[a-z-]+)', re.sub(r'/\*.*?\*/', '', b, flags=re.S))
            print(first.group(1) if first else '?', '-', b.strip().splitlines()[0][:80])
        return
    icons = [n for n in names if n.startswith('i-')]
    if icons:
        if len(icons) != len(names):
            sys.exit('move icons (i-…) and elements (ps-…) in separate runs')
        return promote_icons(icons, dry)
    moved, keep = [], []
    for b in bl:
        (moved if any(owns(b, n) for n in names) and not b.startswith('/* ===') else keep).append(b)
    missing = [n for n in names if not any(owns(b, n) for b in moved)]
    if missing:
        sys.exit('not in elements.css (already in the library?): ' + ', '.join(missing))
    lib = designmd() / 'components.css'
    add = '\n\n/* --- From the production site reference: ' + ', '.join(names) + ' --- */\n' + '\n\n'.join(b.strip() for b in moved) + '\n'
    if dry:
        print(f'would move {len(moved)} block(s), {len(add.splitlines())} lines, into {lib}:\n{add}')
        return
    lib.write_text(lib.read_text().rstrip('\n') + add)
    CSS.write_text('\n\n'.join(b.strip('\n') for b in keep) + '\n')
    log = HERE / 'promoted.json'   # the elements page reads this for its badge and filter
    done = json.loads(log.read_text()) if log.exists() else {}
    done.update({n: date.today().strftime('%b %-d, %Y') for n in names})
    log.write_text(json.dumps(done, indent=2) + '\n')
    subprocess.run([sys.executable, str(designmd() / 'tools' / 'build-packages.py')], check=True)
    subprocess.run([sys.executable, str(HERE / 'build.py')], check=True)
    print('moved into the library: ' + ', '.join(names) + '\nNext: lint and inline the reference, then commit designmd and this repo.')


def promote_icons(names, dry):
    """Icons: the <symbol> leaves _src/icons.svg and joins the kit's sprite."""
    src = HERE / 'icons.svg'
    text = src.read_text()
    syms = {m.group(1): m.group(0) for m in re.finditer(r'  <symbol id="([^"]+)".*?</symbol>\n', text, flags=re.S)}
    missing = [n for n in names if n not in syms]
    if missing:
        sys.exit('not in _src/icons.svg (already in the library?): ' + ', '.join(missing))
    lib = designmd() / 'icons.svg'
    kit = lib.read_text()
    clash = [n for n in names if f'id="{n}"' in kit]
    if clash:
        sys.exit('the kit already has: ' + ', '.join(clash))
    add = ''.join(syms[n] for n in names)
    if dry:
        print(f'would move {len(names)} symbol(s) into {lib}:\n{add}')
        return
    i = kit.rindex('</svg>')
    lib.write_text(kit[:i] + add + kit[i:])
    for n in names:
        text = text.replace(syms[n], '')
    src.write_text(text)
    log = HERE / 'promoted.json'
    done = json.loads(log.read_text()) if log.exists() else {}
    done.update({n: date.today().strftime('%b %-d, %Y') for n in names})
    log.write_text(json.dumps(done, indent=2) + '\n')
    subprocess.run([sys.executable, str(designmd() / 'tools' / 'build-packages.py')], check=True)
    subprocess.run([sys.executable, str(HERE / 'build.py')], check=True)
    print('moved into the kit sprite: ' + ', '.join(names) + '\nNext: lint and inline the reference, then commit designmd and this repo.')


if __name__ == '__main__':
    main(sys.argv[1:])
