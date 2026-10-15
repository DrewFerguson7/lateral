// Local preview: serves the built site plus the ranking API with in-memory storage, seeded with fake players.
// node tools/devserver.mjs <site folder> <fake players> [port]
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
import { handle } from '../netlify/functions/rank.mjs';
const [root = 'site', seed = 0, port = 8770] = process.argv.slice(2), mem = new Map();
const store = { list: async ({ prefix }) => ({ blobs: [...mem.keys()].filter(k => k.startsWith(prefix)).map(key => ({ key })) }), set: async (k, v) => mem.set(k, v) };
const day = new Date().toLocaleDateString('en-CA');
let r = 7; const rnd = () => (r = (r * 16807) % 2147483647) / 2147483647;
for (let i = 0; i < +seed; i++) for (const m of ['n', 'h']) mem.set(`${day}/${m}/seed${m}${String(i).padStart(5, '0')}/${Math.round(1000 * (20 + 18 * (rnd() + rnd() + rnd() + rnd())))}`, '');
http.createServer(async (req, res) => {
  if (req.url.startsWith('/api/rank')) { const body = await new Promise(ok => { let d = ''; req.on('data', c => d += c); req.on('end', () => ok(d)) });
    const out = await handle(new Request('http://x' + req.url, { method: req.method, body: req.method == 'POST' ? body : undefined }), store);
    res.writeHead(out.status, { 'content-type': 'application/json' }); return res.end(await out.text()) }
  const f = path.join(root, req.url == '/' ? 'index.html' : req.url.split('?')[0]);
  fs.readFile(f, (e, d) => { if (e) { res.writeHead(404); return res.end() } res.writeHead(200, { 'content-type': f.endsWith('.html') ? 'text/html' : 'image/png' }); res.end(d) });
}).listen(+port, '127.0.0.1');
