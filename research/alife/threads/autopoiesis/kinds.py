"""Per-kind cell counts from a phase_kinds pack: cells = components of (K1+K2) > 0.05,
kind = dominant catalyst. python kinds.py PACK_DIR [PACK_DIR ...] -> PACK_DIR/kinds.png"""
import sys, json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import ndimage
for pack in sys.argv[1:]:
    z = np.load(pack + "/frames.npz"); R = z["render"].astype(np.float32); rf = z["render_f"]
    meta = json.load(open(pack + "/metrics.json")); dtf = meta["steps_per_frame"] * meta["world"]["dt"]
    n1, n2, mixed = [], [], []
    for F in R:
        k1, k2 = F[1], F[2]
        lab, n = ndimage.label(k1 + k2 > 0.05)
        if n == 0:
            n1.append(0); n2.append(0); mixed.append(0); continue
        a = ndimage.sum(k1, lab, np.arange(1, n + 1)); b = ndimage.sum(k2, lab, np.arange(1, n + 1))
        area = ndimage.sum(np.ones_like(k1), lab, np.arange(1, n + 1)); ok = area >= 6
        fr = b / np.maximum(a + b, 1e-9)
        n1.append(int((ok & (fr < 0.2)).sum())); n2.append(int((ok & (fr > 0.8)).sum())); mixed.append(int((ok & (fr >= 0.2) & (fr <= 0.8)).sum()))
    t = rf * dtf
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.plot(t, n1, label="K1 cells (>80% K1)", color="tab:orange"); ax.plot(t, n2, label="K2 cells (>80% K2)", color="tab:purple")
    ax.plot(t, mixed, label="mixed", color="0.5", ls="--"); ax.set_xlabel("time"); ax.set_ylabel("cells"); ax.legend(fontsize=8)
    ax.set_title(pack.rstrip("/").split("/")[-2] + "/" + pack.rstrip("/").split("/")[-1]); fig.tight_layout(); fig.savefig(pack + "/kinds.png", dpi=80)
    print(pack, "final K1/K2/mixed", n1[-1], n2[-1], mixed[-1], "max K2", max(n2))
