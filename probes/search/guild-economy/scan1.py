"""scan1.py — guild-region scan (settle-only) over theory coords.
Goal: find (over, margin, rho, r0, leak, yW) with BIMODAL guilds at SLACK
(space-saturated) so that market adjustment is turnover-limited.
Logs every candidate to results_scan1.jsonl.
"""
import sys, time, json, itertools
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
out_f = open(WD + "/results_scan1.jsonl", "a")

def settle_eval(tc, seed=0, T=18000):
    p = theory_to_raw(tc)
    rng = np.random.default_rng(seed)
    state = init_state(p, rng)
    step = make_stepper(p, rng)
    fr = []
    for t in range(T):
        step(state)
        if t % 25 == 0:
            fr.append(macro(state)["fr_b"])
        if state[0].sum() < 1e-9 and t > 3000:
            break
    m = macro(state)
    V, E, R, W, A = state
    bm = bimodality(A, V)
    r = dict(tc=tc, ncell=m["ncell"], Vtot=round(m["Vtot"],0),
             fr_b=round(m["fr_b"],3) if np.isfinite(m["fr_b"]) else None,
             purity=round(m["purity"],3) if np.isfinite(m["purity"]) else None,
             bimod=round(bm["bimod"],2), share_lo=round(bm["share_lo"],2),
             Rm=round(m["Rm"],3), Wm=round(m["Wm"],3),
             sd_fr=round(float(np.std(fr[-120:])),4) if len(fr)>120 else None)
    r["guilds_ok"] = bool(bm["bimod"] >= 0.8 and 0.15 <= bm["share_lo"] <= 0.85
                          and (m["purity"] or 0) >= 0.75 and m["ncell"] >= 3000)
    r["saturated"] = bool(m["ncell"] >= 3900)
    return r

grid = []
for over, margin in [(0.6, 3.0), (0.6, 4.5), (1.0, 4.5), (1.0, 6.0), (1.5, 6.0), (1.5, 8.0)]:
    for rho in (1.6, 2.2):
        for r0 in (0.006, 0.009):
            grid.append(dict(rho=rho, yW=0.7, leak=0.4, margin=margin,
                             sig_mut=0.05, over=over, r0=r0))
print(f"{len(grid)} candidates")
t00 = time.time()
for i, tc in enumerate(grid):
    t0 = time.time()
    r = settle_eval(tc)
    r["phase"] = "scan1_settle"
    r["runtime_s"] = round(time.time() - t0, 1)
    out_f.write(json.dumps(r, default=float) + "\n"); out_f.flush()
    Rs = (1 + tc["over"]) / tc["margin"]
    print(f"[{i+1}/{len(grid)}] over={tc['over']} marg={tc['margin']} rho={tc['rho']} r0={tc['r0']} "
          f"(Rs={Rs:.2f}) -> ncell={r['ncell']} bimod={r['bimod']} lo={r['share_lo']} "
          f"pur={r['purity']} Rm={r['Rm']} Wm={r['Wm']} OK={r['guilds_ok']} sat={r['saturated']} ({r['runtime_s']}s)")
print(f"total {time.time()-t00:.0f}s")
