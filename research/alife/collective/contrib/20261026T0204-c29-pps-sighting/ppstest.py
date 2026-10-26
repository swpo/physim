import sys, time, importlib.util, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(int(sys.argv[1]), None); t0 = time.time(); T = [0, 2000, 5000, 10000, 20000, 30000]
fig, axs = plt.subplots(1, len(T), figsize=(4 * len(T), 4)); k = 0; cols = np.array(["green", "brown", "blue", "gold"])
for t in range(T[-1] + 1):
    if t in T:
        p = w.particles(s); ax = axs[k]; k += 1
        ax.scatter(p[:, 0], p[:, 1], s=0.3, c=cols[p[:, 2].astype(int)]); ax.set_title(f"t={t}  N>35: {(s['N']>35).sum()}", fontsize=8); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
        print(t, round(time.time() - t0, 1), np.bincount(p[:, 2].astype(int), minlength=4), flush=True)
    if t < T[-1]: s = w.step(s)
fig.tight_layout(); fig.savefig(sys.argv[2], dpi=60)
