#!/usr/bin/env node
// flow-shots.mjs — render every screen of a prototype's flow map to shots/<n>.png
// with headless Chrome, without clicking anything in the canvas.
//
//   node lib/flow-shots.mjs /action-trace/            (dev server on http://localhost:5733)
//   node lib/flow-shots.mjs /action-trace/ --base=http://localhost:5733 --only=3,7
//
// Reads <proto>/flow/map.json (made by the canvas), opens <proto>/flow/?shot=N for
// each screen — the canvas page in "shot" mode: the prototype live, with the
// screen's clicks replayed — and screenshots it at 1440×900. Then marks each
// screen's `shot` in map.json. Commit shots/ and map.json together.
import { readFileSync, writeFileSync, mkdirSync, existsSync, mkdtempSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { join, resolve } from 'node:path';
import { tmpdir } from 'node:os';

const args = process.argv.slice(2);
const proto = args.find(a => !a.startsWith('--'));
if (!proto) { console.error('usage: node lib/flow-shots.mjs /<prototype>/ [--base=http://localhost:5733] [--only=1,2]'); process.exit(1); }
const opt = Object.fromEntries(args.filter(a => a.startsWith('--')).map(a => { const [k, v = true] = a.slice(2).split('='); return [k, v]; }));
const base = (opt.base || 'http://localhost:5733').replace(/\/$/, '');
const p = proto.endsWith('/') ? proto : proto + '/';
const dir = resolve(process.cwd(), '.' + p + 'flow');
const mapFile = join(dir, 'map.json');
if (!existsSync(mapFile)) { console.error(`no map yet: ${mapFile} — open ${base}${p}flow/ once so the canvas maps the prototype, then Save to the flow folder`); process.exit(1); }
const map = JSON.parse(readFileSync(mapFile, 'utf8'));
const only = opt.only ? String(opt.only).split(',').map(Number) : null;
const chrome = process.env.CHROME || ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/chromium'].find(existsSync);
if (!chrome) { console.error('Chrome not found; set CHROME=/path/to/chrome'); process.exit(1); }
mkdirSync(join(dir, 'shots'), { recursive: true });
const profile = mkdtempSync(join(tmpdir(), 'flow-shots-'));
let n = 0;
for (const s of map.states) {
  if (only && !only.includes(s.id)) continue;
  const out = join(dir, 'shots', `${s.id}.png`);
  const url = `${base}${p}flow/?shot=${s.id}`;
  process.stdout.write(`${s.id}: ${s.name} … `);
  try {
    execFileSync(chrome, ['--headless=new', '--disable-gpu', '--hide-scrollbars', `--user-data-dir=${profile}`, '--window-size=1440,900', '--virtual-time-budget=10000', `--screenshot=${out}`, url], { stdio: ['ignore', 'ignore', 'ignore'], timeout: 60000 });
    s.shot = `shots/${s.id}.png`; n++; console.log('ok');
  } catch (e) { console.log('failed: ' + e.message); }
}
// `when` is left alone: it marks the last map/arrow write, and bumping it here would make the canvas drop arrows drawn since.
writeFileSync(mapFile, JSON.stringify(map, null, 1) + '\n');
console.log(`${n} screen${n === 1 ? '' : 's'} rendered → ${join(dir, 'shots')}; map.json updated`);
