import sys, os, importlib.util, numpy as np
from scipy import ndimage
sys.path.insert(0, '/home/user/physim/research/alife')
spec = importlib.util.spec_from_file_location('w', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'world.py')); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
T = float(sys.argv[1]); seed = int(sys.argv[2]); out = sys.argv[3]
s = w.init(seed, (128, 128)); dt = w.P['dt']; n = int(T / dt); every = int(round(T / 6 / dt)); snaps = []
for i in range(n + 1):
    if i % every == 0:
        inc = 1 - np.abs(s['Z']); L, k = ndimage.label(inc > 0.3)
        print(f"t={s['t']:.0f} spots {k} incoh frac {(inc > 0.3).mean():.2f} meanY {s['Y'].mean():.2f}", flush=True)
        snaps.append(np.stack([inc, np.cos(s['phi'])]))
    if i < n: s = w.step(s)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(2, len(snaps), figsize=(2.2 * len(snaps), 4.4))
for j, S in enumerate(snaps):
    ax[0, j].imshow(S[0], vmin=0, vmax=1, cmap='magma'); ax[1, j].imshow(S[1], cmap='twilight'); ax[0, j].set_title(f't={j * every * dt:.0f}', fontsize=8)
    ax[0, j].axis('off'); ax[1, j].axis('off')
plt.tight_layout(); plt.savefig(out, dpi=60)
