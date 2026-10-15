/* flow.js — the flow canvas: every screen a prototype's CODE can reach, as
 * images on one pannable / zoomable canvas, with hand-drawn arrows showing
 * which click leads where. Zoom out for the whole picture, click a screen
 * to use it live, draw arrows for the developers.
 *
 * Use from a page inside the prototype's folder, e.g. /action-trace/flow/index.html:
 *   <script src="../../lib/flow.js" data-start="page=meetings"></script>
 *
 * Files next to that page (all committed, so the deployed site shows them):
 *   map.json      the screens (with the clicks that reach each one) and which
 *                 image belongs to which screen
 *   shots/<n>.png one image per screen
 * The hand-drawn arrows are NOT in those files: they are shared state, so they
 * live in the review bar's feedback store (/api/feedback, the same place as
 * comments and text edits) and everyone who opens the canvas sees them.
 *
 * Keeping it fresh after the prototype changes — either:
 *   · the Screens panel: Refresh (re-map, re-render changed screens, write files
 *     into the folder you pick once), or
 *   · node lib/flow-shots.mjs /action-trace/   (headless Chrome, no clicking)
 *
 * Modes: ?play=N opens screen N live in the full window; ?shot=N renders it
 * bare for the screenshot script. Needs http (dev server or the deployed site).
 */
