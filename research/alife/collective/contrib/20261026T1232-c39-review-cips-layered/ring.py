"""Per-body s layer by signed distance to the e=0.5 contour, for EVERY body every DT_S time units.
rim = |distance| <= 1.5 px; core = >= 3 px inside; outside = 4-7 px outside and nearest to this body.
usage: python ring.py SEED T DT_S OUT   (WORLD_P overrides as usual)"""
import sys, json, importlib.util, os, numpy as np
from scipy import ndimage
seed, T, DS, out = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py"))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, w.META["size"]); H, W = s["shape"]
rows = []; nxt = DS
def measure(e, sv):
    pad = 24
    E = np.pad(e, pad, mode="wrap"); S = np.pad(sv, pad, mode="wrap"); m = E > 0.5
    din = ndimage.distance_transform_edt(m); dout, (iy, ix) = ndimage.distance_transform_edt(~m, return_indices=True)
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    near = lab[iy, ix]
    res = []
    for i in range(1, n + 1):
        b = lab == i
        cy, cx = ndimage.center_of_mass(b)
        if not (pad <= cy < pad + H and pad <= cx < pad + W): continue   # count each periodic body once
        core = b & (din >= 3); rim = (b & (din <= 1.5)) | ((near == i) & (dout <= 1.5) & ~m)
        outs = (near == i) & (dout >= 4) & (dout <= 7)
        if core.sum() < 3 or outs.sum() < 3: continue
        res.append((float(S[rim].mean() / S[core].mean()), float(S[rim].mean() / S[outs].mean()), int(b.sum())))
    return res
while s["t"] < T - 1e-9:
    w.step(s)
    if s["t"] >= nxt - 1e-9:
        r = measure(s["e"], s["s"]); nxt += DS
        ok = [x for x in r if x[0] >= 1.5 and x[1] >= 1.5]
        rows.append({"t": round(s["t"]), "bodies": len(r), "pass": len(ok),
                     "rim_core_min": min(x[0] for x in r) if r else None, "rim_core_median": float(np.median([x[0] for x in r])) if r else None,
                     "rim_out_min": min(x[1] for x in r) if r else None, "rim_out_median": float(np.median([x[1] for x in r])) if r else None})
        print(rows[-1], flush=True)
json.dump({"seed": seed, "params": os.environ.get("WORLD_P", "defaults"), "rows": rows}, open(out, "w"), indent=0)
