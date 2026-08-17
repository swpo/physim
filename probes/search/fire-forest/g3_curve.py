
import sys, json, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest")
from ff_core import run, measure, nominal_Tg

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest"
# winner family base (W1); response curve: top clock tau3 vs growth rate g,
# holding the ABSOLUTE spark rate f fixed (so the clock is not imposed via Lam)
base = dict(theta=0.78, Lam=4.0, M=2.0, D=8.0, gsig=0.35, rho=0.03)
g0 = 2e-3
f_fix = base["Lam"] / (64 * 64 * nominal_Tg(g0, base["theta"]))
gs = [1e-3, 1.4e-3, 2e-3, 2.8e-3, 4e-3, 5.6e-3]
rows = []
for g in gs:
    taus = []
    per_seed = []
    for seed in (0, 1, 2):
        out = run(L=64, T=60000, g=g, theta=base["theta"], M=base["M"],
                  D=base["D"], gsig=base["gsig"], rho=base["rho"],
                  seed=seed, rec=5, f_abs=f_fix)
        res = measure(out, drop=10000, coarse=50)
        per_seed.append(dict(seed=seed, tau3=res["tau3"], model=res["top_model"],
                             r2=res["top_r2"], n_events=res["n_events"]))
        if res["tau3"]:
            taus.append(res["tau3"])
    med = float(np.median(taus)) if taus else None
    rows.append(dict(g=g, f_abs=f_fix, tau3_med=med, per_seed=per_seed))
    print("g=%.4g tau3_med=%s  seeds=%s" % (
        g, "%.0f" % med if med else "-",
        [("%.0f" % s["tau3"]) if s["tau3"] else "-" for s in per_seed]), flush=True)
json.dump(rows, open(WD + "/g3_curve.json", "w"), indent=1)
print("done")
