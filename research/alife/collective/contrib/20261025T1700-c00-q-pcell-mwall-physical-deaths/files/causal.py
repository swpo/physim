"""(1) Cell-UNWEIGHTED mean ym/zm over time (selection between whole cells, not particle weighting).
(2) Does yield cause growth? Continuing cells: regress dlog(np) over the next LAG snapshots on the cell's
    deviation of ym (zm) from the snapshot mean, controlling for log np (OLS, pooled over t > 5000).
(3) Fate by birth rank restricted to split-born cells (excludes 'appear' cells = possible debris).
usage: python causal.py gen.json"""
import sys, json, numpy as np
d = json.load(open(sys.argv[1])); S = d['series']; E = d['events']
LAG = 40
def um(a, k): return float(np.mean(S[a][k])) if S[a]['n'] else None
idx = [0] + [int(np.argmin([abs(x['t'] - T) for x in S])) for T in (20000, 50000, 75000)] + [len(S) - 1]
out = dict(file=sys.argv[1], unweighted_cell_mean={k: [(S[a]['t'], round(um(a, k), 4)) for a in idx] for k in ('ym', 'zm')})
pos = [{c: i for i, c in enumerate(x['id'])} for x in S]
for key in ('ym', 'zm'):
    X, Y = [], []
    for a in range(len(S) - LAG):
        if S[a]['t'] < 5000 or S[a]['n'] < 4: continue
        m = np.mean(S[a][key])
        for c, i in pos[a].items():
            j = pos[a + LAG].get(c)
            if j is None: continue
            X.append((1.0, S[a][key][i] - m, np.log(S[a]['np'][i]))); Y.append(np.log(S[a + LAG]['np'][j]) - np.log(S[a]['np'][i]))
    X, Y = np.array(X), np.array(Y)
    b, *_ = np.linalg.lstsq(X, Y, rcond=None)
    r = Y - X @ b; s2 = r @ r / (len(Y) - 3); se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out['growth_on_' + key] = dict(n=len(Y), coef_per_unit_trait=round(float(b[1]), 3), se_naive=round(float(se[1]), 3),
                                   effect_of_0p05_dev=round(float(b[1] * 0.05), 3))
# split-born only fate table
bpos = {}
for a, x in enumerate(S):
    for i, c in enumerate(x['id']): bpos.setdefault(c, []).append((a, i))
born = set(); fate = {}
for t, ty, p, ch in E:
    if ty == 'split' and len(ch) >= 2: born.update(ch); fate[p[0]] = 'split'
    if ty == 'death': fate[p[0]] = 'death'
for key in ('ym', 'zm'):
    tab = {'low': [0, 0], 'high': [0, 0]}
    for c in born:
        L = bpos.get(c, [])
        if len(L) < 20 or S[L[0][0]]['t'] <= 1000: continue
        a, i = L[0]; y = S[a][key][i]; o = np.array([v for j, v in enumerate(S[a][key]) if j != i])
        if not len(o): continue
        r = (np.sum(o < y) + 0.5 * np.sum(o == y)) / len(o)
        tab['low' if r < 0.5 else 'high'][0 if fate.get(c) == 'death' else 1] += 1
    from scipy import stats
    out['split_born_fate_' + key] = dict(low_dead_alive=tab['low'], high_dead_alive=tab['high'],
                                         p_fisher=round(float(stats.fisher_exact([tab['low'], tab['high']])[1]), 4))
print(json.dumps(out))
