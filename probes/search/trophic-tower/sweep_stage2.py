
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
    base = dict(sigma1=3.5, mu1=0.4, d1=0.4, sigma2=2.0, eta2=0.45, rho=0.035,
                DH=0.05, Delta=4.0, nu=0.02)
    base.update(kw)
    base["id"] = f"s2-{cid:02d}"; cid += 1
    cands.append(base)

add()                                  # center
for rho in (0.02, 0.028, 0.045, 0.055): add(rho=rho)
for e2 in (0.38, 0.42, 0.48, 0.52):     add(eta2=e2)
for mu1 in (0.32, 0.36, 0.45):          add(mu1=mu1)
for s1 in (3.0, 3.25, 3.75, 4.0):       add(sigma1=s1)
for De in (1.0, 2.0, 8.0):              add(Delta=De)
for DH in (0.02, 0.12):                 add(DH=DH)
for nu in (0.005, 0.05):                add(nu=nu)
for s2 in (1.5, 3.0):                   add(sigma2=s2)

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
    row = dict(stage=2, id=tc["id"], tc=tcc, seed=0, L=64, nticks=56000, **jsonable(m))
    results.append(row)
    tf = m.get("top_fit", {})
    print(f"{tc['id']} s1={tcc['sigma1']} mu1={tcc['mu1']} e2={tcc['eta2']} rho={tcc['rho']} "
          f"De={tcc['Delta']} DH={tcc['DH']} nu={tcc['nu']} s2={tcc['sigma2']}: st={m.get('status')} "
          f"top={tf.get('model')}/{tf.get('r2')} T3={m.get('T3') and round(m['T3'],1)} "
          f"T2={m.get('T2') and round(m['T2'],1)} t1={m.get('tau1') and round(m['tau1'],2)} "
          f"s12={m.get('sep12') and round(m['sep12'],1)} s23={m.get('sep23') and round(m['sep23'],1)} "
          f"cv={m.get('spatial_cv') and round(m['spatial_cv'],2)} np={m.get('npatch_med')} "
          f"des={m.get('desync') and round(m['desync'],2)} G1={m.get('G1')} G2={m.get('G2')} rt={m.get('runtime_s')}", flush=True)
    json.dump(results, open(WD + "/results_stage2.json", "w"), indent=1)
print("DONE stage2")
