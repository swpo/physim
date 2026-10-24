"""Per-species population curves for two-species packs (render channels 0 = prey, 1 = predator).

Counts bodies of each species per recorded frame (> 0.3 of that channel's global max, area >= 12 px),
and reports the prey-to-predator lag that maximizes the cross-correlation of the channel totals
(metrics.json series, all frames, after t_on). Writes species.png next to the pack.
usage: python species.py pack_dir t_on
"""
import json
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

d, t_on = sys.argv[1], float(sys.argv[2])
Z = np.load(f"{d}/frames.npz")
F, fr = Z["render"].astype(np.float32), Z["render_f"]
m = json.load(open(f"{d}/metrics.json"))
dt_frame = m["steps_per_frame"] * 0.05
counts = []
for c in range(2):
    thr = 0.3 * F[:, c].max()
    row = []
    for f in F[:, c]:
        lab, n = ndimage.label(f > thr)
        row.append(int((ndimage.sum(np.ones_like(f), lab, range(1, n + 1)) >= 12).sum()) if n else 0)
    counts.append(row)
counts = np.array(counts)
tot = np.array(m["series"]["totals"])[:, :2]
t = np.arange(len(tot)) * dt_frame
k = t >= t_on + 100
x, y = tot[k, 0] - tot[k, 0].mean(), tot[k, 1] - tot[k, 1].mean()
lags = np.arange(0, len(x) // 3)
cc = [np.corrcoef(x[: len(x) - L], y[L:])[0, 1] for L in lags]
L = lags[int(np.argmax(cc))]
print(f"{d}: prey bodies mean {counts[0][fr * dt_frame > t_on + 100].mean():.1f}, predator bodies mean "
      f"{counts[1][fr * dt_frame > t_on + 100].mean():.1f}; best lag prey->predator {L * dt_frame:.0f} t (r={max(cc):.2f}, r(lag0)={cc[0]:.2f})")
# plot
Wd, Hd = 640, 300
im = Image.new("RGB", (Wd, Hd), (20, 20, 24))
dr = ImageDraw.Draw(im)
for c, col in ((0, (40, 210, 240)), (1, (250, 150, 30))):
    yv = tot[:, c] / tot[:, c].max()
    pts = [(10 + 620 * i / (len(yv) - 1), 140 - 120 * v) for i, v in enumerate(yv)]
    dr.line(pts, fill=col, width=2)
    cv = counts[c] / max(counts.max(), 1)
    pts = [(10 + 620 * f / fr[-1], 290 - 130 * v) for f, v in zip(fr, cv)]
    dr.line(pts, fill=col, width=2)
dr.text((12, 4), "channel totals (prey cyan, predator orange), normalized", fill=(220, 220, 220))
dr.text((12, 150), f"body counts (max {counts.max()}); x = time 0..{t[-1]:.0f}", fill=(220, 220, 220))
im.save(f"{d}/species.png")
