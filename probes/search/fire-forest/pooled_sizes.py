
import sys, json, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest")
from ff_core import run, measure, events_from_series
from hier_metrics import powerlaw_tail
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest"
base = dict(theta=0.78, Lam=4.0, gsig=0.35, M=2.0, D=8.0, rho=0.03, g=2e-3)
sizes = []
for seed in range(6):
    out = run(L=64, T=60000, seed=seed, rec=5, **base)
    ev = events_from_series(out["area"][2000:], out["ign"][2000:], 5)
    sizes += [e["size"] for e in ev if e["size"] > 0]
sizes = np.array(sizes, float)
print("pooled events:", len(sizes), "min/med/max = %.0f/%.0f/%.0f" % (
    sizes.min(), np.median(sizes), sizes.max()))
for xmin in (None, 3, 10):
    pl = powerlaw_tail(sizes, xmin=xmin)
    print("xmin=%s -> alpha=%s decades=%.2f ks=%.3f n=%d" % (
        xmin, "%.2f" % pl["alpha"] if pl["alpha"] else "-", pl["decades"], pl["ks"], pl["n"]))
# histogram in logs
hist, edges = np.histogram(np.log10(sizes), bins=12)
print("log10-size histogram:", dict(zip(np.round(edges[:-1],1).tolist(), hist.tolist())))
json.dump(dict(n=len(sizes), sizes=sizes.tolist()), open(WD + "/w1_pooled_sizes.json", "w"))
