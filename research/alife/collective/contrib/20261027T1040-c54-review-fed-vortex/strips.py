"""(c54) Strips of randomly chosen persistent vortex splits (|omega| > 0.06) (consumer_only.py's segmentation): prey c_a green, consumer q red,
crops of 48 px around the parent's last centroid, frames f-2 .. f+5 (100 t per frame). usage: strips.py frames.npz out.png [seed]"""
import sys, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
F = np.load(sys.argv[1]); R = F["render"].astype(np.float32); q, a = R[:, 0], R[:, 1] * 0; T, H, W = q.shape  # q: |vorticity| (render channel 0)
comps, links = LR._segment_frames(q, 0.06, 6, True)
tracks, ev = M.track(comps, links, (H, W), True); byid = {t["id"]: t for t in tracks}
ps = M.lineage_stats(tracks, ev, T, 100.0, (H, W), True, 5)["persistent_splits"]
rng = np.random.default_rng(int(sys.argv[3]) if len(sys.argv) > 3 else 0)
pick = [ps[i] for i in sorted(rng.choice(len(ps), min(4, len(ps)), replace=False))]
fig, ax = plt.subplots(len(pick), 8, figsize=(12, 1.6 * len(pick)))
for r, e in enumerate(pick):
    f0 = e["frame"]; tr = byid[e["parent"]]
    cy, cx = int(tr["cy"][-1]) % H, int(tr["cx"][-1]) % W
    for j, f in enumerate(range(f0 - 3, f0 + 5)):
        f = min(max(f, 0), T - 1)
        img = np.zeros((H, W, 3)); img[..., 1] = np.clip(a[f], 0, 1); img[..., 0] = np.clip(q[f] / 0.2, 0, 1)
        img = np.roll(np.roll(img, H // 2 - cy, 0), W // 2 - cx, 1)[H // 2 - 24:H // 2 + 24, W // 2 - 24:W // 2 + 24]
        ax[r, j].imshow(img); ax[r, j].set_xticks([]); ax[r, j].set_yticks([])
        ax[r, j].set_title(f"t={int(F["render_f"][f]) * 3}" + (" split" if f == f0 else ""), fontsize=7)
fig.suptitle("random persistent vortex splits (|omega| > 0.06) (render frames ~25 t apart); |omega| red", fontsize=9)
fig.tight_layout(); fig.savefig(sys.argv[2], dpi=80)
