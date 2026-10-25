import sys, os, json, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit.world import load_world
W = load_world(sys.argv[1]); T = float(sys.argv[2]); out = sys.argv[3]; N = int(sys.argv[4]); seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0
s = W.init(seed, (N, N)); dt = s['par']['dt']; n = int(T / dt); every = int(10 / dt)
fr = []
for i in range(n):
    s = W.step(s)
    if (i + 1) % every == 0 and s['t'] >= T - 1000:
        fr.append(np.stack([s['e1'], s['e2']]).astype(np.float16))
np.savez_compressed(out, e=np.array(fr), t0=T - 1000)
