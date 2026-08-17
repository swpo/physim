
import sys, json, numpy as np, itertools, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest")
from ff_core import run, measure, gates

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest"
cands = []
# Group A: relaxation-oscillator target (rare sparks, deep burn, high theta)
for theta in (0.7, 0.8):
    for Lam in (0.7, 1.5, 3.0, 6.0):
        for gsig in (0.0, 0.35):
            cands.append(dict(group="A", theta=theta, Lam=Lam, M=3.0, D=8.0,
                              gsig=gsig, rho=0.03))
# A2: no seed-rain variants (long bottom dwell)
for Lam in (1.5, 3.0):
    cands.append(dict(group="A2", theta=0.8, Lam=Lam, M=3.0, D=8.0,
                      gsig=0.35, rho=0.0))
# Group B: SOC-lean (many sparks, heterogeneous)
for theta in (0.55, 0.65):
    for Lam in (15.0, 40.0, 100.0):
        cands.append(dict(group="B", theta=theta, Lam=Lam, M=3.0, D=5.0,
                          gsig=0.5, rho=0.0))
# Group C: mixed edges (spread margin / burn depth extremes)
for M, D in ((2.0, 8.0), (5.0, 8.0), (3.0, 4.0), (3.0, 12.0)):
    cands.append(dict(group="C", theta=0.75, Lam=2.0, M=M, D=D,
                      gsig=0.35, rho=0.03))
# Group D: spiral / continuous-fire attempt (low theta, shallow burn)
for M, D in ((4.0, 2.0), (6.0, 2.0), (4.0, 3.0)):
    cands.append(dict(group="D", theta=0.35, Lam=0.3, M=M, D=D,
                      gsig=0.0, rho=0.05))

results = []
for i, c in enumerate(cands):
    kw = {k: v for k, v in c.items() if k != "group"}
    try:
        out = run(L=64, T=60000, g=2e-3, seed=0, rec=5, **kw)
        res = measure(out, drop=10000)
        gt = gates(res)
        rec = dict(id=i, group=c["group"], params=dict(g=2e-3, L=64, T=60000, **kw),
                   res={k: v for k, v in res.items() if k not in ("top_all",)},
                   gates=gt)
    except Exception as e:
        rec = dict(id=i, group=c["group"], params=dict(g=2e-3, L=64, T=60000, **kw),
                   error=repr(e), gates=dict(G1=False, G2=False, G5=False))
    results.append(rec)
    r = rec.get("res", {})
    print("%2d %-2s th=%.2f Lam=%5.1f M=%.0f D=%2.0f gs=%.2f rho=%.2f | "
          "top=%s(%s) r2=%.3f nev=%3s t1=%4s t2=%5s t3=%6s s21=%4s s32=%4s pl_dec=%s | G1=%d G2=%d"
          % (i, c["group"], kw["theta"], kw["Lam"], kw["M"], kw["D"], kw["gsig"], kw["rho"],
             r.get("top_model","ERR"), r.get("top_var","-"), r.get("top_r2",0),
             r.get("n_events","-"),
             "-" if not r.get("tau1") else "%.1f"%r["tau1"],
             "-" if not r.get("tau2") else "%.0f"%r["tau2"],
             "-" if not r.get("tau3") else "%.0f"%r["tau3"],
             "-" if not r.get("sep21") else "%.1f"%r["sep21"],
             "-" if not r.get("sep32") else "%.1f"%r["sep32"],
             "-" if not r.get("pl") else r["pl"]["decades"],
             rec["gates"]["G1"], rec["gates"]["G2"]), flush=True)

json.dump(results, open(WD + "/sweep1_results.json", "w"), indent=1)
print("done", len(results))
