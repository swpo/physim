import sys, json, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import ndimage
OUT = "/home/user/evalwork/pm_cips_eval"
tag = sys.argv[1]
z = np.load(f"{OUT}/cips_prep/window_{tag}.npz")
fr = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
fig, ax = plt.subplots(2, 6, figsize=(24, 8.4))
for a, t in zip(ax.flat, fr + [None]):
    if t is None:
        a.imshow(z["s_0tu"].astype(float), origin="lower"); a.set_title("s at 0 tu"); continue
    e = z[f"e_{t}tu"].astype(float)
    a.imshow(e, origin="lower", vmin=0, vmax=1, cmap="magma")
    lab, n = ndimage.label(e > 0.5, structure=np.ones((3, 3)))
    a.set_title(f"e at {t} tu: {n} comps")
    if t == 0:
        for j in range(1, n + 1):
            yy, xx = np.nonzero(lab == j)
            a.text(xx.mean(), yy.mean(), f"{j}:{yy.mean():.0f},{xx.mean():.0f}", color="c", fontsize=8)
fig.tight_layout(); fig.savefig(f"{OUT}/figs/cips_window_{tag}.png", dpi=55)
