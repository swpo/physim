"""c52: run world2m.py, record total predator material of each kind (unclipped) and body counts every 100 t.
usage: mdrive.py out seed T  (WORLD_P from env)"""
import sys, os, json, importlib.util, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from scipy import ndimage
out, seed, T = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
spec = importlib.util.spec_from_file_location('w', os.environ.get('WFILE', 'world2m.py')); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, (128, 128)); dt = w.P['dt']; ev = int(round(100 / dt)); rows = []
def nb(x):
    L, n = ndimage.label(x > 0.5); a = np.bincount(L.ravel())[1:]; return int((a >= 4).sum())
for i in range(int(T / dt) + 1):
    if i % ev == 0:
        cb, ce = (s["pb"] + 1) / 2, (s["pe"] + 1) / 2
        F = w.fields(s)
        rows.append([i * dt, float(cb.mean()), float(ce.mean()), nb(F[0]), nb(F[1]), nb(F[5]),
                     float(cb[cb > 0.5].sum() / cb.sum()), float(ce[ce > 0.5].sum() / max(ce.sum(), 1e-9))])
    if i * dt < T: s = w.step(s)
json.dump({"cols": ["t", "mean_cb", "mean_ce", "n_prey", "n_b", "n_e", "condensed_frac_b", "condensed_frac_e"], "rows": rows, "P": w.P}, open(out + '.json', 'w'))
R = np.array(rows); print(out, 'e/b total at end %.3f' % (R[-1, 2] / R[-1, 1]), 'bodies', R[-1, 3:6], 'cond frac', R[-1, 6:].round(2))
