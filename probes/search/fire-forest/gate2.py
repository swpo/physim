
import sys, json, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest")
from ff_core import run, measure, gates, events_from_series
from hier_metrics import powerlaw_tail
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest"
CANDS = {
 "W6": dict(theta=0.78, Lam=6.0, gsig=0.35, M=2.0, D=8.0, rho=0.03, g=2e-3),
 "W7": dict(theta=0.78, Lam=9.0, gsig=0.35, M=2.0, D=8.0, rho=0.03, g=2e-3),
}
JIT = ("theta", "Lam", "M", "D", "gsig", "rho", "g")
allrec = json.load(open(WD + "/gate_results.json"))
for name, base in CANDS.items():
    entry = dict(base=base, seeds=[], jitter=[])
    pooled = []
    for seed in range(4):
        out = run(L=64, T=60000, seed=seed, rec=5, **base)
        res = measure(out, drop=10000, coarse=50)
        gt = gates(res)
        ok = gt["G1"] and gt["G2"] and gt["G5"]
        ev = events_from_series(out["area"][2000:], out["ign"][2000:], 5)
        pooled += [e["size"] for e in ev if e["size"] > 0]
        entry["seeds"].append(dict(seed=seed, gates=gt, ok=ok, r2=res["top_r2"],
            model=res["top_model"], var=res["top_var"], tau1=res["tau1"],
            tau2=res["tau2"], tau3=res["tau3"], sep21=res["sep21"],
            sep32=res["sep32"], n_events=res["n_events"], pl=res["pl"],
            runtime=res["runtime"]))
        print("%s seed%d ok=%d r2=%.3f nev=%d t1=%.1f t2=%.0f t3=%.0f s21=%.1f s32=%.1f"
              % (name, seed, ok, res["top_r2"], res["n_events"], res["tau1"],
                 res["tau2"], res["tau3"], res["sep21"], res["sep32"]), flush=True)
    rngj = np.random.default_rng(777)
    for j in range(3):
        kw = dict(base)
        for k in JIT:
            kw[k] = base[k] * float(rngj.uniform(0.9, 1.1))
        out = run(L=64, T=60000, seed=20 + j, rec=5, **kw)
        res = measure(out, drop=10000, coarse=50)
        gt = gates(res)
        ok = gt["G1"] and gt["G2"] and gt["G5"]
        entry["jitter"].append(dict(j=j, kw={k: round(v, 5) for k, v in kw.items()},
            gates=gt, ok=ok, r2=res["top_r2"], model=res["top_model"],
            tau3=res["tau3"], sep21=res["sep21"], sep32=res["sep32"],
            n_events=res["n_events"]))
        print("%s jit%d ok=%d r2=%.3f nev=%d t3=%s" % (name, j, ok, res["top_r2"],
              res["n_events"], "%.0f" % res["tau3"] if res["tau3"] else "-"), flush=True)
    npass = sum(s["ok"] for s in entry["seeds"])
    jpass = sum(s["ok"] for s in entry["jitter"])
    entry["G4"] = bool(npass >= 3 and jpass >= 2)
    # pooled size stats (4 seeds)
    ps = np.array(pooled, float)
    pl = powerlaw_tail(ps)
    frac_span = float((ps >= 0.9 * 4096).mean())
    entry["pooled"] = dict(n=len(ps), decades=pl["decades"], alpha=pl["alpha"],
                           ks=pl["ks"], frac_spanning=frac_span,
                           med=float(np.median(ps)))
    print("== %s: seeds %d/4 jitter %d/3 G4=%s | pooled n=%d dec=%.2f alpha=%s frac_span=%.2f"
          % (name, npass, jpass, entry["G4"], len(ps), pl["decades"],
             "%.2f" % pl["alpha"] if pl["alpha"] else "-", frac_span), flush=True)
    allrec[name] = entry
json.dump(allrec, open(WD + "/gate_results.json", "w"), indent=1)
print("done")
