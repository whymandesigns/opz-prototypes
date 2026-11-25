#!/usr/bin/env python3
"""Builds the production-site reference screens.

    python3 production-site-2026-11-25/_src/build.py          # write every screen
    python3 ../designmd/lint.py production-site-2026-11-25/*/index.html
    python3 ../designmd/inline.py <screen>/index.html          # bake before sharing

Nothing about the shell is written here: each screen is designmd's
template/index.html with its title, side nav and content region replaced, the
same thing tools/new-prototype.py does. The content of each screen lives in
screens.py, as kit markup.

What this folder is: the product as it ran on 2026-11-25, rebuilt on the kit as
a reference to start updates and new versions from. Layout, labels and
structure follow the app; the people and the records are made up. The app's
own tenant says "Business as Usual"; these screens say "Processes", as every
Operationalize prototype does (BAU-TERM-001).
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
sys.path.insert(0, str(HERE))
import screens  # noqa: E402


def find_designmd():
    for up in (OUT.parent.parent, OUT.parent):
        cand = up / 'designmd' / 'template' / 'index.html'
        if cand.exists():
            return cand.parent.parent
    sys.exit('designmd not found beside this checkout')


TEMPLATE = (find_designmd() / 'template' / 'index.html').read_text()
ELEMENTS = '<style>\n' + (HERE / 'elements.css').read_text() + '</style>\n'


def finish(html):
    """What every screen gets after its content is written: the anchor nav in
    place of ghost buttons, the kit's editor in place of a bare textarea, and
    the hooks the search box filters on."""
    def nav(m):
        links = re.sub(r'<a class="btn btn-ghost" href="([^"]+)" style="[^"]*">', r'<a class="ps-anchor body-sm" href="\1">', m.group(1)).replace('class="btn-icon"', 'class="icon icon-16"')
        links = links.replace('class="ps-anchor body-sm"', 'class="ps-anchor body-sm is-active"', 1)
        return f'<nav class="ps-anchors" data-view="desktop" aria-label="Sections">{links}</nav>'
    html = re.sub(r'<nav class="stack" data-view="desktop" aria-label="Sections" style="[^"]*">(.*?)</nav>', nav, html, flags=re.S)
    html = re.sub(r'<textarea class="input" rows="\d+"(?: placeholder="([^"]*)")?></textarea>', lambda m: screens.editor(m.group(1) or ''), html)
    html = html.replace('<tr><td>', '<tr data-search-item><td>')
    html = html.replace('<article class="card"><div class="stack" style="gap: var(--spacing-3)">', '<article class="card" data-search-item><div class="stack" style="gap: var(--spacing-3)">')
    html = re.sub(r'(<div class="input-icon input-icon-left toolbar-search">\s*<svg[^>]*>.*?</svg>\s*<input class="input")', r'\1 data-search', html, flags=re.S)
    return html



NAV = [  # label, icon, screen folder
    ('Dashboard', 'i-dashboard', 'dashboard'),
    ('Processes', 'i-cpu-2', 'processes'),
    ('Initiatives', 'i-initiatives', 'initiatives'),
    ('RoB Meetings', 'i-calendar', 'rob-meetings'),
    ('OKRs', 'i-okr', 'okrs'),
    ('People', 'i-participants', 'people'),
    ('Team', 'i-org-unit', 'team'),
]


def sidenav(active, depth):
    up = '../' * depth
    items = []
    for label, icon, folder in NAV:
        cls = 'sidenav-item is-active' if label == active else 'sidenav-item'
        items.append(
            f'        <li><a class="{cls}" href="{up}{folder}/index.html"><svg class="sidenav-item-icon"><use href="#{icon}"/></svg>'
            f'<span class="sidenav-item-label">{label}</span></a></li>')
    return '<ul class="sidenav-list">\n' + '\n'.join(items) + '\n      </ul>'


# A list is a table on a wide screen and a stack of cards on a phone, as in the
# app. The kit has no component that turns one into the other, so both are in
# the page and this shows one, at the edge where the top bar collapses.
VIEW_SCRIPT = '''  <script>
  (() => {
    const phone = matchMedia('(max-width: 1024px)');
    const sync = () => document.querySelectorAll('[data-view]').forEach(el => {
      const on = (el.dataset.view === 'mobile') === phone.matches;
      el.hidden = !on; el.style.display = on ? '' : 'none';
    });
    phone.addEventListener('change', sync); sync();

    // Tabs switch panels, and a control with data-toggle shows or hides a panel.
    const show = (el, on) => { el.hidden = !on; el.style.display = on ? '' : 'none'; };
    const items = strip => [...strip.querySelectorAll('.tab, .segmented-item')];
    const pick = (group, i) => {
      document.querySelectorAll('[data-panel^="' + group + ':"]').forEach(p => show(p, p.dataset.panel === group + ':' + i));
      document.querySelectorAll('[data-tabs="' + group + '"]').forEach(strip => items(strip).forEach((t, n) => {
        const on = n === Number(i);
        t.classList.toggle('is-active', on); if (t.matches('.tab')) t.setAttribute('aria-selected', String(on));
      }));
    };
    document.addEventListener('click', e => {
      const tab = e.target.closest('[data-tabs] .tab, [data-tabs] .segmented-item');
      if (tab) { const strip = tab.closest('[data-tabs]'); pick(strip.dataset.tabs, items(strip).indexOf(tab)); }
      const tog = e.target.closest('[data-toggle]');
      if (tog) { const p = document.getElementById(tog.dataset.toggle); show(p, p.hidden); }
    });
    // #tab-2 opens the third tab; #open-<id> opens that drawer, modal, menu or panel.
    // Several can be joined with &.
    const route = () => {
      const strip = document.querySelector('.tabs[data-tabs]');
      location.hash.slice(1).split('&').forEach(h => {
        if (h.startsWith('tab-') && strip) pick(strip.dataset.tabs, h.slice(4));
        if (h.startsWith('open-')) { const el = document.getElementById(h.slice(5)); if (el) show(el, true); }
        const m = /^show-(.+)-(\d+)$/.exec(h);   // #show-view-1: the second item of the "view" switch
        if (m) pick(m[1], m[2]);
      });
    };
    addEventListener('hashchange', route); route();

    // Work lists: a caret folds a row's children; Expand all does every row.
    const fold = (btn, on) => {
      btn.setAttribute('aria-expanded', String(on));
      document.querySelectorAll('[data-child-of="' + btn.dataset.rows + '"]').forEach(r => show(r, on));
    };
    document.addEventListener('click', e => {
      const caret = e.target.closest('[data-rows]');
      if (caret) fold(caret, caret.getAttribute('aria-expanded') !== 'true');
      const all = e.target.closest('[data-expand-all]');
      if (all) {
        const on = all.textContent.trim() === 'Expand all';
        all.textContent = on ? 'Collapse all' : 'Expand all';
        document.querySelectorAll('[data-rows]').forEach(b => fold(b, on));
      }
      const anchor = e.target.closest('.ps-anchor');
      if (anchor) anchor.parentElement.querySelectorAll('.ps-anchor').forEach(a => a.classList.toggle('is-active', a === anchor));
    });
    // The search box filters the rows and cards on the page as you type.
    document.addEventListener('input', e => {
      if (!e.target.matches('[data-search]')) return;
      const q = e.target.value.trim().toLowerCase();
      document.querySelectorAll('[data-search-item]').forEach(el => show(el, !q || el.textContent.toLowerCase().includes(q)));
    });
  })();
  </script>
'''


def page(title, active, main, ctas=(), overlays='', depth=1, padded=True):
    t = TEMPLATE.replace('{{FEATURE_TITLE}}', title)
    if depth == 1:
        t = t.replace('../../designmd/', '../../../designmd/')
    # top bar: the collapsed-bar CTAs mirror this page's head, action for action
    cta = ''.join(
        f'    <button class="btn {variant} btn-icon-only topbar-cta" type="button" aria-label="{label}">'
        f'<svg class="btn-icon"><use href="#{icon}"/></svg></button>\n' for variant, label, icon in ctas)
    t, n = re.subn(r'(    <button class="btn btn-(?:secondary|primary) btn-icon-only topbar-cta".*\n)+', lambda m: cta, t, count=1)
    assert n == 1
    acct = '<div class="topbar-account"><a class="avatar avatar-md" href="#" aria-label="Open profile">MV</a></div>'
    assert t.count(acct) == 1
    t = t.replace(acct, '<div class="topbar-account"><div class="dropdown"><button class="avatar avatar-md dropdown-trigger" type="button" aria-expanded="false" aria-label="Open account menu">CK</button>'
                  '<div class="dropdown-menu dropdown-menu-end" id="user-menu" hidden>'
                  f'<a class="dropdown-item" href="{"../" * depth}profile/index.html">My profile</a><a class="dropdown-item" href="#">Career map</a>'
                  f'<a class="dropdown-item" href="{"../" * depth}recognitions/index.html">Recognitions</a><div class="dropdown-divider"></div>'
                  f'<a class="dropdown-item" href="{"../" * depth}sign-in/index.html">Sign out</a></div></div></div>')
    t, n = re.subn(r'<ul class="sidenav-list">.*?</ul>', lambda m: sidenav(active, depth), t, count=1, flags=re.S)
    assert n == 1
    pad = ' style="padding: var(--spacing-10)"' if padded else ' style="padding: 0"'
    t, n = re.subn(r'<main class="app-shell-main"[^>]*>.*?</main>',
                   lambda m: f'<main class="app-shell-main"{pad}>\n{main}\n    </main>', t, count=1, flags=re.S)
    assert n == 1
    if overlays:
        i = t.index('\n  <script>')
        t = t[:i] + '\n' + overlays + t[i:]
    brand = re.search(r'<a class="topbar-brand" href="#">.*?</a>', t, flags=re.S)
    t = t[:brand.end()] + '''
    <div class="dropdown" data-view="desktop"><button class="ps-bizline body-sm-semibold dropdown-trigger" type="button" aria-expanded="false">All Business Lines<svg class="icon icon-16" aria-hidden="true"><use href="#i-chevron-down"/></svg></button>
      <div class="dropdown-menu dropdown-menu-start" id="bizline-menu" hidden><button class="dropdown-item is-selected" type="button">All Business Lines</button><button class="dropdown-item" type="button">Services</button><button class="dropdown-item" type="button">Operationalize</button></div></div>''' + t[brand.end():]
    t = finish(t).replace('</head>', ELEMENTS + '</head>')
    return t.replace('</body>', VIEW_SCRIPT + '</body>')


def plain(title, body):
    """The list of screens is ours, not the product's: no top bar and no side nav."""
    sprite = re.search(r"  if \(!document\.getElementById\('i-plus'\)\) \{.*?\n  \}\n", TEMPLATE, flags=re.S).group(0)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <link rel="stylesheet" href="../../designmd/tokens.css" />
  <link rel="stylesheet" href="../../designmd/semantic.css" />
  <link rel="stylesheet" href="../../designmd/components.css" />
{ELEMENTS}</head>
<body>
  <main style="max-width: 1200px; margin: 0 auto; padding: var(--spacing-10) var(--spacing-6)">
{body}
  </main>
  <script>
{sprite}  </script>
</body>
</html>
'''


def main():
    built = []
    for s in screens.SCREENS:
        if s.get('plain'):
            html = plain(s['title'], s['main']).replace('../../designmd/', '../../../designmd/')
        else:
            html = page(s['title'], s['nav'], s['main'], s.get('ctas', ()), s.get('overlays', ''), padded=s.get('padded', True))
        d = OUT / s['folder']
        d.mkdir(exist_ok=True)
        (d / 'index.html').write_text(html)
        built.append(s['folder'])
    (OUT / 'index.html').write_text(plain('Production site · Nov 25, 2026', screens.index()))
    (OUT / 'elements').mkdir(exist_ok=True)
    (OUT / 'elements' / 'index.html').write_text(plain('New elements · Production site', screens.elements_page()).replace('../../designmd/', '../../../designmd/'))
    print('wrote', len(built), 'screens:', ', '.join(built))


if __name__ == '__main__':
    main()
