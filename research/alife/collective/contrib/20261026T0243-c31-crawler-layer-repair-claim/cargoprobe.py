"""Cargo retention across the layer: mean c inside (sd<-0.1) vs just outside (0.1<sd<0.4), by signed distance.
usage: WORLD_P=... python cargoprobe.py world2.py seed T out"""
import sys, json, importlib.util
import numpy as np
from scipy import ndimage
spec = importlib.util.spec_from_file_location("w", sys.argv[1]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
seed, T, out = int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
s = W.init(seed, W.META["size"]); L = W.P["L"]; dx = s["dx"]
rows = []; every = int(round(0.5 / W.P["dt"])); k = 0
while True:
    if k % every == 0:
        c, d = W.polarity(s); sh = (int(round((L/2 - c[1]) / dx)), int(round((L/2 - c[0]) / dx)))
        pc = np.roll(s["phi"], sh, (0, 1)); C = np.roll(s["c"], sh, (0, 1)); m = pc > 0.5
        sd = (ndimage.distance_transform_edt(~m) - ndimage.distance_transform_edt(m)) * dx
        y, x = np.mgrid[0:m.shape[0], 0:m.shape[1]] * dx; u = d / max(np.hypot(*d), 1e-9); proj = (x - L/2) * u[0] + (y - L/2) * u[1]
        ins = C[sd < -0.1].mean(); ou = C[(sd > 0.1) & (sd < 0.4)].mean()
        of = C[(sd > 0.1) & (sd < 0.4) & (proj > 0)].mean(); ob = C[(sd > 0.1) & (sd < 0.4) & (proj <= 0)].mean()
        held = C[sd < 0.06].sum() / max(C.sum(), 1e-12)
        r = dict(t=round(s["t"], 2), cin=float(ins), cout=float(ou), ratio=float(ins / max(ou, 1e-12)), ratio_front=float(ins / max(of, 1e-12)), ratio_back=float(ins / max(ob, 1e-12)), held=float(held), cx=float(c[0]), cy=float(c[1]))
        rows.append(r); print(" ".join(f"{a}={b:.3g}" for a, b in r.items()), flush=True)
        if k % (every * 4) == 0: np.savez_compressed(f"{out}_t{s['t']:.1f}.npz", phi=s["phi"], rho=s["c"], s=s["s"])
    if s["t"] >= T - 1e-9: break
    s = W.step(s); k += 1
json.dump(rows, open(out + ".json", "w"))