(() => {
const STYLE = `
:root { --ink: #191E28; --ink-2: #262D3D; --muted: #6A7389; --line: #CDD1DC; --accent: #2E9BFF; --paper: #F7F8FA; --red: #D42551; }
* { box-sizing: border-box; }
html, body { height: 100%; margin: 0; }
body { font-family: 'Proxima Nova', Inter, system-ui, -apple-system, 'Segoe UI', sans-serif; color: var(--ink); background: #30353F; overflow: hidden; user-select: none; }
button { font-family: inherit; }
.fc-top { position: fixed; left: 0; right: 0; top: 0; height: 48px; z-index: 50; display: flex; align-items: center; gap: 12px; padding: 0 16px; background: var(--ink-2); color: #fff; box-shadow: 0 2px 8px rgba(0,0,0,.2); }
.fc-title { display: flex; align-items: baseline; gap: 10px; font-weight: 700; font-size: 14px; white-space: nowrap; }
.fc-title small { font-weight: 400; color: #AEB6C6; font-size: 12px; }
.fc-sep { width: 1px; height: 22px; background: rgba(255,255,255,.18); }
.fc-btn { height: 30px; padding: 0 10px; border: 1px solid rgba(255,255,255,.22); background: rgba(255,255,255,.06); color: #fff; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; text-decoration: none; }
.fc-btn:hover { background: rgba(255,255,255,.14); }
.fc-btn.is-on { background: #fff; color: var(--ink); }
.fc-btn.is-red.is-on { background: var(--red); color: #fff; border-color: var(--red); }
.fc-btn kbd { font: 10px/1 ui-monospace, Menlo, monospace; background: rgba(0,0,0,.25); padding: 2px 4px; border-radius: 3px; }
.fc-btn.is-on kbd { background: rgba(0,0,0,.12); }
.fc-hint { font-size: 11px; color: #AEB6C6; white-space: nowrap; margin-left: auto; }
.fc-viewport { position: fixed; inset: 48px 0 0 0; overflow: hidden; cursor: grab; background-color: #30353F; background-image: radial-gradient(rgba(255,255,255,.09) 1px, transparent 1.2px); background-size: 24px 24px; }
.fc-viewport.is-panning { cursor: grabbing; }
.fc-viewport.is-connect { cursor: crosshair; }
.fc-world { position: absolute; left: 0; top: 0; transform-origin: 0 0; will-change: transform; --inv: 1; --k: 1; }
.fc-canvas { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
.fc-frame { position: absolute; width: 1440px; height: 900px; background: transparent; border-radius: 14px; }
.fc-frame.is-live { background: #fff; box-shadow: 0 20px 60px rgba(0,0,0,.45); }
.fc-frame.is-focus { box-shadow: 0 0 0 6px var(--accent), 0 30px 80px rgba(25,30,40,.35); }
.fc-frame.is-start .fc-head { background: #E8F3FF; }
.fc-frame.is-target .fc-body { outline: 6px solid var(--red); outline-offset: -6px; }
.fc-tag { position: absolute; left: 0; bottom: 100%; margin-bottom: 6px; transform-origin: 0 100%; transform: scale(min(var(--inv), 5)); max-width: calc(1440px * var(--k) / min(1, var(--k) * min(var(--inv), 5)) - 6px); display: flex; align-items: center; gap: 6px; padding: 3px 8px 3px 4px; background: rgba(255,255,255,.92); color: var(--ink); border-radius: 6px; font-size: 12px; font-weight: 600; white-space: nowrap; overflow: hidden; pointer-events: none; }
.fc-tag span { overflow: hidden; text-overflow: ellipsis; }
.fc-tag i { font-style: normal; min-width: 18px; height: 18px; padding: 0 5px; border-radius: 9px; background: var(--ink); color: #fff; font-size: 11px; display: inline-grid; place-items: center; }
.fc-frame.is-start .fc-tag i { background: var(--accent); color: #fff; }
.fc-world:not(.is-far) .fc-tag { display: none; }
.fc-world.is-far .fc-head { display: none; }
.fc-head { position: absolute; left: 0; bottom: 100%; margin-bottom: 8px; transform-origin: 0 100%; transform: scale(var(--inv)); width: calc(1440px / var(--inv)); height: 52px; display: flex; align-items: center; gap: 10px; padding: 0 12px; border-radius: 10px; background: var(--paper); border: 1px solid var(--line); cursor: pointer; box-shadow: 0 6px 20px rgba(0,0,0,.3); }
.fc-head:hover { background: #fff; }
.fc-num { width: 30px; height: 30px; border-radius: 50%; background: var(--ink); color: #fff; font-weight: 800; font-size: 14px; display: grid; place-items: center; flex: none; }
.fc-frame.is-start .fc-num { background: var(--accent); }
.fc-name { font-size: 15px; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; }
.fc-name small { display: block; font-size: 11px; font-weight: 500; color: var(--muted); margin-top: 1px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.fc-head.is-narrow .fc-name small, .fc-head.is-narrow .fc-open { display: none; }
.fc-head .spacer { flex: 1; }
.fc-head .fc-act { height: 30px; padding: 0 10px; border: 1px solid var(--line); background: #fff; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; color: var(--ink); display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; text-decoration: none; }
.fc-head .fc-act:hover { border-color: var(--ink); }
.fc-head .fc-act.is-on { background: var(--accent); border-color: var(--accent); color: #fff; }
.fc-head .fc-act.is-on:hover { background: #1f85e0; }
.fc-frame.is-focus .fc-head { background: #E8F3FF; border-color: var(--accent); }
.fc-frame.is-focus .fc-head .fc-name small { color: #1f6fb8; }
.fc-body { position: relative; width: 1440px; height: 900px; overflow: hidden; border-radius: 14px; background: transparent; }
.fc-body img, .fc-body iframe { width: 1440px; height: 900px; border: 0; display: block; pointer-events: none; }
.fc-frame.is-focus .fc-body iframe { pointer-events: auto; }
.fc-shield { position: absolute; inset: 0; cursor: zoom-in; }
.fc-frame.is-focus .fc-shield { display: none; }
.fc-viewport.is-connect .fc-shield { cursor: crosshair; }
.fc-frame.is-loading .fc-body:after { content: attr(data-status); position: absolute; inset: 0; display: grid; place-items: center; font-size: 28px; color: var(--muted); background: rgba(247,248,250,.9); pointer-events: none; }
.fc-group { position: absolute; transform-origin: 0 100%; transform: scale(min(var(--inv), 2.6)); font-size: 44px; font-weight: 800; letter-spacing: .02em; color: rgba(255,255,255,.45); text-transform: uppercase; white-space: nowrap; pointer-events: none; }
.fc-group small { display: block; font-size: 22px; font-weight: 600; letter-spacing: 0; text-transform: none; color: rgba(255,255,255,.4); margin-top: 4px; }
/* Hand-drawn arrows */
.fc-links { position: absolute; left: 0; top: 0; overflow: visible; pointer-events: none; }
.fc-links .ln { fill: none; stroke: var(--red); stroke-width: calc(4px * var(--inv)); stroke-linecap: round; pointer-events: stroke; cursor: pointer; }
.fc-links .ln.is-selected { stroke-width: calc(5px * var(--inv)); }
.fc-links .fc-fixed { transform: translate(var(--x), var(--y)) scale(var(--inv)); }
.fc-links .ln.is-selected { stroke: #FF7A00; }
.fc-links .ln.is-temp { stroke-dasharray: 10 8; pointer-events: none; }
.fc-links .hit { fill: none; stroke: transparent; stroke-width: calc(28px * var(--inv)); pointer-events: stroke; cursor: pointer; }
.fc-links .ln.is-orphan { stroke-dasharray: 4 8; opacity: .6; }
.fc-links .dot { fill: var(--red); stroke: #fff; stroke-width: 2; }
.fc-links .head { fill: var(--red); }
.fc-links .is-selected .dot, .fc-links .is-selected .head { fill: #FF7A00; }
.fc-links .hd { fill: #fff; stroke: #FF7A00; stroke-width: 3; cursor: move; pointer-events: all; }
.fc-links .lbl { font: 600 13px/1 'Proxima Nova', Inter, system-ui, sans-serif; fill: #fff; pointer-events: none; }
.fc-links .lbl-bg { fill: var(--red); rx: 8; pointer-events: all; cursor: text; }
.fc-links .is-selected .lbl-bg { fill: #FF7A00; }
.fc-links .del { pointer-events: all; cursor: pointer; }
.fc-links .del circle { fill: #fff; stroke: #FF7A00; stroke-width: 2; }
.fc-links .del path { stroke: #FF7A00; stroke-width: 2; fill: none; }
.fc-label-edit { position: fixed; z-index: 55; display: none; padding: 6px; background: #fff; border-radius: 8px; box-shadow: 0 8px 30px rgba(0,0,0,.3); }
.fc-label-edit.is-on { display: flex; gap: 6px; }
.fc-label-edit input { width: 260px; height: 30px; border: 1px solid var(--line); border-radius: 6px; padding: 0 8px; font: 13px/1 inherit; font-family: inherit; }
.fc-label-edit button { height: 30px; padding: 0 10px; border: 0; border-radius: 6px; background: var(--ink-2); color: #fff; font-size: 12px; font-weight: 600; cursor: pointer; }
/* Focus chip, minimap, progress, notice */
.fc-focus { position: fixed; left: 50%; bottom: 22px; transform: translateX(-50%); z-index: 50; display: none; align-items: center; gap: 10px; padding: 8px 10px 8px 16px; background: var(--ink-2); color: #fff; border-radius: 24px; font-size: 13px; box-shadow: 0 8px 30px rgba(0,0,0,.3); white-space: nowrap; max-width: 90vw; }
.fc-focus.is-on { display: flex; }
.fc-focus b { color: #8FD3FF; }
.fc-mini { position: fixed; right: 16px; bottom: 16px; width: 240px; height: 140px; z-index: 50; background: rgba(20,23,30,.92); border: 1px solid rgba(255,255,255,.12); border-radius: 10px; box-shadow: 0 8px 30px rgba(0,0,0,.4); overflow: hidden; cursor: pointer; }
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
.fc-notice a { color: var(--accent); font-weight: 600; }
.fc-notice a.big { display: block; margin-top: 12px; padding: 12px 14px; background: #E8F3FF; border-radius: 8px; text-decoration: none; font: 600 15px/1.3 ui-monospace, Menlo, monospace; word-break: break-all; }
#fc-crawler { position: fixed; left: -3000px; top: 0; width: 1440px; height: 900px; border: 0; opacity: 0; pointer-events: none; }
.fc-toast { position: fixed; left: 50%; bottom: 70px; transform: translateX(-50%); z-index: 56; padding: 10px 16px; background: var(--ink-2); color: #fff; border-radius: 8px; font-size: 13px; box-shadow: 0 8px 30px rgba(0,0,0,.3); display: none; white-space: nowrap; }
.fc-toast.is-on { display: block; }
/* Screens rail */
.fc-rail { position: fixed; left: 0; top: 48px; bottom: 0; width: 300px; z-index: 40; background: #1E222B; color: #E6E9EF; border-right: 1px solid rgba(255,255,255,.1); overflow: auto; padding: 10px; transform: translateX(-100%); transition: transform .2s; display: flex; flex-direction: column; box-shadow: 8px 0 30px rgba(0,0,0,.35); }
.fc-rail.is-on { transform: none; }
.fc-rail h3 { margin: 6px 6px 8px; font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: #8F98AA; }
.fc-rail-list { flex: 1; }
.fc-rail-list button { display: flex; align-items: center; gap: 8px; width: 100%; border: 0; background: transparent; text-align: left; padding: 7px 8px; border-radius: 6px; font-size: 12px; cursor: pointer; color: #E6E9EF; }
.fc-rail-list button:hover { background: rgba(255,255,255,.08); }
.fc-rail-list button i { font-style: normal; min-width: 20px; height: 20px; padding: 0 5px; border-radius: 10px; background: #fff; color: var(--ink); font-size: 10px; font-weight: 800; display: inline-grid; place-items: center; }
.fc-rail-list button.is-start i { background: var(--accent); color: #fff; }
.fc-rail-list button span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.fc-rail-list button em { margin-left: auto; font-style: normal; font-size: 10px; color: #8F98AA; }
.fc-rail-list .depth { margin: 10px 6px 4px; font-size: 10px; color: #8F98AA; text-transform: uppercase; letter-spacing: .08em; }
.fc-rail-links { display: flex; flex-direction: column; gap: 2px; }
.fc-rail-links .ar { display: flex; align-items: center; gap: 8px; padding: 6px 8px; border-radius: 6px; font-size: 12px; color: #E6E9EF; cursor: pointer; }
.fc-rail-links .ar:hover { background: rgba(255,255,255,.08); }
.fc-rail-links .ar i { font-style: normal; color: var(--red); font-weight: 800; }
.fc-rail-links .ar span { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.fc-rail-links .ar small { color: #8F98AA; font-size: 11px; }
.fc-rail-links .ar button { border: 0; background: transparent; color: #8F98AA; font-size: 14px; cursor: pointer; padding: 0 4px; border-radius: 4px; }
.fc-rail-links .ar button:hover { color: #fff; background: var(--red); }
.fc-rail-links .none { padding: 6px 8px; font-size: 11px; color: #8F98AA; }
.fc-rail-foot { margin-top: 14px; padding: 10px 2px 0; border-top: 1px solid rgba(255,255,255,.1); display: flex; flex-direction: column; gap: 2px; }
.fc-rail-foot button, .fc-rail-foot a { display: block; width: 100%; text-align: left; border: 0; background: transparent; padding: 6px 8px; border-radius: 6px; font-size: 12px; color: #E6E9EF; cursor: pointer; text-decoration: none; }
.fc-rail-foot button:hover, .fc-rail-foot a:hover { background: rgba(255,255,255,.08); }
.fc-rail-foot button small, .fc-rail-foot a small { display: block; color: #8F98AA; font-size: 11px; margin-top: 1px; }
.fc-rail-foot .status { font-size: 11px; color: #AEB6C6; padding: 6px 8px; line-height: 1.5; }
/* Play mode */
.fc-play { position: fixed; inset: 0; display: flex; flex-direction: column; background: var(--ink-2); }
.fc-play-bar { height: 40px; display: flex; align-items: center; gap: 12px; padding: 0 14px; color: #fff; font-size: 13px; }
.fc-play-bar b { color: #8FD3FF; }
.fc-play iframe { flex: 1; border: 0; background: #fff; }
.fc-shot iframe { position: fixed; left: 0; top: 0; width: 1440px; height: 900px; border: 0; }
`;
const MARKUP = `
<header class="fc-top">
  <div class="fc-title">Flow canvas <small id="fc-subtitle">every screen the code can reach</small></div>
  <div class="fc-sep"></div>
  <button class="fc-btn" id="fc-rail-toggle">☰ Screens</button>
  <button class="fc-btn is-red" id="fc-connect" title="Draw an arrow: drag from the spot you click on one screen to the screen it opens"><svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 14L13 3M8 3h5v5"/></svg> Connect</button>
  <div class="fc-hint" id="fc-hint">Drag to pan · ⌘+scroll or pinch to zoom · double-click a screen to zoom to it · Use to click through it live</div>
</header>
<aside class="fc-rail" id="fc-rail">
  <h3>Screens found</h3>
  <div class="fc-rail-list" id="fc-rail-list"></div>
  <h3 style="margin-top:14px">Arrows</h3>
  <div class="fc-rail-links" id="fc-rail-links"></div>
  <div class="fc-rail-foot">
    <div class="status" id="fc-status"></div>
    <button id="fc-refresh">↻ Refresh from the prototype<small>Re-map the screens, re-render the ones that changed, write the files</small></button>
    <button id="fc-repaint">🖼 Repaint changed screens<small>Keep the map, re-render screens whose content changed</small></button>
    <button id="fc-save">⤓ Save to the flow folder<small>Write map.json and shots/ (asks for the folder once); or download map.json. Arrows save themselves to the shared store.</small></button>
    <a id="fc-open-proto" href="#" target="_blank">Open the prototype ↗</a>
  </div>
</aside>
<div class="fc-viewport" id="fc-viewport"><canvas class="fc-canvas" id="fc-canvas"></canvas><div class="fc-world" id="fc-world"><div id="fc-frames"></div><div id="fc-groups"></div><svg class="fc-links" id="fc-links"></svg></div></div>
<div class="fc-focus" id="fc-focus"><span>Using <b id="fc-focus-name"></b> live — click through it like the prototype</span><button class="fc-btn" id="fc-focus-reset">↻ Reset this screen</button><button class="fc-btn is-on" id="fc-focus-exit">Exit <kbd>Esc</kbd></button></div>
<div class="fc-mini" id="fc-mini" title="Click to jump"><svg id="fc-mini-svg"></svg></div>
<div class="fc-progress" id="fc-progress"><h2 id="fc-progress-title">Mapping the prototype…</h2><p id="fc-progress-copy">Opening the prototype, clicking every control on each screen and recording where it lands.</p><div class="bar"><i id="fc-progress-bar"></i></div><div class="log" id="fc-progress-log"></div></div>
<div class="fc-notice" id="fc-notice"></div>
<div class="fc-label-edit" id="fc-label-edit"><input id="fc-label-input" placeholder="What this click does, e.g. Opens the recordings modal" /><button id="fc-label-ok">Save</button></div>
<div class="fc-toast" id="fc-toast"></div>
<iframe id="fc-crawler" title="crawler"></iframe>
`;

/* ============================ Setup ============================ */
const $ = (s, r = document) => r.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const wait = ms => new Promise(r => setTimeout(r, ms));
const q = new URLSearchParams(location.search);
const ME = document.currentScript || document.querySelector('script[src*="flow.js"]');
const CFG = ME ? ME.dataset : {};
let P = q.get('p') || '';
if (!P) { const m = location.pathname.match(/^(.*\/[^/]+\/)flow\/(index\.html)?$/); if (m) P = m[1]; }
if (P && !P.endsWith('/')) P += '/';
const START = q.get('start') || CFG.start || '';
const DEPTH = +(q.get('depth') || CFG.depth || 3), MAX = +(q.get('max') || CFG.max || 24), PER = 16;
const PROTO_URL = P ? `${P}index.html?review=0${START ? '&' + START : ''}` : '';
const HERE = location.pathname.replace(/[^/]*$/, '');                      // folder of this page: where map.json and shots/ live
const CACHE_KEY = 'flowmap:' + P + ':' + START;
const W = 1440, H = 964, SH = 900, GX = 320, GY = 300;
const PLAY = q.get('play'), SHOT = q.get('shot');

/* ---- Shared helpers for finding and clicking controls (used by the crawler, the frames, play and shot modes) ---- */
const CONTROL_SEL = 'button, a, [role="button"], [data-act], [data-page], [data-flow], [data-state], .nav-item, .tab, .tabs-item, .segmented-item, [data-modal-open], [data-modal-close], [data-tab]';
const SKIP_SEL = '.flownav, .verbadge, #rvToggle, [id^="rv"], .rv-bar, .rv-side, .rv-pin, [class*="switcher"], [data-rv-mode], [data-rv-act], .rv-toggle';
const LAYER_SEL = '[data-layer], .layer, .modal-overlay, .drawer-overlay, .modal, .drawer, [role="dialog"]';
const POP_SEL = '[data-pop], .pop, .popover, .dropdown-menu, .menu, .dropdown.is-open, [data-dropdown].is-open';
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
async function replayIn(doc, path, onStep) { for (let i = 0; i < path.length; i++) { onStep && onStep(i); const el = resolve(doc, path[i]); if (!el) return false; el.click(); await wait(350); } return true; }

/* ============================ Play / shot modes (one live screen, no canvas) ============================ */
if (P && (PLAY != null || SHOT != null)) {
  const st = document.createElement('style'); st.textContent = STYLE; document.head.appendChild(st);
  (async () => {
    let map = null; try { map = await (await fetch('map.json', { cache: 'no-store' })).json(); } catch (_) {}
    if (!map) { try { map = JSON.parse(localStorage.getItem(CACHE_KEY) || 'null'); } catch (_) {} }
    const s = map && map.states[+(PLAY ?? SHOT)]; if (!s) { document.body.innerHTML = '<p style="padding:20px;font-family:sans-serif">No such screen in map.json.</p>'; return; }
    if (SHOT != null) { document.body.className = 'fc-shot'; document.body.style.margin = '0'; }
    else document.body.insertAdjacentHTML('beforeend', `<div class="fc-play"><div class="fc-play-bar"><a class="fc-btn" href="./">← Back to the canvas</a><span>Screen <b>${s.id} · ${esc(s.name)}</b></span><span style="color:#AEB6C6;font-size:12px">${esc(s.sub)}</span><a class="fc-btn" style="margin-left:auto" href="${P}index.html" target="_blank">Open the prototype from the start ↗</a></div></div>`);
    const fr = document.createElement('iframe'); fr.title = s.name; (document.querySelector('.fc-play') || document.body).appendChild(fr);
    fr.onload = async () => { await wait(300); await replayIn(fr.contentDocument, s.path); await wait(200); document.title = 'ready · ' + s.name; };
    fr.src = PROTO_URL;
  })();
  return;
}

/* ============================ Canvas ============================ */
const st = document.createElement('style'); st.textContent = STYLE; document.head.appendChild(st);
document.body.insertAdjacentHTML('beforeend', MARKUP);
const notice = html => { $('#fc-notice').innerHTML = html; $('#fc-notice').classList.add('is-on'); };
if (!P) notice(`<h2>No prototype to map</h2>Put this page at <code>/&lt;prototype&gt;/flow/index.html</code>, or add <code>?p=/&lt;prototype&gt;/</code> to the URL.`);
else if (location.protocol === 'file:') { const url = `http://localhost:5733${P}flow/`; notice(`<h2>Open this through the dev server</h2>The canvas has to look inside the prototype's frames to map it, and a <code>file://</code> page is not allowed to. Open it here instead (the Icarus dev server has to be running):<a class="big" href="${url}">${url}</a>`); }
$('#fc-open-proto').href = P ? `${P}index.html` : '#';
if (P) $('#fc-subtitle').textContent = `${P} · every screen the code can reach`;

/* ============================ Crawler ============================ */
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
function nameOf(fp, i) { const top = fp.layers[fp.layers.length - 1]; if (top) { const t = top.split(':').slice(1).join(':'); if (t && t.length > 2) return t; } if (fp.screen) return fp.screen.replace(/^Screen \d+(\.5)?[a-z]? · /, ''); return fp.main || fp.nav[0] || `Screen ${i}`; }
function subOf(fp) { const bits = []; if (fp.screen) bits.push(fp.screen); else if (fp.nav.length) bits.push(fp.nav.join(' · ')); if (fp.layers.length > 1) bits.push(fp.layers.map(l => l.split(':')[0]).join(' + ')); return bits.join(' · ') || 'Base page'; }

let STATES = [], LINKS = [], MAP_WHEN = null;
const prog = { el: null, show(title, copy) { $('#fc-progress-title').textContent = title; $('#fc-progress-copy').textContent = copy; $('#fc-progress-log').textContent = ''; $('#fc-progress-bar').style.width = '2%'; $('#fc-progress').classList.add('is-on'); }, say(m) { const l = $('#fc-progress-log'); l.textContent += m + '\n'; l.scrollTop = 1e6; }, pct(p) { $('#fc-progress-bar').style.width = p + '%'; }, hide() { $('#fc-progress').classList.remove('is-on'); } };
const fr = () => $('#fc-crawler');
const loadCrawler = () => new Promise(res => { const f = fr(); f.onload = () => setTimeout(res, 500); f.src = PROTO_URL + '&_=' + Date.now(); });

async function crawl() {
  prog.show('Mapping the prototype…', 'Opening the prototype, clicking every control on each screen and recording where it lands.');
  await loadCrawler(); let win = fr().contentWindow, doc = fr().contentDocument;
  if (!doc || !doc.body) { prog.hide(); notice(`<h2>Could not read the prototype</h2>The frame at <code>${esc(PROTO_URL)}</code> did not load, or the browser refused access to it.`); return false; }
  let acc = null; try { acc = win.eval('(typeof S === "object" && typeof render === "function") ? ({ get: () => S, set: o => { Object.keys(S).forEach(k => delete S[k]); Object.assign(S, o); }, render: () => render() }) : null'); } catch (_) {}
  const fast = !!acc;
  const snapshot = () => { if (!fast) return null; try { return JSON.parse(JSON.stringify(acc.get())); } catch (_) { return null; } };
  const restore = async s => {
    if (fast && s.snap) { try { acc.set(JSON.parse(JSON.stringify(s.snap))); doc.querySelectorAll('#pops').forEach(p => p.innerHTML = ''); acc.render(); await wait(120); return true; } catch (_) {} }
    await loadCrawler(); win = fr().contentWindow; doc = fr().contentDocument; return replayIn(doc, s.path);
  };
  const old = Object.fromEntries(STATES.map(s => [s.sig, s]));            // keep images + hashes of screens we already know
  const fp0 = fingerprint(win);
  const found = [{ id: 0, fp: fp0, sig: fp0.sig, name: nameOf(fp0, 0), sub: subOf(fp0), path: [], depth: 0, snap: snapshot() }];
  const bySig = new Map([[fp0.sig, 0]]); const queue = [0];
  prog.say(`start: ${found[0].name}  (${fast ? 'state snapshots' : 'reload + replay'})`);
  while (queue.length && found.length < MAX) {
    const s = found[queue.shift()]; if (s.depth >= DEPTH) continue;
    await restore(s); const ctrls = controlsIn(doc).slice(0, PER); prog.say(`screen ${s.id} · ${ctrls.length} controls`);
    for (const c of ctrls) {
      if (found.length >= MAX) break;
      if (!(await restore(s))) continue; const el = resolve(doc, c); if (!el) continue;
      try { el.click(); } catch (_) { continue; } await wait(fast ? 260 : 380);
      if (fr().contentDocument !== doc) { await loadCrawler(); win = fr().contentWindow; doc = fr().contentDocument; await replayIn(doc, s.path); continue; }
      const fp = fingerprint(win); if (fp.sig === s.sig || bySig.has(fp.sig)) continue;
      const id = found.length; const ns = { id, fp, sig: fp.sig, name: nameOf(fp, id), sub: subOf(fp), path: [...s.path, c], depth: s.depth + 1, snap: snapshot() };
      found.push(ns); bySig.set(fp.sig, id); queue.push(id); prog.say(`  + ${id}: ${ns.name}`); prog.pct(Math.min(96, 4 + found.length / MAX * 92));
    }
  }
  found.forEach(s => { const o = old[s.sig]; if (o) { s.shot = o.shot; s.hash = o.hash; } });
  STATES = found; MAP_WHEN = Date.now(); fr().src = 'about:blank';
  prog.pct(100); await wait(150); prog.hide(); cache(); build(); return true;
}

/* ============================ Rendering a screen to an image ============================ */
// The live screen's document is serialised into an SVG <foreignObject> and drawn on a canvas.
// Everything the prototype needs is inlined first (images, CSS url()s, canvases, field values).
const dataCache = new Map();
async function toDataURL(url) { if (dataCache.has(url)) return dataCache.get(url); const p = (async () => { try { const b = await (await fetch(url)).blob(); return await new Promise(r => { const fr = new FileReader(); fr.onload = () => r(fr.result); fr.readAsDataURL(b); }); } catch (_) { return url; } })(); dataCache.set(url, p); return p; }
const hash = s => { let h = 0x811c9dc5; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; } return h.toString(16).padStart(8, '0'); };
async function serializeDoc(doc) {
  const clone = doc.documentElement.cloneNode(true);
  clone.querySelectorAll('script, noscript, #rvToggle, .rv-toggle, .rv-bar, .rv-side, [class*="switcher"]').forEach(e => e.remove());
  // Field values, canvases and scroll offsets are not part of the markup: copy them over.
  const live = [...doc.querySelectorAll('input, textarea, select')], copy = [...clone.querySelectorAll('input, textarea, select')];
  copy.forEach((el, i) => { const src = live[i]; if (!src) return; if (el.tagName === 'TEXTAREA') el.textContent = src.value; else if (el.tagName === 'SELECT') [...el.options].forEach((o, j) => o.selected ? o.setAttribute('selected', '') : o.removeAttribute('selected')); else { el.setAttribute('value', src.value); if (src.checked) el.setAttribute('checked', ''); else el.removeAttribute('checked'); } });
  const lc = [...doc.querySelectorAll('canvas')], cc = [...clone.querySelectorAll('canvas')];
  cc.forEach((el, i) => { try { const img = clone.ownerDocument.createElement('img'); img.setAttribute('src', lc[i].toDataURL()); img.setAttribute('style', el.getAttribute('style') || ''); img.setAttribute('width', lc[i].width); img.setAttribute('height', lc[i].height); el.replaceWith(img); } catch (_) {} });
  const ls = [...doc.querySelectorAll('*')].filter(e => e.scrollTop || e.scrollLeft);
  if (ls.length) { const all = [...doc.querySelectorAll('*')], allc = [...clone.querySelectorAll('*')]; ls.forEach(e => { const c = allc[all.indexOf(e)]; if (!c) return; const inner = c.ownerDocument.createElement('div'); inner.setAttribute('style', `transform:translate(${-e.scrollLeft}px,${-e.scrollTop}px)`); while (c.firstChild) inner.appendChild(c.firstChild); c.appendChild(inner); c.style.overflow = 'hidden'; }); }
  const base = doc.baseURI;
  for (const img of clone.querySelectorAll('img, image')) { const a = img.getAttribute('src') || img.getAttribute('href'); if (a && !a.startsWith('data:')) { const d = await toDataURL(new URL(a, base).href); img.setAttribute(img.hasAttribute('src') ? 'src' : 'href', d); } }
  for (const el of clone.querySelectorAll('[style*="url("]')) { const s = el.getAttribute('style'); const m = [...s.matchAll(/url\((["']?)(?!data:)([^)"']+)\1\)/g)]; let out = s; for (const x of m) out = out.replace(x[0], `url("${await toDataURL(new URL(x[2], base).href)}")`); el.setAttribute('style', out); }
  for (const stl of clone.querySelectorAll('style')) { const s = stl.textContent; const m = [...s.matchAll(/url\((["']?)(?!data:)([^)"']+)\1\)/g)]; if (!m.length) continue; let out = s; for (const x of m) out = out.replace(x[0], `url("${await toDataURL(new URL(x[2], base).href)}")`); stl.textContent = out; }
  clone.querySelectorAll('link[rel="stylesheet"]').forEach(l => l.remove());
  return new XMLSerializer().serializeToString(clone);
}
async function renderShot(doc) {
  const html = await serializeDoc(doc);
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${SH}"><foreignObject width="100%" height="100%">${html}</foreignObject></svg>`;
  const img = new Image(); img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg); await img.decode();
  const c = document.createElement('canvas'); c.width = W; c.height = SH; const ctx = c.getContext('2d'); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, SH); ctx.drawImage(img, 0, 0);
  const blob = await new Promise((res, rej) => c.toBlob(b => b ? res(b) : rej(new Error('toBlob failed')), 'image/png'));
  return { blob, hash: hash(html) };
}
// Images live in IndexedDB until they are written to the folder, so a repaint survives a reload.
const idb = { db: null, async open() { if (this.db) return this.db; return this.db = await new Promise((res, rej) => { const r = indexedDB.open('flowcanvas', 1); r.onupgradeneeded = () => { r.result.createObjectStore('shots'); r.result.createObjectStore('handles'); }; r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); }); },
  async get(store, key) { const db = await this.open(); return new Promise(res => { const t = db.transaction(store).objectStore(store).get(key); t.onsuccess = () => res(t.result); t.onerror = () => res(null); }); },
  async set(store, key, val) { const db = await this.open(); return new Promise(res => { const t = db.transaction(store, 'readwrite').objectStore(store).put(val, key); t.onsuccess = () => res(true); t.onerror = () => res(false); }); } };
const shotKey = s => `${P}|${s.sig}`;

async function repaint(onlyChanged = true) {
  if (!STATES.length) return;
  prog.show('Rendering screens…', onlyChanged ? 'Opening each screen, checking whether it changed, and re-rendering the ones that did.' : 'Opening each screen and rendering it to an image.');
  let done = 0, changed = 0, failed = 0;
  for (const s of STATES) {
    prog.say(`screen ${s.id} · ${s.name}`);
    await loadCrawler(); const doc = fr().contentDocument; if (!doc) { failed++; continue; }
    const ok = await replayIn(doc, s.path); await wait(400);
    try {
      const html = await serializeDoc(doc); const h = hash(html);
      const cached = await idb.get('shots', shotKey(s));
      if (onlyChanged && s.hash === h && (cached || s.shot)) { prog.say('   unchanged'); }
      else { const { blob } = await renderShot(doc); await idb.set('shots', shotKey(s), { blob, hash: h, when: Date.now() }); s.hash = h; s.shot = `shots/${s.id}.png`; s.fresh = true; changed++; prog.say(`   rendered${ok ? '' : ' (replay was incomplete)'}`); }
    } catch (e) { failed++; prog.say(`   could not render: ${e.message}`); }
    done++; prog.pct(Math.round(done / STATES.length * 100));
  }
  fr().src = 'about:blank'; await wait(150); prog.hide(); cache(); build();
  toast(`${changed} screen${changed === 1 ? '' : 's'} re-rendered${failed ? `, ${failed} failed` : ''}. ${dirHandle ? 'Writing files…' : 'Save to the flow folder to keep them.'}`);
  if (dirHandle) await writeAll();
}

/* ============================ Writing files into the flow folder ============================ */
let dirHandle = null;
const mapJSON = (forFile) => JSON.stringify({ version: 2, when: forFile ? Date.now() : (MAP_WHEN || Date.now()), p: P, start: START, depth: DEPTH, max: MAX, states: STATES.map(({ snap, x, y, fresh, ...s }) => s) }, null, 1);
async function getDir(ask) {
  if (!dirHandle) { try { dirHandle = await idb.get('handles', P) || null; } catch (_) {} }
  if (dirHandle) { try { if ((await dirHandle.queryPermission({ mode: 'readwrite' })) === 'granted' || (ask && (await dirHandle.requestPermission({ mode: 'readwrite' })) === 'granted')) return dirHandle; } catch (_) {} dirHandle = null; }
  if (!ask) return null;
  if (!window.showDirectoryPicker) return null;
  try { dirHandle = await window.showDirectoryPicker({ mode: 'readwrite', id: 'flow' + P.replace(/\W/g, '') }); await idb.set('handles', P, dirHandle); return dirHandle; } catch (_) { return null; }
}
async function writeFile(dir, name, data) { const h = await dir.getFileHandle(name, { create: true }); const w = await h.createWritable(); await w.write(data); await w.close(); }
async function writeAll() {
  const dir = await getDir(true);
  if (!dir) { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([mapJSON()], { type: 'application/json' })); a.download = 'map.json'; a.click(); toast('map.json downloaded. Put it next to the flow page; this browser cannot write into folders, so images stay in the browser cache.'); return; }
  try {
    let n = 0; const shots = await dir.getDirectoryHandle('shots', { create: true });
    for (const s of STATES) { const c = await idb.get('shots', shotKey(s)); if (c && c.blob && (s.fresh || !(await exists(shots, `${s.id}.png`)))) { await writeFile(shots, `${s.id}.png`, c.blob); s.shot = `shots/${s.id}.png`; s.fresh = false; n++; } }
    await writeFile(dir, 'map.json', mapJSON(true)); MAP_WHEN = Date.now();
    toast(`Written: map.json${n ? ` and ${n} image${n > 1 ? 's' : ''}` : ''} → ${dir.name}/`); setStatus();
  } catch (e) { toast('Could not write: ' + e.message); }
}
async function exists(dir, name) { try { await dir.getFileHandle(name); return true; } catch (_) { return false; } }
function cache(linksChanged) { if (linksChanged) store.changed(); try { localStorage.setItem(CACHE_KEY, mapJSON()); } catch (_) {} setStatus(); }
/* ---- Arrows live in the review bar's shared store: GET/POST /api/feedback?p=<prototype>, ops { t:'link', l } / { t:'link-del', id }.
   Locally that is tools/serve.mjs writing <prototype>/feedback.json; on Vercel api/feedback.js on Neon. Same token rules as comments. ---- */
const store = {
  api: '/api/feedback', online: false, pollT: null, seen: new Map(),
  token() { try { return localStorage.getItem('rv:token') || ''; } catch (_) { return ''; } },
  askToken() { const t = (prompt('This prototype needs a review token to save changes:') || '').trim(); try { if (t) localStorage.setItem('rv:token', t); } catch (_) {} return t; },
  author() { let n = ''; try { n = localStorage.getItem('rv:author') || ''; } catch (_) {} if (!n) { n = (prompt('Your name, so others know who drew this arrow:') || '').trim().slice(0, 60); try { if (n) localStorage.setItem('rv:author', n); } catch (_) {} } return n; },
  async load() {
    try { const r = await fetch(`${this.api}?p=${encodeURIComponent(P)}`, { cache: 'no-store' }); if (!r.ok) throw 0; const doc = await r.json(); this.online = true; this.adopt(doc.links || []); }
    catch (_) { this.online = false; try { const c = JSON.parse(localStorage.getItem(CACHE_KEY + ':links') || 'null'); if (c) this.adopt(c); } catch (_) {} }
    setStatus();
  },
  adopt(links) { const before = JSON.stringify(LINKS); LINKS = links.map(l => ({ ...l })); this.seen = new Map(LINKS.map(l => [l.id, JSON.stringify(l)])); try { localStorage.setItem(CACHE_KEY + ':links', JSON.stringify(LINKS)); } catch (_) {} if (JSON.stringify(LINKS) !== before) { if (selected != null && !LINKS[selected]) selected = null; drawLinks(); } },
  // After a local edit: send what differs from what the store last gave us.
  async changed() {
    const ops = []; const now = new Map(LINKS.map(l => [l.id, JSON.stringify(l)]));
    for (const [id, json] of now) if (this.seen.get(id) !== json) ops.push({ t: 'link', l: JSON.parse(json) });
    for (const id of this.seen.keys()) if (!now.has(id)) ops.push({ t: 'link-del', id });
    this.seen = now; try { localStorage.setItem(CACHE_KEY + ':links', JSON.stringify(LINKS)); } catch (_) {}
    if (!ops.length) return;
    const post = () => fetch(this.api, { method: 'POST', headers: { 'Content-Type': 'application/json', ...(this.token() ? { 'x-review-token': this.token() } : {}) }, body: JSON.stringify({ p: P, ops }) });
    try {
      let r = await post(); if (r.status === 401 && this.askToken()) r = await post(); if (!r.ok) throw 0; this.online = true;
      const doc = await r.json();
      if (!Array.isArray(doc.links)) toast('The store on this server does not know about arrows yet — restart the Icarus dev server (it needs the new tools/feedback-store.mjs).');
      else { const want = JSON.stringify(LINKS.map(l => l.id).sort()), got = JSON.stringify(doc.links.map(l => l.id).sort()); if (want !== got) { toast('The store kept a different set of arrows — showing what it has.'); this.adopt(doc.links); } }
    }
    catch (_) { this.online = false; toast('Could not save the arrows to the shared store — they are kept in this browser for now.'); }
    setStatus();
  },
  poll() { clearInterval(this.pollT); this.pollT = setInterval(async () => { if (document.hidden || drag) return; try { const r = await fetch(`${this.api}?p=${encodeURIComponent(P)}`, { cache: 'no-store' }); if (!r.ok) throw 0; const doc = await r.json(); this.online = true; if (JSON.stringify(doc.links || []) !== JSON.stringify([...this.seen.values()].map(j => JSON.parse(j)))) this.adopt(doc.links || []); } catch (_) { this.online = false; } setStatus(); }, 5000); },
};
function renderRailLinks() {
  const el = $('#fc-rail-links'); if (!el) return; const S = bySig();
  el.innerHTML = LINKS.length ? LINKS.map((L, i) => { const a = S[L.from.sig], b = S[L.to.sig]; return `<div class="ar" data-sel="${i}"><i>→</i><span>${a && b ? `${a.id} → ${b.id}` : 'screen gone'}${L.label ? ' · ' + esc(L.label) : ''}<br><small>${esc(L.author || 'unknown')}${a && b ? '' : ' · a screen it points at is no longer in the map'}</small></span><button type="button" data-rm="${i}" title="Delete this arrow">✕</button></div>`; }).join('') : '<div class="none">No arrows yet. Press Connect and drag from a spot on one screen to the screen it opens.</div>';
}
function setStatus() { renderRailLinks(); $('#fc-status').innerHTML = `${STATES.length} screens · ${STATES.filter(s => s.shot).length} with images · ${LINKS.length} arrow${LINKS.length === 1 ? '' : 's'} ${store.online ? '<b style="color:#33D097">shared</b>' : '<b style="color:#FFB347">local only</b>'}${dirHandle ? ` · writing to <b>${esc(dirHandle.name)}/</b>` : ''}`; }
let toastT; function toast(m) { const t = $('#fc-toast'); t.textContent = m; t.classList.add('is-on'); clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove('is-on'), 5000); }

/* ============================ Build the canvas ============================ */
const frames = $('#fc-frames'), world = $('#fc-world');
let bounds = { x: 0, y: 0, w: W, h: H };
function build() {
  frames.innerHTML = ''; $('#fc-groups').innerHTML = ''; $('#fc-rail-list').innerHTML = '';
  const cols = {}; STATES.forEach(s => { (cols[s.depth] = cols[s.depth] || []).push(s); });
  STATES.forEach(s => { s.x = 120 + s.depth * (W + GX); s.y = 200 + cols[s.depth].indexOf(s) * (H + GY); });
  Object.keys(cols).forEach(d => { const g = document.createElement('div'); g.className = 'fc-group'; g.style.left = (120 + d * (W + GX)) + 'px'; g.style.top = '-70px'; g.innerHTML = d == 0 ? `Start<small>Where the prototype opens</small>` : `${d} click${d > 1 ? 's' : ''} away<small>${cols[d].length} screen${cols[d].length > 1 ? 's' : ''}</small>`; $('#fc-groups').appendChild(g); });
  const list = $('#fc-rail-list');
  STATES.forEach(s => {
    const el = document.createElement('div'); el.className = `fc-frame${s.depth === 0 ? ' is-start' : ''}`; el.id = 'fc-f-' + s.id; el.style.left = s.x + 'px'; el.style.top = s.y + 'px';
    el.innerHTML = `<div class="fc-tag"><i>${s.id}</i><span>${esc(s.name)}</span></div><div class="fc-head" data-focus="${s.id}"><span class="fc-num">${s.id}</span><div class="fc-name">${esc(s.name)}<small>${esc(s.sub)}</small></div><span class="spacer"></span>
      <a class="fc-act fc-open" href="?play=${s.id}" target="_blank" title="Open this screen live in its own tab">Open ↗</a><button class="fc-act fc-use" data-focus="${s.id}" title="Use this screen live; click again to go back to the overview">Use</button></div>
      <div class="fc-body" data-status="Loading…"><div class="fc-shield" data-focus="${s.id}"></div></div>`;
    frames.appendChild(el); showImage(s);
    if (!list.querySelector(`[data-depth="${s.depth}"]`)) list.insertAdjacentHTML('beforeend', `<div class="depth" data-depth="${s.depth}">${s.depth === 0 ? 'Start' : s.depth + ' click' + (s.depth > 1 ? 's' : '') + ' away'}</div>`);
    const b = document.createElement('button'); b.className = s.depth === 0 ? 'is-start' : ''; b.innerHTML = `<i>${s.id}</i><span>${esc(s.name)}</span>${s.shot ? '' : '<em>live</em>'}`; b.addEventListener('click', () => focus(s.id)); list.appendChild(b);
  });
  const xs = STATES.map(s => s.x), ys = STATES.map(s => s.y);
  bounds = { x: Math.min(...xs) - 200, y: Math.min(...ys) - 320, w: Math.max(...xs) + W - Math.min(...xs) + 400, h: Math.max(...ys) + H - Math.min(...ys) + 520 };
  world.style.width = (bounds.x + bounds.w) + 'px'; world.style.height = (bounds.y + bounds.h) + 'px';
  drawLinks(); drawMini(); setStatus(); fitAll(false);
  if (q.get('focus') != null && STATES[+q.get('focus')]) setTimeout(() => focus(+q.get('focus')), 50);
}
// A frame shows its image when there is one (file next to the page, else the browser cache); otherwise the live prototype.
async function showImage(s) {
  const el = $('#fc-f-' + s.id), body = el.querySelector('.fc-body'); body.querySelectorAll('img, iframe').forEach(x => x.remove());
  el.classList.remove('is-live'); el.dataset.live = '';
  if (s.img) { el.classList.remove('is-loading'); draw(); return; }
  el.classList.add('is-loading'); body.dataset.status = 'Loading…';
  let blob = null;
  const c = await idb.get('shots', shotKey(s)); if (c && c.blob && (!s.hash || c.hash === s.hash)) blob = c.blob;
  if (!blob && s.shot) { try { const r = await fetch(HERE + s.shot, { cache: 'no-store' }); if (r.ok) blob = await r.blob(); } catch (_) {} }
  if (!blob) return showLive(s);
  try {
    s.img = await createImageBitmap(blob);
    s.small = await createImageBitmap(blob, { resizeWidth: 720, resizeHeight: 450, resizeQuality: 'medium' });   // for far zooms: cheaper to paint, smoother to look at
  } catch (_) { return showLive(s); }
  if (el.dataset.live !== '1') { el.classList.remove('is-loading'); draw(); }
}
function showLive(s) {
  const el = $('#fc-f-' + s.id), body = el.querySelector('.fc-body'); body.querySelectorAll('img, iframe').forEach(x => x.remove());
  const f = document.createElement('iframe'); f.title = s.name; el.classList.add('is-loading', 'is-live'); body.dataset.status = 'Loading…'; el.dataset.live = '1'; draw();
  f.onload = async () => { const doc = f.contentDocument; if (!doc) { el.classList.remove('is-loading'); return; } await wait(300); await replayIn(doc, s.path, i => body.dataset.status = `Opening… (${i + 1} of ${s.path.length})`); el.classList.remove('is-loading'); };
  body.prepend(f); f.src = PROTO_URL;
}

/* ============================ Painter: every screen image on one canvas ============================ */
// Painted once per animation frame from the camera, so a zoom gesture never asks the browser to
// re-rasterise large DOM images; the DOM keeps only the small overlays (headers, tags, arrows).
const cv = $('#fc-canvas'); const cx = cv.getContext('2d', { alpha: false });
let dpr = 1;
function sizeCanvas() { dpr = Math.min(2, window.devicePixelRatio || 1); cv.width = Math.round(vp.clientWidth * dpr); cv.height = Math.round(vp.clientHeight * dpr); draw(); }
function draw() {
  cx.setTransform(1, 0, 0, 1, 0, 0); cx.fillStyle = '#30353F'; cx.fillRect(0, 0, cv.width, cv.height);
  cx.setTransform(dpr * k, 0, 0, dpr * k, dpr * tx, dpr * ty);
  cx.imageSmoothingEnabled = true; cx.imageSmoothingQuality = k < 0.5 ? 'low' : 'high';
  const vx0 = -tx / k, vy0 = -ty / k, vx1 = vx0 + vp.clientWidth / k, vy1 = vy0 + vp.clientHeight / k;
  const r = 14;
  for (const s of STATES) {
    if (s.x > vx1 || s.y > vy1 || s.x + W < vx0 || s.y + SH < vy0) continue;               // off screen
    const el = document.getElementById('fc-f-' + s.id); if (el && el.dataset.live === '1') continue;   // live frame: the DOM shows it
    cx.fillStyle = 'rgba(0,0,0,.35)'; cx.beginPath(); cx.roundRect(s.x, s.y + 14 / k, W, SH, r); cx.fill();   // cheap drop shadow
    cx.save(); cx.beginPath(); cx.roundRect(s.x, s.y, W, SH, r); cx.clip();
    cx.fillStyle = '#fff'; cx.fillRect(s.x, s.y, W, SH);
    const bmp = k < 0.5 && s.small ? s.small : s.img; if (bmp) cx.drawImage(bmp, s.x, s.y, W, SH);
    cx.restore();
    cx.lineWidth = 2 / k; cx.strokeStyle = 'rgba(255,255,255,.08)'; cx.beginPath(); cx.roundRect(s.x, s.y, W, SH, r); cx.stroke();
  }
}

/* ============================ Camera ============================ */
const vp = $('#fc-viewport'); let k = 1, tx = 0, ty = 0, focused = null; const MINK = 0.03, MAXK = 2;
// The camera: one transform on the world plus one CSS variable (--inv = 1/zoom) that every
// counter-scaled element (headers, tags, arrow labels, stroke widths) reads in CSS. Wheel
// ticks are coalesced per animation frame, so a zoom gesture costs one style write per frame.
let raf = 0, rafT = 0, narrowNow = null, farNow = null, last = { k: 1, tx: 0, ty: 0 }, anim = null;
function apply(animate) {
  if (animate) {                                                          // tween from where we are to where the camera was just set
    const from = { ...last }, to = { k, tx, ty }; if (anim) cancelAnimationFrame(anim.raf);
    const t0 = performance.now(), D = 350, ease = t => 1 - Math.pow(1 - t, 3);
    const step = () => { const p = Math.min(1, (performance.now() - t0) / D), e = ease(p); const lk = Math.exp(Math.log(from.k) + (Math.log(to.k) - Math.log(from.k)) * e);
      k = lk; tx = from.tx + (to.tx - from.tx) * e; ty = from.ty + (to.ty - from.ty) * e; applyNow(); if (p < 1) sched(step); else anim = null; };
    const sched = fn => { let done = false; const once = () => { if (done) return; done = true; cancelAnimationFrame(anim.raf); clearTimeout(anim.t); fn(); }; anim.raf = requestAnimationFrame(once); anim.t = setTimeout(once, 32); };   // timer fallback for hidden tabs
    anim = { raf: 0, t: 0 }; sched(step); return;
  }
  if (anim) { cancelAnimationFrame(anim.raf); anim = null; }
  if (raf) return;
  const run = () => { if (!raf) return; cancelAnimationFrame(raf); clearTimeout(rafT); raf = 0; applyNow(); };
  raf = requestAnimationFrame(run); rafT = setTimeout(run, 24);          // the timer covers hidden tabs, where animation frames pause
}
function applyNow() {
  last = { k, tx, ty };
  world.style.transform = `translate3d(${tx}px, ${ty}px, 0) scale(${k})`; world.style.setProperty('--inv', 1 / k); world.style.setProperty('--k', k);
  draw();
  const far = k < 0.28; if (far !== farNow) { farNow = far; world.classList.toggle('is-far', far); }
  const narrow = W * k < 620; if (narrow !== narrowNow) { narrowNow = narrow; document.querySelectorAll('.fc-head').forEach(h => h.classList.toggle('is-narrow', narrow)); }
  miniView();
}
function zoomAt(nk, cx, cy, animate) { nk = Math.min(MAXK, Math.max(MINK, nk)); tx = cx - (cx - tx) * (nk / k); ty = cy - (cy - ty) * (nk / k); k = nk; apply(animate); }
function fitRect(x, y, w, h, pad, animate) { const vw = vp.clientWidth, vh = vp.clientHeight; const nk = Math.min(MAXK, Math.min((vw - pad * 2) / w, (vh - pad * 2) / h)); k = nk; tx = (vw - w * nk) / 2 - x * nk; ty = (vh - h * nk) / 2 - y * nk; apply(animate); }
function fitAll(animate) { fitRect(bounds.x, bounds.y, bounds.w, bounds.h, 24, animate); }
const toWorld = (cx, cy) => { const r = vp.getBoundingClientRect(); return { x: (cx - r.left - tx) / k, y: (cy - r.top - ty) / k }; };
vp.addEventListener('wheel', e => { e.preventDefault(); const r = vp.getBoundingClientRect(); const cx = e.clientX - r.left, cy = e.clientY - r.top; if (e.ctrlKey || e.metaKey) zoomAt(k * Math.exp(-e.deltaY * 0.0048), cx, cy, false); else { tx -= e.deltaX; ty -= e.deltaY; apply(false); } }, { passive: false });
let pan = null;
vp.addEventListener('pointerdown', e => {
  if (e.button !== 0) return;
  if (connect) return startConnect(e);
  if (e.target.closest('.fc-head, .fc-frame.is-focus, .fc-links [class]')) return;
  pan = { x: e.clientX, y: e.clientY, tx, ty, moved: false }; vp.classList.add('is-panning'); vp.setPointerCapture(e.pointerId);
});
vp.addEventListener('pointermove', e => { if (drag) return moveConnect(e); if (!pan) return; const dx = e.clientX - pan.x, dy = e.clientY - pan.y; if (Math.abs(dx) + Math.abs(dy) > 3) pan.moved = true; tx = pan.tx + dx; ty = pan.ty + dy; apply(false); });
vp.addEventListener('pointerup', e => { if (drag) return endConnect(e); if (!pan) return; const moved = pan.moved; pan = null; vp.classList.remove('is-panning'); if (!moved && !connect) { const t = e.target.closest('[data-focus]'); if (t) toggleFocus(+t.dataset.focus); else if (selected != null && !e.target.closest('.fc-links')) selectLink(null); } });
vp.addEventListener('click', e => { if (pan || connect || e.target.closest('a')) return; const t = e.target.closest('.fc-head'); if (t) { const id = (e.target.closest('[data-focus]') || t).dataset.focus; if (id != null) toggleFocus(+id); } });
function toggleFocus(id) { if (focused === id) unfocus(true); else focus(id); }
vp.addEventListener('dblclick', e => { if (e.target.closest('.fc-frame.is-focus') || connect) return; const f = e.target.closest('.fc-frame'); if (f) { const s = STATES[+f.id.replace('fc-f-', '')]; return fitRect(s.x, s.y - 70, W, SH + 70, 24, true); } const r = vp.getBoundingClientRect(); zoomAt(k * 2, e.clientX - r.left, e.clientY - r.top, true); });
document.addEventListener('keydown', e => {
  if (e.target.matches('input,textarea,select')) return;
  if (e.key === '+' || e.key === '=') zoomAt(k * 1.6, vp.clientWidth / 2, vp.clientHeight / 2, true);
  if (e.key === '-') zoomAt(k / 1.6, vp.clientWidth / 2, vp.clientHeight / 2, true);
  if (e.key === '0') { unfocus(); fitAll(true); }
  if (e.key === '1') zoomAt(1, vp.clientWidth / 2, vp.clientHeight / 2, true);
  if (e.key === 'Escape') { if (selected != null) { selectLink(null); return; } if (connect) return setConnect(false); unfocus(true); }
  if ((e.key === 'Delete' || e.key === 'Backspace') && selected != null) { LINKS.splice(selected, 1); selectLink(null); drawLinks(); cache(true); toast('Arrow removed'); }
  if (e.key === 'c' || e.key === 'C') setConnect(!connect);
});
addEventListener('resize', () => { sizeCanvas(); if (focused != null) focus(focused); else fitAll(false); });
sizeCanvas();
$('#fc-rail-toggle').addEventListener('click', () => { $('#fc-rail').classList.toggle('is-on'); $('#fc-rail-toggle').classList.toggle('is-on'); });
$('#fc-rail').addEventListener('click', e => {
  const rm = e.target.closest('[data-rm]'); if (rm) { LINKS.splice(+rm.dataset.rm, 1); selectLink(null); cache(true); toast('Arrow removed'); return; }
  const sel = e.target.closest('[data-sel]'); if (sel) { const L = LINKS[+sel.dataset.sel]; const a = bySig()[L.from.sig]; if (a) fitRect(a.x - W * .4, a.y - H * .3, W * 2, H * 1.6, 24, true); selectLink(+sel.dataset.sel); }
});
$('#fc-refresh').addEventListener('click', async () => { unfocus(); if (await crawl()) await repaint(true); });
$('#fc-repaint').addEventListener('click', async () => { unfocus(); await repaint(true); });
$('#fc-save').addEventListener('click', () => writeAll());

/* ============================ Focus (use a screen live, in place) ============================ */
function focus(id) {
  id = +id; const s = STATES[id]; if (!s) return; if (focused != null && focused !== id) unfocus(false); focused = id;
  const el = $('#fc-f-' + id); el.classList.add('is-focus'); if (el.dataset.live !== '1') showLive(s);
  document.querySelectorAll('.fc-use').forEach(b => { const on = +b.dataset.focus === id; b.classList.toggle('is-on', on); b.textContent = on ? '✓ Using · click to stop' : 'Use'; });
  fitRect(s.x, s.y - 70, W, SH + 70, 24, true); $('#fc-focus-name').textContent = `${id} · ${s.name}`; $('#fc-focus').classList.add('is-on');
}
function unfocus(zoomOut) {
  if (focused == null) return; const s = STATES[focused]; focused = null;
  const el = $('#fc-f-' + s.id); el.classList.remove('is-focus'); showImage(s);            // back to the image (or live if there is none)
  const b = el.querySelector('.fc-use'); if (b) { b.classList.remove('is-on'); b.textContent = 'Use'; }
  $('#fc-focus').classList.remove('is-on'); if (zoomOut) fitRect(s.x - W * .6, s.y - SH * .3, W * 2.2, SH * 1.6, 24, true);
}
$('#fc-focus-exit').addEventListener('click', () => unfocus(true));
$('#fc-focus-reset').addEventListener('click', () => { if (focused != null) showLive(STATES[focused]); });

/* ============================ Hand-drawn arrows ============================ */
// A link is { from: { sig, fx, fy }, to: { sig, fx, fy }, label }: fractions of the screen image,
// anchored to the screen's fingerprint so a re-map keeps the arrows on the right screens.
let connect = false, drag = null, selected = null;
const bySig = () => Object.fromEntries(STATES.map(s => [s.sig, s]));
const pt = (s, f) => ({ x: s.x + f.fx * W, y: s.y + f.fy * SH });
function frameAt(e) { const el = document.elementFromPoint(e.clientX, e.clientY); const f = el && el.closest('.fc-frame'); if (!f) return null; const s = STATES[+f.id.replace('fc-f-', '')]; const w = toWorld(e.clientX, e.clientY); const fx = (w.x - s.x) / W, fy = (w.y - s.y) / SH; if (fy < 0) return null; return { s, fx: Math.min(1, Math.max(0, fx)), fy: Math.min(1, Math.max(0, fy)) }; }
function setConnect(on) { connect = on; $('#fc-connect').classList.toggle('is-on', on); vp.classList.toggle('is-connect', on); $('#fc-hint').textContent = on ? 'Drag from the spot you click on one screen to the screen it opens · click an arrow to select it · Esc to stop' : 'Drag to pan · ⌘+scroll or pinch to zoom · double-click a screen to zoom to it · Use to click through it live'; if (!on) { drag = null; drawLinks(); } }
$('#fc-connect').addEventListener('click', () => setConnect(!connect));
function startConnect(e) {
  const hit = e.target.closest('.fc-links .hd'); if (hit) { drag = { move: +hit.dataset.link, end: hit.dataset.end }; vp.setPointerCapture(e.pointerId); return; }
  if (e.target.closest('.fc-links [class]')) return;
  const a = frameAt(e); if (!a) { if (selected != null) selectLink(null); return; } drag = { from: a, cur: toWorld(e.clientX, e.clientY) }; vp.setPointerCapture(e.pointerId); drawLinks();
}
function moveConnect(e) {
  if (drag.move != null) { const t = frameAt(e); if (t) { LINKS[drag.move][drag.end] = { sig: t.s.sig, fx: t.fx, fy: t.fy }; drawLinks(); } return; }
  drag.cur = toWorld(e.clientX, e.clientY); const t = frameAt(e); document.querySelectorAll('.fc-frame.is-target').forEach(f => f.classList.remove('is-target')); if (t && t.s !== drag.from.s) $('#fc-f-' + t.s.id).classList.add('is-target'); drawLinks();
}
function endConnect(e) {
  document.querySelectorAll('.fc-frame.is-target').forEach(f => f.classList.remove('is-target'));
  if (drag.move != null) { drag = null; cache(true); drawLinks(); return; }
  const t = frameAt(e); const from = drag.from; drag = null;
  if (!t || t.s === from.s) { drawLinks(); return; }
  LINKS.push({ id: 'ln' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6), from: { sig: from.s.sig, fx: from.fx, fy: from.fy }, to: { sig: t.s.sig, fx: t.fx, fy: t.fy }, label: '', author: store.author() || undefined, created: new Date().toISOString() });
  cache(true); drawLinks(); selectLink(LINKS.length - 1); editLabel(LINKS.length - 1);
}
function selectLink(i) { selected = i; drawLinks(); if (i != null) $('#fc-hint').textContent = 'Arrow selected · Delete or ⌫ removes it · drag its ends to move it · double-click to label it'; else if (!connect) $('#fc-hint').textContent = 'Drag to pan · ⌘+scroll or pinch to zoom · double-click a screen to zoom to it · Use to click through it live'; }
function editLabel(i) {
  const L = LINKS[i]; const S = bySig(); const a = S[L.from.sig], b = S[L.to.sig]; if (!a || !b) return;
  const p1 = pt(a, L.from), p2 = pt(b, L.to); const r = vp.getBoundingClientRect(); const mx = r.left + tx + (p1.x + p2.x) / 2 * k, my = r.top + ty + (p1.y + p2.y) / 2 * k;
  const ed = $('#fc-label-edit'); ed.style.left = Math.min(innerWidth - 340, Math.max(8, mx - 160)) + 'px'; ed.style.top = Math.min(innerHeight - 60, Math.max(56, my + 14)) + 'px'; ed.classList.add('is-on'); ed.dataset.link = i;
  const inp = $('#fc-label-input'); inp.value = L.label || ''; inp.focus(); inp.select();
}
const closeLabel = save => { const ed = $('#fc-label-edit'); if (!ed.classList.contains('is-on')) return; if (save && LINKS[+ed.dataset.link]) { LINKS[+ed.dataset.link].label = $('#fc-label-input').value.trim(); cache(true); drawLinks(); } ed.classList.remove('is-on'); };
$('#fc-label-ok').addEventListener('click', () => closeLabel(true));
$('#fc-label-input').addEventListener('keydown', e => { if (e.key === 'Enter') closeLabel(true); if (e.key === 'Escape') closeLabel(false); e.stopPropagation(); });
function drawLinks() {
  const svg = $('#fc-links'); svg.setAttribute('width', bounds.x + bounds.w); svg.setAttribute('height', bounds.y + bounds.h); svg.innerHTML = '';
  const ns = 'http://www.w3.org/2000/svg'; const mk = (t, a) => { const e = document.createElementNS(ns, t); Object.entries(a).forEach(([k2, v]) => e.setAttribute(k2, v)); return e; };
  const S = bySig();
  const curve = (p1, p2) => { const dx = Math.max(160, Math.abs(p2.x - p1.x) / 2); return `M${p1.x},${p1.y} C${p1.x + dx},${p1.y} ${p2.x - dx},${p2.y} ${p2.x},${p2.y}`; };
  const fixed = (x, y, cls) => mk('g', { class: 'fc-fixed ' + cls, style: `--x:${x}px;--y:${y}px` });
  LINKS.forEach((L, i) => {
    const a = S[L.from.sig], b = S[L.to.sig]; if (!a || !b) return;      // orphan (screen gone after a re-map): kept in the file, not drawn
    const p1 = pt(a, L.from), p2 = pt(b, L.to); const sel = selected === i; const g = mk('g', { class: sel ? 'is-selected' : '' });
    g.appendChild(mk('path', { d: curve(p1, p2), class: 'hit', 'data-link': i }));
    g.appendChild(mk('path', { d: curve(p1, p2), class: 'ln' + (sel ? ' is-selected' : ''), 'data-link': i }));
    const d1 = fixed(p1.x, p1.y, 'dotg'); d1.appendChild(mk('circle', { r: 7, class: 'dot' })); g.appendChild(d1);
    const tmp = mk('path', { d: curve(p1, p2) }); svg.appendChild(tmp); const len = tmp.getTotalLength(); const end = tmp.getPointAtLength(len), pre = tmp.getPointAtLength(Math.max(0, len - 20)); const mid = tmp.getPointAtLength(len / 2); tmp.remove();
    const ang = Math.atan2(end.y - pre.y, end.x - pre.x) * 180 / Math.PI; const hg = fixed(end.x, end.y, 'headg'); hg.appendChild(mk('path', { d: 'M-18,-9 L0,0 L-18,9 Z', class: 'head', transform: `rotate(${ang})` })); g.appendChild(hg);
    const tw = (L.label || 'Add a label').length * 7.2 + 20;
    if (L.label || sel) { const lg = fixed(mid.x, mid.y, 'fc-label'); lg.appendChild(mk('rect', { x: -tw / 2, y: -13, width: tw, height: 26, class: 'lbl-bg', 'data-edit': i })); const t = mk('text', { x: 0, y: 5, 'text-anchor': 'middle', class: 'lbl' }); t.textContent = L.label || 'Add a label'; lg.appendChild(t);
      if (sel) { const del = mk('g', { class: 'del', 'data-del': i, transform: `translate(${tw / 2 + 18},0)` }); del.appendChild(mk('circle', { r: 11 })); del.appendChild(mk('path', { d: 'M-4,-4 L4,4 M4,-4 L-4,4' })); lg.appendChild(del); }
      g.appendChild(lg); }
    if (sel) [['from', p1], ['to', p2]].forEach(([end2, p]) => { const h = fixed(p.x, p.y, 'hdg'); h.appendChild(mk('circle', { r: 11, class: 'hd', 'data-link': i, 'data-end': end2 })); g.appendChild(h); });
    svg.appendChild(g);
  });
  if (drag && drag.from) { const p1 = pt(drag.from.s, drag.from); svg.appendChild(mk('path', { d: curve(p1, drag.cur), class: 'ln is-temp' })); const d1 = fixed(p1.x, p1.y, 'dotg'); d1.appendChild(mk('circle', { r: 7, class: 'dot' })); svg.appendChild(d1); }
}
$('#fc-links').addEventListener('click', e => {
  const del = e.target.closest('[data-del]'); if (del) { LINKS.splice(+del.dataset.del, 1); selectLink(null); cache(true); toast('Arrow removed'); return; }
  const ed = e.target.closest('[data-edit]'); if (ed) { editLabel(+ed.dataset.edit); return; }
  const ln = e.target.closest('[data-link]'); if (ln) selectLink(+ln.dataset.link);
});
$('#fc-links').addEventListener('dblclick', e => { const ln = e.target.closest('[data-link]'); if (ln) editLabel(+ln.dataset.link); });

/* ============================ Minimap ============================ */
function drawMini() {
  const svg = $('#fc-mini-svg'); svg.setAttribute('viewBox', `${bounds.x} ${bounds.y} ${bounds.w} ${bounds.h}`); svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
  svg.innerHTML = STATES.map(s => `<rect class="f${s.depth === 0 ? ' is-start' : ''}" x="${s.x}" y="${s.y}" width="${W}" height="${SH}" rx="40"/>`).join('') + `<rect class="v" id="fc-mini-view"/>`;
  miniView();
}
function miniView() { const v = $('#fc-mini-view'); if (!v) return; v.setAttribute('x', -tx / k); v.setAttribute('y', -ty / k); v.setAttribute('width', vp.clientWidth / k); v.setAttribute('height', vp.clientHeight / k); }
$('#fc-mini').addEventListener('click', e => { const r = $('#fc-mini-svg').getBoundingClientRect(); const sc = Math.max(bounds.w / r.width, bounds.h / r.height); const ox = (r.width - bounds.w / sc) / 2, oy = (r.height - bounds.h / sc) / 2; const wx = bounds.x + (e.clientX - r.left - ox) * sc, wy = bounds.y + (e.clientY - r.top - oy) * sc; tx = vp.clientWidth / 2 - wx * k; ty = vp.clientHeight / 2 - wy * k; apply(true); });

/* ============================ Boot: map.json, else the browser cache, else crawl ============================ */
function useMap(m, how) { STATES = m.states; MAP_WHEN = m.when || null; $('#fc-subtitle').textContent = `${P} · ${STATES.length} screens · ${how}${m.when ? ' ' + new Date(m.when).toLocaleDateString() : ''}`; build(); }
window.FLOW = { get STATES() { return STATES; }, get LINKS() { return LINKS; }, get camera() { return { k, tx, ty }; }, focus: id => focus(id), zoomTo: id => { const s = STATES[id]; if (s) fitRect(s.x, s.y - 70, W, SH + 70, 24, true); }, mapJSON, crawl, repaint, setConnect, writeAll };
(async () => {
  if (!P || location.protocol === 'file:') return;
  await getDir(false);
  if (!q.get('fresh')) {
    let m = null; try { const r = await fetch('map.json', { cache: 'no-store' }); if (r.ok) m = await r.json(); } catch (_) {}
    let c = null; try { c = JSON.parse(localStorage.getItem(CACHE_KEY) || 'null'); } catch (_) {}
    if (m && m.states && m.states.length) useMap(m, 'mapped');
    else if (c && c.states && c.states.length) useMap(c, 'mapped in this browser');
    else if (await crawl()) await repaint(false);
  } else if (await crawl()) await repaint(false);
  await store.load(); store.poll();
})();
})();
