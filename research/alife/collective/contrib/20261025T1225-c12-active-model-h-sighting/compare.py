"""Passive (zeta=0) vs active (zeta=-1) Model H from the same noise: phi at three times and droplet count
(components of phi > 0, >= 4 px) over time. usage: compare.py"""
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import ndimage
runs = {"passive zeta=0, seed 0": "pack_passive/frames.npz", "active zeta=-1, seed 0": "pack/seed0/frames.npz", "active zeta=-1, seed 1": "pack/seed1/frames.npz"}
fig, ax = plt.subplots(3, 4, figsize=(16, 12))
for r, (name, f) in enumerate(runs.items()):
    F = np.load(f); R = F["render"]; t = F["render_f"] * 250 * 0.05
    n = [ndimage.label(ndimage.binary_opening(R[i, 0] > 1.0))[1] for i in range(len(t))]
    for c, T in enumerate((750, 1250, 2000)):
        i = int(np.argmin(abs(t - T))); ax[r, c].imshow(R[i, 0] - 1, cmap="RdBu_r", vmin=-1.2, vmax=1.2); ax[r, c].set_title(f"{name}, t={t[i]:.0f}", fontsize=9); ax[r, c].axis("off")
    ax[r, 3].plot(t, n); ax[r, 3].set_xlabel("t"); ax[r, 3].set_ylabel("droplets"); ax[r, 3].set_title(f"droplets: {n[int(np.argmin(abs(t-750)))]} at t=750 -> {n[-1]} at t=2000", fontsize=9)
    print(name, "droplets t=750:", n[int(np.argmin(abs(t - 750)))], "t=2000:", n[-1])
plt.tight_layout(); plt.savefig("compare.png", dpi=60)
