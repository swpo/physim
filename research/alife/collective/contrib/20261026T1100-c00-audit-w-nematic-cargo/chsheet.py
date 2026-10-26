"""Per-channel view of one arm: rows = surfactant s (wall) and cargo c, columns = 6 times; full domain plus a
zoomed crop (32x32 around the largest body) at the last 2 times; phi=0 contour in cyan. Colour scales are
fixed across times (and passed explicitly so different arms share them).
usage: chsheet.py frames.npz out.png title [smax cmax]"""
import sys, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage
F = np.load(sys.argv[1]); R = F["render"].astype(np.float32); rf = list(F["render_f"])
T = len(rf); H, W = R.shape[2:]
smax = float(sys.argv[4]) if len(sys.argv) > 4 else float(np.percentile(R[T // 2:, 2], 99.5))
cmax = float(sys.argv[5]) if len(sys.argv) > 5 else float(np.percentile(R[T // 2:, 3], 99.5))
ks = [int(round(x)) for x in np.linspace(T * 0.15, T - 1, 6)]
fig, ax = plt.subplots(3, 8, figsize=(22, 8.4))
for i, k in enumerate(ks):
    for r, (ch, vm, cm) in enumerate(((2, smax, "viridis"), (3, cmax, "magma"))):
        a = ax[r, i]; a.imshow(R[k, ch], cmap=cm, vmin=0, vmax=vm, origin="lower")
        a.contour(R[k, 0], [0], colors="c", linewidths=0.4); a.set_xticks([]); a.set_yticks([])
        a.set_title(f"{'s' if ch == 2 else 'c'} f{rf[k]}", fontsize=8)
    # cargo on a log scale to show the bath level
    a = ax[2, i]; a.imshow(np.log10(np.maximum(R[k, 3], 1e-4)), cmap="magma", vmin=-3, vmax=np.log10(max(cmax, 1e-3)), origin="lower")
    a.contour(R[k, 0], [0], colors="c", linewidths=0.4); a.set_xticks([]); a.set_yticks([]); a.set_title(f"log10 c f{rf[k]}", fontsize=8)
# zoom on the largest body at the last frame and the middle frame
for j, k in enumerate((ks[3], ks[-1])):
    lab, n = ndimage.label(R[k, 0] > 0)
    if n == 0: continue
    big = np.bincount(lab.ravel())[1:].argmax() + 1
    cy, cx = [int(round(v)) for v in ndimage.center_of_mass(lab == big)]
    ys = np.arange(cy - 16, cy + 16) % H; xs = np.arange(cx - 16, cx + 16) % W
    for r, (ch, vm, cm) in enumerate(((2, smax, "viridis"), (3, cmax, "magma"))):
        a = ax[r, 6 + j]; a.imshow(R[k, ch][np.ix_(ys, xs)], cmap=cm, vmin=0, vmax=vm, origin="lower")
        a.contour(R[k, 0][np.ix_(ys, xs)], [0], colors="c", linewidths=0.8); a.set_xticks([]); a.set_yticks([])
        a.set_title(f"zoom {'s' if ch == 2 else 'c'} f{rf[k]}", fontsize=8)
    # radial-ish line profile across the body (through centroid, minor axis approx: horizontal and vertical)
    a = ax[2, 6 + j]
    row = R[k][:, cy % H, xs]
    a.plot(row[0], "c-", label="phi"); a.plot(row[2] / max(smax, 1e-9), "g-", label="s/smax"); a.plot(row[3] / max(cmax, 1e-9), "m-", label="c/cmax")
    a.axhline(0, color="k", lw=0.5); a.set_title(f"row through body f{rf[k]}", fontsize=8); a.legend(fontsize=6)
fig.suptitle(f"{sys.argv[3]}  (s scale 0..{smax:.3g}, c scale 0..{cmax:.3g})", fontsize=10)
fig.tight_layout(); fig.savefig(sys.argv[2], dpi=70)
print(sys.argv[2], "smax", smax, "cmax", cmax)
