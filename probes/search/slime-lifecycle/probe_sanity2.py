
import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle")
from hier_metrics import *
import numpy as np
from slime import run

t0 = time.time()
out = run(T=20000, seed=0, rec=10, snap_times=(0, 1000, 2500, 5000, 8000, 12000, 16000, 19990))
dt = time.time() - t0
ser = out["ser"]
print("ok=%s why=%s t=%d wall=%.1fs (%.2f ms/tick)" % (out["ok"], out["why"], out["t"], dt, 1000*dt/max(out["t"],1)))
n = len(ser["t"])
for i in range(0, n, max(1, n//30)):
    print("t=%6d V=%.3f Vmx=%.2f R=%.3f H=%.2f S=%.4f A=%.3f cv=%.2f lf=%.3f ncl=%3d" % (
        ser["t"][i], ser["vmean"][i], ser["vmax"][i], ser["rmean"][i], ser["hf"][i],
        ser["smean"][i], ser["amean"][i], ser["cv"][i], ser["lf"][i], ser["ncl"][i]))
print("fires mean=%.2f max=%d" % (out["fires"].mean(), out["fires"].max()))
if out["snaps"]:
    ts = sorted(out["snaps"])
    for f, cm, vmx in (("V","magma",None), ("R","viridis",1.0), ("S","inferno",None), ("A","cividis",None)):
        save_strip([out["snaps"][t][f] for t in ts],
                   "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle/strips/sanity2_%s.png" % f,
                   titles=["%s t=%d" % (f, t) for t in ts], cmap=cm, vmax=vmx)
