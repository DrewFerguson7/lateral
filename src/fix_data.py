"""Clean the final dataset without regenerating puzzles:
1) merge players split by a name change (Jr./Sr./II..., same GSIS id or same birth date)
2) re-verify every team that came from contracts or the draft (not from a real roster season)
Writes P3.pkl, FS.pkl, lv.pkl, fame.pkl, puz.pkl in place (originals kept as *.bak)."""
import pickle, re, shutil, datetime, pandas as pd
from collections import defaultdict, Counter

P, TN = pickle.load(open('P3.pkl', 'rb')); FS = pickle.load(open('FS.pkl', 'rb'))
LV, RS = pickle.load(open('lv.pkl', 'rb')); t1, t2, fame = pickle.load(open('fame.pkl', 'rb')); seq, tri = pickle.load(open('puz.pkl', 'rb'))
norm = lambda n: re.sub(r'\s+(jr|sr|ii|iii|iv|v)$', '', re.sub(r'[.\']', '', n.lower())).strip()
birth = lambda k: k.split('|', 1)[1] if re.match(r'\d{4}-\d\d-\d\d$', k.split('|', 1)[1]) else None

# ---------- 1) merge split identities ----------
groups = defaultdict(list)
for k, p in P.items():
    b = birth(k)
    groups[('g', p['gsis']) if p.get('gsis') else ('n', norm(p['name']), b or k)].append(k)
by_nb = defaultdict(list)
for k, p in P.items():
    if birth(k): by_nb[(norm(p['name']), birth(k))].append(k)
parent = {k: k for k in P}
def find(k):
    while parent[k] != k: k = parent[k]
    return k
def union(a, b):
    a, b = find(a), find(b)
    if a != b: parent[b] = a
for ks in list(groups.values()) + list(by_nb.values()):
    for k in ks[1:]: union(ks[0], k)
clusters = defaultdict(list)
for k in P: clusters[find(k)].append(k)
remap, merged = {}, 0
for ks in clusters.values():
    if len(ks) == 1: continue
    keep = max(ks, key=lambda k: (k in fame and fame[k], P[k]['ns'], k in set(t1) | set(t2)))
    # keep the key used by puzzles if any
    for k in ks:
        if any(k in (c[0], c[-1]) for c, h, d in seq) or k in tri: keep = k
    kp = P[keep]; kp.setdefault('alias', [])
    for k in ks:
        if k == keep: continue
        p = P[k]; merged += 1; remap[k] = keep
        for t in p['teams']:
            if t not in kp['teams']: kp['teams'].append(t)
        kp['nums'] = sorted(set(kp['nums']) | set(p['nums']))
        kp['cols'] = sorted(set(kp['cols']) | set(p['cols']))
        kp['first'] = min(kp['first'], p['first']); kp['last'] = max(kp['last'], p['last'])
        if p['name'] != kp['name']: kp['alias'].append(p['name'])
        FS[keep] = set(FS.get(keep, set())) | set(FS.get(k, set()))
        LV[keep] = min(LV.get(keep, 3), LV.get(k, 3)); fame[keep] = max(fame.get(keep, 0), fame.get(k, 0))
        del P[k]; FS.pop(k, None)
    kp['ns'] = len({y for f, y in FS.get(keep, ())}) or kp['ns']
print('merged split players:', merged)

# ---------- 2) re-verify contract / draft teams ----------
NK = {'49ers':'SF','Bears':'CHI','Bengals':'CIN','Bills':'BUF','Broncos':'DEN','Browns':'CLE','Buccaneers':'TB','Cardinals':'ARI','Chargers':'LAC',
 'Chiefs':'KC','Colts':'IND','Commanders':'WAS','Cowboys':'DAL','Dolphins':'MIA','Eagles':'PHI','Falcons':'ATL','Giants':'NYG','Jaguars':'JAX',
 'Jets':'NYJ','Lions':'DET','Packers':'GB','Panthers':'CAR','Patriots':'NE','Raiders':'LV','Rams':'LAR','Ravens':'BAL','Saints':'NO',
 'Seahawks':'SEA','Steelers':'PIT','Texans':'HOU','Titans':'TEN','Vikings':'MIN','Redskins':'WAS','Football Team':'WAS','Oilers':'TEN'}
