"""Periodic centroid path of each body between merge/split events, in its own body lengths.
usage: python path.py frames.npz [dt_per_frame]"""
import sys, numpy as np
from scipy import ndimage as ndi
z = np.load(sys.argv[1]); keys = list(z.keys())
F = z[[k for k in keys if z[k].ndim >= 3][0]]
phi = F[:, 0] if F.ndim == 4 else F
dtf = float(sys.argv[2]) if len(sys.argv) > 2 else 0.2
T, H, W = phi.shape
def comps(m):
    lab, n = ndi.label(m)
    # periodic merge
    for a, b in [(lab[0], lab[-1]), (lab[:, 0], lab[:, -1])]:
        for i, j in zip(a, b):
            if i and j and i != j: lab[lab == j] = i
    out = []
    for l in np.unique(lab)[1:]:
        ys, xs = np.nonzero(lab == l)
        if len(ys) < 50: continue
        cy = np.angle(np.exp(2j*np.pi*ys/H).mean())*H/(2*np.pi) % H
        cx = np.angle(np.exp(2j*np.pi*xs/W).mean())*W/(2*np.pi) % W
        out.append(dict(mask=(lab == l), c=np.array([cy, cx]), a=len(ys)))
    return out
prev = None; segs = []; active = {}
nid = 0
for t in range(T):
    cs = comps(phi[t] > 0.5)
    new = {}
    for c in cs:
        ov = [k for k, p in (prev or {}).items() if (p['mask'] & c['mask']).sum() > 0]
        if len(ov) == 1 and sum((prev[ov[0]]['mask'] & d['mask']).sum() > 0 for d in cs) == 1:
            k = ov[0]; p = prev[k]
            d = (c['c'] - p['c'] + np.array([H, W])/2) % np.array([H, W]) - np.array([H, W])/2
            c['path'] = p['path'] + [p['path'][-1] + d]; c['t0'] = p['t0']; c['areas'] = p['areas'] + [c['a']]
            new[k] = c
        else:
            if ov:  # merge/split ends old segments
                pass
            c['path'] = [np.zeros(2)]; c['t0'] = t; c['areas'] = [c['a']]; new[nid] = c; nid += 1
    for k, p in (prev or {}).items():
        if k not in new: segs.append(p)
    prev = new
segs += list(prev.values())
rows = []
for s in segs:
    P = np.array(s['path']); n = len(P)
    if n < 5: continue
    BL = 2*np.sqrt(np.mean(s['areas'])/np.pi)
    net = np.linalg.norm(P[-1]-P[0]); arc = np.sum(np.linalg.norm(np.diff(P, axis=0), axis=1))
    rows.append((net/BL, arc/BL, s['t0']*dtf, (s['t0']+n-1)*dtf, BL, max(s['areas'])/min(s['areas'])))
rows.sort(reverse=True)
print("net_BL  path_BL  t_start  t_end  bodylen_px  amax/amin")
for r in rows[:8]: print("%.2f  %.2f  %.1f  %.1f  %.0f  %.2f" % r)
