import pickle, json
P, TN = pickle.load(open('P3.pkl', 'rb')); seq, tri = pickle.load(open('puz.pkl', 'rb'))
COL = sorted({c for p in P.values() for c in p['cols']}); ci = {c: i for i, c in enumerate(COL)}
esc = lambda x: x.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
rows = sorted(P.values(), key=lambda p: (-p['ns'], p['disp']))
fs = pickle.load(open('FS.pkl', 'rb')); t1, t2, fame = pickle.load(open('fame.pkl', 'rb'))
from collections import Counter
def tseas(k):
    c = Counter(f for f, y in fs.get(k, ()))
    return ' '.join(f"{t}:{c.get(t, 0)}" for t in P[k]['teams'])
kk = {id(p): k for k, p in P.items()}
LV, _ = pickle.load(open('lv.pkl', 'rb'))  # recognition level by era (recog.py)
# Pro Football Hall of Fame players (Wikipedia list): the longest career with that name gets the flag
HOFK = set()
for n in open('hof.txt').read().strip().split('|'):
    ks = [k for k, p in P.items() if p['name'] == n]
    if ks: HOFK.add(max(ks, key=lambda k: P[k]['ns']))
print('Hall of Famers matched:', len(HOFK))
D = '\n'.join(f"{p['disp']}|{tseas(kk[id(p)])}|{' '.join(map(str, p['nums']))}|{' '.join(str(ci[c]) for c in p['cols'])}|{p.get('main') or ''}|{p['pos']}|{p['first']}|{p['last']}|{p['ns']}|{round(fame.get(kk[id(p)], 0))}|{1 if kk[id(p)] in HOFK else 0}|{LV[kk[id(p)]]}" for p in rows)
path = lambda xs: '>'.join(P[x]['disp'] if x in P else x for x in xs)
# daily hint: 3 famous real teammates of the target (overlapping seasons) that don't connect directly to the start player
from collections import defaultdict
by = defaultdict(set)
for k, s in fs.items():
    for x in s: by[x].add(k)
notable = set(t1) | set(t2)
def conns(k, hard):
    p = P[k]; c = {f'#{n}' for n in p['nums']} | {f'C:{x}' for x in p['cols']}
    return c if hard else c | {f'T:{t}' for t in p['teams']}
def mates(a, b, hard):
    m = set().union(*(by[x] for x in fs.get(b, ()))) - {a, b}
    ca = conns(a, hard)
    m = [k for k in m if k in notable and not (conns(k, hard) & ca)]
    return ';'.join(P[k]['disp'] for k in sorted(m, key=lambda k: -fame.get(k, 0))[:3])
Q = '\n'.join('~'.join([path(c), path(h), str(d), mates(c[0], c[-1], 0), mates(c[0], c[-1], 1)]) for c, h, d in seq)
_qf = json.load(open('qfix.json')) if __import__('os').path.exists('qfix.json') else {}
Q = '\n'.join(('~'.join([_qf[str(i)]] + l.split('~')[1:]) if str(i) in _qf else l) for i, l in enumerate(Q.split('\n')))
few = sum(len(l.split('~')[3].split(';')) < 3 for l in Q.split('\n')); print('puzzles with <3 teammate hints:', few)
import re, pandas as pd
_pl = pd.read_csv('data/colleges.csv', usecols=['college_name', 'college_conference'], low_memory=False).dropna()
_cn = lambda c: re.sub(r'^University of |^The | University$| College$', '', str(c).strip()).strip()
_pl['c'] = [_cn(x.split(';')[-1]) for x in _pl.college_name]
_short = {'Big Twelve Conference': 'Big 12', 'Pacific Twelve Conference': 'Pac-12', 'Pacific Ten Conference': 'Pac-10', 'Southeastern Conference': 'SEC', 'Atlantic Coast Conference': 'ACC', 'Big Ten Conference': 'Big Ten', 'American Athletic Conference': 'American Athletic (AAC)', 'Mid-American Conference': 'Mid-American (MAC)', 'Mid-Eastern Athletic Conference': 'MEAC', 'Southwestern Athletic Conference': 'SWAC', 'Colonial Athletic Association': 'CAA', 'Missouri Valley Football Conference': 'Missouri Valley (MVFC)'}
conf = {c: _short.get(v, v.replace(' Conference', '')) for c, v in _pl[_pl.college_conference != 'NO COLLEGE'].groupby('c').college_conference.agg(lambda x: x.value_counts().index[0]).items()}
conf.update({'Mississippi Valley State': 'SWAC', 'Livingstone': 'CIAA', 'Savannah State': 'SIAC', 'Texas A&M University-Kingsville': 'Lone Star'})
cf = lambda k: next((conf[c] for c in P[k]['cols'] if c in conf), '')
# school colors (College Football Data via cfbfastR) with plain color names
_t = pd.read_parquet('data/t_2024.parquet')
_alias = {'Boston': 'Boston College', 'N.C. State': 'NC State', 'Miami (Ohio)': 'Miami (OH)', 'Mississippi': 'Ole Miss', 'Southern Mississippi': 'Southern Miss',
          'Tennessee-Chattanooga': 'Chattanooga', 'Texas A&M University-Kingsville': 'Texas A&M-Kingsville', 'Southern California': 'USC', 'Louisiana State': 'LSU'}
