"""Local catalyst ablation fork for c02's FCH chemoton (c28 review).
Run seed to t_cut, then branch: (a) fed twin, (b) K erased inside one K-carrying vesicle (filled body + 4 px).
Track amphiphile mass inside the target's dilated region and in other bodies, and save snapshots."""
import sys, json, importlib.util, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
wpath, seed, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
tcut, tend, which = float(sys.argv[4]), float(sys.argv[5]), sys.argv[6] if len(sys.argv) > 6 else "maxK"
spec = importlib.util.spec_from_file_location("w", wpath); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
dt = w.P["dt"]; size = w.META["size"]
s = w.init(seed, size)
for i in range(int(round(tcut / dt))): s = w.step(s)
body = (s["u"] + 1) > 0.6
filled = ndimage.binary_fill_holes(body)
lab, n = ndimage.label(filled)
# periodic merge is ignored; choose components by K mass
Km = ndimage.sum(s["K"], lab, range(1, n + 1)); A = ndimage.sum(np.ones_like(s["K"]), lab, range(1, n + 1))
order = np.argsort(-Km)
info = [dict(lab=int(i + 1), K=float(Km[i]), area=int(A[i])) for i in order]
tgt = int(order[0] + 1) if which == "maxK" else int(order[int(which)] + 1)
region = ndimage.binary_dilation(lab == tgt, iterations=4)
import copy
branches = {"fed": copy.deepcopy(s), "kcut": copy.deepcopy(s)}
branches["kcut"]["K"][region] = 0.0
rec = {b: [] for b in branches}; snaps = {b: [] for b in branches}
times = np.arange(tcut, tend + 1e-9, 25.0)
for k, t in enumerate(times):
    for b, st in branches.items():
        um = st["u"] + 1
        rec[b].append(dict(t=float(t), tgt_u=float(um[region].sum()), tgt_K=float(st["K"][region].sum()),
                           other_u=float(um[~region].sum()), other_K=float(st["K"][~region].sum())))
        if k % 4 == 0: snaps[b].append((t, um.copy(), st["K"].copy()))
    if k + 1 < len(times):
        for b in branches:
            st = branches[b]
            for i in range(int(round(25.0 / dt))): st = w.step(st)
            branches[b] = st
json.dump(dict(seed=seed, tcut=tcut, target=tgt, components=info, region_px=int(region.sum()), rec=rec), open(f"{out}/kcut_s{seed}.json", "w"), indent=1)
ns = len(snaps["fed"]); fig, ax = plt.subplots(4, ns, figsize=(2.2 * ns, 9))
cy, cx = ndimage.center_of_mass(region)
for j in range(ns):
    for r, (b, ch) in enumerate([("fed", 1), ("fed", 2), ("kcut", 1), ("kcut", 2)]):
        t, um, K = snaps[b][j]; img = um if ch == 1 else K
        img = np.roll(np.roll(img, size[0] // 2 - int(cy), 0), size[1] // 2 - int(cx), 1)
        ax[r, j].imshow(img, cmap="magma", vmin=0, vmax=1.6 if ch == 1 else 3); ax[r, j].axis("off")
        ax[r, j].set_title(f"{b} {'u+1' if ch == 1 else 'K'} t={t:.0f}", fontsize=7)
fig.suptitle(f"seed {seed}: K erased at t={tcut:.0f} inside the target vesicle (centred) vs fed twin", fontsize=9)
fig.tight_layout(); fig.savefig(f"{out}/kcut_s{seed}.png", dpi=80)
