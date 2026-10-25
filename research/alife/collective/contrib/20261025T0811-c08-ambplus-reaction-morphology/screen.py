"""screen.py WORLD OUT.png T NFR 'json' [seed] : run, montage, component counts."""
import os, sys, json, time
os.environ['WORLD_P'] = sys.argv[5]
import importlib.util, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
spec = importlib.util.spec_from_file_location('w', sys.argv[1]); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
T = float(sys.argv[3]); nf = int(sys.argv[4]); seed = int(sys.argv[6]) if len(sys.argv) > 6 else 0
size = tuple(json.loads(os.environ.get('SIZE', '[128,128]')))
s = w.init(seed, size); dt = w.P['dt']; n = int(round(T / dt)); every = max(1, n // nf)
frames, times, info = [], [], []
t0 = time.time()
for i in range(n + 1):
    if i % every == 0:
        f = w.fields(s)
        if not np.isfinite(f).all(): print('NAN at', i * dt); break
        frames.append(f.copy()); times.append(i * dt)
        lab, nc = ndimage.label(f[0] > 0)
        areas = np.bincount(lab.ravel())[1:]
        info.append((i * dt, nc, float(np.median(areas)) if nc else 0, float(f[0].mean())))
        print(f"t={i*dt:.0f} n={nc} medA={info[-1][2]:.0f} mean={info[-1][3]:.3f} max={f[0].max():.2f}", flush=True)
    if i < n: s = w.step(s)
C = frames[0].shape[0]
fig, ax = plt.subplots(C, len(frames), figsize=(1.6 * len(frames), 1.7 * C), squeeze=False)
for j, (f, t) in enumerate(zip(frames, times)):
    for c in range(C):
        a = ax[c, j]; a.imshow(f[c], cmap='magma' if c == 0 else 'viridis', vmin=(-1.2 if c == 0 else None), vmax=(1.6 if c == 0 else None)); a.set_xticks([]); a.set_yticks([])
        if c == 0: a.set_title(f"t={t:.0f} n={info[j][1]}", fontsize=7)
fig.suptitle(sys.argv[5], fontsize=7); fig.tight_layout(); fig.savefig(sys.argv[2], dpi=80)
np.save(sys.argv[2].replace(".png", "_final.npy"), frames[-1]); json.dump(info, open(sys.argv[2].replace(".png", "_info.json"), "w")); print("wall", time.time() - t0)
