"""c19: seed 13 fed vs starved (feed cut at t=300): crops of the K vesicle (centre 73,100) and the K-free ring
(centre 180,29, periodic) in u+1 and K at t = 297, 390, 450, 519, 600."""
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
runs = [("fed", "rerun/seed13/frames.npz"), ("starved", "starve/seed13/frames.npz")]
T = [297, 390, 450, 519, 600]; crops = [("K vesicle u", (73, 100), 0), ("K vesicle K", (73, 100), 2), ("K-free ring u", (180, 29), 0)]
fig, ax = plt.subplots(6, len(T), figsize=(2.1 * len(T), 12.6))
for a, (lab, fn) in enumerate(runs):
    d = np.load(fn); R = d["render"].astype(np.float32); f = d["render_f"]
    for c, t in enumerate(T):
        i = int(np.argmin(np.abs(f * 3 - t)))
        for b, (name, (cy, cx), ch) in enumerate(crops):
            img = np.roll(np.roll(R[i, ch], 32 - cy, 0), 32 - cx, 1)[:64, :64]
            x = ax[3 * a + b, c]; x.imshow(img, cmap="magma" if ch == 0 else "viridis", vmin=0, vmax=1.6 if ch == 0 else 4)
            x.set_title(f"{lab} t={f[i] * 3:.0f} {name}", fontsize=7); x.set_xticks([]); x.set_yticks([])
plt.tight_layout(); plt.savefig("fork_s13.png", dpi=70)
