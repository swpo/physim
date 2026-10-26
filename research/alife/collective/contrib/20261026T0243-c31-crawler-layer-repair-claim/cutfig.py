import sys, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out, pre = sys.argv[1], sys.argv[2]; ts = sys.argv[3:]
fig, ax = plt.subplots(4, len(ts), figsize=(2.4*len(ts), 9.6), squeeze=False)
for j, t in enumerate(ts):
    for i, (arm, key, cm, vm) in enumerate((("cut", "s", "magma", 0.7), ("cut", "rho", "viridis", 1.2), ("twin", "s", "magma", 0.7), ("twin", "rho", "viridis", 1.2))):
        d = np.load(f"{pre}_{arm}_t{t}.npz")
        ax[i, j].imshow(d[key], cmap=cm, origin="lower", vmin=0, vmax=vm); ax[i, j].contour(d["phi"], [0.5], colors="c", linewidths=0.5)
        ax[i, j].set_title(f"{arm} {'layer s' if key=='s' else 'cargo c'} t={t}", fontsize=7); ax[i, j].set_xticks([]); ax[i, j].set_yticks([])
plt.tight_layout(); plt.savefig(out, dpi=75)
