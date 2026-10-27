"""Helpers copied unchanged from the c00 audit construction/arms.py (pdist, label_p, pcentroid, pick_targets)."""
import numpy as np
from scipy import ndimage
import sys
sys.path.insert(0, "/home/user/physim/research/alife")
sys.path.insert(0, "/home/user/physim/research/alife/collective/contrib/20261027T2013-c60-halftaxis-ecology")
import world as w

def pdist(H, W, cy, cx):
    yy, xx = np.mgrid[0:H, 0:W]
    dy = (yy - cy + H / 2) % H - H / 2; dx = (xx - cx + W / 2) % W - W / 2
    return np.sqrt(dy * dy + dx * dx)

def label_p(x, th=0.5, amin=4):
    """periodic connected components of x > th with area >= amin"""
    L, n = ndimage.label(x > th)
    H, W = x.shape
    # merge labels across the periodic boundary
    par = list(range(n + 1))
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for a, b in list(zip(L[0], L[-1])) + list(zip(L[:, 0], L[:, -1])):
        if a and b: par[f(a)] = f(b)
    lut = np.array([f(i) for i in range(n + 1)]); L = lut[L]
    ids, L = np.unique(L, return_inverse=True); L = L.reshape(x.shape)
    if ids[0] != 0: L = L + 1
    a = np.bincount(L.ravel())
    small = np.where(a < amin)[0]; small = small[small > 0]
    L[np.isin(L, small)] = 0
    ids, L = np.unique(L, return_inverse=True); L = L.reshape(x.shape)
    return L, int(L.max())

def pcentroid(mask):
    H, W = mask.shape; ys, xs = np.nonzero(mask)
    ay = np.angle(np.exp(2j * np.pi * ys / H).mean()) * H / (2 * np.pi) % H
    ax = np.angle(np.exp(2j * np.pi * xs / W).mean()) * W / (2 * np.pi) % W
    return float(ay), float(ax)

def pick_targets(s, n=3, out=None):
    F = w.fields(s); ca, cb = F[0], F[1]
    Lb, nb = label_p(cb); La, na = label_p(ca)
    H, W = cb.shape
    cand = []
    for i in range(1, nb + 1):
        m = Lb == i; a = int(m.sum())
        if a < 10: continue
        near = ndimage.binary_dilation(m, iterations=2, mask=None)
        # periodic dilation: roll-based
        near = m.copy()
        for _ in range(2):
            near = near | np.roll(near, 1, 0) | np.roll(near, -1, 0) | np.roll(near, 1, 1) | np.roll(near, -1, 1)
        prey = [j for j in np.unique(La[near]) if j > 0]
        if len(prey) != 1: continue
        pm = La == prey[0]
        cy, cx = pcentroid(m | pm)
        R = float(pdist(H, W, cy, cx)[m | pm].max()) + 2.0
        cand.append(dict(pred=i, area=a, prey_area=int(pm.sum()), cy=cy, cx=cx, R=R, pcy=pcentroid(m)[0], pcx=pcentroid(m)[1]))
    med = np.median([c["area"] for c in cand])
    for c in cand:
        d4 = pdist(H, W, c["cy"], c["cx"]) <= c["R"] + 4
        c["_coll"] = int(len([j for j in np.unique(Lb[d4]) if j > 0 and j != c["pred"]]))
    cand.sort(key=lambda c: (c["_coll"] > 0, abs(c["area"] - med)))
    chosen = []
    for c in cand:
        if all(pdist(H, W, d["cy"], d["cx"])[int(round(c["cy"])) % H, int(round(c["cx"])) % W] > 40 for d in chosen):
            chosen.append(c)
        if len(chosen) == n: break
    # other predator bodies inside any target disk (collateral)
    for c in chosen:
        disk = pdist(H, W, c["cy"], c["cx"]) <= c["R"]
        c["other_preds_in_disk"] = int(len([j for j in np.unique(Lb[disk]) if j > 0 and j != c["pred"]]))
        disk4 = pdist(H, W, c["cy"], c["cx"]) <= c["R"] + 4
        c["other_preds_in_disk_R4"] = int(len([j for j in np.unique(Lb[disk4]) if j > 0 and j != c["pred"]]))
        c["other_prey_in_disk_R4"] = int(len([j for j in np.unique(La[disk4]) if j > 0]))
    if out: json.dump(dict(t=s["t"], n_pred=nb, n_prey=na, targets=chosen), open(out, "w"), indent=1)
    return chosen

