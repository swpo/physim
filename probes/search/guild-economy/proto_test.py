import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np

def smooth(x, k=9):
    return np.convolve(x, np.ones(k)/k, mode="valid")

def run_proto(tc, proto, seed=0, T1=20000, T2=24000):
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
    # perturbation
    if proto == "Wdump":
        W += 1.5
    elif proto == "Wdrain":
        W *= 0.05
    elif proto == "Rdrought":
        R *= 0.1
    step2 = step
    if proto == "rho_dn":
        step2 = make_stepper(theory_to_raw(dict(tc, rho=tc["rho"]*0.7)), rng)
    fr = []
    for t in range(T2):
        step2(state)
        if t % 25 == 0:
            fr.append(macro(state)["fr_b"])
    fr = np.array(fr)
    sm = smooth(fr)
    # fit from extremum (after fast demographic phase)
    n3 = len(sm) // 3
    i_ext = int(np.argmax(np.abs(sm[:n3] - fr_star)))
    fit = compact_top_fit(sm[i_ext:], dt=25)
    return dict(fr_star=round(fr_star,3), purity=round(m0["purity"],3),
                ext_at=i_ext*25,
                fr_ext=round(float(sm[i_ext]),3),
                fr_end=round(float(np.median(fr[-40:])),3),
                model=fit["model"], r2=fit["r2"],
                tau=round(fit["params"].get("tau",0),0) if fit["model"]=="relaxation" else None,
                traj=[round(float(v),3) for v in fr[::60]])

base = dict(rho=2.0, yW=0.8, leak=0.5, margin=3.0, sig_mut=0.05, over=0.3)
tests = [
    ("Wdump", base, "Wdump"),
    ("Wdrain", base, "Wdrain"),
    ("rho_dn x0.7", base, "rho_dn"),
    ("Wdump hz4e-4", dict(base, hazard=4e-4), "Wdump"),
]
for tag, tc, proto_name in tests:
    t0 = time.time()
    r = run_proto(tc, proto_name)
    print(f"== {tag} ({time.time()-t0:.0f}s)")
    print(json.dumps(r, default=float))
