import sys, json, os, importlib.util, numpy as np
from scipy import ndimage
sys.path.insert(0, '/home/user/physim/research/alife')
spec = importlib.util.spec_from_file_location('w', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'world.py')); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
T = float(sys.argv[1]); seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
s = w.init(seed, (128, 128)); dt = w.P['dt']; n = int(T / dt); every = int(round(float(os.environ.get('EVERY', 50)) / dt))
snaps = []
for i in range(n + 1):
    if i % every == 0:
        r = np.abs(s['psi']) ** 2; L, k = ndimage.label(r > 4 * r.mean()); sz = ndimage.sum(r, L, range(1, k + 1)) if k else []
        print(f"t={s['t']:.0f} clumps(>4x mean) {k} max rho {r.max():.1f} mass {r.sum():.0f} top masses {sorted(np.round(sz).astype(int))[-4:] if k else []} meanY {s['Y'].mean():.2f}", flush=True)
        snaps.append(np.log10(r + 1e-3).astype(np.float32))
    if i < n: s = w.step(s)
np.save(os.environ.get('OUT', 'snaps.npy'), np.stack(snaps))
