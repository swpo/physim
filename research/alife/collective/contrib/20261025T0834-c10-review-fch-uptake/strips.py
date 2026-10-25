"""Random fission events (a body in render frame i-1 overlapping >= 2 bodies in frame i), crops of u and log c
over frames i-3..i+4 with each body's mean c / outside in the title. Usage: strips.py pack_seed_dir out.png tmin nevents rngseed"""
import sys, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import ndimage
d, out, tmin, ne, rs = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
F = np.load(d + "/frames.npz"); R, rf = F["render"], F["render_f"]
import json; spf = json.load(open(d + "/metrics.json")); dtf = spf["steps_per_frame"] * spf["dt"]
thr = 0.8; labs = [ndimage.label(R[i, 0] > thr) for i in range(len(R))]
ev = []
for i in range(1, len(R) - 5):
    if rf[i] * dtf < tmin: continue
    la, na = labs[i - 1]; lb, nb = labs[i]
    for k in range(1, na + 1):
        kids = set(np.unique(lb[la == k])) - {0}
        if len(kids) >= 2: ev.append((i, k))
rng = np.random.default_rng(rs); pick = [ev[j] for j in rng.choice(len(ev), min(ne, len(ev)), replace=False)]
fig, ax = plt.subplots(2 * len(pick), 8, figsize=(16, 4.2 * len(pick)))
for r, (i, k) in enumerate(pick):
    la, _ = labs[i - 1]; cy, cx = ndimage.center_of_mass(la == k); cy, cx = int(cy), int(cx)
    H = R.shape[2]
    for j, f in enumerate(range(i - 3, i + 5)):
        u, c = R[f, 0], R[f, 1]
        body = u > thr; lab, n = labs[f]; far = ~ndimage.binary_dilation(body, iterations=3)
        cout = max(c[far].mean(), 1e-12)
        sl = (np.arange(cy - 16, cy + 16) % H)[:, None], (np.arange(cx - 16, cx + 16) % H)[None, :]
        ids = [x for x in np.unique(lab[sl]) if x and (lab[sl] == x).sum() > 15]
        rat = [ndimage.mean(c, lab, x) / cout for x in ids]
        ax[2 * r, j].imshow(u[sl], vmin=0, vmax=3, cmap="magma"); ax[2 * r, j].set_title(f"t={rf[f]*dtf:.0f}", fontsize=8)
        ax[2 * r + 1, j].imshow(np.log10(c[sl] + 1e-6), vmin=-2, vmax=1, cmap="viridis")
        ax[2 * r + 1, j].set_title("x" + ",".join(f"{v:.0f}" for v in rat), fontsize=7)
for a in ax.flat: a.set_xticks([]); a.set_yticks([])
fig.suptitle(f"{d}: random fissions after t={tmin:.0f}; top u+1.6, bottom log10 c; titles = mean c per body / outside", fontsize=9)
fig.tight_layout(); fig.savefig(out, dpi=70); print(len(ev), "events;", pick)
