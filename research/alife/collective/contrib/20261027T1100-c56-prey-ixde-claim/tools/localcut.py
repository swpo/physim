"""c56: per-individual fuel cut.  python localcut.py cut_frames.npz fed_frames.npz cy cx r out.png [t0_frame]
Follows the prey body (c_a > 0.5) that covers (cy, cx) at frame t0 by largest overlap in both runs, and counts the other
prey bodies (area >= 4) whose centre lies > r + 15 px from the cut centre. Draws the area time course and crops."""
import sys, json, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
C = np.load(sys.argv[1])['render'].astype(np.float32); Fd = np.load(sys.argv[2])['render'].astype(np.float32)
cy, cx, r = int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]); t0 = int(sys.argv[7]) if len(sys.argv) > 7 else 60
H, W = C.shape[-2:]
yy, xx = np.mgrid[0:H, 0:W]
far = (((yy - cy + H / 2) % H - H / 2) ** 2 + ((xx - cx + W / 2) % W - W / 2) ** 2) > (r + 15) ** 2


def follow(R):
    out = []; L = ndimage.label(R[t0][0] > 0.5)[0]; i = L[cy, cx]
    m = (L == i) if i else None
    for t in range(t0, len(R)):
        L = ndimage.label(R[t][0] > 0.5)[0]
        if m is not None and t > t0:
            ov = L[m]; ov = ov[ov > 0]
            m = (L == np.bincount(ov).argmax()) if ov.size else None
        a = int(m.sum()) if m is not None else 0
        lab, n = ndimage.label(R[t][0] > 0.5); ar = np.bincount(lab.ravel())
        com = ndimage.center_of_mass(np.ones_like(lab), lab, range(1, n + 1)) if n else []
        others = sum(1 for k, (y, x) in enumerate(com) if ar[k + 1] >= 4 and far[int(y) % H, int(x) % W])
        out.append((t, a, others))
    return out


fc, ff = follow(C), follow(Fd)
res = dict(cut=fc, fed=ff)
print(json.dumps(dict(cut_area=[a for _, a, _ in fc][::2], fed_area=[a for _, a, _ in ff][::2],
                      cut_others=[o for _, _, o in fc][::4], fed_others=[o for _, _, o in ff][::4])))
fig = plt.figure(figsize=(11, 4.5)); ax = fig.add_subplot(1, 2, 1)
ax.plot([t * 100 for t, _, _ in fc], [a for _, a, _ in fc], 'r', label='cut: the prey body at the centre')
ax.plot([t * 100 for t, _, _ in ff], [a for _, a, _ in ff], 'k', label='fed twin: same body')
ax.set_xlabel('t'); ax.set_ylabel('area (px)'); ax.legend(fontsize=8)
ax2 = ax.twinx(); ax2.plot([t * 100 for t, _, _ in fc], [o for _, _, o in fc], 'r:'); ax2.plot([t * 100 for t, _, _ in ff], [o for _, _, o in ff], 'k:')
ax2.set_ylabel('prey bodies away from the cut (dotted)')
for k, dt in enumerate((0, 2, 5, 10)):
    for row, R in enumerate((C, Fd)):
        a = fig.add_subplot(2, 8, 5 + k + 8 * row); f = R[min(len(R) - 1, t0 + dt)]
        ys = np.arange(cy - 24, cy + 24) % H; xs = np.arange(cx - 24, cx + 24) % W
        a.imshow(np.stack([np.clip(f[1], 0, 1), np.clip(f[0], 0, 1), 0.4 * np.clip(f[2], 0, 1)], -1)[np.ix_(ys, xs)])
        a.add_patch(plt.Circle((24, 24), r, fill=False, color='w', lw=0.6)); a.set_xticks([]); a.set_yticks([])
        a.set_title(f"{'cut' if row == 0 else 'fed'} t={(t0 + dt) * 100}", fontsize=7)
plt.tight_layout(); plt.savefig(sys.argv[6], dpi=80)
