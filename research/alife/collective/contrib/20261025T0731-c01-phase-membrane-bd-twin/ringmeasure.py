"""Per-cell L-ring measure for phase_membrane and its twin (c01).

python ringmeasure.py world.py seed T(time) out.json [key=val ...]   (key=val overrides world.P)
Every 1000 t from t=2000: cells = periodic components of phi > 1/2 with area >= 40 px.
For each cell, distance d from the wall inside the cell: rim = d <= 2 px, core = d >= 0.6 max(d)
(size-normalized; cells need max(d) >= 3.5 px).
ring = mean L(rim) / mean L(core); out = mean L within 2-5 px outside any cell.
Reports the median and quartiles of ring over cells, and mean L rim/out."""
import json
import sys

import numpy as np
from scipy import ndimage

sys.path.insert(0, ".")
from labkit.world import load_world  # noqa: E402

world, seed, T, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
W = load_world(world)
for kv in sys.argv[5:]:
    k, v = kv.split("=")
    W.P[k] = type(W.P[k])(float(v)) if not isinstance(W.P[k], str) else v
sc = float(W.P.get("scale", 1))
size = tuple(int(round(x * sc)) for x in W.META["size"])
s = W.init(seed, size)
rows = []
dt = float(W.P.get("dt", 1.0))
nper = int(round(1000 / dt))
for k in range(1, int(round(T / dt)) + 1):  # T in time units; census every 1000 t
    s = W.step(s)
    t = int(round(k * dt))
    if t >= 2000 and k % nper == 0:
        phi, L = s["phi"], s["L"]
        ins = phi > 0.5
        big = np.tile(ins, (3, 3))                      # periodic distance via tiling
        d_in = ndimage.distance_transform_edt(big)[ins.shape[0]:2 * ins.shape[0], ins.shape[1]:2 * ins.shape[1]]
        d_out = ndimage.distance_transform_edt(~big)[ins.shape[0]:2 * ins.shape[0], ins.shape[1]:2 * ins.shape[1]]
        lab, n = ndimage.label(ins)
        ratios, sizes = [], []
        for i in range(1, n + 1):
            c = lab == i
            if c.sum() < 40:
                continue
            dm = d_in[c].max()
            if dm < 3.5 * sc:
                continue
            rim, core = c & (d_in <= 2 * sc), c & (d_in >= 0.6 * dm)
            ratios.append(float(L[rim].mean() / max(L[core].mean(), 1e-9)))
            sizes.append(float(dm))
        outside = (d_out >= 2) & (d_out <= 5)
        rim_all = ins & (d_in <= 2)
        rows.append({"t": t, "cells": len(ratios), "ring_median": float(np.median(ratios)) if ratios else None,
                     "ring_q25_q75": [float(np.percentile(ratios, 25)), float(np.percentile(ratios, 75))] if ratios else None,
                     "median_inradius": float(np.median(sizes)) if sizes else None,
                     "rim_over_out": float(L[rim_all].mean() / max(L[outside].mean(), 1e-9))})
json.dump({"world": world, "seed": seed, "overrides": sys.argv[5:], "rows": rows}, open(out, "w"), indent=1)
print(json.dumps(rows[-1]))
