
"""g4_robust.py — seeds + jitter robustness. Usage: g4_robust.py <params.json> <out.json>"""
import sys, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle")
from slime import run
from measure import candidate_metrics, gate_check

basep = json.load(open(sys.argv[1]))
outf = sys.argv[2]
JITTER_KEYS = ["rho", "d0", "pd", "chi_a", "g", "p_spont", "R_star", "R_wake"]
rows = []
# 4 seeds plain
for seed in range(4):
    t0 = time.time()
    o = run(params=basep, T=40000, seed=seed, rec=20)
    m = candidate_metrics(o, rec=20); gt = gate_check(m)
    rows.append(dict(kind="seed", seed=seed, jit=None, G1=gt.get("G1"), G2=gt.get("G2"),
                     detail=gt.get("G2_detail"), sep12=gt.get("sep12"), sep23=gt.get("sep23"),
                     n_fam=m.get("n_famines"), why=m.get("why"), wall=round(time.time()-t0,1)))
    print(rows[-1], flush=True)
# 4 jittered runs (+-10% random per key), seeds 10..13
rng = np.random.default_rng(999)
for k in range(4):
    pp = dict(basep)
    jit = {}
    for key in JITTER_KEYS:
        if key in pp:
            f = float(rng.uniform(0.9, 1.1))
            pp[key] = pp[key] * f
            jit[key] = round(f, 3)
    # keep R_wake > R_star + 0.1
    if pp.get("R_wake", 0.55) < pp.get("R_star", 0.12) + 0.15:
        pp["R_wake"] = pp["R_star"] + 0.15
    t0 = time.time()
    o = run(params=pp, T=40000, seed=10 + k, rec=20)
    m = candidate_metrics(o, rec=20); gt = gate_check(m)
    rows.append(dict(kind="jitter", seed=10 + k, jit=jit, G1=gt.get("G1"), G2=gt.get("G2"),
                     detail=gt.get("G2_detail"), sep12=gt.get("sep12"), sep23=gt.get("sep23"),
                     n_fam=m.get("n_famines"), why=m.get("why"), wall=round(time.time()-t0,1)))
    print(rows[-1], flush=True)
json.dump(rows, open(outf, "w"), indent=1, default=str)
print("wrote", outf)
