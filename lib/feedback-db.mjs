// feedback-db.mjs — the review bar's store, backed by Postgres (Neon).
//
// Same wire contract as the file-based local store (designmd/tools/serve.mjs):
//   read(query, path)        -> { edits, comments, updated }
//   applyOps(query, path, ops)
// so review.js never knows which one it is talking to.
//
// Why rows and not one JSON document per prototype: every op writes a single
// row, so two reviewers posting at the same moment cannot clobber each other.
// The blob store had to read-modify-write the whole document, which silently
// lost updates under concurrency.
//
// Ops (unchanged, see designmd/tools/feedback-store.mjs):
//   { t:'comment', c }   upsert a comment by id (n is assigned here when missing)
//   { t:'del', id }      soft-delete a comment (kept for the record)
//   { t:'edit', k, v }   set (v) or clear (v null) one text edit
//   { t:'edits:clear' }  clear every text edit for the prototype
//
// `query` is (text, params) => Promise<{ rows }> — Neon in production, node-postgres in tests.

export const EMPTY = () => ({ edits: {}, comments: [] });

// A prototype is addressed by its URL path: "/action-trace/". Reject anything odd.
export const cleanPath = p => {
  p = String(p || '').replace(/index\.html$/, '');
  if (!p.startsWith('/') || p.includes('..') || p.length > 200) return null;
  return p.endsWith('/') ? p : p + '/';
};

const rowToComment = r => ({
  id: r.id, n: r.n, path: r.path, el: r.el, html: r.html,
  screenId: r.screen_id, screen: r.screen, url: r.url,
  rect: r.rect || undefined,
  text: r.body, author: r.author || undefined,
  resolved: r.resolved, resolution: r.resolution || undefined,
  created: r.created_at instanceof Date ? r.created_at.toISOString() : r.created_at,
});

export async function read(query, prototype) {
  const [c, e] = await Promise.all([
    query(`select * from comments where prototype = $1 and deleted_at is null order by n`, [prototype]),
    query(`select key, orig, text, screen, author from edits where prototype = $1`, [prototype]),
  ]);
  const edits = {};
  for (const r of e.rows) edits[r.key] = { orig: r.orig, text: r.text, screen: r.screen || undefined, author: r.author || undefined };
  const stamps = [...c.rows.map(r => r.updated_at), ...e.rows.map(r => r.updated_at)].filter(Boolean);
  const updated = stamps.length ? new Date(Math.max(...stamps.map(d => +new Date(d)))).toISOString() : undefined;
  return { edits, comments: c.rows.map(rowToComment), updated };
}

async function upsertComment(query, prototype, c) {
  if (typeof c?.id !== 'string') return;
  const body = typeof c.text === 'string' ? c.text.slice(0, 5000) : '';
  // Update first. If the comment already exists this touches exactly one row and
  // no number is allocated — so resolving/reopening never burns a display number.
  const upd = await query(
    `update comments set
       path = coalesce($3, path), el = coalesce($4, el), html = coalesce($5, html),
       screen_id = coalesce($6, screen_id), screen = coalesce($7, screen), url = coalesce($8, url),
       rect = coalesce($9::jsonb, rect), body = $10, author = coalesce($11, author),
       resolved = coalesce($12, false), resolution = $13, updated_at = now(), deleted_at = null
     where id = $1 and prototype = $2`,
    [c.id, prototype, c.path ?? null, c.el ?? null, c.html ?? null, c.screenId ?? null,
     c.screen ?? null, c.url ?? null, c.rect ? JSON.stringify(c.rect) : null,
     body, c.author ?? null, c.resolved ?? false, c.resolution ?? null]);
  if (upd.rowCount > 0) return;

  // New comment: take the next number from the counter. One statement, so
  // concurrent posts are serialised by the row lock rather than racing.
  const nextN = async () => (await query(
    `insert into counters (prototype, last_n) values ($1, 1)
     on conflict (prototype) do update set last_n = counters.last_n + 1
     returning last_n`, [prototype])).rows[0].last_n;

  let n = c.n;
  if (!n) n = await nextN();
  else    // an imported number (migration): keep the counter ahead of it
    await query(`insert into counters (prototype, last_n) values ($1, $2)
                 on conflict (prototype) do update set last_n = greatest(counters.last_n, excluded.last_n)`,
                [prototype, n]);

  const insert = num => query(
    `insert into comments (id, prototype, n, path, el, html, screen_id, screen, url, rect, body, author, resolved, resolution)
     values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10::jsonb,$11,$12,coalesce($13,false),$14)
     on conflict (id) do nothing`,
    [c.id, prototype, num, c.path ?? null, c.el ?? null, c.html ?? null, c.screenId ?? null,
     c.screen ?? null, c.url ?? null, c.rect ? JSON.stringify(c.rect) : null,
     body, c.author ?? null, c.resolved ?? false, c.resolution ?? null]);

  try { await insert(n); }
  catch (e) {
    // That number is already taken (an import landing on an existing comment),
    // so fall back to a freshly allocated one rather than dropping the comment.
    if (e?.code !== '23505') throw e;
    await insert(await nextN());
  }
}

export async function applyOps(query, prototype, ops) {
  for (const o of Array.isArray(ops) ? ops : []) {
    if (o?.t === 'comment' && o.c) {
      await upsertComment(query, prototype, o.c);
    } else if (o?.t === 'del' && typeof o.id === 'string') {
      // Soft delete — the comment leaves the UI but the record is kept.
      await query(`update comments set deleted_at = now(), updated_at = now() where id = $1 and prototype = $2`, [o.id, prototype]);
    } else if (o?.t === 'edit' && typeof o.k === 'string') {
      if (o.v && typeof o.v === 'object') {
        await query(
          `insert into edits (prototype, key, orig, text, screen, author) values ($1,$2,$3,$4,$5,$6)
           on conflict (prototype, key) do update set text = excluded.text, screen = coalesce(excluded.screen, edits.screen),
             author = coalesce(excluded.author, edits.author), updated_at = now()`,
          [prototype, o.k, String(o.v.orig ?? ''), String(o.v.text ?? ''), o.v.screen ?? null, o.v.author ?? null]);
      } else {
        await query(`delete from edits where prototype = $1 and key = $2`, [prototype, o.k]);
      }
    } else if (o?.t === 'edits:clear') {
      await query(`delete from edits where prototype = $1`, [prototype]);
    }
  }
  return read(query, prototype);
}
