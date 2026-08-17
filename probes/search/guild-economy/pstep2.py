"""pstep2.py — price-step protocol in the guild corner.
Settle at rho1, then STEP the waste price to rho2 (micro constant change,
experimenter protocol); the market relaxes to the new price-determined
equilibrium. Measure tau3 + r2 + new fr*. Also test flip-kick for contrast.
"""
import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np

def smooth(x, k=11):
    return np.convolve(x, np.ones(k)/k, mode="valid")

def settle(tc, seed=0, T1=22000):
    p = theory_to_raw(tc)
    rng = np.random.default_rng(seed)
    state = init_state(p, rng)
    step = make_stepper(p, rng)
    fr = []
    for t in range(T1):
        step(state)
        if t % 25 == 0:
            fr.append(macro(state)["fr_b"])
    return state, rng, float(np.median(fr[-160:])), macro(state)

def price_step(tc, state, rng, rho2, T2=26000):
    p2 = theory_to_raw(dict(tc, rho=rho2))
    step2 = make_stepper(p2, rng)
    fr = []
    for t in range(T2):
        step2(state)
        if t % 25 == 0:
            fr.append(macro(state)["fr_b"])
    fr = np.array(fr)
    sm = smooth(fr)
    fit = compact_top_fit(sm, dt=25)
    return dict(fr_end=round(float(np.median(fr[-40:])),3),
                model=fit["model"], r2=fit["r2"],
                tau=round(fit["params"].get("tau",0),0) if fit["model"]=="relaxation" else str(fit["params"]),
                traj=[round(float(v),3) for v in fr[::80]])

base = dict(rho=2.2, yW=0.7, leak=0.4, margin=8.0, sig_mut=0.05, over=1.5,
            r0=0.006, hazard=7e-4)
import copy
for hz in (7e-4, 1e-3):
    tc = dict(base, hazard=hz)
    t0 = time.time()
    st0, rng0, fr_star, m0 = settle(tc)
    print(f"hz={hz}: settled fr*={fr_star:.3f} pur={m0['purity']:.3f} ({time.time()-t0:.0f}s)")
    for rho2 in (1.8, 2.6):
        st = [x.copy() for x in st0]
        rr = np.random.default_rng(12345)
        t1 = time.time()
        r = price_step(tc, st, rr, rho2)
        print(f"  step rho 2.2->{rho2}: {json.dumps(r, default=float)} ({time.time()-t1:.0f}s)")
