"""Quick-look screen: python screen.py world.py out.png --steps N --frames 8 --size 128 [--set key=val ...]

Overrides entries of the world's module-level P dict, runs, and writes a strip of frames
(each channel as its own row, fixed per-channel scale over the run) plus a one-line
summary (component count of channel 0 above its midrange, over time).
"""
import argparse, sys, time
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from labkit.world import load_world

ap = argparse.ArgumentParser()
ap.add_argument("world"); ap.add_argument("out")
ap.add_argument("--steps", type=int, default=4000)
ap.add_argument("--frames", type=int, default=8)
ap.add_argument("--size", type=int, default=128)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--set", nargs="*", default=[])
a = ap.parse_args()
W = load_world(a.world)
for kv in a.set:
    k, v = kv.split("=")
    W.P[k] = type(W.P[k])(eval(v)) if not isinstance(W.P[k], bool) else v in ("1", "True")
s = W.init(a.seed, (a.size, a.size))
snaps = [np.asarray(W.fields(s))]
per = a.steps // (a.frames - 1)
t0 = time.time()
for f in range(a.frames - 1):
    for _ in range(per):
        s = W.step(s)
    F = np.asarray(W.fields(s))
    snaps.append(F)
    if not np.isfinite(F).all():
        print("NaN at frame", f); break
S = np.stack(snaps)  # T C H W
rows = []
for c in range(S.shape[1]):
    lo, hi = np.percentile(S[:, c], [1, 99.5]); hi = max(hi, lo + 1e-9)
    x = np.clip((S[:, c] - lo) / (hi - lo), 0, 1)
    rows.append(np.concatenate([np.pad(xi, 1, constant_values=1) for xi in x], 1))
img = (np.concatenate(rows, 0) * 255).astype(np.uint8)
Image.fromarray(img).save(a.out)
m = S[:, 0]; mid = 0.5 * (m.min() + m.max())
counts = [ndimage.label(fr > mid)[1] for fr in m]
print(f"{Path(a.out).name}: {time.time()-t0:.0f}s counts {counts} range [{m[-1].min():.2f},{m[-1].max():.2f}] " +
      " ".join(f"tot{c}={S[-1,c].mean():.3f}" for c in range(S.shape[1])))
