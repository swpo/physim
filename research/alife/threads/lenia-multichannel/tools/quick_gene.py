"""Run a gene world, log population trait statistics, save a strip coloured by trait.

python quick_gene.py world.py OUT.png STEPS SIZE SEED [KEY=VAL ...]
Log every STEPS/12: cells (core components), mass-weighted mean g, std of per-cell mean g, min/max cell g, food.
Also writes OUT.json with the series.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from labkit.world import load_world  # noqa: E402

W = load_world(sys.argv[1]); out = sys.argv[2]; steps = int(sys.argv[3]); size = int(sys.argv[4]); seed = int(sys.argv[5])
for kv in sys.argv[6:]:
    k, v = kv.split("=", 1); setattr(W, k, eval(v, dict(vars(W)) | {"np": np}))
s = W.init(seed, (size, size))
every = max(1, steps // 12)
tiles, ser = [], []


def stats(s):
    A0 = s["A"][0]; M = s["A"].sum(0); g = s["g"]
    lab, n = ndimage.label(ndimage.gaussian_filter(A0, 1, mode="wrap") > 0.3)
    cg = []
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() >= 20:
            cg.append(float((g[m] * M[m]).sum() / M[m].sum()))
    mg = float((g * M).sum() / max(M.sum(), 1e-9))
    return dict(n=len(cg), mean=mg, sd=float(np.std(cg)) if cg else 0.0, mn=min(cg) if cg else 0.0,
                mx=max(cg) if cg else 0.0, F=float(s["F"].mean()), cells=cg)


for t in range(steps + 1):
    if t % every == 0:
        st = stats(s); st["t"] = t; ser.append(st)
        M = np.clip(s["A"].sum(0), 0, 1); g = s["g"]
        rgb = np.stack([M * np.clip(0.5 + g, 0, 1), 0.35 * np.clip(s["F"], 0, 1) + 0.25 * M, M * np.clip(0.5 - g, 0, 1)], -1)
        tiles.append(np.pad((255 * np.clip(rgb, 0, 1)).astype(np.uint8), ((2, 2), (2, 2), (0, 0)), constant_values=60))
    if t < steps:
        s = W.step(s)
Image.fromarray(np.concatenate(tiles, 1)).save(out)
json.dump(ser, open(out.replace(".png", ".json"), "w"))
print(" ".join(f"{d['t']}:n{d['n']} g{d['mean']:+.2f}±{d['sd']:.2f}[{d['mn']:+.2f},{d['mx']:+.2f}] F{d['F']:.2f}" for d in ser))
