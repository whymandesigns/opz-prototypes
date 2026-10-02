// Static server for the prototype + a tiny API that persists review feedback
// (inline text edits and comments) to feedback.json next to this file.
import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const FEEDBACK = path.join(ROOT, 'feedback.json');
const PORT = Number(process.env.PORT) || 5733;
const TYPES = { '.html':'text/html; charset=utf-8', '.js':'text/javascript', '.mjs':'text/javascript', '.css':'text/css',
  '.json':'application/json', '.svg':'image/svg+xml', '.png':'image/png', '.jpg':'image/jpeg', '.ico':'image/x-icon' };

http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://x');
  try {
    if (url.pathname === '/api/feedback') {
      if (req.method === 'GET') {
        const data = await fs.readFile(FEEDBACK, 'utf8').catch(() => '{"edits":{},"comments":[]}');
        res.writeHead(200, { 'Content-Type':'application/json', 'Cache-Control':'no-store' }); return res.end(data);
      }
      if (req.method === 'POST') {
        let body = ''; for await (const c of req) body += c;
        const parsed = JSON.parse(body); // validate before writing
        await fs.writeFile(FEEDBACK, JSON.stringify(parsed, null, 2) + '\n');
        res.writeHead(200, { 'Content-Type':'application/json' }); return res.end('{"ok":true}');
      }
      res.writeHead(405); return res.end();
    }
    let file = path.normalize(path.join(ROOT, decodeURIComponent(url.pathname)));
    if (!file.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
    if ((await fs.stat(file).catch(() => null))?.isDirectory()) file = path.join(file, 'index.html');
    const data = await fs.readFile(file);
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream', 'Cache-Control':'no-store' });
    res.end(data);
  } catch (e) {
    res.writeHead(e.code === 'ENOENT' ? 404 : 500); res.end(String(e.message));
  }
}).listen(PORT, () => console.log(`Action Trace prototype on http://localhost:${PORT}`));
