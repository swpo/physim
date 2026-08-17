
import sys, json, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest")
from ff_core import run, measure, nominal_Tg
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest"
base = dict(theta=0.78, M=2.0, D=8.0, gsig=0.35, rho=0.03)
g0 = 2e-3
f_fix = 9.0 / (64 * 64 * nominal_Tg(g0, base["theta"]))   # W7 spark rate, ABSOLUTE
gs = [1e-3, 1.4e-3, 2e-3, 2.8e-3, 4e-3, 5.6e-3]
rows = []
for g in gs:
    taus = []; per_seed = []
    for seed in (0, 1, 2):
        out = run(L=64, T=60000, g=g, seed=seed, rec=5, f_abs=f_fix, **base)
        res = measure(out, drop=10000, coarse=50)
        per_seed.append(dict(seed=seed, tau3=res["tau3"], model=res["top_model"],
                             r2=res["top_r2"], n_events=res["n_events"]))
        if res["tau3"]: taus.append(res["tau3"])
    med = float(np.median(taus)) if taus else None
    rows.append(dict(g=g, f_abs=f_fix, tau3_med=med, per_seed=per_seed))
    print("g=%.4g tau3_med=%s seeds=%s r2=%s" % (g, "%.0f" % med if med else "-",
        [("%.0f" % s["tau3"]) if s["tau3"] else "-" for s in per_seed],
        ["%.2f" % s["r2"] for s in per_seed]), flush=True)
json.dump(rows, open(WD + "/g3_curve_w7.json", "w"), indent=1)
# scaling exponent
gs_a = np.array([r["g"] for r in rows if r["tau3_med"]])
ta = np.array([r["tau3_med"] for r in rows if r["tau3_med"]])
sl = np.polyfit(np.log(gs_a), np.log(ta), 1)[0]
print("scaling: tau3 ~ g^%.2f" % sl)
print("done")
