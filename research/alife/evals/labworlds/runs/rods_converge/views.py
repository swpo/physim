"""Final (50 tu) snapshots of the first two members of saved ensembles: phi, s and c, world-unit axes.
usage: views.py out.png ens1.npz ens2.npz ..."""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

files = sys.argv[2:]
fig, axs = plt.subplots(len(files) * 2, 3, figsize=(9, 3 * 2 * len(files)), squeeze=False)
for i, f in enumerate(files):
    z = np.load(f)
    for m in range(2):
        F = z["snaps"][m]
        for j, (k, name, lim) in enumerate(((0, "phi", (-1, 1)), (3, "s", (0, 0.7)), (4, "c", (0, 3)))):
            ax = axs[2 * i + m, j]
            ax.imshow(F[k], origin="lower", cmap="viridis", vmin=lim[0], vmax=lim[1], extent=(0, 128, 0, 128))
            b = z["bodies"][m]
            ax.set_title(f"{f.split('/')[-1][4:-4]} m{m} {name} bodies {b[0]}->{b[-1]}", fontsize=7)
            ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout()
plt.savefig(sys.argv[1], dpi=80)
