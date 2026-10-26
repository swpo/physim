"""ring.py's per-body signed-distance s-layer test applied to a pack's recorded render frames (frames.npz).
usage: python ring_frames.py PACKDIR DT_FRAME"""
import sys, json, numpy as np
from scipy import ndimage
pk, dtf = sys.argv[1], float(sys.argv[2])
Z = np.load(pk + "/frames.npz"); R = Z["render"].astype(np.float64); fr = Z["render_f"]
def measure(e, sv):
    H, W = e.shape; pad = 24
    E = np.pad(e, pad, mode="wrap"); S = np.pad(sv, pad, mode="wrap"); m = E > 0.5
    din = ndimage.distance_transform_edt(m); dout, (iy, ix) = ndimage.distance_transform_edt(~m, return_indices=True)
    lab, n = ndimage.label(m, structure=np.ones((3, 3))); near = lab[iy, ix]; res = []
    for i in range(1, n + 1):
        b = lab == i; cy, cx = ndimage.center_of_mass(b)
        if not (pad <= cy < pad + H and pad <= cx < pad + W): continue
        core = b & (din >= 3); rim = (b & (din <= 1.5)) | ((near == i) & (dout <= 1.5) & ~m)
        outs = (near == i) & (dout >= 4) & (dout <= 7)
        if core.sum() < 3 or outs.sum() < 3: continue
        res.append((float(S[rim].mean() / S[core].mean()), float(S[rim].mean() / S[outs].mean()), int(b.sum())))
    return res
tot = ok = 0; rc = []; ro = []; fails = []; skipped = 0
for k, f in enumerate(fr):
    if f == 0: continue
    r = measure(R[k, 0], R[k, 3])
    nb = ndimage.label(R[k, 0] > 0.5)[1]
    for x in r:
        tot += 1; rc.append(x[0]); ro.append(x[1])
        if x[0] >= 1.5 and x[1] >= 1.5: ok += 1
        else: fails.append((f * dtf, x))
out = {"frames": int(len(fr) - 1), "body_samples": tot, "pass": ok, "rim_core_min": min(rc), "rim_core_median": float(np.median(rc)),
       "rim_out_min": min(ro), "rim_out_median": float(np.median(ro)), "fails": fails[:20]}
json.dump(out, open(pk + "/ring_frames.json", "w"), indent=1); print(out)
