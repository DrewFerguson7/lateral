import pickle, random, glob, pandas as pd
from collections import defaultdict
P, TN = pickle.load(open('P.pkl', 'rb'))
t1, t2, fame = pickle.load(open('fame.pkl', 'rb'))
# famous players get the plain name; lesser namesakes keep the (POS year) tag
from collections import Counter
grp = defaultdict(list)
for k, p in P.items(): grp[p['name']].append(k)
T12 = set(t1) | set(t2)
for n, ks in grp.items():
    if len(ks) > 1:
        top = max(ks, key=lambda k: fame.get(k, 0))
        if top in T12 and all(fame.get(k, 0) * 3 < fame[top] for k in ks if k != top): P[top]['disp'] = n

def conns(k, hard):
    p = P[k]; c = [f'#{n}' for n in p['nums']] + [f'C:{x}' for x in p['cols']]
    return c if hard else c + [f'T:{t}' for t in p['teams']]
idx = {h: defaultdict(set) for h in (0, 1)}
for k in P:
    for h in (0, 1):
        for c in conns(k, h): idx[h][c].add(k)
def reach(k, h):  # player -> {other player: connector}
    out = {}
    for c in conns(k, h):
        for o in idx[h][c]: out.setdefault(o, c)
    return out
def solve(a, b, h):
    if set(conns(a, h)) & set(conns(b, h)): return None, 1  # too easy
    ra, rb = reach(a, h), reach(b, h)
    br = (set(ra) & set(rb)) - {a, b}
    if br:
        x = max(br, key=lambda k: (fame.get(k, 0), P[k]['ns']))
        return [a, ra[x], x, rb[x], b], len(br)
    for x in ra:  # par 3
        rx = reach(x, h)
        for y in set(rx) & set(rb):
            if y not in (a, b, x) and len({ra[x], rx[y], rb[y]}) == 3: return [a, ra[x], x, rx[y], y, rb[y], b], 0
    return None, 9
random.seed(5); used = defaultdict(int)
def build(A, B, cap, need):
    out = []; pairs = [(a, b) for a in A for b in B if a != b]; random.shuffle(pairs); seen = set()
    for a, b in pairs:
        if used[a] >= cap or used[b] >= cap or frozenset((a, b)) in seen: continue
        c, nc = solve(a, b, 0)
        if not c: continue
        hd, nh = solve(a, b, 1)
        if not hd or len(hd) > 7: continue
        if random.random() < .5: c = c[::-1]; hd = hd[::-1]
        out.append((c, hd)); used[a] += 1; used[b] += 1; seen.add(frozenset((a, b)))
        if len(out) >= need: break
    return out
# endpoints: main days use only the 170 most famous; deeper-cut days add recent, well-known names (no linemen, no pre-1998 non-stars)
T1 = t1[:170]
SK = {'QB', 'RB', 'WR', 'TE'}; OLp = {'T', 'G', 'C', 'OL', 'OT', 'OG'}
BLOCK = {'Andre Roberts'}
DP = [k for k in t1[170:] + t2 if P[k]['name'] not in BLOCK and P[k]['pos'] not in OLp and (P[k]['pos'] in SK and P[k]['last'] >= 2002 and fame.get(k, 0) >= 14 or P[k]['last'] >= 2003 and fame.get(k, 0) >= 20)]
print('main pool', len(T1), 'deep pool', len(DP), [P[k]['disp'] for k in DP[:30]])
main = build(T1, T1, 4, 360)
deep = build(DP, T1, 6, 72)
seq = []; mi = di = 0
for i in range(len(main) + len(deep)):
    if i % 6 == 5 and di < len(deep): seq.append(deep[di] + (1,)); di += 1
    elif mi < len(main): seq.append(main[mi] + (0,)); mi += 1
    else: seq.append(deep[di] + (1,)); di += 1
tri = [k for k in T1 if P[k]['nums'] and P[k]['cols'] and P[k]['teams']]; random.shuffle(tri)
print(len(main), 'main', len(deep), 'deep', len(tri), 'trivia')
for c, h, d in seq[:7]: print(d, [P[x]['disp'] if x in P else x for x in c])
print('trivia:', [P[k]['disp'] for k in tri[:10]])
Pm, _ = pickle.load(open('P_main.pkl', 'rb'))  # keep each player's main jersey number
for k, p in P.items():
    m = Pm.get(k, {}).get('main'); p['main'] = m if m in p['nums'] else (p['nums'][0] if p['nums'] else None)
pickle.dump((seq, tri), open('puz.pkl', 'wb')); pickle.dump((P, TN), open('P3.pkl', 'wb'))
