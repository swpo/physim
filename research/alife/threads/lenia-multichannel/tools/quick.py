"""Quick look at a world with overridden module globals: mass/components over time + a strip PNG.

python quick.py world.py OUT.png --steps 1000 --size 128 --seed 0 --set 'FOOD={"gate":1,...}' --set N_SEED=2
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from labkit.world import load_world  # noqa: E402

PAL = np.array([[0.1, 0.85, 0.95], [1.0, 0.55, 0.1], [0.95, 0.2, 0.55], [0.45, 0.95, 0.3], [0.95, 0.9, 0.25]])


def rgb(F):
    x = np.tensordot(np.clip(F, 0, 1).transpose(1, 2, 0), PAL[: F.shape[0]], axes=1)
    return (255 * (1 - np.exp(-1.6 * x))).astype(np.uint8)


def ncomp(m):
    mask = ndimage.gaussian_filter(m, 1, mode="wrap") > 0.3
    lab, n = ndimage.label(mask)
    if n == 0:
        return 0
    a = ndimage.sum(mask, lab, range(1, n + 1))
    return int((a >= 20).sum())


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("world")
    ap.add_argument("out")
    ap.add_argument("--steps", type=int, default=1000)
    ap.add_argument("--size", type=int, default=128)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--frames", type=int, default=10)
    ap.add_argument("--set", action="append", default=[])
    ap.add_argument("--food-view", action="store_true", help="render F as 4th colour")
    a = ap.parse_args(argv)
    W = load_world(a.world)
    for kv in a.set:
        k, v = kv.split("=", 1)
        setattr(W, k, eval(v, vars(np) | dict(vars(W)) | {"np": np}))
    s = W.init(a.seed, (a.size, a.size))
    C = getattr(W, "C", None) or (len(W.META["matter"]) if W.META.get("matter") else None)
    every = max(1, a.steps // (a.frames - 1))
    tiles, log = [], []
    for t in range(a.steps + 1):
        if t % every == 0:
            F = np.asarray(W.fields(s))
            A = F[:C] if C else F
            log.append((t, float(A.sum()), ncomp(A.sum(0)), float(F[C:].mean()) if C and F.shape[0] > C else -1))
            if len(tiles) < a.frames:
                show = F if a.food_view else A
                tiles.append(np.pad(rgb(show[:5]), ((2, 2), (2, 2), (0, 0)), constant_values=50))
            if not np.isfinite(F).all():
                break
        if t < a.steps:
            s = W.step(s)
    Image.fromarray(np.concatenate(tiles, 1)).save(a.out)
    print(" ".join(f"{t}:{m:.0f}/{n}" + (f"/F{f:.2f}" if f >= 0 else "") for t, m, n, f in log))
    return log


if __name__ == "__main__":
    main()
