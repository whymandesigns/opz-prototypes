/* flow.js — the flow canvas: every screen a prototype's CODE can reach, live,
 * on one pannable / zoomable canvas. Zoom out for the whole picture, click a
 * screen to use it.
 *
 * Use from a page inside the prototype's folder, e.g. /action-trace/flow/index.html:
 *   <script src="../../lib/flow.js" data-start="page=meetings"></script>
 * The prototype is inferred from the folder. A map.json next to that page
 * (saved from the Screens panel) opens instantly; otherwise the page maps the
 * prototype itself: it opens it in a hidden frame, clicks every control on the
 * current screen, fingerprints where it lands, and repeats breadth-first.
 * Each screen then gets a live frame that replays the same clicks.
 * Needs http (the dev server or the deployed site), not file://.
 */
(() => {
const STYLE = `
:root { --ink: #191E28; --ink-2: #262D3D; --muted: #6A7389; --line: #CDD1DC; --accent: #2E9BFF; --paper: #F7F8FA; }
* { box-sizing: border-box; }
html, body { height: 100%; margin: 0; }
body { font-family: 'Proxima Nova', Inter, system-ui, -apple-system, 'Segoe UI', sans-serif; color: var(--ink); background: #E9ECF1; overflow: hidden; user-select: none; }
button { font-family: inherit; }
.fc-top { position: fixed; left: 0; right: 0; top: 0; height: 48px; z-index: 50; display: flex; align-items: center; gap: 14px; padding: 0 16px; background: var(--ink-2); color: #fff; box-shadow: 0 2px 8px rgba(0,0,0,.2); }
.fc-title { display: flex; align-items: baseline; gap: 10px; font-weight: 700; font-size: 14px; white-space: nowrap; }
.fc-title small { font-weight: 400; color: #AEB6C6; font-size: 12px; }
.fc-sep { width: 1px; height: 22px; background: rgba(255,255,255,.18); }
.fc-btn { height: 30px; padding: 0 10px; border: 1px solid rgba(255,255,255,.22); background: rgba(255,255,255,.06); color: #fff; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; text-decoration: none; }
.fc-btn:hover { background: rgba(255,255,255,.14); }
.fc-btn.is-on { background: #fff; color: var(--ink); }
.fc-btn kbd { font: 10px/1 ui-monospace, Menlo, monospace; background: rgba(0,0,0,.25); padding: 2px 4px; border-radius: 3px; }
.fc-btn.is-on kbd { background: rgba(0,0,0,.08); }
.fc-viewport { position: fixed; inset: 48px 0 0 0; overflow: hidden; cursor: grab; background-color: #E9ECF1; background-image: radial-gradient(rgba(25,30,40,.14) 1px, transparent 1.2px); }
.fc-viewport.is-panning { cursor: grabbing; }
.fc-world { position: absolute; left: 0; top: 0; transform-origin: 0 0; will-change: transform; }
.fc-frame { position: absolute; width: 1440px; background: #fff; border-radius: 14px; box-shadow: 0 10px 40px rgba(25,30,40,.22), 0 0 0 2px rgba(25,30,40,.08); }
.fc-frame.is-focus { box-shadow: 0 0 0 6px var(--accent), 0 30px 80px rgba(25,30,40,.35); }
.fc-frame.is-start .fc-head { background: #E8F3FF; }
.fc-tag { position: absolute; left: 0; bottom: 100%; margin-bottom: 6px; transform-origin: 0 100%; display: flex; align-items: center; gap: 6px; padding: 3px 8px 3px 4px; background: rgba(38,45,61,.92); color: #fff; border-radius: 6px; font-size: 12px; font-weight: 600; white-space: nowrap; overflow: hidden; pointer-events: none; }
.fc-tag span { overflow: hidden; text-overflow: ellipsis; }
.fc-tag i { font-style: normal; min-width: 18px; height: 18px; padding: 0 5px; border-radius: 9px; background: #fff; color: var(--ink); font-size: 11px; display: inline-grid; place-items: center; }
.fc-frame.is-start .fc-tag i { background: var(--accent); color: #fff; }
.fc-world.is-near .fc-tag { display: none; }
.fc-head { height: 64px; display: flex; align-items: center; gap: 16px; padding: 0 20px; border-radius: 14px 14px 0 0; background: var(--paper); border-bottom: 2px solid var(--line); cursor: pointer; }
.fc-head:hover { background: #fff; }
.fc-num { width: 40px; height: 40px; border-radius: 50%; background: var(--ink); color: #fff; font-weight: 800; font-size: 18px; display: grid; place-items: center; flex: none; }
.fc-frame.is-start .fc-num { background: var(--accent); }
.fc-name { font-size: 24px; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; }
.fc-name small { display: block; font-size: 14px; font-weight: 500; color: var(--muted); margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.fc-head .spacer { flex: 1; }
.fc-head .fc-act { height: 36px; padding: 0 14px; border: 2px solid var(--line); background: #fff; border-radius: 8px; font-size: 15px; font-weight: 600; cursor: pointer; color: var(--ink); display: inline-flex; align-items: center; gap: 8px; white-space: nowrap; text-decoration: none; }
.fc-head .fc-act:hover { border-color: var(--ink); }
.fc-body { position: relative; width: 1440px; height: 900px; overflow: hidden; border-radius: 0 0 14px 14px; background: #fff; }
.fc-body iframe { width: 1440px; height: 900px; border: 0; display: block; pointer-events: none; }
.fc-frame.is-focus .fc-body iframe { pointer-events: auto; }
.fc-shield { position: absolute; inset: 0; cursor: zoom-in; }
.fc-frame.is-focus .fc-shield { display: none; }
.fc-frame.is-loading .fc-body:after { content: attr(data-status); position: absolute; inset: 0; display: grid; place-items: center; font-size: 28px; color: var(--muted); background: rgba(247,248,250,.9); }
.fc-group { position: absolute; transform-origin: 0 100%; font-size: 44px; font-weight: 800; letter-spacing: .02em; color: rgba(25,30,40,.28); text-transform: uppercase; white-space: nowrap; pointer-events: none; }
.fc-group small { display: block; font-size: 22px; font-weight: 600; letter-spacing: 0; text-transform: none; color: rgba(25,30,40,.4); margin-top: 4px; }
.fc-focus { position: fixed; left: 50%; bottom: 22px; transform: translateX(-50%); z-index: 50; display: none; align-items: center; gap: 10px; padding: 8px 10px 8px 16px; background: var(--ink-2); color: #fff; border-radius: 24px; font-size: 13px; box-shadow: 0 8px 30px rgba(0,0,0,.3); white-space: nowrap; max-width: 90vw; }
.fc-focus.is-on { display: flex; }
.fc-focus b { color: #8FD3FF; }
.fc-mini { position: fixed; right: 16px; bottom: 16px; width: 240px; height: 140px; z-index: 50; background: rgba(38,45,61,.92); border-radius: 10px; box-shadow: 0 8px 30px rgba(0,0,0,.3); overflow: hidden; cursor: pointer; }
.fc-mini svg { width: 100%; height: 100%; display: block; }
.fc-mini rect.f { fill: #9AA3B5; }
.fc-mini rect.f.is-start { fill: var(--accent); }
.fc-mini rect.v { fill: rgba(255,255,255,.12); stroke: #fff; stroke-width: 2; vector-effect: non-scaling-stroke; }
.fc-progress { position: fixed; left: 50%; top: 50%; transform: translate(-50%, -50%); z-index: 60; width: 460px; padding: 22px 24px; background: #fff; border-radius: 12px; box-shadow: 0 20px 60px rgba(0,0,0,.3); display: none; }
.fc-progress.is-on { display: block; }
.fc-progress h2 { margin: 0 0 6px; font-size: 16px; }
.fc-progress p { margin: 0 0 12px; font-size: 13px; color: var(--muted); line-height: 1.5; }
.fc-progress .bar { height: 8px; background: #E0E3EA; border-radius: 4px; overflow: hidden; }
.fc-progress .bar i { display: block; height: 100%; width: 0; background: var(--accent); transition: width .2s; }
.fc-progress .log { margin-top: 10px; font: 11px/1.5 ui-monospace, Menlo, monospace; color: var(--muted); max-height: 120px; overflow: auto; white-space: pre-wrap; }
.fc-notice { position: fixed; left: 50%; top: 50%; transform: translate(-50%, -50%); z-index: 60; width: 560px; padding: 24px 26px; background: #fff; border-radius: 12px; box-shadow: 0 20px 60px rgba(0,0,0,.3); display: none; font-size: 14px; line-height: 1.55; }
.fc-notice.is-on { display: block; }
.fc-notice h2 { margin: 0 0 8px; font-size: 18px; }
.fc-notice code { font: 12px ui-monospace, Menlo, monospace; background: var(--paper); padding: 2px 6px; border-radius: 4px; }
#fc-crawler { position: fixed; left: -3000px; top: 0; width: 1440px; height: 900px; border: 0; opacity: 0; pointer-events: none; }
.fc-rail { position: fixed; left: 0; top: 48px; bottom: 0; width: 290px; z-index: 40; background: rgba(255,255,255,.97); border-right: 1px solid var(--line); overflow: auto; padding: 10px; transform: translateX(-100%); transition: transform .2s; display: flex; flex-direction: column; }
.fc-rail.is-on { transform: none; }
.fc-rail h3 { margin: 6px 6px 8px; font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); }
.fc-rail-list { flex: 1; }
.fc-rail-list button { display: flex; align-items: center; gap: 8px; width: 100%; border: 0; background: transparent; text-align: left; padding: 7px 8px; border-radius: 6px; font-size: 12px; cursor: pointer; color: var(--ink); }
.fc-rail-list button:hover { background: var(--paper); }
.fc-rail-list button i { font-style: normal; min-width: 20px; height: 20px; padding: 0 5px; border-radius: 10px; background: var(--ink); color: #fff; font-size: 10px; font-weight: 800; display: inline-grid; place-items: center; }
.fc-rail-list button.is-start i { background: var(--accent); }
.fc-rail-list button span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.fc-rail-list .depth { margin: 10px 6px 4px; font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: .08em; }
.fc-rail-foot { margin-top: 14px; padding: 10px 2px 0; border-top: 1px solid var(--line); display: flex; flex-direction: column; gap: 2px; }
.fc-rail-foot button, .fc-rail-foot a { display: block; width: 100%; text-align: left; border: 0; background: transparent; padding: 6px 8px; border-radius: 6px; font-size: 12px; color: var(--muted); cursor: pointer; text-decoration: none; }
.fc-rail-foot button:hover, .fc-rail-foot a:hover { background: var(--paper); color: var(--ink); }
`;
const MARKUP = `
<header class="fc-top">
  <div class="fc-title">Flow canvas <small id="fc-subtitle">every screen the code can reach</small></div>
  <div class="fc-sep"></div>
  <button class="fc-btn" id="fc-rail-toggle">☰ Screens</button>
</header>
<aside class="fc-rail" id="fc-rail">
  <h3>Screens found</h3>
  <div class="fc-rail-list" id="fc-rail-list"></div>
  <div class="fc-rail-foot">
    <button id="fc-recrawl" title="Map the prototype again from its code (after it changed)">↻ Re-crawl the prototype</button>
    <button id="fc-download" title="Save the map as map.json; commit it next to this page and it opens instantly for everyone">⤓ Save map.json</button>
    <a id="fc-open-proto" href="#" target="_blank">Open the prototype ↗</a>
  </div>
</aside>
<div class="fc-viewport" id="fc-viewport"><div class="fc-world" id="fc-world"><div id="fc-frames"></div><div id="fc-groups"></div></div></div>
<div class="fc-focus" id="fc-focus"><span>Using <b id="fc-focus-name"></b> live — click through it like the prototype</span><button class="fc-btn" id="fc-focus-reset">↻ Reset this screen</button><button class="fc-btn is-on" id="fc-focus-exit">Exit <kbd>Esc</kbd></button></div>
<div class="fc-mini" id="fc-mini" title="Click to jump"><svg id="fc-mini-svg"></svg></div>
<div class="fc-progress" id="fc-progress"><h2>Mapping the prototype…</h2><p>Opening the prototype, clicking every control on each screen and recording where it lands.</p><div class="bar"><i id="fc-progress-bar"></i></div><div class="log" id="fc-progress-log"></div></div>
<div class="fc-notice" id="fc-notice"></div>
<iframe id="fc-crawler" title="crawler"></iframe>
`;
const st = document.createElement('style'); st.textContent = STYLE; document.head.appendChild(st);
document.body.insertAdjacentHTML('beforeend', MARKUP);

/* ============================ Setup ============================ */
const $ = (s, r = document) => r.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const wait = ms => new Promise(r => setTimeout(r, ms));
const q = new URLSearchParams(location.search);
const ME = document.currentScript || document.querySelector('script[src*="flow.js"]');
const CFG = ME ? ME.dataset : {};
let P = q.get('p') || '';                                                                     // prototype folder, e.g. /action-trace/
if (!P) { const m = location.pathname.match(/^(.*\/[^/]+\/)flow\/(index\.html)?$/); if (m) P = m[1]; }   // /action-trace/flow/ → /action-trace/
if (P && !P.endsWith('/')) P += '/';
const START = q.get('start') || CFG.start || '';                                              // extra query for the prototype, e.g. page=meetings
const DEPTH = +(q.get('depth') || CFG.depth || 3), MAX = +(q.get('max') || CFG.max || 24), PER = 16;
const PROTO_URL = P ? `${P}index.html?review=0${START ? '&' + START : ''}` : '';              // review=0 keeps the review bar out of every frame
const MAP_URL = (!q.get('p') && P) ? 'map.json' : '';                                        // a prebuilt map shipped next to the page
const CACHE_KEY = 'flowmap:' + P + ':' + START;
const W = 1440, H = 964, GX = 320, GY = 300;
const notice = html => { $('#fc-notice').innerHTML = html; $('#fc-notice').classList.add('is-on'); };
if (!P) notice(`<h2>No prototype to map</h2>Put this page at <code>/&lt;prototype&gt;/flow/index.html</code>, or add <code>?p=/&lt;prototype&gt;/</code> to the URL.`);
else if (location.protocol === 'file:') notice(`<h2>Open this through a server</h2>The canvas has to look inside the prototype's frames to map it, and a <code>file://</code> page is not allowed to. Open it through the Icarus dev server:<br><br><code>http://localhost:5733${esc(P)}flow/</code>`);
$('#fc-open-proto').href = P ? `${P}index.html` : '#';
if (P) $('#fc-subtitle').textContent = `${P} · every screen the code can reach`;

/* ============================ Crawler ============================ */
const CONTROL_SEL = 'button, a, [role="button"], [data-act], [data-page], [data-flow], [data-state], .nav-item, .tab, .tabs-item, .segmented-item, [data-modal-open], [data-modal-close], [data-tab]';
const SKIP_SEL = '.flownav, .verbadge, #rvToggle, [id^="rv"], .rv-bar, .rv-side, .rv-pin, [class*="switcher"], [data-rv-mode], [data-rv-act], .rv-toggle';
const LAYER_SEL = '[data-layer], .layer, .modal-overlay, .drawer-overlay, .modal, .drawer, [role="dialog"]';           // what counts as a screen layer
const POP_SEL = '[data-pop], .pop, .popover, .dropdown-menu, .menu, .dropdown.is-open, [data-dropdown].is-open';       // transient menus: clicked into, not screens
const isVisible = el => { if (!el || el.hidden || el.closest('[hidden]')) return false; const cs = el.ownerDocument.defaultView.getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden' || (cs.pointerEvents === 'none' && el.tagName !== 'A')) return false; const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
const text = el => { let t = el.getAttribute('aria-label') || el.title; if (!t) { const lines = (el.innerText || el.textContent || '').split('\n').map(x => x.trim()).filter(Boolean); const i = lines.findIndex(l => l.length >= 3); t = i >= 0 ? lines.slice(0, i + 1).join(' ') : lines.join(' '); } return (t || '').replace(/\s+/g, ' ').trim().slice(0, 48); };
const full = el => (el.textContent || '').replace(/\s+/g, ' ').trim();
function describe(el) {
  const attrs = [...el.attributes].filter(a => a.name.startsWith('data-') && !/^data-(rv|ic|icon|hover|tip|tooltip)/.test(a.name) && a.value.length < 60);
  const t = text(el);
  if (attrs.length) return { sel: el.tagName.toLowerCase() + attrs.map(a => `[${a.name}="${a.value.replace(/"/g, '\\"')}"]`).join(''), text: t, byText: false };
  if (el.id) return { sel: '#' + CSS.escape(el.id), text: t, byText: false };
  return { sel: el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0, 2).map(CSS.escape).join('.') : ''), text: t, byText: true };
}
const ctrlKey = c => c.sel + (c.byText ? '|' + c.text : '');
function resolve(doc, c) { const all = [...doc.querySelectorAll(c.sel)].filter(el => isVisible(el) && !el.closest(SKIP_SEL)); return (c.byText ? all.filter(el => text(el) === c.text) : all)[0] || null; }
function scopeOf(doc) {
  const layers = [...doc.querySelectorAll(LAYER_SEL + ', ' + POP_SEL)].filter(el => isVisible(el) && !el.closest(SKIP_SEL));
  if (!layers.length) return doc.body;
  return layers.reduce((top, el) => { const z = +doc.defaultView.getComputedStyle(el).zIndex || 0; return z >= top.z ? { el, z } : top; }, { el: layers[0], z: -1 }).el;
}
function controlsIn(doc) {
  const scope = scopeOf(doc); const seen = new Set(); const out = [];
  for (const el of scope.querySelectorAll(CONTROL_SEL)) {
    if (!isVisible(el) || el.disabled || el.closest(SKIP_SEL)) continue;
    if (el.tagName === 'A') { const h = el.getAttribute('href') || ''; if (el.target === '_blank' || (h && !h.startsWith('#') && !h.startsWith('javascript'))) continue; }
    if (el.closest('input, textarea, select')) continue;
    const c = describe(el); const k = ctrlKey(c); if (seen.has(k)) continue; seen.add(k); out.push(c);
  }
  return out;
}
function fingerprint(win) {
  const doc = win.document; let screen = null;
  try { const s = win.REVIEW && win.REVIEW.screen && win.REVIEW.screen(); if (s) screen = s.name || String(s.id); } catch (_) {}
  const layers = [...doc.querySelectorAll(LAYER_SEL)].filter(el => isVisible(el) && !el.closest(SKIP_SEL)).map(el => { const h = el.querySelector('h1,h2,h3,.title,.h,.drawer-title,.modal-title,[class*="title"]'); return (el.dataset.layer || el.dataset.pop || el.className.toString().split(/\s+/)[0]) + ':' + (h ? full(h) : text(el)).slice(0, 60); });
  const nav = [...doc.querySelectorAll('.nav-item.active, .nav-item.is-active, .sidenav-item.is-active, [aria-current], .tab.on, .tab.is-active, .tabs-item.is-active, [aria-selected="true"], .segmented-item.is-active, .is-active[data-tab]')].filter(isVisible).map(text);
  const main = text(doc.querySelector('main h1, #main h1, .page-head h1, .page-title, h1') || doc.body).slice(0, 40);
  return { sig: JSON.stringify({ screen, layers, nav, main }), screen, layers, nav, main };
}
function nameOf(fp, i) {
  const top = fp.layers[fp.layers.length - 1]; if (top) { const t = top.split(':').slice(1).join(':'); if (t && t.length > 2) return t; }
  if (fp.screen) return fp.screen.replace(/^Screen \d+(\.5)?[a-z]? · /, '');
  return fp.main || fp.nav[0] || `Screen ${i}`;
}
function subOf(fp) { const bits = []; if (fp.screen) bits.push(fp.screen); else if (fp.nav.length) bits.push(fp.nav.join(' · ')); if (fp.layers.length > 1) bits.push(fp.layers.map(l => l.split(':')[0]).join(' + ')); return bits.join(' · ') || 'Base page'; }

let STATES = [];
async function crawl() {
  const prog = $('#fc-progress'), bar = $('#fc-progress-bar'), log = $('#fc-progress-log'); prog.classList.add('is-on'); log.textContent = ''; bar.style.width = '2%';
  const say = m => { log.textContent += m + '\n'; log.scrollTop = 1e6; };
  const fr = $('#fc-crawler');
  const load = () => new Promise(res => { fr.onload = () => setTimeout(res, 500); fr.src = PROTO_URL + '&_=' + Date.now(); });
  await load(); let win = fr.contentWindow, doc = fr.contentDocument;
  if (!doc || !doc.body) { prog.classList.remove('is-on'); notice(`<h2>Could not read the prototype</h2>The frame at <code>${esc(PROTO_URL)}</code> did not load, or the browser refused access to it. The canvas and the prototype must be served from the same origin.`); return; }
  // Snapshot / restore the prototype's state when it has the usual S + render() shape (reached through an eval in its realm, since they are top-level consts); otherwise reload and replay.
  let acc = null; try { acc = win.eval('(typeof S === "object" && typeof render === "function") ? ({ get: () => S, set: o => { Object.keys(S).forEach(k => delete S[k]); Object.assign(S, o); }, render: () => render() }) : null'); } catch (_) {}
  const fast = !!acc;
  const snapshot = () => { if (!fast) return null; try { return JSON.parse(JSON.stringify(acc.get())); } catch (_) { return null; } };
  const replay = async path => { for (const c of path) { const el = resolve(doc, c); if (!el) return false; el.click(); await wait(350); } return true; };
  const restore = async st => {
    if (fast && st.snap) { try { acc.set(JSON.parse(JSON.stringify(st.snap))); doc.querySelectorAll('#pops').forEach(p => p.innerHTML = ''); acc.render(); await wait(120); return true; } catch (_) {} }
    await load(); win = fr.contentWindow; doc = fr.contentDocument; return replay(st.path);
  };
  const fp0 = fingerprint(win);
  STATES = [{ id: 0, fp: fp0, sig: fp0.sig, name: nameOf(fp0, 0), sub: subOf(fp0), path: [], depth: 0, snap: snapshot() }];
  const bySig = new Map([[fp0.sig, 0]]); const queue = [0];
  say(`start: ${STATES[0].name}  (${fast ? 'state snapshots' : 'reload + replay'})`);
  while (queue.length && STATES.length < MAX) {
    const st = STATES[queue.shift()]; if (st.depth >= DEPTH) continue;
    await restore(st); const ctrls = controlsIn(doc).slice(0, PER);
    say(`screen ${st.id} · ${ctrls.length} controls`);
    for (const c of ctrls) {
      if (STATES.length >= MAX) break;
      if (!(await restore(st))) continue; const el = resolve(doc, c); if (!el) continue;
      try { el.click(); } catch (_) { continue; } await wait(fast ? 260 : 380);
      if (fr.contentDocument !== doc) { await load(); win = fr.contentWindow; doc = fr.contentDocument; await replay(st.path); continue; }   // the click navigated away: ignore it
      const fp = fingerprint(win); if (fp.sig === st.sig || bySig.has(fp.sig)) continue;
      const id = STATES.length; const ns = { id, fp, sig: fp.sig, name: nameOf(fp, id), sub: subOf(fp), path: [...st.path, c], depth: st.depth + 1, snap: snapshot() };
      STATES.push(ns); bySig.set(fp.sig, id); queue.push(id);
      say(`  + ${id}: ${ns.name}`); bar.style.width = Math.min(96, 4 + STATES.length / MAX * 92) + '%';
    }
  }
  bar.style.width = '100%'; await wait(200); prog.classList.remove('is-on'); fr.src = 'about:blank';
  try { localStorage.setItem(CACHE_KEY, mapJSON()); } catch (_) {}
  $('#fc-subtitle').textContent = `${P} · ${STATES.length} screens · mapped just now`;
  build();
}
const mapJSON = () => JSON.stringify({ when: Date.now(), p: P, start: START, depth: DEPTH, max: MAX, states: STATES.map(({ snap, x, y, ...s }) => s) });

/* ============================ Build the canvas ============================ */
const frames = $('#fc-frames'), world = $('#fc-world');
let bounds = { x: 0, y: 0, w: W, h: H };
function build() {
  frames.innerHTML = ''; $('#fc-groups').innerHTML = ''; $('#fc-rail-list').innerHTML = '';
  const cols = {}; STATES.forEach(s => { (cols[s.depth] = cols[s.depth] || []).push(s); });        // one column per depth
  STATES.forEach(s => { s.x = 120 + s.depth * (W + GX); s.y = 200 + cols[s.depth].indexOf(s) * (H + GY); });
  Object.keys(cols).forEach(d => { const g = document.createElement('div'); g.className = 'fc-group'; g.style.left = (120 + d * (W + GX)) + 'px'; g.style.top = '-70px'; g.innerHTML = d == 0 ? `Start<small>Where the prototype opens</small>` : `${d} click${d > 1 ? 's' : ''} away<small>${cols[d].length} screen${cols[d].length > 1 ? 's' : ''}</small>`; $('#fc-groups').appendChild(g); });
  const list = $('#fc-rail-list');
  STATES.forEach(s => {
    const el = document.createElement('div'); el.className = `fc-frame is-loading${s.depth === 0 ? ' is-start' : ''}`; el.id = 'fc-f-' + s.id; el.style.left = s.x + 'px'; el.style.top = s.y + 'px';
    el.innerHTML = `<div class="fc-tag"><i>${s.id}</i><span>${esc(s.name)}</span></div><div class="fc-head" data-focus="${s.id}"><span class="fc-num">${s.id}</span><div class="fc-name">${esc(s.name)}<small>${esc(s.sub)}</small></div><span class="spacer"></span>
      <a class="fc-act" href="${P}index.html" target="_blank" title="Open the prototype on its own">Open ↗</a><button class="fc-act" data-focus="${s.id}">Use</button></div>
      <div class="fc-body" data-status="Loading…"><iframe title="${esc(s.name)}"></iframe><div class="fc-shield" data-focus="${s.id}"></div></div>`;
    frames.appendChild(el); loadFrame(s);
    if (!list.querySelector(`[data-depth="${s.depth}"]`)) list.insertAdjacentHTML('beforeend', `<div class="depth" data-depth="${s.depth}">${s.depth === 0 ? 'Start' : s.depth + ' click' + (s.depth > 1 ? 's' : '') + ' away'}</div>`);
    const b = document.createElement('button'); b.className = s.depth === 0 ? 'is-start' : ''; b.innerHTML = `<i>${s.id}</i><span>${esc(s.name)}</span>`; b.addEventListener('click', () => focus(s.id)); list.appendChild(b);
  });
  const xs = STATES.map(s => s.x), ys = STATES.map(s => s.y);
  bounds = { x: Math.min(...xs) - 200, y: Math.min(...ys) - 320, w: Math.max(...xs) + W - Math.min(...xs) + 400, h: Math.max(...ys) + H - Math.min(...ys) + 520 };
  world.style.width = (bounds.x + bounds.w) + 'px'; world.style.height = (bounds.y + bounds.h) + 'px';
  fitAll(false);
  if (q.get('focus') != null && STATES[+q.get('focus')]) setTimeout(() => focus(+q.get('focus')), 50);
}
// A frame is the prototype itself; after it loads we replay the clicks that reach this screen.
function loadFrame(s) {
  const el = $('#fc-f-' + s.id), body = el.querySelector('.fc-body'), fr = el.querySelector('iframe');
  el.classList.add('is-loading'); body.dataset.status = 'Loading…';
  fr.onload = async () => {
    const doc = fr.contentDocument; if (!doc) { el.classList.remove('is-loading'); return; }
    await wait(300);
    for (let i = 0; i < s.path.length; i++) { body.dataset.status = `Opening… (${i + 1} of ${s.path.length})`; const t = resolve(doc, s.path[i]); if (!t) break; t.click(); await wait(350); }
    el.classList.remove('is-loading');
  };
  fr.src = PROTO_URL;
}

/* ============================ Camera ============================ */
const vp = $('#fc-viewport'); let k = 1, tx = 0, ty = 0, focused = null; const MINK = 0.03, MAXK = 2;
function apply(animate) {
  world.style.transition = animate ? 'transform .35s cubic-bezier(.2,.8,.2,1)' : 'none'; world.style.transform = `translate(${tx}px, ${ty}px) scale(${k})`;
  const inv = 1 / k; world.classList.toggle('is-near', k >= 0.55);
  const tagScale = Math.min(inv, 5);
  document.querySelectorAll('.fc-tag').forEach(t => { t.style.transform = `scale(${tagScale})`; t.style.maxWidth = Math.max(60, W * k / Math.min(1, k * tagScale) - 6) + 'px'; });
  document.querySelectorAll('.fc-group').forEach(g => g.style.transform = `scale(${Math.min(inv, 2.6)})`);
  drawMini();
}
function zoomAt(nk, cx, cy, animate) { nk = Math.min(MAXK, Math.max(MINK, nk)); tx = cx - (cx - tx) * (nk / k); ty = cy - (cy - ty) * (nk / k); k = nk; apply(animate); }
function fitRect(x, y, w, h, pad, animate) { const vw = vp.clientWidth, vh = vp.clientHeight; const nk = Math.min(MAXK, Math.min((vw - pad * 2) / w, (vh - pad * 2) / h)); k = nk; tx = (vw - w * nk) / 2 - x * nk; ty = (vh - h * nk) / 2 - y * nk; apply(animate); }
function fitAll(animate) { fitRect(bounds.x, bounds.y, bounds.w, bounds.h, 24, animate); }
vp.addEventListener('wheel', e => { e.preventDefault(); const r = vp.getBoundingClientRect(); const cx = e.clientX - r.left, cy = e.clientY - r.top; if (e.ctrlKey || e.metaKey) zoomAt(k * Math.exp(-e.deltaY * 0.0022), cx, cy, false); else { tx -= e.deltaX; ty -= e.deltaY; apply(false); } }, { passive: false });
let pan = null;
vp.addEventListener('pointerdown', e => { if (e.button !== 0 || e.target.closest('.fc-head, .fc-frame.is-focus')) return; pan = { x: e.clientX, y: e.clientY, tx, ty, moved: false }; vp.classList.add('is-panning'); vp.setPointerCapture(e.pointerId); });
vp.addEventListener('pointermove', e => { if (!pan) return; const dx = e.clientX - pan.x, dy = e.clientY - pan.y; if (Math.abs(dx) + Math.abs(dy) > 3) pan.moved = true; tx = pan.tx + dx; ty = pan.ty + dy; apply(false); });
vp.addEventListener('pointerup', e => { if (!pan) return; const moved = pan.moved; pan = null; vp.classList.remove('is-panning'); if (!moved) { const t = e.target.closest('[data-focus]'); if (t) focus(+t.dataset.focus); } });
vp.addEventListener('click', e => { if (pan) return; const t = e.target.closest('.fc-head'); if (t) { const id = (e.target.closest('[data-focus]') || t).dataset.focus; if (id != null) focus(+id); } });
vp.addEventListener('dblclick', e => { if (e.target.closest('.fc-frame.is-focus')) return; const r = vp.getBoundingClientRect(); zoomAt(k * 1.6, e.clientX - r.left, e.clientY - r.top, true); });
document.addEventListener('keydown', e => {
  if (e.target.matches('input,textarea,select')) return;
  if (e.key === '+' || e.key === '=') zoomAt(k * 1.3, vp.clientWidth / 2, vp.clientHeight / 2, true);
  if (e.key === '-') zoomAt(k / 1.3, vp.clientWidth / 2, vp.clientHeight / 2, true);
  if (e.key === '0') { unfocus(); fitAll(true); }
  if (e.key === '1') zoomAt(1, vp.clientWidth / 2, vp.clientHeight / 2, true);
  if (e.key === 'Escape') unfocus(true);
});
addEventListener('resize', () => { if (focused != null) focus(focused); else fitAll(false); });
$('#fc-rail-toggle').addEventListener('click', () => { $('#fc-rail').classList.toggle('is-on'); $('#fc-rail-toggle').classList.toggle('is-on'); });
$('#fc-recrawl').addEventListener('click', () => { unfocus(); crawl(); });
$('#fc-download').addEventListener('click', () => { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([mapJSON()], { type: 'application/json' })); a.download = 'map.json'; a.click(); });

