
"""t6_noise0.py -- is slip irregularity stochastic or deterministic?
R=1.85 kc=2e-3, noise in {1e-5, 5e-4, 2e-3}; record ALL slip intervals + CV.
(noise only seeds the initial pattern; the counter itself is deterministic.)
"""
import sys, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
import numpy as np
from sync_sim import simulate2
from sync_metrics import l4_analysis

BASE = dict(ny=8, nx=64, dx=1.0, dt=0.1, a=0.1, b=0.9, Du=1.0, Dv=11.0,
            Dc=10.0, sigma=1.0, kstar2=0.2682)
out = []
R, eps_g = 1.85, 2.4e-3
for noise in [1e-5, 5e-4, 2e-3]:
    p = dict(BASE, eps1=eps_g*np.sqrt(R), eps2=eps_g/np.sqrt(R), kappa_c=2e-3,
             steps=500000, meas_every=25, seed=1, noise_amp=noise)
    r = simulate2(p)
    a = l4_analysis(r["t"], r["nz"][:, 0], r["nz"][:, 1])
    if a["status"] != "ok":
        print("noise=%.0e: %s" % (noise, a["status"]), flush=True)
        continue
    # recompute slip times with the hysteretic counter (copy of metric)
    tt, d = a["delta_t"], a["delta"]
    ref = d[0]; slips = []
    for i in range(len(d)):
        if d[i] - ref >= 1.0: slips.append(tt[i]); ref += 1.0
        elif d[i] - ref <= -1.0: slips.append(tt[i]); ref -= 1.0
    iv = np.diff(slips)
    cv = float(iv.std()/iv.mean()) if len(iv) >= 2 else None
    row = dict(noise=noise, n_slips=len(slips), intervals=[round(float(x),1) for x in iv],
               cv=round(cv,3) if cv else None, rho=round(a["rho"],4))
    out.append(row)
    print(row, flush=True)
with open("results_noiseprobe.json", "w") as f:
    json.dump(out, f, indent=1)
print("t6 done", flush=True)
