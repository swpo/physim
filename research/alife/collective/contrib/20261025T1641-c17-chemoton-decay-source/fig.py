"""Rows: no catalyst with the decay as coded; no catalyst with the decay clipped at u = -1; kb = 0.05 (catalyst dies out).
Amphiphile u+1 (grey, clipped to [0, 2]) at 7 times, with the body amphiphile held and the bath mean in each title."""
import numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
rows = [("no K, decay as coded", "noK/seed5/frames.npz", 1200), ("no K, decay clipped at u=-1", "noK_clip/seed5/frames.npz", 1200), ("kb=0.05 (K extinct by t~150)", "kb05/seed5/frames.npz", 600)]
fig, ax = plt.subplots(3, 7, figsize=(14, 6.6))
for r, (lab, p, T) in enumerate(rows):
    R = np.load(p)["render"]; n = len(R) - 1
    for c, i in enumerate(np.linspace(0, n, 7).astype(int)):
        u = R[i, 0]; b = ndimage.binary_dilation(u > 0.6, iterations=3)
        a = ax[r, c]; a.imshow(np.clip(u, 0, 2), cmap="gray", vmin=0, vmax=2); a.set_xticks([]); a.set_yticks([])
        a.set_title(f"{lab}\nt={i * T / n:.0f} body {u[b].sum():.0f}, bath {u[~b].mean():+.4f}", fontsize=6)
fig.suptitle("FCH chemoton seed 5: the linear decay -kap (u+1) feeds bodies from a bath that sits below u=-1", fontsize=9)
fig.tight_layout(); fig.savefig("decay_source.png", dpi=100)
