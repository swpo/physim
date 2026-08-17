
import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle/cheaters")
from hier_metrics import *
import numpy as np
from slime_evo import run

tag = sys.argv[1]
pp = json.loads(sys.argv[2])
T = int(pp.pop("_T", 120000))
seed = int(pp.pop("_seed", 0))
t0 = time.time()
out = run(params=pp, T=T, seed=seed, rec=50)
w = time.time() - t0
ser = out["ser"]
print("%s ok=%s why=%s t=%s wall=%.0fs" % (tag, out["ok"], out["why"], out["t"], w))
n = len(ser["t"])
for i in range(0, n, max(1, n//30)):
    print("t=%6d V=%.3f hf=%.2f agg=%.2f <c>=%.3f sd=%.3f rass=%.3f" % (
        ser["t"][i], ser["vmean"][i], ser["hf"][i], ser["aggm"][i],
        ser["cmean"][i], ser["csd"][i], ser["rass"][i]))
half = n // 2
c_eq = float(np.median(ser["cmean"][half:]))
sd_eq = float(np.median(ser["csd"][half:]))
print("EQ: c*=%.3f sd*=%.3f (last-half medians)" % (c_eq, sd_eq))
np.savez_compressed("series_%s.npz" % tag, **ser)
