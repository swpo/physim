"""c19: independent re-implementation of c18's outside-supply cut (20261025T1703-c18-cog-gate-is-slow-diffusion).
Run world.py (lcn-cog with gates) from noise to t=600 on a seed, pick the most isolated cog (component of A0 > 0.3,
>= 20 px, farthest from any other), then from that state run arms for T_after with food removed every step in the
annulus 12 < r < 20 around it (c18's starve_disk mechanism): ungated (beta 0), gated (beta = betaW = 8) and uniformly
low diffusivity (D = DW = 0.0007, the gated value exp(-8*0.9)), plus an ungated fed twin. Records cog matter within
r < 12 (relative to the fork) and food within r < 6 every 25 t. usage: annulus.py world.py seed T_after out.json"""
import sys, json, importlib.util, numpy as np
from scipy import ndimage
wp, seed, Ta, out = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
spec = importlib.util.spec_from_file_location("w", wp); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
dt = w.META["dt"]; s = w.init(seed, w.META["size"])
for i in range(int(600 / dt)): s = w.step(s)
H, W = s["F"].shape; lab, n = ndimage.label(s["A"][0] > 0.3); area = np.bincount(lab.ravel())
cs = [ndimage.center_of_mass(lab == j) for j in range(1, n + 1) if area[j] >= 20]
def pd(a, b):
    dy = abs(a[0] - b[0]); dx = abs(a[1] - b[1]); return np.hypot(min(dy, H - dy), min(dx, W - dx))
iso = [min([pd(c, o) for o in cs if o is not c] or [1e9]) for c in cs]; k = int(np.argmax(iso)); cy, cx = cs[k]
yy, xx = np.mgrid[0:H, 0:W]; dy = np.minimum(abs(yy - cy), H - abs(yy - cy)); dx = np.minimum(abs(xx - cx), W - abs(xx - cx)); r = np.hypot(dy, dx)
ann = (r > 12) & (r < 20); inner = r < 12; core = r < 6
state = {k2: (v.copy() if isinstance(v, np.ndarray) else v) for k2, v in s.items() if k2 in ("A", "F", "W", "t", "N0")}
base = dict(w.P); res = {"seed": seed, "cog": [float(cy), float(cx)], "nearest_other_px": float(iso[k]), "n_cogs": len(cs), "arms": {}}
arms = {"fed_ungated": ({}, False), "cut_ungated": ({}, True), "cut_gated": ({"beta": 8.0, "betaW": 8.0}, True), "cut_lowD": ({"D": 0.0007, "DW": 0.0007}, True)}
for name, (pp, cut) in arms.items():
    w.P.clear(); w.P.update(base); w.P.update(pp)
    st = dict(s); st.update({k2: (v.copy() if isinstance(v, np.ndarray) else v) for k2, v in state.items()})
    if cut: st["_mask"] = ann; w.P["starve_disk"] = 1
    else: w.P["starve_disk"] = None
    m0 = st["A"][:, inner].sum(); rec = []
    for i in range(1, int(Ta / dt) + 1):
        st = w.step(st)
        if i % int(round(25 / dt)) == 0: rec.append([round(600 + i * dt, 1), round(float(st["A"][:, inner].sum() / m0), 4), round(float(st["F"][core].mean()), 4)])
    res["arms"][name] = rec; print(name, rec[-1], flush=True)
json.dump(res, open(out, "w"), indent=1)
