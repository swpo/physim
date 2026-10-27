import sys, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
runs = sys.argv[2:]; out = sys.argv[1]
fig, ax = plt.subplots(len(runs), 8, figsize=(14, 1.9 * len(runs)), squeeze=False)
for r, run in enumerate(runs):
    z = np.load(run + "_snaps.npz"); t = z["t"]; idx = np.linspace(0, len(t) - 1, 8).astype(int)
    for j, i in enumerate(idx):
        e = z["e"][i].astype(float); g1 = z["g1"][i].astype(float); g2 = z["g2"][i].astype(float)
        rgb = np.stack([np.clip(g2, 0, 1), np.clip(e, 0, 1) * 0.6, np.clip(g1, 0, 1)], -1)
        rgb = np.maximum(rgb, (np.clip(e, 0, 1) * 0.35)[..., None])
        ax[r, j].imshow(rgb); ax[r, j].axis("off"); ax[r, j].set_title(f"{run.split('/')[-1]} t={t[i]}", fontsize=6)
fig.suptitle("cips-gene: enzyme bodies (grey), g1 blue, g2 red", fontsize=8); fig.tight_layout(); fig.savefig(out, dpi=70)
