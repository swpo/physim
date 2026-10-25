"""Comet count, mean comet size and mean resource r over time for fed / graded / cut arms (labkit frames.npz:
channel 2 = firing f(u), channel 3 = resource r). usage: graded.py out.png label=dir ..."""
import sys, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out, runs = sys.argv[1], [a.split("=", 1) for a in sys.argv[2:]]
fig, ax = plt.subplots(1, 4, figsize=(18, 3.8))
for k, (lab, d) in enumerate(runs):
    F = np.load(d + "/frames.npz"); Rn, fr = F["render"], F["render_f"]; t = fr * 50 * 0.1
    n, sz, rm, rhi = [], [], [], []
    for i in range(len(Rn)):
        m = Rn[i, 2] > 0.5; lb, nn = ndimage.label(m)
        s = ndimage.sum(m, lb, range(1, nn + 1)) if nn else np.array([]); s = s[s >= 6]
        n.append(len(s)); sz.append(s.mean() if len(s) else np.nan); rm.append(Rn[i, 3].mean()); rhi.append((Rn[i, 3] > 0.8).mean())
    for a, y in zip(ax, (n, sz, rm, rhi)): a.plot(t, y, color=f"C{k}", label=lab)
    j = [np.argmin(abs(t - x)) for x in (500, 600, 750, 1000)]
    print(f"{lab}: comets t=500/600/750/1000 {[n[x] for x in j]}; mean size {[None if np.isnan(sz[x]) else round(float(sz[x]),1) for x in j]}; mean r {[round(float(rm[x]),3) for x in j]}; frac r>0.8 {[round(float(rhi[x]),3) for x in j]}")
for a, ttl in zip(ax, ["comets (>= 6 px firing)", "mean comet area (px)", "mean resource r", "fraction of domain with r > 0.8"]):
    a.axvline(500, color="k", lw=0.6, ls=":"); a.set_title(ttl, fontsize=9); a.set_xlabel("t")
ax[0].legend(fontsize=8); plt.suptitle("seed 24: regrowth of r normal (fed), slowed 2x / 4x, or stopped from t=500", fontsize=10)
plt.tight_layout(); plt.savefig(out, dpi=75)
