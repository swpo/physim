
import sys, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/l0/complexity")
import metrics_v1 as M

rng = np.random.default_rng(7)
L, REC = 128.0, 5.0
nT = 900   # 4500tu

def mk_rec(blob_fn, na=1, taus=(3.0, 20.0)):
    blobs = {i: [] for i in range(na)}
    for k in range(nT):
        per = blob_fn(k)
        for i in range(na):
            blobs[i].append([[y % L, x % L, 28.0, 1.2] for (ai, y, x) in per
                             if ai == i])
    ct = np.arange(0, nT, 5) * REC
    patches = {i: [dict(n=len(blobs[i][k]), sizes=[28.0] * len(blobs[i][k]),
                        cover=0.02 * len(blobs[i][k]))
                   for k in range(0, nT, 5)] for i in range(na)}
    return dict(world="synth", L=L, T=nT * REC, na=na, nc=len(taus),
                taus=list(taus), memch=[], memf={},
                t=np.arange(nT) * REC, ct=ct,
                blobs=blobs, patches=patches,
                mass={i: [28.0 * len(blobs[i][k]) for k in range(nT)]
                      for i in range(na)},
                species_seeded=[0] * 12, seed_pts=[], status="ok")

# T1: static lattice -> frozen, no motion, interest LOW
pts0 = [(0, 20.0 + 30 * a, 20.0 + 30 * b) for a in range(3) for b in range(3)]
r = mk_rec(lambda k: pts0)
out = M.full_battery(r)
print("T1 static:", round(out["interest"], 1), out["D"]["d5"]["phase"],
      "mv", out["D"]["d4"]["moving_frac"])
assert out["D"]["d4"]["moving_frac"] == 0.0 and out["D"]["d5"]["phase"] in ("frozen", "gas")

# T2: ballistic flock (all move together, v=0.1 px/tu) -> moving, v_corr ~ 1
def flock(k):
    return [(0, y + 0.5 * k * 0.5, x + 0.5 * k * 0.5) for (_, y, x) in pts0]
r = mk_rec(flock)
out = M.full_battery(r)
d4 = out["D"]["d4"]
print("T2 flock:", round(out["interest"], 1), "mv", round(d4["moving_frac"], 2),
      "vcorr", round(d4["v_corr"], 2), "v", round(d4["v_mean"], 3))
assert d4["moving_frac"] > 0.9 and d4["v_corr"] > 0.9

# T3: random walkers (independent diffusion) -> moving, v_corr ~ 0, liquid churn
walk = {j: np.cumsum(rng.normal(0, 1.2, (nT, 2)), axis=0) for j in range(9)}
def gas(k):
    return [(0, 20 + 30 * (j // 3) + walk[j][k][0],
             20 + 30 * (j % 3) + walk[j][k][1]) for j in range(9)]
r = mk_rec(gas)
out = M.full_battery(r)
d4, d5 = out["D"]["d4"], out["D"]["d5"]
print("T3 walkers:", round(out["interest"], 1), "mv", round(d4["moving_frac"], 2),
      "vcorr", round(d4["v_corr"], 2), "phase", d5["phase"],
      "churn", round(d5["churn100"], 3))
assert d4["moving_frac"] > 0.8 and abs(d4["v_corr"]) < 0.25

# T4: oscillating population n(t): 12 +- 6 blobs, period 500tu
def poposc(k):
    n = int(round(12 + 6 * np.sin(2 * np.pi * k * REC / 500.0)))
    return [(0, 10.0 + 13 * j, 64.0) for j in range(max(n, 1))]
r = mk_rec(poposc)
out = M.full_battery(r)
d1 = out["D"]["d1"]
print("T4 posc:", round(out["interest"], 1), d1["model"], "q", round(d1["osc_q"], 2),
      "cyc", d1["osc_cycles"])
assert d1["model"] == "oscillator" and d1["osc_cycles"] >= 5

# T5: slow hidden mode: static blobs, mass slowly oscillating (period 2000tu)
def mkr5():
    r = mk_rec(lambda k: pts0)
    r["mass"][0] = [252 + 30 * np.sin(2 * np.pi * k * REC / 2000.0)
                    for k in range(nT)]
    return r
out = M.full_battery(mkr5())
d2 = out["D"]["d2"]
print("T5 slowmode: tau_slow", d2["tau_slow"], d2["tau_slow_obs"],
      "r_emerg", round(d2["r_emerg"], 1))
assert d2["tau_slow"] > 250 and "mass" in d2["tau_slow_obs"]
print("ALL SYNTH TESTS PASS")
