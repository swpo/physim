
import sys, json, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest")
from ff_core import run, measure, gates, nominal_Tg

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest"
CANDS = {
 "W1": dict(theta=0.78, Lam=4.0, gsig=0.35, M=2.0, D=8.0, rho=0.03, g=2e-3),
 "W2": dict(theta=0.78, Lam=2.5, gsig=0.35, M=2.0, D=8.0, rho=0.03, g=2e-3),
 "W3": dict(theta=0.72, Lam=2.5, gsig=0.35, M=2.0, D=8.0, rho=0.03, g=2e-3),
 "W4": dict(theta=0.72, Lam=4.0, gsig=0.35, M=2.0, D=8.0, rho=0.03, g=2e-3),
 "W5": dict(theta=0.72, Lam=1.5, gsig=0.35, M=2.0, D=8.0, rho=0.03, g=2e-3),
}
JIT = ("theta", "Lam", "M", "D", "gsig", "rho", "g")
allrec = {}
for name, base in CANDS.items():
    entry = dict(base=base, seeds=[], jitter=[])
    # 4 seeds nominal
    for seed in range(4):
        out = run(L=64, T=60000, seed=seed, rec=5, **base)
        res = measure(out, drop=10000, coarse=50)
        gt = gates(res)
        ok = gt["G1"] and gt["G2"] and gt["G5"]
        entry["seeds"].append(dict(seed=seed, gates=gt, ok=ok,
            r2=res["top_r2"], model=res["top_model"], var=res["top_var"],
            tau1=res["tau1"], tau2=res["tau2"], tau3=res["tau3"],
            sep21=res["sep21"], sep32=res["sep32"], n_events=res["n_events"],
            pl=res["pl"], runtime=res["runtime"],
            sizes=[]))
        print("%s seed%d ok=%d r2=%.3f %s(%s) nev=%d t3=%s s21=%.1f s32=%.1f dec=%s"
              % (name, seed, ok, res["top_r2"], res["top_model"], res["top_var"],
                 res["n_events"], "%.0f" % res["tau3"] if res["tau3"] else "-",
                 res["sep21"] or 0, res["sep32"] or 0,
                 res["pl"]["decades"] if res["pl"] else "-"), flush=True)
    # 3 jitter draws (+-10% on all searched params), fresh seeds
    rngj = np.random.default_rng(999)
    for j in range(3):
        kw = dict(base)
        for k in JIT:
            kw[k] = base[k] * float(rngj.uniform(0.9, 1.1))
        out = run(L=64, T=60000, seed=10 + j, rec=5, **kw)
        res = measure(out, drop=10000, coarse=50)
        gt = gates(res)
        ok = gt["G1"] and gt["G2"] and gt["G5"]
        entry["jitter"].append(dict(j=j, kw={k: round(v, 5) for k, v in kw.items()},
            gates=gt, ok=ok, r2=res["top_r2"], model=res["top_model"],
            var=res["top_var"], tau3=res["tau3"], sep21=res["sep21"],
            sep32=res["sep32"], n_events=res["n_events"]))
        print("%s jit%d ok=%d r2=%.3f %s nev=%d t3=%s s21=%.1f s32=%.1f"
              % (name, j, ok, res["top_r2"], res["top_model"], res["n_events"],
                 "%.0f" % res["tau3"] if res["tau3"] else "-",
                 res["sep21"] or 0, res["sep32"] or 0), flush=True)
    npass = sum(s["ok"] for s in entry["seeds"])
    jpass = sum(s["ok"] for s in entry["jitter"])
    entry["G4"] = bool(npass >= 3 and jpass >= 2)
    print("== %s: seeds %d/4, jitter %d/3 -> G4=%s" % (name, npass, jpass, entry["G4"]), flush=True)
    allrec[name] = entry
json.dump(allrec, open(WD + "/gate_results.json", "w"), indent=1)
print("done")
