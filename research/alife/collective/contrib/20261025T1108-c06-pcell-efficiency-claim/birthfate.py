"""Fate by kind at birth: each cell's kind is fixed at its first snapshot (its yield rank among the
living cells then: low = below the median, high = above), and its later fate is counted: it dies
(death event), it divides (two-way split), or it is still alive at the end / merges. Cells seen in
fewer than MINLIFE snapshots are dropped (transient fragments). The inert marker gives the same table
for a trait without effect. Also reports the life course of dying cells (rank at 0, 0.5, 1 of life).
usage: python birthfate.py gen.json[.gz] [key=ym] [minlife=20]"""
import sys, json, gzip
import numpy as np

fn = sys.argv[1]
d = json.load(gzip.open(fn) if fn.endswith('.gz') else open(fn)); S = d['series']
key = sys.argv[2] if len(sys.argv) > 2 else 'ym'
MINLIFE = int(sys.argv[3]) if len(sys.argv) > 3 else 20
pos = {}
for a, x in enumerate(S):
    for i, cid in enumerate(x['id']):
        pos.setdefault(cid, []).append(a)


def rank(cid, a):
    x = S[a]; i = x['id'].index(cid); y = x[key][i]
    o = np.array([v for j, v in enumerate(x[key]) if j != i])
    return None if not len(o) else (np.sum(o < y) + 0.5 * np.sum(o == y)) / len(o)


fate = {}
for t, ty, p, ch in d['events']:
    if ty == 'death':
        fate[p[0]] = 'death'
    elif ty == 'split' and len(ch) >= 2:
        fate[p[0]] = 'split'
tab = {'low': {'death': 0, 'split': 0, 'other': 0}, 'high': {'death': 0, 'split': 0, 'other': 0}}
life = []
for cid, a in pos.items():
    if len(a) < MINLIFE or S[a[0]]['t'] <= 1000:
        continue
    r0 = rank(cid, a[0])
    if r0 is None:
        continue
    k = 'low' if r0 < 0.5 else 'high'
    f = fate.get(cid, 'other')
    tab[k][f] += 1
    if f == 'death':
        life.append([r0, rank(cid, a[len(a) // 2]), rank(cid, a[-1])])
L = np.array([[np.nan if v is None else v for v in r] for r in life]) if life else np.zeros((0, 3))
out = dict(file=fn, key=key, minlife=MINLIFE, by_birth_rank=tab,
           death_share_low=round(tab['low']['death'] / max(1, sum(tab['low'].values())), 3),
           death_share_high=round(tab['high']['death'] / max(1, sum(tab['high'].values())), 3),
           split_share_low=round(tab['low']['split'] / max(1, sum(tab['low'].values())), 3),
           split_share_high=round(tab['high']['split'] / max(1, sum(tab['high'].values())), 3),
           dying_cells_rank_birth_mid_death=[round(float(np.nanmean(L[:, k])), 3) for k in range(3)] if len(L) else None,
           n_dying=len(L))
print(json.dumps(out))
