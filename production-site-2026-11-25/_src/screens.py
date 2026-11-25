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


def icon(slug, cls='icon'):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#{slug}"/></svg>'


def tag(text, kind='light'):
    return f'<span class="tag tag-{kind}">{text}</span>'


def health(text, kind):
    return f'<span class="tag tag-indicator tag-{kind}">{text}</span>'


def tabs(items, active=0):
    out = ['<div class="tabs" role="tablist">']
    for i, t in enumerate(items):
        on = i == active
        out.append(f'<button class="tab{" is-active" if on else ""}" role="tab" aria-selected="{str(on).lower()}" type="button">{t}</button>')
    return '\n'.join(out) + '\n</div>'


def select(value, options=(), label=None, width=None):
    if width:
        return f'<div style="flex: 0 0 auto; width: {width}px">{select(value, options, label)}</div>'
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
    return f'<div class="segmented" role="group" aria-label="View">{b}</div>'


def desktop(html):
    return f'<div data-view="desktop">{html}</div>'


def mobile(html):
    return f'<div data-view="mobile" hidden>{html}</div>'


def mobile_toolbar(placeholder):
    return mobile(f'''<div class="toolbar" style="margin-bottom: var(--spacing-4)">
        <div class="input-icon input-icon-left toolbar-search">
          {icon("i-search", "icon input-icon-glyph")}
          <input class="input" type="text" placeholder="{placeholder}" aria-label="Search" />
        </div>
        <button class="btn btn-icon-only btn-ghost" type="button" aria-label="Filters">{icon("i-filter", "btn-icon")}</button>
        <button class="btn btn-icon-only btn-ghost" type="button" aria-label="Sort">{icon("i-sort", "btn-icon")}</button>
      </div>''')


def work_card(title, tags, k, unit, href=None):
    name = f'<a class="body-semibold" href="{href}" {LINK}>{title}</a>' if href else f'<span class="body-semibold">{title}</span>'
    return (f'<article class="card"><div class="stack" style="gap: var(--spacing-3)">{name}<div class="row" style="flex-wrap: wrap">{tags}</div>'
            f'<div class="row" style="justify-content: space-between">{user(k, unit)}<span class="row">'
            f'<button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="View RACI">{icon("i-table", "btn-icon")}</button>'
            f'{icon("i-slack", "icon icon-16")}</span></div></div></article>')


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
        <div class="input-icon input-icon-left toolbar-search">
          {icon("i-search", "icon input-icon-glyph")}
          <input class="input" type="text" placeholder="{placeholder}" aria-label="Search" />
        </div>
        <button class="btn btn-secondary" type="button">{icon("i-filter", "btn-icon")}Filters</button>
        <button class="btn btn-secondary" type="button">{icon("i-code", "btn-icon")}Query</button>
        {select(columns, label="Columns", width=220)}
        {select("Updated at", ("Updated at", "Name", "Status"), label="Sort by", width=150)}
        <button class="btn btn-secondary btn-icon-only" type="button" aria-label="Sort descending">{icon("i-arrow-down", "btn-icon")}</button>
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
      {mobile('<div style="margin-bottom: var(--spacing-4)">' + segmented(('Core Strategy 28', 'Other initiatives 34'), 0, 'Initiatives shown') + '</div>')}

      <article class="card" style="margin-bottom: var(--spacing-6)">
        <div class="row" style="flex-wrap: wrap; gap: var(--spacing-3)">
          <span class="body"><span class="body-semibold">6</span> Objectives</span>{icon("i-caret-right", "icon icon-16")}
          <span class="body"><span class="body-semibold">28</span> Initiatives</span>{icon("i-caret-right", "icon icon-16")}
          <span class="body"><span class="body-semibold">138</span> Projects</span>{icon("i-caret-right", "icon icon-16")}
          <span class="body"><span class="body-semibold">118</span> Sub-projects</span>
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: var(--spacing-8); margin-top: var(--spacing-6)">
          <div class="stack" style="flex: 1 1 320px; min-width: 0">
            <div class="row" style="justify-content: space-between"><h2 class="body-semibold" style="margin: 0">Health</h2><span class="body-sm"><span class="body-sm-semibold">60%</span> on track</span></div>
            <div class="progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="60" aria-label="On track">
              <div class="progress-track"><div class="progress-fill" style="width: 60%"></div></div>
              <span class="progress-value" hidden>60%</span>
            </div>
            <div class="row" style="flex-wrap: wrap">{health("170 On track", "positive")}{health("1 At risk", "warning")}{health("1 Off track", "negative")}{health("112 Not active", "light")}</div>
          </div>
          <div class="stack" style="flex: 2 1 480px; min-width: 0">
            <h2 class="body-semibold" style="margin: 0">Status</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: var(--spacing-3)">{stats}</div>
          </div>
        </div>
      </article>

      <div class="toolbar" style="margin-bottom: var(--spacing-3)">
        <div class="input-icon input-icon-left toolbar-search">
          {icon("i-search", "icon input-icon-glyph")}
          <input class="input" type="text" placeholder="Search by name, owner or function" aria-label="Search" />
        </div>
        <span class="toolbar-spacer"></span>
        <button class="btn btn-icon-only btn-ghost" type="button" aria-label="View settings">{icon("i-controls", "btn-icon")}</button>
        {view_modes(2)}
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
    return f'<div class="cell-meta"><span class="cell-meta-title">{r[0]}</span><span class="cell-meta-sub">{tag(r[1])}</span></div>'