/* ============================ Focus ============================ */
function focus(id) {
  id = +id; const s = STATES[id]; if (!s) return; focused = id;
  document.querySelectorAll('.fc-frame').forEach(f => f.classList.toggle('is-focus', f.id === 'fc-f-' + id));
  fitRect(s.x, s.y, W, H, 40, true); $('#fc-focus-name').textContent = `${id} · ${s.name}`; $('#fc-focus').classList.add('is-on');
}
function unfocus(zoomOut) {
  if (focused == null) return; const s = STATES[focused]; focused = null;
  document.querySelectorAll('.fc-frame.is-focus').forEach(f => f.classList.remove('is-focus'));
  $('#fc-focus').classList.remove('is-on'); if (zoomOut) fitRect(s.x - W * .6, s.y - H * .3, W * 2.2, H * 1.6, 24, true);
}
$('#fc-focus-exit').addEventListener('click', () => unfocus(true));
$('#fc-focus-reset').addEventListener('click', () => { if (focused != null) loadFrame(STATES[focused]); });

/* ============================ Minimap ============================ */
function drawMini() {
  const svg = $('#fc-mini-svg'); svg.setAttribute('viewBox', `${bounds.x} ${bounds.y} ${bounds.w} ${bounds.h}`); svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
  const vx = -tx / k, vy = -ty / k, vw = vp.clientWidth / k, vh = vp.clientHeight / k;
  svg.innerHTML = STATES.map(s => `<rect class="f${s.depth === 0 ? ' is-start' : ''}" x="${s.x}" y="${s.y}" width="${W}" height="${H}" rx="40"/>`).join('') + `<rect class="v" x="${vx}" y="${vy}" width="${vw}" height="${vh}"/>`;
}
$('#fc-mini').addEventListener('click', e => {
  const r = $('#fc-mini-svg').getBoundingClientRect(); const sc = Math.max(bounds.w / r.width, bounds.h / r.height); const ox = (r.width - bounds.w / sc) / 2, oy = (r.height - bounds.h / sc) / 2;
  const wx = bounds.x + (e.clientX - r.left - ox) * sc, wy = bounds.y + (e.clientY - r.top - oy) * sc; tx = vp.clientWidth / 2 - wx * k; ty = vp.clientHeight / 2 - wy * k; apply(true);
});

/* ============================ Boot: prebuilt map, else browser cache, else crawl. Never asks. ============================ */
function useMap(m, how) { STATES = m.states; $('#fc-subtitle').textContent = `${P} · ${STATES.length} screens · ${how}${m.when ? ' ' + new Date(m.when).toLocaleDateString() : ''}`; build(); }
window.FLOW = { get STATES() { return STATES; }, focus: id => focus(id), mapJSON, crawl };
(async () => {
  if (!P || location.protocol === 'file:') return;
  if (!q.get('fresh')) {
    if (MAP_URL) { try { const r = await fetch(MAP_URL, { cache: 'no-store' }); if (r.ok) { const m = await r.json(); if (m && m.states && m.states.length) return useMap(m, 'mapped'); } } catch (_) {} }
    try { const c = JSON.parse(localStorage.getItem(CACHE_KEY) || 'null'); if (c && c.states && c.states.length) return useMap(c, 'mapped in this browser'); } catch (_) {}
  }
  crawl();
})();
})();
