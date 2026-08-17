import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np

def smooth(x, k=9):
    return np.convolve(x, np.ones(k)/k, mode="valid")

def run_one(tc, seed=0, T1=22000, T2=16000, frac=0.7):
    p = theory_to_raw(tc)
    rng = np.random.default_rng(seed)
    state = init_state(p, rng)
    step = make_stepper(p, rng)
    blocks = []
    for t in range(T1):
        step(state)
        if t >= T1 - 6000 and t % 20 == 0:
            blocks.append(block_series(state, p["L"]))
    m0 = macro(state)
    if m0["ncell"] < 400:
        return dict(fail="sparse", ncell=m0["ncell"])
    V, E, R, W, A = state
    bm = bimodality(A, V)
    bt = block_tau(blocks, 20)
    t1R = impulse_tau(p, state, "R", seed)
    t1W = impulse_tau(p, state, "W", seed)
    rec = (A < 0.5) & (V > 0.05)
    sel = rec & (rng.random(V.shape) < frac)
    A[sel] = 1.0 - A[sel]
    fr = []
    for t in range(T2):
        step(state)
        if t % 25 == 0:
            fr.append(macro(state)["fr_b"])
    fr = np.array(fr)
    fit = compact_top_fit(smooth(fr), dt=25)
    tau3 = fit["params"].get("tau") if fit["model"] == "relaxation" else None
    return dict(purity=round(m0["purity"],3), bimod=round(bm["bimod"],2),
                shares=(round(bm["share_lo"],2), round(bm["share_hi"],2)),
                bt=bt, t1=(t1R, t1W), model=fit["model"], r2=fit["r2"],
                tau3=round(tau3,0) if tau3 else None,
                s12=round(bt/max(t1R or 1, t1W or 1),1) if bt else None,
                s23=round(tau3/bt,1) if (tau3 and bt) else None,
                fr0=round(float(fr[0]),3), frend=round(float(np.median(fr[-40:])),3))

base = dict(rho=2.0, yW=0.8, leak=0.5, margin=3.0, sig_mut=0.05, over=0.3)
variants = [
    ("base", base),
    ("leak=1.2", dict(base, leak=1.2)),
    ("cap=0.30", dict(base, cap=0.30)),
    ("gate=1.0", dict(base, gate=1.0)),
    ("hz=1.5e-3", dict(base, hazard=1.5e-3)),
    ("hz=1.5e-3+cap.3", dict(base, hazard=1.5e-3, cap=0.30)),
    ("leak1.2+cap.3", dict(base, leak=1.2, cap=0.30)),
    ("sig=0.02", dict(base, sig_mut=0.02)),
]
for tag, tc in variants:
    t0 = time.time()
    r = run_one(tc)
    print(f"{tag:18s} {json.dumps(r, default=float)} ({time.time()-t0:.0f}s)")
