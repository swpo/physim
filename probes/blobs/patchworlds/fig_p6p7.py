import os, sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
B = os.path.dirname(os.path.abspath(__file__))
res = json.load(open(os.path.join(B, "results.json")))
p6rows = [r for r in res if r.get("test") == "P6_seam_force"]
fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
ax = axes[0]
ds = [r["d_lu"] for r in p6rows]; vm = [-r["v_mid"] for r in p6rows]
ve = [-r["v_end"] for r in p6rows]
ax.plot(ds, vm, "ro-", label="|v| early (t=200-600)")
ax.plot(ds, ve, "bs-", label="|v| late (last 300 tu)")
W = 12.0
dd = np.linspace(2, 24, 60)
x0s = 24 - dd
pred = 0.40 * np.abs((1 / np.cosh((x0s - 24) / W) ** 2) / (2 * W)
                     - (1 / np.cosh((72 - x0s) / W) ** 2) / (2 * W))
ax.plot(dd, pred, "k--", lw=1, label="0.40*|drho/dx|")
ax.set_xlabel("distance from seam-1 (lu)"); ax.set_ylabel("expulsion speed (lu/tu)")
ax.set_title("P6: seam force on fresh static blob (w=12)")
ax.legend(fontsize=8)
ax = axes[1]
d7 = np.load(os.path.join(B, "data", "p7_taupatch.npz"))
ax.imshow(d7["kymo"], aspect="auto", origin="lower", cmap="magma",
          extent=[0, 96, 0, 2000])
ax.axvline(24, color="cyan", ls="--", lw=0.8); ax.axvline(72, color="cyan", ls="--", lw=0.8)
ax.set_title("P7: tau-only seam (Dv global): traveler PARKS")
ax.set_xlabel("x (lu)"); ax.set_ylabel("t (tu)")
ax = axes[2]
do_ = np.load(os.path.join(B, "data", "p2_w12_oblique.npz"))
pos, t = do_["pos"], do_["t"]
m = ~np.isnan(pos[:, 0, 1])
ax.plot(pos[m, 0, 1] % 96, pos[m, 0, 0] % 96, "r.-", ms=2, lw=0.5)
ax.axvline(24, color="c", ls="--"); ax.axvline(72, color="c", ls="--")
ax.annotate("kick 45deg from -x", xy=(46, 37), fontsize=8)
ax.set_xlim(0, 96); ax.set_ylim(30, 52)
ax.set_xlabel("x (lu)"); ax.set_ylabel("y (lu)")
ax.set_title("P2 oblique: refraction to NORMAL exit")
fig.tight_layout()
fig.savefig(os.path.join(B, "strips", "p6_p7_force_refraction.png"), dpi=110)
print("saved")
