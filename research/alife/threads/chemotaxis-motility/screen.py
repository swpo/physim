"""Quick-look screener: python threads/chemotaxis-motility/screen.py world.py out.png [steps] [k=v ...]

Overrides entries of the world's module-level P dict, runs `steps` internal steps,
and writes an 8-panel strip per channel (fixed scales) plus a one-line summary.
"""
import sys
import time

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, ".")
from labkit.world import load_world  # noqa: E402

W = load_world(sys.argv[1])
out = sys.argv[2]
steps = int(sys.argv[3]) if len(sys.argv) > 3 and "=" not in sys.argv[3] else 4000
size = tuple(W.META["size"])
for kv in sys.argv[3:]:
    if "=" in kv:
        k, v = kv.split("=")
        if k == "size":
            size = (int(v), int(v))
        elif k == "seed":
            pass
        else:
            W.P[k] = type(W.P[k])(eval(v)) if not isinstance(W.P[k], bool) else v in ("1", "True")
seed = int(dict(kv.split("=") for kv in sys.argv[3:] if "=" in kv).get("seed", 0))
s = W.init(seed, size)
snaps = []
trail = []
t0 = time.time()
nsnap = 8
for i in range(steps + 1):
    if i % (steps // (nsnap - 1)) == 0 and len(snaps) < nsnap:
        snaps.append(np.array(W.fields(s), np.float32))
    if i % max(1, steps // 40) == 0:
        trail.append(np.array(W.fields(s), np.float32)[0])
    if i < steps:
        s = W.step(s)
F = np.stack(snaps)  # T C H W
ok = np.isfinite(F).all()
rows = []
for c in range(F.shape[1]):
    x = F[:, c]
    lo, hi = np.nanpercentile(x, [1, 99.8])
    x = np.clip((x - lo) / max(hi - lo, 1e-9), 0, 1)
    rows.append(np.concatenate([np.pad(f, 1, constant_values=1) for f in x], 1))
img = np.concatenate(rows, 0)
# time-coded overlay of channel 0 (blue = early, red = late), latest frame wins
tr = np.stack(trail)
tr = tr / max(np.percentile(tr, 99.8), 1e-9)
Hh, Ww = tr.shape[1:]
col = np.zeros((Hh, Ww, 3))
for k, f in enumerate(tr):
    c = np.array([k / (len(tr) - 1), 0.3, 1 - k / (len(tr) - 1)])
    msk = f > 0.4
    col[msk] = c * np.clip(f[msk], 0, 1)[:, None]
gray = np.repeat(img[:, :, None], 3, 2)
pad = np.zeros((gray.shape[0], Ww + 2, 3))
pad[:Hh, 1:Ww + 1] = col
Image.fromarray((np.concatenate([gray, pad], 1) * 255).astype(np.uint8)).resize(
    (img.shape[1] + Ww + 2, img.shape[0]), Image.NEAREST).quantize(64).save(out)
m = F[-1, 0]
lab, n = ndimage.label(m > 0.5 * m.max())
print(f"{out}: ok={ok} wall={time.time()-t0:.1f}s blobs_final={n} max={m.max():.3g} "
      f"totals_first={F[0].reshape(F.shape[1],-1).sum(1).round(1)} last={F[-1].reshape(F.shape[1],-1).sum(1).round(1)}")


def cents(f):
    lab, n = ndimage.label(f > 0.4)
    if n == 0:
        return np.zeros((0, 2)), np.zeros(0)
    c = np.array(ndimage.center_of_mass(f, lab, range(1, n + 1)))
    a = ndimage.sum(np.ones_like(f), lab, range(1, n + 1))
    return c, a


half = len(tr) // 2
sp, ns, ar = [], [], []
for k in range(half, len(tr) - 1):
    c0, _ = cents(tr[k])
    c1, a1 = cents(tr[k + 1])
    ns.append(len(c1))
    ar.extend(a1)
    if len(c0) and len(c1):
        d = np.abs(c1[:, None, :] - c0[None, :, :])
        d = np.minimum(d, np.array([Hh, Ww]) - d)
        dd = np.sqrt((d ** 2).sum(-1)).min(1)
        sp.extend(dd[dd < 8])
stride = max(1, steps // 40) * W.P.get("dt", 1)
print(f"   late-half: blobs~{np.mean(ns):.1f} area~{np.mean(ar) if ar else 0:.0f}px "
      f"speed~{np.mean(sp) / stride if sp else 0:.3f} px/time (frac moving>0.5px/snap {np.mean(np.array(sp) > 0.5) if sp else 0:.2f})")
