// /api/feedback — the review bar's shared store, on Neon Postgres.
//
// Same contract as the local file store (designmd/tools/serve.mjs), so review.js
// does not know or care which one it is talking to:
//   GET  /api/feedback?p=/action-trace/   -> { edits, comments, updated }
//   POST /api/feedback  { p, ops }        -> the merged document
// Ops are documented in lib/feedback-db.mjs.
//
// Setup (once):
//   1. Vercel -> this project -> Storage -> Create Database -> Neon Postgres.
//      That injects DATABASE_URL.
//   2. psql "$DATABASE_URL" -f db/schema.sql
//   3. Redeploy. The bar switches from "Local only" to "Shared".
// Until DATABASE_URL exists this answers 503 and the bar keeps working locally,
// queueing its changes until the store appears.
//
// Writes can be gated with REVIEW_TOKEN: set it in the Vercel project and the
// bar will ask reviewers for it once. Reads stay open. Leave it unset to allow
// anyone with the link to comment.
import { neon } from '@neondatabase/serverless';
import { read, applyOps, cleanPath } from '../lib/feedback-db.mjs';

const sql = process.env.DATABASE_URL ? neon(process.env.DATABASE_URL) : null;
// lib/feedback-db.mjs speaks (text, params) => { rows }; Neon's http driver
// takes the same shape through sql.query().
const query = async (text, params) => ({ rows: await sql.query(text, params) });

// Exported as a factory so the tests can drive it against a throwaway database.
export function createHandler(q) {
  return async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (!q) return res.status(503).json({ error: 'Store not configured: add a Neon database to this Vercel project (DATABASE_URL).' });
  try {
    const body = req.method === 'POST' ? (typeof req.body === 'string' ? JSON.parse(req.body || '{}') : req.body || {}) : {};
    const p = cleanPath(req.method === 'POST' ? body.p : req.query?.p);
    if (!p) return res.status(400).json({ error: 'bad prototype path' });

    if (req.method === 'GET') return res.status(200).json(await read(q, p));

    if (req.method === 'POST') {
      const want = process.env.REVIEW_TOKEN;
      if (want && req.headers['x-review-token'] !== want) return res.status(401).json({ error: 'bad or missing review token' });
      if (JSON.stringify(body).length > 200000) return res.status(413).json({ error: 'too large' });
      return res.status(200).json(await applyOps(q, p, body.ops));
    }
    res.status(405).end();
  } catch (e) {
    console.error('feedback', e);
    res.status(500).json({ error: String(e?.message || e) });
  }
  };
}

export default createHandler(sql ? query : null);
