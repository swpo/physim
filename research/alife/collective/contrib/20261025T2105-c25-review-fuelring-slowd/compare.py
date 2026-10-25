"""phi and fuel at t=500 and t=1000 for the four seed-31 arms."""
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
arms = [("world", "rerun/seed31"), ("chi_s=0", "controls/chis0_s31"), ("chi_s=0, Df=0.3", "controls/slowD03_s31"), ("chi_s=0, Df=0.6", "controls/slowD06_s31")]
fig, ax = plt.subplots(3, 4, figsize=(12, 9))
for j, (name, d) in enumerate(arms):
    R = np.load(d + "/frames.npz")["render"]
    for i, (fr, ch, lab, kw) in enumerate([(len(R)//2, 0, "phi mid", dict(vmin=-1, vmax=1, cmap="gray")), (-1, 0, "phi t=1000", dict(vmin=-1, vmax=1, cmap="gray")), (-1, 3, "fuel f t=1000", dict(vmin=0, vmax=1.2, cmap="magma"))]):
        ax[i, j].imshow(R[fr, ch], **kw); ax[i, j].set_xticks([]); ax[i, j].set_yticks([])
        ax[i, j].set_title(f"{name}: {lab}", fontsize=9)
plt.tight_layout(); plt.savefig("compare_s31.png", dpi=70)
