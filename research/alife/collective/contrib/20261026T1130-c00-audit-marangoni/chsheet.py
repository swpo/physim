"""Per-channel sheet: rows = 4 times; columns = phi, surfactant s, cargo c (fixed scale cmax, and log scale), [shadow s2];
each with the phi=0 contour drawn, plus a 2x zoom of the cargo around one body. usage: chsheet.py frames.npz out.png title [cmax] [smax]"""
import sys, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage
F = np.load(sys.argv[1]); R = F["render"].astype(np.float32); rf = list(F["render_f"])
out, title = sys.argv[2], sys.argv[3]
cmax = float(sys.argv[4]) if len(sys.argv) > 4 else float(np.percentile(R[:, 3], 99.5))
smax = float(sys.argv[5]) if len(sys.argv) > 5 else float(np.percentile(R[:, 2], 99.5))
C = R.shape[1]
ks = [int(round(x)) for x in np.linspace(len(rf) * 0.15, len(rf) - 1, 4)]
cols = ["phi", "ring s", "cargo c (lin)", "cargo c (log10)"] + (["shadow s2"] if C > 4 else []) + ["cargo zoom"]
fig, ax = plt.subplots(len(ks), len(cols), figsize=(3.0 * len(cols), 3.0 * len(ks)))
for r, k in enumerate(ks):
    phi = R[k, 0]
    lab, n = ndimage.label(phi > 0); sizes = ndimage.sum(np.ones_like(phi), lab, range(1, n + 1))
    j = int(np.argmax(sizes)) + 1 if n else 0
    cy, cx = ndimage.center_of_mass(lab == j) if n else (64, 64)
    imgs = [(phi, "gray", -1, 1), (R[k, 2], "magma", 0, smax), (R[k, 3], "viridis", 0, cmax),
            (np.log10(np.maximum(R[k, 3], 1e-4)), "viridis", -3, np.log10(cmax))]
    if C > 4: imgs.append((R[k, 4], "magma", 0, smax))
    for cc, (im, cm, lo, hi) in enumerate(imgs):
        a = ax[r, cc]; a.imshow(im, cmap=cm, vmin=lo, vmax=hi, interpolation="nearest")
        a.contour(phi, [0], colors="cyan" if cc else "red", linewidths=0.5); a.set_xticks([]); a.set_yticks([])
        if r == 0: a.set_title(cols[cc], fontsize=9)
    a = ax[r, -1]
    sh = np.roll(np.roll(R[k, 3], 64 - int(cy), 0), 64 - int(cx), 1)[40:88, 40:88]
    ph = np.roll(np.roll(phi, 64 - int(cy), 0), 64 - int(cx), 1)[40:88, 40:88]
    s_ = np.roll(np.roll(R[k, 2], 64 - int(cy), 0), 64 - int(cx), 1)[40:88, 40:88]
    a.imshow(sh, cmap="viridis", vmin=0, vmax=cmax, interpolation="nearest")
    a.contour(ph, [0], colors="red", linewidths=0.8); a.contour(s_, [0.5 * smax], colors="magenta", linewidths=0.6)
    a.set_xticks([]); a.set_yticks([])
    if r == 0: a.set_title(cols[-1] + " (red phi=0, magenta s=smax/2)", fontsize=8)
    ax[r, 0].set_ylabel(f"frame {rf[k]}", fontsize=9)
fig.suptitle(f"{title}  (cargo scale 0..{cmax:.2f}, s scale 0..{smax:.2f})", fontsize=11)
fig.tight_layout(); fig.savefig(out, dpi=70)
