
import sys, json, time, itertools
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from trophic_core import *

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower"
results = []
cands = []
cid = 0
for mu1 in (0.7, 0.9, 1.1):
    for eta2 in (0.25, 0.35, 0.5, 0.65):
        for rho in (0.1, 0.2, 0.3):
            cands.append(dict(id=f"s1-{cid:02d}", sigma1=3.0, mu1=mu1, d1=0.6,
                              sigma2=2.0, eta2=eta2, rho=rho, DH=0.05, Delta=2.0, nu=0.02))
            cid += 1

def jsonable(m):
    def cv(v):
        if isinstance(v, (np.floating, np.integer)): return float(v)
        if isinstance(v, dict): return {k: cv(x) for k, x in v.items()}
        if isinstance(v, (list, tuple)): return [cv(x) for x in v]
        return v
    return {k: cv(v) for k, v in m.items() if k not in ("finalR","finalH","finalP")}

for tc in cands:
    t0 = time.time()
    try:
        rec, m = run_and_measure({k: v for k, v in tc.items() if k != "id"},
                                 L=64, nticks=40000, seed=0, snaps=True)
    except Exception as e:
        m = dict(status="error", error=str(e))
        rec = None
    row = dict(stage=1, id=tc["id"], tc={k: v for k, v in tc.items() if k != "id"},
               seed=0, L=64, nticks=40000, **jsonable(m))
    results.append(row)
    print(f"{tc['id']} mu1={tc['mu1']} e2={tc['eta2']} rho={tc['rho']}: "
          f"st={m.get('status')} top={m.get('fits_all')} G1={m.get('G1')} G2={m.get('G2')} "
          f"T={m.get('T_units') and round(m.get('T_units'),1)} tau2={m.get('tau2_units') and round(m.get('tau2_units'),1)} "
          f"tau1={m.get('tau1_units') and round(m.get('tau1_units'),2)} cv={m.get('spatial_cv') and round(m.get('spatial_cv'),2)} "
          f"np={m.get('npatch_med')} rt={m.get('runtime_s')}s", flush=True)
    json.dump(results, open(WD + "/results_stage1.json", "w"), indent=1)
print("DONE stage1")
