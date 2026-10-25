"""Erase-and-refill and Boltzmann check for the FCH uptake world.
Run seed to T0, then (arm 'erase') set the solute to its uniform background kp0/kd everywhere, or (arm 'keep') leave it;
run on and, every 10 t, report per-body solute contrast (mean c in body / mean c far outside) and the Boltzmann
prediction exp(-chi (u_body - u_out)) averaged over each body. usage: refill.py seed T0 Tafter out.json"""
import sys, json, importlib.util, numpy as np
from scipy import ndimage
seed, T0, Ta, out = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
P = w.P; dt = P["dt"]
s = w.init(seed, w.META["size"])
for _ in range(int(T0 / dt)): w.step(s)
def measure(s, t):
    u, c = s["u"], s["c"]; body = (u - P["u_bg"]) > 0.8
    lab, n = ndimage.label(body); far = ~ndimage.binary_dilation(body, iterations=3)
    cout, uout = c[far].mean(), u[far].mean()
    ids = range(1, n + 1)
    per = np.array(ndimage.mean(c, lab, ids)) / cout
    pred = np.array(ndimage.mean(np.exp(-P["chi"] * (u - uout)), lab, ids))
    area = np.array(ndimage.sum(np.ones_like(u), lab, ids))
    k = area >= 10
    return {"t": t, "n": int(k.sum()), "median_contrast": float(np.median(per[k])), "min_contrast": float(per[k].min()),
            "frac_ge2": float(np.mean(per[k] >= 2)), "median_boltzmann": float(np.median(pred[k])),
            "median_ratio_measured_over_boltzmann": float(np.median(per[k] / pred[k]))}
res = {}
snap = {k: (v.copy() if hasattr(v, "copy") else v) for k, v in s.items()}
for arm in ("keep", "erase"):
    s = {k: (v.copy() if hasattr(v, "copy") else v) for k, v in snap.items()}
    if arm == "erase":
        s["c"][:] = P["kp0"] / P["kd"]
    rec = [measure(s, T0)]
    for i in range(1, int(Ta / dt) + 1):
        w.step(s)
        if i % int(10 / dt) == 0: rec.append(measure(s, T0 + i * dt))
    res[arm] = rec
    print(arm, [(r["t"], round(r["median_contrast"], 1), round(r["median_boltzmann"], 1), r["frac_ge2"]) for r in rec[::2]], flush=True)
json.dump(res, open(out, "w"), indent=1)
