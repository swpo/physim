"""Cell-level selection readout from a genealogy JSON: the yield of each dying cell (its last
snapshot) as a percentile of the living cells' yields at that time; and the same for cells that
split (parent at its last snapshot before the split). Under no selection both are ~uniform (mean 0.5)."""
import sys, json, numpy as np
d = json.load(open(sys.argv[1])); S = d['series']
key = sys.argv[2] if len(sys.argv) > 2 else 'ym'
minlife = int(sys.argv[3]) if len(sys.argv) > 3 else 0  # only cells seen in >= minlife snapshots
pos = {}
for a, x in enumerate(S):
    for i, cid in enumerate(x['id']):
        pos.setdefault(cid, []).append(a)
def pct(cid, tbefore):
    a = [k for k in pos.get(cid, []) if S[k]['t'] < tbefore]
    if not a: return None
    a = a[-1]; x = S[a]; i = x['id'].index(cid); y = x[key][i]
    others = [v for j, v in enumerate(x[key]) if j != i]
    if not others: return None
    return (np.sum(np.array(others) < y) + 0.5 * np.sum(np.array(others) == y)) / len(others), y
D = [pct(e[2][0], e[0]) for e in d['events'] if e[1] == 'death' and e[0] > 1000 and len(pos.get(e[2][0], [])) >= minlife]
B = [pct(e[2][0], e[0]) for e in d['events'] if e[1] == 'split' and len(e[3]) >= 2 and e[0] > 1000]
D = [x for x in D if x]; B = [x for x in B if x]
out = dict(file=sys.argv[1], key=key, minlife=minlife, n_death=len(D), death_pct_mean=round(float(np.mean([p for p, _ in D])), 3) if D else None,
           n_split=len(B), split_pct_mean=round(float(np.mean([p for p, _ in B])), 3) if B else None,
           death_pct_below_median=int(sum(p < 0.5 for p, _ in D)), split_pct_above_median=int(sum(p > 0.5 for p, _ in B)))
print(json.dumps(out))
