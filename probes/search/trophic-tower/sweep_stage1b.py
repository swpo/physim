
import sys, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from trophic_core import *
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower"

# re-measure promising oscillator corner with v2 metrics; vary DH & nu too (they set lambda & desync)
cands = []
cid = 0
for (mu1, e2, rho) in [(0.7,0.25,0.1),(0.7,0.35,0.1),(0.7,0.35,0.2),(0.9,0.25,0.1),
                        (1.1,0.25,0.1),(1.1,0.35,0.1)]:
    for DH in (0.02, 0.05, 0.15):
        for nu in (0.01, 0.04):
            cands.append(dict(id=f"s1b-{cid:02d}", sigma1=3.0, mu1=mu1, d1=0.6, sigma2=2.0,
                              eta2=e2, rho=rho, DH=DH, Delta=2.0, nu=nu))
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
    try:
        rec, m = run_and_measure({k:v for k,v in tc.items() if k!="id"}, L=64, nticks=40000, seed=0)
    except Exception as e:
        m = dict(status="error", error=str(e))
    row = dict(stage="1b", id=tc["id"], tc={k:v for k,v in tc.items() if k!="id"}, seed=0,
               L=64, nticks=40000, **jsonable(m))
    results.append(row)
    print(f"{tc['id']} mu1={tc['mu1']} e2={tc['eta2']} rho={tc['rho']} DH={tc['DH']} nu={tc['nu']}: "
          f"st={m.get('status')} top={m.get('top_fit',{}).get('model')}/{m.get('top_fit',{}).get('r2')} "
          f"T={m.get('T_units') and round(m['T_units'],1)} bT={m.get('blockT_units') and round(m['blockT_units'],1)} "
          f"bfr={m.get('block_cyc_frac')} lam={m.get('ell2_spec') and round(m['ell2_spec'],1)} "
          f"t1={m.get('tau1_used') and round(m['tau1_used'],2)} cv={m.get('spatial_cv') and round(m['spatial_cv'],2)} "
          f"np={m.get('npatch_med')} G1={m.get('G1')} G2={m.get('G2')}", flush=True)
    json.dump(results, open(WD+"/results_stage1b.json","w"), indent=1)
print("DONE")
