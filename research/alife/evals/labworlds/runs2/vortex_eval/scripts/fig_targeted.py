import json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
M = "/home/user/evalwork/vortex_eval/mech"
rows = [("try_rod580a", "sham", "device0 rod: sham (pinch ~23)"), ("try_rod580a", "feed_neck", "feed_neck: Y+ 3x20 (no pinch)"),
        ("try_rod580a", "starve_neck", "starve_neck: Y- 2x6 (pinch ~8)"), ("try_rod580a", "feed_neck_late", "Y+ at t=10 (pinch ~32)"),
        ("try_v580", "sham", "device1 vortex: sham"), ("try_v580", "feed_vortex", "feed_vortex: Y+ 3x25"),
        ("try_v580", "starve_vortex", "starve_vortex: Y- 3x10"), ("try_v580", "stir_destroy", "stir_cut: om- 2x8")]
fig, ax = plt.subplots(len(rows), 11, figsize=(15, 1.45 * len(rows)))
for r, (f, p, lab) in enumerate(rows):
    z = np.load(f"{M}/{f}.npz")
    for c in range(11):
        ax[r, c].imshow(z[p][c][8:40, 8:40], cmap="RdBu_r", vmin=-0.3, vmax=0.3, origin="lower")
        ax[r, c].set_xticks([]); ax[r, c].set_yticks([])
        if r == 0: ax[r, c].set_title(f"t={5 * c}", fontsize=8)
    ax[r, 0].set_ylabel(lab, fontsize=6.5, rotation=0, ha="right", va="center")
plt.subplots_adjust(left=0.17, wspace=0.03, hspace=0.05); plt.savefig(f"{M}/targeted_strips.png", dpi=60)