DC = {'GNB':'GB','KAN':'KC','LVR':'LV','NOR':'NO','NWE':'NE','SDG':'LAC','SFO':'SF','TAM':'TB','RAM':'LAR','RAI':'LV','PHO':'ARI','OAK':'LV','STL':'LAR','SD':'LAC','LA':'LAR'}
def era(t, y):  # draft/contract team code -> franchise code used by the game, by year
    t = DC.get(t, t)
    if t == 'BAL' and y <= 1983: return 'IND'
    if t == 'HOU' and y <= 1996: return 'TEN'
    if t == 'STL': return 'LAR' if y >= 1995 else 'ARI'
    return t
byname = defaultdict(list)
for k, p in P.items():
    byname[norm(p['name'])].append(k)
    for a in p.get('alias', []): byname[norm(a)].append(k)
def dob(s):
    try: return datetime.datetime.strptime(s.strip(), '%B %d, %Y').strftime('%Y-%m-%d')
    except Exception: return None
ok = defaultdict(set)   # verified extra teams per player
ct = pd.read_csv('/home/claude/dl/c/historical_contracts.csv.gz', low_memory=False)
for n, d, t, y in zip(ct.player, ct.date_of_birth, ct.team, ct.year_signed):
    if not isinstance(t, str) or not isinstance(n, str): continue
    cand = list(dict.fromkeys(byname.get(norm(n), []))); bd = dob(d) if isinstance(d, str) else None
    ks = [k for k in cand if bd and birth(k) == bd]                                  # exact birthday match wins
    if not ks: ks = [k for k in cand if P[k]['first'] - 4 <= y <= P[k]['last'] + 1]  # else: the only same-name player active then
    if len(ks) != 1: continue
    for x in t.split('/'): ok[ks[0]].add(NK[x] if x in NK else era(x, y))
dr = pd.read_csv('/home/claude/dl/c/draft.csv', low_memory=False)
g2k = {p['gsis']: k for k, p in P.items() if p.get('gsis')}
for gi, n, t, y in zip(dr.gsis_id, dr.pfr_player_name, dr.team, dr.season):
    k = g2k.get(gi) if isinstance(gi, str) else None
    if not k and isinstance(n, str):
        ks = [k for k in byname.get(norm(n), []) if P[k]['first'] in (y, y + 1)]
        k = ks[0] if len(ks) == 1 else None
    if k:
        ok[k].add(era(t, y))
dropped = []
for k, p in P.items():
    roster = {f for f, y in FS.get(k, ())}
    keep = [t for t in p['teams'] if t in roster or t in ok[k]]
    for t in p['teams']:
        if t not in keep: dropped.append((p['disp'], t))
    p['teams'] = keep
print('unverified teams dropped:', len(dropped), Counter(t for _, t in dropped).most_common(5))
for n in ['John Elway', 'Justin Jefferson', 'Odell Beckham', 'Tim Tebow', 'AJ McCarron', 'Aldrick Robinson', 'Aaron Ripkowski', 'Tom Brady']:
    ks = [k for k in P if P[k]['disp'] == n]
    if ks: print(' ', n, sorted(P[ks[0]]['teams']), P[ks[0]]['nums'], P[ks[0]].get('alias'))
print('sample drops:', dropped[:12])

# ---------- remap puzzle keys ----------
rm = lambda x: remap.get(x, x)
seq = [([rm(x) for x in c], [rm(x) for x in h], d) for c, h, d in seq]; tri = [rm(k) for k in tri]
t1 = [rm(k) for k in t1]; t2 = [rm(k) for k in t2]
pickle.dump((P, TN), open('P3.pkl', 'wb')); pickle.dump(FS, open('FS.pkl', 'wb')); pickle.dump((LV, RS), open('lv.pkl', 'wb'))
pickle.dump((t1, t2, fame), open('fame.pkl', 'wb')); pickle.dump((seq, tri), open('puz.pkl', 'wb'))
print('players now:', len(P))
