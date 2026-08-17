
"""hysteresis.py -- measure the n(C) staircase with hysteresis for the
flagship pair, by slow triangle ramps of C (instrument mode). This is the
L3 compact law: jump-up positions C_up(n) vs jump-down positions C_dn(n).
"""
import sys, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
from morpho_sim import simulate

def loop(Dv, L, seed=1, P=8000.0, lo=0.62, hi=1.5):
    p = dict(ny=8, nx=L, dx=1.0, dt=0.1, a=0.1, b=0.9, Du=1.0, Dv=Dv, Dc=10.0,
             sigma=1.0, mode="ramp", ramp=(lo, hi, P, 20.0), C0=lo,
             steps=int(2 * P / 0.1), meas_every=25, seed=seed, k_ref=0.62,
             noise_amp=2e-3, Cmin=0.4, Cmax=1.9)
    r = simulate(p)
    t, n, C = r["t"], r["nz"].astype(int), r["Cm"]
    ph = (t % P) / P
    up = ph < 0.5
    jumps = []
    for i in range(1, len(n)):
        if n[i] != n[i - 1] and t[i] > 100:
            jumps.append({"t": float(t[i]), "C": round(float(C[i]), 4),
                          "from": int(n[i - 1]), "to": int(n[i]),
                          "dir": "up" if up[i] else "down"})
    return jumps

out = {}
for name, Dv, L in [("F48", 10.0, 48), ("F64", 11.0, 64)]:
    out[name] = {"Dv": Dv, "L": L, "seeds": {}}
    for seed in [1, 2, 3]:
        j = loop(Dv, L, seed=seed)
        out[name]["seeds"][seed] = j
        print(name, "seed", seed, flush=True)
        for e in j:
            print("   %s: n %d->%d at C=%.3f" % (e["dir"], e["from"], e["to"], e["C"]), flush=True)
with open("results_hysteresis.json", "w") as f:
    json.dump(out, f, indent=1)
print("hysteresis done")
