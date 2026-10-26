"""(c34) Look at the surfactant ring directly. Top row: the s channel alone (own colour scale) with the
phi=0 contour, at 4 times. Bottom row: 4 zoomed crops of the largest bodies at the last of those times, and
the signed-distance profile of s (mean s in 0.5-unit bins of distance d to the phi=0 contour, d<0 inside)
pooled over frames >= 20. usage: ringview.py frames.npz out.png [dx] [title]"""
import sys, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage
F = np.load(sys.argv[1]); R = F["render"].astype(np.float32); rf = list(F["render_f"])
dx = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
title = sys.argv[4] if len(sys.argv) > 4 else sys.argv[1]
n = len(rf); ks = [n // 5, 2 * n // 5, 3 * n // 5, n - 1]
smax = np.percentile(R[ks, 2], 99.5)
fig, ax = plt.subplots(2, 5, figsize=(17, 7))
for a, k in zip(ax[0], ks):
    a.imshow(R[k, 2], cmap="magma", vmin=0, vmax=smax, origin="lower")
    a.contour(R[k, 0], [0], colors="c", linewidths=0.6)
    a.set_title(f"s, frame {rf[k]}"); a.axis("off")
phi = R[ks[-1], 0]; lab, nl = ndimage.label(phi > 0)
sizes = ndimage.sum(np.ones_like(phi), lab, range(1, nl + 1)); order = np.argsort(sizes)[::-1][:4]
H, W = phi.shape; h = int(14 / dx)
for a, j in zip(ax[1][:4], order):
    cy, cx = [int(c) for c in ndimage.center_of_mass(lab == j + 1)]
    ys = np.arange(cy - h, cy + h) % H; xs = np.arange(cx - h, cx + h) % W
    a.imshow(R[ks[-1], 2][np.ix_(ys, xs)], cmap="magma", vmin=0, vmax=smax, origin="lower")
    a.contour(phi[np.ix_(ys, xs)], [0], colors="c", linewidths=1)
    a.set_title(f"body {j + 1}, s with phi=0"); a.axis("off")
bins = np.arange(-6, 8.01, 0.5) + 0.25; acc = np.zeros(len(bins) - 1); cnt = np.zeros(len(bins) - 1)
for k, f in enumerate(rf):
    if f < 20 or k % 5: continue
    ins = R[k, 0] > 0
    d = dx * np.where(ins, -(ndimage.distance_transform_edt(ins) - 0.5), ndimage.distance_transform_edt(~ins) - 0.5)
    i = np.digitize(d.ravel(), bins) - 1; ok = (i >= 0) & (i < len(acc))
    acc += np.bincount(i[ok], R[k, 2].ravel()[ok], len(acc)); cnt += np.bincount(i[ok], minlength=len(acc))
c = 0.5 * (bins[1:] + bins[:-1]); keep = cnt > 0; c, prof = c[keep], acc[keep] / cnt[keep]
ax[0][4].axis("off")
ax[1][4].plot(c, prof, "k.-"); ax[1][4].axvline(0, color="c"); ax[1][4].set_xlabel("signed distance to phi=0 (d<0 inside)")
ax[1][4].set_ylabel("mean s"); ax[1][4].set_title("s profile, frames >= 20")
fig.suptitle(title); fig.tight_layout(); fig.savefig(sys.argv[2], dpi=70)
print("peak at d =", c[np.argmax(prof)], " s(peak)/s(d<-1.5) =", round(prof.max() / prof[c <= -1.5][-3:].mean(), 2))
