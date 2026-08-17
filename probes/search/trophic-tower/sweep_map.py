
import sys, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from trophic_core import *
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower"

def jsonable(m):
    def cv(v):
        if isinstance(v, (np.floating, np.integer)): return float(v)
        if isinstance(v, dict): return {k: cv(x) for k, x in v.items()}
        if isinstance(v, (list, tuple)): return [cv(x) for x in v]
        return v
    return {k: cv(v) for k, v in m.items() if k not in ("finalR","finalH","finalP")}

results = []
for e2 in (0.42, 0.44, 0.46, 0.48):
    for rho in (0.030, 0.034, 0.038, 0.042):
        for nu in (0.02, 0.03):
            tc = dict(sigma1=4.5, mu1=0.4, d1=0.4, sigma2=2.0, eta2=e2, rho=rho,
                      DH=0.05, Delta=4.0, nu=nu)
            try:
                rec, m = run_and_measure_teacup(tc, L=64, nticks=56000, seed=0)
            except Exception as e:
                m = dict(status="error", error=str(e))
            results.append(dict(stage="map", tc=tc, seed=0, L=64, nticks=56000, **jsonable(m)))
            tf = m.get("top_fit", {})
            both = m.get("G1") and m.get("G2")
            print(f"e2={e2} rho={rho} nu={nu}: {m.get('status')} top={tf.get('model')}/{tf.get('r2')} "
                  f"T3={m.get('T3') and round(m['T3'],1)} T2={m.get('T2') and round(m['T2'],1)} "
                  f"famp={m.get('fast_amp_frac') and round(m['fast_amp_frac'],2)} "
                  f"np={m.get('npatch_med')} cv={m.get('spatial_cv') and round(m['spatial_cv'],2)} "
                  f"{'BOTH' if both else ('G1' if m.get('G1') else '') + ('G2' if m.get('G2') else '')}", flush=True)
            json.dump(results, open(WD + "/results_map.json", "w"), indent=1)
print("DONE map")
