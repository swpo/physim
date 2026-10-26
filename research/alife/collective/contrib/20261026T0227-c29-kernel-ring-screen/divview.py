"""c28: wide view around a division (parent's last centroid), L with phi=1/2 contour. usage: divview.py tracks.json snap.npz out.png parent_id"""
import json, sys, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
d = json.load(open(sys.argv[1])); Z = np.load(sys.argv[2]); pid = sys.argv[4]; T = d["tracks"]; tr = T[pid]
ts = Z["t"]; N = Z["phi"].shape[1]; C = 50; cy, cx = tr["path"][-1][1], tr["path"][-1][2]; t1 = tr["t1"]
pick = [t for t in ts if t1 - 800 <= t <= t1 + 600]
fig, ax = plt.subplots(1, len(pick), figsize=(2.2 * len(pick), 2.5))
for j, t in enumerate(pick):
    k = int(np.where(ts == t)[0][0]); sh = (int(N / 2 - cy), int(N / 2 - cx))
    L = np.roll(Z["L"][k].astype(float), sh, (0, 1))[N // 2 - C:N // 2 + C, N // 2 - C:N // 2 + C]
    ph = np.roll(Z["phi"][k].astype(float), sh, (0, 1))[N // 2 - C:N // 2 + C, N // 2 - C:N // 2 + C]
    ax[j].imshow(L, cmap="magma", vmin=0, vmax=0.6); ax[j].contour(ph, [0.5], colors="c", linewidths=0.6)
    ax[j].set_title(f"t={t}" + (" (split)" if abs(t - t1) <= 100 else ""), fontsize=8); ax[j].set_xticks([]); ax[j].set_yticks([])
fig.suptitle(f"track {pid} divides at t~{t1 + 20} into {tr['children']} (fixed frame at the parent's last centroid)", fontsize=8)
fig.tight_layout(); fig.savefig(sys.argv[3], dpi=80)
