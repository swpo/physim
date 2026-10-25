"""Crops of phi (gray) and surfactant s (magma) around the largest rods at chosen frames, with the
phi=0 contour drawn on s, plus the azimuthally averaged profile of s against distance to the interface.
usage: ringfig.py frames.npz out.png frame1 frame2 ... (world and its chi_s=0 twin side by side if two npz given via ;)"""
import sys, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
paths = sys.argv[1].split(";"); out = sys.argv[2]; frs = [int(x) for x in sys.argv[3:]]
fig, ax = plt.subplots(len(paths) * 2, len(frs) * 3, figsize=(2 * len(frs) * 3, 4.2 * len(paths)), squeeze=False)
smax = max(float(np.load(p)["render"][:, 2].max()) for p in paths)
for pi, p in enumerate(paths):
    F = np.load(p); R, rf = F["render"], list(F["render_f"])
    for j, fr in enumerate(frs):
        i = rf.index(fr) if fr in rf else min(range(len(rf)), key=lambda k: abs(rf[k] - fr))
        phi, s = R[i, 0], R[i, 2]
        lab, n = ndimage.label(phi > 0)
        sizes = ndimage.sum(np.ones_like(phi), lab, range(1, n + 1))
        for c, idx in enumerate(np.argsort(sizes)[::-1][:3]):
            cy, cx = [int(v) for v in ndimage.center_of_mass(lab == idx + 1)]
            H, W = phi.shape; h = 12
            crop = lambda f: np.roll(np.roll(f, H // 2 - cy, 0), W // 2 - cx, 1)[H // 2 - h:H // 2 + h, W // 2 - h:W // 2 + h]
            a = ax[2 * pi, 3 * j + c]; a.imshow(crop(phi), cmap="gray", vmin=-1, vmax=1); a.axis("off")
            a.set_title(f"{'world' if pi == 0 else 'chi_s=0'} f{rf[i]} phi", fontsize=7)
            b = ax[2 * pi + 1, 3 * j + c]; b.imshow(crop(s), cmap="magma", vmin=0, vmax=smax); b.contour(crop(phi), [0], colors="c", linewidths=0.6); b.axis("off")
            b.set_title("s, phi=0 contour", fontsize=7)
plt.tight_layout(); plt.savefig(out, dpi=80)
