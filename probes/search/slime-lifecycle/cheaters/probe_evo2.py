import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle/cheaters")
from hier_metrics import *
import numpy as np
from slime_evo import run

pp = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
T = int(pp.pop("_T", 30000))
t0 = time.time()
out = run(params=pp, T=T, seed=int(pp.pop("_seed", 0)), rec=50)
w = time.time() - t0
ser = out["ser"]
print("ok=%s why=%s t=%s wall=%.1fs (%.2f ms/tick)" % (out["ok"], out["why"], out["t"], w, 1000*w/max(out["t"],1)))
n = len(ser["t"])
for i in range(0, n, max(1, n//30)):
    print("t=%6d V=%.3f R=%.3f hf=%.2f agg=%.2f <c>=%.3f sd=%.3f rass=%.2f f=%d" % (
        ser["t"][i], ser["vmean"][i], ser["rmean"][i], ser["hf"][i], ser["aggm"][i],
        ser["cmean"][i], ser["csd"][i], ser["rass"][i], ser["fire"][i]))
b = n // 4
for key in ("cmean", "aggm"):
    fit = compact_top_fit(ser[key][b:], dt=50.0)
    print("TOP %-5s:" % key, fit["model"], fit["r2"], fit["params"])
