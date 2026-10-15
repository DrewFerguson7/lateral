import pandas as pd, pickle
from collections import Counter, defaultdict
r = pd.read_pickle('r.pkl'); w = pd.read_pickle('w.pkl'); pl = pd.read_pickle('pl.pkl')
OK = ['ACT', 'RES', 'INA', 'PUP', 'NWT', 'RET']
r = r.dropna(subset=['team', 'full_name']); w = w.dropna(subset=['team', 'full_name'])  # every roster stint counts: cut, practice squad, reserve

DEF = {'AKR':'Akron Pros','BRK':'Brooklyn Dodgers','C-P':'Card-Pitt','CAN':'Canton Bulldogs','CHH':'Chicago Hornets',
 'CHR':'Chicago Rockets','CHT':'Chicago Tigers','COL':'Columbus Panhandles','DAY':'Dayton Triangles','DON':'Los Angeles Dons',
 'DUL':'Duluth Eskimos','ECG':'Evansville Crimson Giants','FYJ':'Frankford Yellow Jackets','HAM':'Hammond Pros','HAR':'Hartford Blues',
 'KEN':'Kenosha Maroons','LOU':'Louisville Colonels','MIL':'Milwaukee Badgers','MUN':'Muncie Flyers','NEW':'Newark Tornadoes',
 'NYB':'New York Bulldogs','NYY':'New York Yankees','OOR':'Oorang Indians','ORG':'Orange Tornadoes','P-P':'Phil-Pitt Steagles',
 'POT':'Pottsville Maroons','PRO':'Providence Steam Roller','RAC':'Racine Legion','RI':'Rock Island Independents',
 'ROC':'Rochester Jeffersons','SI':'Staten Island Stapletons','TOL':'Toledo Maroons','TON':'Tonawanda Kardex'}
OLD = {('BUF',1959):'Buffalo Bisons',('CIN',1967):'Cincinnati Reds',('MIN',1960):'Minneapolis Red Jackets',('MIA',1965):'Miami Seahawks',
 ('KC',1962):'Kansas City Cowboys',('DET',1929):'Detroit Wolverines',('WAS',1936):'Washington Senators',('BAL',1952):'Baltimore Colts (AAFC)',
 ('DAL',1959):'Dallas Texans (1952)',('LA',1949):'Los Angeles Buccaneers'}
MAP = {'ARZ':'ARI','PHO':'ARI','CHC':'ARI','SL':'LAR','RAM':'LAR','SD':'LAC','OAK':'LV','RAI':'LV','HST':'HOU','BLT':'BAL','CLV':'CLE',
 'NYT':'NYJ','NY':'NYG','TEX':'KC','COW':'DAL','CHB':'CHI','DEC':'CHI','CHS':'CHI','POR':'DET'}
def fr(t, s):
    if t in DEF: return t
    for (c, y), _ in OLD.items():
        if t == c and s <= y: return f'{c}{y}'
    if t == 'STL': return 'LAR' if s >= 1995 else ('ARI' if s >= 1960 else 'STL_OLD')
    if t == 'LA': return 'LAR'
    if t == 'BAL' and s <= 1983: return 'IND'
    if t == 'HOU' and s <= 1996: return 'TEN'
    if t == 'CLE' and s < 1946: return 'LAR' if s >= 1937 else 'CLE_OLD'
    if t == 'BOS': return 'NE' if s >= 1960 else ('WAS' if 1932 <= s <= 1936 else 'BOS_OLD')
    return MAP.get(t, t)
TN = {'ARI':'Arizona Cardinals','ATL':'Atlanta Falcons','BAL':'Baltimore Ravens','BUF':'Buffalo Bills','CAR':'Carolina Panthers',
 'CHI':'Chicago Bears','CIN':'Cincinnati Bengals','CLE':'Cleveland Browns','DAL':'Dallas Cowboys','DEN':'Denver Broncos','DET':'Detroit Lions',
 'GB':'Green Bay Packers','HOU':'Houston Texans','IND':'Indianapolis Colts','JAX':'Jacksonville Jaguars','KC':'Kansas City Chiefs',
 'LV':'Las Vegas Raiders','LAC':'Los Angeles Chargers','LAR':'Los Angeles Rams','MIA':'Miami Dolphins','MIN':'Minnesota Vikings',
 'NE':'New England Patriots','NO':'New Orleans Saints','NYG':'New York Giants','NYJ':'New York Jets','PHI':'Philadelphia Eagles',
 'PIT':'Pittsburgh Steelers','SF':'San Francisco 49ers','SEA':'Seattle Seahawks','TB':'Tampa Bay Buccaneers','TEN':'Tennessee Titans',
 'WAS':'Washington Commanders','STL_OLD':'St. Louis All-Stars/Gunners','CLE_OLD':'Cleveland Bulldogs/Indians','BOS_OLD':'Boston Yanks/Bulldogs'}
TN.update(DEF); TN.update({f'{c}{y}': n for (c, y), n in OLD.items()})

# player identity = name + birth date (falls back to name + gsis/position)
bd = {}
for df in (pl.rename(columns={'display_name': 'full_name'}), r, w):
    x = df.dropna(subset=['gsis_id', 'birth_date']); bd.update({g: b for g, b in zip(x.gsis_id, x.birth_date) if g not in bd})
for df in (r, w): df['birth_date'] = df.birth_date.fillna(df.gsis_id.map(bd))
def key(df): return df.full_name + '|' + df.birth_date.fillna(df.gsis_id.fillna('?'))
r['k'] = key(r); w['k'] = key(w)
r['f'] = [fr(t, s) for t, s in zip(r.team, r.season)]
rg = r.dropna(subset=['gsis_id']); g2k = dict(zip(rg.gsis_id, rg.k)); w['k'] = w.gsis_id.map(g2k).fillna(w.k)
w['f'] = [fr(t, s) for t, s in zip(w.team, w.season)]
both = pd.concat([r[['k', 'f', 'season', 'jersey_number', 'position', 'full_name', 'gsis_id', 'college']],
                  w[['k', 'f', 'season', 'jersey_number', 'position', 'full_name', 'gsis_id', 'college']]])
