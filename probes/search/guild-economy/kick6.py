import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"

def smooth(x, k=9):
    return np.convolve(x, np.ones(k)/k, mode="valid")

def kick_eval(tc, frac=0.75, seed=0, T1=20000, T2=24000, save=None):
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
    if m0["ncell"] < 3000:
        return dict(fail="sparse", ncell=m0["ncell"])
    V, E, R, W, A = state
    bm = bimodality(A, V)
    fr_star = float(np.median(fr0[-160:]))
    if save:
        from hier_metrics import save_strip
        save_strip([R, W, V, np.where(V>0.05, A, np.nan)], save,
                   titles=["R","W","V","alloc a"], cmap="viridis")
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
    return dict(purity=round(m0["purity"],3), bimod=round(bm["bimod"],2),
                shares=(round(bm["share_lo"],2), round(bm["share_hi"],2)),
                fr_star=round(fr_star,3), fr_kick=round(float(fr[0]),3),
                fr_end=round(float(np.median(fr[-40:])),3),
                model=fit["model"], r2=fit["r2"],
                tau=round(fit["params"].get("tau",0),0) if fit["model"]=="relaxation" else str(fit["params"]),
                all=fit["all"],
                traj=[round(float(v),3) for v in fr[::60]])

cands = [
    dict(rho=2.2, yW=0.7, leak=0.4, margin=6.0, sig_mut=0.05, over=1.5, r0=0.009),
    dict(rho=1.6, yW=0.7, leak=0.4, margin=8.0, sig_mut=0.05, over=1.5, r0=0.006),
    dict(rho=2.2, yW=0.7, leak=0.4, margin=8.0, sig_mut=0.05, over=1.5, r0=0.006),
]
for i, tc in enumerate(cands):
    t0 = time.time()
    r = kick_eval(tc, save=WD + f"/strips/scan1_cand{i}.png")
    print(f"cand{i} rho={tc['rho']} marg={tc['margin']} r0={tc['r0']}:")
    print("  ", json.dumps(r, default=float), f"({time.time()-t0:.0f}s)")
