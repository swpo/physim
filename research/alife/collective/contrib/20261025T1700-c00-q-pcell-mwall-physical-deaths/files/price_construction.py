"""Price decomposition of the particle-weighted mean trait over cells, from a genealogy JSON
(c14 genealogy.py format). Per snapshot interval t0->t1 (DT=50):
  sel   = sum_{j in K1} n_j y_anc(j) / N_K1 - Ybar0     (between-cell: differential growth + deaths)
  trans = sum_{j in K1} n_j (y_j - y_anc(j)) / N_K1      (within-cell change, incl. daughters vs parent)
  resid = dYbar - sel - trans                             (cells of unknown ancestry: appear, buds, merges)
K1 = t1 cells that continue an id or are split daughters with a known parent.
sel is further split per t0 cell i by the eventual fate of id i: 'death' (dies), 'split', 'other'
(alive at end, absorbed, merged): c_i = (D_i/N_K1 - n_i/N0)(y_i - Ybar0).
usage: price.py gen.json[.gz] [key]"""
import sys, json, gzip
import numpy as np
fn = sys.argv[1]; key = sys.argv[2] if len(sys.argv) > 2 else 'ym'
d = json.load(gzip.open(fn) if fn.endswith('.gz') else open(fn))
S = [x for x in d['series']]
fate = {}
splitpar = {}  # (t, child) -> parent
for t, ty, p, ch in d['events']:
    if ty == 'death':
        fate[p[0]] = 'death'
    elif ty == 'split' and len(ch) >= 2:
        fate.setdefault(p[0], 'split')
    if ty == 'split':
        for c in ch:
            splitpar[c] = p[0]
tot = dict(sel=0.0, trans=0.0, resid=0.0, sel_death=0.0, sel_split=0.0, sel_other=0.0)
t_start = None
for a in range(1, len(S)):
    x0, x1 = S[a - 1], S[a]
    if x0['n'] == 0 or x1['n'] == 0:
        continue
    if x1['t'] <= 1000:
        continue
    id0 = {c: i for i, c in enumerate(x0['id'])}
    n0 = np.array(x0['np'], float); y0 = np.array(x0[key], float)
    n1 = np.array(x1['np'], float); y1 = np.array(x1[key], float)
    Y0 = (n0 * y0).sum() / n0.sum(); Y1 = (n1 * y1).sum() / n1.sum()
    D = np.zeros(len(n0)); acc_sel = 0.0; acc_tr = 0.0; NK = 0.0
    anc = []
    for j, c in enumerate(x1['id']):
        if c in id0:
            i = id0[c]
        elif c in splitpar and splitpar[c] in id0:
            i = id0[splitpar[c]]
        else:
            continue
        anc.append((j, i))
        D[i] += n1[j]; NK += n1[j]
    if NK == 0:
        continue
    for j, i in anc:
        acc_sel += n1[j] * y0[i]; acc_tr += n1[j] * (y1[j] - y0[i])
    sel = acc_sel / NK - Y0; tr = acc_tr / NK
    tot['sel'] += sel; tot['trans'] += tr; tot['resid'] += (Y1 - Y0) - sel - tr
    c = (D / NK - n0 / n0.sum()) * (y0 - Y0)
    for i, cid in enumerate(x0['id']):
        f = fate.get(cid, 'other')
        tot['sel_' + f] += c[i]
    if t_start is None:
        t_start = (x0['t'], Y0)
Yend = (np.array(S[-1]['np']) * np.array(S[-1][key])).sum() / np.sum(S[-1]['np'])
out = dict(file=fn.split('/')[-1], key=key, t0=t_start[0], Ybar_t0=round(t_start[1], 4), Ybar_end=round(float(Yend), 4),
           dY=round(float(Yend - t_start[1]), 4), **{k: round(v, 4) for k, v in tot.items()})
print(json.dumps(out))
