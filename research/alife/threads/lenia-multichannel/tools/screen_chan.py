"""Screen creatures from Chan's catalogue: place one, run, record mass/bbox, save a strip image.

python screen_chan.py catalogue.json OUTDIR idx [idx ...] [--steps N] [--size S] [--T T]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import mcl  # noqa: E402

PAL = np.array([[0.1, 0.85, 0.95], [1.0, 0.55, 0.1], [0.95, 0.2, 0.55], [0.45, 0.95, 0.3]])


def rgb(A):
    x = np.tensordot(A.transpose(1, 2, 0), PAL[: A.shape[0]], axes=1)
    return (255 * (1 - np.exp(-1.6 * x))).astype(np.uint8)


def run(entry, size, steps, T=None, scale=1.0, nframes=8):
    rule, cells = mcl.from_chan(entry)
    C = cells.shape[0]
    R = entry["R"] * scale
    if scale != 1.0:
        from scipy.ndimage import zoom
        cells = np.stack([zoom(c, scale, order=1) for c in cells]).clip(0, 1)
    TT = T or entry["T"]
    sim = mcl.MCL(rule, C, (size, size), R, TT)
    A = np.zeros((C, size, size))
    h, w = cells.shape[1:]
    y0, x0 = (size - h) // 2, (size - w) // 2
    A[:, y0:y0 + h, x0:x0 + w] = cells[:, :min(h, size), :min(w, size)]
    frames, mass = [], []
    every = max(1, steps // (nframes - 1))
    for t in range(steps + 1):
        if t % every == 0 and len(frames) < nframes:
            frames.append(rgb(A))
        mass.append(A.sum((1, 2)))
        if t < steps:
            A = sim.step(A)
    return np.array(mass), frames, A


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cat")
    ap.add_argument("out")
    ap.add_argument("idx", nargs="+", type=int)
    ap.add_argument("--steps", type=int, default=300)
    ap.add_argument("--size", type=int, default=128)
    ap.add_argument("--T", type=float, default=None)
    ap.add_argument("--scale", type=float, default=1.0)
    a = ap.parse_args()
    cat = json.load(open(a.cat))
    Path(a.out).mkdir(parents=True, exist_ok=True)
    for i in a.idx:
        e = cat[i]
        mass, frames, A = run(e, a.size, a.steps, a.T, a.scale)
        m0, m1 = mass[0].sum(), mass[-1].sum()
        occ = float(((A.sum(0)) > 0.1).mean())
        img = np.concatenate([np.pad(f, ((2, 2), (2, 2), (0, 0)), constant_values=40) for f in frames], 1)
        Image.fromarray(img).save(f"{a.out}/c{i}.png")
        print(f"{i} {e['file']} '{e['name']}' C={e['nc']} K={e['nk']} R={e['R']} T={e['T']} mass {m0:.0f}->{m1:.0f} occ {occ:.3f}")
