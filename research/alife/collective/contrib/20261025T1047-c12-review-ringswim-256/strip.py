"""Render biography strips of chosen celltrack tracks (re-simulates the world on the same seed).
usage: python strip.py world.py track.json seed out.png "label:id1,id2,...;label2:..." """
import json, sys
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit.world import load_world
world, tj, seed, out, spec = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
T = json.load(open(tj))["tracks"]
rows = []
for part in spec.split(";"):
    lab, ids = part.split(":")
    pts = []
    for i in ids.split(","):
        P = T[i]["path"]
        n = len(P)
        for j in np.linspace(0, n - 1, min(n, 4)).astype(int):
            pts.append((P[j][0], P[j][1], P[j][2], i))
    rows.append((lab, sorted(pts)))
need = sorted({p[0] for _, pts in rows for p in pts})
W = load_world(world); s = W.init(seed, tuple(W.META["size"])); snaps = {}
for t in range(max(need) + 1):
    if t in need:
        snaps[t] = (s["phi"].copy(), s["L"].copy(), s["K"].copy())
    s = W.step(s)
ncol = max(len(p) for _, p in rows)
fig, axs = plt.subplots(len(rows), ncol, figsize=(1.6 * ncol, 1.8 * len(rows)))
axs = np.atleast_2d(axs)
for r, (lab, pts) in enumerate(rows):
    for c in range(ncol):
        a = axs[r, c]; a.set_xticks([]); a.set_yticks([])
        if c >= len(pts):
            a.axis("off"); continue
        t, cy, cx, i = pts[c]
        phi, L, K = snaps[t]
        sh = (-int(round(cy)) + 32, -int(round(cx)) + 32)
        crop = lambda f: np.roll(f, sh, (0, 1))[:64, :64]
        rgb = np.stack([np.clip(crop(L) / 1.2, 0, 1), np.clip(crop(K), 0, 1) * 0.6, np.clip(4 * crop(phi) * (1 - crop(phi)), 0, 1)], -1)
        a.imshow(rgb); a.set_title(f"#{i} t={t}", fontsize=6)
    axs[r, 0].set_ylabel(lab, fontsize=6)
fig.suptitle("crops 64x64 centred on the track; R = links L (ring), G = catalyst K, B = wall 4phi(1-phi)", fontsize=7)
plt.tight_layout(); plt.savefig(out, dpi=110)
