
"""g3_pure.py — response curves varying exactly ONE raw micro param.
Curve A: rho (resource regen rate) alone, d0 fixed.
Curve B: g (grazing rate) alone, rho fixed.
Usage: g3_pure.py <base_params.json> <out.json>"""
import sys, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle")
from slime import run
from measure import candidate_metrics

basep = json.load(open(sys.argv[1]))
outf = sys.argv[2]
rows = []
rho0 = basep["rho"]; g0 = basep["g"]
for fac in (0.5, 0.75, 1.0, 1.5, 2.25):
    pp = dict(basep); pp["rho"] = rho0 * fac
    T = int(min(max(14 * (1.0/pp["rho"]) * 0.66, 30000), 60000))
    t0 = time.time()
    o = run(params=pp, T=T, seed=0, rec=20)
    m = candidate_metrics(o, rec=20)
    rows.append(dict(curve="rho", fac=fac, rho=pp["rho"], g=pp["g"], T=T,
                     period=m.get("famine_period_med"),
                     acf=(m.get("l3") or {}).get("aggm", {}).get("acf_period"),
                     n_fam=m.get("n_famines"), ok=m.get("ok"), why=m.get("why"),
                     wall=round(time.time()-t0, 1)))
    print(rows[-1], flush=True)
for fac in (0.5, 0.75, 1.0, 1.5, 2.25):
    pp = dict(basep); pp["g"] = g0 * fac
    t0 = time.time()
    o = run(params=pp, T=40000, seed=0, rec=20)
    m = candidate_metrics(o, rec=20)
    rows.append(dict(curve="g", fac=fac, rho=pp["rho"], g=pp["g"], T=40000,
                     period=m.get("famine_period_med"),
                     acf=(m.get("l3") or {}).get("aggm", {}).get("acf_period"),
                     n_fam=m.get("n_famines"), ok=m.get("ok"), why=m.get("why"),
                     wall=round(time.time()-t0, 1)))
    print(rows[-1], flush=True)
json.dump(rows, open(outf, "w"), indent=1, default=float)
print("wrote", outf)
