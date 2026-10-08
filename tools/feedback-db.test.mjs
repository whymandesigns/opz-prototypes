// feedback-db.test.mjs — exercises the Postgres store against a real database.
//   DATABASE_URL=postgres://... node tools/feedback-db.test.mjs
import pg from 'pg';
import { read, applyOps, cleanPath } from '../lib/feedback-db.mjs';

const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });
const query = (text, params) => pool.query(text, params);
let failed = 0;
const ok = (name, cond) => { console.log(`${cond ? '  ok  ' : ' FAIL '} ${name}`); if (!cond) failed++; };

const P = '/test-proto/';
const reset = async () => {
  await query('delete from comments where prototype = $1', [P]);
  await query('delete from edits where prototype = $1', [P]);
  await query('delete from counters where prototype = $1', [P]);
};
await reset();

// paths
ok('cleanPath normalises', cleanPath('/a/index.html') === '/a/' && cleanPath('/a') === '/a/');
ok('cleanPath rejects traversal', cleanPath('/../etc') === null && cleanPath('nope') === null);

// comments
await applyOps(query, P, [{ t:'comment', c:{ id:'c1', text:'First', path:'body/0', el:'div', author:'Ann', rect:{x:1,y:2,w:3,h:4} } }]);
let doc = await read(query, P);
ok('comment stored with n=1', doc.comments.length === 1 && doc.comments[0].n === 1 && doc.comments[0].text === 'First');
{ const r = doc.comments[0].rect || {}; ok('rect round-trips', r.x===1 && r.y===2 && r.w===3 && r.h===4); }

// resolve + reopen
await applyOps(query, P, [{ t:'comment', c:{ id:'c1', text:'First', resolved:true, resolution:'Done' } }]);
doc = await read(query, P);
ok('resolve persists', doc.comments[0].resolved === true && doc.comments[0].resolution === 'Done');
ok('author kept on partial update', doc.comments[0].author === 'Ann');

// soft delete
await applyOps(query, P, [{ t:'del', id:'c1' }]);
doc = await read(query, P);
const kept = await query('select deleted_at from comments where id = $1', ['c1']);
ok('delete hides from the document', doc.comments.length === 0);
ok('delete is soft — row retained', kept.rows.length === 1 && kept.rows[0].deleted_at !== null);

// edits
await applyOps(query, P, [{ t:'edit', k:'body/0#0', v:{ orig:'Old', text:'New', author:'Ann' } }]);
doc = await read(query, P);
ok('edit stored', doc.edits['body/0#0']?.text === 'New' && doc.edits['body/0#0']?.orig === 'Old');
await applyOps(query, P, [{ t:'edit', k:'body/0#0', v:null }]);
ok('edit cleared', Object.keys((await read(query, P)).edits).length === 0);
await applyOps(query, P, [{ t:'edit', k:'a#0', v:{orig:'a',text:'b'} }, { t:'edit', k:'b#0', v:{orig:'c',text:'d'} }]);
await applyOps(query, P, [{ t:'edits:clear' }]);
ok('edits:clear empties', Object.keys((await read(query, P)).edits).length === 0);

// the case that broke the blob store: 30 simultaneous posts
await reset();
await Promise.all(Array.from({ length: 30 }, (_, i) =>
  applyOps(query, P, [{ t:'comment', c:{ id:'x' + i, text:'c' + i } }]).catch(() => null)));
doc = await read(query, P);
ok('30 concurrent comments all persisted', doc.comments.length === 30);
const ns = doc.comments.map(c => c.n).sort((a, b) => a - b);
ok('numbering is unique 1..30', JSON.stringify(ns) === JSON.stringify([...Array(30)].map((_, i) => i + 1)));

// numbers are never reused, so a resolve must not consume one
await reset();
await applyOps(query, P, [{ t:'comment', c:{ id:'r1', text:'one' } }]);
await applyOps(query, P, [{ t:'comment', c:{ id:'r1', text:'one', resolved:true } }]);
await applyOps(query, P, [{ t:'comment', c:{ id:'r2', text:'two' } }]);
doc = await read(query, P);
ok('resolve does not burn a number', doc.comments.find(c => c.id === 'r2')?.n === 2);

// an imported comment carries its own number; the next new one must not collide
await reset();
await applyOps(query, P, [{ t:'comment', c:{ id:'i1', n:1, text:'imported' } }]);
await applyOps(query, P, [{ t:'comment', c:{ id:'i2', text:'fresh' } }]);
doc = await read(query, P);
ok('import then new comment does not collide', doc.comments.length === 2);
ok('new comment numbered after the import', doc.comments.find(c => c.id === 'i2')?.n === 2);

// two imports claiming the same number both survive
await reset();
await applyOps(query, P, [{ t:'comment', c:{ id:'j1', n:1, text:'a' } }]);
await applyOps(query, P, [{ t:'comment', c:{ id:'j2', n:1, text:'b' } }]);
doc = await read(query, P);
ok('duplicate imported number is reassigned, nothing dropped', doc.comments.length === 2);

await reset();
await pool.end();
console.log(failed ? `\n${failed} failing` : '\nall passing');
process.exit(failed ? 1 : 0);
