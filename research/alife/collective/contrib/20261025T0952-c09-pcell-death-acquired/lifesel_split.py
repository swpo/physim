"""Death selection read at different points of each dying cell's life: yield percentile among living
cells at its first snapshot (birth), at mid-life, at 80% of life, and at its last snapshot. Also the
particle count trajectory (np) of dying cells. Under selection on an inherited trait, birth percentiles
of dying cells are already low; if they are ~0.5 at birth and drop only at the end, the low yield is
acquired during dying (within-cell erosion) rather than inherited."""
import sys, json, numpy as np
d = json.load(open(sys.argv[1])); S = d['series']; key = sys.argv[2] if len(sys.argv) > 2 else 'ym'
minlife = int(sys.argv[3]) if len(sys.argv) > 3 else 20
pos = {}
for a, x in enumerate(S):
    for i, cid in enumerate(x['id']):
        pos.setdefault(cid, []).append(a)
def pct_at(cid, a):
    x = S[a]; i = x['id'].index(cid); y = x[key][i]
    o = np.array([v for j, v in enumerate(x[key]) if j != i])
    return (np.sum(o < y) + 0.5 * np.sum(o == y)) / len(o), x['np'][i]
res = {f: [] for f in (0.0, 0.5, 0.8, 0.95, 1.0)}; nps = {f: [] for f in res}
for e in d['events']:
    if e[1] != 'split' or len(e[3]) < 2 or e[0] <= 1000: continue
    cid = e[2][0]; A = pos.get(cid, [])
    if len(A) < minlife: continue
    for f in res:
        a = A[min(len(A) - 1, int(round(f * (len(A) - 1))))]
        p, n = pct_at(cid, a); res[f].append(p); nps[f].append(n)
# reference: same for all cells alive at the end (survivors), at their first snapshot
print(json.dumps({"file": sys.argv[1], "key": key, "n_split": len(res[1.0]),
  "pct_mean_by_life_fraction": {str(f): round(float(np.mean(v)), 3) for f, v in res.items()},
  "share_below_median": {str(f): round(float(np.mean(np.array(v) < 0.5)), 2) for f, v in res.items()},
  "median_particles": {str(f): int(np.median(v)) for f, v in nps.items()}}))
