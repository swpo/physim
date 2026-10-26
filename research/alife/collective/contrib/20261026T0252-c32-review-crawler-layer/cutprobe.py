"""Branch an undamaged twin at cut time, cut the other copy (front sector, in-world cut), log both.
usage: WORLD_P=... python cutprobe.py world.py seed t_cut T frac out_prefix"""
import sys, os, json, copy, importlib.util
import numpy as np
from scipy import ndimage
spec = importlib.util.spec_from_file_location("w", sys.argv[1]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
seed, tc, T, frac, out = int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
L = W.P["L"]
def layer(s):
    dx = s["dx"]; phi, S = s["phi"], s["s"]
    c, d = W.polarity(s)
    sh = (int(round((L/2 - c[1]) / dx)), int(round((L/2 - c[0]) / dx)))
    pc, Sc = np.roll(phi, sh, (0, 1)), np.roll(S, sh, (0, 1))
    m = pc > 0.5
    sd = (ndimage.distance_transform_edt(~m) - ndimage.distance_transform_edt(m)) * dx
    rim = np.abs(sd) < 0.06; core = sd < -0.3; outs = (sd > 0.3) & (sd < 0.8)
    r = Sc[rim].mean(); co = Sc[core].mean() if core.any() else np.nan; ou = Sc[outs].mean()
    # contour coverage: share of rim pixels with s above half the median rim value of a mature twin (0.07)
    cov = float((Sc[rim] > 0.07).mean())
    extra = {}
    if "c" in s:
        Cc = np.roll(s["c"], sh, (0, 1))
        ci = Cc[sd < -0.1].mean(); co_ = Cc[(sd > 0.1) & (sd < 0.4)].mean()
        extra = dict(cin=float(ci), cratio=float(ci / max(co_, 1e-12)), cheld=float(Cc[sd < 0.06].sum() / max(Cc.sum(), 1e-12)), ctot=float(Cc.sum() * dx * dx))
    return dict(**extra, t=round(s["t"], 2), area=float(m.sum() * dx * dx), pol=float(np.hypot(*d)), cx=float(c[0]), cy=float(c[1]),
                rim=float(r), core=float(co), out=float(ou), rim_core=float(r / max(co, 1e-9)), rim_out=float(r / max(ou, 1e-9)), cover=cov)
s = W.init(seed, W.META["size"]); dt = W.P["dt"]
while s["t"] < tc - 1e-9:
    s = W.step(s)
twin = copy.deepcopy(s); twin["rng"] = np.random.default_rng(seed + 1000); s["rng"] = np.random.default_rng(seed + 1000)
W.P["cut_frac"] = frac; W.P["cut_mode"] = "front"
s = W.cut(s)
info = dict(s["cut_info"]); info["s_lost"] = s.get("s_lost")
print("cut", info, flush=True)
rows = {"cut": [], "twin": [], "info": info}
every = int(round(0.25 / dt)); k = 0
while s["t"] < T - 1e-9:
    if k % every == 0:
        a, b = layer(s), layer(twin); rows["cut"].append(a); rows["twin"].append(b)
        print(f"t={a['t']:.2f} CUT A={a['area']:.2f} pol={a['pol']:.3f} rc={a['rim_core']:.2f} ro={a['rim_out']:.1f} cov={a['cover']:.2f} | TWIN A={b['area']:.2f} pol={b['pol']:.3f} rc={b['rim_core']:.2f} cov={b['cover']:.2f} | cargo cut {a.get('cratio',0):.1f}/{a.get('cheld',0):.2f}/{a.get('ctot',0):.3f} twin {b.get('cratio',0):.1f}/{b.get('cheld',0):.2f}/{b.get('ctot',0):.3f}", flush=True)
        if k % (every * 4) == 0:
            np.savez_compressed(f"{out}_cut_t{s['t']:.1f}.npz", phi=s["phi"], rho=s.get("c", s["rho"]), s=s["s"])
            np.savez_compressed(f"{out}_twin_t{s['t']:.1f}.npz", phi=twin["phi"], rho=twin.get("c", twin["rho"]), s=twin["s"])
    s = W.step(s); twin = W.step(twin); k += 1
json.dump(rows, open(out + ".json", "w"))
