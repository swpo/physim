"""Rows: fed twin, local feed cut around cell 23, local cut around cell 13, global feed cut (seed 2). Columns: t ~ 59.4k-70k.
Wall (channel 3) in grey, catalyst K (channel 1) > 0.05 in red, cut disk outlined in cyan."""
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
rows = [("fed twin", "fed/seed2/frames.npz", 100000, None), ("local cut, cell 23", "localcut23/seed2/frames.npz", 70000, (89.4, 63.9, 14)),
        ("local cut, cell 13", "localcut13/seed2/frames.npz", 70000, (53.6, 98.4, 13)), ("global cut", "starve/seed2/frames.npz", 70000, None)]
times = [59400, 60000, 60600, 61200, 63500, 70000]
fig, ax = plt.subplots(len(rows), len(times), figsize=(2 * len(times), 2.1 * len(rows)))
for r, (lab, p, T, cut) in enumerate(rows):
    R = np.load(p)["render"]; n = len(R) - 1
    for c, t in enumerate(times):
        i = int(round(t / T * n)); w, K = R[i, 3], R[i, 1]
        img = np.dstack([np.clip(w, 0, 1) * 0.8] * 3); img[K > 0.05] = [0.95, 0.2, 0.15]
        a = ax[r, c]; a.imshow(img, interpolation="nearest"); a.set_xticks([]); a.set_yticks([])
        if cut: a.add_patch(plt.Circle((cut[1], cut[0]), cut[2], fill=False, ec="c", lw=0.8))
        a.set_title(f"{lab}\nt={i * T / n:.0f}", fontsize=7)
fig.suptitle("pcell-mwall-b42 seed 2: feed cut at t=60000 only inside the cyan disk (rows 2-3) or everywhere (row 4); grey wall, red catalyst", fontsize=8)
fig.tight_layout(); fig.savefig("localcut_seed2.png", dpi=100)
