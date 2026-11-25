"""The content of each screen, as kit markup. build.py wraps it in the shell.

People and records are made up. Structure, labels and order follow the app as
it ran on 2026-11-25.
"""

LINK = 'style="color: var(--color-text-link); text-decoration: none"'
MUTED = 'style="color: var(--color-text-muted)"'

PEOPLE = {
    'ck': ('Cara Keane', 'Delivery Manager'),
    'lh': ('Laszlo Hartley', 'Delivery Manager'),
    'tl': ('Tobias Lindqvist', 'Quality Lead'),
    'lk': ('Lydia Kaminski', 'Operations Director'),
    'jp': ('Julian Park', 'Head of Learning'),
    'el': ('Elias Lowe', 'IT Manager'),
    'ad': ('Adele Delacroix', 'Partnerships Lead'),
    'km': ('Kwame Mensah', 'Hiring Manager'),
    'og': ('Oliver Grant', 'General Counsel'),
    'mt': ('Maya Thompson', 'Analytics Director'),
    'mv': ('Marisol Vega', 'Head of Recruiting'),
    'ac': ('Avery Collins', 'Chief People Officer'),
    'ho': ('Hannah Okafor', 'CEO'),
    'sr': ('Sofia Romano', 'Chief Operating Officer'),
    'nr': ('Nadia Rahman', 'Senior Product Designer'),
}


def ini(k):
    return k.upper()


def user(k, role=None, size='md'):
    name, r = PEOPLE[k]
    return (f'<div class="cell-user"><span class="avatar avatar-{size}">{ini(k)}</span><div class="cell-user-meta">'
            f'<span class="cell-user-name">{name}</span><span class="cell-user-role">{role or r}</span></div></div>')


def art(slug, size, label=''):
    """Artwork from the sprite at a fixed size: a badge or an illustration."""
    return f'<svg width="{size}" height="{size}" role="img" aria-label="{label}" style="flex-shrink: 0"><use href="#{slug}"/></svg>'


def icon(slug, cls='icon'):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#{slug}"/></svg>'


def tag(text, kind='light'):
    return f'<span class="tag tag-{kind}">{text}</span>'


def health(text, kind):
    return f'<span class="tag tag-light"><span class="ps-dot is-{kind}"></span>{text}</span>'


def tabs(items, active=0):
    out = ['<div class="tabs" role="tablist">']
    for i, t in enumerate(items):
        on = i == active
        out.append(f'<button class="tab{" is-active" if on else ""}" role="tab" aria-selected="{str(on).lower()}" type="button">{t}</button>')
    return '\n'.join(out) + '\n</div>'


def select(value, options=(), label=None, width=None, lead=None):
    if width:
        return f'<div style="flex: 0 0 auto; width: {width}px">{select(value, options, label, lead=lead)}</div>'
    if lead:
        return select(value, options, label).replace('<span class="input-select-value">', icon(lead, 'btn-icon') + '<span class="input-select-value">', 1)
    opts = ''.join(f'<button class="dropdown-item{" is-selected" if o == value else ""}" type="button">{o}</button>' for o in (options or (value,)))
    aria = f' aria-label="{label}"' if label else ''
    return (f'<div class="input-select"><button class="input-select-trigger" type="button" aria-expanded="false"{aria}>'
            f'<span class="input-select-value">{value}</span>{icon("i-chevron-down", "btn-icon")}</button>'
            f'<div class="dropdown-menu" hidden>{opts}</div></div>')


def segmented(items, active, label):
    b = ''.join(f'<button class="segmented-item{" is-active" if i == active else ""}" type="button">{t}</button>' for i, t in enumerate(items))
    return f'<div class="segmented" role="group" aria-label="{label}">{b}</div>'


def view_modes(active):
    modes = [('Detailed view', 'i-wide-tables-row'), ('Compact view', 'i-narrow-tables-row'), ('Spreadsheet view', 'i-table')]
    b = ''.join(f'<button class="segmented-item segmented-icon{" is-active" if i == active else ""}" type="button" aria-label="{l}">{icon(s)}</button>'
                for i, (l, s) in enumerate(modes))
    return f'<div class="segmented" role="group" aria-label="View" data-tabs="view">{b}</div>'


def desktop(html):
    return f'<div data-view="desktop">{html}</div>'


def mobile(html):
    return f'<div data-view="mobile" hidden>{html}</div>'


def mobile_toolbar(placeholder):
    return mobile(f'''<div class="toolbar" style="margin-bottom: var(--spacing-4); flex-wrap: nowrap">
        <div class="input-icon input-icon-left toolbar-search" style="flex: 1 1 0; min-width: 0">
          {icon("i-search", "icon input-icon-glyph")}
          <input class="input" type="text" placeholder="{placeholder}" aria-label="Search" />
        </div>
        <button class="btn btn-icon-only btn-ghost" type="button" aria-label="Filters">{icon("i-filter", "btn-icon")}</button>
        <button class="btn btn-icon-only btn-ghost" type="button" aria-label="Sort">{icon("i-sort", "btn-icon")}</button>
      </div>''')


def work_card(title, tags, k, unit, href=None, caret=False):
    name = f'<a class="body-semibold" href="{href}" {LINK}>{title}</a>' if href else f'<span class="body-semibold">{title}</span>'
    if caret:
        name = f'<div class="cell-title-row"><button class="row-toggle" type="button" aria-expanded="false" aria-label="Toggle children">{icon("i-caret-right")}</button>{name}</div>'
    return (f'<article class="card"><div class="stack" style="gap: var(--spacing-3)">{name}<div class="row" style="flex-wrap: wrap">{tags}</div>'
            f'<div class="row" style="justify-content: space-between">{user(k, unit)}<span class="row">'
            f'<button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="View RACI">{icon("i-table", "btn-icon")}</button>'
            f'{icon("i-slack-color", "icon icon-16")}</span></div></div></article>')


def head(title, actions='', after_title=''):
    act = f'\n        <div class="page-head-actions">\n          {actions}\n        </div>' if actions else ''
    return f'''      <div class="page-head">
        <div class="page-head-main">
          <div class="page-head-title">
            <h1 class="page-head-heading">{title}</h1>{after_title}
          </div>
        </div>{act}
      </div>'''


def pager(pages=('1', '2', '3', '…', '6')):
    cur = ' aria-current="page"'
    b = ''.join(f'<button class="btn btn-secondary btn-xs" type="button"{cur if p == "1" else ""}>{p}</button>' for p in pages)
    return (f'<div class="row" style="margin-top: var(--spacing-4)"><button class="btn btn-secondary btn-xs" type="button" disabled>Prev</button>'
            f'{b}<button class="btn btn-secondary btn-xs" type="button">Next</button></div>')


def work_toolbar(placeholder, columns, view=0):
    return desktop(f'''<div class="toolbar" style="margin-bottom: var(--spacing-4)">
        <div class="input-icon input-icon-left toolbar-search" style="flex: 0 1 300px">
          {icon("i-search", "icon input-icon-glyph")}
          <input class="input" type="text" placeholder="{placeholder}" aria-label="Search" />
        </div>
        <span class="row" data-hide-in="view:2"><button class="btn btn-secondary" type="button">{icon("i-filter", "btn-icon")}Filters</button>
        <button class="btn btn-secondary" type="button">{icon("i-code", "btn-icon")}Query</button></span>
        <span class="toolbar-spacer"></span>
        <span class="row" data-hide-in="view:2">{select(columns, label="Columns", width=190, lead="i-settings")}
        {select("Updated at", ("Updated at", "Name", "Status"), label="Sort by", width=150)}
        <button class="btn btn-secondary btn-icon-only" type="button" aria-label="Sort descending">{icon("i-arrow-down", "btn-icon")}</button></span>
        <button class="btn btn-icon-only btn-ghost" type="button" aria-label="View settings" data-show-in="view:2" hidden>{icon("i-controls", "btn-icon")}</button>
        {view_modes(view)}
      </div>''') + mobile_toolbar(placeholder)


PAIR = 'style="display: flex; flex-wrap: wrap; align-items: center; gap: var(--spacing-2) var(--spacing-6)"'


def field_row(label, value):
    return (f'<div {PAIR}><span class="body-sm" style="flex: 0 0 200px; color: var(--color-text-muted)">{label}</span>'
            f'<div style="flex: 1 1 240px; min-width: 0">{value}</div></div>')


GRID = 'style="display: flex; flex-direction: column; gap: var(--spacing-4)"'
RULE = 'style="margin: 0; padding-bottom: var(--spacing-3); border-bottom: 1px solid var(--color-border)"'

# --------------------------------------------------------------- Dashboard
OBJECTIVES = [
    ('Faster customer onboarding', 'sr', 'Onboarding in one week', 'Cut the time from signed contract to first delivered work.', 'Execution', 'blue'),
    ('Faster customer onboarding', 'sr', 'Self-serve account setup', 'Let customers set up billing and users without a call.', 'Definition', 'light'),
    ('Reliable delivery', 'lk', 'Delivery health reviews', 'A weekly review of every active engagement.', 'Execution', 'blue'),
    ('Reliable delivery', 'lk', 'Refund handling', 'One way of handling refund requests across regions.', 'Idea', 'light'),
    ('A stronger partner channel', 'ad', 'Partner marketing sites', 'Co-branded pages for the ten largest partners.', 'Execution', 'blue'),
    ('A stronger partner channel', 'ad', 'Partner certification', 'A short certification for partner sales teams.', 'Opportunity assessment', 'light'),
    ('Grow the team well', 'ac', 'Learning programs', 'A formal learning program for managers.', 'Execution', 'blue'),
    ('Grow the team well', 'ac', 'Recruiting pipeline', 'One pipeline view for every open role.', 'Complete', 'positive'),
]


def dashboard():
    rows = ''.join(
        f'<tr><td>{i}</td><td>{o}</td><td>{PEOPLE[k][0]}</td><td><span class="cell-title">{n}</span></td><td>{d}</td><td>{tag(s, kind)}</td></tr>'
        for i, (o, k, n, d, s, kind) in enumerate(OBJECTIVES, 1))
    stats = ''.join(f'<div class="stat-card"><p class="stat-card-label">{l}</p><p class="stat-card-value">{v}</p></div>'
                    for l, v in (('Idea', 33), ('Opportunity assessment', 5), ('Definition', 7), ('Execution', 53), ('Impact assessment', 0), ('Complete', 34)))
    actions = (segmented(('Core Strategy 28', 'Other initiatives 34'), 0, 'Initiatives shown') +
               f'\n          <button class="btn btn-icon-only btn-ghost" type="button" aria-label="More actions">{icon("i-dots-three-vertical", "btn-icon")}</button>')
    return f'''{head("TopTrack Dashboard", actions)}
      {mobile('<div class="ps-seg-fill" style="margin-bottom: var(--spacing-4)">' + segmented(('Core Strategy 28', 'Other initiatives 34'), 0, 'Initiatives shown') + '</div>')}

      <article class="card" style="margin-bottom: var(--spacing-6)">
        <div class="row" style="flex-wrap: wrap; gap: var(--spacing-2); margin: calc(-1 * var(--spacing-2)) 0 0; padding-bottom: var(--spacing-3); border-bottom: 1px solid var(--color-border); color: var(--color-text-muted)">
          <span class="body-sm"><span class="body-sm-semibold" style="color: var(--color-text)">6</span> Objectives</span>{icon("i-chevron-right", "icon icon-16")}
          <span class="body-sm"><span class="body-sm-semibold" style="color: var(--color-text)">28</span> Initiatives</span>{icon("i-chevron-right", "icon icon-16")}
          <span class="body-sm"><span class="body-sm-semibold" style="color: var(--color-text)">138</span> Projects</span>{icon("i-chevron-right", "icon icon-16")}
          <span class="body-sm"><span class="body-sm-semibold" style="color: var(--color-text)">118</span> Sub-projects</span>
        </div>
        <div class="ps-split" style="margin-top: var(--spacing-4)">
          <div class="stack" style="flex: 1 1 320px; min-width: 0">
            <div class="row" style="justify-content: space-between"><h2 class="body-semibold" style="margin: 0">Health</h2><span class="body-sm"><span class="body-sm-semibold">60%</span> on track</span></div>
            <div class="progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="60" aria-label="On track">
              <div class="progress-track"><div class="progress-fill" style="width: 60%"></div></div>
              <span class="progress-value" hidden>60%</span>
            </div>
            <div class="row" style="flex-wrap: wrap">{health("170 On track", "positive")}{health("1 At risk", "warning")}{health("1 Off track", "negative")}{health("112 Not active", "light")}</div>
          </div>
          <div class="stack ps-split-next" style="flex: 2 1 480px; min-width: 0">
            <h2 class="body-semibold" style="margin: 0">Status</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: var(--spacing-3)">{stats}</div>
          </div>
        </div>
      </article>

      {mobile_toolbar("Search by name, owner or function")}
      <div class="toolbar" data-view="desktop" style="margin-bottom: var(--spacing-3)">
        <div class="input-icon input-icon-left toolbar-search" style="flex: 0 1 290px">
          {icon("i-search", "icon input-icon-glyph")}
          <input class="input" type="text" placeholder="Search by name, owner or function" aria-label="Search" />
        </div>
        {"".join(f'<span data-panel="view:{i}"{"" if i == 0 else " hidden"}><span class="row"><button class="btn btn-secondary" type="button">' + icon("i-filter", "btn-icon") + 'Filters</button><button class="btn btn-secondary" type="button">' + icon("i-code", "btn-icon") + 'Query</button>' + check("Show in hierarchy", True) + '</span></span>' for i in (0, 1))}
        <span class="row" data-hide-in="view:2">{select("Strategic Objective, Objective Owner", ("Strategic Objective", "Objective Owner", "Status", "Health", "Accountability", "Roadmap", "RoB Meeting"), label="Columns", width=150, lead="i-settings")}
        {select("Updated at", ("Updated at", "Name", "Status", "Health"), label="Sort by", width=160)}
        <button class="btn btn-secondary btn-icon-only" type="button" aria-label="Sort descending">{icon("i-arrow-down", "btn-icon")}</button></span>
        <span class="toolbar-spacer"></span>
        <button class="btn btn-icon-only btn-ghost" type="button" aria-label="View settings" data-show-in="view:2" hidden>{icon("i-controls", "btn-icon")}</button>
        {view_modes(0)}
      </div>
      <div class="row" style="margin-bottom: var(--spacing-4)"><span class="chip">Tags: Core Strategy<button class="chip-remove" type="button" aria-label="Remove">{icon("i-x", "")}</button></span></div>

      <div class="table-scroll" style="max-height: none">
        <table class="table">
          <thead><tr><th>#</th><th>Strategic Objective</th><th>Objective Owner</th><th>Name</th><th>Description</th><th>Status</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>'''


# ---------------------------------------------------------------- Processes
PROCESSES = [
    ('Vendor Management', 'Not active', 'lk', 'Operations', ''),
    ('Learning Programs', 'Not started', 'jp', 'Learning & Development', ''),
    ('Workplace and IT', 'Active', 'el', 'IT', ''),
    ('Partner Marketing Sites', 'Active', 'ad', 'Partnerships', ''),
    ('Refund requests', 'Active', 'ck', 'Delivery', ('Oct 14 • 10:30am', 'Every week on Wednesday')),
    ('Northwind Hire', 'Paused', 'km', 'Northwind Hire', ''),
    ('Legal Operations', 'Active', 'og', 'Legal', ('Oct 09 • 11:00pm', 'Every week on Friday')),
    ('Analytics Reporting', 'Active', 'mt', 'Business Analytics', ('Oct 12 • 1:00pm', 'Every week on Monday')),
    ('Recruiting Pipeline', 'Active', 'mv', 'Recruiting', ('Oct 12 • 4:00pm', 'Every week on Monday')),
    ('Member Experience', 'Not started', 'ac', 'People', ''),
]


def rob_cell(r):
    if not r:
        return ''
    return f'<div class="cell-meta"><span class="cell-meta-title row" style="gap: var(--spacing-2)">{icon("i-calendar", "icon icon-16")}{r[0]}</span><span class="cell-meta-sub">{tag(r[1])}</span></div>'


def raci_btn():
    return (f'<div class="cell-actions"><button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="View RACI">{icon("i-table", "btn-icon")}</button>'
            f'<button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="Open Slack channel">{icon("i-slack-color", "btn-icon")}</button></div>')


def processes():
    rows = ''.join(
        f'<tr><td><span class="cell-title">{n}</span><div>{tag("Process")}</div></td><td>{tag(s)}</td><td>{user(k, unit)}</td><td>{rob_cell(r)}</td><td>{raci_btn()}</td></tr>'
        for n, s, k, unit, r in PROCESSES)
    cards = ''.join(work_card(n, tag("Process") + tag(s), k, unit) for n, s, k, unit, r in PROCESSES)
    return f'''{head("Processes", '<button class="btn btn-primary" type="button">Create Process</button>')}

{work_toolbar("Search by name, owner or function", "Status, Accountability, RoB Meeting")}

      {mobile('<div class="stack">' + cards + '</div>')}
      <div class="table-scroll" style="max-height: none" data-view="desktop">
        <table class="table">
          <thead><tr><th>Name <button class="btn btn-ghost btn-xs" type="button">Expand all</button></th><th>Status</th><th>Accountability</th><th>RoB Meeting</th><th style="text-align: right">Actions</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
      {pager()}'''


# -------------------------------------------------------------- Initiatives
INITIATIVES = [
    ('Onboarding in one week', 'Execution', 'blue', ('On track', 'positive'), 'sr', 'Operations', 'Q4 2026', ('Oct 13 • 10:30am', 'Every week on Tuesday')),
    ('Self-serve account setup', 'Definition', 'light', ('Not active', 'light'), 'el', 'IT', 'Q1 2027', ''),
    ('Delivery health reviews', 'Execution', 'blue', ('At risk', 'warning'), 'lk', 'Operations', 'Q4 2026', ('Oct 15 • 2:00pm', 'Every 2 weeks on Thursday')),
    ('Refund handling', 'Idea', 'light', ('Not active', 'light'), 'ck', 'Delivery', '', ''),
    ('Partner marketing sites', 'Execution', 'blue', ('On track', 'positive'), 'ad', 'Partnerships', 'Q4 2026', ('Oct 12 • 9:00am', 'Every week on Monday')),
    ('Partner certification', 'Opportunity assessment', 'light', ('Not active', 'light'), 'ad', 'Partnerships', '', ''),
    ('Learning programs', 'Execution', 'blue', ('Off track', 'negative'), 'jp', 'Learning & Development', 'Q4 2026', ('Oct 16 • 11:00am', 'Every week on Friday')),
    ('Recruiting pipeline', 'Complete', 'positive', ('On track', 'positive'), 'mv', 'Recruiting', 'Q3 2026', ''),
]


def initiatives():
    rows = []
    for i, (n, s, kind, h, k, unit, road, r) in enumerate(INITIATIVES):
        name = (f'<a class="cell-title" href="../initiative-view/index.html" {LINK}>{n}</a>' if i == 0 else f'<span class="cell-title">{n}</span>')
        rows.append(f'<tr><td>{name}<div>{tag("Initiative")}</div></td><td>{tag(s, kind)}</td><td>{health(*h)}</td><td>{user(k, unit)}</td>'
                    f'<td><span class="body-sm">{road}</span></td><td>{rob_cell(r)}</td><td>{raci_btn()}</td></tr>')
    cards = ''.join(work_card(n, health(*h) + tag("Initiative") + tag(s, kind), k, unit, '../initiative-view/index.html' if i == 0 else None)
                    for i, (n, s, kind, h, k, unit, road, r) in enumerate(INITIATIVES))
    return f'''{head("Initiatives", '<a class="btn btn-primary" href="../initiative-create/index.html" style="text-decoration: none">Create Initiative</a>')}

{work_toolbar("Search by name, owner or function", "Status, Health, Accountability")}

      {mobile('<div class="stack">' + cards + '</div>')}
      <div class="table-scroll" style="max-height: none" data-view="desktop">
        <table class="table">
          <thead><tr><th>Name</th><th>Status</th><th>Health {icon("i-info", "icon icon-16")}</th><th>Accountability</th><th>Roadmap</th><th>RoB Meeting</th><th style="text-align: right">Actions</th></tr></thead>
          <tbody>{"".join(rows)}</tbody>
        </table>
      </div>
      {pager(("1", "2", "3"))}'''


SECTIONS = [('General', 'i-list'), ('People', 'i-participants'), ('Timeline', 'i-calendar'), ('Description', 'i-list-unordered'),
            ('Connections', 'i-link'), ('Documents', 'i-attachment'), ('Projects', 'i-folder')]


def section_nav():
    items = ''.join(f'<a class="btn btn-ghost" href="#sec-{l.lower()}" style="justify-content: flex-start; text-decoration: none">{icon(s, "btn-icon")}{l}</a>'
                    for l, s in SECTIONS)
    return f'<nav class="stack" data-view="desktop" aria-label="Sections" style="position: sticky; top: var(--spacing-6); gap: var(--spacing-1); flex: 0 0 200px">{items}</nav>'


def raci_table(rows):
    body = ''.join(f'<tr><td><span class="cell-title">{u}</span><div><span class="body-xs" {MUTED}>{t}</span></div></td><td>{a}</td><td>{r}</td><td>{c}</td><td>{i}</td></tr>'
                   for u, t, a, r, c, i in rows)
    return (f'<div class="table-scroll" style="max-height: none"><table class="table"><thead><tr><th>Org Unit</th><th>Accountable <span {MUTED}>(max 1)</span></th>'
            f'<th>Responsible <span {MUTED}>(max 20)</span></th><th>Consulted <span {MUTED}>(max 20)</span></th><th>Informed <span {MUTED}>(max 20)</span></th></tr></thead><tbody>{body}</tbody></table></div>')


def crumbs(last):
    return (f'<nav class="breadcrumbs" aria-label="Breadcrumb"><a class="breadcrumb" href="../initiatives/index.html">Initiatives</a>'
            f'<span class="breadcrumb is-current" aria-current="page">{last}</span></nav>')


def initiative_view():
    general = ''.join((
        field_row('Status', tag('Execution')),
        field_row('Health', health('On track', 'positive')),
        field_row('Executive sponsor', user('ho')),
        field_row('Beneficiary function', f'<div class="row">{icon("i-function", "icon icon-16")}<span class="body-sm-semibold">Operations</span></div>'),
        field_row('Related initiatives &amp; projects', f'<a class="body-sm" href="#" {LINK}>Self-serve account setup</a>'),
        field_row('Core strategy', health('On', 'positive')),
        field_row('Company strategic objective', '<span class="body-sm">Faster customer onboarding</span>'),
    ))
    people = ''.join((
        field_row('Accountable owner', user('sr')),
        field_row('Project manager', user('ck')),
        field_row('Working team', f'<div class="row" style="flex-wrap: wrap; gap: var(--spacing-4)">{user("lh")}{user("tl")}{user("nr")}</div>'),
    ))
    timeline = ''.join((
        field_row('Estimated duration', '<span class="body-sm">6 months</span>'),
        field_row('Start date', '<span class="body-sm">Jul 1, 2026</span>'),
        field_row('End date', '<span class="body-sm">Dec 18, 2026</span>'),
        field_row('Initial impact date', '<span class="body-sm">Oct 1, 2026</span>'),
        field_row('Full impact date', '<span class="body-sm">Mar 1, 2027</span>'),
    ))
    raci = raci_table([('Operations', 'Function', user('sr'), user('ck'), user('lk'), user('ho')),
                       ('Delivery', 'Subfunction', '', user('lh'), user('tl'), '')])
    projects = ''.join(
        f'<tr><td><span class="cell-title">{n}</span><div>{tag("Project")}</div></td><td>{tag(s, k)}</td><td>{user(u)}</td></tr>'
        for n, s, k, u in (('Kick-off checklist', 'Execution', 'blue', 'ck'), ('Contract to workspace handoff', 'Execution', 'blue', 'lh'), ('First-week survey', 'Idea', 'light', 'tl')))
    return f'''      <div style="padding: var(--spacing-6) var(--spacing-10) var(--spacing-10)">
      {crumbs("Onboarding in one week")}
      <div class="row" style="flex-wrap: wrap; justify-content: space-between; margin-top: var(--spacing-3)">
        <h1 class="h2" style="margin: 0">Onboarding in one week</h1>
        <div class="row">
          <button class="btn btn-icon-only btn-ghost" type="button" aria-label="Copy Link">{icon("i-link", "btn-icon")}</button>
        </div>
      </div>
      <p class="body-xs" style="margin: var(--spacing-1) 0 var(--spacing-4); color: var(--color-text-muted)">Last edit was made 18 hours ago by <a href="#" {LINK}>Sofia Romano</a></p>
      {tabs(("Overview", "Activity log"))}

      <div style="display: flex; align-items: flex-start; gap: var(--spacing-10); margin-top: var(--spacing-6)">
        <div class="stack" style="flex: 1; min-width: 0; gap: var(--spacing-8)">
          <section class="stack" id="sec-general"><h2 class="h4" {RULE}>General</h2><div {GRID}>{general}</div></section>
          <section class="stack" id="sec-people"><h2 class="h4" {RULE}>People</h2><div {GRID}>{people}</div>
            <h3 class="body-semibold" style="margin: var(--spacing-2) 0 0">RACI</h3>{raci}</section>
          <section class="stack" id="sec-timeline"><h2 class="h4" {RULE}>Timeline</h2><div {GRID}>{timeline}</div></section>
          <section class="stack" id="sec-description"><h2 class="h4" {RULE}>Description</h2>
            <div><span class="body-sm" {MUTED}>Problem / Opportunity</span><p class="body" style="margin: var(--spacing-2) 0 0">New customers wait three weeks between signing and the first delivered work. Most of that time is handoffs.</p></div>
            <div><span class="body-sm" {MUTED}>Objective(s)</span><p class="body" style="margin: var(--spacing-2) 0 0">Every new customer has work in progress within one week of signing.</p></div>
            <div><span class="body-sm" {MUTED}>Success metrics</span><p class="body" style="margin: var(--spacing-2) 0 0">Median time from contract to first delivery is 7 days or less.</p></div>
          </section>
          <section class="stack" id="sec-connections"><h2 class="h4" {RULE}>Connections</h2>
            <div style="display: grid; grid-template-columns: minmax(140px, 220px) 1fr; gap: var(--spacing-4); align-items: center">
              <div class="row"><span class="icon-tile icon-tile-sm">{icon("i-calendar")}</span><span class="body-sm">RoB Meetings</span></div>
              <div><a class="body-sm" href="../rob-meeting-view/index.html" {LINK}>[RoB] Onboarding in one week</a><div class="row"><span class="body-sm">Oct 13 • 10:30am</span>{tag("Every week on Tuesday")}</div></div>
              <div class="row"><span class="icon-tile icon-tile-sm">{icon("i-slack-color")}</span><span class="body-sm">Slack channels</span></div>
              <div class="row"><a class="body-sm" href="#" {LINK}># onboarding-one-week</a>{tag("Default")}</div>
              <div class="row"><span class="icon-tile icon-tile-sm">{icon("i-bookmark")}</span><span class="body-sm">Tags</span></div>
              <div class="row"><span class="chip">#Core Strategy</span></div>
            </div>
            <h3 class="body-semibold row" style="margin: var(--spacing-2) 0 0">Agenda{tag("0")}</h3>
            <div class="row" style="padding: var(--spacing-4); border: 1px solid var(--color-border); border-radius: var(--radius-sm)">{icon("i-list-unordered", "icon icon-16")}<span class="body-sm">No Agenda Items yet</span></div>
          </section>
          <section class="stack" id="sec-documents"><h2 class="h4" {RULE}>Documents</h2>
            <div class="row" style="justify-content: center; color: var(--color-text-muted)">{icon("i-search", "icon icon-16")}<span class="body-sm">No attachments</span></div></section>
          <section class="stack" id="sec-projects"><h2 class="h4" {RULE}>Projects</h2>
            <div>{"".join(f'<a class="ps-linkrow" href="#"><span class="body-sm">{n}</span>{icon("i-chevron-right", "icon icon-16")}</a>' for n in ("Kick-off checklist", "Account setup in one day", "Onboarding status page", "Contract to workspace handoff", "First-week survey"))}</div></section>
        </div>
        {section_nav()}
      </div>
      </div>'''


def fld(label, control, hint=''):
    h = f'<span class="field-hint">{hint}</span>' if hint else ''
    return (f'<div {PAIR}><span class="body-sm" style="flex: 0 0 200px">{label}</span>'
            f'<div style="flex: 1 1 240px; min-width: 0">{control}{h}</div></div>')


def ph_select(text, label, width=None):
    if width:
        return f'<div style="flex: 0 0 auto; width: {width}px">{ph_select(text, label)}</div>'
    return (f'<div class="input-select"><button class="input-select-trigger" type="button" aria-expanded="false" aria-label="{label}">'
            f'<span class="input-select-value input-select-placeholder">{text}</span>{icon("i-chevron-down", "btn-icon")}</button><div class="dropdown-menu" hidden></div></div>')


def add_btn(text):
    return f'<button class="btn btn-ghost" type="button">{icon("i-plus", "btn-icon")}{text}</button>'


def date_input(label):
    return (f'<div class="input-icon input-icon-left">{icon("i-calendar", "icon input-icon-glyph")}'
            f'<input class="input" type="text" placeholder="Add date" aria-label="{label}" /></div>')


