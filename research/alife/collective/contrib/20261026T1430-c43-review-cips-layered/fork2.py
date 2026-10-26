"""c43: graded fuel fork from one shared state. Run world.py to T_FORK, then branch arms with the fuel
regrowth rate kF lowered to the listed values (kF=0.2 is the fed twin) for T_AFTER; count bodies (e>0.5,
8-connected), body area and mean F every 100 t.
usage: python fork2.py SEED T_FORK T_AFTER OUTPREFIX"""
import sys, os, json, copy, importlib.util
import numpy as np
from scipy import ndimage
seed, tf, ta, out = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py"))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, w.META["size"])
while s["t"] < tf - 1e-9:
    w.step(s)
def count(e):
    lab, n = ndimage.label(e > 0.5, structure=np.ones((3, 3)))
    return n, float((e > 0.5).sum())
arms = {"kF0.2_fed": 0.2, "kF0.1": 0.1, "kF0.05": 0.05, "kF0.02": 0.02}
res, snaps = {}, {}
for name, kf in arms.items():
    a = copy.deepcopy(s); a["par"] = dict(s["par"], kF=kf)
    log, sn = [], []; k = 0
    while a["t"] < tf + ta - 1e-9:
        if k % 1000 == 0:
            n, area = count(a["e"]); log.append((round(a["t"]), n, area, float(a["F"].mean())))
            if k % 5000 == 0: sn.append((round(a["t"]), a["e"].copy()))
        w.step(a); k += 1
    n, area = count(a["e"]); log.append((round(a["t"]), n, area, float(a["F"].mean()))); sn.append((round(a["t"]), a["e"].copy()))
    res[name] = log; snaps[name] = sn; print(name, log[0], log[-1], flush=True)
json.dump({"seed": seed, "t_fork": tf, "columns": ["t", "bodies", "body_area_px", "mean_F"], "arms": res}, open(out + "_counts.json", "w"), indent=0)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
nc = max(len(v) for v in snaps.values())
fig, ax = plt.subplots(len(arms), nc, figsize=(2.0 * nc, 2.1 * len(arms)))
for i, name in enumerate(arms):
    for j in range(nc):
        ax[i, j].axis("off")
        if j < len(snaps[name]):
            tt, im = snaps[name][j]; ax[i, j].imshow(im, cmap="magma", vmin=0, vmax=1)
            ax[i, j].set_title(f"{name} t={tt} n={count(im)[0]}", fontsize=7)
fig.suptitle(f"seed {seed}: enzyme e, fuel regrowth lowered at t={tf:.0f}", fontsize=8)
fig.tight_layout(); fig.savefig(out + ".png", dpi=70)
