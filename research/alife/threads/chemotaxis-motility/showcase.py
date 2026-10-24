"""Render the showcase movie: evopursuit from noise to evolutionary rescue.

Runs the world itself and records every `every` time units. Colours are fixed for the whole movie:
prey allele A cyan, prey allele B orange, predators magenta, nutrient as a dim green background
(dark wakes = eaten food). A strip at the bottom plots prey-A, prey-B and predator mass so far.
usage: python showcase.py world.py out.mp4 seed size T [every=5] [k=v ...]
"""
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, ".")
import imageio.v2 as imageio  # noqa: E402
from labkit.world import load_world  # noqa: E402

args = [a for a in sys.argv[1:] if "=" not in a]
kv = dict(a.split("=") for a in sys.argv[1:] if "=" in a)
every = float(kv.pop("every", 5))
W = load_world(args[0])
for k, v in kv.items():
    W.P[k] = float(v)
out, seed, N, T = args[1], int(args[2]), int(args[3]), float(args[4])
s = W.init(seed, (N, N))
nsub = int(round(every / W.P["dt"]))
cA, cB, cQ = np.array([0.15, 0.85, 1.0]), np.array([1.0, 0.6, 0.1]), np.array([1.0, 0.2, 0.75])
hist, imgs = [], []
t = 0.0
SC = 3 if N <= 192 else 2
while t <= T + 1e-9:
    A, B, q, n = np.asarray(W.fields(s), np.float32)
    hist.append((A.sum(), B.sum(), q.sum()))
    base = np.stack([0.05 + 0.10 * n, 0.08 + 0.22 * n, 0.05 + 0.08 * n], -1)   # dark-green food field
    rgb = base
    for f, c in ((A, cA), (B, cB), (q, cQ)):
        a = np.clip(f / 0.9, 0, 1)[..., None]
        rgb = rgb * (1 - 0.85 * a) + c * a
    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).resize((N * SC, N * SC), Image.BILINEAR)
    # population strip
    Hs = 90
    canvas = Image.new("RGB", (N * SC, N * SC + Hs + 22), (14, 14, 18))
    canvas.paste(im, (0, 22))
    d = ImageDraw.Draw(canvas)
    lab, nb = ndimage.label((A + B) > 0.35)
    nA = nB = 0
    if nb:
        ids = range(1, nb + 1)
        fa = np.array(ndimage.sum(A, lab, ids)); fbb = np.array(ndimage.sum(B, lab, ids))
        frac = fbb / np.maximum(fa + fbb, 1e-9)
        area = np.array(ndimage.sum(np.ones_like(A), lab, ids))
        nA, nB = int(((frac < 0.5) & (area >= 12)).sum()), int(((frac >= 0.5) & (area >= 12)).sum())
    d.text((6, 4), f"evopursuit  seed {seed}  t = {t:5.0f}   prey bodies: A {nA:2d}  B {nB:2d}", fill=(230, 230, 230))
    hh = np.array(hist)
    mx = max(hh.max(), 1e-9)
    y0 = N * SC + 22
    for j, c in enumerate((cA, cB, cQ)):
        pts = [(5 + (N * SC - 10) * i / max(T / every, 1), y0 + Hs - 6 - (Hs - 12) * v / mx) for i, v in enumerate(hh[:, j])]
        if len(pts) > 1:
            d.line(pts, fill=tuple((c * 255).astype(int)), width=2)
    d.text((8, y0 + 2), "mass: prey A (cyan), prey B (orange), predators (magenta)", fill=(200, 200, 200))
    imgs.append(np.asarray(canvas))
    for _ in range(nsub):
        s = W.step(s)
    t += every
imageio.mimwrite(out, imgs, fps=20, codec="libx264", quality=6, macro_block_size=1, ffmpeg_log_level="error")
print(out, len(imgs), "frames")
