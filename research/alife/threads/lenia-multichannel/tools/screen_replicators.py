"""Screen random graphs for spontaneous replication: start from a SMALL noise patch and flag rules whose
number of discrete, bounded-size individuals keeps increasing.

python screen_replicators.py OUT FAMILY N [--size 128] [--patch 24] [--steps 1500] [--seed 0]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).parent))
import mcl  # noqa: E402
from screen_random import make_rule, rgb  # noqa: E402


def comps(A):
    m = ndimage.gaussian_filter(A.sum(0), 1, mode="wrap")
    mask = m > 0.3 * max(m.max(), 1e-9)
    lab, n = ndimage.label(mask)
    if n == 0:
        return 0, 0.0, 0.0
    a = ndimage.sum(mask, lab, range(1, n + 1))
    a = a[a >= 12]
    return len(a), float(mask.mean()), float(a.max()) if len(a) else 0.0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("fam")
    ap.add_argument("n", type=int)
    ap.add_argument("--size", type=int, default=128)
    ap.add_argument("--patch", type=int, default=24)
    ap.add_argument("--steps", type=int, default=1500)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--R", type=float, default=10)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(5000 + a.seed)
    rows, hits = [], []
    checks = [a.steps // 3, 2 * a.steps // 3, a.steps]
    for i in range(a.n):
        C, ks = make_rule(a.fam, rng)
        sim = mcl.MCL([dict(k) for k in ks], C, (a.size, a.size), a.R, 10)
        r2 = np.random.default_rng(i)
        A = np.zeros((C, a.size, a.size))
        c0 = a.size // 2 - a.patch // 2
        A[:, c0:c0 + a.patch, c0:c0 + a.patch] = r2.random((C, a.patch, a.patch))
        series, frames = [], []
        for t in range(1, a.steps + 1):
            A = sim.step(A)
            if t in checks:
                series.append(comps(A))
                frames.append(rgb(A))
            if t == checks[0] and A.sum() < 1:
                break
        while len(series) < 3:
            series.append((0, 0.0, 0.0))
            frames.append(rgb(A))
        n1, n2, n3 = (s[0] for s in series)
        occ, amax = series[-1][1], series[-1][2]
        rep = n3 >= 4 and n3 > n1 and n2 >= n1 and occ < 0.5 and amax < 0.05 * a.size ** 2
        rows.append(dict(i=i, fam=a.fam, C=C, n=[n1, n2, n3], occ=occ, amax=amax, rep=bool(rep), rule=ks))
        if rep:
            hits.append((i, np.concatenate([np.pad(f, ((1, 1), (1, 1), (0, 0)), constant_values=60) for f in frames], 1)))
        print(i, "REP" if rep else "", n1, n2, n3, f"occ {occ:.2f}", flush=True)
    json.dump(rows, open(out / f"rep_{a.fam}_s{a.seed}.json", "w"))
    if hits:
        Image.fromarray(np.concatenate([h for _, h in hits[:30]], 0)).save(out / f"rep_{a.fam}_s{a.seed}.png")
        (out / f"rep_{a.fam}_s{a.seed}.txt").write_text(" ".join(str(i) for i, _ in hits[:30]))
    print("hits", [i for i, _ in hits])
