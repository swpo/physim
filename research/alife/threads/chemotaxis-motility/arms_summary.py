"""Summarize the fixed-allele arms (evopursuit with m = 0): prey and predator mass, prey body counts.

usage: python arms_summary.py arms_dir out.md
Expects <arm>_s<seed>/ pack dirs (labkit) with metrics.json and frames.npz.
"""
import glob
import json
import os
import sys

import numpy as np
from scipy import ndimage

root, out = sys.argv[1], sys.argv[2]
arms = sorted({os.path.basename(d).rsplit("_s", 1)[0] for d in glob.glob(f"{root}/*_s[0-9]") if os.path.isdir(d)})
rows = []
for arm in arms:
    vals = []
    for d in sorted(glob.glob(f"{root}/{arm}_s[0-9]")):
        if not os.path.exists(f"{d}/metrics.json"):
            continue
        m = json.load(open(f"{d}/metrics.json"))
        tot = np.array(m["series"]["totals"], dtype=float)
        prey = tot[:, 0] + tot[:, 1]
        pred = tot[:, 2]
        t = np.arange(len(tot)) * m["steps_per_frame"] * m.get("dt", 0.05)
        Z = np.load(f"{d}/frames.npz")
        F = Z["render"].astype(np.float32)
        tf = Z["render_f"] * m["steps_per_frame"] * m.get("dt", 0.05)
        P = F[:, 0] + F[:, 1]
        thr = 0.35 * P.max()
        nb = []
        for k in np.nonzero(tf >= 1000)[0]:
            lab, n = ndimage.label(P[k] > thr)
            nb.append(int((ndimage.sum(np.ones_like(P[k]), lab, range(1, n + 1)) >= 12).sum()) if n else 0)
        i150 = int(np.argmin(np.abs(t - 150)))
        vals.append((prey[-1] / prey[i150], pred[-1] / max(pred[i150], 1e-9) if pred[i150] > 0 else np.nan,
                     np.mean(nb), prey[-1]))
    if vals:
        v = np.array(vals)
        rows.append((arm, len(v), v))
with open(out, "w") as f:
    f.write("| arm | seeds | prey mass t=1500 / t=150 | predator mass t=1500 / t=150 | prey bodies (mean, t 1000-1500) | prey mass t=1500 |\n|---|---|---|---|---|---|\n")
    for arm, n, v in rows:
        fmt = lambda col, p=2: ", ".join("—" if np.isnan(x) else f"{x:.{p}f}" for x in v[:, col])
        f.write(f"| {arm} | {n} | {fmt(0)} | {fmt(1)} | {fmt(2, 1)} | {fmt(3, 0)} |\n")
print(open(out).read())
