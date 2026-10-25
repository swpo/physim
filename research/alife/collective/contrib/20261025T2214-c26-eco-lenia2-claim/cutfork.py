"""Local food cut on one cell with a fed twin (RUBRIC L4c: a local ablation that cuts one individual's
supply while its neighbours keep theirs).

usage: python cutfork.py world.py seed species(A|B) t_fork t_after out_prefix [radius=12] [rank=0.5]

Runs the world to t_fork, picks the cell of `species` (core channel > 0.35, area >= 20) at the given
size rank (0.5 = median), copies the state, and in the copy holds the food at 0 inside a disk of
`radius` around that cell for the rest of the run. Both copies run on in lockstep. Every 5 t it records,
in both arms, the species' core mass inside the disk (the target) and the number of cells of each
species in the domain. Writes out_prefix.json and out_prefix.png (crops of both arms + mass curves).
"""
import copy
import json
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage

sys.path.insert(0, "/home/user/physim/research/alife")
from labkit.world import load_world  # noqa: E402

args = [a for a in sys.argv[1:] if "=" not in a]
opt = dict(a.split("=") for a in sys.argv[1:] if "=" in a)
W = load_world(args[0])
seed, sp, tf, ta, out = int(args[1]), args[2], float(args[3]), float(args[4]), args[5]
rad, rank = float(opt.get("radius", 12)), float(opt.get("rank", 0.5))
dt = 0.1
s = W.init(seed, W.META["size"])
for _ in range(int(round(tf / dt))):
    s = W.step(s)
H, Wd = s["F"].shape
X = s[sp][0]
lab, n = ndimage.label(X > 0.35)
ids = np.arange(1, n + 1)
area = ndimage.sum(np.ones_like(X), lab, ids)
ok = ids[area >= 20]
j = ok[np.argsort(area[ok - 1])[int(rank * (len(ok) - 1))]]
cy, cx = [float(v) for v in ndimage.center_of_mass(lab == j)]
yy = np.minimum(np.abs(np.arange(H) - cy), H - np.abs(np.arange(H) - cy))[:, None]
xx = np.minimum(np.abs(np.arange(Wd) - cx), Wd - np.abs(np.arange(Wd) - cx))[None, :]
disk = (yy ** 2 + xx ** 2) <= rad ** 2
cut = copy.deepcopy(s)
cut["cut"] = disk
cut["F"][disk] = 0
if "FB" in cut:
    cut["FB"][disk] = 0


def count(Xc):
    lab, k = ndimage.label(Xc > 0.35)
    if not k:
        return 0
    a = ndimage.sum(np.ones_like(Xc), lab, np.arange(1, k + 1))
    return int((a >= 20).sum())


rows, crops = [], []
for i in range(int(round(ta / dt)) + 1):
    if i % 50 == 0:
        t = tf + i * dt
        r = [round(t, 1)]
        for st in (s, cut):
            r += [float(st[sp][0][disk].sum()), count(st["A"][0]), count(st["B"][0]), float(st["F"][disk].mean())]
        rows.append(r)
        if i % 500 == 0:
            c = []
            for st in (s, cut):
                img = np.stack([np.clip(st["A"][0], 0, 1), np.clip(st["F"], 0, 1) * 0.5, np.clip(st["B"][0], 0, 1)], -1)
                img = np.roll(np.roll(img, H // 2 - int(cy), 0), Wd // 2 - int(cx), 1)[H // 2 - 32:H // 2 + 32, Wd // 2 - 32:Wd // 2 + 32]
                c.append(img)
            crops.append((t, c))
    s = W.step(s)
    cut = W.step(cut)
m0 = rows[0][1]
res = dict(seed=seed, species=sp, t_fork=tf, center=[cy, cx], radius=rad, target_area=float(area[j - 1]),
           cols=["t", "fed_mass", "fed_nA", "fed_nB", "fed_food", "cut_mass", "cut_nA", "cut_nB", "cut_food"], rows=rows,
           fed_final_frac=rows[-1][1] / m0, cut_final_frac=rows[-1][5] / m0,
           cut_below10_at=next((r[0] for r in rows if r[5] < 0.1 * m0), None))
json.dump(res, open(out + ".json", "w"))
print(json.dumps({k: v for k, v in res.items() if k not in ("rows", "cols")}))
fig, ax = plt.subplots(2, len(crops) + 1, figsize=(2.2 * (len(crops) + 1), 4.6))
for k, (t, c) in enumerate(crops):
    for r in range(2):
        a = ax[r, k]
        a.imshow(c[r])
        a.add_patch(plt.Circle((32, 32), rad, fill=False, color="w", lw=0.8, ls="--"))
        a.set_title(f"{'fed' if r == 0 else 'cut'} t={t:.0f}", fontsize=8)
        a.axis("off")
R = np.array(rows)
ax[0, -1].plot(R[:, 0], R[:, 1] / m0, "k", label="fed twin")
ax[0, -1].plot(R[:, 0], R[:, 5] / m0, "r", label="food cut")
ax[0, -1].set_title(f"{sp} core mass in disk / at fork", fontsize=8)
ax[0, -1].legend(fontsize=7)
ax[1, -1].plot(R[:, 0], R[:, 2 if sp == "A" else 3], "k")
ax[1, -1].plot(R[:, 0], R[:, 6 if sp == "A" else 7], "r")
ax[1, -1].set_title(f"{sp} cells in domain", fontsize=8)
plt.tight_layout()
plt.savefig(out + ".png", dpi=70)
