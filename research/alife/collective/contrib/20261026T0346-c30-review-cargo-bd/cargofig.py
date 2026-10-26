"""Cargo field c with the phi=1/2 contour at t=2, 6, 10 for the three arms on seed 5 (from cargoprobe snapshots)."""
import os, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
H = os.path.dirname(os.path.abspath(__file__))
arms = [("kappa=10, D (world)", "k10_s5"), ("kappa=0, D", "k0_s5"), ("kappa=0, D/4", "k0D4_s5")]
ts = [2.0, 6.0, 10.0]
fig, ax = plt.subplots(len(arms), len(ts), figsize=(3.2 * len(ts), 3.2 * len(arms)))
for i, (lab, f) in enumerate(arms):
    for j, t in enumerate(ts):
        d = np.load(os.path.join(H, "runs", f"{f}_t{t:.1f}.npz")); a = ax[i, j]
        a.imshow(d["rho"], cmap="magma", vmin=0, vmax=0.4, origin="lower"); a.contour(d["phi"], [0.5], colors="c", linewidths=0.8)
        a.set_title(f"{lab}  t={t:.0f}", fontsize=8); a.set_xticks([]); a.set_yticks([])
plt.tight_layout(); plt.savefig(os.path.join(H, "cargo_s5.png"), dpi=70)
