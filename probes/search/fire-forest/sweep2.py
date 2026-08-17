
import sys, json, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest")
from ff_core import run, measure, gates

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest"
cands = []
# refine the G1+G2 region; push for pl decades via gsig and Lam
for theta in (0.72, 0.78):
    for Lam in (1.5, 2.5, 4.0):
        for gsig in (0.35, 0.6):
            for M in (2.0, 3.0):
                cands.append(dict(theta=theta, Lam=Lam, gsig=gsig, M=M,
                                  D=8.0, rho=0.03))
# middle-ground: moderate Lam with strong heterogeneity, coarse view
for Lam in (6.0, 9.0):
    for gsig in (0.6, 0.9):
        cands.append(dict(theta=0.78, Lam=Lam, gsig=gsig, M=3.0, D=8.0, rho=0.03))

results = []
for i, c in enumerate(cands):
    try:
        out = run(L=64, T=60000, g=2e-3, seed=0, rec=5, **c)
        res = measure(out, drop=10000, coarse=50)
        gt = gates(res)
        rec = dict(id=100 + i, params=dict(g=2e-3, L=64, T=60000, **c),
                   res={k: v for k, v in res.items() if k != "top_all"}, gates=gt)
    except Exception as e:
        rec = dict(id=100 + i, params=dict(g=2e-3, L=64, T=60000, **c),
                   error=repr(e), gates=dict(G1=False, G2=False, G5=False))
    results.append(rec)
    r = rec.get("res", {})
    tp = r.get("top_params", {})
    print("%3d th=%.2f Lam=%4.1f gs=%.2f M=%.0f | top=%s(%s) r2=%.3f flips=%s "
          "nev=%3s t3=%6s s21=%5s s32=%5s dec=%s | G1=%d G2=%d" % (
        100 + i, c["theta"], c["Lam"], c["gsig"], c["M"],
        r.get("top_model", "ERR"), r.get("top_var", "-"), r.get("top_r2", 0),
        tp.get("n_flips", tp.get("n_cycles", "-")),
        r.get("n_events", "-"),
        "-" if not r.get("tau3") else "%.0f" % r["tau3"],
        "-" if not r.get("sep21") else "%.1f" % r["sep21"],
        "-" if not r.get("sep32") else "%.1f" % r["sep32"],
        "-" if not r.get("pl") else r["pl"]["decades"],
        rec["gates"]["G1"], rec["gates"]["G2"]), flush=True)

json.dump(results, open(WD + "/sweep2_results.json", "w"), indent=1)
print("done", len(results))
