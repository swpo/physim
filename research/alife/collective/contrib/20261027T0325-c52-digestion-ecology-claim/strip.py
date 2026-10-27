import sys, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
d = np.load(sys.argv[1]); R = d['render'] if 'render' in d else d[d.files[0]]
f0, f1, step = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]); y0, x0, L = [int(v) for v in sys.argv[6:9]]
fr = list(range(f0, f1, step)); fig, axs = plt.subplots(2, len(fr), figsize=(1.3*len(fr), 2.8))
for k, f in enumerate(fr):
    F = R[f]; a = np.roll(np.roll(F, -y0, -2), -x0, -1)[:, :L, :L]
    rgb = np.zeros((L, L, 3)); rgb[..., 0] = np.clip(a[1], 0, 1); rgb[..., 1] = np.clip(a[0], 0, 1)
    axs[0, k].imshow(rgb); axs[0, k].set_title(f'f{f}', fontsize=6); axs[0, k].axis('off')
    axs[1, k].imshow(a[4] if a.shape[0] > 4 else a[2], cmap='magma'); axs[1, k].axis('off')
plt.tight_layout(); plt.savefig(sys.argv[2], dpi=80)
