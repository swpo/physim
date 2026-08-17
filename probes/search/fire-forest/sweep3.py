
import sys, json, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest")
from ff_core import run, measure, gates
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest"
cands = []
for Lam in (6.0, 9.0, 15.0, 25.0):
    cands.append(dict(theta=0.78, Lam=Lam, gsig=0.35, M=2.0, D=8.0, rho=0.03))
for Lam in (9.0, 15.0):
    cands.append(dict(theta=0.78, Lam=Lam, gsig=0.7, M=2.0, D=5.0, rho=0.03))
results = []
for i, c in enumerate(cands):
    out = run(L=64, T=60000, g=2e-3, seed=0, rec=5, **c)
    res = measure(out, drop=10000, coarse=50)
    gt = gates(res)
    rec = dict(id=200 + i, params=dict(g=2e-3, L=64, T=60000, **c),
               res={k: v for k, v in res.items() if k != "top_all"}, gates=gt)
    results.append(rec)
    print("%3d Lam=%4.1f gs=%.2f D=%d | top=%s r2=%.3f nev=%3d s21=%.1f s32=%s dec=%s | G1=%d G2=%d"
          % (200 + i, c["Lam"], c["gsig"], c["D"], res["top_model"], res["top_r2"],
             res["n_events"], res["sep21"] or 0,
             "%.1f" % res["sep32"] if res["sep32"] else "-",
             res["pl"]["decades"] if res["pl"] else "-",
             gt["G1"], gt["G2"]), flush=True)
json.dump(results, open(WD + "/sweep3_results.json", "w"), indent=1)
print("done")