def initiative_create():
    general = ''.join((
        fld('Status', select('Idea', ('Idea', 'Opportunity assessment', 'Definition', 'Execution', 'Impact assessment', 'Complete'), 'Status')),
        fld('Health', select('Not active', ('Not active', 'On track', 'At risk', 'Off track'), 'Health')),
        fld('Executive sponsor', ph_select('Select who gives governance and backing', 'Executive sponsor')),
        fld('Beneficiary function ' + icon("i-info", "icon icon-16"), ph_select('Select the function that benefits from the outcome', 'Beneficiary function')),
        fld('Related initiatives &amp; projects', ph_select('Link initiatives or projects this relates to', 'Related initiatives and projects')),
        fld('Core strategy<span class="body-xs" style="display: block; color: var(--color-text-muted)">Supports a company-level objective</span>',
            '<label class="row"><span class="switch"><input type="checkbox" class="switch-input" aria-label="Core strategy" /><span class="switch-track"></span></span></label>'),
    ))
    people = ''.join((
        fld('Accountable owner', select('Cara Keane', label='Accountable owner')),
        fld('Project manager', ph_select('Select who runs day-to-day delivery', 'Project manager')),
        fld('Working team', add_btn('Add team member')),
    ))
    timeline = ''.join((
        fld('Estimated duration', ph_select('Select a duration', 'Estimated duration')),
        fld('Start date', date_input('Start date')), fld('End date', date_input('End date')),
        fld('Initial impact date', date_input('Initial impact date')), fld('Full impact date', date_input('Full impact date')),
    ))
    raci = raci_table([('Operationalize', 'Team', user('ck'), '', '', '')])

    def area(label, ph):
        return f'<label class="field"><span class="field-label">{label}</span><textarea class="input" rows="3" placeholder="{ph}"></textarea></label>'
    return f'''      <div style="display: flex; flex-direction: column; min-height: calc(100vh - var(--header-height))">
      <div style="flex: 1; padding: var(--spacing-6) var(--spacing-10) var(--spacing-10)">
      {crumbs("New initiative")}

      <div style="display: flex; align-items: flex-start; gap: var(--spacing-10); margin-top: var(--spacing-3)">
        <div class="stack" style="flex: 1; min-width: 0; gap: var(--spacing-8)">
          <input class="input" type="text" placeholder="Add initiative name" aria-label="Initiative name" style="width: 100%; max-width: none" />
          <section class="stack" id="sec-general"><h2 class="h4" {RULE}>General</h2><div {GRID}>{general}</div>
            <div class="row">{add_btn("Add business lines")}{add_btn("Add tags")}</div></section>
          <section class="stack" id="sec-people"><h2 class="h4" {RULE}>People</h2><div {GRID}>{people}</div>
            <div class="row" style="justify-content: space-between"><h3 class="body-semibold" style="margin: 0">RACI</h3><a class="row body-sm" href="#" {LINK}>{icon("i-info", "icon icon-16")}RACI Guide</a></div>{raci}</section>
          <section class="stack" id="sec-timeline"><h2 class="h4" {RULE}>Timeline</h2><div {GRID}>{timeline}</div></section>
          <section class="stack" id="sec-description"><h2 class="h4" {RULE}>Description</h2>
            {area("Problem / Opportunity", "What problem does this solve, or what opportunity does it open?")}
            {area("Objective(s)", "What will be true when this is done?")}
            <div class="row">{add_btn("Add objective")}</div>
            {area("Success metrics", "How will you measure it?")}
            <div class="row">{add_btn("Add success metric")}</div>
          </section>
          <section class="stack" id="sec-connections"><h2 class="h4" {RULE}>Connections</h2>
            <div class="alert">{icon("i-info", "icon alert-icon")}<p class="alert-message">RACI members with the roles selected for auto-invite in the RACI drawer will become the RoB participants</p></div>
            <article class="card"><div class="row">{icon("i-slack-color", "icon icon-24")}<div><p class="body-semibold" style="margin: 0">Slack</p><p class="body-sm" style="margin: 0; color: var(--color-text-muted)">Create or add Slack channels to sync conversations with this initiative</p></div></div></article>
            <article class="card"><div class="row">{icon("i-calendar", "icon icon-24")}<div><p class="body-semibold" style="margin: 0">RoB Meetings</p><p class="body-sm" style="margin: 0; color: var(--color-text-muted)">Keep your team aligned with recurring meetings.</p></div></div></article>
          </section>
          <section class="stack" id="sec-documents"><h2 class="h4" {RULE}>Documents</h2><div class="row">{add_btn("Add URL links")}</div></section>
          <section class="stack" id="sec-projects"><h2 class="h4" {RULE}>Projects</h2>
            <p class="body-sm" style="margin: 0; color: var(--color-text-muted)">Projects can be added once the initiative is created.</p></section>
        </div>
        {section_nav()}
      </div>
      </div>
      <div class="row row-end" style="position: sticky; bottom: 0; background: var(--color-surface); border-top: 1px solid var(--color-border); padding: var(--spacing-4) calc(var(--spacing-10) + var(--spacing-12)) var(--spacing-4) var(--spacing-10)">
        <a class="btn btn-secondary" href="../initiatives/index.html" style="text-decoration: none">Cancel</a>
        <button class="btn btn-primary" type="button">Create Initiative</button>
      </div>
      </div>'''


# -------------------------------------------------------------- RoB Meetings
EVENTS = {  # day of November 2026 -> (title, time and unit)
    2: [('[RoB] Onboarding in one week', '10:30am Operations')], 9: [('[RoB] Onboarding in one week', '10:30am Operations')],
    16: [('[RoB] Onboarding in one week', '10:30am Operations')], 23: [('[RoB] Onboarding in one week', '10:30am Operations'), ('Delivery All Hands', '2:00pm Delivery')],
    11: [('[RoB] Refund requests', '1:30pm Delivery')], 18: [('[RoB] Refund requests', '1:30pm Delivery')], 25: [('[RoB] Refund requests', '1:30pm Delivery')],
    12: [('[RoB] Partner marketing sites', '4:00pm Partnerships')], 26: [('[RoB] Partner marketing sites', '4:00pm Partnerships')],
}


def rob_calendar():
    weeks = [[2, 3, 4, 5, 6], [9, 10, 11, 12, 13], [16, 17, 18, 19, 20], [23, 24, 25, 26, 27], [30, None, None, None, None]]
    body = []
    for w in weeks:
        tds = []
        for d in w:
            if d is None:
                tds.append('<td></td>')
                continue
            num = (f'<span class="count-badge">{d}</span>' if d == 25 else f'<span class="body-xs" {MUTED}>{d:02d}</span>')
            ev = ''.join(f'<a class="list-row" href="../rob-meeting-view/index.html" style="text-decoration: none"><div><p class="list-row-title">{t}</p><p class="list-row-meta">{m}</p></div></a>'
                         for t, m in EVENTS.get(d, ()))
            tds.append(f'<td style="vertical-align: top; height: 120px"><div class="row row-end">{num}</div>{ev}</td>')
        body.append('<tr>' + ''.join(tds) + '</tr>')
    return f'''{head("RoB Meetings", '<button class="btn btn-primary" type="button" disabled title="Creating meetings is closed for this account on staging">Create meeting</button>', after_title=icon("i-info", "icon icon-16"))}

      {tabs(("My events", "All events"))}

      <div class="toolbar" style="margin: var(--spacing-4) 0">
        <div class="input-icon input-icon-left toolbar-search">
          {icon("i-search", "icon input-icon-glyph")}
          <input class="input" type="text" placeholder="Search" aria-label="Search meetings" />
        </div>
        <button class="btn btn-secondary" type="button">{icon("i-filter", "btn-icon")}Filters</button>
        <span class="toolbar-spacer"></span>
        {segmented(("Schedule", "Week", "Month"), 2, "Calendar view")}
      </div>

      <div class="row" style="justify-content: space-between; margin-bottom: var(--spacing-3)">
        <h2 class="h3" style="margin: 0">November 2026</h2>
        <div class="row">
          <button class="btn btn-secondary btn-icon-only" type="button" aria-label="Previous month">{icon("i-arrow-long-left", "btn-icon")}</button>
          <button class="btn btn-secondary" type="button">Today</button>
          <button class="btn btn-secondary btn-icon-only" type="button" aria-label="Next month">{icon("i-arrow-long-right", "btn-icon")}</button>
        </div>
      </div>

      <div class="table-scroll" style="max-height: none">
        <table class="table" style="table-layout: fixed; min-width: 880px">
          <thead><tr><th>Monday</th><th>Tuesday</th><th>Wednesday</th><th>Thursday</th><th>Friday</th></tr></thead>
          <tbody>{"".join(body)}</tbody>
        </table>
      </div>'''


def user_marked(k, mark='', size='md'):
    """A person with a mark on the avatar: 'yes' or 'no' for whether they
    accepted the meeting, 'talent' for a talent network member."""
    name, r = PEOPLE[k]
    m = {'yes': f'<span class="ps-avatar-mark is-yes" title="Accepted">{icon("i-check-minor", "icon")}</span>', 'no': f'<span class="ps-avatar-mark is-no" title="Declined">{icon("i-close-minor", "icon")}</span>',
         'talent': '<span class="ps-avatar-mark is-talent" title="Talent network member">T</span>'}.get(mark, '')
    return (f'<div class="cell-user"><span class="ps-avatar-wrap"><span class="avatar avatar-{size}">{ini(k)}</span>{m}</span><div class="cell-user-meta">'
            f'<span class="cell-user-name">{name}</span><span class="cell-user-role">{r}</span></div></div>')


def rob_meeting_view():
    def sec(title, inner, sid):
        return f'<section class="stack" id="mv-{sid}"><h3 class="h4" {RULE}>{title}</h3>{inner}</section>'

    def empty(text):
        return f'<div class="row" style="color: var(--color-text-muted)">{icon("i-list-unordered", "icon icon-16")}<span class="body-sm">{text}</span></div>'
    details = f'''<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: var(--spacing-4)">
              <div class="row">{icon("i-calendar", "icon icon-16")}<span class="body-sm">Tuesday, November 10</span></div>
              <div class="row">{icon("i-time", "icon icon-16")}<span class="body-sm">10:30 AM – 11:30 AM</span></div>
              <div class="row">{icon("i-globe", "icon icon-16")}<span class="body-sm">GMT+1</span></div>
              <div class="row">{icon("i-update", "icon icon-16")}<span class="body-sm">Every week on Tuesday until Dec 22, 2026</span>{health("High", "warning")}</div>
              <div class="row">{icon("i-video-on", "icon icon-16")}<a class="body-sm" href="#" {LINK}>Zoom: 954 0000 0000</a>{health("REC", "negative")}</div>
              <div class="row">{icon("i-availability-full-time", "icon icon-16")}<span class="body-sm">Busy</span></div>
              <div class="row">{icon("i-function", "icon icon-16")}<a class="body-sm" href="#" {LINK}>Operations</a></div>
              <div class="row">{icon("i-org-unit", "icon icon-16")}<span class="body-sm">Services</span></div>
            </div>
            <div class="row" style="align-items: flex-start">{icon("i-list-unordered", "icon icon-16")}<p class="body-sm" style="margin: 0">A weekly working session for the team that runs Onboarding in one week: a short round of status, then decisions and actions.</p></div>'''
    people = ''.join(f'<div class="row" style="justify-content: space-between">{user_marked(k, m)}{tag(r, "positive") if r else ""}</div>'
                     for k, m, r in (('ck', 'yes', 'R'), ('lh', 'yes', 'R'), ('tl', 'no', ''), ('lk', 'yes', 'C'), ('nr', 'yes', ''), ('el', '', '')))
    def item(no, text, freq, k):
        return (f'<div class="ps-agenda-row"><span class="body-sm" {MUTED}>{no}</span><span class="body-sm">{text}</span>{tag(freq)}'
                f'<span class="row" style="gap: var(--spacing-1); flex-wrap: nowrap"><span class="avatar avatar-xs">{ini(k)}</span><span class="body-xs" style="white-space: nowrap">{PEOPLE[k][0]}</span></span></div>')
    agenda_block = (f'<p class="body-sm-semibold row" style="margin: 0">This meeting{tag("1")}</p>'
                    + item('1', 'Onboarding status: where each new customer is in the first week, and what is blocking them', 'Weekly', 'ck')
                    + f'<p class="body-sm-semibold row" style="margin: var(--spacing-3) 0 0">Other meetings{tag("3")}</p>'
                    + item('-', 'Roadmap review: scope and any shifts to milestones or dates since last time', 'Monthly', 'sr')
                    + item('-', 'Decisions needed: open questions that need sign-off before work starts', 'Bi-weekly', 'lk')
                    + item('-', 'Handoff problems: what went wrong between sales and delivery this week', 'Weekly', 'ck'))
    deck = (f'<article class="card" style="background: var(--color-accent); color: var(--color-text-inverse); min-height: 200px; display: flex; align-items: flex-end">'
            f'<p class="h2" style="margin: 0; color: inherit">Onboarding in one week</p></article>')
    metric = (f'<div class="row" style="justify-content: space-between"><span class="row">{icon("i-target", "icon icon-16")}<span class="body-sm">Add key metric</span></span>'
              f'<button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="Edit key metric">{icon("i-pencil", "btn-icon")}</button></div>')
    nav = ''.join(f'<a class="btn btn-ghost" href="#mv-{i}" style="justify-content: flex-start; text-decoration: none">{icon(s, "btn-icon")}{l}</a>'
                  for l, s, i in (('Details', 'i-list', 'details'), ('Recording', 'i-video-on', 'recording'), ('Deck', 'i-presenter', 'deck'), ('Agenda', 'i-list-unordered', 'agenda'), ('Action items', 'i-list-checkboxes', 'actions'),
                                  ('Pre-read materials', 'i-attachment', 'preread'), ('Connections', 'i-link', 'connections'), ('History', 'i-time', 'history')))
    return f'''  <div class="modal-overlay" id="meeting-view">
    <div class="modal modal-full" role="dialog" aria-modal="true" aria-labelledby="meeting-view-title">
      <header class="modal-header" style="flex-wrap: wrap">
        <h2 class="modal-title" id="meeting-view-title">[RoB] Onboarding in one week</h2>
        <div class="row" style="flex-wrap: wrap">
          <button class="btn btn-secondary btn-icon-only" type="button" aria-label="Previous meeting">{icon("i-chevron-left", "btn-icon")}</button>
          <span class="row body-sm-semibold" style="flex-wrap: wrap">{icon("i-calendar", "icon icon-16")}Tuesday, November 10 · 10:30 AM – 11:30 AM (GMT+1)</span>
          <button class="btn btn-secondary btn-icon-only" type="button" aria-label="Next meeting">{icon("i-chevron-right", "btn-icon")}</button>
          <button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="More actions">{icon("i-dots-three-vertical", "btn-icon")}</button>
          <a class="btn btn-icon-only btn-ghost btn-xs modal-close" href="../rob-meetings/index.html" aria-label="Close">{icon("i-x")}</a>
        </div>
      </header>
      <div class="modal-body">
        <div style="display: flex; flex-wrap: wrap; align-items: flex-start; gap: var(--spacing-10)">
          <div class="stack" style="flex: 3 1 320px; min-width: 0; gap: var(--spacing-8)">
            {sec("Details", details + metric, "details")}
            {sec("Recording", f'<div class="row">{icon("i-video-on", "icon icon-16")}<a class="body-sm" href="#" {LINK}>Zoom Recording</a><span class="body-sm" {MUTED}>(1h 8m)</span><button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="Copy link">{icon("i-copy", "btn-icon")}</button></div>', "recording")}
            {sec("Deck", deck, "deck")}
            {sec("Agenda", agenda_block, "agenda")}
            {sec('Action items <span class="count-badge count-badge-secondary">0</span>', empty("No action items were added in this meeting."), "actions")}
            {sec("Pre-read materials", empty("No pre-read materials yet"), "preread")}
            {sec("Connections", f'<div class="row"><span class="icon-tile icon-tile-sm">{icon("i-initiatives")}</span><a class="body-sm" href="../initiative-view/index.html" {LINK}>Onboarding in one week</a>{tag("Initiative")}</div>', "connections")}
            {sec("History", f'<p class="body-sm" style="margin: 0; color: var(--color-text-muted)">Created by Sofia Romano on Jul 3, 2026</p>', "history")}
          </div>
          <div class="stack" style="flex: 2 1 240px; min-width: 0">
            <h3 class="h4" style="margin: 0">Owner</h3>
            <div class="row" style="justify-content: space-between">{user_marked("sr", "yes")}{tag("A", "negative")}</div>
            <h3 class="h4 row" style="margin: var(--spacing-4) 0 0">Participants <span class="count-badge count-badge-secondary">6</span>{icon("i-info", "icon icon-16")}</h3>
            {people}
          </div>
          <nav class="stack" data-view="desktop" aria-label="Sections" style="position: sticky; top: 0; gap: var(--spacing-1); flex: 0 0 200px">{nav}</nav>
        </div>
      </div>
    </div>
  </div>'''


# --------------------------------------------------------------------- OKRs
OKRS = [
    ('Faster customer onboarding', 'Active', 'positive', [('Median time from contract to first delivery is 7 days', 64), ('Nine in ten customers finish setup without a call', 40)]),
    ('Reliable delivery', 'Active', 'positive', [('Every engagement has a weekly health review', 85)]),
    ('A stronger partner channel', 'Draft', 'light', [('Ten partner sites live', 30), ('Fifty certified partner sellers', 0)]),
    ('Grow the team well', 'Draft', 'light', [('Every manager completes the learning program', 0)]),
]


def okrs():
    cards = []
    for name, st, kind, krs in OKRS:
        rows = ''.join(
            f'<div class="list-row" style="flex-wrap: wrap"><div><p class="list-row-title">{kr}</p></div><div class="row">'
            f'{tag(icon("i-cpu-2", "icon") + " 1")}{tag(icon("i-initiatives", "icon") + " 2")}{tag(icon("i-okr", "icon") + " 0")}'
            f'<span class="body-sm-semibold">{pct}%</span></div></div>' for kr, pct in krs)
        cards.append(f'<article class="card"><div class="row"><h3 class="body-lg-semibold" style="margin: 0">{name}</h3>{tag(st, kind)}</div>{rows}</article>')
    actions = (f'<button class="btn btn-secondary" type="button">{icon("i-info", "btn-icon")}Performance attributes</button>\n          '
               '<button class="btn btn-secondary" type="button">Export as CSV</button>\n          <button class="btn btn-primary" type="button" disabled title="Creating OKRs is closed for this account on staging">Create OKR</button>')
    return f'''{head("OKRs", actions, after_title=select("2026", ("2025", "2026", "2027"), "Year"))}

      {tabs(("Company Vision", "Company Objective", "Function Annual", "Function Quarterly", "Team Quarterly", "Shared Key Results"))}

      <div class="toolbar" style="margin: var(--spacing-4) 0">
        <div class="input-icon input-icon-left toolbar-search">
          {icon("i-search", "icon input-icon-glyph")}
          <input class="input" type="text" placeholder="Search OKR" aria-label="Search OKR" />
        </div>
        {select("All attributes", label="Attributes", width=180)}
        {select("Date Created", ("Date Created", "Name", "Progress"), label="Sort by", width=160)}
        <button class="btn btn-secondary btn-icon-only" type="button" aria-label="Sort ascending">{icon("i-arrow-down", "btn-icon")}</button>
      </div>

      <div class="stack">{"".join(cards)}</div>
      {pager(("1", "2"))}'''


# ------------------------------------------------------------------- People
DIRECTORY = [
    ('ad', ('Partnerships', 'Function'), 'ho', ('Lyon', 'France'), '09:54'),
    ('ac', ('People', 'Function'), 'ho', ('Austin', 'Texas, United States'), '02:54'),
    ('ck', ('Delivery', 'Subfunction in Operations'), 'lk', ('Dublin', 'Ireland'), '08:54'),
    ('el', ('IT', 'Function'), 'sr', ('Toronto', 'Ontario, Canada'), '03:54'),
    ('jp', ('Learning &amp; Development', 'Subfunction in People'), 'ac', ('Seoul', 'South Korea'), '17:54'),
    ('km', ('Northwind Hire', 'Team in Recruiting'), 'mv', ('Accra', 'Ghana'), '08:54'),
    ('lh', ('Delivery', 'Subfunction in Operations'), 'lk', ('Budapest', 'Hungary'), '09:54'),
    ('lk', ('Operations', 'Function'), 'sr', ('Warsaw', 'Poland'), '09:54'),
    ('mv', ('Recruiting', 'Subfunction in People'), 'ac', ('Valencia', 'Spain'), '09:54'),
    ('mt', ('Business Analytics', 'Function'), 'ho', ('Denver', 'Colorado, United States'), '01:54'),
]


def two(a, b):
    return f'<div class="cell-meta"><span class="cell-meta-title">{a}</span><span class="cell-meta-sub">{b}</span></div>'


def people():
    rows, cards = [], []
    for i, (k, unit, mgr, loc, t) in enumerate(DIRECTORY):
        who = user(k)
        if k == 'ck':
            who = f'<a href="../profile/index.html" style="text-decoration: none; color: inherit">{who}</a>'
        rows.append(f'<tr><td>{who}</td><td>{two(*unit)}</td><td>{two(*PEOPLE[mgr])}</td><td>{two(*loc)}</td><td><span class="body-sm">{t}</span></td></tr>')
        pairs = ''.join(f'<span class="body-sm-semibold" {MUTED}>{l}</span><div>{v}</div>' for l, v in (
            ('Name', who), ('Org unit', two(*unit)), ('Manager', two(*PEOPLE[mgr])), ('Location', two(*loc)), ('Local Time', f'<span class="body-sm">{t}</span>')))
        cards.append(f'<article class="card"><div style="display: grid; grid-template-columns: 96px 1fr; gap: var(--spacing-4); align-items: center">{pairs}</div></article>')
    return f'''{head("People")}

      {tabs(("Directory", "Reporting relationships", "Geography"))}

      <div class="toolbar" style="margin: var(--spacing-4) 0">
        <div class="input-icon input-icon-left toolbar-search">
          {icon("i-search", "icon input-icon-glyph")}
          <input class="input" type="text" placeholder="Search by name" aria-label="Search by name" />
        </div>
        <span class="row" data-view="desktop">{ph_select("Team", "Team", 160)}
        {ph_select("Position", "Position", 160)}
        {ph_select("Location", "Location", 160)}
        {select("Active members", ("Active members", "All members"), label="Membership", width=170)}
        <button class="btn btn-icon-only btn-ghost" type="button" aria-label="Reset filters">{icon("i-reset", "btn-icon")}</button></span>
        <button class="btn btn-icon-only btn-ghost" type="button" aria-label="Filters" data-view="mobile" hidden>{icon("i-filter", "btn-icon")}</button>
      </div>

      {mobile('<div class="stack">' + "".join(cards) + '</div>')}
      <div class="table-scroll" style="max-height: none" data-view="desktop">
        <table class="table">
          <thead><tr><th>{SORTED("Name")}</th><th>Org unit</th><th>Manager</th><th>Location</th><th>Local Time</th></tr></thead>
          <tbody>{"".join(rows)}</tbody>
        </table>
      </div>
      {pager()}'''


def org_node(k, role=None):
    name, r = PEOPLE[k]
    return (f'<div class="org-node"><span class="avatar avatar-lg">{ini(k)}</span><div class="org-node-meta"><span class="org-node-name">{name}</span>'
            f'<span class="org-node-role">{role or r}</span></div></div>')


def talent_node(name, role):
    initials = ''.join(w[0] for w in name.split())
    return (f'<div class="org-node"><span class="ps-avatar-wrap"><span class="avatar avatar-md">{initials}</span><span class="ps-avatar-mark is-talent" title="Talent network member">T</span></span>'
            f'<div class="org-node-meta"><span class="org-node-name">{name}</span><span class="org-node-role">{role}</span></div></div>')


def chain(ancestors, peers, current):
    """Who someone reports to, left to right, ending in the column of people
    beside them, with that person marked."""
    link = '<span class="ps-chain-link"></span>'
    col = ''.join(f'<div class="ps-chain-item{" is-current" if k == current else ""}">{org_node(k)}</div>' for k in peers)
    return '<div class="ps-chain">' + ''.join(f'<div class="ps-chain-node">{org_node(k)}</div>{link}' for k in ancestors) + f'<div class="ps-chain-col">{col}</div></div>'


def profile():
    def f(label, value):
        return f'<div><span class="body-sm" {MUTED}>{label}</span><div>{value}</div></div>'

    def contact(ic, text):
        return (f'<div class="row" style="justify-content: space-between; flex-wrap: nowrap"><span class="row" style="min-width: 0; flex-wrap: nowrap">{icon(ic, "icon icon-16")}<a class="body-sm" href="#" style="color: var(--color-text-link); text-decoration: none; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap">{text}</a></span>'
                f'<button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="Copy">{icon("i-copy", "btn-icon")}</button></div>')
    return f'''{head("My Profile", '<a class="btn btn-secondary" href="../profile-edit/index.html" style="text-decoration: none">Edit profile</a>' + f'<button class="btn btn-icon-only btn-ghost" type="button" aria-label="More actions">{icon("i-dots-three-vertical", "btn-icon")}</button>')}

      <div class="row" style="flex-wrap: wrap; align-items: flex-start; gap: var(--spacing-6)">
        <span class="avatar avatar-2xl">CK</span>
        <div class="stack" style="flex: 1 1 140px; min-width: 0; gap: var(--spacing-2)">
          <div class="row"><h2 class="h2" style="margin: 0">Cara Keane</h2><button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="Hear the name">{icon("i-sound-on", "btn-icon")}</button></div>
          <span class="body" {MUTED}>Delivery Manager</span>
          <span class="row body-sm" {MUTED}>{icon("i-cake", "icon icon-16")}March 14</span>
        </div>
        <div class="row">{art("i-badge-culture", 40, "Culture Ambassador")}{art("i-badge-anniversary", 40, "Anniversary")}</div>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: var(--spacing-6); margin: var(--spacing-6) 0; padding: var(--spacing-6) 0; border-top: 1px solid var(--color-border); border-bottom: 1px solid var(--color-border)">
        {f("Manager", f'<a class="body" href="#" {LINK}>Lydia Kaminski</a>')}
        {f("Function", f'<a class="body" href="../team-profile/index.html" {LINK}>Operations</a>')}
        {f("Team", f'<a class="body" href="#" {LINK}>Delivery</a>')}
        {f("Business Lines", f'<div class="row">{tag("Services")}{tag("Operationalize")}</div>')}
        {f("Hire Date", '<span class="body">Dec 2, 2019</span>')}
      </div>

      <div style="display: flex; flex-wrap: wrap; gap: var(--spacing-8); margin-bottom: var(--spacing-8)">
        <div class="stack" style="flex: 0 1 220px; min-width: 0"><span class="body-sm" {MUTED}>Contacts</span>
          {contact("i-email", "cara.keane@harborsupport.com")}{contact("i-slack-color", "Cara Keane")}{contact("i-phone", "+353 1 555 0142")}</div>
        <div class="stack" style="flex: 1 1 320px; min-width: 0"><span class="body-sm" {MUTED}>About</span>
          <p class="body" style="margin: 0">I run the Delivery team in Dublin. Before that I spent eight years in customer support, which is where I learned that most problems are handoff problems.</p></div>
        <div class="stack" style="flex: 0 1 240px; min-width: 0"><span class="body-sm" {MUTED}>Location</span>
          <article class="card"><div class="row">{icon("i-pin", "icon icon-16")}<span class="body-sm">Dublin, Ireland</span></div></article></div>
      </div>

      {tabs(("Reporting Relationships", "Initiatives", "Processes", "Work History", "RoB Meetings", "Action Items", "Time Off"))}

      <h2 class="h3" style="margin: var(--spacing-6) 0 var(--spacing-1)">Reporting Relationships</h2>
      <p class="body-sm" style="margin: 0 0 var(--spacing-4); color: var(--color-text-muted)">5 people associated with Cara as Delivery Manager</p>
      {chain(("sr", "lk"), ("nr", "ck", "lh", "tl"), "ck")}'''


# --------------------------------------------------------------------- Team
UNITS = [
    ('Business Analytics', 'mt', 'Consists of 4 active Teams, with 13 members', True),
    ('Customer', 'ad', 'Consists of 4 active Subfunctions, with 169 members', True),
    ('Finance', 'og', 'Consists of 3 active Subfunctions, with 23 members', True),
    ('IT', 'el', '14 members', False),
    ('Legal', 'og', '9 members', False),
    ('Operations', 'lk', 'Consists of 2 active Subfunctions, with 47 members', True),
    ('Partnerships', 'ad', '6 members', False),
    ('People', 'ac', 'Consists of 3 active Subfunctions, with 31 members', True),
]


UNIT_KIDS = {
    'Business Analytics': [('Reporting', 'Team', 'mt', '5 members'), ('Data Engineering', 'Team', 'mt', '4 members'), ('Forecasting', 'Team', 'mt', '2 members'), ('Insights', 'Team', 'mt', '2 members')],
    'Customer': [('Customer Support', 'Subfunction', 'ad', '61 members'), ('Customer Success', 'Subfunction', 'ad', '48 members'), ('Sales', 'Subfunction', 'ad', '44 members'), ('Sales Operations', 'Subfunction', 'ad', '16 members')],
    'Finance': [('Accounting', 'Subfunction', 'og', '11 members'), ('Billing', 'Subfunction', 'og', '8 members'), ('Planning', 'Subfunction', 'og', '4 members')],
    'Operations': [('Delivery', 'Subfunction', 'ck', '29 members'), ('Quality', 'Subfunction', 'tl', '18 members')],
    'People': [('Learning & Development', 'Subfunction', 'jp', '9 members'), ('Recruiting', 'Subfunction', 'mv', '14 members'), ('People Operations', 'Subfunction', 'ac', '8 members')],
}