def raci_btn():
    return f'<div class="cell-actions"><button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="View RACI">{icon("i-table", "btn-icon")}</button></div>'


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
                    f'<td><span class="body-sm">{road}</span></td><td>{rob_cell(r)}</td></tr>')
    cards = ''.join(work_card(n, health(*h) + tag("Initiative") + tag(s, kind), k, unit, '../initiative-view/index.html' if i == 0 else None)
                    for i, (n, s, kind, h, k, unit, road, r) in enumerate(INITIATIVES))
    return f'''{head("Initiatives", '<a class="btn btn-primary" href="../initiative-create/index.html" style="text-decoration: none">Create Initiative</a>')}

{work_toolbar("Search by name, owner or function", "Status, Health, Accountability")}

      {mobile('<div class="stack">' + cards + '</div>')}
      <div class="table-scroll" style="max-height: none" data-view="desktop">
        <table class="table">
          <thead><tr><th>Name</th><th>Status</th><th>Health</th><th>Accountability</th><th>Roadmap</th><th>RoB Meeting</th></tr></thead>
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
        field_row('Status', tag('Execution', 'blue')),
        field_row('Health', health('On track', 'positive')),
        field_row('Executive sponsor', user('ho')),
        field_row('Beneficiary function', f'<div class="row">{icon("i-function", "icon icon-16")}<span class="body-sm-semibold">Operations</span></div>'),
        field_row('Related initiatives &amp; projects', f'<a class="body-sm" href="#" {LINK}>Self-serve account setup</a>'),
        field_row('Core strategy', health('On', 'positive')),
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
          <button class="btn btn-secondary" type="button">{icon("i-pencil", "btn-icon")}Edit</button>
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
              <div class="row"><span class="icon-tile icon-tile-sm">{icon("i-slack")}</span><span class="body-sm">Slack channels</span></div>
              <div class="row"><a class="body-sm" href="#" {LINK}># onboarding-one-week</a>{tag("Default")}</div>
              <div class="row"><span class="icon-tile icon-tile-sm">{icon("i-okr")}</span><span class="body-sm">OKRs</span></div>
              <div><a class="body-sm" href="../okrs/index.html" {LINK}>Faster customer onboarding</a></div>
            </div>
          </section>
          <section class="stack" id="sec-documents"><h2 class="h4" {RULE}>Documents</h2>
            <div class="row" style="justify-content: center; color: var(--color-text-muted)">{icon("i-search", "icon icon-16")}<span class="body-sm">No attachments</span></div></section>
          <section class="stack" id="sec-projects"><h2 class="h4" {RULE}>Projects</h2>
            <div class="table-scroll" style="max-height: none"><table class="table"><thead><tr><th>Name</th><th>Status</th><th>Accountability</th></tr></thead><tbody>{projects}</tbody></table></div></section>
        </div>
        {section_nav()}
      </div>
      </div>'''


