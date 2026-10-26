"""c43: prey and consumer body counts (c_a > 0.5, q > 0.5) and max q, fed twin (pack/seedS) vs prey-removal fork
(efork_t3000/seedS, prey set to phi_a=-1 and its production stopped at t=3000), from labkit frames.
usage: python forkplot.py OUT.png SEED [SEED ...]"""
import sys, json, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out, seeds = sys.argv[1], [int(x) for x in sys.argv[2:]]
fig, ax = plt.subplots(1, 2 * len(seeds), figsize=(5 * len(seeds), 2.6)); res = {}
for k, s in enumerate(seeds):
    for name, T, ls in (("pack", 12000, "-"), ("efork_t3000", 8000, "--")):
        R = np.load(f"{name}/seed{s}/frames.npz")["render"]; ts = np.linspace(0, T, len(R))
        sel = (ts >= 2000) & (ts <= 5000)
        npre = [ndimage.label(R[i][0] > 0.5)[1] for i in np.nonzero(sel)[0]]
        ncon = [ndimage.label(R[i][1] > 0.5)[1] for i in np.nonzero(sel)[0]]
        qmax = [float(R[i][1].max()) for i in np.nonzero(sel)[0]]
        res[f"{name}_s{s}"] = {"t": [round(x) for x in ts[sel]], "prey": npre, "consumers": ncon, "q_max": qmax}
        ax[2 * k].plot(ts[sel], ncon, "r" + ls, label=f"consumers {name}"); ax[2 * k].plot(ts[sel], npre, "g" + ls, label=f"prey {name}")
        ax[2 * k + 1].plot(ts[sel], qmax, "r" + ls, label=f"max q {name}")
    ax[2 * k].set_title(f"seed {s}: bodies (solid fed, dashed prey removed at t=3000)", fontsize=7); ax[2 * k].legend(fontsize=5)
    ax[2 * k + 1].set_title(f"seed {s}: max consumer enzyme q", fontsize=7); ax[2 * k + 1].legend(fontsize=5)
fig.tight_layout(); fig.savefig(out, dpi=80); json.dump(res, open(out.replace(".png", ".json"), "w"))
