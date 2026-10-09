// Local test of the ranking function with an in-memory stand-in for Netlify Blobs.
import { handle } from '../netlify/functions/rank.mjs';
const mem = new Map(), store = { list: async ({ prefix }) => ({ blobs: [...mem.keys()].filter(k => k.startsWith(prefix)).map(key => ({ key })) }), set: async (k, v) => mem.set(k, v) };
const now = Date.parse('2026-10-09T19:00:00Z'), call = async b => (await handle(new Request('http://x', { method: 'POST', body: JSON.stringify(b) }), store, now)).json();
const ok = (c, m) => { if (!c) { console.log('FAIL', m); process.exitCode = 1 } else console.log('ok  ', m) };
for (let i = 0; i < 20; i++) await call({ day: '2026-10-09', hard: 0, ms: 20000 + i * 5000, id: 'dev' + String(i).padStart(6, '0') });
let r = await call({ day: '2026-10-09', hard: 0, ms: 42000, id: 'me12345678' });
ok(r.n == 21 && r.pct == 75, `21 players, 42s beats 15 of 20 others -> ${r.pct}%`);
r = await call({ day: '2026-10-09', hard: 0, ms: 5000, id: 'me12345678' });
ok(r.n == 21 && r.you == 42000 && r.pct == 75, 'replay does not count or change your time');
r = await call({ day: '2026-10-09', hard: 1, ms: 30000, id: 'me12345678' });
ok(r.n == 1 && r.pct === null, 'hard mode ranked separately; first finisher has no percent');
ok((await call({ day: '2026-10-01', hard: 0, ms: 30000, id: 'me12345678' })).error == 'bad day', 'old day rejected');
ok((await call({ day: '2026-10-09', hard: 0, ms: 900, id: 'x2345678' })).error == 'bad time', 'impossible time rejected');
ok((await call({ day: '2026-10-09', hard: 0, ms: 9000, id: 'bad id!' })).error == 'bad id', 'bad id rejected');
ok((await call({ day: '2026-10-10', hard: 0, ms: 9000, id: 'tokyo1234' })).n == 1, 'tomorrow (ahead time zones) accepted');
