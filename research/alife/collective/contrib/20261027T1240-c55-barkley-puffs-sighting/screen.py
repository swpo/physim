import sys, os, importlib.util, numpy as np
from scipy import ndimage
sys.path.insert(0, '/home/user/physim/research/alife')
spec = importlib.util.spec_from_file_location('w', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'world.py')); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
T = float(sys.argv[1]); seed = int(sys.argv[2]); out = sys.argv[3]
s = w.init(seed, w.META['size']); dt = w.P['dt']; n = int(T / dt); every = int(round(T / 8 / dt)); snaps = []; line = []
for i in range(n + 1):
    if i % every == 0:
        L, k = ndimage.label(s['q'] > 0.4, structure=np.ones((3, 3)))
        print(f"t={s['t']:.0f} puffs {k} turb frac {(s['q'] > 0.4).mean():.2f} min u {s['u'].min():.2f}", flush=True)
        snaps.append(s['q'].copy())
    if i % int(round(5 / dt)) == 0: line.append(s['q'].mean(0))
    if i < n: s = w.step(s)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(2, 1, figsize=(10, 6), gridspec_kw={'height_ratios': [1, 2]})
ax[0].imshow(np.concatenate([np.concatenate([x, np.full((2, x.shape[1]), np.nan)]) for x in snaps[::2]]), vmin=0, vmax=2, cmap='inferno', aspect='auto'); ax[0].set_title('q snapshots (top to bottom: t = 0, T/4, T/2, 3T/4, T)', fontsize=8)
ax[1].imshow(np.array(line), vmin=0, vmax=1.5, cmap='inferno', aspect='auto', origin='lower'); ax[1].set_xlabel('x (co-moving)'); ax[1].set_ylabel('time / 5'); ax[1].set_title('space-time: q averaged over y', fontsize=8)
plt.tight_layout(); plt.savefig(out, dpi=70)
