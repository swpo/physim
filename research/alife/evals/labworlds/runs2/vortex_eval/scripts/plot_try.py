import json, sys, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
name = sys.argv[1]
z = np.load(f"/home/user/evalwork/vortex_eval/mech/try_{name}.npz"); js = json.load(open(f"/home/user/evalwork/vortex_eval/mech/try_{name}.json"))
progs = list(js["programs"])
fig, ax = plt.subplots(len(progs), 11, figsize=(16, 1.6 * len(progs) + 0.4), squeeze=False)
for r, p in enumerate(progs):
    for c in range(11):
        ax[r, c].imshow(z[p][c], cmap="RdBu_r", vmin=-0.3, vmax=0.3, origin="lower"); ax[r, c].set_xticks([]); ax[r, c].set_yticks([])
        if r == 0: ax[r, c].set_title(f"t={5 * c}", fontsize=8)
    ax[r, 0].set_ylabel(p[:18], fontsize=8)
plt.tight_layout(); plt.savefig(f"/home/user/evalwork/vortex_eval/mech/try_{name}.png", dpi=55)
