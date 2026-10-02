// Emits one line per comment that becomes "queued" in feedback.json (used by the Claude Code session to auto-apply).
import fs from 'node:fs';
const F = new URL('./feedback.json', import.meta.url);
const seen = new Map();
setInterval(() => {
  let fb; try { fb = JSON.parse(fs.readFileSync(F, 'utf8')); } catch { return; }
  for (const c of fb.comments || []) {
    const key = c.requeuedAt || c.created;
    if (c.status === 'queued' && seen.get(c.id) !== key) { seen.set(c.id, key); console.log(`QUEUED #${c.n} ${c.id} [screen ${c.step}] ${c.el} :: ${String(c.text).replace(/\s+/g, ' ').slice(0, 200)}`); }
  }
}, 1000);
