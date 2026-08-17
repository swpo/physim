import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np

idx = int(sys.argv[1])
cfgs = [
    (dict(rho=2.2, yW=0.7, leak=0.60, margin=7.0, sig_mut=0.05, over=1.5, r0=0.006,
          hazard=3e-4, DW=0.02, L=96, init="bimodal"), 0),
    (dict(rho=2.2, yW=0.7, leak=0.60, margin=7.0, sig_mut=0.05, over=1.5, r0=0.006,
          hazard=4.5e-4, DW=0.02, L=96, init="bimodal"), 0),
    (dict(rho=2.1, yW=0.7, leak=0.65, margin=7.0, sig_mut=0.05, over=1.5, r0=0.006,
          hazard=3e-4, DW=0.02, L=96, init="bimodal"), 0),
    (dict(rho=2.3, yW=0.7, leak=0.55, margin=7.0, sig_mut=0.05, over=1.5, r0=0.006,
          hazard=3e-4, DW=0.02, L=96, init="bimodal"), 0),
]
tc, seed = cfgs[idx]
p = theory_to_raw(tc)
rng = np.random.default_rng(seed)
state = init_state(p, rng)
step = make_stepper(p, rng)
t0 = time.time()
for t in range(40000):
    step(state)
    if t % 4000 == 3999:
        m = macro(state)
        print(f"t={t+1}: fr_site={m['fr_site']:.3f} pur={m['purity']:.3f} ncell={m['ncell']}", flush=True)
print(f"idx={idx} done {time.time()-t0:.0f}s")
