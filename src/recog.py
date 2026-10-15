"""Recognition level for every player, ranked within his era.
0 star (Hall of Fame or top 1%) · 1 well known (top 5%) · 2 lesser known (top 25%) · 3 obscure · 4 barely played / pre-1960
"""
import pickle, glob, pandas as pd
from collections import defaultdict
P, TN = pickle.load(open('P3.pkl', 'rb'))
g2k = {p['gsis']: k for k, p in P.items() if p['gsis']}
byname = defaultdict(list)
for k, p in P.items(): byname[p['name']].append(k)
R = defaultdict(float)

def rd(pattern, cols):
    return pd.concat([pd.read_csv(f, usecols=cols, low_memory=False) for f in glob.glob(pattern) if __import__('os').path.getsize(f) > 2000])
off = rd('/home/claude/dl/s/s_*.csv', ['player_id', 'season_type', 'fantasy_points_ppr'])
for g, v in off[off.season_type == 'REG'].groupby('player_id').fantasy_points_ppr.sum().items():
    if g in g2k: R[g2k[g]] += v / 150
dfn = rd('/home/claude/dl/def/def_*.csv', ['player_id', 'season_type', 'def_tackles', 'def_sacks', 'def_interceptions', 'def_fumbles_forced'])
d = dfn[dfn.season_type == 'REG'].groupby('player_id')[['def_tackles', 'def_sacks', 'def_interceptions', 'def_fumbles_forced']].sum()
for g, r in d.iterrows():
    if g in g2k: R[g2k[g]] += r.def_tackles / 110 + r.def_sacks * .45 + r.def_interceptions * .7 + r.def_fumbles_forced * .4
kk = rd('/home/claude/dl/def/kicking_*.csv', ['player_id', 'season_type', 'fg_made'])
for g, v in kk[kk.season_type == 'REG'].groupby('player_id').fg_made.sum().items():
    if g in g2k: R[g2k[g]] += v / 45
dr = pd.read_csv('/home/claude/dl/c/draft.csv', low_memory=False)
for g, n, y, pb, ap, rnd in zip(dr.gsis_id, dr.pfr_player_name, dr.season, dr.probowls, dr.allpro, dr['round']):
    k = g2k.get(g)
    if not k:
        ks = [k for k in byname.get(n, []) if abs(P[k]['first'] - y) <= 1]
        k = ks[0] if len(ks) == 1 else None
    if k: R[k] += 3 * pb + 4 * ap + (2.5 if rnd == 1 else 1 if rnd == 2 else 0)
for k, p in P.items(): R[k] += min(p['ns'], 18) * .35
hofk = set()
for n in open('hof.txt').read().strip().split('|'):
    ks = [k for k in P if P[k]['name'] == n]
    if ks: hofk.add(max(ks, key=lambda k: P[k]['ns']))

era = lambda p: 0 if p['last'] < 1960 else 1 if p['last'] < 1980 else 2 if p['last'] < 1999 else 3
lv = {}
for e in range(4):
    ks = sorted((k for k in P if era(P[k]) == e), key=lambda k: -R[k]); n = len(ks)
    for i, k in enumerate(ks):
        q = i / n
        lv[k] = 0 if q < .03 else 1 if q < .08 else 2 if q < .30 else 3
for k, p in P.items():
    if k in hofk: lv[k] = 0
    elif p['last'] < 1960: lv[k] = 4
    elif p['ns'] <= 2 and p['last'] < 2024 and lv[k] >= 2: lv[k] = 4
pickle.dump((lv, {k: round(R[k], 1) for k in P}), open('lv.pkl', 'wb'))
from collections import Counter
print('levels:', sorted(Counter(lv.values()).items()))
ref = ['Joe Namath', 'Jim Plunkett', 'Jack Tatum', 'Lyle Alzado', 'Jalen Mills', 'Elliott Fry', 'Andrew Luck', 'Mike Evans', 'Danny Amendola', 'Julian Edelman',
       'Chris Snee', 'Matt Bryant', 'Jalen Ramsey', 'Daryl Worley', 'Brandin Cooks', 'Wes Welker', 'Rob Gronkowski', 'Ken Anderson', 'Greg Davis', 'Caleb Williams', 'Jayden Daniels', 'Matthew Wright', 'Tillie Voss', 'Mark Gastineau', 'Bernard Carter', 'Junior Seau']
for n in ref:
    ks = [k for k in P if P[k]['disp'] == n]
    if ks: print(f'{n:16} level {lv[ks[0]]}  R={R[ks[0]]:.1f}  {P[ks[0]]["pos"]} {P[ks[0]]["first"]}-{P[ks[0]]["last"]}')