def fld(label, control, hint=''):
    h = f'<span class="field-hint">{hint}</span>' if hint else ''
    return (f'<div {PAIR}><span class="body-sm" style="flex: 0 0 200px">{label}</span>'
            f'<div style="flex: 1 1 240px; min-width: 0; max-width: 420px">{control}{h}</div></div>')


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
        fld('Beneficiary function', ph_select('Select the function that benefits from the outcome', 'Beneficiary function')),
        fld('Related initiatives &amp; projects', ph_select('Link initiatives or projects this relates to', 'Related initiatives and projects')),
        fld('Core strategy', '<label class="row"><span class="switch"><input type="checkbox" class="switch-input" aria-label="Core strategy" /><span class="switch-track"></span></span></label>',
            'Supports a company-level objective'),
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
      <input class="input" type="text" placeholder="Add initiative name" aria-label="Initiative name" style="width: 100%; max-width: none; margin: var(--spacing-3) 0 var(--spacing-6)" />

      <div style="display: flex; align-items: flex-start; gap: var(--spacing-10)">
        <div class="stack" style="flex: 1; min-width: 0; gap: var(--spacing-8)">
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
            <article class="card"><div class="row">{icon("i-slack", "icon icon-24")}<div><p class="body-semibold" style="margin: 0">Slack</p><p class="body-sm" style="margin: 0; color: var(--color-text-muted)">Create or add Slack channels to sync conversations with this initiative</p></div></div></article>
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
    return f'''{head("RoB Meetings", '<button class="btn btn-primary" type="button">Create meeting</button>')}

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


def rob_meeting_view():
    def sec(title, inner, sid):
        return f'<section class="stack" id="mv-{sid}"><h3 class="h4" {RULE}>{title}</h3>{inner}</section>'

    def empty(text):
        return f'<div class="row" style="color: var(--color-text-muted)">{icon("i-list-unordered", "icon icon-16")}<span class="body-sm">{text}</span></div>'
    details = f'''<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: var(--spacing-4)">
              <div class="row">{icon("i-calendar", "icon icon-16")}<span class="body-sm">Tuesday, November 10</span></div>
              <div class="row">{icon("i-time", "icon icon-16")}<span class="body-sm">10:30 AM – 11:30 AM</span></div>
              <div class="row">{icon("i-globe", "icon icon-16")}<span class="body-sm">GMT+1</span></div>
              <div class="row">{icon("i-update", "icon icon-16")}<span class="body-sm">Every week on Tuesday until Dec 22, 2026</span></div>
              <div class="row">{icon("i-video-on", "icon icon-16")}<a class="body-sm" href="#" {LINK}>Zoom: 954 0000 0000</a></div>
              <div class="row">{icon("i-availability-full-time", "icon icon-16")}<span class="body-sm">Busy</span></div>
              <div class="row">{icon("i-function", "icon icon-16")}<a class="body-sm" href="#" {LINK}>Operations</a></div>
            </div>
            <div class="row" style="align-items: flex-start">{icon("i-list-unordered", "icon icon-16")}<p class="body-sm" style="margin: 0">A weekly working session for the team that runs Onboarding in one week: a short round of status, then decisions and actions.</p></div>'''
    people = ''.join(f'<div class="row" style="justify-content: space-between">{user(k)}</div>' for k in ('ck', 'lh', 'tl', 'lk', 'nr', 'el'))
    nav = ''.join(f'<a class="btn btn-ghost" href="#mv-{i}" style="justify-content: flex-start; text-decoration: none">{icon(s, "btn-icon")}{l}</a>'
                  for l, s, i in (('Details', 'i-list', 'details'), ('Recording', 'i-video-on', 'recording'), ('Agenda', 'i-list-unordered', 'agenda'), ('Action items', 'i-list-checkboxes', 'actions'),
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
            {sec("Details", details, "details")}
            {sec("Recording", f'<div class="row">{icon("i-video-on", "icon icon-16")}<a class="body-sm" href="#" {LINK}>Zoom Recording</a><span class="body-sm" {MUTED}>(1h 8m)</span></div>', "recording")}
            {sec("Agenda", empty("No Agenda items yet"), "agenda")}
            {sec('Action items <span class="count-badge count-badge-secondary">0</span>', empty("No action items were added in this meeting."), "actions")}
            {sec("Pre-read materials", empty("No pre-read materials yet"), "preread")}
            {sec("Connections", f'<div class="row"><span class="icon-tile icon-tile-sm">{icon("i-initiatives")}</span><a class="body-sm" href="../initiative-view/index.html" {LINK}>Onboarding in one week</a>{tag("Initiative")}</div>', "connections")}
            {sec("History", f'<p class="body-sm" style="margin: 0; color: var(--color-text-muted)">Created by Sofia Romano on Jul 3, 2026</p>', "history")}
          </div>
          <div class="stack" style="flex: 2 1 240px; min-width: 0">
            <h3 class="h4" style="margin: 0">Owner</h3>
            {user("sr")}
            <h3 class="h4" style="margin: var(--spacing-4) 0 0">Participants <span class="count-badge count-badge-secondary">6</span></h3>
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
               '<button class="btn btn-secondary" type="button">Export as CSV</button>\n          <button class="btn btn-primary" type="button">Create OKR</button>')
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
          <thead><tr><th>Name</th><th>Org unit</th><th>Manager</th><th>Location</th><th>Local Time</th></tr></thead>
          <tbody>{"".join(rows)}</tbody>
        </table>
      </div>
      {pager()}'''


