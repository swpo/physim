"""Render a showcase movie of a world with fixed colour scales over the whole run.
python showcase.py WORLD OUT.mp4 SIZE STEPS EVERY [seed] [key=val ...]"""
import sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, ".")
from labkit.world import load_world
from labkit import render as R
import imageio.v2 as imageio

world, out, size, steps, every = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
seed = int(sys.argv[6]) if len(sys.argv) > 6 else 0
W = load_world(world)
for kv in sys.argv[7:]:
    k, v = kv.split("="); W.P[k] = type(W.P[k])(eval(v))
s = W.init(seed, (size, size))
frames, ts = [], []
for t in range(steps + 1):
    if t % every == 0:
        frames.append(np.asarray(W.fields(s), np.float16)); ts.append(t)
    s = W.step(s)
F = np.stack(frames).astype(np.float32)
sc = R.channel_scales(F)
names = W.META["channels"]
with imageio.get_writer(out, fps=20, codec="libx264", quality=7, macro_block_size=1) as wr:
    for fr, t in zip(F, ts):
        img = Image.fromarray(R.composite(R.normalize(fr, sc))).resize((512, 512), Image.BILINEAR)
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, 512, 18], fill=(10, 10, 14))
        d.text((6, 3), f"{W.META['name']}  t={t * W.META['dt']:g}   " + " | ".join(names), fill=(230, 230, 230))
        wr.append_data(np.asarray(img))
print("frames", len(ts), "->", out)
