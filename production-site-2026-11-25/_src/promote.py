#!/usr/bin/env python3
"""Move an element from this reference into the Icarus library.

    python3 production-site-2026-11-25/_src/promote.py ps-bars [ps-health ...]
    python3 production-site-2026-11-25/_src/promote.py --dry-run ps-bars
    python3 production-site-2026-11-25/_src/promote.py --list

The element's rules leave _src/elements.css and are appended to designmd's
components.css; the kit packages are regenerated so dist/kit.json lists the
classes, and the reference is rebuilt. From then on the linter treats the
element as a kit class, the elements page shows it as "In library", and the
next screen takes it from the library instead of building it again.

It edits the designmd checkout next to this one and commits nothing: review
the diff there and commit it as any other library change.
"""
import re
import subprocess
import sys
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
        for b in bl[1:]:
            first = re.search(r'\.(ps-[a-z-]+)', re.sub(r'/\*.*?\*/', '', b, flags=re.S))
            print(first.group(1) if first else '?', '-', b.strip().splitlines()[0][:80])
        return
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
    subprocess.run([sys.executable, str(designmd() / 'tools' / 'build-packages.py')], check=True)
    subprocess.run([sys.executable, str(HERE / 'build.py')], check=True)
    print('moved into the library: ' + ', '.join(names) + '\nNext: lint and inline the reference, then commit designmd and this repo.')


if __name__ == '__main__':
    main(sys.argv[1:])
