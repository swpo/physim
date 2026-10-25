"""food paid per unit matter per t (world's own ledger counter) over 50 t from pre<seed>_ckpt.npz"""
import numpy as np, importlib.util, json, sys
spec = importlib.util.spec_from_file_location('w', 'world.py'); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
res = {}
for sd in map(int, sys.argv[1:]):
    s = w.init(sd, w.META['size']); c = np.load(f'pre{sd}_ckpt.npz'); s['A'] = c['A'].copy(); s['F'] = c['F'].copy(); s['W'] = c['W'].copy()
    s['N0'] = s['A'].sum()/2 + s['F'].sum() + s['W'].sum(); s['paid'] = 0.0
    n = 500; dt = w.META['dt']; M = 0.0
    for i in range(n):
        M += s['A'].sum(); s = w.step(s)
    M /= n; rate = s['paid'] * w.P['Y'] / (n * dt) / M
    res[sd] = {"mean_matter": round(M, 1), "matter_built_per_matter_per_t": round(rate, 4), "imposed_decay": w.P["decay"], "turnover_time_t": round(1/rate, 1)}
print(json.dumps(res)); json.dump(res, open('turnover.json', 'w'), indent=1)
