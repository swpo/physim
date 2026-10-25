import sys, json, time, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit.world import load_world
from scipy import ndimage
W = load_world(sys.argv[1]); W.P.update(json.loads(sys.argv[2])); T = int(sys.argv[3]); seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
s = W.init(seed, (128, 128)); t0 = time.time()
for t in range(1, T + 1):
    W.step(s)
    if t % (T // 10) == 0:
        lab, n = ndimage.label(s["phi"] > 0); ar = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1)) if n else [0]
        print(f"step={t} drops={n} medarea={np.median(ar):.0f} occ={(s['phi']>0).mean():.3f} N={len(s['py'])} vmax={np.hypot(s['vx'],s['vy']).max():.3f} ({time.time()-t0:.0f}s)", flush=True)
