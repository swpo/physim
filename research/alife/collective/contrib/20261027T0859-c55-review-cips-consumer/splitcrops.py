"""c55: crops (prey green, predator red) at f-1, f, f+1, f+5 around 8 persistent predator splits from coinc.json rows."""
import sys, json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
pack, cj, out = sys.argv[1:4]
R = np.load(pack + '/frames.npz')['render'].astype(np.float32); T = len(R); H = R.shape[2]
rows = json.load(open(cj))['pred_split_rows']; rows = rows[::max(1, len(rows) // 8)][:8]
fig, ax = plt.subplots(len(rows), 4, figsize=(6, 1.6 * len(rows)), squeeze=False); h = 22
for r, (f, cy, cx, hit) in enumerate(rows):
    for c, d in enumerate((-2, -1, 0, 4)):
        F = R[min(T - 1, max(0, f + d))]; ys = np.arange(cy - h, cy + h) % H; xs = np.arange(cx - h, cx + h) % H
        ax[r, c].imshow(np.stack([F[1], F[0], 0 * F[0]], -1)[np.ix_(ys, xs)].clip(0, 1)); ax[r, c].set_xticks([]); ax[r, c].set_yticks([])
        ax[r, c].set_title(f't={(f + d) * 100}' + (' split' + (' +prey split' if hit else '') if d == 0 else ''), fontsize=6)
plt.tight_layout(); plt.savefig(out, dpi=90)
