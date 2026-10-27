"""c43: share of consumer bodies (q > 0.5, area >= 4 px) that touch no prey (c_a > 0.5 dilated by 2 px), every 100 t
from T0 to T, for several WORLD_P settings on one seed.
usage: python free.py OUT.json SEED T0 T 'json list of overrides'"""
import sys, json, os, importlib.util, numpy as np
from scipy import ndimage
out, seed, T0, T, sets = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), json.loads(sys.argv[5])
here = os.path.dirname(os.path.abspath(__file__)); res = {}
for ov in sets:
    os.environ["WORLD_P"] = json.dumps(ov)
    spec = importlib.util.spec_from_file_location("w", os.path.join(here, "world.py")); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
    s = w.init(seed, w.META["size"]); dt = w.P["dt"]; n = int(T / dt); ev = int(100 / dt); rows = []
    for i in range(n + 1):
        if i * dt >= T0 and i % ev == 0:
            F = w.fields(s); prey = ndimage.binary_dilation(F[0] > 0.5, iterations=2)
            lab, k = ndimage.label(F[1] > 0.5); a = np.bincount(lab.ravel())
            ids = [j for j in range(1, k + 1) if a[j] >= 4]
            free = [j for j in ids if not prey[lab == j].any()]
            rows.append((round(i * dt), len(ids), len(free)))
        if i < n: w.step(s)
    tot = sum(r[1] for r in rows); fr = sum(r[2] for r in rows)
    res[json.dumps(ov)] = {"rows": rows, "free_share": fr / max(tot, 1)}; print(ov, round(fr / max(tot, 1), 3), rows[-1], flush=True)
json.dump(res, open(out, "w"), indent=0)
