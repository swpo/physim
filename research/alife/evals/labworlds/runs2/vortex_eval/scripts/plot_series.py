import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
z = np.load("/home/user/evalwork/vortex_eval/prep/series_s31.npz")
ts = list(range(540, 601, 4))
fig, ax = plt.subplots(2, len(ts), figsize=(20, 3.2))
for c, t in enumerate(ts):
    om = z[f"om_{t}"]
    sh = np.roll(np.roll(om, 64 - 100, 0), 64 - 120, 1)  # centre body 0
    ax[0, c].imshow(sh[34:94, 34:94], cmap="RdBu_r", vmin=-0.22, vmax=0.22, origin="lower"); ax[0, c].set_title(f"t={t}", fontsize=8)
    ax[1, c].imshow(om, cmap="RdBu_r", vmin=-0.22, vmax=0.22, origin="lower")
    for a in ax[:, c]: a.set_xticks([]); a.set_yticks([])
plt.tight_layout(); plt.savefig("/home/user/evalwork/vortex_eval/prep/series_body0.png", dpi=55)
