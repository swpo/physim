import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np

for tag, tc in [
    ("A rho1.8 lk.55", dict(rho=1.8, yW=0.7, leak=0.55, margin=7.0, sig_mut=0.05, over=1.5, r0=0.006, hazard=7e-4)),
    ("B rho2.1 lk.65", dict(rho=2.1, yW=0.7, leak=0.65, margin=7.0, sig_mut=0.05, over=1.5, r0=0.006, hazard=7e-4)),
]:
    p = theory_to_raw(tc)
    rng = np.random.default_rng(0)
    state = init_state(p, rng)
    step = make_stepper(p, rng)
    t0 = time.time()
    marks = {}
    for t in range(46000):
        step(state)
        if t % 2000 == 1999:
            m = macro(state)
            marks[t+1] = (round(m["fr_site"],3), round(m["purity"],3))
    print(tag, f"({time.time()-t0:.0f}s)")
    for k in (6000, 12000, 18000, 24000, 30000, 36000, 42000, 46000):
        if k in marks: print("  t=%d fr_site=%.3f pur=%.3f" % (k, *marks[k]))
