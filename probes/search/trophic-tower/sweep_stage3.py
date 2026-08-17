
import sys, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from trophic_core import *
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower"

cands = []
cid = 0
def add(**kw):
    global cid
    base = dict(sigma1=3.5, mu1=0.4, d1=0.4, sigma2=2.0, eta2=0.45, rho=0.03,
                DH=0.05, Delta=4.0, nu=0.02, L=64)
    base.update(kw)
    base["id"] = f"s3-{cid:02d}"; cid += 1
    cands.append(base)

# teacup region refinement with warm start
for rho in (0.025, 0.03, 0.035, 0.04):
    for e2 in (0.45, 0.48):
        add(rho=rho, eta2=e2)
# desynchronization exploration
for DH in (0.01, 0.02):
    for nu in (0.02, 0.06):
        add(DH=DH, nu=nu)
add(DH=0.02, nu=0.04, L=96)   # size scaling of desync
add(mu1=0.36, rho=0.03)
add(mu1=0.44, rho=0.03)
add(sigma1=4.0, rho=0.03)

def jsonable(m):
    def cv(v):
        if isinstance(v, (np.floating, np.integer)): return float(v)
        if isinstance(v, dict): return {k: cv(x) for k, x in v.items()}
        if isinstance(v, (list, tuple)): return [cv(x) for x in v]
        return v
    return {k: cv(v) for k, v in m.items() if k not in ("finalR","finalH","finalP")}

results = []
for tc in cands:
    L = tc["L"]
    tcc = {k: v for k, v in tc.items() if k not in ("id", "L")}
    try:
        rec, m = run_and_measure_teacup(tcc, L=L, nticks=56000, seed=0)
    except Exception as e:
        m = dict(status="error", error=str(e))
    row = dict(stage=3, id=tc["id"], tc=tcc, seed=0, L=L, nticks=56000, **jsonable(m))
    results.append(row)
    tf = m.get("top_fit", {})
    print(f"{tc['id']} rho={tcc['rho']} e2={tcc['eta2']} mu1={tcc['mu1']} s1={tcc['sigma1']} "
          f"DH={tcc['DH']} nu={tcc['nu']} L={L}: st={m.get('status')} "
          f"top={tf.get('model')}/{tf.get('r2')} T3={m.get('T3') and round(m['T3'],1)} "
          f"T2={m.get('T2') and round(m['T2'],1)} t1={m.get('tau1') and round(m['tau1'],2)} "
          f"s12={m.get('sep12') and round(m['sep12'],1)} s23={m.get('sep23') and round(m['sep23'],1)} "
          f"cv={m.get('spatial_cv') and round(m['spatial_cv'],2)} np={m.get('npatch_med')} "
          f"des={m.get('desync') and round(m['desync'],2)} G1={m.get('G1')} G2={m.get('G2')} rt={m.get('runtime_s')}", flush=True)
    json.dump(results, open(WD + "/results_stage3.json", "w"), indent=1)
print("DONE stage3")
