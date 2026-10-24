"""Mean prey-body speed per arm (centroids matched to the nearest body in the next recorded frame, t >= 300).

usage: python preyspeed.py pack_seed_dir [...]
"""
import json
import sys

import numpy as np
from scipy import ndimage

for d in sys.argv[1:]:
    Z = np.load(f"{d}/frames.npz")
    F = Z["render"].astype(np.float32)
    m = json.load(open(f"{d}/metrics.json"))
    tf = Z["render_f"] * m["steps_per_frame"] * m.get("dt", 0.05)
    P = F[:, 0] + F[:, 1]
    thr = 0.35 * P.max()
    H, W = P.shape[1:]
    cs = []
    for k in range(len(P)):
        lab, n = ndimage.label(P[k] > thr)
        cs.append(np.array(ndimage.center_of_mass(P[k], lab, range(1, n + 1))) if n else np.zeros((0, 2)))
    sp = []
    for k in range(len(P) - 1):
        if tf[k] < 300 or len(cs[k]) == 0 or len(cs[k + 1]) == 0:
            continue
        dd = np.abs(cs[k + 1][:, None] - cs[k][None])
        dd = np.minimum(dd, np.array([H, W]) - dd)
        r = np.sqrt((dd ** 2).sum(-1)).min(1)
        sp.extend(r[r < 15] / (tf[k + 1] - tf[k]))
    print(f"{d.split('/')[-1]}: prey body speed mean {np.mean(sp):.3f} px/t, median {np.median(sp):.3f} (n={len(sp)})")
