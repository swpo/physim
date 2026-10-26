"""Planted-spot probe for the SH delay map: optional asymmetric kick (u += kick * du/dx) to seed the
translation (Goldstone) mode, centroid displacement of the brightest spot, spot count, snapshots."""
import os, sys, json, importlib.util, numpy as np
from scipy import ndimage as ndi
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
wp = json.loads(sys.argv[1]); T = float(sys.argv[2]); kick = float(sys.argv[3]); tag = sys.argv[4]
os.environ["WORLD_P"] = json.dumps(wp)
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py")); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(0, w.META["size"])
dx = w.P["L"] / w.P["N"]
s["u"] = s["u"] + kick * np.gradient(s["u"], axis=1) / dx
if w.P["PYR"]: s["v"] = s["u"].copy()
def peak(u): return np.array(np.unravel_index(np.argmax(ndi.gaussian_filter(u, 1.0, mode="wrap")), u.shape)) * dx
c0 = peak(s["u"]); rows = []; snaps = []
nsteps = int(round(T / w.P["dt"])); every = max(1, nsteps // 12)
for i in range(nsteps):
    s = w.step(s)
    if (i + 1) % every == 0:
        u = s["u"]; n = ndi.label(ndi.gaussian_filter(u, 1.5, mode="wrap") > 0.4)[1]
        d = (peak(u) - c0 + w.P["L"] / 2) % w.P["L"] - w.P["L"] / 2
        rows.append("t=%d n=%d disp=%.1f umax=%.2f" % (round(s["t"]), n, np.hypot(*d) if n else -1, u.max()))
        snaps.append((s["t"], u.copy()))
print(tag, json.dumps({k: wp[k] for k in ("kap", "tau", "r", "PYR") if k in wp}), "kick", kick, "|", "; ".join(rows), flush=True)
fig, ax = plt.subplots(1, 6, figsize=(15, 2.8))
for a, (t, u) in zip(ax, snaps[1::2]):
    a.imshow(u, cmap="magma", vmin=-0.5, vmax=2.0); a.set_title("t=%.0f" % t, fontsize=8); a.axis("off")
fig.suptitle("%s  %s kick=%g" % (tag, json.dumps(wp), kick), fontsize=8); plt.tight_layout(); plt.savefig("snap_%s.png" % tag, dpi=60)
