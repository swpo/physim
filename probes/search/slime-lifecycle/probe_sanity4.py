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
    print("t=%6d V=%.3f Vmx=%5.1f R=%.3f H=%.2f A=%.3f cv=%.2f lf=%.3f agg=%.2f ncl=%3d f=%d" % (
        ser["t"][i], ser["vmean"][i], ser["vmax"][i], ser["rmean"][i], ser["hf"][i],
        ser["amean"][i], ser["cv"][i], ser["lf"][i], ser["aggm"][i], ser["ncl"][i], ser["fire"][i]))
print("fires mean=%.2f max=%d" % (out["fires"].mean(), out["fires"].max()))
for key in ("cv", "aggm", "hf", "vmean", "rmean"):
    x = ser[key][30:]
    fit = compact_top_fit(x, dt=10.0)
    print("TOP %-5s:" % key, fit["model"], fit["r2"], fit["params"])
if out["snaps"]:
    ts = sorted(out["snaps"])
    for f, cm, vmx in (("V","magma",None), ("R","viridis",1.0), ("S","inferno",None), ("A","cividis",None)):
        save_strip([out["snaps"][t][f] for t in ts],
                   "strips/sanity4_%s.png" % f,
                   titles=["%s t=%d" % (f, t) for t in ts], cmap=cm, vmax=vmx)
