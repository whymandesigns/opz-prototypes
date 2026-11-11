// Rewrites the "N prototypes" label on each folder card in the root index.html
// from the real number of cards in that folder's own index.html.
//   node tools/sync-folder-counts.mjs
// (index.html also refreshes these live when served over http, so a deployed
// page cannot drift; this keeps the static text right for file:// and first paint.)
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
const root = new URL('../', import.meta.url).pathname;
let html = readFileSync(root + 'index.html', 'utf8');
let changed = 0;
html = html.replace(/(<a class="card" href="\.\/([^\/"]+)\/(?:index\.html)?"[^>]*>(?:(?!<\/a>)[\s\S])*?<span class="thumb-folder-count">)\d+ prototypes?(<\/span>)/g,
  (m, pre, dir, post) => {
    const f = root + dir + '/index.html';
    if (!existsSync(f)) return m;
    const n = (readFileSync(f, 'utf8').match(/<a class="card"(?![^>]*\bhidden\b)/g) || []).length;
    const next = `${pre}${n} ${n === 1 ? 'prototype' : 'prototypes'}${post}`;
    if (next !== m) changed++;
    return next;
  });
writeFileSync(root + 'index.html', html);
console.log(`folder counts updated: ${changed}`);
