
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
    base = dict(sigma1=4.5, mu1=0.4, d1=0.4, sigma2=2.0, eta2=0.45, rho=0.03,
                DH=0.05, Delta=4.0, nu=0.02)
    base.update(kw)
    base["id"] = f"s6-{cid:02d}"; cid += 1
    cands.append(base)

for s1 in (4.5, 5.0):
    for e2 in (0.45, 0.5, 0.55):
        for rho in (0.025, 0.03):
            add(sigma1=s1, eta2=e2, rho=rho)
for s2 in (2.5, 3.0):     # deeper predator saturation at the good spot
    add(sigma2=s2)
    add(sigma2=s2, eta2=0.5)
for mu1 in (0.35, 0.45):
    add(mu1=mu1)
add(nu=0.01); add(nu=0.005)

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
    nboth = 0
    for sd in (0, 1):
        try:
            rec, m = run_and_measure_teacup(tcc, L=64, nticks=56000, seed=sd)
        except Exception as e:
            m = dict(status="error", error=str(e))
        row = dict(stage=6, id=tc["id"], tc=tcc, seed=sd, L=64, nticks=56000, **jsonable(m))
        results.append(row)
        tf = m.get("top_fit", {})
        both = m.get("G1") and m.get("G2")
        nboth += int(bool(both))
        print(f"{tc['id']} sd={sd} s1={tcc['sigma1']} s2={tcc['sigma2']} e2={tcc['eta2']} rho={tcc['rho']} "
              f"mu1={tcc['mu1']} nu={tcc['nu']}: {m.get('status')} top={tf.get('model')}/{tf.get('r2')} "
              f"T3={m.get('T3') and round(m['T3'],1)} T2={m.get('T2') and round(m['T2'],1)} "
              f"famp={m.get('fast_amp_frac') and round(m['fast_amp_frac'],2)} "
              f"s23={m.get('sep23') and round(m['sep23'],1)} des={m.get('desync') and round(m['desync'],2)} "
              f"G1={m.get('G1')} G2={m.get('G2')} {'**BOTH**' if both else ''}", flush=True)
        json.dump(results, open(WD + "/results_stage6.json", "w"), indent=1)
    print(f"  -> {tc['id']}: {nboth}/2 seeds BOTH", flush=True)
print("DONE stage6")
