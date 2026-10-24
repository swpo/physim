"""Sweep one or two RULE entries of a world and log component counts over time + a montage of final frames.

python sweep.py world.py OUT.png --steps 2000 --size 128 --seed 0 --expr 'RULE[0]["h"]' --vals 0.1 0.2 0.3
    (each value v is applied as exec(f"{expr} = {v}") on a fresh copy of the module's RULE)
"""
import argparse
import copy
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import quick  # noqa: E402
from labkit.world import load_world  # noqa: E402

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("world")
    ap.add_argument("out")
    ap.add_argument("--steps", type=int, default=2000)
    ap.add_argument("--size", type=int, default=128)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--expr", required=True)
    ap.add_argument("--vals", nargs="+", required=True)
    ap.add_argument("--frames", type=int, default=8)
    a = ap.parse_args()
    W = load_world(a.world)
    base = copy.deepcopy(W.RULE)
    rows = []
    for v in a.vals:
        W.RULE = copy.deepcopy(base)
        exec(f"{a.expr} = {v}", {"RULE": W.RULE})
        s = W.init(a.seed, (a.size, a.size))
        every = max(1, a.steps // (a.frames - 1))
        tiles, log = [], []
        for t in range(a.steps + 1):
            if t % every == 0:
                A = np.asarray(W.fields(s))[: W.C]
                log.append(f"{t}:{A.sum():.0f}/{quick.ncomp(A.sum(0))}")
                tiles.append(np.pad(quick.rgb(A), ((2, 2), (2, 2), (0, 0)), constant_values=50))
            if t < a.steps:
                s = W.step(s)
        print(f"{a.expr}={v}: " + " ".join(log), flush=True)
        rows.append(np.concatenate(tiles[: a.frames], 1))
    Image.fromarray(np.concatenate(rows, 0)).save(a.out)
