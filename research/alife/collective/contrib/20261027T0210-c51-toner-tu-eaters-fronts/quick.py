import sys, json, os, importlib.util, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
spec = importlib.util.spec_from_file_location('w', sys.argv[1]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
T = float(sys.argv[2]); out = sys.argv[3]; nshow = 8
s = W.init(int(os.environ.get('SEED', 0)), W.META['size']); dt = W.P['dt']; n = int(T / dt)
snaps = []
for i in range(n + 1):
    if i % (n // (nshow - 1)) == 0: snaps.append((s['t'], W.fields(s).copy()))
    s = W.step(s)
    if not np.isfinite(s['rho']).all(): print('blowup at', s['t']); break
fig, ax = plt.subplots(2, len(snaps), figsize=(2.2 * len(snaps), 4.6))
for j, (t, f) in enumerate(snaps):
    ax[0, j].imshow(f[0], cmap='magma', vmin=0, vmax=1); ax[0, j].set_title(f't={t:.0f} max {f[0].max():.2f}', fontsize=7)
    ax[1, j].imshow(f[1], cmap='viridis', vmin=0, vmax=1); ax[1, j].set_title(f'food; |p| max {f[2].max():.2f}', fontsize=7)
for a in ax.flat: a.axis('off')
plt.tight_layout(); plt.savefig(out, dpi=70)
print('final rho mean %.3f max %.3f, c mean %.3f' % (snaps[-1][1][0].mean(), snaps[-1][1][0].max(), snaps[-1][1][1].mean()))
