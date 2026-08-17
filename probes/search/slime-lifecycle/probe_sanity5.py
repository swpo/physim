import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle")
from hier_metrics import *
import numpy as np
from slime import run

t0 = time.time()
T = 40000
out = run(T=T, seed=0, rec=10,
          snap_times=tuple(range(0, T, 4000)) + (T-10,), s_probe=True)
dt = time.time() - t0
ser = out["ser"]
print("ok=%s why=%s t=%d wall=%.1fs (%.2f ms/tick)" % (out["ok"], out["why"], out["t"], dt, 1000*dt/max(out["t"],1)))
n = len(ser["t"])
for i in range(0, n, max(1, n//40)):
    print("t=%6d V=%.3f Vmx=%5.1f R=%.3f H=%.2f A=%.3f cv=%.2f lf=%.3f agg=%.2f ncl=%3d f=%d" % (
        ser["t"][i], ser["vmean"][i], ser["vmax"][i], ser["rmean"][i], ser["hf"][i],
        ser["amean"][i], ser["cv"][i], ser["lf"][i], ser["aggm"][i], ser["ncl"][i], ser["fire"][i]))
print("fires mean=%.2f max=%d" % (out["fires"].mean(), out["fires"].max()))
burn = n // 4
for key in ("cv", "aggm", "hf", "vmean", "rmean"):
    x = ser[key][burn:]
    fit = compact_top_fit(x, dt=10.0)
    print("TOP %-5s:" % key, fit["model"], fit["r2"], fit["params"])
if out["snaps"]:
    ts = sorted(out["snaps"])
    for f, cm, vmx in (("V","magma",None), ("R","viridis",1.0), ("S","inferno",None)):
        save_strip([out["snaps"][t][f] for t in ts],
                   "strips/sanity5_%s.png" % f,
                   titles=["%s t=%d" % (f, t) for t in ts], cmap=cm, vmax=vmx)
