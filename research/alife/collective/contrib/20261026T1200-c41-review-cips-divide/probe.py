"""Run world_iso.py with WORLD_P overrides, log bodies (e>0.5, 8-connected, periodic-agnostic) and the principal-axis
angle (deg, 0 = x axis, 45 = grid diagonal) and aspect ratio of every body with aspect > 1.4, every `every` t; save snapshots.
usage: probe.py '<WORLD_P json>' T every tag [seed]"""
import os, sys, json, importlib.util, numpy as np
from scipy import ndimage as ndi
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
wp = json.loads(sys.argv[1]); T = float(sys.argv[2]); every = float(sys.argv[3]); tag = sys.argv[4]
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0
os.environ["WORLD_P"] = json.dumps(wp)
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("w", os.path.join(here, "world_iso.py")); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, w.META["size"])
def bodies(e):
    lab, n = ndi.label(e > 0.5, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        yy, xx = np.nonzero(lab == i)
        if len(yy) < 10: continue
        if np.ptp(yy) > e.shape[0] / 2 or np.ptp(xx) > e.shape[1] / 2:
            out.append((len(yy), None, None)); continue
        c = np.cov(np.vstack([xx, yy])); ev, evec = np.linalg.eigh(c)
        asp = np.sqrt(ev[1] / max(ev[0], 1e-9)); ang = np.degrees(np.arctan2(evec[1, 1], evec[0, 1])) % 180
        out.append((len(yy), round(float(asp), 2), round(float(ang))))
    return out
snaps = []; nxt = 0.0
while s["t"] <= T + 1e-9:
    if s["t"] >= nxt - 1e-9:
        b = bodies(s["e"])
        el = [(a, asp, ang) for a, asp, ang in b if asp and asp > 1.4]
        print(tag, "t=%d n=%d areas=%s elongated(area,asp,ang)=%s emin=%.3f emax=%.3f" % (s["t"], len(b), sorted([a for a, _, _ in b])[-6:], el, s["e"].min(), s["e"].max()), flush=True)
        snaps.append((s["t"], s["e"].copy())); nxt += every
    w.step(s)
k = np.linspace(0, len(snaps) - 1, min(8, len(snaps))).astype(int)
fig, ax = plt.subplots(1, len(k), figsize=(2.2 * len(k), 2.5))
for a, j in zip(np.atleast_1d(ax), k):
    a.imshow(snaps[j][1], cmap="magma", vmin=0, vmax=1); a.set_title("t=%.0f" % snaps[j][0], fontsize=8); a.axis("off")
fig.suptitle("%s %s seed %d" % (tag, json.dumps(wp), seed), fontsize=7); fig.tight_layout(); fig.savefig("probe_%s.png" % tag, dpi=70)
