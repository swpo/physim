import os, sys, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BASE = os.path.dirname(os.path.abspath(__file__))
u0 = -0.7035399190279488

fig = plt.figure(figsize=(15, 5))

# (a) XVR portrait
ax = fig.add_subplot(1, 3, 1)
F = np.load(f"{BASE}/data/XVR_N6_wn_final.npz")["F"].astype(float)
comb = np.zeros_like(F[0])
ax.imshow(F[0] - u0, origin="lower", extent=[0, 96, 0, 96], cmap="Reds", vmin=0, vmax=1.9, alpha=0.95)
m2 = np.ma.masked_where(F[3] - u0 < 0.3, F[3] - u0)
ax.imshow(m2, origin="lower", extent=[0, 96, 0, 96], cmap="Blues", vmin=0, vmax=1.9, alpha=0.95)
ax.set_title("(a) BONUS: alternating A-B ring (12 blobs)\ncross-bond braced, 5000tu + noise")
ax.set_xticks([]); ax.set_yticks([])

# (b) R4 hammer: blob radial deviation vs cargo distance
ax = fig.add_subplot(1, 3, 2)
bins = [(15, 18), (18, 21), (21, 25), (25, 30), (30, 40)]
vals = [-0.01398, 0.00290, -0.00066, -0.00085, 0.00078]
ctr = [(lo + hi) / 2 for lo, hi in bins]
ax.bar(ctr, vals, width=[hi - lo - 0.4 for lo, hi in bins], color=["tab:red" if v < 0 else "tab:gray" for v in vals])
ax.axhline(0, color="k", lw=0.7)
ax.axhspan(-0.010, 0.010, color="gold", alpha=0.25, label="working-noise sigma band")
ax.set_xlabel("cargo-to-membrane-blob distance (px)")
ax.set_ylabel("mean blob radial deviation (px)")
ax.set_title("(b) R4 hammer (noiseless, eta21=0.01):\nsub-pixel PULL at close approach; NULL vs noise")
ax.legend(fontsize=8)

# (c) barrier curve final: V_w ridge vs etaw with outcomes
ax = fig.add_subplot(1, 3, 3)
etaws = np.array([0.2, 0.3, 0.4, 0.6, 0.7, 0.9, 1.0, 1.4])
ridge = 0.046 * etaws
ax.plot(etaws, ridge, "k-", lw=1, label="V_w(gap ridge) = 0.046 etaw")
# outcome markers for tau1=5.8
conf58 = {0.9: True, 1.0: True}
for w in etaws:
    ok = conf58.get(float(w), False)
    ax.scatter([w], [0.046 * w], marker="o" if ok else "x", s=90,
               c=("tab:green" if ok else "tab:red"), zorder=3)
ax.axvspan(1.05, 1.5, color="tab:red", alpha=0.15, label="nucleation zone (etaw>=1.05)")
ax.set_xlabel("etaw12 (membrane wall strength)")
ax.set_ylabel("gap-saddle barrier (k1-units)")
ax.set_title("(c) membrane operating window\ngreen=confines tau=5.8 cargo; red x=porous;\nshaded=interior vacuum nucleates")
ax.legend(fontsize=7)

fig.suptitle("R4 + bonus material: membrane response boundary and the alternating-species ring", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(f"{BASE}/strips/fig5_R4_and_xvr.png", dpi=110)
print("fig5 saved")
