import sys, copy, json, numpy as np, importlib.util
from scipy import ndimage
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
seed = int(sys.argv[1]); spec = importlib.util.spec_from_file_location('w', 'world.py'); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
dt = w.META['dt']; s = w.init(seed, w.META['size'])
for i in range(int(200/dt)): s = w.step(s)
res = {}; fig, ax = plt.subplots(2, 5, figsize=(13, 5.4))
for r, arm in enumerate(('fed', 'starved')):
    st = copy.deepcopy(s); cfg = dict(w.CFG)
    if arm == 'starved': st['phi'][:] = 0; w.CFG['rho_f'] = 0.0
    rec = []
    for i in range(1, int(300/dt)+1):
        st = w.step(st)
        if i % int(25/dt) == 0:
            A = st['A'].sum(0); k = ndimage.label(ndimage.gaussian_filter(A, 1) > 0.15)[1]; rec.append((200 + i*dt, k, float(A.max())))
        if i % int(75/dt) == 0 and i // int(75/dt) <= 4:
            j = i // int(75/dt); A = st['A'].sum(0); ax[r, j].imshow(np.stack([np.zeros_like(A), np.clip(A/2, 0, 1), np.clip(st['phi'], 0, 1)], -1)); ax[r, j].set_title(f'{arm} t={200+i*dt:.0f}', fontsize=8); ax[r, j].axis('off')
    w.CFG.update(cfg); res[arm] = rec
    A = s['A'].sum(0); ax[r, 0].imshow(np.stack([np.zeros_like(A), np.clip(A/2, 0, 1), np.clip(s['phi'], 0, 1)], -1)); ax[r, 0].set_title(f'fork t=200', fontsize=8); ax[r, 0].axis('off')
plt.tight_layout(); plt.savefig(f'dfork{__import__("os").environ.get("TAG","")}_s{seed}.png', dpi=65)
print(json.dumps({a: [(int(t), k, round(m, 2)) for t, k, m in v] for a, v in res.items()}))
