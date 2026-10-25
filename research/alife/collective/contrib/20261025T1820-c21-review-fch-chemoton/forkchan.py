"""(c21) FCH chemoton fed vs feed-cut twin: amphiphile u+1 and catalyst K at fixed times, plus channel totals.
usage: forkchan.py fed_dir starve_dir out.png  (labkit dirs with frames.npz; frame time = 3 x frame index)"""
import sys, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
A, B = np.load(sys.argv[1] + "/frames.npz"), np.load(sys.argv[2] + "/frames.npz")
times = [60, 150, 297, 330, 400, 500, 600]
fig, ax = plt.subplots(5, len(times), figsize=(2.1 * len(times), 11))
kmax = float(np.percentile(A["render"][:, 2], 99.9))
for r0, F, nm in ((0, A, "fed"), (2, B, "cut")):
    rf = np.array(F["render_f"]) * 3
    for c, t in enumerate(times):
        i = int(np.argmin(abs(rf - t)))
        ax[r0, c].imshow(F["render"][i, 0], cmap="magma", vmin=0, vmax=2); ax[r0, c].set_title(f"{nm} u+1 t={rf[i]}", fontsize=7)
        ax[r0 + 1, c].imshow(F["render"][i, 2], cmap="inferno", vmin=0, vmax=kmax); ax[r0 + 1, c].set_title(f"{nm} K t={rf[i]}", fontsize=7)
for a in ax[:4].ravel(): a.axis("off")
for a in ax[4]: a.remove()
g = fig.add_subplot(5, 1, 5)
for F, nm, ls in ((A, "fed", "-"), (B, "cut at t=300", "--")):
    rf = np.array(F["render_f"]) * 3; R = F["render"]
    g.plot(rf, R[:, 0].sum((1, 2)) / R[0, 0].sum(), "C0" + ls, label="amphiphile u+1, " + nm)
    g.plot(rf, R[:, 2].sum((1, 2)) / max(R[:, 2].sum((1, 2)).max(), 1e-9), "C3" + ls, label="catalyst K (rel. max), " + nm)
g.set_xlabel("t"); g.legend(fontsize=7); g.set_title("channel totals (render units)", fontsize=8)
fig.tight_layout(); fig.savefig(sys.argv[3], dpi=70)
