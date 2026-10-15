"""Fixes from the Oct 2026 data audit. Idempotent: run on P3.pkl/FS.pkl (backups kept as *.pre_audit)."""
import pickle, shutil, os, datetime, re, pandas as pd
from collections import defaultdict
for f in ['P3.pkl', 'FS.pkl']:
    if not os.path.exists(f + '.pre_audit'): shutil.copy(f, f + '.pre_audit')
P, TN = pickle.load(open('P3.pkl', 'rb')); FS = pickle.load(open('FS.pkl', 'rb'))
by = defaultdict(list)
for k, p in P.items(): by[p['disp']].append(k)
key = lambda n: by[n][0] if len(by[n]) == 1 else (_ for _ in ()).throw(KeyError(f'{n}: {by[n]}'))
log = []

# 1) team codes split by era (old codes lumped different franchises together)
TN.update({'DET1921': 'Detroit Heralds/Tigers', 'DET1926': 'Detroit Panthers', 'BUF1929': 'Buffalo All-Americans/Bisons',
           'BUF1959': 'Buffalo Bills (AAFC)', 'CIN1921': 'Cincinnati Celts', 'MIN1960': 'Minneapolis Marines/Red Jackets'})
def recode(c, y):
    if c == 'CHR' and y >= 1960: return 'LAC'            # 1960 Los Angeles Chargers, not the AAFC Chicago Rockets
    if c == 'DET1929': return 'DET1921' if y <= 1921 else 'DET1926' if y <= 1926 else c
    if c == 'BUF1959' and y <= 1929: return 'BUF1929'
    if c == 'CIN1967' and y <= 1921: return 'CIN1921'
    return c
for k in P:
    old = FS.get(k, set()); new = {(recode(c, y), y) for c, y in old}
    if new != old:
        FS[k] = new; fr = {c for c, y in old}; to = {c for c, y in new}
        P[k]['teams'] = list(dict.fromkeys([t for t in P[k]['teams'] if t not in fr - to] + sorted(to - fr)))
        log.append(('recode', P[k]['disp'], sorted(fr - to), sorted(to - fr)))

# 2) stray seasons / wrong rows
STRAY = {'Bernard Williams': [('PHI', 2023)], 'Donald Washington': [('PIT', 2016)], 'Tim Shaw': [('TEN', 2016)],
         'Tyronne Green': [('CAR', 2016)], 'Ray Flaherty': [('LA1949', 1926)], 'Quinnen Williams': [('NYG', 2019)]}
for n, rows in STRAY.items():
    k = key(n); FS[k] -= set(rows)
    for c, y in rows:
        if c not in {f for f, _ in FS[k]} and c in P[k]['teams']: P[k]['teams'].remove(c)
    ys = sorted({y for _, y in FS[k]}); P[k]['first'], P[k]['last'] = ys[0], ys[-1]; P[k]['ns'] = len(ys)
    log.append(('stray', n, rows))

# 3) contract teams: kept as before (contract birth dates are often slightly off, so a strict rule drops real stints)
ok = defaultdict(set)

# 4) verified stints the sources miss (drafted before 1980, or camp signings)
ADD = {'Johnny Unitas': 'PIT', 'Steve Largent': 'TEN', 'Chad Ochocinco': 'MIA', 'Terrell Owens': 'SEA', 'Chris Hovan': 'LAR',
       'Darrell Russell': 'TB', 'Steve DeBerg': 'DAL', 'Jeff Bostic': 'PHI', 'Joe Namath': 'ARI'}
for n, t in ADD.items():
    for k in by[n]:
        ok[k].add(t)
        if t not in P[k]['teams']: P[k]['teams'].append(t); log.append(('add', P[k]['disp'], t))
DROP = {'Derrick Johnson': 'NYG'}   # confirmed never with the Giants (contract belonged to someone else)
for k, p in P.items():
    roster = {f for f, _ in FS.get(k, ())}
    keep = list(p['teams'])
    if p['disp'] in DROP: keep = [t for t in keep if t != DROP[p['disp']]]
    for t in p['teams']:
        if t not in keep: log.append(('drop', p['disp'], t))
    p['teams'] = keep

# 5) numbers
k = key('Quinnen Williams'); P[k]['nums'] = [n for n in P[k]['nums'] if n != 49]
k = key('James Williams (DB 1990)'); P[k]['nums'] = [31]; P[k]['main'] = 31
pickle.dump((P, TN), open('P3.pkl', 'wb')); pickle.dump(FS, open('FS.pkl', 'wb'))
for l in log: print(*l)
print('changes:', len(log))
