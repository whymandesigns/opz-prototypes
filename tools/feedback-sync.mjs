// feedback-sync.mjs — move review-bar feedback between the database and the repo.
//
//   DATABASE_URL=... node tools/feedback-sync.mjs push [prototype|all]   repo -> database
//   DATABASE_URL=... node tools/feedback-sync.mjs pull [prototype|all]   database -> repo
//
// `push` is the one-off migration of prototypes that already have a local
// feedback.json (written by the dev server) into the shared database.
//
// `pull` is the archive step: once a prototype is approved and the review is
// over, write its comments back to feedback.json next to index.html and commit
// them. The long-term record then lives in git, in a plain format no vendor
// owns — so the database is only ever the live working copy.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import pg from 'pg';
import { read, applyOps } from '../lib/feedback-db.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const [cmd, which = 'all'] = process.argv.slice(2);
if (!['push', 'pull'].includes(cmd)) {
  console.error('Usage: feedback-sync.mjs <push|pull> [prototype|all]');
  process.exit(1);
}
if (!process.env.DATABASE_URL) { console.error('DATABASE_URL is not set'); process.exit(1); }

const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });
const query = (text, params) => pool.query(text, params);

const dirs = which === 'all'
  ? (await fs.readdir(ROOT, { withFileTypes: true }))
      .filter(d => d.isDirectory() && !d.name.startsWith('.') && !d.name.startsWith('_') &&
                   !['api', 'lib', 'tools', 'db', 'node_modules', 'archive'].includes(d.name))
      .map(d => d.name)
  : [which.replace(/^\/|\/$/g, '')];

let touched = 0;
for (const name of dirs) {
  const file = path.join(ROOT, name, 'feedback.json');
  const proto = `/${name}/`;

  if (cmd === 'push') {
    let doc; try { doc = JSON.parse(await fs.readFile(file, 'utf8')); } catch { continue; }
    const ops = [
      ...(doc.comments || []).map(c => ({ t: 'comment', c })),
      ...Object.entries(doc.edits || {}).map(([k, v]) => ({ t: 'edit', k, v })),
    ];
    if (!ops.length) { console.log(`${name}: nothing to push`); continue; }
    await applyOps(query, proto, ops);
    console.log(`${name}: pushed ${doc.comments?.length || 0} comment(s), ${Object.keys(doc.edits || {}).length} edit(s)`);
    touched++;
  } else {
    const doc = await read(query, proto);
    if (!doc.comments.length && !Object.keys(doc.edits).length) continue;
    // Keep any keys the review bar doesn't own (e.g. version history).
    let existing = {}; try { existing = JSON.parse(await fs.readFile(file, 'utf8')); } catch {}
    await fs.writeFile(file, JSON.stringify({ ...existing, ...doc }, null, 2) + '\n');
    console.log(`${name}: archived ${doc.comments.length} comment(s) -> ${path.relative(ROOT, file)}`);
    touched++;
  }
}
await pool.end();
console.log(touched ? `\n${cmd} complete (${touched} prototype${touched > 1 ? 's' : ''})` : '\nnothing to do');
