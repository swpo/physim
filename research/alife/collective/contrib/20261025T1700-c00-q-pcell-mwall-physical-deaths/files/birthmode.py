"""How each mature cell (>= MINLIFE snapshots, first seen after t=1000) was born: as a split daughter, by
'appear' (a new component whose particles came from no t0 cell at >= 20%: grown from free particles or a
sub-20-particle fragment), by a merge, or as an unlogged bud (a new id with a parent but no event). Then the
fate (death / split / other) and mean birth rank in the trait (key), per birth mode."""
import sys, json, gzip
import numpy as np
fn = sys.argv[1]; key = sys.argv[2] if len(sys.argv) > 2 else 'ym'; MINLIFE = 20
d = json.load(gzip.open(fn)); S = d['series']
mode = {}
for t, ty, p, ch in d['events']:
    if ty == 'split':
        for c in ch: mode[c] = 'split'
    elif ty == 'appear':
        for c in ch: mode[c] = 'appear'
    elif ty == 'merge':
        for c in ch: mode[c] = 'merge'
fate = {}
for t, ty, p, ch in d['events']:
    if ty == 'death': fate[p[0]] = 'death'
    elif ty == 'split' and len(ch) >= 2: fate[p[0]] = 'split'
pos = {}
for a, x in enumerate(S):
    for i, cid in enumerate(x['id']): pos.setdefault(cid, []).append((a, i))
tab = {}
for cid, a in pos.items():
    if len(a) < MINLIFE or S[a[0][0]]['t'] <= 1000: continue
    m = mode.get(cid, 'bud')
    x = S[a[0][0]]; i = a[0][1]; y = x[key][i]; o = np.array([v for j, v in enumerate(x[key]) if j != i])
    r = (np.sum(o < y) + 0.5 * np.sum(o == y)) / len(o) if len(o) else np.nan
    f = fate.get(cid, 'other')
    T = tab.setdefault(m, dict(n=0, death=0, split=0, other=0, rank=[], np0=[]))
    T['n'] += 1; T[f] += 1; T['rank'].append(r); T['np0'].append(x['np'][i])
out = {m: dict(n=T['n'], death=T['death'], split=T['split'], other=T['other'], birth_rank=round(float(np.nanmean(T['rank'])), 3),
               np_at_birth=int(np.median(T['np0']))) for m, T in tab.items()}
print(json.dumps(dict(file=fn.split('/')[-1], key=key, **out)))
