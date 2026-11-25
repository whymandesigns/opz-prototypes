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
    html = html.replace('<table class="table">', '<table class="table ps-striped">')   # the product stripes its lists
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
      // a control can also drop out of, or appear in, one choice of a switch
      document.querySelectorAll('[data-hide-in^="' + group + ':"]').forEach(el => show(el, el.dataset.hideIn !== group + ':' + i));
      document.querySelectorAll('[data-show-in^="' + group + ':"]').forEach(el => show(el, el.dataset.showIn === group + ':' + i));
      document.querySelectorAll('[data-tabs="' + group + '"]').forEach(strip => items(strip).forEach((t, n) => {
        const on = n === Number(i);
        t.classList.toggle('is-active', on); if (t.matches('.tab')) t.setAttribute('aria-selected', String(on));
      }));
    };
    document.addEventListener('click', e => {
      const tab = e.target.closest('[data-tabs] .tab, [data-tabs] .segmented-item');
      if (tab) { const strip = tab.closest('[data-tabs]'); pick(strip.dataset.tabs, items(strip).indexOf(tab)); }
      const acc = e.target.closest('.accordion-summary');
      if (acc) { const on = acc.parentElement.classList.toggle('is-open'); acc.setAttribute('aria-expanded', String(on)); }
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
    // A tree table stripes the rows that are open, not every second row in the markup.
    const stripe = () => document.querySelectorAll('.ps-wtree tbody, .ps-wtree-list').forEach(tb => {
      let i = 0;
      [...tb.children].forEach(r => { if (!r.hidden) r.classList.toggle('is-alt', i++ % 2 === 1); });
    });
    const fold = (btn, on) => {
      btn.setAttribute('aria-expanded', String(on));
      document.querySelectorAll('[data-child-of="' + btn.dataset.rows + '"]').forEach(r => {
        show(r, on);
        if (!on) r.querySelectorAll('[data-rows]').forEach(inner => fold(inner, false));   // closing a row closes what is under it
      });
      stripe();
    };
    stripe();
    // Prototype links: a button that finishes a flow, and a person's cell or card.
    document.addEventListener('click', e => {
      const go = e.target.closest('[data-go]');
      if (go) { location.href = go.dataset.go; return; }
      if (e.target.closest('a, button, input, label')) return;
      const who = e.target.closest('.table .cell-user, .org-node, .ps-tree-node');
      if (who) location.href = who.querySelector('.is-talent') ? '../talent-profile/index.html' : '../profile/index.html';
    });
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
      document.querySelectorAll('[data-search-item]').forEach(el => show(el, q ? el.textContent.toLowerCase().includes(q) : !el.dataset.childOf));
      if (!q) document.querySelectorAll('[data-rows]').forEach(c => c.setAttribute('aria-expanded', 'false'));
      stripe();
    });
  })();
  </script>
'''


def page(title, active, main, ctas=(), overlays='', depth=1, padded=True):
    t = TEMPLATE.replace('{{FEATURE_TITLE}}', title)
    # The menu's foot as the product has it for this account: a group that
    # opens (with the Watercooler in it) and the learning hub. No admin settings.
    fun_open = active == 'Watercooler'
    up = '../' * depth
    sub = lambda label, href, on=False: f'<li><a class="sidenav-item sidenav-subitem{" is-active" if on else ""}" href="{href}"><span class="sidenav-item-label">{label}</span></a></li>'
    foot = f'''<div class="sidenav-footer">
        <div class="sidenav-group">
          <button class="sidenav-item sidenav-group-trigger" type="button" aria-expanded="{str(fun_open).lower()}">
            <svg class="sidenav-item-icon"><use href="#i-group-3"/></svg>
            <span class="sidenav-item-label">Team Fun</span>
            <svg class="sidenav-item-chevron"><use href="#i-chevron-down"/></svg>
          </button>
          <ul class="sidenav-sublist">
            {sub("Confluence", "#")}
            {sub("Watercooler", up + "watercooler/index.html", fun_open)}
            {sub("TopTaste", "#")}
          </ul>
        </div>
        <div class="sidenav-group">
          <button class="sidenav-item sidenav-group-trigger" type="button" aria-expanded="false">
            <svg class="sidenav-item-icon"><use href="#i-lightbulb"/></svg>
            <span class="sidenav-item-label">Learning hub</span>
            <svg class="sidenav-item-chevron"><use href="#i-chevron-down"/></svg>
          </button>
          <ul class="sidenav-sublist">
            {sub("Demo: create a Process", "#")}
            {sub("Complete your profile", up + "profile-edit/index.html")}
            {sub("Onboarding", "#")}
          </ul>
        </div>
      </div>'''
    t, n = re.subn(r'<div class="sidenav-footer">.*?</div>\n    </aside>', lambda m: foot + '\n    </aside>', t, count=1, flags=re.S)
    assert n == 1
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
    pad = ' style="padding: var(--spacing-3) var(--spacing-8) var(--spacing-10)"' if padded else ' style="padding: 0"'
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
  <main style="max-width: 1440px; margin: 0 auto; padding: var(--spacing-10) var(--spacing-6)">
{body}
  </main>
  <script>
{sprite}  </script>
</body>
</html>
'''


