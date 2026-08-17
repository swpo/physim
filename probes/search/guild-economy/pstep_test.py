import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np

def smooth(x, k=9):
    return np.convolve(x, np.ones(k)/k, mode="valid")

def price_step(tc, rho2, seed=0, T1=20000, T2=20000):
    p = theory_to_raw(tc)
    rng = np.random.default_rng(seed)
    state = init_state(p, rng)
    step = make_stepper(p, rng)
    fr1 = []
    for t in range(T1):
        step(state)
        if t % 25 == 0:
            fr1.append(macro(state)["fr_b"])
    m0 = macro(state)
    if m0["ncell"] < 400:
        return None
    fr1_star = float(np.median(fr1[-160:]))
    p2 = theory_to_raw(dict(tc, rho=rho2))
    step2 = make_stepper(p2, rng)
    fr2 = []
    for t in range(T2):
        step2(state)
        if t % 25 == 0:
            fr2.append(macro(state)["fr_b"])
    fr2 = np.array(fr2)
    sm = smooth(fr2)
    fit = compact_top_fit(sm, dt=25)
    return dict(fr1_star=round(fr1_star,3), fr2_end=round(float(np.median(fr2[-40:])),3),
                model=fit["model"], r2=fit["r2"],
                params={k: round(v,1) if isinstance(v,float) else v for k,v in fit["params"].items()},
                all=fit["all"], traj=[round(float(v),3) for v in fr2[::50]])

base = dict(rho=2.0, yW=0.8, leak=0.5, margin=3.0, sig_mut=0.05, over=0.3)
tests = [
    ("rho 2.0->3.0", base, 3.0),
    ("rho 2.0->1.4", base, 1.4),
    ("rho 2.0->3.0 r0=8e-3", dict(base, r0=0.008), 3.0),
    ("rho 2.0->3.0 hz=4e-4", dict(base, hazard=4e-4), 3.0),
]
for tag, tc, rho2 in tests:
    t0 = time.time()
    r = price_step(tc, rho2)
    print(f"== {tag} ({time.time()-t0:.0f}s)")
    print(json.dumps(r, default=float))
