"""Add a new season's rosters (trades, signings, rookies) to the player data without touching existing puzzles.
Additive only: existing players gain teams, numbers and seasons; new players are added with a unique display name.
Usage: python3 update_season.py 2026   (reads data/rosters_2026.csv, data/players_latest.csv, data/draft_2026.csv)"""
import pickle, re, sys, shutil, os, pandas as pd
from collections import Counter
Y = int(sys.argv[1]) if len(sys.argv) > 1 else 2026
for f in ['P3.pkl', 'FS.pkl', 'lv.pkl']:
    if not os.path.exists(f'{f}.pre{Y}'): shutil.copy(f, f'{f}.pre{Y}')
P, TN = pickle.load(open('P3.pkl', 'rb')); FS = pickle.load(open('FS.pkl', 'rb')); LV, RS = pickle.load(open('lv.pkl', 'rb'))
MAP = {'ARZ': 'ARI', 'LA': 'LAR', 'SD': 'LAC', 'OAK': 'LV', 'STL': 'LAR', 'HST': 'HOU', 'BLT': 'BAL', 'CLV': 'CLE', 'WSH': 'WAS', 'JAC': 'JAX'}
cn = lambda c: c and re.sub(r'^University of |^The | University$| College$', '', str(c).strip()).strip()
r = pd.read_csv(f'data/rosters_{Y}.csv', low_memory=False).dropna(subset=['team', 'full_name'])
pl = pd.read_csv('data/players_latest.csv', low_memory=False)
col_g = {g: c for g, c in zip(pl.gsis_id, pl.college_name) if isinstance(g, str) and isinstance(c, str)}
dr = pd.read_csv(f'data/draft_{Y}.csv') if os.path.exists(f'data/draft_{Y}.csv') else pd.DataFrame(columns=['gsis_id', 'round'])
rd1 = set(dr[dr['round'] == 1].gsis_id.dropna())
g2k = {p['gsis']: k for k, p in P.items() if p.get('gsis')}
nb = {}
for k, p in P.items():
    b = k.split('|', 1)[1]
    for n in [p['name']] + p.get('alias', []): nb.setdefault((n, b), k)
disp_taken = Counter(p['disp'] for p in P.values())
byname = {}
for k0, p0 in P.items(): byname.setdefault(p0['name'], []).append(k0)
added_links, new_players, upd = [], [], set()
for g, rows in r.groupby(r.gsis_id.fillna(r.full_name + '|' + r.birth_date.fillna('?'))):
    row = rows.iloc[0]; b = str(row.birth_date)[:10] if isinstance(row.birth_date, str) else '?'
    k = g2k.get(g) or nb.get((row.full_name, b))
    if k is None:   # same name, no birth date on file, active in the last two seasons: same person
        cand = [x for x in byname.get(row.full_name, []) if x.endswith('|?') and P[x]['last'] >= Y - 2]
        if len(cand) == 1: k = cand[0]
    teams = sorted({MAP.get(t, t) for t in rows.team if MAP.get(t, t) in TN})
    nums = sorted({int(x) for x in pd.to_numeric(rows.jersey_number, errors='coerce').dropna() if 0 < x < 100})
    if not teams: continue
    if k is None:   # brand-new player (rookie or first NFL roster spot)
        k = f'{row.full_name}|{b}'
        if k in P: k += f'|{g}'
        col = col_g.get(g) or (row.college if isinstance(row.college, str) else None)
        name = row.full_name; disp = name if not disp_taken[name] and name not in byname else f'{name} ({row.position} {Y})'
        while disp_taken[disp]: disp += '*'
        disp_taken[disp] += 1
        P[k] = dict(name=name, pos=str(row.position), teams=[], nums=[], cols=sorted({cn(x) for x in str(col).split(';') if cn(x)}) if col else [],
                    first=Y, last=Y, ns=1, gsis=g if isinstance(g, str) and g.startswith('00-') else None, disp=disp, main=nums[0] if nums else None)
        LV[k] = 2 if g in rd1 else 3; new_players.append(disp)
    p = P[k]
    for t in teams:
        if t not in p['teams']: p['teams'].append(t); added_links.append((p['disp'], t))
        FS.setdefault(k, set()).add((t, Y))
    p['nums'] = sorted(set(p['nums']) | set(nums))
    if not p.get('main') and nums: p['main'] = nums[0]
    p['last'] = max(p['last'], Y); p['ns'] = len({y for _, y in FS[k]}) or p['ns']; upd.add(k)
pickle.dump((P, TN), open('P3.pkl', 'wb')); pickle.dump(FS, open('FS.pkl', 'wb')); pickle.dump((LV, RS), open('lv.pkl', 'wb'))
print(f'{Y}: {len(upd)} players updated, {len(added_links)} new team links, {len(new_players)} new players')
print('sample new links:', added_links[:25])
print('sample new players:', new_players[:15])
