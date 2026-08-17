
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
    base = dict(sigma1=4.0, mu1=0.4, d1=0.4, sigma2=2.0, eta2=0.45, rho=0.03,
                DH=0.05, Delta=4.0, nu=0.02, L=64, seeds=(0,1,2,3))
    base.update(kw)
    base["id"] = f"s5-{cid:02d}"; cid += 1
    cands.append(base)

add()                                    # s4-13 exact, 4 seeds
add(DH=0.03)
add(DH=0.03, Delta=2.0)
add(nu=0.04)
add(sigma1=4.5)
add(sigma1=4.25, eta2=0.46, rho=0.028)
add(L=96, seeds=(0,1))                   # size effect

def jsonable(m):
    def cv(v):
        if isinstance(v, (np.floating, np.integer)): return float(v)
        if isinstance(v, dict): return {k: cv(x) for k, x in v.items()}
        if isinstance(v, (list, tuple)): return [cv(x) for x in v]
        return v
    return {k: cv(v) for k, v in m.items() if k not in ("finalR","finalH","finalP")}

results = []
for tc in cands:
    L = tc["L"]; seeds = tc["seeds"]
    tcc = {k: v for k, v in tc.items() if k not in ("id", "L", "seeds")}
    for sd in seeds:
        try:
            rec, m = run_and_measure_teacup(tcc, L=L, nticks=56000, seed=sd)
        except Exception as e:
            m = dict(status="error", error=str(e))
        row = dict(stage=5, id=tc["id"], tc=tcc, seed=sd, L=L, nticks=56000, **jsonable(m))
        results.append(row)
        tf = m.get("top_fit", {})
        both = "**BOTH**" if (m.get("G1") and m.get("G2")) else ""
        print(f"{tc['id']} sd={sd} s1={tcc['sigma1']} e2={tcc['eta2']} rho={tcc['rho']} DH={tcc['DH']} "
              f"De={tcc['Delta']} nu={tcc['nu']} L={L}: {m.get('status')} top={tf.get('model')}/{tf.get('r2')} "
              f"T3={m.get('T3') and round(m['T3'],1)} T2={m.get('T2') and round(m['T2'],1)} "
              f"s12={m.get('sep12') and round(m['sep12'],1)} s23={m.get('sep23') and round(m['sep23'],1)} "
              f"des={m.get('desync') and round(m['desync'],2)} G1={m.get('G1')} G2={m.get('G2')} {both}", flush=True)
        json.dump(results, open(WD + "/results_stage5.json", "w"), indent=1)
print("DONE stage5")
