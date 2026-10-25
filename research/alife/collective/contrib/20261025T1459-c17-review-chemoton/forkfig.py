"""Rows = runs (labkit frames.npz of the FCH chemoton), columns = recorded frames; amphiphile u+1 in grey,
catalyst K > 0.5 in red. usage: forkfig.py out.png title label1=path1 label2=path2 ..."""
import sys, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out, title, runs = sys.argv[1], sys.argv[2], [a.split("=", 1) for a in sys.argv[3:]]
cols = [55, 59, 62, 70, 80, 95, 119]
fig, ax = plt.subplots(len(runs), len(cols), figsize=(1.6 * len(cols), 1.7 * len(runs)))
for r, (lab, p) in enumerate(runs):
    R = np.load(p)["render"]
    for c, i in enumerate(cols):
        u, P, K = R[i]
        img = np.dstack([np.clip(u / 2, 0, 1)] * 3)
        img[K > 0.5] = [1, 0.15, 0.1]
        a = ax[r, c]; a.imshow(img, interpolation="nearest"); a.set_xticks([]); a.set_yticks([])
        a.set_title(f"{lab} t~{i * 600 / 119:.0f}\nu+1 total {u.sum():.0f}", fontsize=6)
fig.suptitle(title, fontsize=8); fig.tight_layout(); fig.savefig(out, dpi=110)
