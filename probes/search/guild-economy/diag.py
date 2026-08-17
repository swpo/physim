"""diag.py — instrumented single-candidate diagnosis.
Settle one candidate, then from the SAME settled state run 4 perturbation
protocols; record fr_b, fr_site, purity, Rm, Wm; plot + fit each.
"""
import sys, time, json, pickle
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
tc = dict(rho=1.8, yW=0.7, leak=0.55, margin=7.0, sig_mut=0.05, over=1.5,
          r0=0.006, hazard=7e-4)
p = theory_to_raw(tc)
rng = np.random.default_rng(0)
state = init_state(p, rng)
step = make_stepper(p, rng)
t0 = time.time()
for t in range(24000):
    step(state)
m0 = macro(state)
print(f"settled ({time.time()-t0:.0f}s): fr_b={m0['fr_b']:.3f} fr_site={m0['fr_site']:.3f} pur={m0['purity']:.3f}")
pickle.dump(state, open(WD + "/settled_A.pkl", "wb"))

def run_protocol(name, mutate, T2=30000, rho2=None):
    st = [x.copy() for x in state]
    rr = np.random.default_rng(4242)
    stp = make_stepper(theory_to_raw(dict(tc, rho=rho2)) if rho2 else p, rr)
    V, E, R, W, A = st
    mutate(st, rr)
    rows = {k: [] for k in ("t", "fr_b", "fr_site", "purity", "Rm", "Wm")}
    for t in range(T2):
        stp(st)
        if t % 25 == 0:
            m = macro(st)
            rows["t"].append(t)
            for k in ("fr_b", "fr_site", "purity", "Rm", "Wm"):
                rows[k].append(m[k])
    return {k: np.array(v) for k, v in rows.items()}

def kill_kick(st, rr):
    V, E, R, W, A = st
    rec = (A < 0.5) & (V > 0.05)
    sel = rec & (rr.random(V.shape) < 0.85)
    V[sel] = 0; E[sel] = 0

def flip_kick(st, rr):
    V, E, R, W, A = st
    rec = (A < 0.5) & (V > 0.05)
    sel = rec & (rr.random(V.shape) < 0.8)
    A[sel] = 1.0 - A[sel]

def dilute_kick(st, rr):
    V, E, R, W, A = st
    rec = (A < 0.5) & (V > 0.05)
    V[rec] *= 0.3; E[rec] *= 0.3

protos = [
    ("kill85", kill_kick, None),
    ("flip80", flip_kick, None),
    ("dilute30", dilute_kick, None),
    ("rho_step_2.6", lambda st, rr: None, 2.6),
]
results = {}
for name, mut, rho2 in protos:
    t0 = time.time()
    results[name] = run_protocol(name, mut, rho2=rho2)
    print(f"{name} done ({time.time()-t0:.0f}s)")

fig, axes = plt.subplots(2, 2, figsize=(13, 8))
for ax, (name, _, _) in zip(axes.flat, protos):
    r = results[name]
    ax.plot(r["t"], r["fr_b"], label="fr_b (biomass)", lw=1)
    ax.plot(r["t"], r["fr_site"], label="fr_site (territory)", lw=1)
    ax.axhline(m0["fr_b"], color="C0", ls=":", lw=0.8)
    ax.axhline(m0["fr_site"], color="C1", ls=":", lw=0.8)
    ax.set_title(name); ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig(WD + "/strips/diag_protocols.png", dpi=110)
print("saved diag_protocols.png")

def smooth(x, k=11):
    return np.convolve(x, np.ones(k)/k, mode="valid")
for name in results:
    r = results[name]
    for var in ("fr_b", "fr_site"):
        sm = smooth(r[var])
        fit = compact_top_fit(sm, dt=25)
        tau = fit["params"].get("tau")
        print(f"{name:14s} {var:8s}: {fit['model']:10s} r2={fit['r2']:.3f} "
              f"tau={round(tau) if tau else None} end={sm[-40:].mean():.3f}")
json.dump({name: {k: v.tolist() for k, v in r.items()} for name, r in results.items()},
          open(WD + "/diag_series.json", "w"))
