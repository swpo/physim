"""c57: quick screen driver: python screen.py out.png T nframes '{json params}' [seed] [size]"""
import sys, os, json, importlib.util, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
out, T, nf, pj = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0; N = int(sys.argv[6]) if len(sys.argv) > 6 else 128
os.environ["WORLD_P"] = pj
spec = importlib.util.spec_from_file_location('w', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'world.py'))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, (N, N)); dt = w.P["dt"]; nsteps = int(T / dt); every = nsteps // nf
fr, log = [], []
for i in range(nsteps + 1):
    if i % every == 0:
        h = s["h"] - w.P["ha"]
        if not np.isfinite(h).all(): log.append(f"t={s['t']:.0f} NaN"); break
        L, n = ndimage.label(h > 0.5); a = np.bincount(L.ravel())[1:]
        log.append(f"t={s['t']:.0f} n={(a>=6).sum()} hmax={h.max():.2f} mass={h.mean():.3f} V={s['V'].mean():.3f} amed={np.median(a) if len(a) else 0:.0f}")
        fr.append((s['t'], h.copy()))
    s = w.step(s)
print("\n".join(log))
k = len(fr); fig, ax = plt.subplots(1, k, figsize=(2 * k, 2.2))
vmax = max(1.0, max(f[1].max() for f in fr))
for a_, (t, h) in zip(ax, fr):
    a_.imshow(h, vmin=0, vmax=vmax, cmap='magma'); a_.set_title(f"t={t:.0f}", fontsize=8); a_.axis('off')
plt.suptitle(pj, fontsize=7); plt.tight_layout(); plt.savefig(out, dpi=70)
