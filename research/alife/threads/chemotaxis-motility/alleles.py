"""Per-body allele composition for swimevo packs (render channels 0 = A, 1 = B).

For each recorded frame: segment bodies on A+B (> 0.35 of the global max, area >= 12 px),
compute each body's B fraction, and classify it as A (< 0.2), B (> 0.8) or mixed.
Prints a table at a few times and writes alleles.png (counts of A, B and mixed bodies versus time)
for every pack directory given. Several packs are drawn as rows of one image.
usage: python alleles.py out.png pack_seed_dir [pack_seed_dir ...]
"""
import json
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

out = sys.argv[1]
rows = []
for d in sys.argv[2:]:
    Z = np.load(f"{d}/frames.npz")
    F, fr = Z["render"].astype(np.float32), Z["render_f"]
    spf = json.load(open(f"{d}/metrics.json"))["steps_per_frame"]
    t = fr * spf * 0.05
    tot = F[:, 0] + F[:, 1]
    thr = 0.35 * tot.max()
    cnt = []
    for k in range(len(F)):
        lab, n = ndimage.label(tot[k] > thr)
        if n == 0:
            cnt.append((0, 0, 0))
            continue
        ids = range(1, n + 1)
        area = ndimage.sum(np.ones_like(tot[k]), lab, ids)
        a = ndimage.sum(F[k, 0], lab, ids)
        b = ndimage.sum(F[k, 1], lab, ids)
        f = b / np.maximum(a + b, 1e-9)
        ok = area >= 12
        cnt.append((int(((f < 0.2) & ok).sum()), int(((f > 0.8) & ok).sum()), int(((f >= 0.2) & (f <= 0.8) & ok).sum())))
    cnt = np.array(cnt)
    sel = [np.argmin(np.abs(t - x)) for x in (150, 600, 900, 1200, 1500, t[-1])]
    print(d, " | ".join(f"t={t[i]:.0f}: A{cnt[i,0]} B{cnt[i,1]} mix{cnt[i,2]}" for i in sel))
    rows.append((d, t, cnt))
Wd, Hr = 640, 150
im = Image.new("RGB", (Wd, Hr * len(rows)), (20, 20, 24))
dr = ImageDraw.Draw(im)
mx = max(r[2].max() for r in rows)
for j, (d, t, cnt) in enumerate(rows):
    y0 = j * Hr
    for c, col in ((0, (40, 210, 240)), (1, (250, 150, 30)), (2, (200, 200, 200))):
        pts = [(10 + 620 * tt / t[-1], y0 + Hr - 10 - (Hr - 30) * v / mx) for tt, v in zip(t, cnt[:, c])]
        dr.line(pts, fill=col, width=2)
    dr.text((12, y0 + 4), f"{d.split('packs/')[-1]}: bodies A (cyan) / B (orange) / mixed (grey), max {mx}, t 0..{t[-1]:.0f}",
            fill=(220, 220, 220))
im.save(out)
