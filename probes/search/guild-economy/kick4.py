import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np

def smooth(x, k=9):
    return np.convolve(x, np.ones(k)/k, mode="valid")

def flip_kick(tc, frac, seed=0, T1=22000, T2=24000):
    p = theory_to_raw(tc)
    rng = np.random.default_rng(seed)
    state = init_state(p, rng)
    step = make_stepper(p, rng)
    fr0 = []
    for t in range(T1):
        step(state)
        if t % 25 == 0:
            fr0.append(macro(state)["fr_b"])
    m0 = macro(state)
    fr_star = float(np.median(fr0[-160:]))
    V, E, R, W, A = state
    rec = (A < 0.5) & (V > 0.05)
    sel = rec & (rng.random(V.shape) < frac)
    A[sel] = 1.0 - A[sel]
    fr = []
    for t in range(T2):
        step(state)
        if t % 25 == 0:
            fr.append(macro(state)["fr_b"])
    fr = np.array(fr)
    sm = smooth(fr)
    fit = compact_top_fit(sm, dt=25)
    # extremum-anchored variant
    i_ext = int(np.argmin(sm[:len(sm)//3]))
    fit2 = compact_top_fit(sm[i_ext:], dt=25)
    return dict(fr_star=round(fr_star,3), fr_kick=round(float(fr[0]),3),
                fr_end=round(float(np.median(fr[-40:])),3),
                full=(fit["model"], fit["r2"], fit["params"].get("tau")),
                ext=(fit2["model"], fit2["r2"], fit2["params"].get("tau")),
                traj=[round(float(v),3) for v in fr[::60]])

base = dict(rho=2.0, yW=0.8, leak=0.5, margin=3.0, sig_mut=0.05, over=0.3)
for hz in (7e-4, 4e-4):
    for frac in (0.25, 0.4, 0.6):
        t0 = time.time()
        r = flip_kick(dict(base, hazard=hz), frac)
        tau_f = round(r["full"][2],0) if r["full"][2] else None
        tau_e = round(r["ext"][2],0) if r["ext"][2] else None
        print(f"hz={hz} frac={frac}: star={r['fr_star']} kick={r['fr_kick']} end={r['fr_end']} | "
              f"full={r['full'][0]},r2={r['full'][1]:.3f},tau={tau_f} | ext={r['ext'][0]},r2={r['ext'][1]:.3f},tau={tau_e} ({time.time()-t0:.0f}s)")
        print("   ", r["traj"])
