"""cut vs fed twin: matter inside the cut disk and in the neighbour annulus; crops centred on the cut cog. usage: cutplot.py out.png seeds..."""
import sys, json, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
out = sys.argv[1]; seeds = list(map(int, sys.argv[2:]))
H = W = 192; yy, xx = np.mgrid[:H, :W]
fig, ax = plt.subplots(len(seeds), 6, figsize=(19, 3.2*len(seeds)), squeeze=False); res = {}
for r, sd in enumerate(seeds):
    c = np.load(f'cut_{sd}.npz'); m = c['mask']; cy, cx, rad = float(c['cy']), float(c['cx']), float(c['rad'])
    dy = np.minimum(abs(yy-cy), H-abs(yy-cy)); dx = np.minimum(abs(xx-cx), W-abs(xx-cx)); d = np.hypot(dy, dx)
    ann = d >= rad + 5   # every other body (all matter outside the disk)
    Xc = np.load(f'cutrun{sd}_snaps.npz'); t = Xc['t']; Xc = Xc['X'].astype(np.float32)
    Xf = np.load(f'fed{sd}_snaps.npz')['X'].astype(np.float32)[:len(Xc)]
    A0 = c['A'][:, m].sum(); An = c['A'][:, ann].sum()
    ic = Xc[:, :2][:, :, m].sum((1, 2))/A0; iff = Xf[:, :2][:, :, m].sum((1, 2))/A0
    nc = Xc[:, :2][:, :, ann].sum((1, 2))/An; nf = Xf[:, :2][:, :, ann].sum((1, 2))/An
    sh = (int(H//2-cy), int(W//2-cx)); s0 = 96-int(rad)-35; s1 = 96+int(rad)+35
    for j, (X, i, lab) in enumerate([(Xc, 0, 'cut'), (Xc, 8, 'cut'), (Xc, len(t)-1, 'cut'), (Xf, 8, 'fed twin'), (Xf, len(t)-1, 'fed twin')]):
        Y = np.roll(X[i], sh, (1, 2))
        im = np.stack([Y[1], Y[0], np.clip(Y[2]/1.5, 0, 1)], -1).clip(0, 1)[s0:s1, s0:s1]
        ax[r, j].imshow(im); ax[r, j].add_patch(plt.Circle((96-s0, 96-s0), rad, fill=False, color='w', ls='--'))
        ax[r, j].set_title(f'seed{sd} {lab} t={t[i]:.0f}', fontsize=8); ax[r, j].axis('off')
    a = ax[r, 5]; a.plot(t, ic, 'r', label='cut cog (inside disk)'); a.plot(t, iff, 'r--', label='same cog, fed twin')
    a.plot(t, nc, 'b', label='all other bodies, cut run'); a.plot(t, nf, 'b--', label='all other bodies, fed twin'); a.set_ylim(0, 1.5); a.legend(fontsize=6); a.set_xlabel('t')
    below = t[np.argmax(ic < 0.1)] if (ic < 0.1).any() else None
    res[sd] = {"cut_inside_end": round(float(ic[-1]), 3), "fed_inside_end": round(float(iff[-1]), 3), "cut_neighbours_end": round(float(nc[-1]), 3),
               "fed_neighbours_end": round(float(nf[-1]), 3), "t_inside_below_0.1": None if below is None else float(below), "nearest_other_core_px": round(float(c['dmin']), 1)}
plt.tight_layout(); plt.savefig(out, dpi=65); print(json.dumps(res, indent=1)); json.dump(res, open(out[:-4]+'.json', 'w'), indent=1)
