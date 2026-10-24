"""Run ad5-style worlds (state['a'] is (N,H,W)); print per-allele droplet counts; save colour strip.
python alleles.py world.py out.png --steps N --frames K --seed s --set k=v ..."""
import argparse, sys, time
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from labkit.world import load_world
from labkit.metrics import periodic_label
from scipy import ndimage
ap = argparse.ArgumentParser(); ap.add_argument("world"); ap.add_argument("out")
ap.add_argument("--steps", type=int, default=40000); ap.add_argument("--frames", type=int, default=12)
ap.add_argument("--size", type=int, default=128); ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--set", nargs="*", default=[])
a = ap.parse_args(); W = load_world(a.world)
for kv in a.set:
    k, v = kv.split("="); W.P[k] = type(W.P[k])(v) if isinstance(W.P[k], str) else type(W.P[k])(eval(v))
COL = np.array([[0.3, 0.6, 1.0], [0.3, 1.0, 0.4], [1.0, 0.8, 0.2], [1.0, 0.25, 0.25], [0.8, 0.3, 1.0], [1, 1, 1]])
s = W.init(a.seed, (a.size, a.size)); per = a.steps // (a.frames - 1); imgs = []; t0 = time.time()
rows = []
for f in range(a.frames):
    if f:
        for _ in range(per): s = W.step(s)
    lab, n = periodic_label(s["phi"] > 0)
    N = s["a"].shape[0]
    cnt = np.zeros(N + 1, int)
    if n:
        means = np.stack([ndimage.mean(s["a"][i], lab, range(1, n + 1)) for i in range(N)])
        kind = np.where(means.max(0) > 0.05, means.argmax(0), N)
        cnt = np.bincount(kind, minlength=N + 1)
    ev = s["events"]; nm = sum(e[0] == "mut" for e in ev); nd = sum(e[0] == "dil" for e in ev)
    print(f"t={s['t']:.0f} droplets={n} per-allele={cnt[:N].tolist()} none={cnt[N]} muts={nm} dils={nd}", flush=True)
    al = s["a"]; dom = al.argmax(0); amp = np.clip(al.max(0), 0, 1)
    body = np.clip((s["phi"] + 1) / 2, 0, 1)
    rgb = COL[dom] * amp[..., None] * 0.9 + 0.25 * body[..., None]
    imgs.append(np.pad(np.clip(rgb, 0, 1), ((1, 1), (1, 1), (0, 0)), constant_values=1))
Image.fromarray((np.concatenate(imgs, 1) * 255).astype(np.uint8)).save(a.out)
print(f"{time.time()-t0:.0f}s")
