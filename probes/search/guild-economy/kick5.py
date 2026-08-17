import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np

def smooth(x, k=9):
    return np.convolve(x, np.ones(k)/k, mode="valid")

def flip_kick_site(tc, frac=0.75, seed=0, T1=20000, T2=24000):
    p = theory_to_raw(tc)
    rng = np.random.default_rng(seed)
    state = init_state(p, rng)
    step = make_stepper(p, rng)
    fs0 = []
    for t in range(T1):
        step(state)
        if t % 25 == 0:
            fs0.append(macro(state)["fr_site"])
    m0 = macro(state)
    if m0["ncell"] < 400: return dict(fail="sparse")
    V, E, R, W, A = state
    bm = bimodality(A, V)
    fs_star = float(np.median(fs0[-160:]))
    rec = (A < 0.5) & (V > 0.05)
    sel = rec & (rng.random(V.shape) < frac)
    A[sel] = 1.0 - A[sel]
    fs, fb = [], []
    for t in range(T2):
        step(state)
        if t % 25 == 0:
            m = macro(state)
            fs.append(m["fr_site"]); fb.append(m["fr_b"])
    fs = np.array(fs); fb = np.array(fb)
    sm = smooth(fs)
    fit = compact_top_fit(sm, dt=25)
    return dict(purity=round(m0["purity"],3), bimod=round(bm["bimod"],2),
                shares=(round(bm["share_lo"],2), round(bm["share_hi"],2)),
                fs_star=round(fs_star,3), fs_kick=round(float(fs[0]),3),
                fs_end=round(float(np.median(fs[-40:])),3),
                model=fit["model"], r2=fit["r2"],
                tau=round(fit["params"].get("tau",0),0) if fit["model"]=="relaxation" else fit["params"],
                traj=[round(float(v),3) for v in fs[::60]])

base = dict(rho=2.0, yW=0.8, leak=0.5, margin=3.0, sig_mut=0.05, over=0.3)
for leak in (0.5, 0.7, 0.9):
    for hz in (7e-4,):
        t0 = time.time()
        r = flip_kick_site(dict(base, leak=leak, hazard=hz))
        print(f"leak={leak} hz={hz}: {json.dumps(r, default=float)} ({time.time()-t0:.0f}s)")
