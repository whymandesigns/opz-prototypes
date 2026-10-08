// feedback-api.test.mjs — drives the serverless handler against a real database.
//   DATABASE_URL=postgres://... node tools/feedback-api.test.mjs
import pg from 'pg';
import { createHandler } from '../api/feedback.js';

const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });
const query = (text, params) => pool.query(text, params);
let failed = 0;
const ok = (name, cond) => { console.log(`${cond ? '  ok  ' : ' FAIL '} ${name}`); if (!cond) failed++; };

// minimal res double
const mkRes = () => { const r = { code: 0, body: null, headers: {} };
  r.setHeader = (k, v) => { r.headers[k] = v; };
  r.status = c => { r.code = c; return r; };
  r.json = b => { r.body = b; return r; };
  r.end = () => r; return r; };
const call = async (h, req) => { const res = mkRes(); await h(req, res); return res; };

const P = '/api-test/';
await query('delete from comments where prototype = $1', [P]);
await query('delete from counters where prototype = $1', [P]);

const h = createHandler(query);

// unconfigured store
const none = await call(createHandler(null), { method: 'GET', query: { p: P } });
ok('503 when no database configured', none.code === 503);

// bad paths
ok('400 on traversal', (await call(h, { method: 'GET', query: { p: '/../etc' } })).code === 400);
ok('405 on unsupported method', (await call(h, { method: 'DELETE', query: { p: P } })).code === 405);

// write + read
const post = await call(h, { method: 'POST', body: { p: P, ops: [{ t: 'comment', c: { id: 'a1', text: 'Hello' } }] } });
ok('POST stores and returns the document', post.code === 200 && post.body.comments[0].text === 'Hello');
const get = await call(h, { method: 'GET', query: { p: P } });
ok('GET returns the same document', get.code === 200 && get.body.comments.length === 1);
ok('no-store header set', get.headers['Cache-Control'] === 'no-store');

// body as a JSON string (some runtimes do not parse it)
const raw = await call(h, { method: 'POST', body: JSON.stringify({ p: P, ops: [{ t: 'comment', c: { id: 'a2', text: 'Raw' } }] }) });
ok('POST accepts a raw JSON string body', raw.code === 200 && raw.body.comments.length === 2);

// oversized payload
const big = await call(h, { method: 'POST', body: { p: P, ops: [{ t: 'comment', c: { id: 'big', text: 'x'.repeat(300000) } }] } });
ok('413 on oversized payload', big.code === 413);

// token gate
process.env.REVIEW_TOKEN = 'secret';
ok('401 without the token', (await call(h, { method: 'POST', body: { p: P, ops: [] }, headers: {} })).code === 401);
ok('401 with a wrong token', (await call(h, { method: 'POST', body: { p: P, ops: [] }, headers: { 'x-review-token': 'nope' } })).code === 401);
ok('200 with the right token', (await call(h, { method: 'POST', body: { p: P, ops: [] }, headers: { 'x-review-token': 'secret' } })).code === 200);
ok('reads stay open when a token is set', (await call(h, { method: 'GET', query: { p: P }, headers: {} })).code === 200);
delete process.env.REVIEW_TOKEN;

await query('delete from comments where prototype = $1', [P]);
await query('delete from counters where prototype = $1', [P]);
await pool.end();
console.log(failed ? `\n${failed} failing` : '\nall passing');
process.exit(failed ? 1 : 0);