pc = pl.dropna(subset=['college_name'])
pg = pc.dropna(subset=['gsis_id']); by_g = dict(zip(pg.gsis_id, pg.college_name))
by_nb = dict(zip(pc.display_name + '|' + pc.birth_date.fillna('?'), pc.college_name))
pj = {gi: int(n) for gi, n in zip(pl.gsis_id, pd.to_numeric(pl.jersey_number, errors='coerce')) if isinstance(gi, str) and n == n and 0 < n < 100}
import re
cn = lambda c: c and re.sub(r'^University of |^The | University$| College$','',str(c).strip()).strip()
P = {}
for k, g in both.groupby('k'):
    nums = sorted({int(x) for x in pd.to_numeric(g.jersey_number, errors='coerce').dropna() if 0 < x < 100})
    gs = g.gsis_id.dropna()
    if not nums and len(gs) and pj.get(gs.iloc[0]): nums = [pj[gs.iloc[0]]]
    col = (by_g.get(gs.iloc[0]) if len(gs) else None) or by_nb.get(k) or (g.college.dropna().iloc[0] if g.college.notna().any() else None)
    cols = sorted({cn(x) for x in str(col).split(';') if cn(x)}) if col else []
    P[k] = dict(name=g.full_name.iloc[0], pos=g.position.mode().iloc[0] if g.position.notna().any() else '?',
                teams=sorted(set(g.f)), nums=nums, cols=cols, first=int(g.season.min()), last=int(g.season.max()), ns=g.season.nunique(), gsis=gs.iloc[0] if len(gs) else None)
# extra teams: every contract signed (OverTheCap) and the drafting team, so preseason-only stints count
NK = {'49ers':'SF','Bears':'CHI','Bengals':'CIN','Bills':'BUF','Broncos':'DEN','Browns':'CLE','Buccaneers':'TB','Cardinals':'ARI','Chargers':'LAC',
 'Chiefs':'KC','Colts':'IND','Commanders':'WAS','Cowboys':'DAL','Dolphins':'MIA','Eagles':'PHI','Falcons':'ATL','Giants':'NYG','Jaguars':'JAX',
 'Jets':'NYJ','Lions':'DET','Packers':'GB','Panthers':'CAR','Patriots':'NE','Raiders':'LV','Rams':'LAR','Ravens':'BAL','Saints':'NO',
 'Seahawks':'SEA','Steelers':'PIT','Texans':'HOU','Titans':'TEN','Vikings':'MIN'}
DC = {'GNB':'GB','KAN':'KC','LVR':'LV','NOR':'NO','NWE':'NE','SDG':'LAC','SFO':'SF','TAM':'TB','RAM':'LAR','RAI':'LV','PHO':'ARI'}
byname = defaultdict(list)
for k, p in P.items(): byname[p['name']].append(k)
def find(name, dob, yr):
    ks = byname.get(name, [])
    if dob == dob and dob and name + '|' + str(dob) in P: return name + '|' + str(dob)
    if len(ks) == 1: return ks[0] if P[ks[0]]['first'] - 4 <= yr <= P[ks[0]]['last'] + 12 else None
    ks = [k for k in ks if P[k]['first'] - 2 <= yr <= P[k]['last'] + 2]
    return ks[0] if len(ks) == 1 else None
ct = pd.read_csv('/home/claude/dl/c/historical_contracts.csv.gz', low_memory=False); added = 0
for n, dob, t, y in zip(ct.player, ct.date_of_birth, ct.team, ct.year_signed):
    k = find(n, dob, y)
    if not k or not isinstance(t, str): continue
    for x in t.split('/'):
        x = NK.get(x, x)
        if x in TN and x not in P[k]['teams']: P[k]['teams'].append(x); added += 1
dr = pd.read_csv('/home/claude/dl/c/draft.csv', low_memory=False); g2 = {p['gsis']: k for k, p in P.items() if p['gsis']}
for gi, n, t, y in zip(dr.gsis_id, dr.pfr_player_name, dr.team, dr.season):
    k = g2.get(gi) or find(n, None, y)
    if not k: continue
    x = fr(DC.get(t, t), y) if t != 'STL' else ('LAR' if y >= 1995 else 'ARI')
    if x in TN and x not in P[k]['teams']: P[k]['teams'].append(x); added += 1
print('added team links from contracts/draft:', added)
c = Counter(p['name'] for p in P.values()); seen = Counter()
for k, p in sorted(P.items(), key=lambda kv: (-kv[1]['ns'], kv[1]['first'])):
    if c[p['name']] == 1: p['disp'] = p['name']
    else:
        d = f"{p['name']} ({p['pos']} {p['first']})"; seen[d] += 1
        p['disp'] = d if seen[d] == 1 else f"{p['name']} ({p['pos']} {p['first']} #{seen[d]})"
print(len(P), 'players;', sum(bool(p['nums']) for p in P.values()), 'with numbers;', sum(bool(p['cols']) for p in P.values()), 'with college')
print(Counter(len(p['nums']) for p in P.values()).most_common(6))
for n in ['Tim Tebow','Tom Brady','Jalen Mills']: print([(p['disp'], p['teams'], p['nums'], p['cols']) for p in P.values() if p['name'] == n])
print(Counter(len(p['cols']) for p in P.values()))
pickle.dump((P, TN), open('P.pkl', 'wb'))
