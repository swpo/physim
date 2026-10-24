"""Render a long movie of a world with fixed colour scales, a time stamp and a legend bar.

python threads/flow-lenia/scripts/showcase.py WORLD OUT.mp4 --seed 0 --size 192 192 --steps 12000 --every 40 --scale 3 --set k=v
Also writes OUT_sheet.png (12 frames) and OUT_totals.json (channel totals per frame).
"""
import argparse, ast, json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from labkit.world import load_world  # noqa: E402
from labkit import render as R  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("world"); ap.add_argument("out")
ap.add_argument("--seed", type=int, default=0); ap.add_argument("--size", type=int, nargs=2)
ap.add_argument("--steps", type=int, default=12000); ap.add_argument("--every", type=int, default=40)
ap.add_argument("--scale", type=int, default=3); ap.add_argument("--fps", type=int, default=20)
ap.add_argument("--legend", default=""); ap.add_argument("--set", nargs="*", default=[])
a = ap.parse_args()
W = load_world(a.world)
for kv in a.set:
    k, v = kv.split("=", 1)
    try: v = ast.literal_eval(v)
    except Exception: pass
    W.CFG[k] = v
s = W.init(a.seed, tuple(a.size or W.META["size"]))
frames, tt, totals = [], [], []
for t in range(a.steps + 1):
    if t: s = W.step(s)
    if t % a.every == 0:
        F = np.asarray(W.fields(s), np.float32)
        frames.append(F.astype(np.float16)); tt.append(t * float(W.META["dt"])); totals.append(F.reshape(F.shape[0], -1).sum(1).tolist())
st = np.stack(frames).astype(np.float32)
scales = R.channel_scales(st)
names = W.META["channels"]
rgb = []
for F, t in zip(st, tt):
    im = Image.fromarray(R.composite(R.normalize(F, scales))).resize((F.shape[2] * a.scale, F.shape[1] * a.scale), Image.NEAREST)
    canvas = Image.new("RGB", (im.width, im.height + 22), (16, 16, 20)); canvas.paste(im, (0, 22))
    d = ImageDraw.Draw(canvas)
    d.text((6, 4), f"{W.META['name']}  t={t:7.1f}   {a.legend or '  '.join(names)}", fill=(235, 235, 235))
    rgb.append(np.asarray(canvas))
R.save_movie(rgb, a.out, fps=a.fps)
pick = np.unique(np.linspace(0, len(rgb) - 1, 12).round().astype(int))
R.contact_sheet([np.asarray(Image.fromarray(rgb[k]).resize((256, 278))) for k in pick], [f"t={tt[k]:g}" for k in pick], ncols=6,
                title=f"{W.META['name']} seed {a.seed} (fixed colour scales)").save(a.out.replace(".mp4", "_sheet.png"))
Path(a.out.replace(".mp4", "_totals.json")).write_text(json.dumps({"t": tt, "totals": totals, "channels": names}))
print("wrote", a.out, len(rgb), "frames", Path(a.out).stat().st_size // 1024, "KB")
