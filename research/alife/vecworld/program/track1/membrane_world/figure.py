"""figure -- results/pilot.png: phi snapshots with tracked cells (member 0, arm main) and level-2 traces per arm."""
import json
import os

import _paths
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

import membrane_world as MW  # noqa: E402

R = _paths.RESULTS
D = {a: np.load(os.path.join(R, f"pilot_{a}.npz")) for a in ("main", "dt025", "dt1", "det", "sa03")
     if os.path.exists(os.path.join(R, f"pilot_{a}.npz"))}
M = json.load(open(os.path.join(R, "pilot_main.json")))
K, H, TT = M["K"], M["H"], M["tick_time"]

fig, ax = plt.subplots(2, 3, figsize=(12, 7.6))
for i, t in enumerate((25, 100, 600)):
    a = ax[0, i]
    a.imshow(D["main"][f"phi_t{t}"], cmap="Greys_r", vmin=0, vmax=1, origin="lower")
    T = D["main"]["L1"][0, t, :K * 12].reshape(K, 12).astype(float)
    p = T[:, 0] > 0.5
    cx = (np.arctan2(T[p, 4], T[p, 3]) * H / (2 * np.pi)) % H
    cy = (np.arctan2(T[p, 6], T[p, 5]) * H / (2 * np.pi)) % H
    a.scatter(cx, cy, s=14, c="tab:cyan")
    a.set_title(f"phi, member 0, t = {t * TT:.0f}: {p.sum()} tracked cells", fontsize=9)
    a.set_xticks([]), a.set_yticks([])
cols = {"main": "k", "dt025": "tab:blue", "dt1": "tab:orange", "det": "tab:green", "sa03": "tab:purple"}
lab = {"main": "dt 0.5, sigma_a 0.01", "dt025": "dt 0.25", "dt1": "dt 1 (source)", "det": "sigma_a 0", "sa03": "sigma_a 0.03"}
t = np.arange(D["main"]["L2"].shape[1]) * TT
L2 = {arm: MW.level2_from_level1(z["L1"], K, TT) for arm, z in D.items()}   # the declared level 2, every arm
for j, (k, nm) in enumerate(((0, "cells N"), (1, "mean size (phi-area, px)"), (2, "divisions per cell per 100 t (50-tick window)"))):
    a = ax[1, j]
    for arm in D:
        a.plot(t, L2[arm][..., k].mean(0), color=cols[arm], lw=1.2 if arm == "main" else 0.9, label=lab[arm])
    a.set_xlabel("time (10 per tick)")
    a.set_title(nm + " (mean over 16 seeds)", fontsize=9)
ax[1, 0].legend(fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(R, "pilot.png"), dpi=80)
print("wrote", os.path.join(R, "pilot.png"))
