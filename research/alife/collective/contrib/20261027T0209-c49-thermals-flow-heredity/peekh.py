import sys, os, numpy as np, importlib.util
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.path.insert(0, '/home/user/physim/research/alife')
spec = importlib.util.spec_from_file_location('w', 'world.py'); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
T = float(sys.argv[2]); s = w.init(int(sys.argv[3]) if len(sys.argv) > 3 else 0, (128, 128)); dt = w.P['dt']; n = int(T / dt)
snaps = set(np.linspace(0, n, 10).astype(int)); out = []
for i in range(n + 1):
    if i in snaps: out.append((i * dt, s['T'].copy(), s['a'].copy(), s['b'].copy()))
    if i < n: s = w.step(s)
fig, ax = plt.subplots(1, 10, figsize=(25, 2.8))
for j, (t, Tf, a, b) in enumerate(out):
    rgb = np.stack([np.clip(a, 0, 1), np.clip(Tf / 0.7, 0, 1) * 0.6, np.clip(b, 0, 1)], -1)
    ax[j].imshow(rgb, origin='lower'); ax[j].set_title(f't={t:.0f}', fontsize=8); ax[j].axis('off')
plt.tight_layout(); plt.savefig(sys.argv[1], dpi=60)
