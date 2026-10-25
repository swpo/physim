"""K2 biomass share over time for membrane_evo arms. usage: share.py world.py seed T out.json"""
import sys, json, importlib.util, numpy as np
wp, seed, T, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
spec = importlib.util.spec_from_file_location("w", wp); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, w.META["size"]); rec = []
from scipy import ndimage
for t in range(T + 1):
    if t % 1000 == 0:
        k1, k2 = float(s["K"].sum()), float(s["K2"].sum())
        lab, n = ndimage.label(s["phi"] > 0.5)
        idx = range(1, n + 1)
        a1 = ndimage.sum(s["K"], lab, idx) if n else []; a2 = ndimage.sum(s["K2"], lab, idx) if n else []
        n2 = int(sum(1 for x, y in zip(a1, a2) if y > x)); 
        rec.append(dict(t=t, share=k2 / max(k1 + k2, 1e-9), cells=n, cells_K2=n2))
    if t < T: s = w.step(s)
ev = s["events"]
json.dump(dict(rec=rec, flips=sum(1 for e in ev if e[1] == "flip"), deaths=sum(1 for e in ev if e[1] == "death"), events=len(ev)), open(out, "w"))
print(out, "final share %.2f cells %d K2cells %d" % (rec[-1]["share"], rec[-1]["cells"], rec[-1]["cells_K2"]), "flips", sum(1 for e in ev if e[1] == "flip"))
