"""Find clean divisions in a pack's frames.npz and draw parent -> child -> grandchild strips.

python threads/flow-lenia/scripts/division_chain.py PACKDIR OUT.png [--thr 0.15] [--live 20]
A clean division: one component at frame f overlaps >= 2 components at f+1 that overlap nothing
else, and each child then lives >= --live frames in 1-to-1 correspondence (no merge, no split).
A chain is a clean division whose child later divides cleanly itself (2 generations).
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage


def segment(m, thr):
    lab, n = ndimage.label(ndimage.gaussian_filter(m, 1, mode="wrap") > thr)
    if n:
        area = ndimage.sum(np.ones_like(m), lab, range(1, n + 1))
        for i, a in enumerate(area):
            if a < 6:
                lab[lab == i + 1] = 0
    return lab


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pack"); ap.add_argument("out")
    ap.add_argument("--thr", type=float, default=0.15)
    ap.add_argument("--live", type=int, default=20)
    a = ap.parse_args()
    M = np.load(Path(a.pack) / "frames.npz")["matter"].astype(np.float32)
    T, H, W = M.shape
    labs = [segment(m, a.thr) for m in M]
    fwd, bwd = [], []  # fwd[f][i] = set of components at f+1 overlapping i at f
    for f in range(T - 1):
        A, B = labs[f], labs[f + 1]
        mask = (A > 0) & (B > 0)
        pairs = set(zip(A[mask].tolist(), B[mask].tolist()))
        F, Bk = {}, {}
        for i, j in pairs:
            F.setdefault(i, set()).add(j); Bk.setdefault(j, set()).add(i)
        fwd.append(F); bwd.append(Bk)

    def follow(f, j):
        """Follow component j from frame f while 1-to-1; return list of (frame, id)."""
        path = [(f, j)]
        while f < T - 1:
            nxt = fwd[f].get(j, set())
            if len(nxt) != 1:
                break
            k = next(iter(nxt))
            if len(bwd[f].get(k, set())) != 1:
                break
            f, j = f + 1, k
            path.append((f, j))
        return path

    divisions = []
    for f in range(T - 1):
        for i, ch in fwd[f].items():
            if len(ch) < 2 or any(len(bwd[f][c]) != 1 for c in ch):
                continue
            paths = [follow(f + 1, c) for c in ch]
            if all(len(p) >= a.live for p in paths):
                divisions.append({"frame": f, "parent": i, "paths": paths})
    print(f"{len(divisions)} clean divisions (children live >= {a.live} frames)")
    # chains: a child path that ends in another clean division
    chains = []
    for d in divisions:
        for p in d["paths"]:
            fe, je = p[-1]
            for d2 in divisions:
                if d2["frame"] == fe and d2["parent"] == je:
                    chains.append((d, p, d2))
    print(f"{len(chains)} two-generation chains")

    def cen(f, j):
        ys, xs = np.nonzero(labs[f] == j)
        return ys.mean(), xs.mean()

    def crop(f, cy, cx, half=18):
        ys = (np.arange(int(cy) - half, int(cy) + half)) % H
        xs = (np.arange(int(cx) - half, int(cx) + half)) % W
        x = M[f][np.ix_(ys, xs)] / max(M.max() * 0.8, 1e-9)
        rgb = np.stack([x ** 0.8, x ** 1.5 * 0.9 + 0.1 * x, 0.35 * x + 0.65 * x ** 3], -1)
        return Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).resize((96, 96), Image.NEAREST)

    rows = []
    for d, p, d2 in chains[:4]:
        # frames: 4 before division 1, the division, along child p, division 2, after
        f1, f2 = d["frame"], d2["frame"]
        seq = [max(0, f1 - 10), f1, f1 + 1, f1 + 5]
        seq += [int(x) for x in np.linspace(f1 + 10, f2 - 2, 3)] + [f2, f2 + 1, f2 + 5, f2 + 15]
        seq = [min(s, T - 1) for s in seq]
        tiles = []
        for s in seq:
            if s <= f1:
                cy, cx = cen(f1, d["parent"])
            elif s <= f2:
                cy, cx = cen(*p[min(s - p[0][0], len(p) - 1)])
            else:
                q = d2["paths"][0]
                cy, cx = cen(*q[min(s - q[0][0], len(q) - 1)])
            tiles.append((s, crop(s, cy, cx)))
        rows.append(tiles)
    if not rows:
        return
    ncol = max(len(r) for r in rows)
    img = Image.new("RGB", (ncol * 100, len(rows) * 114 + 20), (20, 20, 24))
    dr = ImageDraw.Draw(img)
    dr.text((4, 4), f"{Path(a.pack).name}: parent -> division -> child -> child divides (frame numbers; crops follow the lineage)", fill=(230, 230, 230))
    for r, tiles in enumerate(rows):
        for c, (s, t) in enumerate(tiles):
            img.paste(t, (c * 100 + 2, 20 + r * 114))
            dr.text((c * 100 + 4, 20 + r * 114 + 97), f"f{s}", fill=(220, 220, 220))
    img.save(a.out)


if __name__ == "__main__":
    main()
