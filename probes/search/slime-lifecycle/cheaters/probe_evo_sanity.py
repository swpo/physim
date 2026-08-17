
import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle/cheaters")
from hier_metrics import *
import numpy as np
from slime_evo import run

t0 = time.time()
out = run(params=dict(lam_c=2e-3, mu=0.01), T=20000, seed=0, rec=50)
w = time.time() - t0
ser = out["ser"]
print("ok=%s why=%s t=%s wall=%.1fs (%.2f ms/tick)" % (out["ok"], out["why"], out["t"], w, 1000*w/max(out["t"],1)))
n = len(ser["t"])
for i in range(0, n, max(1, n//25)):
    print("t=%6d V=%.3f R=%.3f hf=%.2f agg=%.2f <c>=%.3f sd=%.3f rass=%.2f" % (
        ser["t"][i], ser["vmean"][i], ser["rmean"][i], ser["hf"][i], ser["aggm"][i],
        ser["cmean"][i], ser["csd"][i], ser["rass"][i]))
