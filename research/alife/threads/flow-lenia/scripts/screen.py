"""Quick screen: run a world with CFG overrides and save a strip of frames.

python threads/flow-lenia/scripts/screen.py WORLD OUT.png --steps 600 --frames 8 --set key=val ...
Prints mass drift, n components (threshold 0.1*max) at the end, and wall time.
"""
import argparse
import ast
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from labkit.world import load_world  # noqa: E402
from labkit import render as R  # noqa: E402


def run(world, out, steps=600, nframes=8, size=None, seed=0, sets=(), tile=128, quiet=False):
    W = load_world(world)
    for kv in sets:
        k, v = kv.split("=", 1)
        try:
            v = ast.literal_eval(v)
        except Exception:
            pass
        W.CFG[k] = v
    size = tuple(size or W.META["size"])
    s = W.init(seed, size)
    F0 = np.asarray(W.fields(s), float)
    m0 = F0[: (W.CFG.get("C", F0.shape[0]))].sum()
    keep = np.unique(np.linspace(0, steps, nframes).round().astype(int))
    frames, t0 = [], time.time()
    def com(F):
        m = F[: W.CFG.get("C", F.shape[0])].sum(0); H, Wd = m.shape
        ang = lambda n, ax: np.angle((m.sum(ax) * np.exp(2j * np.pi * np.arange(n) / n)).sum()) * n / (2 * np.pi)
        return np.array([ang(H, 1), ang(Wd, 0)])
    path = [com(F0)]
    for t in range(steps + 1):
        if t:
            s = W.step(s)
        if t in keep:
            frames.append(np.asarray(W.fields(s), float))
            path.append(com(frames[-1]))
    F = frames[-1]
    m1 = F[: (W.CFG.get("C", F.shape[0]))].sum()
    mat = F[: W.CFG.get("C", F.shape[0])].sum(0)
    lab, n = ndimage.label(ndimage.gaussian_filter(mat, 1) > 0.15 * mat.max())
    areas = ndimage.sum(np.ones_like(mat), lab, range(1, n + 1)) if n else []
    occ = float((lab > 0).mean())
    d = np.diff(np.array(path), axis=0); d = (d + size[0] / 2) % size[0] - size[0] / 2
    travel = float(np.hypot(*d.sum(0)))
    st = np.stack(frames)
    scales = R.channel_scales(st)
    ims = [R.composite(R.normalize(f, scales)) for f in frames]
    ims = [np.asarray(Image.fromarray(i).resize((tile, tile), Image.NEAREST)) for i in ims]
    R.contact_sheet(ims, [f"t{t}" for t in keep], ncols=len(ims), title=Path(out).stem).save(out)
    msg = (f"{Path(out).stem}: drift {m1 / m0 - 1:+.2e}  comps {n} areas {sorted(int(a) for a in areas)[-6:]} "
           f"occ {occ:.2f} com_travel {travel:.1f}px  wall {time.time() - t0:.1f}s")
    if not quiet:
        print(msg, flush=True)
    return msg


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("world"); ap.add_argument("out")
    ap.add_argument("--steps", type=int, default=600)
    ap.add_argument("--frames", type=int, default=8)
    ap.add_argument("--size", type=int, nargs=2)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--set", nargs="*", default=[])
    a = ap.parse_args()
    run(a.world, a.out, a.steps, a.frames, a.size, a.seed, a.set)
