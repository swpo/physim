"""Crops of phi around the first N peak births after t=100 (births as in births.py), 8 snapshots from 8 t before to 20 t after."""
import sys, os, json, importlib.util, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import ndimage
os.environ["WORLD_P"] = sys.argv[1]; T = int(sys.argv[2]); N = int(sys.argv[3]); out = sys.argv[4]
spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(0, (128, 128)); hist = []; prev = None; ev = []
def peaks(p):
    return np.argwhere((p == ndimage.maximum_filter(p, size=7, mode="wrap")) & (p > 0.0))
def dmin(a, B):
    d = np.abs(B - a); d = np.minimum(d, 128 - d); return np.hypot(d[:, 0], d[:, 1]).min() if len(B) else 1e9
for n in range(1, T + 1):
    w.step(s)
    if n % 20 == 0:
        hist.append((n * w.P["dt"], s["phi"].copy()))
        pk = peaks(s["phi"])
        if prev is not None and n * w.P["dt"] > 100 and len(ev) < N:
            for a in pk:
                if dmin(a, prev) > 3 and len(ev) < N: ev.append((len(hist) - 1, a))
        prev = pk
offs = [-4, -2, -1, 0, 1, 3, 6, 10]
fig, ax = plt.subplots(len(ev), len(offs), figsize=(2 * len(offs), 2.1 * len(ev)), squeeze=False)
for r, (i, (y, x)) in enumerate(ev):
    for j, o in enumerate(offs):
        k = min(max(i + o, 0), len(hist) - 1); t, ph = hist[k]
        crop = np.roll(np.roll(ph, 64 - y, 0), 64 - x, 1)[44:84, 44:84]
        ax[r, j].imshow(crop, cmap="magma", vmin=-1.6, vmax=1.0); ax[r, j].axis("off"); ax[r, j].set_title(f"t={t:.0f}", fontsize=8)
        if o == 0: ax[r, j].plot(20, 20, "c+", ms=10)
fig.suptitle("peak births (cyan + = new peak, frame of first detection), phi in a fixed 40x40 window", fontsize=9)
fig.tight_layout(); fig.savefig(out, dpi=70)
