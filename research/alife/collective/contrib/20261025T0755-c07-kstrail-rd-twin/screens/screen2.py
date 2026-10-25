# like screen.py but couples beta = 20*kh (fixed static strength) and tracks spot centroids
import sys, json, importlib.util, itertools, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import ndimage
spec = importlib.util.spec_from_file_location("w", sys.argv[1]); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
grid = json.loads(sys.argv[2]); T = float(sys.argv[3]); out = sys.argv[4]; N = int(sys.argv[5]) if len(sys.argv) > 5 else 128
keys = list(grid); combos = list(itertools.product(*grid.values()))
fig, axs = plt.subplots(len(combos), 4, figsize=(9, 2.3*len(combos))); axs = np.atleast_2d(axs)
base = dict(w.P)
for i, c in enumerate(combos):
    pp = dict(base); pp.update(dict(zip(keys, c)))
    if "kh" in keys: pp["beta"] = 20 * pp["kh"]
    w.P.clear(); w.P.update(pp)
    s = w.init(int(pp.get("seed", 0)), (N, N)); nsteps = int(T / pp["dt"])
    trail = np.zeros((N, N)); j = 0
    for n in range(1, nsteps+1):
        s = w.step(s)
        if n % 200 == 0:
            u = w.fields(s)[0]; trail = np.maximum(trail * 0.0 + trail, (u > 0.5) * n)
        if n * pp["dt"] >= T * (j+1) / 3 - 1e-9 and j < 3:
            u = w.fields(s)[0]; lab, k = ndimage.label(u > 0.5)
            axs[i, j].imshow(u, vmin=0, vmax=1, cmap="magma"); axs[i, j].set_title(f"t={n*pp['dt']:.0f} n={k}", fontsize=6); j += 1
    axs[i, 3].imshow(trail, cmap="viridis"); axs[i, 3].set_title("last time u>0.5 (path)", fontsize=6)
    axs[i, 0].set_ylabel(str(dict(zip(keys, c))), fontsize=5)
    for a in axs[i]: a.set_xticks([]); a.set_yticks([])
    print(dict(zip(keys, c)), "comps", k, "mean", float(u.mean()), flush=True)
plt.tight_layout(); plt.savefig(out, dpi=100)