def team():
    rows = []

    def unit(n, kind, k, line, rid='', parent=''):
        toggle = (f'<button class="row-toggle" type="button" aria-expanded="false" aria-label="Toggle {n}" data-rows="{rid}">{icon("i-caret-right")}</button>' if rid
                  else '<span class="row-toggle-spacer"></span>')
        name = (f'<a class="body-semibold" href="../team-profile/index.html" {LINK}>{n}</a>' if n == 'Operations' else f'<a class="body-semibold" href="#" {LINK}>{n}</a>')
        hide = f' data-child-of="{parent}" hidden style="padding-left: var(--spacing-10)"' if parent else ''
        return (f'<div class="list-row"{hide}><div class="cell-title-row">{toggle}<span class="avatar avatar-sm avatar-team">{icon("i-function")}</span>'
                f'<div><p class="list-row-title">{name} {tag(kind)}</p><p class="list-row-meta">Led by <a href="#" {LINK}>{PEOPLE[k][0]}</a>, {PEOPLE[k][1]}</p>'
                f'<p class="list-row-meta">{line}</p></div></div></div>')
    for n, k, line, kids in UNITS:
        rid = 'unit-' + n.lower().replace(' ', '-').replace('&', 'and') if kids else ''
        rows.append(unit(n, 'Function', k, line, rid))
        rows += [unit(kn, kk, kp, kl, parent=rid) for kn, kk, kp, kl in UNIT_KIDS.get(n, [])]
    return f'''{head("Organizational Structure")}

      {tabs(("Organizational Units", "Divisions", "Talent Network Members", "Skills"))}

      <div style="max-width: 400px; margin: var(--spacing-4) 0">{ph_select("Select org unit", "Org unit")}</div>

      <div class="ps-striped-list ps-wtree-list">{"".join(rows)}</div>'''


def team_profile():
    return f'''{head("Team Profile")}

      <div class="row" style="align-items: flex-start; gap: var(--spacing-6)">
        <span class="avatar avatar-2xl avatar-team">{icon("i-function")}</span>
        <div class="stack" style="gap: var(--spacing-2)">
          <h2 class="h2" style="margin: 0">Operations</h2>
          <span class="body" {MUTED}>Function</span>
          <span class="body">Led by <a href="#" {LINK}>Lydia Kaminski</a></span>
        </div>
      </div>

      <div style="display: flex; flex-wrap: wrap; gap: var(--spacing-8); margin: var(--spacing-6) 0 var(--spacing-8)">
        <div class="stack" style="flex: 0 1 320px; min-width: 0"><span class="body-sm" {MUTED}>About</span>
          <p class="body" style="margin: 0">Operations runs the work customers pay for: delivery, quality and the handoffs between them. The function is measured on time to first delivery and on engagement health.</p></div>
        <div class="stack"><span class="body-sm" {MUTED}>Slack Channels</span>
          <span class="body-sm" {MUTED}>No Slack channels attached</span></div>
      </div>

      {tabs(("Org Structure", "OKRs", "Initiatives", "Processes", "Time off", "RoB Meetings"))}

      <h2 class="h3" style="margin: var(--spacing-6) 0 var(--spacing-1)">Reporting Relationships</h2>
      <p class="body-sm" style="margin: 0 0 var(--spacing-4); color: var(--color-text-muted)">5 people comprise Operations, and 6 Talents are associated with it</p>
      <div class="org-chart"><div class="org-chart-group" style="flex: 1 1 420px">
        <p class="body-sm-semibold" style="margin: 0 0 var(--spacing-3)">Operations</p>
        {org_node("lk")}
        <ul class="org-node-children"><li>{org_node("ck")}
          <ul class="org-node-children"><li>{org_node("lh")}</li><li>{org_node("tl")}</li></ul></li><li>{org_node("nr")}</li></ul>
      </div><div class="org-chart-group">
        <p class="body-sm-semibold" style="margin: 0 0 var(--spacing-3)">Talent Network Members (6)</p>
        <div class="stack" style="gap: var(--spacing-3)">{"".join(talent_node(n, r) for n, r in (("Rosa Dahl", "Product Manager"), ("Imran Suleiman", "Product Manager"), ("Greta Lund", "Designer"), ("Samir Haddad", "Developer"), ("Lina Okoye", "Sales Analyst"), ("Paolo Ferri", "Developer")))}</div>
      </div></div>'''



# ----------------------------------------------------- Batch 2: other pages
def head_sub(title, sub, actions='', below=False):
    if below:   # the line sits under the title, not beside it
        h = head(title, actions)
        k = '</h1>\n          </div>'
        assert h.count(k) == 1
        return h.replace(k, k + f'\n          <p class="body-sm" style="margin: var(--spacing-1) 0 0; color: var(--color-text-muted)">{sub}</p>')
    return head(title, actions, after_title=f'\n            <p class="page-head-subtitle">{sub}</p>')


def empty_state(ic, title, text):
    return (f'<div class="stack" style="align-items: center; text-align: center; padding: var(--spacing-12) 0; gap: var(--spacing-2)">'
            f'<span class="icon-tile">{icon(ic)}</span><p class="body-semibold" style="margin: var(--spacing-2) 0 0">{title}</p>'
            f'<p class="body-sm" style="margin: 0; color: var(--color-text-muted)">{text}</p></div>')


CHANNELS = [
    ('wc-all-things-running', '', 11, 0), ('wc-bookclub', 'Share what you are reading and join the monthly discussion.', 90, 3),
    ('wc-dealsandsteals', 'Share your best deals, buys and finds here.', 4, 0), ('wc-formula-1', 'Predictions and race weekends.', 27, 9),
    ('wc-game-nights', 'Cooperative and competitive game nights.', 21, 1), ('wc-games', 'Talk about video games and board games.', 36, 0),
    ('wc-greenthumb', 'House plant and gardening tips.', 20, 0), ('wc-history-bits', 'History in bite-sized chunks. No politics.', 7, 0),
    ('wc-home-improvements', 'Do-it-yourselfers share ideas and pictures.', 15, 0), ('wc-knit-and-crochet', '', 6, 0),
    ('wc-music-sharing', 'Share what you listen to. No judging.', 23, 0), ('wc-motorcycles', 'For riders, builders and enthusiasts.', 12, 0),
]


def watercooler():
    cards = ''.join(
        f'<article class="card"><h3 class="card-title">{n}</h3>' + (f'<p class="card-body">{d}</p>' if d else '') +
        f'<div class="row" style="gap: var(--spacing-4); margin-top: var(--spacing-3)"><span class="row body-sm">{icon("i-participants", "icon icon-16")}{m}</span>'
        f'<span class="row body-sm">{icon("i-chat", "icon icon-16")}{c}</span></div></article>' for n, d, m, c in CHANNELS)
    return f'''{head_sub("Watercooler", "Connect with team members around the world who share similar interests")}

      {tabs(("Channels", "Top Messages"))}

      <h2 class="row body-lg-semibold" style="margin: var(--spacing-6) 0 var(--spacing-4)">{icon("i-happy-emoji", "icon icon-24")}Hobbies</h2>
      <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: var(--spacing-4)">{cards}</div>'''


OOO = [('ck', ('Delivery', 'Subfunction in Operations'), ('Dublin', 'Ireland'), '12 days'), ('lh', ('Delivery', 'Subfunction in Operations'), ('Budapest', 'Hungary'), '21 days'),
       ('nr', ('Delivery', 'Subfunction in Operations'), ('Lisbon', 'Portugal'), '8 days'), ('tl', ('Delivery', 'Subfunction in Operations'), ('Malmö', 'Sweden'), '34 days')]


def time_off():
    rows = ''.join(f'<tr><td>{user(k)}</td><td>{two(*u)}</td><td>{two(*l)}</td><td><span class="body-sm">{d}</span></td></tr>' for k, u, l, d in OOO)
    cards = ''.join(
        '<article class="card"><div style="display: grid; grid-template-columns: 96px 1fr; gap: var(--spacing-4); align-items: center">' +
        ''.join(f'<span class="body-sm-semibold" {MUTED}>{lab}</span><div>{v}</div>' for lab, v in (
            ('Name', user(k)), ('Org unit', two(*u)), ('Location', two(*l)), ('OOO length', f'<span class="body-sm">{d}</span>'))) + '</div></article>'
        for k, u, l, d in OOO)
    return f'''{head("Time off")}

      {tabs(("OOO summary", "OOO details"))}

      <div class="toolbar" style="margin: var(--spacing-4) 0">
        <div class="input-icon input-icon-left toolbar-search" style="flex: 0 1 220px">
          {icon("i-search", "icon input-icon-glyph")}
          <input class="input" type="text" placeholder="Search by name" aria-label="Search by name" />
        </div>
        <span class="row" data-view="desktop">{select("Direct reports", ("Direct reports", "All reports", "Everyone"), label="People shown", width=180)}
        <div class="input-icon input-icon-left" style="width: 240px">{icon("i-calendar", "icon input-icon-glyph")}<input class="input" type="text" value="Jan 1, 2026 - Dec 31, 2026" aria-label="Date range" /></div>
        <button class="btn btn-icon-only btn-ghost" type="button" aria-label="Reset filters">{icon("i-reset", "btn-icon")}</button></span>
        <button class="btn btn-icon-only btn-ghost" type="button" aria-label="Filters" data-view="mobile" hidden>{icon("i-filter", "btn-icon")}</button>
      </div>

      {mobile('<div class="stack">' + cards + '</div>')}
      <div class="table-scroll" style="max-height: none" data-view="desktop">
        <table class="table">
          <thead><tr><th>Name {icon("i-arrow-up-minor", "icon icon-16")}</th><th>Org unit</th><th>Location</th><th>OOO length</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>'''


def recognitions():
    return f'''{head("Recognitions &amp; Badges", '<button class="btn btn-primary ps-btn-accent" type="button">Give recognition</button>')}

      {tabs(("Recognitions", "Badges"))}

      {empty_state("i-recognize", "No recognitions", "You’ll be notified when you receive a recognition.")}'''


PENDING_FB = [('ad', 'Peer feedback', 'Sep 11, 2026'), ('mt', 'Peer request', 'Apr 12, 2026')]


def peer_feedback():
    acts = (f'<div class="cell-actions"><a class="body-sm" href="#" {LINK}>Skip</a>'
            '<button class="btn btn-secondary btn-xs" type="button">Give Feedback</button></div>')
    rows = ''.join(f'<tr><td>{user(k)}</td><td>{tag(r)}</td><td><span class="body-sm">{d}</span></td><td>{acts}</td></tr>' for k, r, d in PENDING_FB)
    cards = ''.join(f'<article class="card"><div class="stack" style="gap: var(--spacing-3)">{user(k)}<div class="row">{tag(r)}<span class="body-sm">{d}</span></div>'
                    f'<div class="row row-end"><a class="body-sm" href="#" {LINK}>Skip</a><button class="btn btn-secondary btn-xs" type="button">Give Feedback</button></div></div></article>'
                    for k, r, d in PENDING_FB)
    actions = '<button class="btn btn-secondary" type="button">Request feedback</button>\n          <button class="btn btn-primary" type="button">Give feedback</button>'
    return f'''{head_sub("Peer Feedback", "Sharing and receiving feedback across all levels promotes growth, alignment, and stronger teamwork.", actions, below=True)}

      {tabs(("Pending (2)", "Received", "Given"))}

      <div class="toolbar" style="margin: var(--spacing-4) 0">
        <div class="input-icon input-icon-left toolbar-search" style="flex: 1 1 0">
          {icon("i-search", "icon input-icon-glyph")}
          <input class="input" type="text" placeholder="Receiver" aria-label="Receiver" />
        </div>
        <span class="row" data-view="desktop" style="flex: 2 1 0; flex-wrap: nowrap"><div style="flex: 1 1 0; min-width: 0">{ph_select("Relationship", "Relationship")}</div>
        <div class="input-icon input-icon-left" style="flex: 1 1 0; min-width: 0">{icon("i-calendar", "icon input-icon-glyph")}<input class="input" type="text" placeholder="Date requested" aria-label="Date requested" /></div></span>
        <button class="btn btn-icon-only btn-ghost" type="button" aria-label="Filters" data-view="mobile" hidden>{icon("i-filter", "btn-icon")}</button>
      </div>

      {mobile('<div class="stack">' + cards + '</div>')}
      <div class="table-scroll" style="max-height: none" data-view="desktop">
        <table class="table">
          <thead><tr><th>Feedback receiver</th><th>Relationship {icon("i-help", "icon icon-16")}</th><th>Date Received</th><th style="text-align: right">Actions</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>'''


def self_review():
    def q(text):
        return (f'<div><p class="body-sm" style="margin: 0 0 var(--spacing-2)">{text}</p>'
                f'<div class="card"><span class="body" {MUTED}>—</span></div></div>')
    return f'''{head("Self-review")}

      <div class="stack" style="max-width: 800px; margin: 0 auto; gap: var(--spacing-6)">
        <div class="row" style="justify-content: space-between">{user("ck")}<button class="btn btn-secondary" type="button">Edit</button></div>
        <article class="card"><div class="stack"><h2 class="h4" style="margin: 0">Achievements and opportunities</h2>
          {q("Please highlight your achievements and wins since your last self review.")}
          {q("Please highlight your challenges and development opportunities since your last self review.")}</div></article>
        <article class="card"><div class="stack"><h2 class="h4" style="margin: 0">Career goals</h2>
          {q("What does career growth mean to you?")}
          {q("What type of development opportunities would you like to see in order to progress with your growth goals?")}
          {q("How much time are you able to spend on skill development each month?")}</div></article>
      </div>'''


def profile_edit():
    def txt(label, ph, value=''):
        return f'<label class="field" style="flex: 1 1 220px"><span class="field-label">{label}</span><input class="input" type="text" placeholder="{ph}" value="{value}" /></label>'

    def sel(label, control):
        return f'<div class="field" style="flex: 1 1 220px"><span class="field-label">{label}</span>{control}</div>'
    return f'''{head("Edit Profile")}

      {tabs(("Personal", "Work", "Contacts"))}

      <div style="display: flex; flex-wrap: wrap; gap: var(--spacing-8); margin-top: var(--spacing-6)">
        <div class="stack" style="flex: 3 1 420px; min-width: 0; max-width: 640px">
          <div class="row" style="flex-wrap: wrap; align-items: flex-start; gap: var(--spacing-4)">{txt("First name", "First name", "Cara")}{txt("Last name", "Last name", "Keane")}</div>
          <div class="row" style="flex-wrap: wrap; align-items: flex-start; gap: var(--spacing-4)">{txt("Preferred first name (optional)", "First name")}<span style="flex: 1 1 220px"></span></div>
          <div class="row" style="flex-wrap: wrap; align-items: flex-start; gap: var(--spacing-4)">
            {sel("Location", select("Dublin, Ireland", label="Location") + '<span class="field-hint">Local time: 13:22</span>')}
            {sel("Working hours " + icon("i-help", "icon icon-16"), '<div class="row">' + "".join(f'<div class="input-icon input-icon-right" style="flex: 1 1 0; min-width: 0">{icon("i-time", "icon input-icon-glyph")}<input class="input" type="text" value="{v}" aria-label="{l}" /></div>' for v, l in (("09:00", "Working hours start"), ("17:00", "Working hours end"))) + '</div>')}
          </div>
          <div class="row" style="flex-wrap: wrap; align-items: flex-end; gap: var(--spacing-4)">
            {sel("Date of Birth (optional)", '<div class="row" style="flex-wrap: nowrap">' + select("March", label="Month of birth", width=150) + select("14", label="Day of birth", width=110) + '</div>')}
            <label class="checkbox" style="flex: 1 1 220px"><input type="checkbox" class="checkbox-input" checked /><span class="checkbox-box">{icon("i-check", "checkbox-mark")}</span><span class="checkbox-label">Show in my Operationalize profile {icon("i-help", "icon icon-16")}</span></label>
          </div>
          <label class="field"><span class="field-label">About Cara (optional)</span><textarea class="input" rows="8" placeholder="Share a bit about your background, interests, and what drives you…"></textarea></label>
        </div>
        <div class="stack" style="flex: 1 1 160px">
          <span class="field-label">Avatar (optional)</span>
          <span class="avatar avatar-2xl">CK</span>
        </div>
      </div>

      <div class="row" style="margin-top: var(--spacing-6)">
        <a class="btn btn-secondary" href="../profile/index.html" style="text-decoration: none">Cancel</a>
        <button class="btn btn-primary" type="button">Save Changes</button>
      </div>'''


PAUSED = [('06 Feb, 10:02 PM', '[Quarterly] Operations business review', 'lk'), ('03 Aug, 7:01 PM', '[RoB] Vendor Management', 'lk'),
          ('30 Jul, 6:24 PM', '[RoB] Partner certification', 'ad'), ('06 Jul, 2:37 PM', '[RoB] Northwind Hire daily', 'km'),
          ('09 Mar, 3:54 PM', '[RoB] Learning programs', 'jp'), ('20 Jan, 11:18 PM', '[RoB] Legal Operations', 'og')]


def paused_meetings():
    rows = ''.join(f'<tr><td><span class="body-sm">{d}</span></td><td><a class="body-sm" href="#" {LINK}>{n}</a></td><td>{user(k)}</td></tr>' for d, n, k in PAUSED)
    cards = ''.join(f'<article class="card"><div class="stack" style="gap: var(--spacing-3)"><a class="body-semibold" href="#" {LINK}>{n}</a>'
                    f'<span class="body-sm" {MUTED}>Last meeting: {d}</span>{user(k)}</div></article>' for d, n, k in PAUSED)
    return f'''{head("View Paused Meetings")}

      {mobile('<div class="stack">' + cards + '</div>')}
      <div class="table-scroll" style="max-height: none" data-view="desktop">
        <table class="table">
          <thead><tr><th>Last meeting</th><th>Name</th><th>Accountability</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>'''


def not_found():
    return f'''      <div class="stack" style="align-items: center; justify-content: center; text-align: center; min-height: 60vh; gap: var(--spacing-2)">
        {art("i-art-not-found", 112, "Page not found")}
        <h1 class="h3" style="margin: var(--spacing-2) 0 0">404</h1>
        <p class="body-sm" style="margin: 0; color: var(--color-text-muted)">Page not found</p>
        <a class="btn btn-primary ps-btn-accent" href="../dashboard/index.html" style="text-decoration: none; margin-top: var(--spacing-3)">Go back to dashboard</a>
      </div>'''


# ------------------------------------------------------------- Batch 3
def talent_profile():
    def f(label, value):
        return f'<div><span class="body-sm" {MUTED}>{label}</span><div>{value}</div></div>'
    work = [('Onboarding in one week', 'Initiative', 0, 'Execution', 'blue', ('Dec 01 • 4:00pm', 'Every week on Tuesday'), ''),
            ('Kick-off checklist', 'Project', 1, 'Execution', 'blue', ('Dec 01 • 5:30pm', 'Every week on Tuesday'), ''),
            ('First-week survey', 'Sub-project', 2, 'Complete', 'positive', '', 'R')]
    none = '<span class="row body-sm">' + icon('i-warning', 'icon icon-16') + 'No meeting connected</span>'
    rows = ''.join(
        f'<tr><td><div style="padding-left: calc({lvl} * var(--spacing-6))"><span class="cell-title">{n}</span><div>{tag(kind)}</div></div></td><td>{tag(st, c)}</td>'
        f'<td>{rob_cell(r) if r else none}</td>'
        f'<td>{tag(role, "positive") if role else ""}</td><td>{raci_btn()}</td></tr>' for n, kind, lvl, st, c, r, role in work)
    cards = ''.join(work_card(n, tag(kind) + tag(st, c), 'sr', 'Operations') for n, kind, lvl, st, c, r, role in work)
    return f'''{head("Talent Network Member Profile")}

      <div class="alert alert-warning" style="margin-bottom: var(--spacing-6)">{icon("i-warning", "icon alert-icon")}<p class="alert-message">Not a Core Team member: Please reach out to Sofia Romano for more details</p></div>

      <div class="row" style="flex-wrap: wrap; align-items: flex-start; gap: var(--spacing-6)">
        <span class="ps-avatar-wrap"><span class="avatar avatar-2xl">RD</span><span class="ps-avatar-mark is-talent" title="Talent network member">T</span></span>
        <div class="stack" style="flex: 1 1 240px; min-width: 0">
          <h2 class="h2" style="margin: 0">Rosa Dahl</h2>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, max-content)); gap: var(--spacing-6)">
            {f("Manager", f'<a class="body" href="#" {LINK}>Sofia Romano</a>')}
            {f("Function", f'<a class="body" href="../team-profile/index.html" {LINK}>Operations</a>')}
            {f("Team", f'<a class="body" href="#" {LINK}>Delivery</a>')}
            {f("Hire Date", '<span class="body">Jun 1, 2026</span>')}
          </div>
        </div>
      </div>

      <div class="stack" style="margin: var(--spacing-6) 0; gap: var(--spacing-2)"><span class="body-sm" {MUTED}>Contacts</span>
        <div class="row" style="flex-wrap: wrap; gap: var(--spacing-6)">
          <span class="row">{icon("i-email", "icon icon-16")}<a class="body-sm" href="#" {LINK}>rosa.dahl@harborsupport.com</a></span>
          <span class="row">{icon("i-slack-color", "icon icon-16")}<a class="body-sm" href="#" {LINK}>Rosa Dahl</a></span>
        </div></div>

      {tabs(("Initiatives", "Processes"))}

      {mobile('<div class="stack" style="margin-top: var(--spacing-4)">' + cards + '</div>')}
      <div class="table-scroll" style="max-height: none; margin-top: var(--spacing-4)" data-view="desktop">
        <table class="table">
          <thead><tr><th>Name</th><th>Status</th><th>RoB Meeting</th><th>Roles</th><th style="text-align: right">Actions</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>'''


def public_profile_edit():
    def txt(label):
        return f'<label class="field" style="flex: 1 1 220px"><span class="field-label">{label}</span><input class="input" type="text" /></label>'

    def area(label):
        return f'<label class="field"><span class="field-label">{label}</span><textarea class="input" rows="6"></textarea></label>'
    actions = ('<a class="btn btn-secondary" href="../profile/index.html" style="text-decoration: none">Cancel</a>\n          '
               '<button class="btn btn-primary ps-btn-accent" type="button">Save changes</button>')
    wrap = 'class="row" style="flex-wrap: wrap; align-items: flex-start; gap: var(--spacing-4)"'
    return f'''{head("Edit public profile for Cara", actions)}

      <div style="display: flex; flex-wrap: wrap; gap: var(--spacing-8)">
        <div class="stack" style="flex: 3 1 420px; min-width: 0; max-width: 720px">
          <div {wrap}>{txt("Name (optional)")}{txt("Job title (optional)")}</div>
          <div {wrap}>{txt("Previously at (optional)")}
            <div class="field" style="flex: 1 1 220px"><span class="field-label">Career start year (optional)</span>{ph_select("Select a year", "Career start year")}</div></div>
          {area("Bio (optional)")}
          {area("Career highlight (optional)")}
          {area("Achievements (optional)")}
          <div {wrap}>{txt("External URL (optional)")}{txt("Phone (optional)")}</div>
          <div {wrap}>{txt("Country (optional)")}{txt("City (optional)")}</div>
        </div>
        <div class="stack" style="flex: 1 1 160px">
          <span class="field-label">Profile image (optional)</span>
          <span class="avatar avatar-2xl">CK</span>
        </div>
      </div>'''


# ------------------------------------------------ Tabs, drawers and modals
import re as _re


def with_tabs(html, group, panels, suffix=''):
    """Make a screen's tab strip switch panels. Everything after the strip is
    the first tab; `panels` are the others, in order. build.py's script does
    the switching and reads #tab-N from the address."""
    if suffix:
        assert html.rstrip().endswith(suffix.strip()), group
        html = html.rstrip()[:-len(suffix.strip())]
    m = _re.search(r'<div class="tabs" role="tablist">.*?</div>', html, flags=_re.S)
    strip = m.group(0).replace('<div class="tabs" role="tablist">', f'<div class="tabs" role="tablist" data-tabs="{group}">')
    n = [0]

    def num(mm):
        n[0] += 1
        return f'<button data-tab="{n[0] - 1}" class="tab'
    strip = _re.sub(r'<button class="tab', num, strip)
    assert n[0] == len(panels) + 1, (group, n[0], len(panels))
    out = html[:m.start()] + strip + f'\n<div data-panel="{group}:0">' + html[m.end():] + '</div>'
    for i, p in enumerate(panels, 1):
        out += f'\n<div data-panel="{group}:{i}" hidden style="margin-top: var(--spacing-6)">{p}</div>'
    return out + ('\n' + suffix if suffix else '')


def SORTED(label):
    return f'<span class="row" style="gap: var(--spacing-1)">{label}{icon("i-arrow-up-minor", "icon icon-16")}</span>'


def table(heads, rows):
    th = ''.join(f'<th>{h}</th>' for h in heads)
    return f'<div class="table-scroll" style="max-height: none"><table class="table"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>'


def sub(text):
    return f'<span class="body-sm">{text}</span>'


def work_rows(work):
    none = '<span class="row body-sm">' + icon('i-warning', 'icon icon-16') + 'No meeting connected</span>'
    return ''.join(
        f'<tr><td><div style="padding-left: calc({lvl} * var(--spacing-6))"><span class="cell-title">{n}</span><div>{tag(kind)}</div></div></td><td>{tag(st, c)}</td>'
        f'<td>{rob_cell(r) if r else none}</td><td>{tag(role, "positive") if role else ""}</td><td>{raci_btn()}</td></tr>' for n, kind, lvl, st, c, r, role in work)


WORK = [('Onboarding in one week', 'Initiative', 0, 'Execution', 'blue', ('Nov 30 • 10:00am', 'Every week on Monday'), ''),
        ('Kick-off checklist', 'Project', 1, 'Execution', 'blue', ('Nov 30 • 10:00am', 'Every week on Monday'), 'R'),
        ('Delivery health reviews', 'Initiative', 0, 'Execution', 'blue', ('Dec 03 • 2:00pm', 'Every 2 weeks on Thursday'), 'C')]
WORK_HEADS = ('Name', 'Status', 'RoB Meeting', 'Roles', '<span style="display: block; text-align: right">Actions</span>')


