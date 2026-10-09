// POST /api/rank  {day:"2026-10-09", hard:0|1, ms:41000, id:"device id"}
// Saves one finish time per device per daily puzzle, then returns how it ranks against everyone else.
import { getStore } from '@netlify/blobs';

const json = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });

export async function handle(req, store, now = Date.now()) {
  if (req.method !== 'POST') return json({ error: 'POST only' }, 405);
  let b; try { b = await req.json() } catch { return json({ error: 'bad json' }, 400) }
  const { day, hard, ms, id } = b || {};
  const d = Date.parse(day + 'T12:00:00Z');
  if (!/^\d{4}-\d\d-\d\d$/.test(day || '') || !(Math.abs(d - now) < 2 * 864e5)) return json({ error: 'bad day' }, 400);   // only today's puzzle (any time zone)
  if (!/^[a-z0-9]{8,32}$/.test(id || '')) return json({ error: 'bad id' }, 400);
  const t = Math.round(+ms);
  if (!(t >= 3000 && t <= 3 * 3600e3)) return json({ error: 'bad time' }, 400);                  // under 3 seconds isn't humanly possible
  const pre = `${day}/${hard ? 'h' : 'n'}/`;
  const mine = await store.list({ prefix: pre + id + '/' });
  if (!mine.blobs.length) await store.set(`${pre}${id}/${t}`, '');                                // first finish only; replays don't count
  const { blobs } = await store.list({ prefix: pre });
  const times = blobs.map(x => +x.key.split('/').pop()).filter(Number.isFinite).sort((a, c) => a - c);
  const you = mine.blobs.length ? +mine.blobs[0].key.split('/').pop() : t;
  const others = times.length - 1, slower = times.filter(x => x > you).length;
  return json({ n: times.length, you, pct: others > 0 ? Math.round(100 * slower / others) : null,
    secs: times.length > 4000 ? times.filter((_, i) => i % Math.ceil(times.length / 4000) == 0).map(x => Math.round(x / 1000)) : times.map(x => Math.round(x / 1000)) });
}

export default req => handle(req, getStore({ name: 'times', consistency: 'strong' }));
export const config = { path: '/api/rank' };
