"""Fed vs starved neural-field comets: firing f(u) and resource r at times around the cut. usage: forkfig_nf.py out.png seed label=dir ..."""
import sys, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out, seed, runs = sys.argv[1], sys.argv[2], [a.split("=", 1) for a in sys.argv[3:]]
times = [480, 520, 560, 600, 700, 1000]
fig, ax = plt.subplots(2 * len(runs), len(times), figsize=(2.0 * len(times), 2.1 * 2 * len(runs)))
for r, (lab, d) in enumerate(runs):
    F = np.load(d + "/frames.npz"); R, fr = F["render"], F["render_f"]; tt = fr * 50 * 0.1
    for c, T in enumerate(times):
        i = int(np.argmin(np.abs(tt - T)))
        ax[2 * r, c].imshow(R[i, 2], cmap="magma", vmin=0, vmax=1); ax[2 * r, c].set_title(f"{lab} f(u) t={tt[i]:.0f}", fontsize=7)
        ax[2 * r + 1, c].imshow(R[i, 3], cmap="viridis", vmin=0, vmax=1); ax[2 * r + 1, c].set_title(f"{lab} resource r", fontsize=7)
for a in ax.flat: a.set_xticks([]); a.set_yticks([])
fig.suptitle(f"seed {seed}: recovery of r cut at t=500 (everywhere, or in the left half only) vs the fed twin", fontsize=9)
plt.tight_layout(); plt.savefig(out, dpi=70)
