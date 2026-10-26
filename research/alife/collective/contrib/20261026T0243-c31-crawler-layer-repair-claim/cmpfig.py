import sys, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
# usage: cmpfig.py out.png title_a prefix_a title_b prefix_b t1 t2 ...  (npz with phi, rho=cargo, s)
out, ta, pa, tb, pb = sys.argv[1:6]; ts = sys.argv[6:]
fig, ax = plt.subplots(3, len(ts), figsize=(2.6*len(ts), 7.8), squeeze=False)
for j, t in enumerate(ts):
    A = np.load(f"{pa}_t{t}.npz"); B = np.load(f"{pb}_t{t}.npz")
    vm = max(A["rho"].max(), 1e-6)
    for i, (D, im, ttl, cm, v) in enumerate(((A, "s", ta + " layer s", "magma", 0.7), (A, "rho", ta + " cargo c", "viridis", vm), (B, "rho", tb + " cargo c", "viridis", vm))):
        ax[i, j].imshow(D[im], cmap=cm, origin="lower", vmin=0, vmax=v); ax[i, j].contour(D["phi"], [0.5], colors="w", linewidths=0.5)
        ax[i, j].set_title(f"{ttl} t={t}", fontsize=7); ax[i, j].set_xticks([]); ax[i, j].set_yticks([])
plt.tight_layout(); plt.savefig(out, dpi=80)
