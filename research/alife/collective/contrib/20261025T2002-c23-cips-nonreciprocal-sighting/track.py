"""Nearest-centroid tracking of e1 bodies and e2 bodies (threshold 0.4) in a hires npz (frames every 10 t, periodic).
Reports, for tracks alive the whole window, net displacement / body diameter and path length / diameter."""
import sys, numpy as np
from scipy import ndimage
E = np.load(sys.argv[1])['e'].astype(float); T, C, H, W = E.shape
def cents(f):
    lab, n = ndimage.label(f > 0.4)
    if n == 0: return np.zeros((0, 2)), np.zeros(0)
    c = np.array(ndimage.center_of_mass(f > 0.4, lab, range(1, n + 1))); a = np.bincount(lab.ravel())[1:]
    k = a >= 8
    return c[k], a[k]
for ch, name in ((0, 'e1'), (1, 'e2')):
    tracks = []  # list of lists of positions (unwrapped)
    c0, a0 = cents(E[0][ch]); cur = [[p.copy()] for p in c0]; area = [[a] for a in a0]; alive = [True] * len(cur)
    for t in range(1, T):
        c1, a1 = cents(E[t][ch])
        for k, tr in enumerate(cur):
            if not alive[k] or len(c1) == 0: alive[k] = False; continue
            last = tr[-1]
            d = (c1 - last + np.array([H / 2, W / 2])) % np.array([H, W]) - np.array([H / 2, W / 2])
            j = np.argmin((d ** 2).sum(1))
            if np.sqrt((d[j] ** 2).sum()) > 4 or abs(a1[j] - area[k][-1]) > 0.5 * area[k][-1]: alive[k] = False; continue
            tr.append(last + d[j]); area[k].append(a1[j])
    res = []
    for k, tr in enumerate(cur):
        if alive[k] and len(tr) == T:
            tr = np.array(tr); D = 2 * np.sqrt(np.mean(area[k]) / np.pi)
            net = np.sqrt(((tr[-1] - tr[0]) ** 2).sum()); path = np.sqrt((np.diff(tr, axis=0) ** 2).sum(1)).sum()
            res.append((net / D, path / D, D))
    res = np.array(res)
    if len(res):
        print(name, 'tracks alive whole window', len(res), 'of', len(c0), '| net/D median %.2f max %.2f | path/D median %.2f | D median %.1f' % (np.median(res[:, 0]), res[:, 0].max(), np.median(res[:, 1]), np.median(res[:, 2])))
    else:
        print(name, 'no full tracks of', len(c0))
