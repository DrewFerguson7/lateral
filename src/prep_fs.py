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
fs = {}
for k, f, y in zip(both.k, both.f, both.season): fs.setdefault(k, set()).add((f, int(y)))
pickle.dump(fs, open('FS.pkl', 'wb')); print(len(fs), 'players with seasons')
