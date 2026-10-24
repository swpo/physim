"""Screen random channel/kernel graphs from noise.

python screen_random.py OUT FAMILY N [--size 96] [--R 10] [--steps 400] [--seed 0]

Families (graph topology of kernel c0 -> c1 edges):
  full   : C=3, 3 self kernels per channel + all 6 cross edges (Chan 2020 '233' template)
  cycle  : C=3, 2 self kernels per channel + cycle 0->1->2->0
  shell  : C=2, core channel 0 (3 self kernels), shell 1 fed by 0 through an outer-ring
           kernel, shell inhibits core (cross kernel with low m), shell self kernel
  two    : C=2, 2 self per channel + both cross edges
  star   : C=3, channel 0 self-sustains (3 self), 1 and 2 only fed by 0 and by themselves
Classification at the end, with a persistence check between 75% and 100% of the run.
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

PAL = np.array([[0.1, 0.85, 0.95], [1.0, 0.55, 0.1], [0.95, 0.2, 0.55]])


def rgb(A):
    x = np.tensordot(A.transpose(1, 2, 0), PAL[: A.shape[0]], axes=1)
    return (255 * (1 - np.exp(-1.6 * x))).astype(np.uint8)


def rand_b(rng):
    B = rng.integers(1, 4)
    b = [int(rng.integers(0, 13)) for _ in range(B)]
    b[int(rng.integers(B))] = 12
    return ",".join(f"{x}/12" for x in b)


def rand_k(rng, c0, c1, m=None, b=None, s=None, r=None):
    m = float(rng.uniform(0.1, 0.5)) if m is None else m
    s = float(m * rng.uniform(0.1, 0.35)) if s is None else s
    return dict(c0=c0, c1=c1, b=b or rand_b(rng), m=round(m, 4), s=round(s, 4), h=round(float(rng.uniform(0.3, 1)), 3),
                r=r if r is not None else round(float(rng.uniform(0.5, 1.0)), 3))


def make_rule(fam, rng):
    ks = []
    if fam == "full":
        C = 3
        for c in range(C):
            ks += [rand_k(rng, c, c) for _ in range(3)]
        for a in range(C):
            for b in range(C):
                if a != b:
                    ks.append(rand_k(rng, a, b))
    elif fam == "cycle":
        C = 3
        for c in range(C):
            ks += [rand_k(rng, c, c) for _ in range(2)]
        for a in range(C):
            ks.append(rand_k(rng, a, (a + 1) % C))
    elif fam == "two":
        C = 2
        for c in range(C):
            ks += [rand_k(rng, c, c) for _ in range(2)]
        ks += [rand_k(rng, 0, 1), rand_k(rng, 1, 0)]
    elif fam == "star":
        C = 3
        ks += [rand_k(rng, 0, 0) for _ in range(3)]
        for c in (1, 2):
            ks += [rand_k(rng, c, c), rand_k(rng, 0, c), rand_k(rng, c, 0)]
    elif fam == "shell":
        C = 2
        ks += [rand_k(rng, 0, 0) for _ in range(3)]
        # shell grows where the core is seen on an outer ring but not at the centre
        ks.append(rand_k(rng, 0, 1, b=f"0,{int(rng.integers(0, 6))}/12,12/12", m=float(rng.uniform(0.05, 0.3))))
        ks.append(rand_k(rng, 0, 1, r=round(float(rng.uniform(0.2, 0.5)), 3), m=float(rng.uniform(0.0, 0.05)),
                         s=float(rng.uniform(0.01, 0.05))))      # dies where core is dense nearby
        ks.append(rand_k(rng, 1, 1))
        ks.append(rand_k(rng, 1, 0, m=float(rng.uniform(0.0, 0.1)), s=float(rng.uniform(0.01, 0.06))))  # shell suppresses core
    else:
        raise ValueError(fam)
    return C, ks


def classify(A, H, W):
    m = A.sum(0)
    mask = ndimage.gaussian_filter(m, 1, mode="wrap") > 0.3 * max(m.max(), 1e-9)
    occ = float(mask.mean())
    lab, n = ndimage.label(mask)
    areas = ndimage.sum(mask, lab, range(1, n + 1)) if n else np.array([])
    big = areas[areas >= 12]
    return occ, int(len(big)), float(big.max() / (H * W)) if len(big) else 0.0


def run_one(C, ks, size, R, steps, seed, T=10):
    rng = np.random.default_rng(seed)
    H = W = size
    sim = mcl.MCL([dict(k) for k in ks], C, (H, W), R, T)
    A = np.zeros((C, H, W))
    p = int(size * 0.6)
    A[:, :p, :p] = rng.random((C, p, p))
    A = np.roll(A, (size // 5, size // 5), (1, 2))
    snaps = {}
    for t in range(steps + 1):
        if t in (int(0.75 * steps), steps):
            snaps[t] = A.copy()
        if t < steps:
            A = sim.step(A)
    c1 = classify(snaps[int(0.75 * steps)], H, W)
    c2 = classify(A, H, W)
    mass = float(A.sum())
    if mass < 1:
        cls = "dead"
    elif c2[0] > 0.5:
        cls = "sea"
    elif c2[1] >= 1 and c2[2] < 0.15 and abs(c2[1] - c1[1]) <= max(1, 0.3 * c1[1]) and c1[1] >= 1:
        cls = "individuals"
    elif c2[1] >= 1 and c2[2] < 0.15:
        cls = "transient"
    else:
        cls = "blob/pattern"
    return cls, c2, A


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("fam")
    ap.add_argument("n", type=int)
    ap.add_argument("--size", type=int, default=96)
    ap.add_argument("--R", type=float, default=10)
    ap.add_argument("--steps", type=int, default=400)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(1000 + a.seed)
    rows, thumbs = [], []
    for i in range(a.n):
        C, ks = make_rule(a.fam, rng)
        cls, c2, A = run_one(C, ks, a.size, a.R, a.steps, i)
        rows.append(dict(i=i, fam=a.fam, cls=cls, occ=c2[0], ncomp=c2[1], maxfrac=c2[2], C=C, rule=ks))
        if cls == "individuals":
            thumbs.append((i, rgb(A)))
        print(i, cls, f"occ {c2[0]:.2f} n {c2[1]}", flush=True)
    json.dump(rows, open(out / f"{a.fam}_s{a.seed}.json", "w"))
    if thumbs:
        tiles = [np.pad(t, ((2, 2), (2, 2), (0, 0)), constant_values=60) for _, t in thumbs[:40]]
        while len(tiles) % 8:
            tiles.append(np.zeros_like(tiles[0]))
        grid = np.concatenate([np.concatenate(tiles[j:j + 8], 1) for j in range(0, len(tiles), 8)], 0)
        Image.fromarray(grid).save(out / f"{a.fam}_s{a.seed}_ind.png")
        (out / f"{a.fam}_s{a.seed}_ind.txt").write_text(" ".join(str(i) for i, _ in thumbs[:40]))
    from collections import Counter
    print(Counter(r["cls"] for r in rows))
