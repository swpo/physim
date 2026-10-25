"""Population mean heritable rate y vs inert marker z (particle means) and rod count, every T/20 steps."""
import sys, json, time, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit.world import load_world
from scipy import ndimage
W = load_world(sys.argv[1]); W.P.update(json.loads(sys.argv[2])); T = int(sys.argv[3]); seed = int(sys.argv[4])
s = W.init(seed, (128, 128)); t0 = time.time()
for t in range(1, T + 1):
    W.step(s)
    if t % (T // 20) == 0:
        lab, n = ndimage.label(s["phi"] > 0)
        H, Wd = s["phi"].shape
        inr = lab[s["py"].astype(int) % H, s["px"].astype(int) % Wd] > 0
        print(f"step={t} rods={n} N={len(s['py'])} in_rods={inr.mean():.2f} y={s['y'][inr].mean():.4f} z={s['z'][inr].mean():.4f} ({time.time()-t0:.0f}s)", flush=True)
