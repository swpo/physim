"""Crops of phi, shell s and fuel f around the 3 largest rods at one frame, for several runs
(world and its ablations), with the phi=0 contour on s and f. Also prints the mean fuel inside
rods (phi > 0.3) per run.
usage: ringfig.py out.png frame label1=frames1.npz label2=frames2.npz ..."""
import sys, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out, fr = sys.argv[1], int(sys.argv[2]); runs = [a.split("=", 1) for a in sys.argv[3:]]
fig, ax = plt.subplots(3 * len(runs), 3, figsize=(6, 6.2 * len(runs)), squeeze=False)
Rs = [np.load(p)["render"] for _, p in runs]
smax = max(float(R[:, 2].max()) for R in Rs); fmax = max(float(R[:, 3].max()) for R in Rs)
for pi, ((lab_, p), R) in enumerate(zip(runs, Rs)):
    rf = list(np.load(p)["render_f"]); i = min(range(len(rf)), key=lambda k: abs(rf[k] - fr))
    phi, s, f = R[i, 0], R[i, 2], R[i, 3]
    print(lab_, "frame", rf[i], "fuel inside rods", round(float(f[phi > 0.3].mean()), 3), "shell at interface", round(float(s[np.abs(phi) < 0.3].mean()), 3), "shell inside", round(float(s[phi > 0.6].mean()), 3))
    lab, n = ndimage.label(phi > 0)
    sizes = ndimage.sum(np.ones_like(phi), lab, range(1, n + 1))
    for c, idx in enumerate(np.argsort(sizes)[::-1][:3]):
        cy, cx = [int(v) for v in ndimage.center_of_mass(lab == idx + 1)]
        H, W = phi.shape; h = 14
        crop = lambda g: np.roll(np.roll(g, H // 2 - cy, 0), W // 2 - cx, 1)[H // 2 - h:H // 2 + h, W // 2 - h:W // 2 + h]
        for r, (g, cm, vmax, name) in enumerate([(phi, "gray", 1, "phi"), (s, "magma", smax, "shell s"), (f, "viridis", fmax, "fuel f")]):
            a = ax[3 * pi + r, c]; a.imshow(crop(g), cmap=cm, vmin=-1 if r == 0 else 0, vmax=vmax); a.axis("off")
            if r: a.contour(crop(phi), [0], colors="c", linewidths=0.6)
            a.set_title(f"{lab_} t-frame {rf[i]} {name}", fontsize=7)
plt.tight_layout(); plt.savefig(out, dpi=80)