_col = {r.school: [c for c in (r.color, r.alt_color) if isinstance(c, str) and len(c) == 7 and c != '#null'] for r in _t.itertuples()}
_names = [('black','#000000'),('white','#ffffff'),('gray','#8a8d8f'),('silver','#c0c0c0'),('navy blue','#0b1f41'),('royal blue','#0033a0'),('light blue','#7bafd4'),('red','#cc0000'),('crimson','#9e1b32'),('maroon','#5d1725'),('cardinal','#8c1515'),('burnt orange','#bf5700'),('orange','#ff7f00'),('gold','#c99700'),('yellow','#ffcd00'),('old gold','#b3a369'),('green','#006a4e'),('dark green','#154734'),('kelly green','#2e8b57'),('purple','#4b2e83'),('teal','#00797c'),('brown','#4e3629'),('cream','#f4e7c5'),('vegas gold','#c5b358'),('tan','#d2b48c')]
_rgb = lambda h: [int(h[i:i+2], 16) for i in (1, 3, 5)]
_nm = lambda h: 'black' if max(_rgb(h)) < 70 and max(_rgb(h)) - min(_rgb(h)) < 25 else min(_names, key=lambda n: sum((a - b) ** 2 for a, b in zip(_rgb(h), _rgb(n[1]))))[0]
def sc(k):
    for c in P[k]['cols']:
        cs = _col.get(_alias.get(c, c))
        if cs:
            out = []
            for h in cs:
                n = _nm(h.lower())
                if n not in [o[0] for o in out]: out.append((n, h.lower()))
            return ','.join(f'{n}:{h}' for n, h in out)
    return ''
TV = '\n'.join(f"{P[k]['disp']}|{P[k]['pos']}|{P[k]['first']}–{P[k]['last']}|{cf(k)}|{sc(k)}" for k in tri)
print('trivia players with school colors:', sum(1 for l in TV.split('\n') if l.split('|')[4]), 'of', len(tri))
t = open('tpl2.html').read().replace('`__HR__`', '`' + (open('hr.txt').read() if __import__('os').path.exists('hr.txt') else '') + '`').replace('__AL__', json.dumps({__import__('re').sub(r'\s+(jr|sr|ii|iii|iv|v)$', '', __import__('re').sub(r"[.'’]", '', a.lower())).strip(): p['disp'] for p in P.values() for a in p.get('alias', [])})).replace('__MX__', open('mx.json').read() if __import__('os').path.exists('mx.json') else '{}').replace('__COL__', json.dumps(COL)).replace('__HBCU__', json.dumps(['Alabama A&M', 'Alabama State', 'Albany State (GA)', 'Albany State (Ga.)', 'Alcorn State', 'Arkansas at Pine Bluff', 'Benedict', 'Bethune-Cookman', 'Bishop', 'Bowie State', 'Central State University, Oh', 'Cheyney', 'Clark Atlanta', 'Delaware State', 'Elizabeth City State Univ', 'Fayetteville State', 'Florida A&M', 'Fort Valley State', 'Grambling', 'Grambling State', 'Hampton', 'Howard', 'Jackson State', 'Johnson C. Smith', 'Kentucky State', 'Knoxville', 'Lane', 'Langston', 'Lincoln University (MO)', 'Livingstone', 'Miles', 'Mississippi Valley State', 'Morehouse', 'Morgan State', 'Norfolk State', 'North Carolina A&T', 'North Carolina Central', 'Prairie View A&M', 'Savannah State', 'Shaw', 'South Carolina State', 'Southern', 'Stillman', 'Tennessee State', 'Texas Southern', 'Tuskegee', 'Virginia State', 'Virginia Union', 'West Virginia State', 'Wiley'])).replace('__TN__', json.dumps(TN)).replace('`__Q__`', '`' + esc(Q) + '`').replace('`__D__`', '`' + esc(D) + '`').replace('`__TV__`', '`' + esc(TV) + '`')
open('out/gridiron-handoff.html', 'w').write(t)
print(len(t) // 1024, 'KB', len(P), 'players', len(COL), 'colleges', len(seq), 'puzzles', len(tri), 'trivia')
