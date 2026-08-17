
import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
import numpy as np
from sync_sim import simulate2
from sync_metrics import l4_analysis, counting_alive

base = dict(ny=8, nx=64, dx=1.0, dt=0.1, a=0.1, b=0.9, Du=1.0, Dv=11.0, Dc=10.0,
            sigma=1.0, kstar2=0.2682, eps1=3.2e-3, eps2=2.4e-3,
            steps=160000, meas_every=25, seed=1, noise_amp=2e-3)
for kc in [0.0, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2]:
    t0 = time.time()
    r = simulate2(dict(base, kappa_c=kc))
    el = time.time() - t0
    a = l4_analysis(r["t"], r["nz"][:, 0], r["nz"][:, 1])
    c1 = counting_alive(r["t"], r["nz"][:, 0])
    c2 = counting_alive(r["t"], r["nz"][:, 1])
    if a["status"] != "ok":
        print("kc=%.0e: %s (alive %s/%s) %.0fs" % (kc, a["status"], c1["alive"], c2["alive"], el))
        continue
    print("kc=%.0e: T1=%.0f T2=%.0f rho=%.3f net=%.2f exc=%.2f slips=%d T_slip=%s locked=%s alive=%s/%s (%.0fs)"
          % (kc, a["T1"], a["T2"], a["rho"], a["net_wind"], a["max_exc"],
             a["n_slips"], round(a["T_slip"],0) if a["T_slip"] else None,
             a["locked"], c1["alive"], c2["alive"], el), flush=True)
