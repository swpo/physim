import sys, os, json, numpy as np, importlib.util
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy import ndimage
out, seed, T = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
spec = importlib.util.spec_from_file_location('w', 'world.py'); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, w.META['size']); dt = w.META['dt']; n = int(T/dt); NP = 6; snaps = set(np.linspace(0, n, NP+1).astype(int)[1:]); imgs = []
for i in range(1, n+1):
    s = w.step(s)
    if i in snaps:
        A = s['A'].sum(0); imgs.append((i*dt, np.stack([np.clip(s['S'],0,1), np.clip(A/2,0,1), np.clip(s['phi']/0.2,0,1)], -1)))
US = w.irfft2(w.rfft2(s['A'].sum(0)) * s['KS'], s['A'].shape[1:])
A = s['A'].sum(0); lab, k = ndimage.label(ndimage.gaussian_filter(A, 1) > 0.15)
print(out, 'bodies', k, 'Amax %.2f' % A.max(), 'US max %.3f p50(inside) %.3f' % (US.max(), np.median(US[A > 0.3]) if (A > 0.3).any() else 0), 'S mean %.3f' % s['S'].mean(), 'S>0.5 frac %.3f' % (s['S'] > 0.5).mean())
fig, ax = plt.subplots(1, NP, figsize=(3*NP, 3.3))
for a, (t, im) in zip(ax, imgs): a.imshow(im); a.set_title(f't={t:.0f}'); a.axis('off')
fig.suptitle(os.environ.get('WORLD_P', '') + f' seed{seed}  R=S shell G=A body B=food', fontsize=8); plt.tight_layout(); plt.savefig(out + '.png', dpi=70)
