"""(c32) Branched fed/starved fork of c02's fch-pchemoton with per-vesicle fates.
Run seed to T0 (fed); branch: fed twin and starved arm (precursor feed F=0 from T0). Every 15 time units
segment individuals (u+1 > 0.6, holes filled, periodic), record each one's area, amphiphile, catalyst K,
and follow every individual present at T0 by maximum overlap. usage: forkfates.py seed T0 T1 out"""
import sys, os, json, copy, importlib.util
import numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("w", os.path.join(here, os.environ.get("WORLD", "world.py")))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, T0, T1, out = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
os.makedirs(out, exist_ok=True)
dt = w.P["dt"]; every = int(round(15 / dt))

def plabel(m):
    m = ndimage.binary_fill_holes(m)
    lab, n = ndimage.label(m)
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):
        for u, v in set(zip(a.tolist(), b.tolist())):
            if u and v and u != v: lab[lab == v] = u
    return lab

def seg(s):
    lab = plabel(s["u"] + 1 > 0.6)
    ids = [k for k in np.unique(lab) if k and (lab == k).sum() >= 12]
    return lab, ids

s = w.init(seed, (192, 192))
for i in range(int(round(T0 / dt))): s = w.step(s)
lab0, ids0 = seg(s)
arms = {"fed": copy.deepcopy(s), "starved": copy.deepcopy(s)}
Fsave = w.P["F"]
recs = {a: {int(k): [] for k in ids0} for a in arms}
cur = {a: {int(k): lab0 == k for k in ids0} for a in arms}
snaps = {a: [] for a in arms}
tot = {a: [] for a in arms}
nstep = int(round((T1 - T0) / dt))
for i in range(nstep + 1):
    if i % every == 0:
        t = T0 + i * dt
        for a, st in arms.items():
            lab, ids = seg(st)
            tot[a].append([t, float((st["u"] + 1).sum()), float(st["K"].sum()), len(ids)])
            for k in recs[a]:
                m = cur[a][k]
                ov = lab[m]; ov = ov[ov > 0]
                if m.sum() == 0 or len(ov) == 0:
                    recs[a][k].append([t, 0, 0.0, 0.0]); cur[a][k] = np.zeros_like(m); continue
                kk = np.bincount(ov).argmax(); mm = lab == kk; cur[a][k] = mm
                recs[a][k].append([t, int(mm.sum()), float((st["u"][mm] + 1).sum()), float(st["K"][mm].sum())])
            if i % (every * 4) == 0: snaps[a].append((t, (st["u"] + 1).copy(), st["K"].copy()))
    if i < nstep:
        for a in arms:
            w.P["F"] = Fsave if a == "fed" else 0.0
            arms[a] = w.step(arms[a])
w.P["F"] = Fsave
res = {"seed": seed, "T0": T0, "T1": T1, "totals": tot, "cells": {}}
for k in recs["fed"]:
    res["cells"][k] = {a: recs[a][k] for a in arms}
    f, sv = recs["fed"][k], recs["starved"][k]
    print(f"cell {k}: T0 area {f[0][1]} K {f[0][3]:.1f} | fed end area {f[-1][1]} K {f[-1][3]:.1f} | starved end area {sv[-1][1]} K {sv[-1][3]:.1f} lost_at {next((r[0] for r in sv if r[1]==0), None)}", flush=True)
json.dump(res, open(f"{out}/fates.json", "w"))
n = len(snaps["fed"])
fig, axs = plt.subplots(4, n, figsize=(2 * n, 8.4))
for j in range(n):
    for r, (a, q) in enumerate((("fed", 1), ("fed", 2), ("starved", 1), ("starved", 2))):
        t, U, K = snaps[a][j]
        ax = axs[r, j]; ax.set_xticks([]); ax.set_yticks([])
        ax.imshow(U if q == 1 else K, cmap="magma", vmin=0, vmax=1.6 if q == 1 else 3)
        ax.set_title(f"{a} {'u+1' if q==1 else 'K'} t={t:.0f}", fontsize=7)
fig.suptitle(f"fch-pchemoton seed {seed}: branched fork at t={T0:.0f}, fed twin vs precursor feed cut", fontsize=9)
fig.tight_layout(); fig.savefig(f"{out}/fork.png", dpi=60)
