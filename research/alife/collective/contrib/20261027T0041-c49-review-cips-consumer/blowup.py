"""python blowup.py world.py seed T : steps the world (WORLD_P honoured) and prints the first time a field is non-finite."""
import sys, importlib.util, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
spec = importlib.util.spec_from_file_location('w', sys.argv[1]); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, T = int(sys.argv[2]), float(sys.argv[3]); s = w.init(seed, (128, 128)); dt = w.P['dt']; bad = None
for i in range(int(T / dt)):
    s = w.step(s)
    if not (np.isfinite(s['q']).all() and np.isfinite(s['pa']).all()): bad = (i + 1) * dt; break
print('seed', seed, 'dt', dt, 'first non-finite t =', bad, 'q max', float(np.nanmax(s['q'])))
