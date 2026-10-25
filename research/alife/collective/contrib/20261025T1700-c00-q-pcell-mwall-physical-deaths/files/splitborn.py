"""Dying mature cells by birth mode: mean trait rank at birth / mid-life / last snapshot (birthfate.py logic),
for split-born cells versus appear-born remnants; pooled over the files given."""
import sys, json, gzip
import numpy as np
res = {}
for fn in sys.argv[1:]:
    d = json.load(gzip.open(fn)); S = d['series']
    pos = {}
    for a, x in enumerate(S):
        for i, cid in enumerate(x['id']): pos.setdefault(cid, []).append(a)
    mode = {}
    for t, ty, p, ch in d['events']:
        if ty in ('split', 'appear', 'merge'):
            for c in ch: mode[c] = ty
    dead = {p[0] for t, ty, p, ch in d['events'] if ty == 'death'}
    def rank(cid, a, key):
        x = S[a]; i = x['id'].index(cid); y = x[key][i]; o = np.array([v for j, v in enumerate(x[key]) if j != i])
        return (np.sum(o < y) + 0.5 * np.sum(o == y)) / len(o) if len(o) else np.nan
    for cid, a in pos.items():
        if len(a) < 20 or S[a[0]]['t'] <= 1000 or cid not in dead: continue
        m = mode.get(cid, 'bud')
        for key in ('ym', 'zm'):
            r = [rank(cid, a[0], key), rank(cid, a[len(a) // 2], key), rank(cid, a[-1], key)]
            res.setdefault((fn.split('/')[-1], m, key), []).append(r)
for (f, m, k), v in sorted(res.items()):
    V = np.array(v)
    print(json.dumps(dict(file=f, mode=m, key=k, n=len(V), rank_birth_mid_death=[round(float(np.nanmean(V[:, j])), 3) for j in range(3)])))
