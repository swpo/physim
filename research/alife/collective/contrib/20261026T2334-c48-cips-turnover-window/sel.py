"""c48 selection driver for the cips-gene world: logs bodies (e>0.5, >=10 px) with their mean g1, g2 every 100 t,
the washout and swap logs, and e/g1/g2 snapshots every 2000 t. usage: python sel.py SEED T OUT (WORLD_P from env)"""
import sys, os, json, importlib.util, numpy as np
from scipy import ndimage
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py"))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, T, out = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
s = w.init(seed, w.META["size"]); H, W = s["shape"]; log, snaps, k = [], [], 0
def bodies(s):
    lab, n = ndimage.label(s["e"] > 0.5)
    for a, b in [(lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])]:
        for i, j in zip(a, b):
            if i and j and i != j: lab[lab == j] = i
    res = []
    for j in np.unique(lab):
        if not j: continue
        m = lab == j
        if m.sum() >= 10:
            yy, xx = np.nonzero(m)
            res.append([int(m.sum()), round(float(s["g1"][m].mean()), 3), round(float(s["g2"][m].mean()), 3), int(yy.mean()), int(xx.mean())])
    return res
while s["t"] < T - 1e-9:
    w.step(s); k += 1
    if k % 1000 == 0:
        log.append({"t": round(s["t"]), "bodies": bodies(s)})
    if k % 20000 == 0:
        snaps.append((round(s["t"]), s["e"].astype(np.float16), s["g1"].astype(np.float16), s["g2"].astype(np.float16)))
        json.dump({"par": {k_: v for k_, v in s["par"].items() if isinstance(v, (int, float))}, "log": log, "wash_log": s.get("wash_log", []), "swap_log": s.get("swap_log", [])}, open(out + ".json", "w"))
        np.savez_compressed(out + "_snaps.npz", t=[x[0] for x in snaps], e=np.array([x[1] for x in snaps]), g1=np.array([x[2] for x in snaps]), g2=np.array([x[3] for x in snaps]))
json.dump({"par": {k_: v for k_, v in s["par"].items() if isinstance(v, (int, float))}, "log": log, "wash_log": s.get("wash_log", []), "swap_log": s.get("swap_log", [])}, open(out + ".json", "w"))
print("done", flush=True)
