"""Figure for ports_check.py signed (lab env python: matplotlib). usage: plot_signed.py DIR"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

out = Path(sys.argv[1])
z = np.load(out / "signed_device0.npz")
z1 = np.load(out / "signed_device1.npz")
f = np.load(out / "signed_fields_50tu.npz")
fig, ax = plt.subplots(1, 4, figsize=(20, 4.6))
t = z["times"]
for k, c in (("sham", "0.4"), ("plus", "tab:red"), ("minus", "tab:blue")):
    ax[0].plot(t, z[f"{k}_device0"][0, :, 0, 0], color=c, label=f"{k}")
    ax[1].plot(t, z[f"{k}_global"][0, :, 0, 0] - z["sham_global"][0, :, 0, 0], color=c, label=f"{k} (pulse at device0)")
    ax[1].plot(t, z1[f"{k}_global"][0, :, 0, 0] - z1["sham_global"][0, :, 0, 0], color=c, ls="--", label=f"{k} (pulse at device1)")
ax[0].axhline(0, color="k", lw=0.5)
ax[0].set_xlabel("t (tu)"); ax[0].set_ylabel("vorticity at device0 centre node")
ax[0].set_title("amp 3 for 50 tu at device0, om gain 0.01"); ax[0].legend(fontsize=8)
ax[1].axhline(0, color="k", lw=0.5)
ax[1].set_xlabel("t (tu)"); ax[1].set_ylabel("global mean om minus sham"); ax[1].legend(fontsize=7)
c = f["centre"]
cy, cx = int(c[0]), int(c[1])
for i, k in enumerate(("sham", "minus")):
    a = np.roll(np.roll(f[k], 64 - cy, axis=0), 64 - cx, axis=1)
    im = ax[i + 2].imshow(a, cmap="RdBu_r", vmin=-0.35, vmax=0.35, origin="lower")
    ax[i + 2].plot(64, 64, "k+", ms=14, mew=2)
    ax[i + 2].set_title(f"om at t=50, {k} (recentred on device0, +)")
    fig.colorbar(im, ax=ax[i + 2], fraction=0.046)
fig.tight_layout()
fig.savefig(out / "signed_vortex.png", dpi=80)
