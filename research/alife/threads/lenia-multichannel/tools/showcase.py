"""Showcase movie: full grid, fixed colour scales (A channels and food all on [0, 1]).

python showcase.py world.py OUT.mp4 STEPS SIZE SEED EVERY [SCALE] [KEY=VAL ...]
Colours: A0 cyan, A1 orange, A2 magenta (labkit palette, soft saturation); food F is a dim green
background (black = eaten). Label: simulation time and number of cells (A0 > 0.3 components >= 20 px).
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from labkit.render import PALETTE, save_movie, _font  # noqa: E402
from labkit.world import load_world  # noqa: E402

W = load_world(sys.argv[1]); out = sys.argv[2]
steps, size, seed, every = (int(x) for x in sys.argv[3:7])
scale = int(sys.argv[7]) if len(sys.argv) > 7 and "=" not in sys.argv[7] else 2
for kv in [a for a in sys.argv[7:] if "=" in a]:
    k, v = kv.split("=", 1); setattr(W, k, eval(v, dict(vars(W)) | {"np": np}))
s = W.init(seed, (size, size))
dt = float(W.META["dt"])
frames = []
for t in range(steps + 1):
    if t % every == 0:
        A = np.clip(s["A"], 0, 1)
        rgb = np.tensordot(A.transpose(1, 2, 0), PALETTE[:A.shape[0]], axes=1)
        rgb = 1 - np.exp(-1.6 * rgb)
        if "F" in s:
            F = np.clip(s["F"], 0, 1)
            rgb = rgb + (1 - rgb) * np.stack([0.10 * F, 0.32 * F, 0.10 * F], -1)
        lab, n = ndimage.label(A[0] > 0.3)
        nc = int((ndimage.sum(np.ones_like(A[0]), lab, range(1, n + 1)) >= 20).sum()) if n else 0
        im = Image.fromarray((255 * np.clip(rgb, 0, 1)).astype(np.uint8)).resize((size * scale, size * scale), Image.NEAREST)
        ImageDraw.Draw(im).text((6, 4), f"t = {t * dt:.0f}   cells = {nc}", fill=(255, 255, 255), font=_font(14))
        frames.append(np.asarray(im))
    if t < steps:
        s = W.step(s)
save_movie(frames, out, fps=15)
print(out, len(frames))
