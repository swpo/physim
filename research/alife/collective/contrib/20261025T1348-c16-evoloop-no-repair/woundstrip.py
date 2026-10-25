"""Visual wound test: same candidates as wound.py (seed-permuted side-`side` loops at t_a); for the first `n` loops,
remove k random core cells and show wounded vs twin crops at +0, +60, +150, +300 steps."""
import sys, os, json, importlib.util, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from evo_track import holes
COL = np.array([[0,0,0],[0,0,255],[255,0,0],[0,255,0],[255,255,0],[255,0,255],[255,255,255],[0,255,255],[255,128,0]])/255
params, seed, L, ta, side, n, k, out = json.loads(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), sys.argv[8]
os.environ["WORLD_P"] = json.dumps(params)
spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, (L, L))
for t in range(ta): w.step(s)
g0 = s["g"].copy(); lab, ids, area = holes(g0)
cand = [h for h in ids if round(np.sqrt(area[h])) == side]
rng = np.random.default_rng(seed); cand = [cand[i] for i in rng.permutation(len(cand))]
offs = [0, 60, 150, 300]; rows = []
for h in cand:
    ii, jj = np.nonzero(lab == h)
    if ii.max() - ii.min() > L / 2 or jj.max() - jj.min() > L / 2: continue
    i0, i1, j0, j1 = ii.min() - 3, ii.max() + 4, jj.min() - 3, jj.max() + 4
    box = (slice(max(i0, 0), min(i1, L)), slice(max(j0, 0), min(j1, L)))
    ga = g0.copy(); sub = ga[box]; ci, cj = np.nonzero(sub == 1); kk = rng.permutation(len(ci))[:k]; sub[ci[kk], cj[kk]] = 0; ga[box] = sub
    c = (int(ii.mean()), int(jj.mean())); R = int(1.6 * (ii.max() - ii.min()) + 8)
    crops = {}
    for name, g in (("twin", g0), ("wounded", ga)):
        st = dict(s); st["g"] = g.copy()
        for t in range(max(offs) + 1):
            if t in offs: crops[(name, t)] = st["g"][np.ix_((c[0] + np.arange(-R, R)) % L, (c[1] + np.arange(-R, R)) % L)].copy()
            w.step(st)
    rows.append(crops)
    if len(rows) == n: break
fig, ax = plt.subplots(2 * n, len(offs), figsize=(2.2 * len(offs), 2.3 * 2 * n))
for r, crops in enumerate(rows):
    for a, name in enumerate(("twin", "wounded")):
        for j, t in enumerate(offs):
            x = ax[2 * r + a, j]; x.imshow(COL[crops[(name, t)]], interpolation='nearest'); x.set_xticks([]); x.set_yticks([])
            x.set_title(f"loop {r + 1} {name} +{t}", fontsize=7)
fig.suptitle(f"evoloop {params or 'm=15'} seed {seed}: side-{side} loops at t={ta}, {k} core cells removed (wounded) vs untouched twin", fontsize=8)
plt.tight_layout(rect=(0, 0, 1, 0.98)); plt.savefig(out, dpi=75)
