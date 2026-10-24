"""Render a protocell pack (phi, u, [psi], alleles...) from frames.npz into a readable movie + sheet.
python protocell_movie.py pack/seedN [--psi 2] [--alleles 3] [--labels a,b,c,d]
Background: fuel (dark = depleted). Body: colour of the dominant allele (brightness = catalyst level).
Membrane: amphiphile drawn as a white rim. Writes protocells.mp4 and protocells.png in the seed dir."""
import argparse, json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from labkit.render import save_movie, _font
ap = argparse.ArgumentParser(); ap.add_argument("seed_dir")
ap.add_argument("--psi", type=int, default=2); ap.add_argument("--alleles", type=int, default=3)
ap.add_argument("--labels", default=None); ap.add_argument("--scale", type=int, default=3)
a = ap.parse_args()
d = Path(a.seed_dir); z = np.load(d / "frames.npz"); R = z["render"].astype(np.float32); fr = z["render_f"]
m = json.load(open(d / "metrics.json")); dtf = m["steps_per_frame"] * 0.5
COL = np.array([[0.35, 0.55, 1.0], [0.25, 0.95, 0.45], [1.0, 0.75, 0.15], [1.0, 0.3, 0.3], [0.8, 0.4, 1.0]])
psmax = np.percentile(R[:, a.psi], 99.7) if a.psi >= 0 else 1
umin, umax = np.percentile(R[:, 1], [1, 99.5])
out = []
for F in R:
    body = np.clip((F[0] + 1) / 2, 0, 1)
    fuel = np.clip((F[1] - umin) / (umax - umin + 1e-9), 0, 1)
    bg = np.stack([0.20 + 0.25 * fuel, 0.13 + 0.17 * fuel, 0.08 + 0.05 * fuel], -1)
    al = F[a.alleles:]
    dom = al.argmax(0); amp = np.clip(al.max(0) / 0.9, 0, 1)
    cell = COL[dom % len(COL)] * (0.35 + 0.65 * amp[..., None])
    rgb = bg * (1 - body[..., None]) + cell * body[..., None]
    if a.psi >= 0:
        mem = np.clip(F[a.psi] / psmax, 0, 1)[..., None] ** 0.8
        rgb = rgb * (1 - mem) + mem * np.array([1.0, 0.97, 0.92])
    img = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).resize(
        (rgb.shape[1] * a.scale, rgb.shape[0] * a.scale), Image.BICUBIC)
    out.append(img)
labels = (a.labels.split(",") if a.labels else [f"allele {i}" for i in range(R.shape[1] - a.alleles)])
font = _font(13)
frames = []
for img, f in zip(out, fr):
    im = img.copy(); dr = ImageDraw.Draw(im)
    dr.text((6, 4), f"t={f * dtf:.0f}", fill=(255, 255, 255), font=font)
    x = 6
    for i, lb in enumerate(labels):
        c = tuple(int(255 * v) for v in COL[i % len(COL)])
        dr.rectangle([x, im.height - 16, x + 10, im.height - 6], fill=c); dr.text((x + 13, im.height - 19), lb, fill=(230, 230, 230), font=font)
        x += 14 + 8 * len(lb)
    frames.append(np.asarray(im))
save_movie(frames, d / "protocells.mp4", fps=10)
idx = np.linspace(0, len(frames) - 1, 12).round().astype(int)
tiles = [frames[i] for i in idx]
row = lambda ts: np.concatenate([np.pad(t, ((2, 2), (2, 2), (0, 0))) for t in ts], 1)
sheet = np.concatenate([row(tiles[:6]), row(tiles[6:])], 0)
Image.fromarray(sheet).resize((sheet.shape[1] // 2, sheet.shape[0] // 2), Image.LANCZOS).save(d / "protocells.png")
print("wrote", d / "protocells.mp4", d / "protocells.png")
