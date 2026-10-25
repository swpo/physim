"""Montage of isolation runs: rows = theta, columns = snapshots (saved by isolate.py as .npy). usage: isomontage.py out.png seed dir"""
import sys, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out, sd, d = sys.argv[1], sys.argv[2], sys.argv[3]
ths = ["0.5", "0.495", "0.49", "0.485", "0.48"]; cols = [0, 2, 4, 6, 8, 11]; times = np.linspace(0, 600, 12).round().astype(int)
fig, ax = plt.subplots(len(ths), len(cols), figsize=(2.1 * len(cols), 2.2 * len(ths)))
for r, th in enumerate(ths):
    A = np.load(f"{d}/iso_{th}_{sd}.npy").astype(float)
    for c, j in enumerate(cols):
        ax[r, c].imshow(A[j], cmap="magma", vmin=0, vmax=1); ax[r, c].set_xticks([]); ax[r, c].set_yticks([])
        ax[r, c].set_title(f"theta {th}, +{times[j]}", fontsize=8)
fig.suptitle(f"world run at each theta to t=200 (seed {sd}), then only the median-size body kept (rest reset to 0); firing f(u)", fontsize=9)
plt.tight_layout(); plt.savefig(out, dpi=70)
