
import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle")
from hier_metrics import *
import numpy as np
from slime import run

t0 = time.time()
out = run(T=12000, seed=0, rec=10, snap_times=(0, 1500, 3000, 6000, 9000, 11990))
dt = time.time() - t0
ser = out["ser"]
print("ok=%s why=%s t=%d wall=%.1fs (%.2f ms/tick)" % (out["ok"], out["why"], out["t"], dt, 1000*dt/max(out["t"],1)))
n = len(ser["t"])
for i in range(0, n, max(1, n//25)):
    print("t=%6d V=%.3f R=%.3f H=%.2f S=%.3f cv=%.2f lf=%.3f ncl=%3d" % (
        ser["t"][i], ser["vmean"][i], ser["rmean"][i], ser["hf"][i], ser["smean"][i],
        ser["cv"][i], ser["lf"][i], ser["ncl"][i]))
print("fires mean=%.2f max=%d" % (out["fires"].mean(), out["fires"].max()))
if out["snaps"]:
    ts = sorted(out["snaps"])
    save_strip([out["snaps"][t][0] for t in ts], 
               "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle/strips/sanity_V.png",
               titles=["V t=%d" % t for t in ts], cmap="magma")
    save_strip([out["snaps"][t][1] for t in ts],
               "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle/strips/sanity_R.png",
               titles=["R t=%d" % t for t in ts], cmap="viridis", vmax=1.0)
    save_strip([out["snaps"][t][2] for t in ts],
               "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle/strips/sanity_S.png",
               titles=["S t=%d" % t for t in ts], cmap="inferno")
