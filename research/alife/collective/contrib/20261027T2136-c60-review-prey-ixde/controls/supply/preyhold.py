"""Prey supply holds in c52's world: from a t=6000 state, fuel regrowth kF is held at frac * kF inside a fixed disk (r 12)
around one prey body, reached at once (ramp 0) or linearly over `ramp` t; F inside the disk is left as is.
Tracks the prey body by overlap. usage: preyhold.py STATE SEED cy cx frac ramp T OUT.json"""
import sys, json, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife'); sys.path.insert(0, '/home/user/physim/research/alife/collective/contrib/20261027T0325-c52-digestion-ecology-claim')
from scipy import ndimage
import world as w
st, seed, cy, cx, frac, ramp, T, out = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7]), sys.argv[8]
s = w.init(seed, (128, 128)); d = np.load(st)
for k in ["pa", "pb", "p", "F", "w", "q"]: s[k] = d[k].copy()
s["t"] = float(d["t"]); t0 = s["t"]; s["par"] = dict(s["par"]); dt = s["par"]["dt"]; H, W = s["shape"]
yy, xx = np.mgrid[0:H, 0:W]; dy = (yy - cy + H / 2) % H - H / 2; dx = (xx - cx + W / 2) % W - W / 2; disk = dy * dy + dx * dx <= 144
kmap = np.full((H, W), s["par"]["kF"]); s["par"]["kF"] = kmap; kF0 = w.P["kF"]
ca = w.fields(s)[0]; L, n = ndimage.label(ca > 0.5); m = L == L[int(cy), int(cx)]
rec = []
for i in range(int(round(T / dt)) + 1):
    if i % int(round(50 / dt)) == 0:
        el = s["t"] - t0; f = frac if ramp <= 0 else 1 - (1 - frac) * min(1.0, el / ramp)
        kmap[:] = kF0; kmap[disk] = f * kF0
        ca = w.fields(s)[0]; L, n = ndimage.label(ca > 0.5)
        if m.any():
            ov = L[m]; ov = ov[ov > 0]; m = (L == np.bincount(ov).argmax()) if ov.size else np.zeros_like(m)
        rec.append(dict(t=el, frac=f, area=int(m.sum()), n_prey=int(n)))
    if i < int(round(T / dt)): s = w.step(s)
json.dump(dict(cy=cy, cx=cx, frac=frac, ramp=ramp, rows=rec), open(out, "w"))
dead = [r["t"] for r in rec if r["area"] == 0]
print(out, "dead at", dead[0] if dead else None, "final area", rec[-1]["area"])
