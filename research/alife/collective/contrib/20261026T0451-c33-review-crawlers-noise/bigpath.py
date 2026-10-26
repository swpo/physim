"""bigpath.py frames.npz: follow the largest body (matter > 0.5, periodic) frame to frame by maximum overlap and
report its unwrapped centroid path in body lengths (sqrt of its mean area) between t0 and the end."""
import sys, numpy as np
from scipy import ndimage
d = np.load(sys.argv[1]); M = d["matter"]; T, H, W = M.shape; dtf = 16.0 / (T - 1)
def lab(m):
    l, n = ndimage.label(m)
    for a, b in ((l[0], l[-1]), (l[:, 0], l[:, -1])):
        for u, v in set(zip(a.tolist(), b.tolist())):
            if u and v and u != v: l[l == v] = u
    return l
def cen(mask):
    ys, xs = np.nonzero(mask)
    return np.array([np.angle(np.exp(2j*np.pi*ys/H).mean())*H/(2*np.pi), np.angle(np.exp(2j*np.pi*xs/W).mean())*W/(2*np.pi)])
t0 = int(sys.argv[2]) if len(sys.argv) > 2 else T // 2
l = lab(M[t0] > 0.5 * M.max()); sizes = np.bincount(l.ravel()); sizes[0] = 0; cur = l == sizes.argmax()
path = [cen(cur)]; areas = [cur.sum()]
for f in range(t0 + 1, T):
    l = lab(M[f] > 0.5 * M.max()); ov = np.bincount(l[cur], minlength=l.max() + 1); ov[0] = 0
    if ov.max() == 0: break
    cur = l == ov.argmax(); path.append(cen(cur)); areas.append(cur.sum())
p = np.array(path); dp = (np.diff(p, axis=0) + [H/2, W/2]) % [H, W] - [H/2, W/2]; net = np.hypot(*dp.sum(0)); BL = np.sqrt(np.mean(areas))
print(f"largest body from frame {t0} (t={t0*dtf:.1f}) for {len(p)} frames: net {net:.0f} px = {net/BL:.1f} body lengths (sqrt area {BL:.0f} px), area {areas[0]} -> {areas[-1]}")
