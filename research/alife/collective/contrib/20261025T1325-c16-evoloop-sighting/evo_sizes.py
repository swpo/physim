"""Hole-size census of an evoloop run: every loop's enclosed empty region (hole side = sqrt(area))."""
import sys, os, json, importlib.util, numpy as np
from scipy import ndimage
wp = sys.argv[1]; os.environ["WORLD_P"] = sys.argv[2]; T = int(sys.argv[3]); seed = int(sys.argv[4]); L = int(sys.argv[5]); out = sys.argv[6]
spec = importlib.util.spec_from_file_location("w", wp); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, (L, L))
def holes(g):
    z = g == 0; lab, n = ndimage.label(z)
    # merge labels across periodic edges
    for a, b in [(lab[0], lab[-1]), (lab[:, 0], lab[:, -1])]:
        for x, y in zip(a, b):
            if x and y and x != y: lab[lab == y] = x
    area = np.bincount(lab.ravel()); area[0] = 0
    bg = np.argmax(area); area[bg] = 0
    a = area[area >= 4]
    return a
rec = []; snaps = {}
for t in range(1, T + 1):
    w.step(s)
    if t % 1000 == 0:
        a = holes(s["g"]); sz = np.sqrt(a)
        h = np.bincount(np.round(sz).astype(int), minlength=20)
        rec.append({"t": t, "live": int((s["g"] > 0).sum()), "n": int(len(a)), "mean_side": round(float(sz.mean()), 2) if len(a) else None, "hist": h.tolist()})
        if t % 10000 == 0: print(t, rec[-1]["n"], rec[-1]["mean_side"], h[:16].tolist(), flush=True)
    if t in (2000, 10000, 30000, 60000, 100000, 200000): np.save(f"{out}_g{t}.npy", s["g"])
json.dump(rec, open(out + ".json", "w"))
