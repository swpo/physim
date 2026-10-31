import json, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(3, 6, figsize=(18, 9.6))
for r, s in enumerate((21, 22)):
    z = np.load(f"fv_s{s}_L0.003.npz")
    rec = z["rec"]
    js = json.load(open(f"fv_s{s}_L0.003.json"))
    for c, t in enumerate((0, 300, 1200, 2100, 2850, 3000)):
        f = int(t / 3)
        ax[r, c].imshow(rec[f], cmap="RdBu_r", vmin=-0.25, vmax=0.25, origin="lower")
        ax[r, c].set_title(f"seed {s}  t={t}")
        ax[r, c].axis("off")
    np.savez_compressed(f"snap_s{s}.npz", **{f"om_{t}": rec[int(t / 3)] for t in (0, 300, 600, 1200, 2100, 2850, 3000)})
    ps = js["ps_times"]
    ax[2, r * 3].hist(ps, bins=np.arange(0, 3001, 150)); ax[2, r * 3].set_title(f"seed {s}: persistent splits per 150 t")
    bt = js["bodies_by_time"]; ax[2, r * 3 + 1].plot([int(k) for k in bt], list(bt.values()), "o-"); ax[2, r * 3 + 1].set_title("bodies")
    ax[2, r * 3 + 2].axis("off")
plt.tight_layout(); plt.savefig("behav_noise.png", dpi=60)
