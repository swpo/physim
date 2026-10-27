"""c56: figure for freepred.py output.  python plotfree.py frames.npz free.json out.png [dt_per_frame]
Top: per-frame gap (px) of every predator body to the nearest prey body, histogram; free-spell lengths and fates;
parent gap at every predator division. Bottom: one detach event (prey green, predator red), frames around it."""
import sys, json, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
R = np.load(sys.argv[1])['render'].astype(np.float32); J = json.load(open(sys.argv[2]))
DTF = float(sys.argv[4]) if len(sys.argv) > 4 else 100.0
H, W = R.shape[-2:]
# recompute gaps for histogram (sampled frames)
gaps = []
for t in range(J['frames_from'], len(R), 5):
    pa = R[t][0] > 0.5; l, n = ndimage.label(R[t][1] > 0.5, structure=np.ones((3, 3)))
    if not n: continue
    ar = np.bincount(l.ravel()); l[ar[l] < 4] = 0
    d = ndimage.distance_transform_edt(np.tile(~pa, (3, 3)))[H:2 * H, W:2 * W]
    ids = np.unique(l[l > 0]); gaps += list(ndimage.minimum(d, l, ids))
gaps = np.array(gaps)
fig = plt.figure(figsize=(12, 6.2))
ax = fig.add_subplot(2, 3, 1)
ax.hist(np.clip(gaps, 0, 15), bins=np.arange(0, 16, 1), color='C3')
ax.axvline(2, color='k', ls=':'); ax.set_xlabel('gap to nearest prey body (px; 0 = touching)'); ax.set_ylabel('predator bodies')
ax.set_title(f"{100 * J['free_frac']:.0f}% of predator bodies free (gap > 2 px)", fontsize=9)
ax = fig.add_subplot(2, 3, 2)
f = J['spell_fates']; ax.bar(['dissolved\nwhile free', 'reattached', 'free at end'], [J['free_end_kind'].get('dissolved', 0), f['reattach'], f['alive_at_end']], color=['k', 'C2', 'C0'])
ax.set_title(f"{J['detach_events']} detachments; spell median {J['spell_frames_median'] * DTF:.0f} t, max {J['spell_frames_max'] * DTF:.0f} t;\n"
             f"{J['hops']} moves to another prey > 10 px away", fontsize=8)
ax = fig.add_subplot(2, 3, 3)
dl = J['div_list']; ax.hist([d['parent_gap'] for d in dl], bins=np.arange(0, 8, 0.5), color='C3', label='parent at t')
ax.hist([max(d['kid_gap5']) for d in dl], bins=np.arange(0, 8, 0.5), histtype='step', color='k', label='farther daughter, t+500')
ax.axvline(2, color='k', ls=':'); ax.legend(fontsize=7); ax.set_xlabel('gap to nearest prey (px)')
ax.set_title(f"{J['divisions']} predator divisions: {J['div_parent_free']} with a free parent", fontsize=9)
# example: a detach -> dissolve event; find a predator that is free and vanishes
ex = None
for t in range(J['frames_from'] + 3, len(R) - 2):
    pa = R[t][0] > 0.5; l, n = ndimage.label(R[t][1] > 0.5, structure=np.ones((3, 3)))
    d = ndimage.distance_transform_edt(np.tile(~pa, (3, 3)))[H:2 * H, W:2 * W]
    for i in range(1, n + 1):
        m = l == i
        if m.sum() < 15 or d[m].min() <= 4: continue
        if not (R[t + 2][1][m] > 0.5).any() and (R[t - 3][0][ndimage.binary_dilation(m, iterations=4)] > 0.5).any():
            ex = (t, *[int(v) for v in ndimage.center_of_mass(m)]); break
    if ex: break
if ex:
    t, cy, cx = ex; h = 20
    for c, dt_ in enumerate((-4, -2, 0, 1, 2, 3)):
        a = fig.add_subplot(2, 6, 7 + c); fr = R[min(len(R) - 1, t + dt_)]
        ys = np.arange(cy - h, cy + h) % H; xs = np.arange(cx - h, cx + h) % W
        rgb = np.stack([np.clip(fr[1], 0, 1), np.clip(fr[0], 0, 1), 0 * fr[0]], -1)[np.ix_(ys, xs)]
        a.imshow(rgb); a.set_xticks([]); a.set_yticks([]); a.set_title(f"t={(t + dt_) * DTF:.0f}", fontsize=8)
    fig.text(0.5, 0.02, 'example: a predator (red) that left its prey (green) dissolves', ha='center', fontsize=9)
plt.tight_layout(rect=(0, 0.04, 1, 1)); plt.savefig(sys.argv[3], dpi=80)
print('example', ex)
