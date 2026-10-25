"""Snapshots of the starve fork (starve.py npz): grey food F, blue core C (t=1), red core (t=3), orange membrane M, black bonds."""
import sys, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
pre, L, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
cols = {0: "0.7", 1: "tab:blue", 2: "tab:orange", 3: "tab:red"}
panels = [(a, arm, t) for a in ("b", "n") for arm, t in (("fed", 60), ("fed", 140), ("starve", 100), ("starve", 140))]
fig, ax = plt.subplots(2, 4, figsize=(16, 8))
for k, (a, arm, t) in enumerate(panels):
    x = ax.flat[k]; d = np.load(f"{pre}/{a}_{arm}_t{t}.npz"); X, T = d["x"], d["t"]
    for ty, c in cols.items():
        m = T == ty; x.scatter(X[m, 0], X[m, 1], s=1.5 if ty == 0 else 4, c=c)
    for B in (d["bA"], d["bB"]):
        for i, j in enumerate(B):
            if j > i:
                dd = X[j] - X[i]
                if np.abs(dd).max() < L / 2: x.plot([X[i, 0], X[j, 0]], [X[i, 1], X[j, 1]], "k-", lw=0.6)
    x.set_xlim(0, L); x.set_ylim(0, L); x.set_aspect("equal"); x.set_xticks([]); x.set_yticks([])
    x.set_title(f"{'bonds on' if a == 'b' else 'bonds off'}, {arm}, t={t}  (C {int(((T==1)|(T==3)).sum())}, M {int((T==2).sum())})", fontsize=9)
fig.suptitle("bondcell N=2000, seed 3: fork at t=60, starve = k_cat 0", fontsize=10); fig.tight_layout(); fig.savefig(out, dpi=70)