def week_grid(events=()):
    hours = ['9:00am', '10:00am', '11:00am', '12:00pm', '1:00pm', '2:00pm', '3:00pm', '4:00pm', '5:00pm']
    ev = dict(events)
    rows = ''
    for h in hours:
        cells = ''.join('<td>' + (f'<div class="list-row"><div><p class="list-row-title">{ev[(d, h)][0]}</p><p class="list-row-meta">{ev[(d, h)][1]}</p></div></div>' if (d, h) in ev else '') + '</td>'
                        for d in range(5))
        rows += f'<tr><td style="width: calc(2 * var(--spacing-10))"><span class="body-xs" {MUTED}>{h}</span></td>{cells}</tr>'
    heads = ''.join(f'<th>{d} <span class="body-sm">{n}</span></th>' for d, n in (('Monday', 23), ('Tuesday', 24), ('Wednesday', 25), ('Thursday', 26), ('Friday', 27)))
    return (f'<div class="table-scroll" style="max-height: none"><table class="table" style="table-layout: fixed; min-width: 880px"><thead><tr><th><span class="body-xs">GMT+1</span></th>{heads}</tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


def radios(name, options, on=0):
    return ''.join(f'<label class="radio"><input type="radio" class="radio-input" name="{name}"{" checked" if i == on else ""} /><span class="radio-circle"></span><span class="radio-label">{o}</span></label>'
                   for i, o in enumerate(options))


def period_nav(label, sub_label=''):
    below = f'<span class="body-xs" style="display: block; color: var(--color-text-muted)">{sub_label}</span>' if sub_label else ''
    return (f'<div class="row"><button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="Previous">{icon("i-chevron-left", "btn-icon")}</button>'
            f'<span class="body-semibold" style="text-align: center">{label}{below}</span>'
            f'<button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="Next">{icon("i-chevron-right", "btn-icon")}</button><button class="btn btn-secondary" type="button">Today</button></div>')


def rob_tab(who, count, show_label, show_opts, events):
    return f'''<h2 class="h3" style="margin: 0 0 var(--spacing-1)">RoB Meetings</h2>
      <p class="body-sm" style="margin: 0 0 var(--spacing-4); color: var(--color-text-muted)">{who}</p>
      <div class="toolbar" style="margin-bottom: var(--spacing-4)">
        {period_nav("Nov 23-29", count)}
        <span class="toolbar-spacer"></span>
        <span class="row" role="radiogroup" aria-label="{show_label}"><span class="body-sm-semibold">{show_label}</span>{radios("rob-" + show_label.lower(), show_opts)}</span>
        {segmented(("Schedule", "Week", "Month", "List"), 1, "Calendar view")}
      </div>
      {week_grid(events)}'''


def month_table(title, first, days, marks=()):
    cells, rows = [''] * first + [str(d) for d in range(1, days + 1)], ''
    while len(cells) % 7:
        cells.append('')
    for i in range(0, len(cells), 7):
        rows += '<tr>' + ''.join('<td>' + ((f'<span class="count-badge">{c}</span>' if c and int(c) in marks else f'<span class="body-sm">{c}</span>')) + '</td>' for c in cells[i:i + 7]) + '</tr>'
    return (f'<div style="flex: 1 1 320px; min-width: 0"><h3 class="body-semibold" style="margin: 0 0 var(--spacing-2)">{title}</h3>'
            + table(('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'), rows) + '</div>')


# Profile
def profile_panels():
    initiatives_p = table(WORK_HEADS, work_rows(WORK))
    processes_p = empty_state('i-cpu-2', 'You don’t own any Processes', 'No Processes yet')
    hist = ''.join(f'<div class="ps-timeline-item{" is-current" if i == 0 else ""}"><div><p class="body-semibold" style="margin: 0">{t}</p>'
                   f'<p class="row body-sm" style="margin: var(--spacing-1) 0 0">{icon("i-org-unit", "icon icon-16")}{u}</p></div><span class="body-sm" style="text-align: right; color: var(--color-text-muted)">{d}</span></div>'
                   for i, (t, u, d) in enumerate((
        ('Delivery Manager', 'Delivery Subfunction in Operations', 'Apr 2024 -<br />Present'), ('Senior Project Coordinator', 'Delivery Subfunction in Operations', 'Jul 2022 -<br />Apr 2024'),
        ('Project Coordinator', 'Customer Support Team in Customer', 'Dec 2019 -<br />Jul 2022'))))
    work_history = (f'<h2 class="h3" style="margin: 0 0 var(--spacing-1)">Work History</h2><p class="body-sm" style="margin: 0 0 var(--spacing-4); color: var(--color-text-muted)">Cara has been working here for 7 years.</p>'
                    f'<div class="row" style="flex-wrap: wrap; gap: var(--spacing-4); margin-bottom: var(--spacing-4); padding: var(--spacing-3) var(--spacing-4); border: 1px solid var(--color-border); border-radius: var(--radius-sm); max-width: 720px">'
                    f'<span class="body-sm-semibold">Type of Change</span>{check("Position &amp; Team Change", True)}{check("Associated Membership")}{check("Business Ownership")}</div>'
                    f'<div class="ps-timeline" style="max-width: 720px">{hist}</div>')
    rob = rob_tab('Cara attends 4 RoB Meetings', '4 meetings', 'Role', ('All', 'Owner', 'Attendee'),
                  [((0, '10:00am'), ('[RoB] Onboarding in one week', 'Operations')), ((2, '1:00pm'), ('[RoB] Refund requests', 'Delivery')),
                   ((0, '3:00pm'), ('Delivery All Hands', 'Delivery')), ((3, '4:00pm'), ('[RoB] Partner marketing sites', 'Partnerships'))])
    actions = (f'<h2 class="body-semibold row" style="margin: 0 0 var(--spacing-3)">[RoB] Onboarding in one week · August 3, 2026'
               f'<a class="btn btn-icon-only btn-ghost btn-xs" href="../rob-meeting-view/index.html" aria-label="Open the meeting">{icon("i-external-link", "btn-icon")}</a></h2>'
               f'<div class="ps-action is-done"><div class="row"><span class="ps-action-status"><span class="ps-action-dot"></span>Done</span>'
               f'<span class="row" style="gap: var(--spacing-1)"><span class="avatar avatar-xs">{ini("ck")}</span><span class="body-xs-semibold">Cara Keane</span></span></div>'
               f'<p class="ps-action-text">Draft the kick-off checklist for new customers</p></div>')
    side = lambda t, body: f'<div><h3 class="body-semibold" style="margin: 0 0 var(--spacing-2)">{t}</h3>{body}</div>'
    time_off_p = (f'<h2 class="h3" style="margin: 0 0 var(--spacing-4)">Time Off</h2><div style="margin-bottom: var(--spacing-6)">{period_nav("Nov 2026")}</div>'
                  f'<div style="display: flex; flex-wrap: wrap; gap: var(--spacing-8)">{month_table("November 2026", 6, 30, (25,))}{month_table("December 2026", 1, 31, tuple(range(21, 32)))}'
                  f'<div class="stack" style="flex: 1 1 240px; min-width: 0; gap: var(--spacing-6)">{side("Upcoming Time Off", sub("Dec 21, 2026 - Dec 31, 2026"))}'
                  f'{side("Who Is Covering", sub("No one is covering this time off"))}{side("Total Time Off", sub("9 days taken in 2026"))}</div></div>')
    return [initiatives_p, processes_p, work_history, rob, actions, time_off_p]


# Team profile
def team_profile_panels():
    def show(name):
        return (f'<div class="row" style="flex-wrap: wrap; gap: var(--spacing-4); margin-bottom: var(--spacing-4); padding: var(--spacing-3) var(--spacing-4); border: 1px solid var(--color-border); border-radius: var(--radius-sm)">'
                f'<span class="body-sm-semibold">Show</span>{radios(name, ("All", "Direct Members Only", "Associated Members Only"))}</div>')
    okrs_p = (f'<p class="body" style="margin: 0 0 var(--spacing-4)">OKRs owned by Operations are managed on the OKRs page.</p><div class="row">'
              f'<a class="btn btn-secondary" href="../okrs/index.html#tab-2" style="text-decoration: none">Open Function Annual OKRs</a>'
              f'<a class="btn btn-secondary" href="../okrs/index.html#tab-3" style="text-decoration: none">Open Function Quarterly OKRs</a></div>')
    days = list(range(23, 31)) + list(range(1, 7))
    heads = ['Name, Position'] + [f'{d:02d}' for d in days]
    def ooo(k, off):
        return f'<tr><td>{user(k)}</td>' + ''.join('<td>' + (tag('O', 'warning') if d in off else '') + '</td>' for d in days) + '</tr>'
    time_off_p = (f'<div class="row" style="margin-bottom: var(--spacing-4)"><span class="body-semibold">Nov 2026</span><button class="btn btn-secondary" type="button">Today</button></div>'
                  + table(heads, ooo('lk', ()) + ooo('ck', (26, 27)) + ooo('lh', ()) + ooo('tl', (30, 1, 2))))
    rob = rob_tab('', 'No meetings', 'Show', ('All', 'Function', 'Subfunction'), [])
    return [okrs_p, show('tp-show-ini') + table(WORK_HEADS, work_rows(WORK)), show('tp-show-proc') + empty_state('i-cpu-2', 'Operations doesn’t own any Processes', 'No Processes yet'), time_off_p, rob]


# People
def people_panels():
    tree = (f'<div style="max-width: 280px; margin-bottom: var(--spacing-4)"><div class="input-icon input-icon-left">{icon("i-search", "icon input-icon-glyph")}<input class="input" type="text" value="Cara Keane" aria-label="Search people" /></div></div>'
            f'<div class="org-chart"><div class="org-chart-group">{org_node("ho")}<ul class="org-node-children"><li>{org_node("sr")}<ul class="org-node-children"><li>{org_node("lk")}'
            f'<ul class="org-node-children"><li>{org_node("ck")}</li><li>{org_node("nr")}</li></ul></li><li>{org_node("el")}</li></ul></li><li>{org_node("ac")}</li><li>{org_node("ad")}</li></ul></div></div>')
    geo = (f'<div class="toolbar" style="margin-bottom: var(--spacing-4)"><div class="input-icon input-icon-left toolbar-search">{icon("i-search", "icon input-icon-glyph")}<input class="input" type="text" placeholder="Search by name" aria-label="Search by name" /></div>'
           f'<span class="row" data-view="desktop">{ph_select("Team", "Team", 160)}{ph_select("Position", "Position", 160)}{ph_select("Location", "Location", 160)}{select("Active members", label="Membership", width=170)}</span></div>'
           f'<article class="card" style="min-height: 420px"><div class="stack" style="align-items: center; justify-content: center; min-height: 380px; gap: var(--spacing-2)">{icon("i-globe", "icon icon-24")}'
           f'<p class="body-semibold" style="margin: 0">Map of where people are</p><p class="body-sm" style="margin: 0; color: var(--color-text-muted)">731 results shown (731 active members in total)</p></div></article>')
    return [tree, geo]


# Team
def team_panels():
    def unit(n, kind, owner, line):
        own = f'<a href="#" {LINK}>{owner}</a>' if owner else f'<span {MUTED}>Unassigned</span>'
        return (f'<div class="list-row"><div class="cell-title-row"><button class="row-toggle" type="button" aria-expanded="false" aria-label="Toggle children">{icon("i-caret-right")}</button>'
                f'<span class="avatar avatar-sm avatar-team">{icon("i-group-3")}</span><div><p class="list-row-title"><a class="body-semibold" href="#" {LINK}>{n}</a> {tag(kind)}</p>'
                f'<p class="list-row-meta">Owner {own}</p><p class="list-row-meta">{line}</p></div></div></div>')
    divisions = (f'<div class="toolbar" style="margin-bottom: var(--spacing-6)"><div class="input-icon input-icon-left toolbar-search">{icon("i-search", "icon input-icon-glyph")}<input class="input" type="text" placeholder="Search for a division" aria-label="Search for a division" /></div>'
                 f'<label class="checkbox"><input type="checkbox" class="checkbox-input" /><span class="checkbox-box">{icon("i-check", "checkbox-mark")}</span><span class="checkbox-label">Show archived</span></label>'
                 f'<span class="toolbar-spacer"></span>{select("Structure View", ("Structure View", "Table View"), label="View", width=170)}</div>'
                 f'<h2 class="body-lg-semibold" style="margin: 0 0 var(--spacing-3)">Categories &amp; Practices</h2><div class="ps-striped-list">'
                 + unit('Consulting', 'Category', 'Lydia Kaminski', 'Consists of 4 Practices ● Owns 1 Vertical and 2 Specializations')
                 + unit('Technology Services', 'Category', 'Elias Lowe', 'Consists of 6 Practices ● Owns 3 Verticals and 5 Specializations')
                 + unit('Marketing Agency', 'Category', 'Adele Delacroix', 'Consists of 7 Practices ● Owns 1 Vertical')
                 + f'</div><h2 class="body-lg-semibold" style="margin: var(--spacing-8) 0 var(--spacing-3)">Verticals</h2><div class="ps-striped-list">'
                 + unit('Consultants', 'Vertical', '', 'Consists of 4 Specializations ● Owned By Consulting')
                 + unit('Developer', 'Vertical', '', 'Consists of 13 Specializations ● Owned By Technology Services')
                 + unit('Design', 'Vertical', '', 'Consists of 2 Specializations') + '</div>')
    def t(k, unit_, mgr, loc, time):
        return f'<tr><td>{user_marked(k, "talent")}</td><td>{two(*unit_)}</td><td>{user(mgr)}</td><td>{sub("-")}</td><td>{two(*loc)}</td><td>{sub(time)}</td></tr>'
    talents = (f'<div class="toolbar" style="margin-bottom: var(--spacing-4)"><button class="btn btn-secondary" type="button">{icon("i-filter", "btn-icon")}Filters</button></div>'
               + table((SORTED('Name'), 'Associated Org Units', 'Manager', 'Division', 'Location', 'Local Time'),
                       t('nr', ('Delivery', 'Subfunction in Operations'), 'sr', ('Lisbon', 'Portugal'), '09:17') + t('km', ('Northwind Hire', 'Team in Recruiting'), 'mv', ('Accra', 'Ghana'), '09:17')
                       + t('tl', ('Delivery', 'Subfunction in Operations'), 'lk', ('Malmö', 'Sweden'), '10:17')))
    skills_rows = ''.join(f'<tr><td><a class="body-sm" href="#" {LINK}>{n}</a></td><td>{sub(o)}</td><td>{sub(c)}</td><td>{sub(p)}</td><td>{sub(v)}</td></tr>' for n, o, c, p, v in (
        ('2D Animation', '', '', '', 'Design'), ('3D Modeling', '', '', '', 'Design'), ('Accessibility Testing', '', 'Technology Services', '', 'Developer'),
        ('Brand Strategy', '', 'Marketing Agency', '', ''), ('Business Valuation', '', 'Consulting', '', 'Consultants'), ('Cloud Migration', '', 'Technology Services', '', 'Developer'),
        ('Design Systems', '', '', '', 'Design'), ('Financial Modeling', '', 'Consulting', '', 'Consultants')))
    def fi(ph):
        return f'<input class="input" type="text" placeholder="{ph}" aria-label="{ph}" style="width: 180px" />'
    skills = (f'<div class="toolbar" style="margin-bottom: var(--spacing-4)">{fi("Skill Name")}{fi("Owner")}{ph_select("Category", "Category", 180)}{ph_select("Practice", "Practice", 180)}{ph_select("Vertical", "Vertical", 180)}'
              f'<button class="btn btn-icon-only btn-ghost" type="button" aria-label="Reset filters">{icon("i-reset", "btn-icon")}</button></div>'
              + table(('Skill Name', 'Owner', 'Category', 'Practice', 'Vertical'), skills_rows))
    return [divisions, talents, skills]


def okr_panels():
    def cards(items):
        out = ''
        for name, st, kind, krs in items:
            rows = ''.join(f'<div class="list-row" style="flex-wrap: wrap"><div><p class="list-row-title">{kr}</p></div><span class="body-sm-semibold">{p}%</span></div>' for kr, p in krs)
            out += f'<article class="card"><div class="row"><h3 class="body-lg-semibold" style="margin: 0">{name}</h3>{tag(st, kind)}</div>{rows}</article>'
        return f'<div class="stack">{out}</div>'
    return [cards([('Customers start in a week', 'Active', 'positive', [('Median time to first delivery is 7 days', 64)])]),
            cards([('Operations: one handoff, not three', 'Active', 'positive', [('Contract to workspace handoff is automatic', 50), ('Kick-off checklist used on every engagement', 80)])]),
            cards([('Operations Q4: checklist live', 'Active', 'positive', [('Checklist in use on 20 engagements', 45)]), ('IT Q4: self-serve setup', 'Draft', 'light', [('Billing setup without a call', 10)])]),
            empty_state('i-okr', 'No OKRs found', 'No OKRs have been created for this level and period yet.'),
            cards([('Shared: time to first delivery', 'Active', 'positive', [('Median time to first delivery is 7 days', 64)])])]


def activity_log():
    items = ''.join(f'<div class="list-row"><div><p class="list-row-meta">{d}</p><p class="list-row-title">{t}</p></div></div>' for d, t in (
        ('Nov 24, 2026', 'Status was changed from Definition to Execution by Sofia Romano on Nov 24, 2026, 4:10 PM'),
        ('Jul 3, 2026', 'Project Manager was added by Sofia Romano on Jul 3, 2026, 9:12 AM'),
        ('Jul 1, 2026', 'Accountable owner was added by Sofia Romano on Jul 1, 2026, 2:40 PM'),
        ('Jul 1, 2026', 'Initiative was created by Sofia Romano on Jul 1, 2026, 2:38 PM')))
    return f'<div style="padding: 0 var(--spacing-10) var(--spacing-10)"><h2 class="h4" {RULE}>Timeline</h2>{items}</div>'


def ooo_details():
    rows = ''.join(f'<tr><td>{user(k)}</td><td>{sub(t)}</td><td>{two(*u)}</td><td>{sub(d)}</td><td>{sub(n)}</td><td>{tag(st, "positive")}</td></tr>' for k, t, u, d, n, st in (
        ('ck', 'Vacation', ('Delivery', 'Operations'), 'Jan 1, 2026 - Jan 1, 2026', '1 day', 'Approved'),
        ('ck', 'Vacation', ('Delivery', 'Operations'), 'Feb 23, 2026 - Mar 2, 2026', '6 days', 'Approved'),
        ('lh', 'Sick leave', ('Delivery', 'Operations'), 'Apr 7, 2026 - Apr 8, 2026', '2 days', 'Approved'),
        ('tl', 'Vacation', ('Delivery', 'Operations'), 'Jul 13, 2026 - Jul 31, 2026', '15 days', 'Approved')))
    bar = (f'<div class="toolbar" style="margin-bottom: var(--spacing-4)"><div class="input-icon input-icon-left toolbar-search" style="flex: 0 1 220px">{icon("i-search", "icon input-icon-glyph")}<input class="input" type="text" placeholder="Search by name" aria-label="Search by name" /></div>'
           f'<span class="row" data-view="desktop">{select("Direct reports", ("Direct reports", "All reports", "Everyone"), label="People shown", width=170)}'
           f'<div class="input-icon input-icon-left" style="width: 230px">{icon("i-calendar", "icon input-icon-glyph")}<input class="input" type="text" value="Jan 1, 2026 - Dec 31, 2026" aria-label="Date range" /></div>'
           f'{ph_select("OOO type", "OOO type", 170)}{select("Approved, Pending", ("Approved", "Pending", "Rejected", "Cancelled"), label="Status", width=190)}'
           f'<button class="btn btn-icon-only btn-ghost" type="button" aria-label="Reset filters">{icon("i-reset", "btn-icon")}</button></span></div>')
    return bar + table(('Name', 'OOO type', 'Org unit', SORTED('OOO dates'), 'OOO length', 'Status'), rows)


def badges():
    cards = ''.join(f'<article class="card"><div class="stack" style="align-items: center; text-align: center; gap: var(--spacing-2)">{art(ic, 72, n)}'
                    f'<h3 class="card-title">{n}</h3><p class="card-body">{d}</p></div></article>' for ic, n, d in (
        ('i-badge-ambitious', 'Ambitious', 'You set your sights on extraordinary outcomes and push estimates and expectations.'), ('i-badge-anniversary', 'Anniversary', 'Awarded for years of service'),
        ('i-badge-challenging', 'Challenging', 'You question and challenge ideas, from policy to product decisions.'), ('i-badge-culture', 'Culture Ambassador', 'Recognized for being a Culture Ambassador'),
        ('i-badge-driven', 'Driven', 'You are driven to achieve.'), ('i-badge-helpful', 'Helpful', 'You are always available to help.'),
        ('i-badge-hipo', 'HiPo', 'Recognized for graduating from the high-potential program'), ('i-badge-inspiring', 'Inspiring', 'You care deeply about what you do.')))
    return f'<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: var(--spacing-4)">{cards}</div>'


def feedback_panels():
    view = f'<div class="cell-actions"><a class="body-sm" href="#" {LINK}>View</a></div>'
    rec = ''.join(f'<tr><td>{user(k)}</td><td><div class="row">{"".join(tag(x) for x in r)}</div></td><td>{sub(d)}</td><td>{view}</td></tr>' for k, r, d in (
        ('lh', ('RACI', 'Team'), 'Jun 19, 2026'), ('tl', ('Team',), 'Feb 14, 2026'), ('lk', ('RACI',), 'Feb 14, 2026')))
    giv = ''.join(f'<tr><td>{user(k)}</td><td>{tag(r)}</td><td>{tag("Submitted", "positive")}</td><td>{sub(d)}</td><td>{view}</td></tr>' for k, r, d in (
        ('nr', 'Peer feedback', 'Oct 11, 2026'), ('el', 'Manager request', 'Apr 5, 2026'), ('jp', 'Team', 'Mar 20, 2026')))
    act = '<span style="display: block; text-align: right">Actions</span>'
    return [table(('Feedback provider', 'Relationship', 'Date Received', act), rec), table(('Feedback receiver', 'Relationship', 'Status', 'Date Submitted', act), giv)]


def profile_edit_panels():
    def txt(label, ph=''):
        return f'<label class="field" style="flex: 1 1 220px"><span class="field-label">{label}</span><input class="input" type="text" placeholder="{ph}" /></label>'
    def sel(label, control):
        return f'<div class="field" style="flex: 1 1 220px"><span class="field-label">{label}</span>{control}</div>'
    wrap = 'class="row" style="flex-wrap: wrap; align-items: flex-start; gap: var(--spacing-4)"'
    foot = ('<div class="row" style="margin-top: var(--spacing-6)"><a class="btn btn-secondary" href="../profile/index.html" style="text-decoration: none">Cancel</a>'
            '<button class="btn btn-secondary" type="button" disabled>Save Changes</button></div>')
    work = (f'<div class="stack" style="max-width: 640px"><div {wrap}>{txt("Hire date")}{txt("Termination date (optional)")}</div>'
            f'<div {wrap}>{sel("User Type (optional)", ph_select("Select a type", "User type"))}{txt("Job title")}</div>'
            f'<div {wrap}>{sel("Primary manager (optional)", select("Lydia Kaminski", label="Primary manager"))}{sel("Secondary manager (optional)", ph_select("Select a manager", "Secondary manager"))}</div>'
            f'<div {wrap}>{sel("Direct team", select("Delivery in Operations", label="Direct team"))}{sel("Associated teams", select("Delivery in Operations", label="Associated teams"))}</div>'
            f'<div {wrap}>{sel("Business lines (optional)", ph_select("Select business lines", "Business lines"))}{sel("Special groups (optional)", ph_select("Select special groups", "Special groups"))}</div></div>{foot}')
    contacts = (f'<div class="stack" style="max-width: 640px"><div {wrap}>{txt("Work Email")}{txt("Slack (optional)")}</div>'
                f'<div class="field"><span class="field-label">Phone (optional)</span><div>{add_btn("Add phone number")}</div></div>'
                f'<div {wrap}>{txt("LinkedIn (optional)")}{txt("GitHub (optional)")}</div><div {wrap}>{txt("Dribbble (optional)")}{txt("X (optional)")}</div>'
                f'<div {wrap}>{txt("WhatsApp (optional)")}{txt("Telegram (optional)")}</div></div>{foot}')
    return [work, contacts]


# Overlays on the Processes list: the process drawer, the create drawer, RACI.
def process_overlays():
    def x(label='Close drawer'):
        return f'<button class="btn btn-icon-only btn-ghost btn-xs modal-close" type="button" data-modal-close aria-label="{label}">{icon("i-x", "btn-icon")}</button>'
    drawer = f'''  <div class="drawer-overlay" id="process-drawer" hidden>
    <aside class="drawer drawer-regular" role="dialog" aria-modal="true" aria-labelledby="process-drawer-title">
      <header class="drawer-header">
        <div><h2 class="modal-title" id="process-drawer-title">Refund requests</h2>
          <div class="row" style="margin-top: var(--spacing-1); flex-wrap: wrap">{tag("Process", "blue")}{tag("Active")}<span class="body-sm" {MUTED}>Last edit was made 14 hours ago by <a href="#" {LINK}>Cara Keane</a></span></div></div>
        <div class="row"><button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="Copy Link">{icon("i-link", "btn-icon")}</button>{x()}</div>
      </header>
      <div class="drawer-body"><div class="stack">
        {tabs(("Overview", "Activity log")).replace('role="tablist"', 'role="tablist" data-tabs="pdrawer"')}
        <div class="stack" data-panel="pdrawer:0">
        <div {GRID}>{field_row("Accountable owner", user("ck", "Delivery"))}{field_row("End date", sub("Jun 30, 2027"))}</div>
        <div><span class="body-sm" {MUTED}>Description</span><p class="body" style="margin: var(--spacing-2) 0 0">Read the customer’s request, check the order and what arrived, issue the refund for the right items, reply to the customer and close the ticket.</p></div>
        <div class="stack" style="padding-top: var(--spacing-4); border-top: 1px solid var(--color-border)"><h3 class="h4" style="margin: 0">Connections</h3>
          <div class="row">{add_btn("Add Processes")}</div>
          <div class="row"><button class="btn btn-ghost" type="button" data-modal-open="raci-drawer">{icon("i-table", "btn-icon")}View RACI</button></div></div>
        <div class="stack" style="padding-top: var(--spacing-4); border-top: 1px solid var(--color-border)"><h3 class="h4" style="margin: 0">Documents</h3><div class="row" style="justify-content: center; color: var(--color-text-muted)">{icon("i-search", "icon icon-16")}<span class="body-sm">No attachments</span></div></div>
        <div class="stack" style="padding-top: var(--spacing-4); border-top: 1px solid var(--color-border)"><h3 class="h4" style="margin: 0">Activities</h3><p class="body-sm" style="margin: 0; color: var(--color-text-muted)">No Activities yet. Update the process to start creating Activities</p></div>
        </div>
        <div data-panel="pdrawer:1" hidden>{timeline((('Nov 24, 2026', 'Status was changed from Not started to Active by Cara Keane on Nov 24, 2026, 7:34 PM'), ('Nov 24, 2026', 'Accountable owner was added by Cara Keane on Nov 24, 2026, 7:34 PM'), ('Nov 24, 2026', 'Process was created by Cara Keane on Nov 24, 2026, 7:34 PM')))}</div>
      </div></div>
    </aside>
  </div>'''
    create = f'''  <div class="drawer-overlay" id="create-process" hidden>
    <aside class="drawer drawer-regular" role="dialog" aria-modal="true" aria-label="Create Process">
      <header class="drawer-header">
        <div style="flex: 1; min-width: 0"><input class="input" type="text" placeholder="Add process name" aria-label="Process name" style="width: 100%; max-width: none" />
          <div class="row" style="margin-top: var(--spacing-2)">{tag("Process", "blue")}{tag("Not started")}</div></div>
        {x()}
      </header>
      <div class="drawer-body"><div class="stack">
        <div {GRID}>{field_row("Accountable owner", select("Cara Keane", label="Accountable owner"))}{field_row("End date", date_input("End date"))}</div>
        <label class="field"><span class="field-label">Description</span><textarea class="input" rows="6" placeholder="Describe the core of this process and start adding activities that support it"></textarea><span class="field-hint">300 characters minimum</span></label>
        <h3 class="h4" style="margin: 0">Connections</h3>
        <div class="alert alert-info">{icon("i-info", "icon alert-icon")}<p class="alert-message">RACI members with the roles selected for auto-invite in the RACI drawer will become the RoB participants</p></div>
        <article class="card"><div class="row">{icon("i-slack-color", "icon icon-24")}<div><p class="body-semibold" style="margin: 0">Slack</p><p class="body-sm" style="margin: 0; color: var(--color-text-muted)">Create or add Slack channels to sync conversations with this process</p></div></div></article>
        <article class="card"><div class="row">{icon("i-calendar", "icon icon-24")}<div><p class="body-semibold" style="margin: 0">RoB Meetings</p><p class="body-sm" style="margin: 0; color: var(--color-text-muted)">Keep your team aligned with recurring meetings.</p></div></div></article>
        <div class="accordion-group"><div class="accordion">
          <button class="accordion-summary" type="button" aria-expanded="false"><span class="accordion-title">More details</span>{icon("i-chevron-down", "icon accordion-chevron")}</button>
          <div class="accordion-details"><div><div class="accordion-content"><div class="row" style="flex-wrap: wrap">{add_btn("Add business lines")}{add_btn("Add beneficiary function")}{add_btn("Add tags")}{add_btn("Add URL links")}</div></div></div></div>
        </div></div>
      </div></div>
      <footer class="drawer-footer" style="padding-right: calc(var(--spacing-6) + var(--spacing-12))"><button class="btn btn-secondary" type="button" data-modal-close>Cancel</button><button class="btn btn-secondary" type="button">Create</button></footer>
    </aside>
  </div>'''
    raci = f'''  <div class="drawer-overlay" id="raci-drawer" hidden>
    <aside class="drawer drawer-ultra" role="dialog" aria-modal="true" aria-labelledby="raci-drawer-title">
      <header class="drawer-header">
        <div><h2 class="modal-title" id="raci-drawer-title">RACI for Refund requests</h2><p class="body-xs" style="margin: var(--spacing-1) 0 0; color: var(--color-text-muted)">Last edit was made 17 hours ago by <a href="#" {LINK}>Cara Keane</a></p></div>
        {x()}
      </header>
      <div class="drawer-body"><div class="stack">
        <div class="row" style="justify-content: space-between; flex-wrap: wrap"><a class="row body-sm" href="#" {LINK}>{icon("i-info", "icon icon-16")}RACI Guide</a>
          <div class="row"><button class="btn btn-ghost" type="button">{icon("i-eye", "btn-icon")}Show Informed</button>{segmented(("Detailed view", "Compact view"), 0, "RACI view")}</div></div>
        <div class="alert alert-info">{icon("i-info", "icon alert-icon")}<p class="alert-message"><span class="body-sm-semibold">You have view-only access to this RACI.</span> To change it, contact <a href="#" {LINK}>Cara Keane</a>, the accountable owner, or request edit access from the admin team.</p>
          <div class="alert-actions"><button class="btn btn-secondary btn-xs" type="button">Request edit access</button></div></div>
        {raci_table([("Delivery", "Subfunction", user("ck"), user("lh"), user("tl"), "")])}
      </div></div>
    </aside>
  </div>'''
    return drawer + '\n' + create + '\n' + raci


QUERY_PANEL = (f'<article class="card" id="query-panel" hidden style="margin-bottom: var(--spacing-4)"><p class="body-semibold" style="margin: 0 0 var(--spacing-2)">Advanced filters</p>'
               '<p class="body-sm" style="margin: 0">Use advanced filters to:</p><ul class="body-sm" style="margin: var(--spacing-2) 0"><li>Show processes being supported by specific functions</li>'
               '<li>Show processes where you have RACI roles assigned</li><li>Combine AND logic with OR logic using filter groups</li></ul>'
               f'<p class="body-sm" style="margin: 0 0 var(--spacing-3); color: var(--color-text-muted)">Hiding advanced filters will clear results and filter criteria</p><a class="body-sm-semibold" href="#" {LINK}>Add Filter Group</a></article>')


def give_feedback_modal():
    return f'''  <div class="modal-overlay" id="give-feedback" hidden>
    <div class="modal modal-md" role="dialog" aria-modal="true" aria-labelledby="give-feedback-title">
      <header class="modal-header"><h2 class="modal-title" id="give-feedback-title">Give feedback</h2>
        <button class="btn btn-icon-only btn-ghost btn-xs modal-close" type="button" data-modal-close aria-label="Close">{icon("i-x")}</button></header>
      <div class="modal-body"><div class="stack">
        <div class="row" style="align-items: flex-start"><span class="avatar avatar-xl">AD</span><div><p class="body-semibold" style="margin: 0">Adele Delacroix</p>
          <p class="body-sm" style="margin: 0; color: var(--color-text-muted)">Partnerships Lead in Partnerships</p>{tag("Peer feedback")}</div></div>
        <p class="body" style="margin: 0">Please select a minimum of two attributes for Adele.<br />Your feedback helps build stronger teams.</p>
        <p class="body-semibold" style="margin: 0">Sharing options</p>
        <label class="checkbox"><input type="checkbox" class="checkbox-input" /><span class="checkbox-box">{icon("i-check", "checkbox-mark")}</span><span class="checkbox-label">Share with Adele</span></label>
        <label class="checkbox"><input type="checkbox" class="checkbox-input" checked disabled /><span class="checkbox-box">{icon("i-check", "checkbox-mark")}</span><span class="checkbox-label">Share with Adele’s Manager</span></label>
      </div></div>
      <footer class="modal-footer"><button class="btn btn-secondary" type="button" data-modal-close>Cancel</button><button class="btn btn-secondary" type="button">Continue</button></footer>
    </div>
  </div>'''


def timeline(items):
    return ''.join(f'<div class="list-row"><div><p class="list-row-meta">{d}</p><p class="list-row-title">{t}</p></div></div>' for d, t in items)


def check(label, on=False):
    return (f'<label class="checkbox"><input type="checkbox" class="checkbox-input"{" checked" if on else ""} /><span class="checkbox-box">{icon("i-check", "checkbox-mark")}</span>'
            f'<span class="checkbox-label">{label}</span></label>')


def text_in(ph, ic=None):
    if ic:
        return f'<div class="input-icon input-icon-left">{icon(ic, "icon input-icon-glyph")}<input class="input" type="text" placeholder="{ph}" aria-label="{ph}" /></div>'
    return f'<input class="input" type="text" placeholder="{ph}" aria-label="{ph}" />'


def filters_panel(pid, rows):
    body = ''.join(f'<div {PAIR}><span class="body-sm-semibold" style="flex: 0 0 140px">{l}</span><div class="row" style="flex: 1 1 240px; min-width: 0; flex-wrap: wrap">{c}</div></div>' for l, c in rows)
    return (f'<article class="card" id="{pid}" hidden style="margin-bottom: var(--spacing-4); max-width: 760px"><div class="row" style="justify-content: space-between; margin-bottom: var(--spacing-4)">'
            f'<span class="body-semibold">Filters</span><a class="body-sm-semibold" href="#" {LINK}>Clear all</a></div><div class="stack">{body}</div></article>')


def work_filters(noun, types):
    grow = 'style="flex: 1 1 160px; min-width: 0"'
    return filters_panel('filters-panel', [
        ('Name', f'<div {grow}>{text_in(noun + " name", "i-search")}</div>'),
        ('Accountable owner', f'<div {grow}>{text_in("Owner", "i-search")}</div><span class="body-sm-semibold">Accountable function</span><div {grow}>{ph_select("Function", "Accountable function")}</div>'),
        ('Beneficiary function', f'<div {grow}>{ph_select("Function", "Beneficiary function")}</div>'),
        ('Type', ''.join(check(t) for t in types)),
        ('RoB Meeting', f'<div {grow}>{ph_select("RoB meeting name", "RoB meeting")}</div>'),
        ('Tags', f'<div {grow}>{ph_select("Tags", "Tags")}</div>'),
        ('Start date', f'<div {grow}>{text_in("Start date", "i-calendar")}</div><span class="body-sm-semibold">End date</span><div {grow}>{text_in("End date", "i-calendar")}</div>'),
        ('Created at', f'<div {grow}>{text_in("Created at", "i-calendar")}</div><span class="body-sm-semibold">Updated at</span><div {grow}>{text_in("Updated at", "i-calendar")}</div>'),
        ('Status', ''.join(check(t) for t in ('Not started', 'Planning', 'Active', 'Not active', 'Paused'))),
        ('', check('Show archived')),
    ])


def with_views(html, compact, sheet, extra_panels=''):
    """Detailed, compact and spreadsheet views of a work list. The detailed view
    is what the screen already holds below its toolbars."""
    k = '<div data-view="mobile" hidden><div class="stack">'
    assert html.count(k) == 1
    i = html.index(k)
    return (html[:i] + extra_panels + '<div data-panel="view:0">' + html[i:] + '</div>'
            + f'\n<div data-panel="view:1" hidden>{compact}</div>\n<div data-panel="view:2" hidden>{sheet}</div>')


def toggle(html, label, pid):
    k = [x for x in (f'<button class="btn btn-secondary" type="button">{icon(ic, "btn-icon")}{label}</button>' for ic in ('i-filter', 'i-code')) if x in html]
    assert len(k) == 1 and html.count(k[0]) == 1, label
    return html.replace(k[0], k[0].replace('type="button">', f'type="button" data-toggle="{pid}">'))


def compact_rows(items):
    return ''.join(f'<tr><td><span class="row"><span class="cell-title">{n}</span>{tag(kind)}</span></td><td>{tag(st, c)}</td><td><span class="row"><span class="avatar avatar-sm">{ini(k)}</span>{sub(PEOPLE[k][0])}</span></td>'
                   f'<td>{sub(r[0]) if r else ""}</td></tr>' for n, kind, st, c, k, r in items)


def sheet_table(heads, rows):
    body = ''.join('<tr><td>' + sub(i) + '</td>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for i, r in enumerate(rows, 1))
    return table(('#',) + heads, body)


def indent(n, lvl, bold=False):
    cls = 'body-sm-semibold' if bold else 'body-sm'
    return f'<span class="{cls}" style="padding-left: calc({lvl} * var(--spacing-4))">{n}</span>'


def processes_views():
    comp = tree_table(PROC_TREE, cols=('status', 'acc', 'rob', 'actions'), kinds=('Process', 'Activity', 'Sub-activity'), prefix='procc', sticky=False, compact=True,
                      links={'Refund requests': 'href="#open-process-drawer" data-modal-open="process-drawer"'}) + pager()
    return comp, sheet_tree(PROC_TREE, 'procs', with_health=False)


def initiatives_views():
    comp = tree_table(INIT_TREE, cols=('status', 'health', 'acc', 'roadmap', 'rob', 'actions'), prefix='initc', sticky=False, compact=True,
                      links={'Onboarding in one week': 'href="../initiative-view/index.html"'}) + pager(("1", "2", "3"))
    return comp, sheet_tree(INIT_TREE, 'inits')


INIT_QUERY = QUERY_PANEL.replace('Show processes being supported', 'Show initiatives being supported').replace('Show processes where', 'Show initiatives where')


def initiatives_with_states():
    h = toggle(toggle(initiatives(), 'Filters', 'filters-panel'), 'Query', 'query-panel')
    h = swap_table(h, tree_table(INIT_TREE, cols=('status', 'health', 'acc', 'roadmap', 'rob', 'actions'), prefix='init', sticky=False, attrs=' data-view="desktop"',
                                 tags=lambda name, level: tag('# Core Strategy') if name in KIDS or level else tag('Operationalize', 'blue-light') if name == 'Learning programs' else '',
                                 links={'Onboarding in one week': 'href="../initiative-view/index.html"'}))
    h = h.replace('aria-label="View RACI">', 'aria-label="View RACI" data-modal-open="raci-drawer">')
    return with_views(h, *initiatives_views(), extra_panels=work_filters('Initiative', ('Initiative', 'Project', 'Sub-project')) + INIT_QUERY)


def raci_overlay(name):
    o = process_overlays()
    return o[o.index('  <div class="drawer-overlay" id="raci-drawer"'):].replace('Refund requests', name)


def no_access():
    return f'''      <div class="alert alert-warning" style="border-radius: 0; border-width: 0 0 1px; padding-left: var(--spacing-12)">{icon("i-exclamation-solid" if False else "i-warning", "icon alert-icon")}<p class="alert-message">You do not have rights to edit the Org Unit</p></div>'''


HEALTH_KIND = {'On track': 'positive', 'At risk': 'warning', 'Off track': 'negative', 'Not active': 'light'}
STATUS_KIND = {'Execution': 'blue', 'Impact assessment': 'blue-light', 'Complete': 'positive'}
# Core Strategy work as a tree: initiative > project > sub-project.
# (name, status, health, accountable, unit, rob meeting (date, recurrence, past) or None, children)
DASH_TREE = [
    ('Faster customer onboarding', 'sr', ('Onboarding in one week', 'Impact assessment', 'On track', 'ck', 'Delivery', ('Oct 27 • 4:00pm', 'Every 2 weeks on Tuesday', True), [
        ('Kick-off checklist', 'Execution', 'On track', 'lh', 'Delivery', None, [
            ('Checklist template', 'Complete', 'On track', 'lh', 'Delivery', None, []),
            ('Customer welcome call', 'Execution', 'Not active', 'tl', 'Delivery', None, [])]),
        ('Account setup in one day', 'Definition', 'Not active', 'el', 'IT', None, []),
        ('Onboarding status page', 'Complete', 'On track', 'nr', 'Operations', None, [])])),
    ('Faster customer onboarding', 'sr', ('Self-serve account setup', 'Execution', 'On track', 'el', 'IT', ('Dec 01 • 5:00pm', 'Every week on Tuesday', False), [
        ('Billing setup wizard', 'Execution', 'Not active', 'el', 'IT', None, []),
        ('Invite your team flow', 'Execution', 'On track', 'nr', 'Operations', None, [
            ('Bulk invite by file', 'Definition', 'Not active', 'nr', 'Operations', None, []),
            ('Role presets', 'Complete', 'On track', 'nr', 'Operations', None, [])]),
        ('Usage dashboard for admins', 'Definition', 'Not active', 'mt', 'Business Analytics', None, []),
        ('Help centre rewrite', 'Complete', 'On track', 'jp', 'Learning & Development', None, [])])),
    ('Reliable delivery', 'lk', ('Delivery health reviews', 'Idea', 'Not active', 'lk', 'Operations', ('Oct 22 • 5:00pm', 'Every week on Thursday', True), [])),
    ('Reliable delivery', 'lk', ('Refund handling', 'Execution', 'On track', 'ck', 'Delivery', ('Nov 26 • 12:00pm', 'Every weekday', False), [
        ('One refund policy', 'Complete', 'On track', 'og', 'Legal', None, []),
        ('Refund review queue', 'Execution', 'At risk', 'ck', 'Delivery', None, [
            ('Queue triage rules', 'Execution', 'At risk', 'tl', 'Delivery', None, [])])])),
    ('A stronger partner channel', 'ad', ('Partner marketing sites', 'Idea', 'Not active', 'ad', 'Partnerships', None, [])),
    ('A stronger partner channel', 'ad', ('Partner certification', 'Execution', 'On track', 'ad', 'Partnerships', ('Nov 25 • 3:00pm', 'Every 2 weeks on Wednesday', False), [
        ('Certification syllabus', 'Complete', 'On track', 'jp', 'Learning & Development', None, []),
        ('Partner exam', 'Execution', 'Off track', 'ad', 'Partnerships', None, [])])),
    ('Grow the team well', 'ac', ('Learning programs', 'Execution', 'On track', 'jp', 'Learning & Development', ('Nov 30 • 6:00pm', 'Every week on Monday', False), [])),
    ('Grow the team well', 'ac', ('Recruiting pipeline', 'Execution', 'On track', 'mv', 'Recruiting', ('Oct 14 • 6:00pm', 'Every week on Wednesday', True), [
        ('One pipeline view', 'Complete', 'On track', 'mv', 'Recruiting', None, []),
        ('Interview scorecards', 'Execution', 'On track', 'km', 'Northwind Hire', None, [])])),
    ('Reliable delivery', 'lk', ('Engagement health score', 'Execution', 'On track', 'mt', 'Business Analytics', None, [])),
    ('Faster customer onboarding', 'sr', ('First-week success plan', 'Execution', 'On track', 'ck', 'Delivery', ('Oct 27 • 4:00pm', 'Every 2 weeks on Tuesday', True), [])),
]
KINDS = ('Initiative', 'Project', 'Sub-project')
TREE_COLS = {'objective': ('Strategic Objective', 192), 'owner': ('Objective Owner', 136), 'status': ('Status', 144), 'health': ('Health', 96),
             'acc': ('Accountability', 152), 'roadmap': ('Roadmap', 88), 'rob': ('RoB Meeting', 184), 'actions': ('Actions', 104)}


def tree_table(tree, cols=('objective', 'owner', 'status', 'health', 'acc', 'roadmap', 'rob', 'actions'), kinds=KINDS, prefix='dash', sticky=True,
               tags=lambda name, level: tag('# Core Strategy'), links=None, attrs='', compact=False):
    """A work list as the product draws it: rows that open a second and a
    third layer. With sticky, the name column stays put while the rest scrolls
    sideways (the dashboard); without, the table fills the page (the lists).
    tree: (objective, owner, node); node: (name, status, health, person, unit,
    rob meeting (date, recurrence, past) or None, children)."""
    out, n, links = [], [0], links or {}

    def row(node, level, objective, owner, parent):
        name, status, hlth, k, unit, rob, kids = node
        n[0] += 1
        rid = f'{prefix}-{n[0]}'
        caret = (f'<button class="row-toggle" type="button" aria-expanded="false" aria-label="Toggle {name}" data-rows="{rid}">{icon("i-chevron-down")}</button>' if kids
                 else '<span class="row-toggle-spacer"></span>')
        link = f'<a class="ps-wtree-title" {links[name]}>{name}</a>' if name in links else f'<span class="ps-wtree-title">{name}</span>'
        first = (f'<div class="ps-wtree-name" data-level="{level}">{caret}<div class="stack" style="gap: var(--spacing-1); align-items: flex-start; min-width: 0">{link}'
                 f'{"" if compact else tag(kinds[level]) + tags(name, level)}</div></div>')
        if rob:
            date = f'<s>{rob[0]}</s>' if rob[2] else rob[0]
            meet = (f'<div class="cell-meta"><span class="cell-meta-title row" style="gap: var(--spacing-2); flex-wrap: nowrap">{icon("i-calendar", "icon icon-16")}<span style="white-space: nowrap">{date}</span></span>'
                    f'<span class="cell-meta-sub">{tag(rob[1])}</span></div>')
            if compact:
                meet = f'<span class="row body-sm" style="gap: var(--spacing-2); flex-wrap: nowrap; white-space: nowrap">{icon("i-calendar", "icon icon-16")}<span>{date}</span></span>'
        elif 'health' in cols:
            meet = f'<span class="row body-sm" style="gap: var(--spacing-1); flex-wrap: nowrap; white-space: nowrap; color: var(--color-text-muted)"><span style="color: var(--color-warning); display: inline-flex">{icon("i-info", "icon icon-16")}</span>No meeting connected</span>'
        else:
            meet = ''
        cell = {'objective': lambda: sub(objective), 'owner': lambda: sub(PEOPLE[owner][0]), 'status': lambda: tag(status, STATUS_KIND.get(status, 'light')),
                'health': lambda: health(hlth, HEALTH_KIND[hlth]),
                'acc': lambda: f'<span class="body-sm-semibold" style="white-space: nowrap">{PEOPLE[k][0]}</span>' if compact else user(k, unit),
                'roadmap': lambda: (f'<button class="btn btn-icon-only btn-ghost btn-xs ps-roadmap is-{HEALTH_KIND[hlth]}" type="button" aria-label="View roadmap for {name}">{icon("i-roadmap", "btn-icon")}</button>' if level == 0 else ''),
                'rob': lambda: meet, 'actions': raci_btn}
        hide = f' data-child-of="{parent}" hidden' if parent else ''
        out.append(f'<tr class="ps-wtree-row" data-search-item{hide}><td>{first}</td>' + ''.join(f'<td>{cell[c]()}</td>' for c in cols) + '</tr>')
        for kid in kids:
            row(kid, level + 1, objective, owner, rid)

    for objective, owner, node in tree:
        row(node, 0, objective, owner, '')
    width = lambda w: f' style="width: {w}px"' if sticky else ''
    th = f'<th{width(256) if sticky else chr(32) + chr(115) + "tyle=" + chr(34) + "width: 30%" + chr(34)}><span class="row" style="gap: var(--spacing-2); flex-wrap: nowrap">Name<button class="btn btn-ghost btn-xs" type="button" data-expand-all>Expand all</button></span></th>'
    for c in cols:
        h, w = TREE_COLS[c]
        inner = (f'<span class="row" style="gap: var(--spacing-1); flex-wrap: nowrap">Health{icon("i-info", "icon icon-16")}</span>' if c == 'health'
                 else '<span style="display: block; text-align: right">Actions</span>' if c == 'actions' else h)
        th += f'<th{width(w)}>{inner}</th>'
    total = 256 + sum(TREE_COLS[c][1] for c in cols)
    style = f' style="min-width: {total}px; table-layout: fixed"' if sticky else ''
    return (f'<div class="table-scroll" style="max-height: none"{attrs}><table class="table ps-wtree{" ps-wtree-sticky" if sticky else ""}{" ps-wtree-compact" if compact else ""}"{style}>'
            f'<thead><tr>{th}</tr></thead><tbody>{"".join(out)}</tbody></table></div>')


DESCR = {n: d for o, k, n, d, st, kind in OBJECTIVES}
DESCR.update({
    'Refund requests': 'Read the request, check the order, issue the refund and close the ticket.', 'Refund review': 'Check the order and what arrived against the request.',
    'Partial refunds': 'Refund only the items that were wrong or missing.', 'Vendor Management': 'Choose, onboard and review the vendors the company depends on.',
    'Supplier onboarding': 'Contracts, security review and access for a new vendor.', 'Workplace and IT': 'Equipment, accounts and access for everyone on the team.',
    'Legal Operations': 'Contract templates, reviews and renewals.', 'Kick-off checklist': 'One checklist every engagement starts from.',
    'Checklist template': 'The shared template, with an owner for every line.', 'Customer welcome call': 'A first call in the week the contract is signed.',
    'Account setup in one day': 'Accounts, billing and access ready the day after signing.', 'Onboarding status page': 'One page that shows where each new customer is.',
    'Learning Programs': 'Courses and coaching for every team.', 'Partner Marketing Sites': 'The co-branded pages partners send customers to.',
    'Northwind Hire': 'Hiring run for the Northwind business line.', 'Analytics Reporting': 'The weekly numbers every function reads.',
    'Recruiting Pipeline': 'Sourcing, interviews and offers for open roles.', 'Member Experience': 'How the team experiences working here.',
    'Billing setup wizard': 'Guide a new customer through billing without a call.', 'Invite your team flow': 'Let an admin bring their team in themselves.',
    'One refund policy': 'The same refund rules in every region.', 'Refund review queue': 'One queue for refunds that need a second look.',
})


def sheet_tree(tree, prefix, with_health=True):
    """The spreadsheet view: every layer open, numbered rows, ruled cells, a
    column of carets, and the description beside the name."""
    out, n = [], [0]

    def row(node, level, parent):
        name, status, hlth, k, unit, rob, kids = node
        n[0] += 1
        rid = f'{prefix}-{n[0]}'
        caret = (f'<button class="row-toggle" type="button" aria-expanded="true" aria-label="Toggle {name}" data-rows="{rid}">{icon("i-chevron-down")}</button>' if kids else '')
        cells = [sub(n[0]), caret, f'<div class="ps-wtree-name" data-level="{level}"><span class="{"body-sm-semibold" if kids else "body-sm"}">{name}</span></div>',
                 sub(DESCR.get(name, '')), tag(status, STATUS_KIND.get(status, 'light'))]
        if with_health:
            cells.append(health(hlth, HEALTH_KIND[hlth]))
        cells += [sub(PEOPLE[k][0]), sub(PEOPLE[k][0]), sub(unit)]
        hide = f' data-child-of="{parent}"' if parent else ''
        out.append(f'<tr data-search-item{hide}>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
        for kid in kids:
            row(kid, level + 1, rid)

    for _, _, node in tree:
        row(node, 0, '')
    heads = ['#', f'<span style="display: inline-flex">{icon("i-chevron-down", "icon icon-16")}</span>', 'Name', 'Description', 'Status'] + (['Health'] if with_health else []) + ['Owner', 'Project manager', 'Beneficiary function']
    th = ''.join(f'<th>{h}</th>' for h in heads)
    return f'<div class="table-scroll" style="max-height: none"><table class="table ps-sheet"><thead><tr>{th}</tr></thead><tbody>{"".join(out)}</tbody></table></div>'


def swap_table(html, table_html):
    """Put a tree table where a screen's plain desktop table is."""
    m = re_table.search(html)
    assert m and len(re_table.findall(html)) == 1
    return html[:m.start()] + table_html + html[m.end():]


re_table = _re.compile(r'<div class="table-scroll" style="max-height: none" data-view="desktop">.*?</table>\s*</div>', _re.S)
PAST = lambda r: (r[0], r[1], r[0].startswith('Oct')) if r else None
KIDS = {node[0]: node[6] for _, _, node in DASH_TREE}
PROC_KIDS = {
    'Vendor Management': [('Supplier onboarding', 'Active', None, 'lk', 'Operations', None, []), ('Contract renewals', 'Not started', None, 'og', 'Legal', None, [])],
    'Refund requests': [('Refund review', 'Active', None, 'lh', 'Delivery', None, [('Partial refunds', 'Active', None, 'tl', 'Delivery', None, []), ('Refunds over the limit', 'Paused', None, 'ck', 'Delivery', None, [])]),
                        ('Reply to the customer', 'Active', None, 'tl', 'Delivery', None, [])],
    'Legal Operations': [('Contract review', 'Active', None, 'og', 'Legal', None, []), ('Policy updates', 'Not active', None, 'og', 'Legal', None, [])],
    'Recruiting Pipeline': [('Sourcing', 'Active', None, 'mv', 'Recruiting', None, [('Referral intake', 'Active', None, 'km', 'Northwind Hire', None, [])])],
    'Analytics Reporting': [('Weekly numbers', 'Active', None, 'mt', 'Business Analytics', None, [])],
}
PROC_TREE = [(None, None, (n, st, None, k, unit, PAST(r), PROC_KIDS.get(n, []))) for n, st, k, unit, r in PROCESSES]
DASH_LINKS = {n: 'href="../initiative-view/index.html"' for n in KIDS}
INIT_TREE = [(None, None, (n, st, h[0], k, unit, PAST(r), KIDS.get(n, []))) for n, st, kind, h, k, unit, road, r in INITIATIVES]


def dashboard_with_states():
    h = dashboard()
    more = '<button class="btn btn-icon-only btn-ghost" type="button" aria-label="More actions">' + icon("i-dots-three-vertical", "btn-icon") + '</button>'
    assert h.count(more) == 1
    h = h.replace(more, '<div class="dropdown">' + more.replace('class="btn btn-icon-only btn-ghost"', 'class="btn btn-icon-only btn-ghost dropdown-trigger" aria-expanded="false"')
                  + '<div class="dropdown-menu dropdown-menu-end" id="dash-more" hidden><button class="dropdown-item" type="button">Edit strategic objectives</button></div></div>')
    seg = '<div class="segmented" role="group" aria-label="Initiatives shown">'
    assert h.count(seg) == 2
    h = h.replace(seg, seg.replace('>', ' data-tabs="scope">'))
    k0 = '      <article class="card" style="margin-bottom: var(--spacing-6)">'
    assert h.count(k0) == 1
    j = h.index(k0)
    stats = ''.join(f'<div class="stat-card"><p class="stat-card-label">{l}</p><p class="stat-card-value">{v}</p></div>'
                    for l, v in (('Idea', 9), ('Opportunity assessment', 0), ('Definition', 8), ('Execution', 31), ('Impact assessment', 7), ('Complete', 60), ('On hold', 18)))
    orow = ''.join(f'<tr><td><span class="cell-title">{n}</span><div>{tag("Initiative")}</div></td><td>{tag(st, kind)}</td><td>{health(*hh)}</td><td>{user(k, unit)}</td><td>{sub(road)}</td><td>{rob_cell(r)}</td><td>{raci_btn()}</td></tr>'
                   for n, st, kind, hh, k, unit, road, r in INITIATIVES[2:7])
    ocards = ''.join(work_card(n, health(*hh) + tag("Initiative") + tag(st, kind), k, unit, caret=True) for n, st, kind, hh, k, unit, road, r in INITIATIVES[2:7])
    other = f'''<article class="card" style="margin-bottom: var(--spacing-6)">
        <div class="row" style="flex-wrap: wrap; gap: var(--spacing-3)"><span class="body"><span class="body-semibold">34</span> Initiatives</span>{icon("i-caret-right", "icon icon-16")}
          <span class="body"><span class="body-semibold">136</span> Projects</span>{icon("i-caret-right", "icon icon-16")}<span class="body"><span class="body-semibold">104</span> Sub-projects</span></div>
        <div style="display: flex; flex-wrap: wrap; gap: var(--spacing-8); margin-top: var(--spacing-6)">
          <div class="stack" style="flex: 1 1 320px; min-width: 0">
            <div class="row" style="justify-content: space-between"><h2 class="body-semibold" style="margin: 0">Health</h2><span class="body-sm"><span class="body-sm-semibold">76%</span> on track</span></div>
            <div class="progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="76" aria-label="On track"><div class="progress-track"><div class="progress-fill" style="width: 76%"></div></div><span class="progress-value" hidden>76%</span></div>
            <div class="row" style="flex-wrap: wrap">{health("206 On track", "positive")}{health("0 At risk", "warning")}{health("6 Off track", "negative")}{health("59 Not active", "light")}</div>
          </div>
          <div class="stack" style="flex: 2 1 480px; min-width: 0"><h2 class="body-semibold" style="margin: 0">Status</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: var(--spacing-3)">{stats}</div></div>
        </div>
      </article>
      {mobile_toolbar("Search by name, owner or function")}
      <div data-view="desktop"><div class="toolbar" style="margin-bottom: var(--spacing-4)">
        <div class="input-icon input-icon-left toolbar-search">{icon("i-search", "icon input-icon-glyph")}<input class="input" type="text" placeholder="Search by name, owner or function" aria-label="Search" /></div>
        <button class="btn btn-secondary" type="button">{icon("i-filter", "btn-icon")}Filters</button><button class="btn btn-secondary" type="button">{icon("i-code", "btn-icon")}Query</button>
      </div>
      {tree_table(INIT_TREE[1:7], cols=("status", "health", "acc", "roadmap", "rob", "actions"), prefix="dasho", sticky=False, tags=lambda name, level: "")}</div>
      {mobile('<div class="stack">' + ocards + '</div>')}'''
    h = h.replace('<table class="table">\n          <thead><tr><th>#</th>', '<table class="table ps-sheet">\n          <thead><tr><th>#</th>')
    h = h.replace('<table class="table">', '<table class="table ps-striped">')
    h = h[:j] + '<div data-panel="scope:0">' + h[j:] + '</div>\n<div data-panel="scope:1" hidden>' + other + '</div>'
    k = '      <div class="table-scroll" style="max-height: none">'
    assert h.count(k) == 2   # the spreadsheet table, then the Other initiatives one
    i = h.index(k)
    heads = ('Name', 'Strategic Objective', 'Objective Owner', 'Status', 'Health', 'Accountability', 'Roadmap', 'RoB Meeting')
    hl = {'Execution': ('On track', 'positive'), 'Complete': ('On track', 'positive')}
    det = ''.join(f'<tr><td><span class="cell-title">{n}</span><div>{tag("Initiative")}{tag("# Core Strategy")}</div></td><td>{sub(o)}</td><td>{sub(PEOPLE[k][0])}</td><td>{tag(st, kind)}</td>'
                  f'<td>{health(*hl.get(st, ("Not active", "light")))}</td><td>{user(k)}</td><td>{sub("Q4 2026" if st == "Execution" else "")}</td><td></td></tr>' for o, k, n, d, st, kind in OBJECTIVES)
    comp = ''.join(f'<tr><td><span class="row"><span class="cell-title">{n}</span>{tag("Initiative")}</span></td><td>{sub(o)}</td><td>{sub(PEOPLE[k][0])}</td><td>{tag(st, kind)}</td>'
                   f'<td>{health(*hl.get(st, ("Not active", "light")))}</td><td><span class="row"><span class="avatar avatar-sm">{ini(k)}</span>{sub(PEOPLE[k][0])}</span></td><td></td><td></td></tr>' for o, k, n, d, st, kind in OBJECTIVES)
    e = h.index('</div>\n<div data-panel="scope:1" hidden>')
    ccards = ''.join(work_card(nd[0], health(nd[2], HEALTH_KIND[nd[2]]) + tag("Initiative") + tag(nd[1], STATUS_KIND.get(nd[1], "light")) + tag("# Core Strategy"), nd[3], nd[4], caret=bool(nd[6])) for o, k, nd in DASH_TREE)
    h = (h[:i] + f'<div data-view="desktop"><div data-panel="view:0">{tree_table(DASH_TREE, links=DASH_LINKS)}</div>\n<div data-panel="view:1" hidden>{tree_table(DASH_TREE, links=DASH_LINKS, compact=True, prefix="dashc")}</div>\n<div data-panel="view:2" hidden>' + h[i:e] + '</div></div>'
         + mobile('<div class="stack">' + ccards + '</div>') + h[e:])
    charts = [barchart([('Idea', 33, ''), ('Opportunity assessment', 5, ''), ('Definition', 7, ''), ('Execution', 53, 'is-accent'), ('Impact assessment', 0, ''), ('Complete', 34, 'is-success'), ('On hold', 6, '')]),
              barchart([('Idea', 9, ''), ('Opportunity assessment', 0, ''), ('Definition', 8, ''), ('Execution', 31, 'is-accent'), ('Impact assessment', 7, ''), ('Complete', 60, 'is-success'), ('On hold', 18, '')])]
    bars = [healthbar(170, 1, 1, 112), healthbar(206, 0, 6, 59)]
    h, n = _re.subn(r'<div style="display: grid; grid-template-columns: repeat\(auto-fit, minmax\(120px, 1fr\)\); gap: var\(--spacing-3\)">(?:<div class="stat-card">.*?</div>)+</div>', lambda m: charts.pop(0), h, flags=_re.S)
    assert n == 2, n
    h, n = _re.subn(r'<div class="progress" role="progressbar".*?</span>\s*</div>', lambda m: bars.pop(0), h, flags=_re.S)
    assert n == 2, n
    return h


def rob_with_states():
    h = rob_calendar()
    k = '      <div class="row" style="justify-content: space-between; margin-bottom: var(--spacing-3)">\n        <h2 class="h3" style="margin: 0">November 2026</h2>'
    assert h.count(k) == 1
    i = h.index(k)
    day = ''.join(f'<a class="list-row" href="../rob-meeting-view/index.html" style="text-decoration: none"><div><p class="list-row-title">{t}</p><p class="list-row-meta">{m}</p></div></a>'
                  for t, m in (('[RoB] Onboarding in one week', '10:30am Operations'), ('Delivery All Hands', '2:00pm Delivery')))
    nav = (f'<div class="row"><button class="btn btn-secondary btn-icon-only" type="button" aria-label="Previous">{icon("i-arrow-long-left", "btn-icon")}</button>'
           f'<button class="btn btn-secondary" type="button">Today</button><button class="btn btn-secondary btn-icon-only" type="button" aria-label="Next">{icon("i-arrow-long-right", "btn-icon")}</button></div>')
    sched = f'<div class="row" style="justify-content: space-between; margin-bottom: var(--spacing-3)"><h2 class="h3" style="margin: 0">23 November 2026, <span class="body">Monday</span></h2>{nav}</div>{day}'
    week = (f'<div class="row" style="justify-content: space-between; margin-bottom: var(--spacing-3)"><h2 class="h3" style="margin: 0">Nov 23-29</h2>{nav}</div>'
            + week_grid([((0, '10:00am'), ('[RoB] Onboarding in one week', 'Operations')), ((2, '1:00pm'), ('[RoB] Refund requests', 'Delivery')), ((3, '4:00pm'), ('[RoB] Partner marketing sites', 'Partnerships'))]))
    grow = 'style="flex: 1 1 200px; min-width: 0"'
    filt = filters_panel('rob-filters', [('Meeting name', f'<div {grow}>{text_in("Meeting name")}</div>')] +
                         [(l, f'<div {grow}>{select("All", label=l)}</div>') for l in ('Team', 'Meeting owners', 'Attendee', 'Divisions', 'Slack channels')] +
                         [('', check('Show sub teams', True) + check('Hide 1:1 Meetings', True))])
    h = (h[:i] + filt + '<div data-panel="robview:0" hidden>' + sched + '</div>\n<div data-panel="robview:1" hidden>' + week + '</div>\n<div data-panel="robview:2">' + h[i:] + '</div>')
    h = h.replace('<div class="segmented" role="group" aria-label="Calendar view">', '<div class="segmented" role="group" aria-label="Calendar view" data-tabs="robview">')
    h = toggle(h, 'Filters', 'rob-filters')
    # All events: the same month, every team's meetings, with the two default filters on
    more = {2: 40, 3: 60, 4: 53, 5: 58, 6: 38, 9: 43, 10: 60, 11: 53, 12: 58, 13: 35, 16: 39, 17: 55, 18: 46, 19: 58, 20: 36}
    allgrid = cal_month([[2, 3, 4, 5, 6], [9, 10, 11, 12, 13], [16, 17, 18, 19, 20]],
                        lambda d: [('[RoB] Onboarding in one week', '10:00am Operations', True), ('Delivery daily sync-up', '10:30am Delivery', False), ('IT daily sync-up', '11:00am IT', False)], more)
    chip = lambda t: f'<span class="chip">{t}<button class="chip-remove" type="button" aria-label="Remove">{icon("i-x", "")}</button></span>'
    allev = (f'<div class="toolbar" style="margin-bottom: var(--spacing-3)"><div class="input-icon input-icon-left toolbar-search">{icon("i-search", "icon input-icon-glyph")}<input class="input" type="text" placeholder="Search" aria-label="Search meetings" /></div>'
             f'<button class="btn btn-secondary" type="button">{icon("i-filter", "btn-icon")}Filters (2)</button><span class="toolbar-spacer"></span>{segmented(("Schedule", "Week", "Month"), 2, "Calendar view")}</div>'
             f'<div class="row" style="margin-bottom: var(--spacing-4)">{chip("Hide 1:1 Meetings")}{chip("Show sub teams: Yes")}</div>'
             f'<div class="row" style="justify-content: space-between; margin-bottom: var(--spacing-3)"><h2 class="h3" style="margin: 0">November 2026</h2>{nav}</div>'             + allgrid)
    t = '      <div class="toolbar" style="margin: var(--spacing-4) 0">'
    assert h.count(t) == 1
    j = h.index(t)
    h = h[:j] + desktop(h[j:]) + mobile(rob_phone(False))
    return with_tabs(h, 'rob', [desktop(allev) + mobile(rob_phone(True))])


def minical(title, lead, days, tail, today, dots=()):
    """A small month: seven weekdays across, the days before and after the
    month greyed, today filled, a dot under days that have meetings."""
    cells = ''.join(f'<span class="ps-minical-head">{d}</span>' for d in ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'))
    cells += ''.join(f'<span class="ps-minical-day is-out">{d}</span>' for d in lead)
    cells += ''.join(f'<button class="ps-minical-day{" is-today" if d == today else ""}{" has-events" if d in dots else ""}" type="button">{d}</button>' for d in range(1, days + 1))
    cells += ''.join(f'<span class="ps-minical-day is-out">{d}</span>' for d in tail)
    return (f'<div class="ps-minical"><div class="ps-minical-nav"><button class="btn btn-icon-only btn-ghost" type="button" aria-label="Previous month">{icon("i-chevron-left", "btn-icon")}</button>'
            f'<span class="body-lg-semibold">{title}</span><button class="btn btn-icon-only btn-ghost" type="button" aria-label="Next month">{icon("i-chevron-right", "btn-icon")}</button></div>'
            f'<div class="ps-minical-grid">{cells}</div></div>')


def agenda(items):
    """The day's meetings, one per line: time, name, a coloured rule at the
    left. 'now' draws the line that marks the current time."""
    out = []
    for it in items:
        if it == 'now':
            out.append('<div class="ps-agenda-now"></div>')
            continue
        time, name, cls = it
        out.append(f'<a class="ps-agenda-item {cls}" href="../rob-meeting-view/index.html"><span>{time}</span><span>{name}</span></a>')
    return '<div class="ps-agenda">' + ''.join(out) + '</div>'


def rob_phone(everyone):
    chip = lambda t: f'<span class="chip">{t}<button class="chip-remove" type="button" aria-label="Remove">{icon("i-x", "")}</button></span>'
    count = '<span class="count-badge">2</span>' if everyone else ''
    bar = (f'<div class="toolbar" style="margin: var(--spacing-4) 0 var(--spacing-3)"><div class="input-icon input-icon-left toolbar-search">{icon("i-search", "icon input-icon-glyph")}<input class="input" type="text" placeholder="Search" aria-label="Search meetings" /></div>'
           f'<button class="btn btn-icon-only btn-ghost" type="button" aria-label="Filters">{icon("i-filter", "btn-icon")}</button>{count}</div>')
    chips = f'<div class="row" style="flex-wrap: wrap; margin-bottom: var(--spacing-4)">{chip("Hide 1:1 Meetings")}{chip("Show sub teams: Yes")}</div>' if everyone else ''
    mine = [('10:30am - 11:30am', '[RoB] Onboarding in one week', 'is-past'), 'now', ('2:00pm - 3:00pm', 'Delivery All Hands', '')]
    allm = [('10:00am - 10:30am', '[RoB] Onboarding in one week', 'is-past is-declined'), ('10:30am - 10:50am', 'Delivery daily sync-up', 'is-past is-declined'), ('11:00am - 11:30am', 'IT daily sync-up', 'is-past is-maybe'),
            ('12:00pm - 1:00pm', '[RoB] Refund requests', ''), 'now', ('1:30pm - 1:55pm', '[RoB] Partner marketing sites', ''), ('2:00pm - 3:00pm', 'Delivery All Hands', ''), ('4:00pm - 4:30pm', '[RoB] Legal operations', '')]
    return bar + chips + minical('November 2026', (26, 27, 28, 29, 30, 31), 30, (1, 2, 3, 4, 5, 6), 25, (25,)) + agenda(allm if everyone else mine)


ATTRS = [('Brand', 'How customers, talent and the market see us'), ('Growth', 'New customers, markets and offerings'),
         ('Dynamic/Process', 'Efficient, adaptable ways of working that keep improving'), ('Growth/Revenue', 'Revenue and margin, directly'),
         ('People', 'Hiring, developing and keeping great people'), ('Organization', 'Structure, roles and accountability that let teams execute'),
         ('Speed', 'Deciding and shipping faster'), ('Quality', 'Higher standards, fewer defects, better customer experience')]


def perf_attrs_modal():
    rows = ''.join(f'<div class="list-row"><div><p class="list-row-title">{n}</p><p class="list-row-meta">{d}</p></div><span class="count-badge count-badge-secondary">{c}</span></div>'
                   for (n, d), c in zip(ATTRS, (0, 2, 1, 0, 1, 0, 0, 0)))
    return f'''  <div class="modal-overlay" id="perf-attrs" hidden>
    <div class="modal modal-md" role="dialog" aria-modal="true" aria-labelledby="perf-attrs-title">
      <header class="modal-header"><h2 class="modal-title" id="perf-attrs-title">Performance attributes</h2>
        <button class="btn btn-icon-only btn-ghost btn-xs modal-close" type="button" data-modal-close aria-label="Close">{icon("i-x")}</button></header>
      <div class="modal-body"><p class="body-sm" style="margin: 0 0 var(--spacing-3); color: var(--color-text-muted)">Each objective and key result can support one attribute. Numbers are for 2026.</p>{rows}</div>
    </div>
  </div>'''


def okrs_with_states():
    h = with_tabs(okrs(), 'okrs', okr_panels())
    k = '<button class="btn btn-secondary" type="button">' + icon("i-info", "btn-icon") + 'Performance attributes</button>'
    assert h.count(k) == 1
    return h.replace(k, k.replace('type="button">', 'type="button" data-modal-open="perf-attrs">'))


def tree_cells(html):
    """A work list's name cell as the kit means it: a caret, the name, and its
    kind under it. Every top-level row gets the caret; a row with children
    built in keeps its own, which is the one that folds."""
    spare = f'<button class="row-toggle" type="button" aria-expanded="false" aria-label="Toggle children">{icon("i-caret-right")}</button>'

    def cell(m):
        own, el, attrs, name, kind = m.groups()
        return (f'<td><div class="cell-title-row">{(own or spare).strip()}<div class="cell-title"><{el} class="cell-title-text"{attrs}>{name}</{el}>'
                f'<span class="cell-title-sub">{kind}</span></div></div></td>')
    html = _re.sub(r'<td>(<button class="row-toggle"[^>]*>.*?</button> )?<(span|a) class="cell-title"([^>]*)>(.*?)</\2><div>(.*?)</div></td>', cell, html, flags=_re.S)
    return html.replace('<table class="table">\n          <thead><tr><th>Name', '<table class="table ps-striped">\n          <thead><tr><th>Name')


def kid_cell(name, kind):
    return (f'<div class="cell-title-row"><span class="row-toggle-spacer"></span><div class="cell-title"><span class="cell-title-text">{name}</span>'
            f'<span class="cell-title-sub">{tag(kind)}</span></div></div>')


def processes_with_states():
    h = processes()
    k = '<button class="btn btn-secondary" type="button">' + icon("i-code", "btn-icon") + 'Query</button>'
    assert h.count(k) == 1
    h = h.replace(k, '<button class="btn btn-secondary" type="button" data-toggle="query-panel">' + icon("i-code", "btn-icon") + 'Query</button>')
    k = '<div data-view="mobile" hidden><div class="stack">'
    assert h.count(k) == 1
    h = h.replace(k, QUERY_PANEL + '\n' + k)
    h = h.replace('<button class="btn btn-primary" type="button">Create Process</button>', '<button class="btn btn-primary" type="button" data-modal-open="create-process">Create Process</button>')
    h = h.replace('<span class="cell-title">Refund requests</span>', f'<a class="cell-title" href="#open-process-drawer" data-modal-open="process-drawer" {LINK}>Refund requests</a>')
    h = h.replace('<span class="body-semibold">Refund requests</span>', f'<a class="body-semibold" href="#open-process-drawer" data-modal-open="process-drawer" {LINK}>Refund requests</a>')
    h = h.replace('<button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="View RACI">', '<button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="View RACI" data-modal-open="raci-drawer">')
    h = toggle(h, 'Filters', 'filters-panel')
    h = h.replace('<button class="btn btn-ghost btn-xs" type="button">Expand all</button>', '<button class="btn btn-ghost btn-xs" type="button" data-expand-all>Expand all</button>')
    h = swap_table(h, tree_table(PROC_TREE, cols=('status', 'acc', 'rob', 'actions'), kinds=('Process', 'Activity', 'Sub-activity'), prefix='proc', sticky=False, attrs=' data-view="desktop"',
                                 tags=lambda name, level: tag('Northwind Hire', 'blue-light') if name == 'Northwind Hire' else '',
                                 links={'Refund requests': 'href="#open-process-drawer" data-modal-open="process-drawer"'}))
    h = h.replace('aria-label="View RACI">', 'aria-label="View RACI" data-modal-open="raci-drawer">')
    return with_views(h, *processes_views(), extra_panels=work_filters('Process', ('Process', 'Activity', 'Sub-activity')))


def peer_feedback_with_states():
    h = with_tabs(peer_feedback(), 'feedback', feedback_panels())
    return h.replace('<button class="btn btn-secondary btn-xs" type="button">Give Feedback</button>', '<button class="btn btn-secondary btn-xs" type="button" data-modal-open="give-feedback">Give Feedback</button>')


def sign_in():
    return f'''    <div class="stack" style="align-items: center; gap: var(--spacing-6)">
      <img class="sidenav-logo" src="../../../designmd/assets/logo-dark.svg" alt="Operationalize" />
      <div class="stack" style="align-items: center; justify-content: center; min-height: 60vh; width: 100%; max-width: 500px; gap: var(--spacing-4)">
        <h1 class="h2" style="margin: 0 0 var(--spacing-2)">Log in to Operationalize</h1>
        <button class="btn btn-secondary" type="button" style="width: 100%">{icon("i-google", "btn-icon")}Log in with Google</button>
      </div>
    </div>'''


# Every state built so far: screen folder, name, kind, and the address that opens it.
STATES = (
    [('profile', n, 'Tab', f'#tab-{i}') for i, n in enumerate(('Initiatives', 'Processes', 'Work History', 'RoB Meetings', 'Action Items', 'Time Off'), 1)]
    + [('team-profile', n, 'Tab', f'#tab-{i}') for i, n in enumerate(('OKRs', 'Initiatives', 'Processes', 'Time off', 'RoB Meetings'), 1)]
    + [('people', n, 'Tab', f'#tab-{i}') for i, n in enumerate(('Reporting relationships', 'Geography'), 1)]
    + [('team', n, 'Tab', f'#tab-{i}') for i, n in enumerate(('Divisions', 'Talent Network Members', 'Skills'), 1)]
    + [('okrs', n, 'Tab', f'#tab-{i}') for i, n in enumerate(('Company Objective', 'Function Annual', 'Function Quarterly', 'Team Quarterly', 'Shared Key Results'), 1)]
    + [('initiative-view', 'Activity log', 'Tab', '#tab-1'), ('watercooler', 'Top Messages', 'Tab', '#tab-1'), ('time-off', 'OOO details', 'Tab', '#tab-1'),
       ('recognitions', 'Badges', 'Tab', '#tab-1'), ('peer-feedback', 'Received', 'Tab', '#tab-1'), ('peer-feedback', 'Given', 'Tab', '#tab-2'),
       ('profile-edit', 'Work', 'Tab', '#tab-1'), ('profile-edit', 'Contacts', 'Tab', '#tab-2'), ('talent-profile', 'Processes', 'Tab', '#tab-1'),
       ('processes', 'Process drawer', 'Drawer', '#open-process-drawer'), ('processes', 'Create Process', 'Drawer', '#open-create-process'),
       ('processes', 'RACI', 'Drawer', '#open-raci-drawer'), ('processes', 'Query panel', 'Panel', '#open-query-panel'),
       ('peer-feedback', 'Give feedback', 'Modal', '#open-give-feedback')])
STATES_2 = [
    ('processes', 'Compact view', 'View', '#show-view-1'), ('processes', 'Spreadsheet view', 'View', '#show-view-2'), ('processes', 'Filters', 'Panel', '#open-filters-panel'),
    ('processes', 'Process drawer, Activity log', 'Tab', '#open-process-drawer&show-pdrawer-1'),
    ('initiatives', 'Compact view', 'View', '#show-view-1'), ('initiatives', 'Spreadsheet view', 'View', '#show-view-2'), ('initiatives', 'Filters', 'Panel', '#open-filters-panel'),
    ('initiatives', 'Query panel', 'Panel', '#open-query-panel'),
    ('dashboard', 'Detailed view', 'View', '#show-view-0'), ('dashboard', 'Compact view', 'View', '#show-view-1'),
    ('rob-meetings', 'All events', 'Tab', '#tab-1'), ('rob-meetings', 'Schedule view', 'View', '#show-robview-0'), ('rob-meetings', 'Week view', 'View', '#show-robview-1'),
    ('rob-meetings', 'Filters', 'Panel', '#open-rob-filters'),
    ('okrs', 'Performance attributes', 'Modal', '#open-perf-attrs'), ('dashboard', 'User menu', 'Menu', '#open-user-menu'),
]
STATES_3 = [
    ('dashboard', 'Other initiatives', 'View', '#show-scope-1'), ('dashboard', 'More actions menu', 'Menu', '#open-dash-more'),
    ('okrs', 'A level with no OKRs', 'Tab', '#tab-4'), ('initiatives', 'RACI', 'Drawer', '#open-raci-drawer'),
    ('no-access', 'No rights to edit', 'Page', ''),
]
STATE_GROUPS = [(STATES, 4), (STATES_2, 6), (STATES_3, 7)]   # each list of states, and the pass that built it


# ------------------------------------------------------------ New elements
def library_page(title, kind, items):
    """The list of what this reference added to the kit: elements or icons.
    Each has See it in place and Add to library; what promote.py has moved
    into the kit stays listed, badged, and the filter picks those out."""
    icons = kind == 'icons'
    noun = 'icon' if icons else 'element'
    other = (f'<a href="../elements/index.html" {LINK}>New elements</a>' if icons else f'<a href="../icons/index.html" {LINK}>New icons</a>')
    intro = ((f'Icons and artwork the product has and the kit does not. These {len(items)} were drawn for the reference screens, coloured with the kit’s tokens, and kept in one sprite, <code>_src/icons.svg</code>. '
              if icons else
              f'What the product has and the kit does not. Each of these {len(items)} elements was built for the reference screens on the kit’s tokens, in one stylesheet, <code>_src/elements.css</code>. ')
             + f'<span class="body-semibold">Add to library</span> copies the request for that {noun}: paste it to Claude, or run the command in it, and the {noun} moves into the kit. '
               f'It stays on this page with an <span class="body-semibold">Added to library</span> badge, so the filter below gives developers the list of what they still have to implement. See also: {other}.')
    out = []
    try:
        import json as _json
        from pathlib import Path as _P
        here = _P(__file__).resolve()
        kit = next(p for p in (here.parents[3] / 'designmd' / 'dist' / 'kit.json', here.parents[2] / 'designmd' / 'dist' / 'kit.json') if p.exists()).read_text()
        kit_icons = (here.parents[3] / 'designmd' / 'icons.svg').read_text() if (here.parents[3] / 'designmd' / 'icons.svg').exists() else (here.parents[2] / 'designmd' / 'icons.svg').read_text()
    except Exception:
        kit = kit_icons = ''
    try:   # what promote.py has moved into the library, and when
        added = _json.loads((_P(__file__).resolve().parent / 'promoted.json').read_text())
    except Exception:
        added = {}
    n_added = 0
    for name, cls, where, link, demo in items:
        slug = cls.replace('ps-', 'el-')
        code = cls if icons else '.' + cls
        ask = f'Add the {name} {noun} ({code}) from production-site-2026-11-25 to the Icarus library: python3 production-site-2026-11-25/_src/promote.py {cls}'
        inlib = cls in added or (f'id="{cls}"' in kit_icons if icons else f'"{cls}"' in kit)
        n_added += inlib
        lib = (tag('Added to library' + (' · ' + added[cls] if cls in added else ''), 'positive') if inlib else
               f'<button class="btn btn-secondary btn-xs" type="button" data-add-to-library="{ask}">{icon("i-plus", "btn-icon")}<span>Add to library</span></button>')
        out.append(f'<section class="stack" id="{slug}" data-lib="{"added" if inlib else "new"}" style="gap: var(--spacing-3); padding: var(--spacing-6) 0; border-top: 1px solid var(--color-border)">'
                   f'<div class="row" style="flex-wrap: wrap; justify-content: space-between"><div><h2 class="h3" style="margin: 0">{name}</h2>'
                   f'<p class="body-sm" style="margin: var(--spacing-1) 0 0; color: var(--color-text-muted)">{where}</p></div>'
                   f'<div class="row"><code class="body-sm">{code}</code><a class="btn btn-secondary btn-xs" href="../{link}" style="text-decoration: none">See it in place</a>{lib}</div></div>{demo}</section>')
    return f'''    <p class="body-sm" style="margin: 0 0 var(--spacing-2)"><a href="../index.html" {LINK}>Production site · Nov 25, 2026</a></p>
    <h1 class="h1" style="margin: 0 0 var(--spacing-2)">{title}</h1>
    <p class="body" style="margin: 0 0 var(--spacing-6); max-width: 760px; color: var(--color-text-muted)">{intro}</p>
    <div class="segmented" role="group" aria-label="Shown" data-lib-filter style="margin-bottom: var(--spacing-6)">
      <button class="segmented-item is-active" type="button" data-show="all">All {len(items)}</button>
      <button class="segmented-item" type="button" data-show="added">Added to library {n_added}</button>
      <button class="segmented-item" type="button" data-show="new">Not in library yet {len(items) - n_added}</button>
    </div>
    <p class="body-sm" data-lib-none hidden style="margin: 0; color: var(--color-text-muted)">Nothing here yet.</p>
    {"".join(out)}
    <script>
    const filter = show => {{
      let n = 0;
      document.querySelectorAll('section[data-lib]').forEach(s => {{ const on = show === 'all' || s.dataset.lib === show; s.style.display = on ? '' : 'none'; n += on; }});
      document.querySelectorAll('[data-lib-filter] .segmented-item').forEach(b => b.classList.toggle('is-active', b.dataset.show === show));
      document.querySelector('[data-lib-none]').hidden = n > 0;
    }};
    document.addEventListener('click', e => {{
      const f = e.target.closest('[data-lib-filter] .segmented-item');
      if (f) {{ filter(f.dataset.show); history.replaceState(null, '', '#' + f.dataset.show); }}
    }});
    if (['added', 'new'].includes(location.hash.slice(1))) filter(location.hash.slice(1));
    document.addEventListener('click', e => {{
      const b = e.target.closest('[data-add-to-library]');
      if (!b) return;
      const label = b.querySelector('span'), done = () => {{ label.textContent = 'Copied. Paste it to Claude'; setTimeout(() => {{ label.textContent = 'Add to library'; }}, 2500); }};
      navigator.clipboard ? navigator.clipboard.writeText(b.dataset.addToLibrary).then(done, () => prompt('Copy this request:', b.dataset.addToLibrary)) : prompt('Copy this request:', b.dataset.addToLibrary);
    }});
    </script>'''


# What the product has and the kit does not, built in elements.css (ps-*).
# The functions below replace the kit stand-ins the first passes used.
def barchart(items):
    top = max(v for _, v, _ in items) or 1
    cols = ''.join(
        f'<div class="ps-bar{" " + cls if cls else ""}{" is-empty" if not v else ""}"><div class="ps-bar-col body-sm" style="height: {max(14, round(100 * v / top))}%">{v}</div>'
        f'<span class="ps-bar-label body-xs">{l}</span></div>' for l, v, cls in items)
    return f'<div class="ps-bars" role="img" aria-label="Initiatives by status">{cols}</div>'


def healthbar(ok, risk, off, rest):
    total = ok + risk + off + rest
    seg = ''.join(f'<span class="{c}" style="width: {100 * v / total:.2f}%"></span>' for c, v in (('is-success', ok), ('is-warning', risk), ('is-danger', off)) if v)
    return f'<div class="ps-health" role="img" aria-label="{round(100 * ok / total)}% on track">{seg}</div>'


def pager(pages=('1', '2', '3', '…', '6')):
    b = ''.join('<span class="ps-page-gap">…</span>' if p == '…' else f'<button class="ps-page{" is-current" if p == "1" else ""}" type="button"{" aria-current=" + chr(34) + "page" + chr(34) if p == "1" else ""}>{p}</button>' for p in pages)
    return f'<nav class="ps-pagination" aria-label="Pages"><button class="ps-page" type="button" disabled>Prev</button>{b}<button class="ps-page" type="button">Next</button></nav>'


EMPTY_ART = {'i-recognize': 'i-art-empty-list', 'i-cpu-2': 'i-art-empty-alert'}


def empty_state(ic, title, text):
    if ic in EMPTY_ART:
        return (f'<div class="ps-empty">{art(EMPTY_ART[ic], 96)}<p class="body-semibold" style="margin: 0">{title}</p>'
                f'<p class="body-sm" style="margin: 0; color: var(--color-text-muted)">{text}</p></div>')
    return (f'<div class="ps-empty"><span class="ps-empty-art">{icon(ic)}</span><p class="body-semibold" style="margin: 0">{title}</p>'
            f'<p class="body-sm" style="margin: 0; color: var(--color-text-muted)">{text}</p></div>')


def cal_month(weeks, events, more=None, today=25):
    heads = ''.join(f'<div class="ps-cal-head body-xs-semibold">{d}</div>' for d in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'))
    cells = ''
    for w in weeks:
        for d in w:
            if d is None:
                cells += '<div class="ps-cal-day"></div>'
                continue
            ev = ''.join(f'<a class="ps-cal-event{" is-mine" if mine else ""}" href="../rob-meeting-view/index.html"><span class="ps-cal-event-title body-sm">{t}</span>'
                         f'<span class="ps-cal-event-meta body-xs">{m}</span></a>' for t, m, mine in events(d))
            extra = f'<a class="ps-cal-more body-xs-semibold" href="#">{more[d]} More</a>' if more and d in more else ''
            cells += f'<div class="ps-cal-day{" is-today" if d == today else ""}"><span class="ps-cal-num body-xs">{d:02d}</span>{ev}{extra}</div>'
    return f'<div class="ps-cal-scroll"><div class="ps-cal">{heads}{cells}</div></div>'


def week_grid(events=()):
    hours = ['9:00am', '10:00am', '11:00am', '12:00pm', '1:00pm', '2:00pm', '3:00pm', '4:00pm', '5:00pm']
    ev = dict(events)
    out = '<div class="ps-week-head body-xs">GMT+1</div>' + ''.join(f'<div class="ps-week-head body-xs-semibold">{d} {n}</div>' for d, n in (('Monday', 23), ('Tuesday', 24), ('Wednesday', 25), ('Thursday', 26), ('Friday', 27)))
    for h in hours:
        out += f'<div class="ps-week-time body-xs">{h}</div>'
        for d in range(5):
            e = ev.get((d, h))
            out += '<div class="ps-week-slot">' + (f'<a class="ps-cal-event is-mine" href="../rob-meeting-view/index.html"><span class="ps-cal-event-title body-sm">{e[0]}</span><span class="ps-cal-event-meta body-xs">{h} {e[1]}</span></a>' if e else '') + '</div>'
    return f'<div class="ps-cal-scroll"><div class="ps-week">{out}</div></div>'


def month_table(title, first, days, marks=()):
    cells = [('', 'is-outside')] * first + [(str(d), 'is-off' if d in marks else '') for d in range(1, days + 1)]
    while len(cells) % 7:
        cells.append(('', 'is-outside'))
    body = ''.join(f'<span class="ps-month-dow body-xs">{d}</span>' for d in ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'))
    body += ''.join(f'<span class="ps-month-day body-sm{" " + c if c else ""}{" is-weekend" if i % 7 > 4 else ""}">{d}</span>' for i, (d, c) in enumerate(cells))
    return f'<div style="flex: 1 1 280px; min-width: 0; max-width: 360px"><h3 class="body-semibold" style="margin: 0 0 var(--spacing-2)">{title}</h3><div class="ps-month">{body}</div></div>'


def ooo_grid(days, people):
    wk = {28, 29, 5, 6}
    head = '<div class="ps-ooo-head body-xs" style="text-align: left; padding-left: var(--spacing-3)">Name, Position</div>' + ''.join(
        f'<div class="ps-ooo-head body-xs{" is-weekend" if d in wk else ""}">{d:02d}</div>' for d in days)
    rows = ''
    for k, off in people:
        rows += f'<div class="ps-ooo-name">{user(k)}</div>' + ''.join(f'<div class="ps-ooo-cell{" is-off" if d in off else ""}{" is-weekend" if d in wk else ""}"></div>' for d in days)
    return (f'<div class="ps-cal-scroll"><div class="ps-ooo" style="grid-template-columns: minmax(220px, 1.5fr) repeat({len(days)}, minmax(28px, 1fr))" role="img" aria-label="Who is out of office on which day">'
            f'{head}{rows}</div></div>')


def tree_node(k, current=False):
    n, r = PEOPLE[k]
    return (f'<a class="ps-tree-node{" is-current" if current else ""}" href="../profile/index.html"><span class="ps-tree-dot"></span>'
            f'<span><span class="ps-tree-name body-sm-semibold">{n}</span><span class="ps-tree-role body-xs">{r}</span></span></a>')


def reporting_tree():
    return (f'<ul class="ps-tree"><li>{tree_node("ho")}<ul><li>{tree_node("sr")}<ul><li>{tree_node("lk")}<ul><li>{tree_node("ck", True)}<ul><li>{tree_node("lh")}</li><li>{tree_node("tl")}</li></ul></li>'
            f'<li>{tree_node("nr")}</li></ul></li><li>{tree_node("el")}</li></ul></li><li>{tree_node("ac")}<ul><li>{tree_node("jp")}</li><li>{tree_node("mv")}</li></ul></li><li>{tree_node("ad")}</li><li>{tree_node("og")}</li></ul></li></ul>')


def map_panel(pins, count=None, small=False):
    dots = ''.join(f'<span class="ps-map-pin" style="left: {x}%; top: {y}%"></span>' for x, y in pins)
    label = f'<span class="ps-map-count body-xs">{count}</span>' if count else ''
    return f'<div class="ps-map{" is-small" if small else ""}" role="img" aria-label="Map of where people are">{dots}{label}</div>'


PINS = [(18, 34), (22, 52), (27, 41), (31, 30), (36, 47), (40, 38), (44, 55), (47, 33), (52, 44), (55, 61), (58, 36), (63, 50), (67, 42), (72, 58), (76, 35), (81, 49), (24, 66), (49, 70), (60, 24), (70, 72)]


def okr_card(name, st, kind, krs, counters=True):
    c = (tag(icon("i-cpu-2", "icon") + " 1") + tag(icon("i-initiatives", "icon") + " 2") + tag(icon("i-okr", "icon") + " 0")) if counters else ''
    rows = ''.join(f'<div class="ps-okr-kr"><span class="body-sm">{kr}</span><span class="row">{c}<span class="ps-okr-pct body-sm">{p}%</span></span></div>' for kr, p in krs)
    return f'<article class="ps-okr"><div class="ps-okr-head"><h3 class="body-lg-semibold" style="margin: 0">{name}</h3>{tag(st, kind)}</div>{rows}</article>'


def editor(placeholder=''):
    b = lambda label, ic: f'<button class="editor-toolbar-btn" type="button" aria-label="{label}">{icon(ic, "icon icon-16")}</button>'
    return (f'<div class="editor"><div class="editor-toolbar"><div class="input-select editor-toolbar-select"><button class="input-select-trigger" aria-expanded="false" type="button"><span class="input-select-value">Normal Text</span>{icon("i-chevron-down", "btn-icon")}</button>'
            f'<div class="dropdown-menu" hidden><button class="dropdown-item" type="button">Normal Text</button><button class="dropdown-item" type="button">Heading 1</button><button class="dropdown-item" type="button">Heading 2</button></div></div>'
            f'<span class="editor-toolbar-divider"></span>{b("Bold", "i-bold")}{b("Italic", "i-italic")}<span class="editor-toolbar-divider"></span>{b("Bulleted list", "i-list-bullet")}{b("Numbered list", "i-list-ordered")}'
            f'<span class="editor-toolbar-divider"></span>{b("Link", "i-link")}</div><div class="editor-content" contenteditable="true" data-placeholder="{placeholder}"></div></div>')


def filters_panel(pid, rows):
    body = ''.join(f'<div {PAIR}><span class="body-sm-semibold" style="flex: 0 0 140px">{l}</span><div class="row" style="flex: 1 1 240px; min-width: 0; flex-wrap: wrap">{c}</div></div>' for l, c in rows)
    return (f'<div class="ps-popover-anchor"><div class="ps-popover" id="{pid}" hidden><div class="row" style="justify-content: space-between; margin-bottom: var(--spacing-4)">'
            f'<span class="body-semibold">Filters</span><a class="body-sm-semibold" href="#" {LINK}>Clear all</a></div><div class="stack">{body}</div></div></div>')


def child_rows(html, anchor_text, rid, children, cols):
    """Give one row of a work list a caret and the rows that fold under it."""
    m = _re.search(r'<a class="cell-title"[^>]*' + _re.escape(anchor_text), html)   # the table's link, not the phone card's
    assert m, anchor_text
    a, i = m.start(), m.end()
    caret = (f'<button class="row-toggle" type="button" aria-expanded="false" aria-label="Toggle children" data-rows="{rid}">{icon("i-caret-right")}</button> ')
    html = html[:a] + caret + html[a:]
    end = html.index('</tr>', i) + len('</tr>')
    kids = ''.join(f'<tr class="ps-row-child" data-child-of="{rid}" hidden>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>' for row in children)
    assert all(len(r) == cols for r in children)
    return html[:end] + kids + html[end:]


_rob_meeting_view, _profile, _tpp, _okrs = rob_meeting_view, profile, team_profile_panels, okrs


def profile():
    card = f'<article class="card"><div class="row">{icon("i-pin", "icon icon-16")}<span class="body-sm">Dublin, Ireland</span></div></article>'
    h = _profile()
    assert h.count(card) == 1
    return h.replace(card, map_panel([(46, 52)], 'Dublin, Ireland', small=True))


def team_profile_panels():
    p = _tpp()
    days = list(range(23, 31)) + list(range(1, 7))
    p[3] = (f'<div class="toolbar" style="margin-bottom: var(--spacing-4)">{period_nav("Nov 2026")}<span class="toolbar-spacer"></span>'
            f'{select("Direct members, Associated members", label="Members shown", width=220)}<div style="width: 180px">{text_in("Name")}</div>{ph_select("Position", "Position", 180)}</div>'
            + ooo_grid(days, [('lk', ()), ('ck', (26, 27)), ('lh', ()), ('tl', (30, 1, 2)), ('nr', ())]))
    return p


def people_panels():
    tree = (f'<div style="max-width: 280px; margin-bottom: var(--spacing-6)"><div class="input-icon input-icon-left">{icon("i-search", "icon input-icon-glyph")}<input class="input" type="text" value="Cara Keane" aria-label="Search people" /></div></div>'
            + reporting_tree())
    geo = (f'<div class="toolbar" style="margin-bottom: var(--spacing-4)"><div class="input-icon input-icon-left toolbar-search">{icon("i-search", "icon input-icon-glyph")}<input class="input" type="text" placeholder="Search by name" aria-label="Search by name" /></div>'
           f'<span class="row" data-view="desktop">{ph_select("Team", "Team", 160)}{ph_select("Position", "Position", 160)}{ph_select("Location", "Location", 160)}{select("Active members", label="Membership", width=170)}</span></div>'
           + map_panel(PINS, '731 results shown (731 active members in total)'))
    return [tree, geo]


def okrs():
    h = _okrs()
    a = h.index('      <div class="stack">')
    b = h.index('<nav class="ps-pagination"') if '<nav class="ps-pagination"' in h else h.index('<div class="row" style="margin-top: var(--spacing-4)">')
    return h[:a] + '      ' + empty_state('i-okr', 'No OKRs found', 'No OKRs have been created for this level and period yet.')


def okr_panels():
    one = lambda *items: '<div class="stack">' + ''.join(okr_card(n, st, k, krs) for n, st, k, krs in items) + '</div>'
    return ['<div class="stack">' + ''.join(okr_card(*o) for o in OKRS) + '</div>' + pager(('1', '2')),
            one(('Operations: one handoff, not three', 'Active', 'positive', [('Contract to workspace handoff is automatic', 50), ('Kick-off checklist used on every engagement', 80)])),
            one(('Operations Q4: checklist live', 'Active', 'positive', [('Checklist in use on 20 engagements', 45)]), ('IT Q4: self-serve setup', 'Draft', 'light', [('Billing setup without a call', 10)])),
            empty_state('i-okr', 'No OKRs found', 'No OKRs have been created for this level and period yet.'),
            one(('Shared: time to first delivery', 'Active', 'positive', [('Median time to first delivery is 7 days', 64)]))]


def rob_calendar():
    weeks = [[2, 3, 4, 5, 6], [9, 10, 11, 12, 13], [16, 17, 18, 19, 20], [23, 24, 25, 26, 27], [30, None, None, None, None]]
    grid = cal_month(weeks, lambda d: [(t, m, True) for t, m in EVENTS.get(d, ())])
    return f'''{head("RoB Meetings", '<button class="btn btn-primary" type="button" disabled title="Creating meetings is closed for this account on staging">Create meeting</button>', after_title=icon("i-info", "icon icon-16"))}

      {tabs(("My events", "All events"))}

      <div class="toolbar" style="margin: var(--spacing-4) 0">
        <div class="input-icon input-icon-left toolbar-search">
          {icon("i-search", "icon input-icon-glyph")}
          <input class="input" type="text" placeholder="Search" aria-label="Search meetings" />
        </div>
        <button class="btn btn-secondary" type="button">{icon("i-filter", "btn-icon")}Filters</button>
        <span class="toolbar-spacer"></span>
        {segmented(("Schedule", "Week", "Month"), 2, "Calendar view")}
      </div>

      <div class="row" style="justify-content: space-between; margin-bottom: var(--spacing-3)">
        <h2 class="h3" style="margin: 0">November 2026</h2>
        <div class="row">
          <button class="btn btn-secondary btn-icon-only" type="button" aria-label="Previous month">{icon("i-arrow-long-left", "btn-icon")}</button>
          <button class="btn btn-secondary" type="button">Today</button>
          <button class="btn btn-secondary btn-icon-only" type="button" aria-label="Next month">{icon("i-arrow-long-right", "btn-icon")}</button>
        </div>
      </div>

      {grid}'''


P1 = ('btn-primary',)
SCREENS = [
    dict(folder='dashboard', title='TopTrack Dashboard', nav='Dashboard', main=dashboard_with_states(), route='/dashboard',
         ctas=[('btn-secondary', 'More actions', 'i-dots-three-vertical')]),
    dict(folder='processes', title='Processes', nav='Processes', main=processes_with_states(), overlays=process_overlays(), route='/bau/list',
         ctas=[('btn-primary', 'Create Process', 'i-plus')]),
    dict(folder='initiatives', title='Initiatives', nav='Initiatives', main=initiatives_with_states(), overlays=raci_overlay('Onboarding in one week'), route='/initiatives/list',
         ctas=[('btn-primary', 'Create Initiative', 'i-plus')]),
    dict(folder='initiative-view', title='Onboarding in one week', nav='Initiatives', main=with_tabs(initiative_view(), 'initiative', [activity_log()], suffix='      </div>'), route='/initiatives/:id', padded=False),
    dict(folder='initiative-create', title='New initiative', nav='Initiatives', main=initiative_create(), route='/initiatives/create', padded=False),
    dict(folder='rob-meetings', title='RoB Meetings', nav='RoB Meetings', main=rob_with_states(), route='/rob',
         ctas=[('btn-primary', 'Create meeting', 'i-plus')]),
    dict(folder='rob-meeting-view', title='RoB Meetings', nav='RoB Meetings', main=rob_calendar().replace('btn btn-primary', 'btn btn-secondary'),
         overlays=rob_meeting_view(), route='/rob?calendarId=…&externalId=…', ctas=[('btn-secondary', 'Create meeting', 'i-plus')]),
    dict(folder='okrs', title='OKRs', nav='OKRs', main=okrs_with_states(), overlays=perf_attrs_modal(), route='/okrs/list',
         ctas=[('btn-secondary', 'Performance attributes', 'i-info'), ('btn-secondary', 'Export as CSV', 'i-download'), ('btn-primary', 'Create OKR', 'i-plus')]),
    dict(folder='people', title='People', nav='People', main=with_tabs(people(), 'people', people_panels()), route='/people/directory'),
    dict(folder='profile', title='My Profile', nav='People', main=with_tabs(profile(), 'profile', profile_panels()), route='/people/:userId',
         ctas=[('btn-secondary', 'Edit profile', 'i-pencil')]),
    dict(folder='team', title='Organizational Structure', nav='Team', main=with_tabs(team(), 'team', team_panels()), route='/org-structure/org-units'),
    dict(folder='team-profile', title='Team Profile', nav='Team', main=with_tabs(team_profile(), 'teamprofile', team_profile_panels()), route='/teams/:teamId'),
    dict(folder='rob-paused-meetings', batch=2, title='View Paused Meetings', nav='RoB Meetings', main=paused_meetings(), route='/rob/paused-meetings'),
    dict(folder='profile-edit', batch=2, title='Edit Profile', nav='People', main=with_tabs(profile_edit(), 'profileedit', profile_edit_panels()), route='/people/:userId/edit'),
    dict(folder='watercooler', batch=2, title='Watercooler', nav='Watercooler', main=with_tabs(watercooler(), 'watercooler', [empty_state('i-chat', 'No Top Messages Available', 'Messages with the most reactions show up here.')]), route='/watercooler'),
    dict(folder='time-off', batch=2, title='Time off', nav=None, main=with_tabs(time_off(), 'timeoff', [ooo_details()]), route='/time-off'),
    dict(folder='recognitions', batch=2, title='Recognitions & Badges', nav=None, main=with_tabs(recognitions(), 'recognitions', [badges()]), route='/recognitions',
         ctas=[('btn-primary', 'Give recognition', 'i-plus')]),
    dict(folder='peer-feedback', batch=2, title='Peer Feedback', nav=None, main=peer_feedback_with_states(), overlays=give_feedback_modal(), route='/peer-feedbacks/:viewMode/:tab',
         ctas=[('btn-secondary', 'Request feedback', 'i-comment-ask'), ('btn-primary', 'Give feedback', 'i-plus')]),
    dict(folder='self-review', batch=2, title='Self-review', nav=None, main=self_review(), route='/self-review/:userId'),
    dict(folder='not-found', batch=2, title='Page not found', nav=None, main=not_found(), route='/404'),
    dict(folder='talent-profile', batch=3, title='Talent Network Member Profile', nav='Team', main=with_tabs(talent_profile(), 'talent', [empty_state('i-cpu-2', 'Rosa doesn’t own any Processes', 'No Processes yet')]), route='/talent/:talentId'),
    dict(folder='no-access', batch=7, title='Edit org unit', nav='Team', main=no_access(), padded=False, route='/teams/:teamId/edit'),
    dict(folder='sign-in', batch=5, plain=True, title='Log in', nav=None, main=sign_in(), route='/signin'),
    dict(folder='profile-public-edit', batch=3, title='Edit public profile', nav='People', main=public_profile_edit(), route='/people/:userId/edit-public-profile',
         ctas=[('btn-secondary', 'Cancel', 'i-x'), ('btn-primary', 'Save changes', 'i-check')]),
]


# Every primary screen the walk of the app found, by area: name, route, and the
# folder here once it is built.
INVENTORY = [
    ('Dashboard', [('TopTrack Dashboard', '/dashboard', 'dashboard')]),
    ('Processes', [('Processes', '/bau/list', 'processes')]),
    ('Initiatives', [('Initiatives', '/initiatives/list', 'initiatives'), ('Initiative', '/initiatives/:id', 'initiative-view'),
                     ('Create and edit initiative', '/initiatives/create', 'initiative-create')]),
    ('RoB Meetings', [('RoB Meetings calendar', '/rob', 'rob-meetings'), ('RoB meeting', '/rob?calendarId=…', 'rob-meeting-view'),
                      ('Create and edit meeting', '/rob/create-meeting/:step', None), ('Filters', '/rob/filters', None),
                      ('Paused meetings', '/rob/paused-meetings', 'rob-paused-meetings'), ('Slack card', '/rob/slack_cards/:id', None)]),
    ('OKRs', [('OKRs', '/okrs/list', 'okrs')]),
    ('People and profile', [('People', '/people/directory', 'people'), ('Profile', '/people/:userId', 'profile'),
                            ('Edit profile', '/people/:userId/edit', 'profile-edit'), ('Edit public profile', '/people/:userId/edit-public-profile', 'profile-public-edit'),
                            ('Create profile', '/people/create', None)]),
    ('Team and org structure', [('Organizational Structure', '/org-structure/org-units', 'team'), ('Team Profile', '/teams/:teamId', 'team-profile'),
                                ('Create org unit', '/org-structure/create', None), ('Edit org unit', '/teams/:teamId/edit', None),
                                ('Create division', '/org-structure/divisions/create', None), ('Edit division', '/org-structure/divisions/edit/:id', None),
                                ('Talent profile', '/talent/:talentId', 'talent-profile'), ('Create and edit talent', '/talent/create', None)]),
    ('Watercooler, Time off, Recognitions', [('Watercooler', '/watercooler', 'watercooler'), ('Time off', '/time-off', 'time-off'), ('Recognitions', '/recognitions', 'recognitions')]),
    ('Peer feedback', [('Peer feedback', '/peer-feedbacks/:viewMode/:tab', 'peer-feedback'), ('Give feedback', '/peer-feedbacks/:feedbackId/edit', None),
                       ('Feedback', '/peer-feedbacks/:feedbackId/view', None)]),
    ('Performance review and self-review', [
        ('Self-assessment', '/performance-review/self-assessment', None), ('Manager view', '/performance-review/manager/:tab', None),
        ('Assessments', '/performance-review/assessments', None), ('Edit assessment', '/performance-review/assessments/edit/:assessmentId', None),
        ('Assessment', '/performance-review/assessment/:reviewId/:userId', None), ('Reports', '/performance-review/reports', None),
        ('Cycle report', '/performance-review/reports/:cycleId', None), ('Reviewee breakdown', '/performance-review/reports/:cycleId/:revieweeId', None),
        ('Self-review', '/self-review/:userId', 'self-review'), ('Team self-review', '/self-review/team', None)]),
    ('Outside the main navigation', [('Sign in', '/signin', 'sign-in'), ('Sign up', '/signup', None), ('Forgot password', '/forgot-password', None),
                                     ('Reset password', '/reset-password', None), ('Page not found', '/404', 'not-found'), ('Onboarding', '/onboarding', None),
                                     ('Demo: create a Process', '/demo/create-a-process', None), ('Demo: create an Initiative', '/demo/create-an-initiative', None)]),
    ('Admin settings', [(n, r, None) for n, r in (
        ('Settings', '/admin/settings'), ('Permissions', '/admin/permissions'), ('Roles management', '/admin/settings/roles-management'),
        ('Roles', '/admin/settings/roles-management/roles'), ('Users', '/admin/settings/roles-management/users'), ('Positions', '/admin/positions'),
        ('Org unit types', '/admin/org-unit-types'), ('OKR levels', '/admin/okr-levels'), ('Channel browser', '/admin/channel-browser'),
        ('Newcomers email', '/admin/newcomers-email'), ('Salary data', '/admin/salary-data'),
        ('Performance review templates', '/admin/performance-review-templates'), ('Performance review template', '/admin/performance-review-templates/:id'),
        ('Performance review cycles', '/admin/performance-review-cycles'), ('Performance review cycle', '/admin/performance-review-cycles/:id'),
        ('Integrations', '/admin/integrations'), ('Integration streams', '/admin/integrations/:connector/streams/:id'))]),
    ('Planning cycles', [('Planning cycles', '/planning-cycles/cycles', None), ('Create planning cycle', '/planning-cycles/create', None),
                         ('Planning cycle builder', '/planning-cycles/builder/:cycleId', None)]),
]


# The work log: one entry per sitting. Minutes are wall-clock time from the
# request to the finished, checked batch, read from file and commit timestamps.
# A screen's build time is its batch's minutes divided by the batch's screens.
BATCHES = {
    1: dict(date='Nov 25, 2026', span='09:51–10:06', minutes=15,
            note='Includes the one-off setup: the folder, the build script, the phone layouts and this list.'),
    2: dict(date='Nov 25, 2026', span='10:08–10:14', minutes=6,
            note='Capturing eight more screens on staging and building them.'),
    3: dict(date='Nov 25, 2026', span='10:16–10:19', minutes=4,
            note='Mostly spent finding what staging lets this account open; two screens came out of it.'),
    5: dict(date='Nov 25, 2026', span='10:46–10:52', minutes=6,
            note='Staging signed the account out mid-pass, which showed the sign-in page; nothing else could be captured.'),
    7: dict(date='Nov 25, 2026', span='11:16–11:18', minutes=4, states=True,
            note='Little of what is left opens for this account on staging: Create OKR and Create meeting are disabled, and the top-bar popovers did not open.'),
    6: dict(date='Nov 25, 2026', span='11:10–11:14', minutes=6, states=True,
            note='View modes, filter and query panels, the calendar views, the Performance attributes modal and the account menu.'),
    4: dict(date='Nov 25, 2026', span='10:21–10:27', minutes=8, states=True,
            note='The other tabs of every built screen, the Processes drawers and query panel, and the give-feedback modal.'),
}
# Why a screen is not built yet, where the reason is known.
BLOCKED = {
    'No access on staging': ['Create org unit', 'Edit org unit', 'Create division', 'Edit division', 'Create and edit talent', 'Create profile',
                             'Create and edit meeting'] + [n for a, rows in INVENTORY if a in ('Admin settings', 'Planning cycles') for n, _, _ in rows],
    'Errors on staging': ['Self-assessment', 'Manager view', 'Assessments', 'Edit assessment', 'Assessment', 'Reports', 'Cycle report', 'Reviewee breakdown'],
    'Not a separate screen on desktop': ['Filters'],
    'Full-screen page the kit has no layout for': ['Onboarding', 'Demo: create a Process', 'Demo: create an Initiative'],
    'Redirects to Sign in on this tenant, which logs in with Google only': ['Sign up', 'Forgot password', 'Reset password'],
}
WHY = {n: reason for reason, names in BLOCKED.items() for n in names}
# Where each screen lives on staging, for the floating "Open on staging" link.
# exact=False: the screen needs a record id this reference does not keep, so
# the link opens the nearest list and the record is one click from there.
STAGING_HOST = 'https://team-staging.toptal.net'
STAGING = {
    'dashboard': ('/dashboard', True), 'processes': ('/bau/list', True), 'initiatives': ('/initiatives/list', True),
    'initiative-view': ('/initiatives/list', False), 'initiative-create': ('/initiatives/create', True),
    'rob-meetings': ('/rob', True), 'rob-meeting-view': ('/rob', False), 'okrs': ('/okrs/list', True),
    'people': ('/people/directory', True), 'profile': ('/people/me', True), 'team': ('/org-structure/org-units', True),
    'team-profile': ('/teams/1103', True), 'rob-paused-meetings': ('/rob/paused-meetings', True), 'profile-edit': ('/people/me/edit', True),
    'watercooler': ('/watercooler', True), 'time-off': ('/time-off', True), 'recognitions': ('/recognitions', True),
    'peer-feedback': ('/peer-feedbacks', True), 'self-review': ('/self-review/me', True), 'not-found': ('/404', True),
    'talent-profile': ('/org-structure/talents', False), 'no-access': ('/teams/1103/edit', True), 'sign-in': ('/signin', True),
    'profile-public-edit': ('/people/me/edit-public-profile', True),
}


# The staging address of each tab, in the order of the screen's tab strip, so
# the link follows the tab that is open. RoB Meetings and OKRs are not here:
# their tabs do not have a stable address on staging.
STAGING_TABS = {
    'profile': ['/people/me', '/people/me/initiatives', '/people/me/bau', '/people/me/work-history', '/people/me/rob', '/people/me/action-items', '/people/me/time-off'],
    'team-profile': ['/teams/1103/structure', '/teams/1103/OKRs', '/teams/1103/initiatives', '/teams/1103/bau', '/teams/1103/time-off', '/teams/1103/RoB'],
    'people': ['/people/directory', '/people/reporting-relationships', '/people/geography'],
    'team': ['/org-structure/org-units', '/org-structure/divisions', '/org-structure/talents', '/org-structure/skills'],
    'time-off': ['/time-off/summary', '/time-off/events'],
    'recognitions': ['/recognitions', '/recognitions/badges'],
    'watercooler': ['/watercooler/channels', '/watercooler/top-messages'],
    'peer-feedback': ['/peer-feedbacks/individual-contributor/pending', '/peer-feedbacks/individual-contributor/received', '/peer-feedbacks/individual-contributor/given'],
}


def staging_link(folder):
    if folder not in STAGING:
        return ''
    path, exact = STAGING[folder]
    tip = 'Open this screen on staging in a new tab' if exact else 'Staging needs a record id for this screen: opens the nearest list in a new tab'
    tabs_ = STAGING_TABS.get(folder, [])
    follow = '' if not tabs_ else ("""  <script>
  (() => {   // the staging link follows the open tab
    const a = document.querySelector('.ps-staging'), strip = document.querySelector('.tabs[data-tabs]');
    if (!a || !strip) return;
    const paths = a.dataset.stagingTabs.split(' ');
    const sync = () => { const i = [...strip.querySelectorAll('.tab')].findIndex(t => t.classList.contains('is-active')); if (paths[i]) a.href = a.dataset.stagingHost + paths[i]; };
    document.addEventListener('click', () => setTimeout(sync, 0));
    addEventListener('hashchange', () => setTimeout(sync, 0));
    setTimeout(sync, 0);
  })();
  </script>
""")
    data = f' data-staging-host="{STAGING_HOST}" data-staging-tabs="{" ".join(tabs_)}"' if tabs_ else ''
    raised = ' is-raised' if folder in ('initiative-create',) else ''   # a bar of form buttons sits at the bottom of these
    return (f'  <a class="btn btn-secondary ps-staging{raised}" href="{STAGING_HOST}{path}" target="_blank" rel="noopener" title="{tip}"{data}>'
            f'{icon("i-external-link", "btn-icon")}{"Open on staging" if exact else "Staging: nearest list"}</a>\n' + follow)


UPDATES = [  # one dict(date, span, minutes, screens=[folders] or 'all', note) per update pass
    dict(date='Nov 25, 2026', span='11:56–12:01', minutes=8, screens='all',
         note='Fifteen elements the kit lacks were built and put in place of the stand-ins on every screen; rows fold, the search box filters, filters drop as a popover.'),
    dict(date='Nov 25, 2026', span='12:14–12:17', minutes=6,
         screens=['dashboard', 'processes', 'initiatives', 'people', 'profile', 'time-off', 'peer-feedback', 'rob-paused-meetings', 'talent-profile', 'team', 'team-profile', 'initiative-view', 'initiative-create'],
         note='Compared with staging: lists are striped, every row has its caret, the toolbar is ordered as in the product, and the RoB and action cells carry their icons.'),
    dict(date='Nov 25, 2026', span='12:20–12:21', minutes=5,
         screens=['rob-meeting-view', 'initiative-view', 'rob-meetings', 'talent-profile', 'time-off', 'peer-feedback'],
         note='Compared with staging: the meeting view gains its Deck section, key metric row, priority and recording tags, RACI letters and attendance marks; smaller fixes on five more screens.'),
    dict(date='Nov 25, 2026', span='12:23–12:26', minutes=6,
         screens=['profile', 'team-profile', 'team', 'initiative-create', 'profile-edit'],
         note='Compared with staging: Work History is a timeline with checkboxes, Time Off and the RoB tab have their period navigation and radios, lists of org units are striped, and two forms get their icons and hints.'),
    dict(date='Nov 25, 2026', span='12:28–12:34', minutes=6,
         screens=['profile', 'team-profile', 'team', 'time-off', 'processes'],
         note='Compared the remaining tabs and drawers with staging: Action Items is the grey box with its done mark, Show is a row of radios, talents carry the T mark and a manager with a picture, OOO details has its own type and status filters, and Create Process folds its optional fields under More details.'),    dict(date='Nov 25, 2026', span='12:34–12:41', minutes=7,
         screens=['dashboard', 'rob-meetings', 'profile', 'processes', 'initiatives'],
         note='Compared the phone versions with staging: the dashboard list is cards with its own search, filter and sort, the status chart scrolls sideways, RoB Meetings is a small month with the day’s agenda, and the profile header and fields sit two across.'),    dict(date='Nov 25, 2026', span='12:59–13:04', minutes=5, screens=[],
         note='Compared the remaining phone screens with staging and found nothing to change. Each new element got an Add to library button, with the script that moves it into the kit.'),    dict(date='Nov 25, 2026', span='13:05–13:10', minutes=5, screens=[],
         note='Elements page: an element moved into the library stays listed with an Added to library badge and the date, and a filter on top shows all, added, or not yet in the library.'),    dict(date='Nov 25, 2026', span='13:09–13:17', minutes=8,
         screens=['recognitions', 'profile', 'team-profile', 'talent-profile', 'processes', 'initiatives', 'dashboard', 'initiative-view', 'initiative-create'],
         note='Twelve icons the kit lacks were drawn and put in place: open in new tab, Slack in colour, the eight badges and the two empty-state drawings. They have their own list with See it in place and Add to library.'),    dict(date='Nov 25, 2026', span='13:18–13:22', minutes=4, screens='all',
         note='Every screen has a floating Open on staging link that opens the same view on the staging server in a new tab, for comparing the two.'),    dict(date='Nov 25, 2026', span='13:21–13:28', minutes=7,
         screens=['profile', 'team-profile', 'people', 'team', 'time-off', 'recognitions', 'watercooler', 'peer-feedback'],
         note='The Open on staging link follows the open tab on eight screens: it opens that same tab on staging.'),    dict(date='Nov 25, 2026', span='13:28–13:35', minutes=7, screens=['dashboard'],
         note='Dashboard rebuilt against staging, side by side: the list is a tree that opens a second and a third layer, with the name column held in place, the Roadmap, RoB Meeting and Actions columns, struck-through past meetings, the column and sort controls, and the card’s rule and health pills. Four elements and one icon were added to the lists.'),    dict(date='Nov 25, 2026', span='13:34–13:39', minutes=5, screens=['processes', 'initiatives'],
         note='Processes and Initiatives rebuilt against staging: both lists are the same tree as the dashboard, opening activities and sub-activities, projects and sub-projects, with struck-through past meetings and the roadmap marker.'),    dict(date='Nov 25, 2026', span='13:38–13:41', minutes=3, screens=['team', 'people', 'okrs'],
         note='Compared with staging: org units are plain striped rows that open their sub-units, the People list has its sort arrow and heavier names, and Create OKR is disabled as it is for this account.'),    dict(date='Nov 25, 2026', span='13:41–13:46', minutes=5, screens=['profile', 'team-profile', 'rob-meetings'],
         note='Compared with staging: the profile’s reporting relationships are the left-to-right chain with the person marked among the people beside them, Team Profile lists its talent network members in a second column, and Create meeting is disabled as it is for this account.'),    dict(date='Nov 25, 2026', span='13:45–13:49', minutes=4, screens='all',
         note='Compared Time off, Watercooler and Peer Feedback with staging; they were close. The side menu on every screen now ends as the product does for this account: a group that opens to Confluence, Watercooler and TopTaste, and the Learning hub with its three items, instead of Admin Settings. Peer Feedback has its line under the title and Time off a narrower search.'),    dict(date='Nov 25, 2026', span='13:49–13:52', minutes=3, screens=['initiative-view', 'initiative-create'],
         note='Compared the initiative view with a real one on staging; it was close. Connections now has Tags and the Agenda block, Projects is a list of link rows, the status tag is grey as there, and the staging link no longer covers the form’s Create button.'),    dict(date='Nov 25, 2026', span='13:56–14:00', minutes=4, screens=['initiative-create', 'profile-edit', 'rob-meeting-view'],
         note='Compared two forms and the meeting view with staging; all three were close. The initiative form’s fields span the main column, Edit Profile has month and day side by side and a plain About box, and the meeting’s Agenda lists items under This meeting and Other meetings.'),    dict(date='Nov 25, 2026', span='14:00–14:04', minutes=4, screens=['not-found', 'no-access', 'self-review', 'talent-profile', 'rob-paused-meetings', 'profile-public-edit'],
         note='Compared the last screens with staging. Paused meetings, the public-profile form, the talent profile and the self-review already matched. The 404 page has its drawing, the no-rights notice runs edge to edge, and the self-review’s staging link opens the page itself.'),    dict(date='Nov 25, 2026', span='14:04–14:09', minutes=5, screens=['processes', 'initiatives', 'dashboard'],
         note='Compact and spreadsheet views redone against staging: compact is the same tree with one line per row, spreadsheet is a numbered, ruled grid with every layer open and a description beside the name. The spreadsheet view drops the filter and sort controls, as there.'),    dict(date='Nov 25, 2026', span='14:17–14:23', minutes=6, screens='all',
         note='Measured staging’s sizes against ours and matched them on every screen: tighter page padding, tabs straight under the title, tables without an outer box, shorter rows, larger pictures. Blue main buttons where the product has them, OKRs opening empty as there, the dashboard’s other tab as a tree. Each screen now carries a match estimate.'),    dict(date='Nov 25, 2026', span='14:23–14:25', minutes=2, screens=['profile-edit', 'team'],
         note='Checked the tabs marked as not yet compared. Edit Profile was first compared while staging was still loading: its About box is a rich-text editor and Save Changes is green after all, so both are put back, and the form is filled in. Divisions rows lose their borders.'),
]


# How close each screen is to staging: my own estimate from putting the two side
# by side, not a measurement. The second item is what still differs.
MATCH = {
    'dashboard': (93, 'Actions column on staging not seen; spreadsheet view has its own columns'),
    'processes': (93, 'Rows under a process were not opened on staging; naming'),
    'initiatives': (95, 'Made-up data only'),
    'initiative-view': (93, 'No documents; fields filled where staging has dashes'),
    'initiative-create': (94, 'Only the first screen of the form was compared'),
    'rob-meetings': (90, 'Staging’s calendar was still loading when compared'),
    'rob-meeting-view': (92, 'R and A letters are square tags; deck is a title card'),
    'okrs': (90, 'Tabs after the first could not be read on staging'),
    'people': (96, 'Made-up data only'),
    'profile': (93, 'Name and role on two lines in the chain; photo and map are placeholders'),
    'team': (95, 'Skills rows are striped here, plain on staging'),
    'team-profile': (93, 'Logo is a generic icon; other tabs not re-compared'),
    'rob-paused-meetings': (96, 'Made-up data only'),
    'profile-edit': (95, 'Field labels on Work and Contacts match; their layout was compared by text only'),
    'watercooler': (95, 'Fewer channels, made-up text'),
    'time-off': (95, 'Made-up data only'),
    'recognitions': (95, 'Badges are redrawn, not copied'),
    'peer-feedback': (95, 'Made-up data only'),
    'self-review': (94, 'Compared by reading the text, not by eye'),
    'not-found': (96, 'Drawing is redrawn'),
    'talent-profile': (93, 'Compared by reading the text, not by eye'),
    'no-access': (96, 'Icon shape'),
    'sign-in': (None, 'Not compared: needs logging out of staging'),
    'profile-public-edit': (95, 'Only the first screen of the form was compared'),
}


def index():
    by_folder = {x['folder']: x for x in SCREENS}
    per_batch = {b: sum(1 for x in SCREENS if x.get('batch', 1) == b) for b in BATCHES}
    total = sum(len(rows) for _, rows in INVENTORY)
    done = sum(1 for _, rows in INVENTORY for r in rows if r[2])
    spent = sum(b['minutes'] for b in BATCHES.values() if not b.get('states'))
    spent_states = sum(b['minutes'] for b in BATCHES.values() if b.get('states'))
    titles = {name_folder[2]: name_folder[0] for _, rows in INVENTORY for name_folder in rows if name_folder[2]}
    avg = spent / done
    left = round((total - done) * avg)
    yes = '<svg class="icon icon-16" role="img" aria-label="Built" style="color: var(--color-success)"><use href="#i-done-solid"/></svg>'
    no = '<svg class="icon icon-16" role="img" aria-label="Not built" style="color: var(--color-text-subtle)"><use href="#i-bullet-outline"/></svg>'
    dash = f'<span class="body-sm" {MUTED}>—</span>'
    body = []
    for area, rows in INVENTORY:
        n = sum(1 for r in rows if r[2])
        body.append(f'<tr><td colspan="9"><span class="body-semibold">{area}</span> <span class="body-sm" {MUTED}>{n} of {len(rows)}</span></td></tr>')
        for name, route, folder in rows:
            if folder:
                b = by_folder[folder].get('batch', 1)
                mins = BATCHES[b]['minutes'] / per_batch[b]
                u = [x for x in UPDATES if x['screens'] == 'all' or folder in x['screens']]
                ud = f'<span class="body-sm">{u[-1]["date"]}</span>' if u else dash
                ut = f'<span class="body-sm">{u[-1]["minutes"] / (done if u[-1]["screens"] == "all" else len(u[-1]["screens"])):.1f} min</span>' if u else dash
                cells = (f'<td><a class="cell-title" href="{folder}/index.html" {LINK}>{name}</a></td><td><code class="body-sm">{route}</code></td>'
                         f'<td><span class="body-sm">{BATCHES[b]["date"]}</span></td><td><span class="body-sm">{mins:.1f} min</span></td><td>{ud}</td><td>{ut}</td>'
                         + (f'<td>{tag(str(MATCH[folder][0]) + "%", "positive" if MATCH[folder][0] >= 95 else "warning") if MATCH[folder][0] else dash}</td><td><span class="body-sm" {MUTED}>{MATCH[folder][1]}</span></td>'))
            else:
                why = f'<span class="body-sm" {MUTED}>{WHY[name]}</span>' if name in WHY else dash
                cells = (f'<td><span class="cell-title" {MUTED}>{name}</span></td><td><code class="body-sm">{route}</code></td>'
                         f'<td colspan="6">{why}</td>')
            body.append(f'<tr><td style="width: var(--spacing-10)">{yes if folder else no}</td>{cells}</tr>')
    srows = ''.join(
        f'<tr><td style="width: var(--spacing-10)">{yes}</td><td><span class="body-sm">{titles.get(f, "Edit org unit")}</span></td>'
        f'<td><a class="cell-title" href="{f}/index.html{h}" {LINK}>{n}</a></td><td>{tag(k)}</td><td><span class="body-sm">Nov 25, 2026</span></td>'
        f'<td><span class="body-sm">{BATCHES[b]["minutes"] / len(group):.1f} min</span></td><td>{dash}</td><td>{dash}</td></tr>' for group, b in STATE_GROUPS for f, n, k, h in group)
    n_states = sum(len(g) for g, _ in STATE_GROUPS)
    by_pass = {b: len(g) for g, b in STATE_GROUPS}
    log = ''.join(f'<tr><td><span class="body-sm-semibold">Build {b}</span></td><td><span class="body-sm">{v["date"]}, {v["span"]}</span></td>'
                  f'<td><span class="body-sm">{str(by_pass[b]) + " states" if v.get("states") else str(per_batch[b]) + " screens"}</span></td><td><span class="body-sm">{v["minutes"]} min</span></td>'
                  f'<td><span class="body-sm">{v["note"]}</span></td></tr>' for b, v in BATCHES.items())
    log += ''.join(f'<tr><td><span class="body-sm-semibold">Update</span></td><td><span class="body-sm">{u["date"]}, {u["span"]}</span></td>'
                   f'<td><span class="body-sm">{done if u["screens"] == "all" else len(u["screens"])} screens</span></td><td><span class="body-sm">{u["minutes"]} min</span></td>'
                   f'<td><span class="body-sm">{u["note"]}</span></td></tr>' for u in UPDATES)
    stats = ''.join(f'<div class="stat-card"><p class="stat-card-label">{l}</p><p class="stat-card-value">{v}</p></div>' for l, v in (
        ('Primary screens built', f'{done} of {total}'), ('Build time so far', f'{spent} min'), ('Average per screen', f'{avg:.1f} min'),
        ('Tabs, drawers and modals built', f'{n_states}'), ('Time on those', f'{spent_states} min'), ('Update passes', str(len(UPDATES)) if UPDATES else 'None yet')))
    return f'''    <h1 class="h1" style="margin: 0 0 var(--spacing-2)">Production site · Nov 25, 2026</h1>
    <p class="body" style="margin: 0 0 var(--spacing-6); max-width: 760px; color: var(--color-text-muted)">Our own list, not a product screen: which primary screens of the product are rebuilt on the kit, when, and how long each took to build and to update. A green tick links to the screen. Each screen covers desktop and phone width. What the kit did not have was built as <a href="elements/index.html" {LINK}>new elements</a> and <a href="icons/index.html" {LINK}>new icons</a>. The second table lists the tabs, drawers and modals built on top of them; each links straight to that state.</p>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: var(--spacing-4); margin-bottom: var(--spacing-8)">{stats}</div>

    <h2 class="h3" style="margin: 0 0 var(--spacing-3)">Screens</h2>
    <div class="table-scroll" style="max-height: none; margin-bottom: var(--spacing-8)">
      <table class="table"><thead><tr><th><span aria-hidden="true"></span></th><th>Screen</th><th>Route in the app</th><th>Built</th><th>Time to build</th><th>Updated</th><th>Time to update</th><th>Match with staging</th><th>Still different</th></tr></thead><tbody>{"".join(body)}</tbody></table>
    </div>

    <h2 class="h3" style="margin: 0 0 var(--spacing-3)">Tabs, drawers and modals</h2>
    <div class="table-scroll" style="max-height: none; margin-bottom: var(--spacing-8)">
      <table class="table"><thead><tr><th><span aria-hidden="true"></span></th><th>Screen</th><th>State</th><th>Kind</th><th>Built</th><th>Time to build</th><th>Updated</th><th>Time to update</th></tr></thead><tbody>{srows}</tbody></table>
    </div>

    <h2 class="h3" style="margin: 0 0 var(--spacing-3)">Work log</h2>
    <div class="table-scroll" style="max-height: none; margin-bottom: var(--spacing-4)">
      <table class="table"><thead><tr><th>Pass</th><th>When</th><th>Covered</th><th>Took</th><th>Notes</th></tr></thead><tbody>{log}</tbody></table>
    </div>
    <p class="body-sm" style="margin: 0; max-width: 760px; color: var(--color-text-muted)">Times are wall-clock minutes for the whole pass, from the request to the checked result, so a screen’s or a state’s time to build is its pass divided by what the pass covered. A screen’s time to update is the update pass divided by the screens it touched.</p>'''

# The page of new elements: each one live, with where it is used.
def elements_page():
    weeks = [[23, 24, 25, 26, 27]]
    items = [
        ('Bar chart', 'ps-bars', 'Dashboard: initiatives by status.', 'dashboard/index.html',
         barchart([('Idea', 33, ''), ('Definition', 7, ''), ('Execution', 53, 'is-accent'), ('Impact assessment', 0, ''), ('Complete', 34, 'is-success')])),
        ('Health bar', 'ps-health', 'Dashboard: one track split into on track, at risk and off track.', 'dashboard/index.html', healthbar(170, 12, 8, 112)),
        ('Month calendar', 'ps-cal', 'RoB Meetings: a month of weekdays with the meetings in each day, today marked, and a link to the rest.', 'rob-meetings/index.html',
         cal_month(weeks, lambda d: [('[RoB] Onboarding in one week', '10:30am Operations', True)] if d in (23, 25) else [], {24: 12})),
        ('Week grid', 'ps-week', 'RoB Meetings, Profile and Team Profile: hours down, weekdays across.', 'rob-meetings/index.html#show-robview-1',
         week_grid([((0, '10:00am'), ('[RoB] Onboarding in one week', 'Operations')), ((2, '1:00pm'), ('[RoB] Refund requests', 'Delivery'))])),
        ('Mini month', 'ps-month', 'Profile, Time Off tab: the days someone is away.', 'profile/index.html#tab-6', month_table('December 2026', 1, 31, tuple(range(21, 32)))),
        ('Out-of-office grid', 'ps-ooo', 'Team Profile, Time off tab: one row per person, one column per day.', 'team-profile/index.html#tab-4',
         ooo_grid(list(range(23, 31)) + list(range(1, 7)), [('ck', (26, 27)), ('tl', (30, 1, 2))])),
        ('Pagination', 'ps-pagination', 'Under every paged list.', 'processes/index.html', pager()),
        ('Empty state', 'ps-empty', 'Wherever a list has nothing in it yet.', 'recognitions/index.html', empty_state('i-recognize', 'No recognitions', 'You’ll be notified when you receive a recognition.')),
        ('Anchor nav', 'ps-anchors', 'Initiative, New initiative and the meeting view: the sections of a long page.', 'initiative-view/index.html',
         '<nav class="ps-anchors" style="position: static" aria-label="Sections">' + ''.join(
             f'<a class="ps-anchor body-sm{" is-active" if i == 0 else ""}" href="#el-anchor">{icon(ic, "icon icon-16")}{l}</a>' for i, (l, ic) in enumerate(SECTIONS[:4])) + '</nav>'),
        ('Popover panel', 'ps-popover', 'Filters on Processes, Initiatives and RoB Meetings: a panel that drops from a toolbar button.', 'processes/index.html#open-filters-panel',
         '<div class="ps-popover" style="position: static"><div class="row" style="justify-content: space-between; margin-bottom: var(--spacing-4)"><span class="body-semibold">Filters</span>'
         f'<a class="body-sm-semibold" href="#el-popover" {LINK}>Clear all</a></div><div class="row" style="flex-wrap: wrap">{check("Not started")}{check("Active", True)}{check("Paused")}</div></div>'),
        ('Reporting tree', 'ps-tree', 'People, Reporting relationships tab. The product draws curved lines; this one draws straight ones.', 'people/index.html#tab-1', reporting_tree()),
        ('Map panel', 'ps-map', 'People, Geography tab, and the location on a profile. A placeholder field with pins: a real map needs a map provider.', 'people/index.html#tab-2',
         map_panel(PINS[:10], '731 results shown (731 active members in total)', small=True)),
        ('OKR card', 'ps-okr', 'OKRs: an objective with its key results, their connections and progress.', 'okrs/index.html', okr_card(*OKRS[0])),
        ('Business line switcher', 'ps-bizline', 'Top bar of every screen. Its options are assumed: the menu did not open on staging.', 'dashboard/index.html#open-bizline-menu',
         '<div style="display: inline-flex; padding: var(--spacing-2); background: var(--color-graphite-800); border-radius: var(--radius-sm)"><button class="ps-bizline body-sm-semibold" type="button" style="margin: 0; border-left: 0">All Business Lines'
         + icon("i-chevron-down", "icon icon-16") + '</button></div>'),
        ('Avatar mark', 'ps-avatar-mark', 'Meeting view: who accepted or declined. Talent profile: the T that marks a talent network member.', 'rob-meeting-view/index.html',
         f'<div class="row" style="gap: var(--spacing-8)">{user_marked("ck", "yes")}{user_marked("tl", "no")}{user_marked("nr", "talent")}</div>'),
        ('Striped table', 'ps-striped', 'Every list: each second row is tinted.', 'people/index.html',
         table(('Name', 'Status'), ''.join(f'<tr><td><span class="cell-title">{n}</span></td><td>{tag("Active")}</td></tr>' for n in ('Vendor Management', 'Learning Programs', 'Workplace and IT', 'Refund requests'))).replace('class="table"', 'class="table ps-striped"')),
        ('Timeline', 'ps-timeline', 'Profile, Work History tab: positions down a rail, newest first.', 'profile/index.html#tab-3',
         '<div class="ps-timeline" style="max-width: 560px"><div class="ps-timeline-item is-current"><div><p class="body-semibold" style="margin: 0">Delivery Manager</p><p class="body-sm" style="margin: 0">Delivery Subfunction in Operations</p></div>'
         '<span class="body-sm">Apr 2024 - Present</span></div><div class="ps-timeline-item"><div><p class="body-semibold" style="margin: 0">Senior Project Coordinator</p><p class="body-sm" style="margin: 0">Delivery Subfunction in Operations</p></div>'
         '<span class="body-sm">Jul 2022 - Apr 2024</span></div></div>'),
        ('Tree rows', 'ps-row-child', 'Processes and Initiatives: rows that fold under a parent row. Click the caret on Refund requests.', 'processes/index.html',
         table(('Name', 'Status'), f'<tr><td><span class="cell-title">Refund requests</span></td><td>{tag("Active")}</td></tr><tr class="ps-row-child"><td><span class="cell-title">Refund review</span></td><td>{tag("Active")}</td></tr>')),
        ('Tree table', 'ps-wtree', 'Dashboard: rows open a second and a third layer, each layer set in with a rule; the name column stays in place while the others scroll sideways; stripes follow the rows that are open.', 'dashboard/index.html',
         '<div style="max-width: 760px">' + tree_table(DASH_TREE[:2]) + '</div>'),
        ('Status dot', 'ps-dot', 'Health everywhere: the coloured dot inside a grey tag.', 'dashboard/index.html',
         f'<div class="row">{health("On track", "positive")}{health("At risk", "warning")}{health("Off track", "negative")}{health("Not active", "light")}</div>'),
        ('Roadmap marker', 'ps-roadmap', 'Dashboard, Roadmap column: a button that opens the roadmap, with a dot for its health.', 'dashboard/index.html',
         ''.join(f'<button class="btn btn-icon-only btn-ghost btn-xs ps-roadmap is-{k}" type="button" aria-label="View roadmap">{icon("i-roadmap", "btn-icon")}</button>' for k in ('positive', 'warning', 'negative', 'light'))),
        ('Split card', 'ps-split', 'Dashboard: two halves of a card with a rule between them, stacking on a narrow screen.', 'dashboard/index.html',
         '<article class="card"><div class="ps-split"><div style="flex: 1 1 200px"><p class="body-semibold" style="margin: 0">Health</p></div><div style="flex: 2 1 300px"><p class="body-semibold" style="margin: 0">Status</p></div></div></article>'),
        ('Reporting chain', 'ps-chain', 'Profile, Reporting Relationships: who someone reports to, left to right, ending in the column of people beside them with that person marked.', 'profile/index.html',
         chain(("sr", "lk"), ("nr", "ck", "lh"), "ck")),
        ('Link row', 'ps-linkrow', 'Initiative view, Projects: a row that is one link, with a chevron at the end.', 'initiative-view/index.html',
         '<div style="max-width: 560px">' + ''.join(f'<a class="ps-linkrow" href="#"><span class="body-sm">{n}</span>{icon("i-chevron-right", "icon icon-16")}</a>' for n in ('Kick-off checklist', 'Account setup in one day')) + '</div>'),
        ('Agenda row', 'ps-agenda-row', 'Meeting view, Agenda: its number, the item, how often it comes up and who brings it.', 'rob-meeting-view/index.html',
         '<div style="max-width: 640px"><div class="ps-agenda-row"><span class="body-sm">1</span><span class="body-sm">Onboarding status: where each new customer is in the first week</span>' + tag('Weekly') + '<span class="body-xs">Cara Keane</span></div></div>'),
        ('Sheet table', 'ps-sheet', 'Processes and Initiatives, spreadsheet view: numbered rows, ruled cells, every layer open, a column of carets.', 'initiatives/index.html#show-view-2',
         sheet_tree(INIT_TREE[:1], 'el-sheet')),
        ('Blue action button', 'ps-btn-accent', 'Recognitions, the public-profile form and the 404 page: the product’s main action there is blue, where the kit’s primary button is green.', 'recognitions/index.html',
         '<div class="row"><button class="btn btn-primary ps-btn-accent" type="button">Give recognition</button><button class="btn btn-secondary ps-btn-accent" type="button" disabled>Save changes</button></div>'),
        ('Product density', 'ps-density', 'Every screen: the product’s tighter page padding, tabs set straight under the title, tables without an outer box, shorter rows and larger pictures. Rules that adjust kit classes, kept together.', 'people/index.html',
         '<p class="body-sm" style="margin: 0">See any list screen; this entry has no markup of its own.</p>'),
        ('Action item', 'ps-action', 'Profile, Action Items tab: a grey box with the state, the person and the text, struck through once done.', 'profile/index.html#tab-5',
         f'<div class="ps-action is-done" style="max-width: 560px"><div class="row"><span class="ps-action-status"><span class="ps-action-dot"></span>Done</span><span class="body-xs-semibold">Cara Keane</span></div>'
         '<p class="ps-action-text">Draft the kick-off checklist for new customers</p></div>'
         '<div class="ps-action" style="max-width: 560px; margin-top: var(--spacing-2)"><div class="row"><span class="ps-action-status"><span class="ps-action-dot"></span>To do</span><span class="body-xs-semibold">Cara Keane</span></div>'
         '<p class="ps-action-text">Send the refund policy to the partner team</p></div>'),
        ('Small month', 'ps-minical', 'RoB Meetings on a phone: seven days across, today filled, a dot under a day with meetings.', 'rob-meetings/index.html',
         '<div style="max-width: 360px">' + minical('November 2026', (26, 27, 28, 29, 30, 31), 30, (1, 2, 3, 4, 5, 6), 25, (25,)) + '</div>'),
        ('Agenda', 'ps-agenda', 'RoB Meetings on a phone: the day’s meetings under the small month, past ones greyed, a line at the current time.', 'rob-meetings/index.html',
         '<div style="max-width: 360px">' + agenda([('10:30am - 11:30am', '[RoB] Onboarding in one week', 'is-past'), 'now', ('2:00pm - 3:00pm', 'Delivery All Hands', '')]) + '</div>'),
        ('Fill switch', 'ps-seg-fill', 'Dashboard on a phone: the kit’s segmented control stretched to the full row.', 'dashboard/index.html',
         '<div class="ps-seg-fill" style="max-width: 360px">' + segmented(('Core Strategy 28', 'Other initiatives 34'), 0, 'Example switch') + '</div>'),
    ]
    return library_page('New elements', 'elements', items)


def icons_page():
    big = lambda slug, name: f'<div class="row" style="gap: var(--spacing-6); align-items: flex-end">{art(slug, 96, name)}{art(slug, 64, name)}{art(slug, 40, name)}</div>'
    line = lambda slug: (f'<div class="row" style="gap: var(--spacing-6)">{icon(slug, "icon icon-24")}{icon(slug, "icon icon-16")}'
                         f'<button class="btn btn-secondary btn-icon-only" type="button" aria-label="Example">{icon(slug, "btn-icon")}</button></div>')
    badge_where = 'Recognitions, Badges tab'
    items = [
        ('Open in new tab', 'i-external-link', 'Profile, Action Items tab: the link beside the meeting name.', 'profile/index.html#tab-5', line('i-external-link')),
        ('Slack, in colour', 'i-slack-color', 'Work lists, Create Process and profiles: the kit’s Slack mark in four colours, from the kit’s tokens rather than Slack’s own shades.', 'initiatives/index.html', line('i-slack-color')),
        ('Badge: Ambitious', 'i-badge-ambitious', badge_where + '.', 'recognitions/index.html#tab-1', big('i-badge-ambitious', 'Ambitious')),
        ('Badge: Anniversary', 'i-badge-anniversary', badge_where + ' and the profile header.', 'recognitions/index.html#tab-1', big('i-badge-anniversary', 'Anniversary')),
        ('Badge: Challenging', 'i-badge-challenging', badge_where + '.', 'recognitions/index.html#tab-1', big('i-badge-challenging', 'Challenging')),
        ('Badge: Culture Ambassador', 'i-badge-culture', badge_where + ' and the profile header. The product’s flag carries the company mark; this one is plain.', 'recognitions/index.html#tab-1', big('i-badge-culture', 'Culture Ambassador')),
        ('Badge: Driven', 'i-badge-driven', badge_where + '.', 'recognitions/index.html#tab-1', big('i-badge-driven', 'Driven')),
        ('Badge: Helpful', 'i-badge-helpful', badge_where + '.', 'recognitions/index.html#tab-1', big('i-badge-helpful', 'Helpful')),
        ('Badge: HiPo', 'i-badge-hipo', badge_where + '.', 'recognitions/index.html#tab-1', big('i-badge-hipo', 'HiPo')),
        ('Badge: Inspiring', 'i-badge-inspiring', badge_where + '.', 'recognitions/index.html#tab-1', big('i-badge-inspiring', 'Inspiring')),
        ('Empty list', 'i-art-empty-list', 'Recognitions: the drawing above “No recognitions”.', 'recognitions/index.html', big('i-art-empty-list', 'Empty list')),
        ('Roadmap', 'i-roadmap', 'Dashboard, Roadmap column.', 'dashboard/index.html', line('i-roadmap')),
        ('Page not found', 'i-art-not-found', 'The 404 page: the drawing above “Page not found”.', 'not-found/index.html', big('i-art-not-found', 'Page not found')),
        ('Nothing owned', 'i-art-empty-alert', 'Profile and Team Profile, Processes tab: the drawing above “No Processes yet”.', 'profile/index.html#tab-2', big('i-art-empty-alert', 'Nothing owned')),
    ]
    return library_page('New icons', 'icons', items)
