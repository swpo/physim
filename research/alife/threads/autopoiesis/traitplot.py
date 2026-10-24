"""Trait trajectories from phase_trait packs: K-weighted mean c and per-cell 10/90% bands.
python traitplot.py OUT.png PACK_SEED_DIR [...]"""
import sys, json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import ndimage
fig, ax = plt.subplots(figsize=(8, 4))
for i, pack in enumerate(sys.argv[2:]):
    z = np.load(pack + "/frames.npz"); R = z["render"].astype(np.float32); rf = z["render_f"]
    meta = json.load(open(pack + "/metrics.json")); t = rf * meta["steps_per_frame"] * meta["world"]["dt"]
    mean, lo, hi = [], [], []
    for F in R:
        K, c = F[1], F[2] * 0.6
        m = K > 0.05
        mean.append((c * K)[m].sum() / max(K[m].sum(), 1e-9))
        lab, n = ndimage.label(m)
        if n:
            ck = ndimage.sum(c * K, lab, np.arange(1, n + 1)) / np.maximum(ndimage.sum(K, lab, np.arange(1, n + 1)), 1e-9)
            lo.append(np.percentile(ck, 10)); hi.append(np.percentile(ck, 90))
        else:
            lo.append(np.nan); hi.append(np.nan)
    col = "tab:blue" if "c20" not in pack else "tab:red"
    name = pack.rstrip("/").split("/")[-2] + "/" + pack.rstrip("/").split("/")[-1]
    ax.plot(t, mean, color=col, lw=1.5, label=name)
    ax.fill_between(t, lo, hi, color=col, alpha=0.08)
    print(name, "c_mean start/end", round(mean[0], 3), round(mean[-1], 3))
ax.set_xlabel("time"); ax.set_ylabel("catalyst trait c (K-weighted mean; band = cells 10-90%)")
ax.legend(fontsize=7); ax.set_title("phase_trait: two ancestral traits, 3 seeds each")
fig.tight_layout(); fig.savefig(sys.argv[1], dpi=80)
