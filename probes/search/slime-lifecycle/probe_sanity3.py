import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle")
from hier_metrics import *
import numpy as np
from slime import run

t0 = time.time()
out = run(T=30000, seed=0, rec=10,
          snap_times=(0, 500, 1000, 2000, 4000, 8000, 12000, 16000, 20000, 24000, 29990),
          s_probe=True)
dt = time.time() - t0
ser = out["ser"]
print("ok=%s why=%s t=%d wall=%.1fs (%.2f ms/tick)" % (out["ok"], out["why"], out["t"], dt, 1000*dt/max(out["t"],1)))
n = len(ser["t"])
for i in range(0, n, max(1, n//35)):
    print("t=%6d V=%.3f Vmx=%5.1f R=%.3f H=%.2f S=%.3f A=%.3f cv=%.2f lf=%.3f agg=%.2f ncl=%3d" % (
        ser["t"][i], ser["vmean"][i], ser["vmax"][i], ser["rmean"][i], ser["hf"][i],
        ser["smean"][i], ser["amean"][i], ser["cv"][i], ser["lf"][i], ser["aggm"][i], ser["ncl"][i]))
print("fires mean=%.2f max=%d" % (out["fires"].mean(), out["fires"].max()))
# top-law check on cv
x = ser["cv"][20:]
fit = compact_top_fit(x, dt=10.0)
print("TOP cv:", fit)
x2 = ser["aggm"][20:]
print("TOP aggm:", compact_top_fit(x2, dt=10.0))
if out["snaps"]:
    ts = sorted(out["snaps"])
    for f, cm, vmx in (("V","magma",None), ("R","viridis",1.0), ("S","inferno",None), ("A","cividis",None)):
        save_strip([out["snaps"][t][f] for t in ts],
                   "strips/sanity3_%s.png" % f,
                   titles=["%s t=%d" % (f, t) for t in ts], cmap=cm, vmax=vmx)
