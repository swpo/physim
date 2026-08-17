import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np

def settle_and_kick(tc, seed=0, T1=18000, T2=25000, frac=0.6, mode="flip"):
    p = theory_to_raw(tc)
    rng = np.random.default_rng(seed)
    state = init_state(p, rng)
    step = make_stepper(p, rng)
    for t in range(T1):
        step(state)
    m0 = macro(state)
    V, E, R, W, A = state
    rec = (A < 0.5) & (V > 0.05)
    sel = rec & (rng.random(V.shape) < frac)
    if mode == "flip":
        A[sel] = 1.0 - A[sel]
    rec_fr = []
    for t in range(T2):
        step(state)
        if t % 25 == 0:
            rec_fr.append(macro(state)["fr_b"])
    return np.array(rec_fr), m0

tc = dict(rho=2.0, yW=0.8, leak=0.5, margin=3.0, sig_mut=0.05, over=0.3)
for hz, frac in [(7e-4, 0.6), (4e-4, 0.6), (7e-4, 0.9)]:
    t0 = time.time()
    fr, m0 = settle_and_kick(dict(tc, hazard=hz), frac=frac)
    fit = compact_top_fit(fr, dt=25)
    rt = relaxation_tau(fr, dt=25)
    print(f"hz={hz} frac={frac}: pre={m0['fr_b']:.3f} kick_start={fr[0]:.3f} end={fr[-1]:.3f} "
          f"fit={fit['model']} r2={fit['r2']} params={fit['params']} | relax tau={rt['tau']} r2={rt['r2']:.3f} ({time.time()-t0:.0f}s)")
    print("   traj:", [round(float(v),3) for v in fr[::50]])