def org_node(k, role=None):
    name, r = PEOPLE[k]
    return (f'<div class="org-node"><span class="avatar avatar-lg">{ini(k)}</span><div class="org-node-meta"><span class="org-node-name">{name}</span>'
            f'<span class="org-node-role">{role or r}</span></div></div>')


def profile():
    def f(label, value):
        return f'<div><span class="body-sm" {MUTED}>{label}</span><div>{value}</div></div>'

    def contact(ic, text):
        return (f'<div class="row" style="justify-content: space-between"><span class="row">{icon(ic, "icon icon-16")}<a class="body-sm" href="#" {LINK}>{text}</a></span>'
                f'<button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="Copy">{icon("i-copy", "btn-icon")}</button></div>')
    return f'''{head("My Profile", '<a class="btn btn-secondary" href="#" style="text-decoration: none">Edit profile</a>')}

      <div class="row" style="flex-wrap: wrap; align-items: flex-start; gap: var(--spacing-6)">
        <span class="avatar avatar-2xl">CK</span>
        <div class="stack" style="flex: 1 1 200px; min-width: 0; gap: var(--spacing-2)">
          <div class="row"><h2 class="h2" style="margin: 0">Cara Keane</h2><button class="btn btn-icon-only btn-ghost btn-xs" type="button" aria-label="Hear the name">{icon("i-sound-on", "btn-icon")}</button></div>
          <span class="body" {MUTED}>Delivery Manager</span>
          <span class="row body-sm" {MUTED}>{icon("i-cake", "icon icon-16")}March 14</span>
        </div>
        <div class="row"><span class="icon-tile">{icon("i-award")}</span><span class="icon-tile">{icon("i-badge-star")}</span></div>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: var(--spacing-6); margin: var(--spacing-6) 0; padding: var(--spacing-6) 0; border-top: 1px solid var(--color-border); border-bottom: 1px solid var(--color-border)">
        {f("Manager", f'<a class="body" href="#" {LINK}>Lydia Kaminski</a>')}
        {f("Function", f'<a class="body" href="../team-profile/index.html" {LINK}>Operations</a>')}
        {f("Team", f'<a class="body" href="#" {LINK}>Delivery</a>')}
        {f("Business Lines", f'<div class="row">{tag("Services")}{tag("Operationalize")}</div>')}
        {f("Hire Date", '<span class="body">Dec 2, 2019</span>')}
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: var(--spacing-8); margin-bottom: var(--spacing-8)">
        <div class="stack"><span class="body-sm" {MUTED}>Contacts</span>
          {contact("i-email", "cara.keane@harborsupport.com")}{contact("i-slack", "Cara Keane")}{contact("i-phone", "+353 1 555 0142")}</div>
        <div class="stack"><span class="body-sm" {MUTED}>About</span>
          <p class="body" style="margin: 0">I run the Delivery team in Dublin. Before that I spent eight years in customer support, which is where I learned that most problems are handoff problems.</p>
          <div><button class="btn btn-ghost btn-xs" type="button">Read more</button></div></div>
        <div class="stack"><span class="body-sm" {MUTED}>Location</span>
          <article class="card"><div class="row">{icon("i-pin", "icon icon-16")}<span class="body-sm">Dublin, Ireland</span></div></article></div>
      </div>

      {tabs(("Reporting Relationships", "Initiatives", "Processes", "Work History", "RoB Meetings", "Action Items", "Time Off"))}

      <h2 class="h3" style="margin: var(--spacing-6) 0 var(--spacing-1)">Reporting Relationships</h2>
      <p class="body-sm" style="margin: 0 0 var(--spacing-4); color: var(--color-text-muted)">4 people associated with Cara as Delivery Manager</p>
      <div class="org-chart"><div class="org-chart-group">
        {org_node("lk")}
        <ul class="org-node-children"><li>{org_node("ck")}
          <ul class="org-node-children"><li>{org_node("lh")}</li><li>{org_node("tl")}</li><li>{org_node("nr")}</li></ul></li></ul>
      </div></div>'''


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


