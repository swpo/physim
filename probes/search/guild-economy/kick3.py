import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np

def smooth(x, k=7):
    return np.convolve(x, np.ones(k)/k, mode="valid")

def protocol(tc, seed=0, T1=16000, T2=12000, frac=0.5):
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
    A[sel] = 1.0 - A[sel]
    fr = []
    for t in range(T2):
        step(state)
        if t % 25 == 0:
            fr.append(macro(state)["fr_b"])
    return np.array(fr), m0

tc = dict(rho=2.0, yW=0.8, leak=0.5, margin=3.0, sig_mut=0.05, over=0.3)
for frac in (0.3, 0.5, 0.75):
    t0 = time.time()
    fr, m0 = protocol(tc, frac=frac)
    frs = smooth(fr)
    fit = compact_top_fit(frs, dt=25)
    print(f"frac={frac}: pre={m0['fr_b']:.3f} start={fr[0]:.3f} end={fr[-1]:.3f} "
          f"fit={fit['model']} r2={fit['r2']} params={ {k: round(v,1) if isinstance(v,float) else v for k,v in fit['params'].items()} } ({time.time()-t0:.0f}s)")
