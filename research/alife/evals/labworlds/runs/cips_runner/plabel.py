"""Periodic 8-connected labelling of e > 0.5 (area >= 6 px)."""
import numpy as np
from scipy import ndimage

ST = np.ones((3, 3))


def plabel(mask, min_area=6):
    lab, n = ndimage.label(mask, structure=ST)
    parent = np.arange(n + 1)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        if a and b:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)

    H, W = mask.shape
    for d in (-1, 0, 1):   # wrap rows (8-connected: diagonal neighbours across the edge too)
        a, b = lab[H - 1], np.roll(lab[0], d)
        for x, y in zip(a[(a > 0) & (b > 0)], b[(a > 0) & (b > 0)]):
            union(x, y)
        a, b = lab[:, W - 1], np.roll(lab[:, 0], d)
        for x, y in zip(a[(a > 0) & (b > 0)], b[(a > 0) & (b > 0)]):
            union(x, y)
    roots = np.array([find(i) for i in range(n + 1)])
    lab = roots[lab]
    ids = [i for i in np.unique(lab) if i]
    out = np.zeros_like(lab)
    j = 0
    for i in ids:
        m = lab == i
        if m.sum() >= min_area:
            j += 1
            out[m] = j
    return out, j
