"""Random fission strips: pick elongated bodies (about to pinch) at random frames >= fmin, show u and log c in a
crop over the next frames, with each body's mean c / outside. Also prints the share of body-frames >= 2x.
Usage: strips.py pack_dir out.png fmin seed"""
import sys, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import ndimage
d, out, fmin, sd = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
F = np.load(d + "/frames.npz"); R = F["render"]; rf = list(F["render_f"]); thr = 0.8
share = []
def bodies(i):
    u, c = R[i, 0], R[i, 1]; b = u > thr; lab, n = ndimage.label(b)
    far = ~ndimage.binary_dilation(b, iterations=3); co = c[far].mean()
    return lab, n, ndimage.mean(c, lab, range(1, n + 1)) / co, co
for i in range(5, len(rf)):
    _, n, per, _ = bodies(i); share += list(per >= 2)
print(f"{d}: share of body-frames >= 2x (frames 5-end): {np.mean(share):.3f} of {len(share)}")
rng = np.random.default_rng(sd); picks = []
while len(picks) < 4:
    i = int(rng.integers(fmin, len(rf) - 13)); lab, n, _, _ = bodies(i)
    for k in rng.permutation(n) + 1:
        ys, xs = np.nonzero(lab == k)
        if len(ys) < 20: continue
        cov = np.cov(np.vstack([ys, xs])); ev = np.linalg.eigvalsh(cov)
        if all(abs(i - p[0]) > 3 for p in picks) and ev[1] / ev[0] > 2.5 and 12 < ys.mean() < 116 and 12 < xs.mean() < 116:
            picks.append((i, int(ys.mean()), int(xs.mean()))); break
fig, ax = plt.subplots(8, 7, figsize=(12, 14))
for r, (i, y, x) in enumerate(picks):
    for j, f in enumerate(range(i - 2, i + 12, 2)):
        lab, n, per, co = bodies(f); sl = (slice(y - 12, y + 12), slice(x - 12, x + 12))
        ids = np.unique(lab[sl]); ids = ids[ids > 0]
        ax[2 * r, j].imshow(R[f, 0][sl], cmap="magma", vmin=0, vmax=2.6); ax[2 * r, j].set_title(f"frame {rf[f]}", fontsize=7)
        ax[2 * r + 1, j].imshow(np.log10(R[f, 1][sl] + 1e-3), cmap="viridis", vmin=-1, vmax=3)
        ax[2 * r + 1, j].set_title("x" + ",".join(f"{per[k-1]:.0f}" for k in ids), fontsize=7)
for a in ax.flat: a.axis("off")
fig.suptitle(f"{d}: random pinching bodies; top u, bottom log10 c; 'xN' = each body's mean c / outside", fontsize=9)
plt.tight_layout(); plt.savefig(out, dpi=80)
