import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle")
from hier_metrics import *
import numpy as np
from slime import run

pp = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
T = int(pp.pop("_T", 40000))
tag = pp.pop("_tag", "tune")
t0 = time.time()
out = run(params=pp, T=T, seed=int(pp.pop("_seed", 0)) if "_seed" in pp else 0, rec=10,
          snap_times=tuple(range(0, T, T//10)) + (T-10,))
dt = time.time() - t0
ser = out["ser"]
print("ok=%s why=%s t=%d wall=%.1fs" % (out["ok"], out["why"], out["t"], dt))
n = len(ser["t"])
for i in range(0, n, max(1, n//40)):
    print("t=%6d V=%.3f R=%.3f H=%.2f cv=%.2f lf=%.3f agg=%.2f ncl=%3d f=%d" % (
        ser["t"][i], ser["vmean"][i], ser["rmean"][i], ser["hf"][i],
        ser["cv"][i], ser["lf"][i], ser["aggm"][i], ser["ncl"][i], ser["fire"][i]))
burn = n // 5
for key in ("cv", "aggm", "hf", "vmean", "rmean"):
    fit = compact_top_fit(ser[key][burn:], dt=10.0)
    print("TOP %-5s:" % key, fit["model"], fit["r2"], fit["params"])
if out["snaps"]:
    ts = sorted(out["snaps"])
    for f, cm, vmx in (("V","magma",None), ("R","viridis",1.0), ("S","inferno",None)):
        save_strip([out["snaps"][t][f] for t in ts], "strips/%s_%s.png" % (tag, f),
                   titles=["t=%d" % t for t in ts], cmap=cm, vmax=vmx)
