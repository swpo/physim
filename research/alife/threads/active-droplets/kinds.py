"""Run a catalyst world and print per-kind droplet counts over time; save strip image.
python kinds.py world.py out.png --steps N --frames K --size S --seed s --set k=v ...
Kind of a droplet = argmax of mean catalyst (a vs b) inside the phi>0 component."""
import argparse, sys, time
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from labkit.world import load_world
ap = argparse.ArgumentParser(); ap.add_argument("world"); ap.add_argument("out")
ap.add_argument("--steps", type=int, default=20000); ap.add_argument("--frames", type=int, default=10)
ap.add_argument("--size", type=int, default=128); ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--set", nargs="*", default=[])
a = ap.parse_args(); W = load_world(a.world)
for kv in a.set:
    k, v = kv.split("="); W.P[k] = type(W.P[k])(eval(v))
s = W.init(a.seed, (a.size, a.size)); per = a.steps // (a.frames - 1); imgs = []; t0 = time.time()
def look(s):
    phi, A, B = s["phi"], s["a"], s["b"]
    lab, n = ndimage.label(phi > 0)
    if n == 0: return 0, 0, 0
    ma = ndimage.mean(A, lab, range(1, n + 1)); mb = ndimage.mean(B, lab, range(1, n + 1))
    mixed = np.sum(np.minimum(ma, mb) > 0.3 * np.maximum(ma, mb))
    return int(np.sum(ma > mb)), int(np.sum(mb >= ma)), int(mixed)
for f in range(a.frames):
    if f: 
        for _ in range(per): s = W.step(s)
    na, nb, nm = look(s)
    print(f"t={f*per*W.P['dt']:.0f} A={na} B={nb} mixed={nm}", flush=True)
    rgb = np.stack([np.clip(s["a"], 0, 1), np.clip((s["phi"] + 1) / 2, 0, 1) * 0.5, np.clip(s["b"], 0, 1)], -1)
    rgb[..., 1] += 0.5 * np.clip((s["phi"] + 1) / 2, 0, 1) * (1 - np.clip(s["a"] + s["b"], 0, 1))
    imgs.append(np.pad(rgb, ((1, 1), (1, 1), (0, 0)), constant_values=1))
Image.fromarray((np.concatenate(imgs, 1) * 255).clip(0, 255).astype(np.uint8)).save(a.out)
print(f"{time.time()-t0:.0f}s")
