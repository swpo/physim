"""Are 'appear' cells remnants of cells just recorded as dead? For each mature appear cell (>= 20 snapshots),
find deaths in the preceding WIN steps and the smallest |ym(appear, first) - ym(dead, last)| and |zm - zm|
(both traits are near-fingerprints of a particle population). Null: the same distance to deaths drawn from
other times. Then recompute the claim's statistics without the appear lineages:
 - death percentile (deathsel.py logic, minlife 20) over deaths of cells not born by 'appear';
 - birth-rank fate (birthfate.py logic) over split-born cells only."""
import sys, json, gzip
import numpy as np
fn = sys.argv[1]; WIN = 2000
d = json.load(gzip.open(fn)); S = d['series']
pos = {}
for a, x in enumerate(S):
    for i, cid in enumerate(x['id']): pos.setdefault(cid, []).append((a, i))
def val(cid, which, key):
    a, i = pos[cid][0] if which == 'first' else pos[cid][-1]
    return S[a][key][i], S[a]['t'], S[a]['np'][i]
mode = {}
for t, ty, p, ch in d['events']:
    if ty in ('split', 'appear', 'merge'):
        for c in ch: mode[c] = ty
deaths = [(t, p[0]) for t, ty, p, ch in d['events'] if ty == 'death' and p[0] in pos]
rng = np.random.default_rng(0)
match, null, nprev = [], [], []
for cid, a in pos.items():
    if mode.get(cid) != 'appear' or len(a) < 20: continue
    ya, ta, na = val(cid, 'first', 'ym'); za = val(cid, 'first', 'zm')[0]
    prev = [(t, c) for t, c in deaths if ta - WIN <= t <= ta and c != cid]
    nprev.append(len(prev))
    if not prev: match.append(None); continue
    dist = [max(abs(ya - val(c, 'last', 'ym')[0]), abs(za - val(c, 'last', 'zm')[0])) for t, c in prev]
    k = int(np.argmin(dist)); match.append((round(dist[k], 4), ta - prev[k][0], val(prev[k][1], 'last', 'np')[2]))
    other = [c for t, c in deaths if abs(t - ta) > 5000]
    if other:
        pick = rng.choice(len(other), min(len(prev), len(other)), replace=False)
        null.append(min(max(abs(ya - val(other[j], 'last', 'ym')[0]), abs(za - val(other[j], 'last', 'zm')[0])) for j in pick))
m = [x for x in match if x]
print(json.dumps(dict(file=fn.split('/')[-1], n_appear_mature=len(match), with_death_in_prev_2000=len(m),
      median_dist=float(np.median([x[0] for x in m])) if m else None, share_dist_below_0p01=round(float(np.mean([x[0] < 0.01 for x in m])), 2) if m else None,
      median_lag=float(np.median([x[1] for x in m])) if m else None, null_median_dist=round(float(np.median(null)), 4) if null else None,
      null_share_below_0p01=round(float(np.mean([v < 0.01 for v in null])), 2) if null else None)))
# recompute selection statistics without appear-born cells
def pct(cid, tbefore, key):
    a = [k for k, _ in pos.get(cid, []) if S[k]['t'] < tbefore]
    if not a: return None
    x = S[a[-1]]; i = x['id'].index(cid); y = x[key][i]
    o = np.array([v for j, v in enumerate(x[key]) if j != i])
    return None if not len(o) else (np.sum(o < y) + 0.5 * np.sum(o == y)) / len(o)
for key in ('ym', 'zm'):
    allD = [pct(p, t, key) for t, p in deaths if t > 1000 and len(pos[p]) >= 20]
    noapp = [pct(p, t, key) for t, p in deaths if t > 1000 and len(pos[p]) >= 20 and mode.get(p) != 'appear']
    allD = [v for v in allD if v is not None]; noapp = [v for v in noapp if v is not None]
    fate = {}
    for t, ty, p, ch in d['events']:
        if ty == 'death': fate[p[0]] = 'death'
        elif ty == 'split' and len(ch) >= 2: fate[p[0]] = 'split'
    tab = {'low': [0, 0], 'high': [0, 0]}
    for cid, a in pos.items():
        if len(a) < 20 or S[a[0][0]]['t'] <= 1000 or mode.get(cid) != 'split': continue
        x = S[a[0][0]]; i = a[0][1]; y = x[key][i]; o = np.array([v for j, v in enumerate(x[key]) if j != i])
        r = (np.sum(o < y) + 0.5 * np.sum(o == y)) / len(o)
        k = 'low' if r < 0.5 else 'high'
        tab[k][0] += 1; tab[k][1] += fate.get(cid) == 'death'
    print(json.dumps(dict(key=key, n_death_all=len(allD), pct_all=round(float(np.mean(allD)), 3), n_death_no_appear=len(noapp),
          pct_no_appear=round(float(np.mean(noapp)), 3) if noapp else None, below_median_no_appear=int(sum(v < 0.5 for v in noapp)),
          splitborn_low_died=f"{tab['low'][1]}/{tab['low'][0]}", splitborn_high_died=f"{tab['high'][1]}/{tab['high'][0]}")))
