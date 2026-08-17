"""longrun.py — instrumented 72k-tick free runs; is the equilibrium reachable
within budget, and what does the settle trajectory look like?"""
import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
which = int(sys.argv[1])
cands = [
    ("A", dict(rho=1.8, yW=0.7, leak=0.55, margin=7.0, sig_mut=0.035, over=1.5, r0=0.006, hazard=7e-4)),
    ("B", dict(rho=2.1, yW=0.7, leak=0.65, margin=7.0, sig_mut=0.035, over=1.5, r0=0.006, hazard=7e-4)),
    ("C", dict(rho=2.1, yW=0.7, leak=0.65, margin=7.0, sig_mut=0.035, over=1.5, r0=0.006, hazard=5e-4)),
    ("D", dict(rho=1.8, yW=0.7, leak=0.55, margin=7.0, sig_mut=0.05, over=1.5, r0=0.006, hazard=7e-4)),
]
tag, tc = cands[which]
p = theory_to_raw(tc)
rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv) > 2 else 0)
state = init_state(p, rng)
step = make_stepper(p, rng)
rows = {k: [] for k in ("t", "fr_site", "fr_b", "purity", "Wm", "Rm")}
t0 = time.time()
for t in range(72000):
    step(state)
    if t % 50 == 0:
        m = macro(state)
        rows["t"].append(t)
        for k in ("fr_site", "fr_b", "purity", "Wm", "Rm"):
            rows[k].append(m[k])
json.dump(rows, open(WD + f"/longrun_{tag}.json", "w"))
fs = np.array(rows["fr_site"]); ts = np.array(rows["t"])
for tmark in (20000, 30000, 40000, 50000, 60000, 70000):
    i = np.searchsorted(ts, tmark)
    print(f"t={tmark}: fr_site={np.median(fs[max(0,i-20):i+20]):.3f}", flush=True)
print(f"{tag} done {time.time()-t0:.0f}s")
