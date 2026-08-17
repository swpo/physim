
"""t2_slipreg.py -- slip-point design probe BEFORE final metric lock:
does lower kinetic noise regularize slip timing (T_med ~ T_rate) and which
projection of Delta gives the best compact_top_fit? (sin vs cos vs frac)
"""
import sys, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
import numpy as np
from sync_sim import simulate2
from sync_metrics import l4_analysis
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from hier_metrics import compact_top_fit

BASE = dict(ny=8, nx=64, dx=1.0, dt=0.1, a=0.1, b=0.9, Du=1.0, Dv=11.0,
            Dc=10.0, sigma=1.0, kstar2=0.2682)
for R, noise in [(1.82, 2e-3), (1.82, 5e-4), (1.80, 5e-4), (1.85, 5e-4)]:
    eps_g = 2.4e-3
    p = dict(BASE, eps1=eps_g*np.sqrt(R), eps2=eps_g/np.sqrt(R), kappa_c=2e-3,
             steps=500000, meas_every=25, seed=1, noise_amp=noise)
    r = simulate2(p)
    a = l4_analysis(r["t"], r["nz"][:, 0], r["nz"][:, 1])
    if a["status"] != "ok":
        print("R=%.2f noise=%.0e: %s" % (R, noise, a["status"]), flush=True); continue
    dtt = float(a["delta_t"][1] - a["delta_t"][0])
    d = a["delta"]
    fits = {}
    for name, x in [("sin", np.sin(2*np.pi*d)), ("cos", np.cos(2*np.pi*d)),
                    ("frac", d % 1.0)]:
        ft = compact_top_fit(x, dt=dtt)
        fits[name] = (ft["model"], ft["r2"], ft["params"].get("n_flips") or ft["params"].get("n_cycles"))
    print("R=%.2f noise=%.0e: slips=%d T_med=%s T_rate=%s T3=%.0f rho=%.3f | fits: %s"
          % (R, noise, a["n_slips"], round(a["T_slip"],0) if a["T_slip"] else None,
             round(a["T_slip_rate"],0) if a["T_slip_rate"] else None,
             0.5*(a["T1"]+a["T2"]), a["rho"], fits), flush=True)
