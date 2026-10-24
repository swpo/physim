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
# motion: link components frame to frame by nearest periodic centroid; report max path in body diameters
from scipy import ndimage as ndi
def cents(fr):
    lab, n = ndi.label(fr > 0)
    if n == 0: return np.zeros((0, 2)), np.zeros(0)
    H, Wd = fr.shape
    out = []
    ar = ndi.sum(np.ones_like(fr), lab, range(1, n + 1))
    for i in range(1, n + 1):
        yy, xx = np.nonzero(lab == i)
        ang_y = np.angle(np.exp(2j*np.pi*yy/H).mean())*H/(2*np.pi) % H
        ang_x = np.angle(np.exp(2j*np.pi*xx/Wd).mean())*Wd/(2*np.pi) % Wd
        out.append((ang_y, ang_x))
    return np.array(out), np.array(ar)
paths = None
H = m.shape[1]
prevc = None
best = 0.0
for fr in m[1:]:
    c, ar = cents(fr)
    if prevc is not None and len(c) and len(prevc):
        d = c[:, None, :] - prevc[0][None]
        d = (d + H/2) % H - H/2
        dist = np.sqrt((d**2).sum(-1)); j = dist.argmin(1); step = dist[np.arange(len(c)), j]
        cum = prevc[2][j] + np.where(step < 6, step, 0)
        diam = 2*np.sqrt(ar/np.pi)
        best = max(best, float((cum/diam).max()))
        prevc = (c, ar, cum)
    elif len(c):
        prevc = (c, ar, np.zeros(len(c)))
print(f"max path {best:.2f} body diameters;", end=" ")
print(f"{Path(a.out).name}: {time.time()-t0:.0f}s counts {counts} range [{m[-1].min():.2f},{m[-1].max():.2f}] " +
      " ".join(f"tot{c}={S[-1,c].mean():.3f}" for c in range(S.shape[1])))