def wire(html, folder):
    """Make the reference click through like the product: every name that is a
    person, a unit, a meeting or a piece of work goes to its screen, and the
    buttons that finish a flow land where the product would land."""
    people = {n for n, _ in screens.PEOPLE.values()}
    talents = {'Rosa Dahl', 'Imran Suleiman', 'Greta Lund', 'Samir Haddad', 'Lina Okoye', 'Paolo Ferri'}
    units = ({u[0] for u in screens.UNITS} | {k[0] for kids in screens.UNIT_KIDS.values() for k in kids} | set(screens.UNIT_OF.values())) - {''}
    work = set()

    def collect(node):
        work.add(node[0])
        for kid in node[6]:
            collect(kid)
    for tree in (screens.DASH_TREE, screens.INIT_TREE):
        for _, _, node in tree:
            collect(node)
    work |= {'Contract to workspace handoff', 'First-week survey', 'Self-serve account setup'}
    procs = set()
    for _, _, node in screens.PROC_TREE:
        procs.add(node[0])

    def target(text):
        if text in talents:
            return '../talent-profile/index.html'
        if text in people:
            return '../profile/index.html'
        if text in units:
            return '../team-profile/index.html'
        if text.startswith('['):
            return '../rob-meeting-view/index.html'
        if text in work:
            return '../initiative-view/index.html'
        if text in procs:
            return '../processes/index.html#open-process-drawer'
        return None

    def link(m):
        text = re.sub(r'<[^>]+>', '', m.group(3)).strip()
        to = target(text)
        return m.group(0) if not to else f'<a{m.group(1)}href="{to}"{m.group(2)}>{m.group(3)}</a>'
    html = re.sub(r'<a\b([^>]*?)href="#"([^>]*)>(.*?)</a>', link, html, flags=re.S)
    html = html.replace('<a class="topbar-brand" href="#">', '<a class="topbar-brand" href="../dashboard/index.html">')
    # buttons that finish a flow
    go = {'Create Initiative': '../initiative-view/index.html', 'Save Changes': '../profile/index.html', 'Save changes': '../profile/index.html',
          'Log in with Google': '../dashboard/index.html', 'Edit': '../profile-edit/index.html' if folder == 'self-review' else None}
    for label, to in go.items():
        if to:
            html = re.sub(r'<button class="(btn [^"]*)" type="button"((?: style="[^"]*")?)>((?:<svg[^>]*>.*?</svg>)?)' + re.escape(label) + '</button>',
                          lambda m: f'<button class="{m.group(1)}" type="button"{m.group(2)} data-go="{to}">{m.group(3)}{label}</button>', html, flags=re.S)
    if 'id="give-feedback"' in html:
        html = html.replace('<button class="btn btn-primary" type="button">Give feedback</button>', '<button class="btn btn-primary" type="button" data-modal-open="give-feedback">Give feedback</button>')
        html = html.replace('<button class="btn btn-secondary" type="button">Continue</button>', '<button class="btn btn-secondary" type="button" data-modal-close>Continue</button>')
    html = html.replace('<button class="btn btn-secondary" type="button">Create</button>', '<button class="btn btn-secondary" type="button" data-modal-close>Create</button>')
    # every RACI button opens the RACI drawer, on whichever screen it sits
    raci = '<button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="View RACI">'
    if raci in html:
        if 'id="raci-drawer"' not in html:
            html = html.replace('<script', screens.raci_overlay('Onboarding in one week') + '\n  <script', 1)
        html = html.replace(raci, raci.replace('>', ' data-modal-open="raci-drawer">'))
    html = re.sub(r'<a\b([^>]*?)href="#"([^>]*)>(.*?)</a>', link, html, flags=re.S)   # again, for what the drawer brought in
    return re.sub(r'<a class="ps-cal-more body-xs-semibold" href="#">', '<a class="ps-cal-more body-xs-semibold" href="#show-robview-0">', html)


def with_icons(html):
    """Icons drawn for this reference live in _src/icons.svg until promote.py
    moves them into the kit's sprite. A page gets the ones it names."""
    src = HERE / 'icons.svg'
    if not src.exists():
        return html
    names = set(re.findall(r'href="#([\w-]+)"', html))
    syms = [s for s in re.findall(r'  <symbol id="([^"]+)".*?</symbol>\n', src.read_text(), flags=re.S) if s in names]
    if not syms:
        return html
    body = ''.join(m.group(0) for m in re.finditer(r'  <symbol id="([^"]+)".*?</symbol>\n', src.read_text(), flags=re.S) if m.group(1) in names)
    sprite = '<svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" data-local-icons style="position:absolute;width:0;height:0;overflow:hidden">\n' + body + '</svg>\n'
    return re.sub(r'(<body[^>]*>\n)', lambda m: m.group(1) + sprite, html, count=1)


def main():
    built = []
    elements_html, icons_html = screens.elements_page(), screens.icons_page()   # first: they name what the audit control lists
    for s in screens.SCREENS:
        if s.get('plain'):
            html = plain(s['title'], s['main']).replace('../../designmd/', '../../../designmd/')
        else:
            html = page(s['title'], s['nav'], s['main'], s.get('ctas', ()), s.get('overlays', ''), padded=s.get('padded', True))
        d = OUT / s['folder']
        d.mkdir(exist_ok=True)
        html = wire(html, s['folder'])
        html = html.replace('</body>', screens.staging_link(s['folder']) + screens.audit_ui(s['folder']) + '</body>', 1)
        html = with_icons(html)
        screens.AUDIT[s['folder']] = screens.audit_count(html)
        (d / 'index.html').write_text(html)
        built.append(s['folder'])
    (OUT / 'index.html').write_text(plain('Production site · Nov 25, 2026', screens.index()))
    (OUT / 'elements').mkdir(exist_ok=True)
    (OUT / 'elements' / 'index.html').write_text(with_icons(plain('New elements · Production site', elements_html).replace('../../designmd/', '../../../designmd/')))
    (OUT / 'icons').mkdir(exist_ok=True)
    (OUT / 'icons' / 'index.html').write_text(with_icons(plain('New icons · Production site', icons_html).replace('../../designmd/', '../../../designmd/')))
    print('wrote', len(built), 'screens:', ', '.join(built))


if __name__ == '__main__':
    main()
