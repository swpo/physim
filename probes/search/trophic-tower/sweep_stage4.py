
import sys, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from trophic_core import *
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower"

cands = []
cid = 0
for s1 in (3.75, 4.0, 4.25):
    for rho in (0.025, 0.03, 0.035):
        for e2 in (0.42, 0.45, 0.48):
            cands.append(dict(id=f"s4-{cid:02d}", sigma1=s1, mu1=0.4, d1=0.4, sigma2=2.0,
                              eta2=e2, rho=rho, DH=0.05, Delta=4.0, nu=0.02))
            cid += 1

def jsonable(m):
    def cv(v):
        if isinstance(v, (np.floating, np.integer)): return float(v)
        if isinstance(v, dict): return {k: cv(x) for k, x in v.items()}
        if isinstance(v, (list, tuple)): return [cv(x) for x in v]
        return v
    return {k: cv(v) for k, v in m.items() if k not in ("finalR","finalH","finalP")}

results = []
for tc in cands:
    tcc = {k: v for k, v in tc.items() if k != "id"}
    try:
        rec, m = run_and_measure_teacup(tcc, L=64, nticks=56000, seed=0)
    except Exception as e:
        m = dict(status="error", error=str(e))
    row = dict(stage=4, id=tc["id"], tc=tcc, seed=0, L=64, nticks=56000, **jsonable(m))
    results.append(row)
    tf = m.get("top_fit", {})
    both = "**BOTH**" if (m.get("G1") and m.get("G2")) else ""
    print(f"{tc['id']} s1={tcc['sigma1']} rho={tcc['rho']} e2={tcc['eta2']}: st={m.get('status')} "
          f"top={tf.get('model')}/{tf.get('r2')} T3={m.get('T3') and round(m['T3'],1)} "
          f"T2={m.get('T2') and round(m['T2'],1)} s12={m.get('sep12') and round(m['sep12'],1)} "
          f"s23={m.get('sep23') and round(m['sep23'],1)} cv={m.get('spatial_cv') and round(m['spatial_cv'],2)} "
          f"des={m.get('desync') and round(m['desync'],2)} G1={m.get('G1')} G2={m.get('G2')} {both}", flush=True)
    json.dump(results, open(WD + "/results_stage4.json", "w"), indent=1)
print("DONE stage4")
