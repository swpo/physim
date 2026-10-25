import sys, os, numpy as np, importlib.util
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy import ndimage
out, seed, T = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
spec = importlib.util.spec_from_file_location('w', 'world.py'); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, w.META['size']); dt = w.META['dt']; n = int(T/dt); NP = 8; snaps = set(np.linspace(0, n, NP+1).astype(int)[1:]); imgs = []; M0 = s['A'].sum()
for i in range(1, n+1):
    s = w.step(s)
    if i in snaps:
        A = s['A'].sum(0); k = ndimage.label(ndimage.gaussian_filter(A, 1) > 0.15)[1]
        imgs.append((i*dt, k, np.stack([np.zeros_like(A), np.clip(A/2, 0, 1), np.clip(s['phi'], 0, 1)], -1)))
print(out, 'bodies', [x[1] for x in imgs], 'matter drift %.2e' % (s['A'].sum()/M0 - 1), 'phi mean %.2f min %.2f' % (s['phi'].mean(), s['phi'].min()))
fig, ax = plt.subplots(1, NP, figsize=(2.6*NP, 2.9))
for a, (t, k, im) in zip(ax, imgs): a.imshow(im); a.set_title(f't={t:.0f} n={k}', fontsize=8); a.axis('off')
fig.suptitle(os.environ.get('WORLD_P', '') + f' seed{seed} G=matter B=food', fontsize=8); plt.tight_layout(); plt.savefig(out + '.png', dpi=65)
