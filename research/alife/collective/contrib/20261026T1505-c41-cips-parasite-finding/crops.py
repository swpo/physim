"""Close-up of predator c inside prey condensates from pred.py snapshots: e and c side by side on a 96x96 crop
around the largest body, plus radial c/e profiles about each body's centroid (c in core vs rim).
usage: crops.py snaps.npz tag"""
import sys, numpy as np
from scipy import ndimage as ndi
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
S = np.load(sys.argv[1]); tag = sys.argv[2]; T = S["t"]; E = S["e"].astype(float); C = S["c"].astype(float)
idx = [0, 1, len(T) // 2, len(T) - 1]
fig, ax = plt.subplots(2, len(idx), figsize=(2.6 * len(idx), 5.2))
k = len(T) - 1; lab, n = ndi.label(E[k] > 0.5, structure=np.ones((3, 3)))
cy, cx = ndi.center_of_mass(E[k] > 0.5, lab, int(np.argmax(ndi.sum(np.ones_like(E[k]), lab, range(1, n + 1))) + 1))
H, W = E[k].shape
for j, i in enumerate(idx):
    e = np.roll(np.roll(E[i], int(H / 2 - cy), 0), int(W / 2 - cx), 1)[H // 2 - 48:H // 2 + 48, W // 2 - 48:W // 2 + 48]
    c = np.roll(np.roll(C[i], int(H / 2 - cy), 0), int(W / 2 - cx), 1)[H // 2 - 48:H // 2 + 48, W // 2 - 48:W // 2 + 48]
    ax[0, j].imshow(e, cmap="viridis", vmin=0, vmax=1); ax[0, j].set_title("enzyme e t=%.0f" % T[i], fontsize=8); ax[0, j].axis("off")
    ax[1, j].imshow(c, cmap="magma", vmin=0, vmax=max(0.05, float(C[-1].max()))); ax[1, j].set_title("predator c t=%.0f" % T[i], fontsize=8); ax[1, j].axis("off")
fig.suptitle(tag + ": 96x96 crop on the largest body at the end", fontsize=8); fig.tight_layout(); fig.savefig("crops_%s.png" % tag, dpi=70)
# per-body c content at the last frame
e, c = E[k], C[k]; lab, n = ndi.label(e > 0.5, structure=np.ones((3, 3)))
cin = ndi.mean(c, lab, range(1, n + 1)); area = ndi.sum(np.ones_like(e), lab, range(1, n + 1))
print(tag, "bodies", n, "area median %.0f" % np.median(area), "c inside bodies median %.3f" % np.median(cin), "c outside mean %.4f" % c[lab == 0].mean(),
      "bodies with c>0.1 inside: %d" % int((np.array(cin) > 0.1).sum()))
