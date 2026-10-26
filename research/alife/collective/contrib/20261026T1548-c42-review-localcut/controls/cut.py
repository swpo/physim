"""Local fuel cut on one body: run world.py to T_CUT, pick the body whose nearest other body is farthest,
then branch (a) fed twin and (b) kF=0 inside a disk of radius R_CUT around that body only.
Records the target's enzyme mass inside the disk and the number of bodies outside it.
usage: python cut.py SEED T_CUT T_AFTER OUT"""
import sys, os, json, copy, importlib.util, numpy as np
from scipy import ndimage
seed, tc, ta, out = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py"))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, w.META["size"]); H, W = s["shape"]
while s["t"] < tc - 1e-9: w.step(s)
def bodies(e):
    # periodic labelling: label a 2x2 tiling, keep bodies whose centroid lies in the first tile
    E = np.tile(e, (2, 2)); lab, n = ndimage.label(E > 0.5, structure=np.ones((3, 3)))
    cs = ndimage.center_of_mass(E > 0.5, lab, range(1, n + 1))
    return [(cy % H, cx % W) for cy, cx in cs if cy < H + 1e-9 and cx < W + 1e-9 and (cy >= H / 2 or True)]
def uniq(cs):
    u = []
    for c in cs:
        if all(min(abs(c[0] - d[0]), H - abs(c[0] - d[0])) ** 2 + min(abs(c[1] - d[1]), W - abs(c[1] - d[1])) ** 2 > 4 for d in u): u.append(c)
    return u
cs = uniq(bodies(s["e"]))
def pd(a, b):
    dy = min(abs(a[0] - b[0]), H - abs(a[0] - b[0])); dx = min(abs(a[1] - b[1]), W - abs(a[1] - b[1])); return (dy * dy + dx * dx) ** 0.5
nn = [min(pd(c, d) for d in cs if d is not c) for c in cs]
i = int(np.argmax(nn)); tgt = cs[i]; R = max(14.0, 0.6 * nn[i])
yy, xx = np.mgrid[0:H, 0:W]
dy = (yy - tgt[0] + H / 2) % H - H / 2; dx = (xx - tgt[1] + W / 2) % W - W / 2
disk = dy * dy + dx * dx <= R * R
arms = {"fed": {}, "cut": {"cut_t": tc, "cut_r": R, "cut_y": tgt[0], "cut_x": tgt[1]}}
res, snaps = {}, {}
for name, mod in arms.items():
    a = copy.deepcopy(s); a["par"] = dict(s["par"], **mod)
    log, sn, k = [], [], 0
    while a["t"] <= tc + ta + 1e-9:
        if k % 250 == 0:
            e = a["e"]; out_n = len(uniq([c for c in bodies(np.where(disk, 0, e))]))
            log.append({"t": round(a["t"]), "target_enzyme_in_disk": float((e * disk).sum()), "target_px_e>0.5": int(((e > 0.5) & disk).sum()),
                        "F_in_disk": float(a["F"][disk].mean()), "bodies_outside_disk": out_n})
        if k % 1500 == 0: sn.append((round(a["t"]), a["e"].copy(), a["F"].copy()))
        w.step(a); k += 1
    res[name] = log; snaps[name] = sn
json.dump({"seed": seed, "t_cut": tc, "target_centroid": tgt, "nearest_other_body": nn[i], "cut_radius": R, "arms": res}, open(out + ".json", "w"), indent=0)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
nc = len(snaps["fed"]); fig, ax = plt.subplots(3, nc, figsize=(1.9 * nc, 6))
th = np.linspace(0, 2 * np.pi, 100)
for j in range(nc):
    for r, (name, ch, cm) in enumerate([("fed", 1, "magma"), ("cut", 1, "magma"), ("cut", 2, "viridis")]):
        t, e, F = snaps[name][j]; img = e if ch == 1 else F
        ax[r, j].imshow(np.roll(np.roll(img, int(H / 2 - tgt[0]), 0), int(W / 2 - tgt[1]), 1), cmap=cm, vmin=0, vmax=1)
        ax[r, j].plot(W / 2 + R * np.cos(th), H / 2 + R * np.sin(th), "w--", lw=0.6); ax[r, j].axis("off")
        ax[r, j].set_title(f"{name} {'e' if ch == 1 else 'F'} t={t}", fontsize=7)
fig.suptitle(f"seed {seed}: kF=0 only inside the dashed disk (r={R:.0f}) around one body from t={tc:.0f}; rows: fed twin e, cut e, cut F (box recentred on the target)", fontsize=8)
fig.tight_layout(); fig.savefig(out + ".png", dpi=70)
for name in res: print(name, res[name][0], res[name][-1])
