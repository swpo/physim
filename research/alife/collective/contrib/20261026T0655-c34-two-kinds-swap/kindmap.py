"""(c34) Kind maps: surfactant A in red, B in blue (each scaled to its 99.5th percentile), phi=0 contour in white,
at 5 times, for one or more runs. usage: kindmap.py out.png label=frames.npz [label=frames.npz ...]"""
import sys, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
runs = [a.rsplit("=", 1) for a in sys.argv[2:]]
fig, ax = plt.subplots(len(runs), 5, figsize=(15, 3.2 * len(runs)), squeeze=False)
for i, (lab, p) in enumerate(runs):
    F = np.load(p); R = F["render"].astype(np.float32); rf = list(F["render_f"]); n = len(rf)
    m = max(np.percentile(R[:, 2], 99.5), np.percentile(R[:, 3], 99.5))
    for j, k in enumerate([n // 8, n // 4, n // 2, 3 * n // 4, n - 1]):
        img = np.stack([np.clip(R[k, 2] / m, 0, 1), np.zeros_like(R[k, 2]), np.clip(R[k, 3] / m, 0, 1)], -1)
        ax[i, j].imshow(img, origin="lower"); ax[i, j].contour(R[k, 0], [0], colors="w", linewidths=0.4)
        ax[i, j].set_title(f"{lab} frame {rf[k]}", fontsize=8); ax[i, j].axis("off")
fig.suptitle("red = kind A (Marangoni swimmer), blue = kind B"); fig.tight_layout(); fig.savefig(sys.argv[1], dpi=70)
