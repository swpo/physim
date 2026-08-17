
import sys, json, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession")
from sf_core import run
SD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession"
base = dict(g=2e-3, Lam=9.0, theta=0.78, M=2.0, D=8.0, gsig=0.35, rho=0.03,
            gT=1e-4, mu=1.5e-5, kapT=1.5, Tm=0.45, rhoT=0.03, cT=0.5)
rows = []
for seed in (1, 2, 3):
    o_s = run(L=64, T_ticks=60000, seed=seed, init="savanna", **base)
    o_f = run(L=64, T_ticks=60000, seed=seed, init="forest", **base)
    r = dict(seed=seed, sav_fF=float(o_s["fracForest"][-100:].mean()),
             for_fF=float(o_f["fracForest"][-100:].mean()))
    r["bistable"] = bool(r["sav_fF"] < 0.15 and r["for_fF"] > 0.6)
    rows.append(r); print(r, flush=True)
# jitter draw on all params
rngj = np.random.default_rng(777)
for j in range(2):
    kw = {k: v * float(rngj.uniform(0.9, 1.1)) for k, v in base.items()}
    o_s = run(L=64, T_ticks=60000, seed=40 + j, init="savanna", **kw)
    o_f = run(L=64, T_ticks=60000, seed=40 + j, init="forest", **kw)
    r = dict(jit=j, sav_fF=float(o_s["fracForest"][-100:].mean()),
             for_fF=float(o_f["fracForest"][-100:].mean()))
    r["bistable"] = bool(r["sav_fF"] < 0.15 and r["for_fF"] > 0.6)
    rows.append(r); print(r, flush=True)
json.dump(rows, open(SD + "/bistability_seeds.json", "w"), indent=1)
print("done")
