"""Fuel fork from one shared state: run world.py to t_fork, then branch
fed (unchanged), fork (kF=0 everywhere) and fork_d0 (kF=0 and enzyme turnover d=0) for T_after.
usage: python fork.py SEED T_FORK T_AFTER OUTPREFIX"""
import sys, os, json, copy, importlib.util
import numpy as np
from scipy import ndimage
seed, tf, ta, out = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(__file__) or ".", "world.py"))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, w.META["size"])
while s["t"] < tf - 1e-9:
    w.step(s)
def count(e):
    lab, n = ndimage.label(e > 0.5, structure=np.ones((3, 3)))
    return n, float((e > 0.5).sum())
arms = {"fed": {}, "fork": {"fork_t": tf}, "fork_d0": {"fork_t": tf, "fork_d": 0.0}}
res, snaps = {}, {}
times = [0, 100, 200, 400, 800, ta]
for name, mod in arms.items():
    a = copy.deepcopy(s); a["par"] = dict(s["par"], **mod)
    log, sn = [], []
    k = 0
    while a["t"] < tf + ta - 1e-9:
        dt_rel = a["t"] - tf
        if k % 500 == 0:
            n, area = count(a["e"]); log.append((round(a["t"]), n, area, float(a["F"].mean()), float(a["e"].max())))
        if any(abs(dt_rel - x) < 0.05 for x in times):
            sn.append((round(dt_rel), a["e"].copy()))
        w.step(a); k += 1
    n, area = count(a["e"]); log.append((round(a["t"]), n, area, float(a["F"].mean()), float(a["e"].max())))
    sn.append((round(a["t"] - tf), a["e"].copy()))
    res[name] = log; snaps[name] = sn
json.dump({"seed": seed, "t_fork": tf, "columns": ["t", "bodies", "body_area_px", "mean_F", "max_e"], "arms": res}, open(out + "_counts.json", "w"))
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
nc = max(len(v) for v in snaps.values())
fig, ax = plt.subplots(3, nc, figsize=(2.0 * nc, 6.4))
for i, name in enumerate(arms):
    for j in range(nc):
        ax[i, j].axis("off")
        if j < len(snaps[name]):
            tt, im = snaps[name][j]; ax[i, j].imshow(im, cmap="magma", vmin=0, vmax=1)
            n = ndimage.label(im > 0.5, structure=np.ones((3, 3)))[1]
            ax[i, j].set_title(f"{name} t={tf+tt:.0f} n={n}", fontsize=7)
fig.suptitle(f"seed {seed}: enzyme e, fuel fork at t={tf:.0f} (rows: fed twin, kF=0, kF=0 and turnover d=0)", fontsize=8)
fig.tight_layout(); fig.savefig(out + ".png", dpi=70)
for name in res: print(name, res[name][0], res[name][len(res[name])//2], res[name][-1])
