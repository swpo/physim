"""Movie of a gene world, coloured by trait: red = high g, blue = low g, white-ish = g near 0, green = food.

python movie_gene.py world.py OUT.mp4 STEPS SIZE SEED EVERY [KEY=VAL ...] [-- KEY=VAL ...]
Arguments after "--" define a second run shown side by side (same seed), e.g. selection | neutral.
LABEL=... inside each argument group sets that panel title.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from labkit.render import save_movie, _font  # noqa: E402
from labkit.world import load_world  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

out = sys.argv[2]
steps, size, seed, every = (int(x) for x in sys.argv[3:7])
rest = sys.argv[7:]
cfgs = [rest[:rest.index("--")], rest[rest.index("--") + 1:]] if "--" in rest else [rest]


def run(cfg):
    W = load_world(sys.argv[1])
    label = ""
    for kv in cfg:
        k, v = kv.split("=", 1)
        if k == "LABEL":
            label = v
            continue
        setattr(W, k, eval(v, dict(vars(W)) | {"np": np}))
    return W, W.init(seed, (size, size)), label


panels = [run(c) for c in cfgs]
frames = []
for t in range(steps + 1):
  row = []
  for pi, (W, s, label) in enumerate(panels):
    if t % every == 0:
        M = np.clip(s["A"].sum(0), 0, 1)
        core = np.clip(s["A"][0], 0, 1)
        g = np.clip(s["g"], -1, 1)
        F = np.clip(s["F"], 0, 1)
        r = M * np.clip(0.55 + 0.6 * g, 0, 1)
        b = M * np.clip(0.55 - 0.6 * g, 0, 1)
        gr = 0.30 * F * (1 - M) + 0.45 * core * (1 - np.abs(g))
        rgb = (255 * np.clip(np.stack([r + 0.15 * core, gr + 0.05, b + 0.15 * core], -1), 0, 1)).astype(np.uint8)
        im = Image.fromarray(rgb).resize((size * 3, size * 3), Image.NEAREST)
        ImageDraw.Draw(im).text((6, 4), f"{label}  step {t}", fill=(255, 255, 255), font=_font(14))
        row.append(np.pad(np.asarray(im), ((0, 0), (0, 4), (0, 0))))
    if t < steps:
        panels[pi] = (W, W.step(s), label)
  if row:
    frames.append(np.concatenate(row, 1))
save_movie(frames, out, fps=12)
print(out, len(frames), "frames")
