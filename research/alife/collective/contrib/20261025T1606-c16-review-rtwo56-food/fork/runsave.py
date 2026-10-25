"""run world, save snapshots every EVERY t (float16) + a full checkpoint at the end. usage: runsave.py world out seed T [ckpt_in]"""
import sys, os, numpy as np, importlib.util
wp, out, seed, T = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
spec = importlib.util.spec_from_file_location('w', wp); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, w.META['size']); dt = w.META['dt']; t0 = 0.0
if len(sys.argv) > 5:
    c = np.load(sys.argv[5]); s['A'] = c['A'].copy(); s['F'] = c['F'].copy(); s['W'] = c['W'].copy(); t0 = float(c['t'])
    if os.environ.get('STARVE_ALL'):
        s['F'][:] = 0; s['W'][:] = 0          # abrupt removal of all food and waste at the fork
    s['N0'] = s['A'].sum()/w.P['Y'] + s['F'].sum() + s['W'].sum()
    if 'mask' in c.files and os.environ.get('CUT'):
        s['_mask'] = c['mask']; w.P['starve_disk'] = 1
every = float(os.environ.get('EVERY', '5')); k = int(round(every/dt))
snaps = []; ts = []
for i in range(1, int(T/dt)+1):
    s = w.step(s)
    if i % k == 0:
        snaps.append(np.concatenate([s['A'], s['F'][None]]).astype(np.float16)); ts.append(t0 + i*dt)
np.savez_compressed(out + '_snaps.npz', X=np.array(snaps), t=np.array(ts))
np.savez_compressed(out + '_ckpt.npz', A=s['A'], F=s['F'], W=s['W'], t=t0 + T)
print(out, 'done t=', t0+T)