def team():
    rows = []
    for n, k, line, kids in UNITS:
        toggle = (f'<button class="row-toggle" type="button" aria-expanded="false" aria-label="Toggle children">{icon("i-caret-right")}</button>' if kids
                  else '<span class="row-toggle-spacer"></span>')
        name = (f'<a class="body-semibold" href="../team-profile/index.html" {LINK}>{n}</a>' if n == 'Operations' else f'<a class="body-semibold" href="#" {LINK}>{n}</a>')
        rows.append(f'<div class="list-row"><div class="cell-title-row">{toggle}<span class="avatar avatar-sm avatar-team">{icon("i-function")}</span>'
                    f'<div><p class="list-row-title">{name} {tag("Function")}</p><p class="list-row-meta">Led by <a href="#" {LINK}>{PEOPLE[k][0]}</a>, {PEOPLE[k][1]}</p>'
                    f'<p class="list-row-meta">{line}</p></div></div></div>')
    return f'''{head("Organizational Structure")}

      {tabs(("Organizational Units", "Divisions", "Talent Network Members", "Skills"))}

      <div style="max-width: 420px; margin: var(--spacing-4) 0">{ph_select("Select org unit", "Org unit")}</div>

      <div>{"".join(rows)}</div>'''


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

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: var(--spacing-8); margin: var(--spacing-6) 0 var(--spacing-8)">
        <div class="stack"><span class="body-sm" {MUTED}>About</span>
          <p class="body" style="margin: 0">Operations runs the work customers pay for: delivery, quality and the handoffs between them. The function is measured on time to first delivery and on engagement health.</p></div>
        <div class="stack"><span class="body-sm" {MUTED}>Slack Channels</span>
          <span class="body-sm" {MUTED}>No Slack channels attached</span></div>
      </div>

      {tabs(("Org Structure", "OKRs", "Initiatives", "Processes", "Time off", "RoB Meetings"))}

      <h2 class="h3" style="margin: var(--spacing-6) 0 var(--spacing-1)">Reporting Relationships</h2>
      <p class="body-sm" style="margin: 0 0 var(--spacing-4); color: var(--color-text-muted)">5 people comprise Operations, and 6 Talents are associated with it</p>
      <div class="org-chart"><div class="org-chart-group">
        {org_node("lk")}
        <ul class="org-node-children"><li>{org_node("ck")}
          <ul class="org-node-children"><li>{org_node("lh")}</li><li>{org_node("tl")}</li></ul></li><li>{org_node("nr")}</li></ul>
      </div></div>'''


P1 = ('btn-primary',)
SCREENS = [
    dict(folder='dashboard', title='TopTrack Dashboard', nav='Dashboard', main=dashboard(), route='/dashboard',
         ctas=[('btn-secondary', 'More actions', 'i-dots-three-vertical')]),
    dict(folder='processes', title='Processes', nav='Processes', main=processes(), route='/bau/list',
         ctas=[('btn-primary', 'Create Process', 'i-plus')]),
    dict(folder='initiatives', title='Initiatives', nav='Initiatives', main=initiatives(), route='/initiatives/list',
         ctas=[('btn-primary', 'Create Initiative', 'i-plus')]),
    dict(folder='initiative-view', title='Onboarding in one week', nav='Initiatives', main=initiative_view(), route='/initiatives/:id', padded=False),
    dict(folder='initiative-create', title='New initiative', nav='Initiatives', main=initiative_create(), route='/initiatives/create', padded=False),
    dict(folder='rob-meetings', title='RoB Meetings', nav='RoB Meetings', main=rob_calendar(), route='/rob',
         ctas=[('btn-primary', 'Create meeting', 'i-plus')]),
    dict(folder='rob-meeting-view', title='RoB Meetings', nav='RoB Meetings', main=rob_calendar().replace('btn btn-primary', 'btn btn-secondary'),
         overlays=rob_meeting_view(), route='/rob?calendarId=…&externalId=…', ctas=[('btn-secondary', 'Create meeting', 'i-plus')]),
    dict(folder='okrs', title='OKRs', nav='OKRs', main=okrs(), route='/okrs/list',
         ctas=[('btn-secondary', 'Performance attributes', 'i-info'), ('btn-secondary', 'Export as CSV', 'i-download'), ('btn-primary', 'Create OKR', 'i-plus')]),
    dict(folder='people', title='People', nav='People', main=people(), route='/people/directory'),
    dict(folder='profile', title='My Profile', nav='People', main=profile(), route='/people/:userId',
         ctas=[('btn-secondary', 'Edit profile', 'i-pencil')]),
    dict(folder='team', title='Organizational Structure', nav='Team', main=team(), route='/org-structure/org-units'),
    dict(folder='team-profile', title='Team Profile', nav='Team', main=team_profile(), route='/teams/:teamId'),
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
                      ('Paused meetings', '/rob/paused-meetings', None), ('Slack card', '/rob/slack_cards/:id', None)]),
    ('OKRs', [('OKRs', '/okrs/list', 'okrs')]),
    ('People and profile', [('People', '/people/directory', 'people'), ('Profile', '/people/:userId', 'profile'),
                            ('Edit profile', '/people/:userId/edit', None), ('Edit public profile', '/people/:userId/edit-public-profile', None),
                            ('Create profile', '/people/create', None)]),
    ('Team and org structure', [('Organizational Structure', '/org-structure/org-units', 'team'), ('Team Profile', '/teams/:teamId', 'team-profile'),
                                ('Create org unit', '/org-structure/create', None), ('Edit org unit', '/teams/:teamId/edit', None),
                                ('Create division', '/org-structure/divisions/create', None), ('Edit division', '/org-structure/divisions/edit/:id', None),
                                ('Talent profile', '/talent/:talentId', None), ('Create and edit talent', '/talent/create', None)]),
    ('Watercooler, Time off, Recognitions', [('Watercooler', '/watercooler', None), ('Time off', '/time-off', None), ('Recognitions', '/recognitions', None)]),
    ('Peer feedback', [('Peer feedback', '/peer-feedbacks/:viewMode/:tab', None), ('Give feedback', '/peer-feedbacks/:feedbackId/edit', None),
                       ('Feedback', '/peer-feedbacks/:feedbackId/view', None)]),
    ('Performance review and self-review', [
        ('Self-assessment', '/performance-review/self-assessment', None), ('Manager view', '/performance-review/manager/:tab', None),
        ('Assessments', '/performance-review/assessments', None), ('Edit assessment', '/performance-review/assessments/edit/:assessmentId', None),
        ('Assessment', '/performance-review/assessment/:reviewId/:userId', None), ('Reports', '/performance-review/reports', None),
        ('Cycle report', '/performance-review/reports/:cycleId', None), ('Reviewee breakdown', '/performance-review/reports/:cycleId/:revieweeId', None),
        ('Self-review', '/self-review/:userId', None), ('Team self-review', '/self-review/team', None)]),
    ('Outside the main navigation', [('Sign in', '/signin', None), ('Sign up', '/signup', None), ('Forgot password', '/forgot-password', None),
                                     ('Reset password', '/reset-password', None), ('Page not found', '/404', None), ('Onboarding', '/onboarding', None),
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


def index():
    total = sum(len(rows) for _, rows in INVENTORY)
    done = sum(1 for _, rows in INVENTORY for r in rows if r[2])
    pct = round(100 * done / total)
    yes = f'<svg class="icon icon-16" role="img" aria-label="Built" style="color: var(--color-success)"><use href="#i-done-solid"/></svg>'
    no = f'<svg class="icon icon-16" role="img" aria-label="Not built" style="color: var(--color-text-subtle)"><use href="#i-bullet-outline"/></svg>'
    body = []
    for area, rows in INVENTORY:
        n = sum(1 for r in rows if r[2])
        body.append(f'<tr><td colspan="4"><span class="body-semibold">{area}</span> <span class="body-sm" {MUTED}>{n} of {len(rows)}</span></td></tr>')
        for name, route, folder in rows:
            title = f'<a class="cell-title" href="{folder}/index.html" {LINK}>{name}</a>' if folder else f'<span class="cell-title" {MUTED}>{name}</span>'
            lay = tag("Desktop and phone") if folder else ''
            body.append(f'<tr><td style="width: var(--spacing-10)">{yes if folder else no}</td><td>{title}</td><td><code class="body-sm">{route}</code></td><td>{lay}</td></tr>')
    return f'''{head("Production site · Nov 25, 2026")}

      <div class="alert" style="margin-bottom: var(--spacing-6)">{icon("i-info", "icon alert-icon")}
        <p class="alert-message">The product as it ran on November 25, 2026, rebuilt on the kit. Start an update or a new version of a screen from its copy here. Layout, labels and structure follow the app; the people and the records are made up. Only each screen’s basic state is built so far: tabs, drawers and modals come next.</p></div>

      <div class="stack" style="max-width: 480px; margin-bottom: var(--spacing-6)">
        <div class="row" style="justify-content: space-between"><span class="body-semibold">{done} of {total} primary screens built</span><span class="body-sm">{pct}%</span></div>
        <div class="progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{pct}" aria-label="Screens built">
          <div class="progress-track"><div class="progress-fill" style="width: {pct}%"></div></div>
          <span class="progress-value" hidden>{pct}%</span>
        </div>
      </div>

      <div class="table-scroll" style="max-height: none">
        <table class="table"><thead><tr><th><span aria-hidden="true"></span></th><th>Screen</th><th>Route in the app</th><th>Layouts</th></tr></thead><tbody>{"".join(body)}</tbody></table>
      </div>'''
