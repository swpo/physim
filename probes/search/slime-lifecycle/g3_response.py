
"""g3_response.py — lifecycle period vs resource regen time (theory coord T_fam).
Usage: g3_response.py <base_params.json> <out.json> [seed]"""
import sys, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle")
from slime import run
from measure import candidate_metrics
from hier_metrics import macro_period_quality

basep = json.load(open(sys.argv[1]))
outf = sys.argv[2]
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
R_star = basep.get("R_star", 0.12); R_wake = basep.get("R_wake", 0.55)
lnfac = np.log((1 - R_star) / (1 - R_wake))
rows = []
for T_fam in (1000, 1750, 3000, 5000, 8000):
    pp = dict(basep); pp["rho"] = lnfac / T_fam
    # keep dose = d0*T_fam constant so famine mortality pressure is invariant
    pp["d0"] = basep["d0"] * (basep.get("_T_fam_ref", 3000) / T_fam)
    T = int(min(max(12 * T_fam, 30000), 60000))
    t0 = time.time()
    o = run(params={k: v for k, v in pp.items() if not k.startswith("_")}, T=T, seed=seed, rec=20)
    m = candidate_metrics(o, rec=20)
    per = m.get("famine_period_med")
    acf = (m.get("l3") or {}).get("aggm", {})
    rows.append(dict(T_fam=T_fam, rho=pp["rho"], T=T, period=per,
                     acf_period=acf.get("acf_period"), n_fam=m.get("n_famines"),
                     ok=m.get("ok"), why=m.get("why"), wall=round(time.time()-t0, 1)))
    print(rows[-1], flush=True)
json.dump(rows, open(outf, "w"), indent=1)
print("wrote", outf)
