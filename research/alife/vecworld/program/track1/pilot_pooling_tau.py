"""P0 follow-up: does the closure-optimal block feature approach the block sum as the target horizon grows?
Conservative ring (n = 64, D = 0.2), b = 8; optimise c(tau*) for tau* in (1, 4, 16, 64).
Run from this folder: /home/user/evalwork/vecworld/vw1/.venv/bin/python -B pilot_pooling_tau.py
"""
import json
import time

import numpy as np
from scipy.optimize import minimize

from pilot_pooling import Cw, certs, cos_to_uniform, system

A, Q, S = system("conservative", D=0.2, g=0.0)
b, out, t0 = 8, {}, time.time()
for ts in (1, 4, 16, 64):
    def neg(wv):
        wv = np.abs(wv) / (np.linalg.norm(wv) + 1e-15)  # positive windows (signed ones are far worse)
        return -certs(A, Q, S, Cw(wv), taus=(ts,))["ceiling"][0]
    best = None
    for x0 in (np.ones(b), np.hanning(b + 2)[1:-1]):
        r = minimize(neg, x0, method="Nelder-Mead", options={"maxiter": 1200, "xatol": 1e-5, "fatol": 1e-9})
        best = r if best is None or r.fun < best.fun else best
    w = np.abs(best.x) / np.linalg.norm(best.x)
    cu = certs(A, Q, S, Cw(np.ones(b)), taus=(ts,))["ceiling"][0]
    out[ts] = {"w": [round(v, 3) for v in w], "cos_to_uniform": round(cos_to_uniform(w), 4),
               "ceiling_opt": round(-best.fun, 5), "ceiling_uniform": round(cu, 5)}
    print(ts, out[ts], round(time.time() - t0, 1), flush=True)
json.dump({"b": b, "by_target_tau": out, "wall_seconds": round(time.time() - t0, 1)},
          open("/home/user/evalwork/vecworld/program/track1/pooling_tau.json", "w"), indent=1)
