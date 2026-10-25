"""K2 biomass share and per-kind cell counts over time for membrane_evo arms (same seed = identical event RNG)."""
import sys, os, json, importlib.util, numpy as np
from scipy import ndimage
world, seed, T, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
spec = importlib.util.spec_from_file_location("w", world); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, (128, 128)); rec = []
for t in range(1, T + 1):
    s = w.step(s)
    if t % 1000 == 0:
        K1, K2 = s["K"], s["K2"]; lab, n = ndimage.label(s["phi"] > 0.5)
        k1 = ndimage.sum(K1, lab, range(1, n + 1)); k2 = ndimage.sum(K2, lab, range(1, n + 1))
        tot = K1.sum() + K2.sum()
        rec.append({"t": t, "K2_share": round(float(K2.sum() / tot), 3) if tot > 0 else None, "cells": int(n),
                    "cells_K2_major": int(np.sum(np.array(k2) > np.array(k1))), "cells_K1_major": int(np.sum(np.array(k1) >= np.array(k2)))})
ev = s.get("events", [])
types = {}
for e in ev: types[e[1]] = types.get(e[1], 0) + 1
json.dump({"world": world, "seed": seed, "T": T, "series": rec, "event_counts": types}, open(out, "w"))
print(world.split('/')[-2], seed, rec[-1], types)
