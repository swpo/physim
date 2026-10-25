"""render snapshot npz: panels + body/mass timeseries. usage: render.py out.png snaps1.npz [snaps2.npz ...] (each a row)"""
import sys, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy import ndimage
out = sys.argv[1]; files = sys.argv[2:]; NP = 6
fig, ax = plt.subplots(len(files), NP+1, figsize=(3*(NP+1), 3.1*len(files)), squeeze=False)
for r, f in enumerate(files):
    d = np.load(f); X = d['X'].astype(np.float32); t = d['t']
    idx = np.linspace(0, len(t)-1, NP).astype(int)
    for j, i in enumerate(idx):
        im = np.stack([X[i,1], X[i,0], np.clip(X[i,2]/1.5,0,1)], -1).clip(0,1)
        ax[r,j].imshow(im); ax[r,j].set_title(f"{f.split('/')[-1][:-10]} t={t[i]:.0f}", fontsize=8); ax[r,j].axis('off')
    mass = X[:, :2].sum((1,2,3)); nb = [ndimage.label(ndimage.gaussian_filter(x[0]+x[1],1)>0.3)[1] for x in X]
    a = ax[r,NP]; a.plot(t, mass/mass[0], label='matter/matter(t0)'); a.plot(t, X[:,2].mean((1,2)), label='mean F')
    a2 = a.twinx(); a2.plot(t, nb, 'k', lw=0.8, label='bodies'); a2.set_ylabel('bodies')
    a.legend(fontsize=7, loc='upper right'); a.set_xlabel('t')
plt.tight_layout(); plt.savefig(out, dpi=70)
