"""Scan a_th (and seed) of c09's AC-gel world; report cell fraction and number of phi>0.5 components over time."""
import sys, json, os, time, importlib.util
import numpy as np
from scipy import ndimage
spec = importlib.util.spec_from_file_location("w", "/tmp/c20ac/world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
over = json.loads(sys.argv[1]); seed = int(sys.argv[2]); T = float(sys.argv[3])
w.P.update(over)
s = w.init(seed, w.META["size"]); n = int(T / w.P["dt"]); out = []
t0 = time.time()
for i in range(1, n + 1):
    s = w.step(s)
    if i % int(10 / w.P["dt"]) == 0:
        m = s["phi"] > 0.5; lab, k = ndimage.label(m)
        sizes = ndimage.sum(m, lab, range(1, k + 1)) if k else []
        k12 = int(sum(1 for z in sizes if z >= 12))
        out.append((round(i * w.P["dt"]), round(float(m.mean()), 3), k12))
print(json.dumps(over), seed, out, f"{time.time()-t0:.0f}s", flush=True)
