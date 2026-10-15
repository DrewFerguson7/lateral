import pandas as pd, pickle, glob
from collections import defaultdict
P, TN = pickle.load(open('P.pkl', 'rb'))
d = pd.read_csv('/home/claude/dl/c/draft.csv', low_memory=False)
s = pd.concat([pd.read_csv(f, usecols=['player_id', 'season_type', 'fantasy_points_ppr'], low_memory=False) for f in glob.glob('/home/claude/dl/s/s_*.csv') if f[-8:] != '2025.csv'])
fp = s[s.season_type == 'REG'].groupby('player_id').fantasy_points_ppr.sum()
g2k = {p['gsis']: k for k, p in P.items() if p['gsis']}
byname = defaultdict(list)
for k, p in P.items(): byname[p['name']].append(k)
fame = defaultdict(float); hofs = set(); fpk = {}
for g, v in fp.items():
    if g in g2k: fame[g2k[g]] += v / 150; fpk[g2k[g]] = fpk.get(g2k[g], 0) + v          # ~ +1 per 150 career PPR points (Brady ~40)
for g, n, y, pb, ap, hof in zip(d.gsis_id, d.pfr_player_name, d.season, d.probowls, d.allpro, d.hof):
    k = g2k.get(g)
    if not k:
        ks = [k for k in byname.get(n, []) if abs(P[k]['first'] - y) <= 1]
        k = ks[0] if len(ks) == 1 else None
    if k: fame[k] += 3 * pb + 4 * ap + 30 * bool(hof); hofs.add(k) if hof else None
# casual-fan recognition: older non-Hall of Famers and non-HOF defenders count for less
DEF = {'DE','DT','DL','NT','LB','ILB','OLB','MLB','CB','S','SS','FS','DB'}
for k in list(fame):
    if k in hofs: continue
    if P[k]['last'] < 1995: fame[k] *= .45
    elif P[k]['last'] < 2000: fame[k] *= .75
    if P[k]['pos'] in DEF: fame[k] *= .85
    if P[k]['pos'] == 'FB': fame[k] *= .5
    if P[k]['pos'] in ('WR', 'RB', 'TE') and P[k]['last'] >= 2001 and fpk.get(k, 0) < 400: fame[k] *= .3  # return specialists
SKIP = {'K', 'P', 'LS'}; OL = {'T', 'G', 'C', 'OL', 'OT', 'OG'}
rank = sorted((k for k in fame if P[k]['pos'] not in SKIP and P[k]['last'] >= 1985 and P[k]['nums']), key=lambda k: -fame[k])
t1 = [k for k in rank if P[k]['pos'] not in OL][:230]
t2 = [k for k in rank if k not in set(t1)][:340]
print('tier1 sample:', [P[k]['disp'] for k in t1[:25]])
print('tier1 tail:', [P[k]['disp'] for k in t1[-40:]])
for n in ['Lorenzo Neal','Hardy Nickerson','Ray Childress','Michael Bates','Albert Lewis','Tim McDonald',"Leslie O'Neal"]: print(n, [('t1' if k in t1 else 't2' if k in t2 else '-') for k in P if P[k]['name']==n and k in fame])
print('tier2 tail:', [P[k]['disp'] for k in t2[-12:]])
pickle.dump((t1, t2, dict(fame)), open('fame.pkl', 'wb'))
