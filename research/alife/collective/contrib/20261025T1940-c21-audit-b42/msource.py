"""(c21) Where is the wall material M made? Runs pcell-mwall-b42 and, every 1000 steps after t=10000, splits
the production bm K S into pixels inside cells (phi > 0.5), the rim band (0.05 < phi <= 0.5) and the bath
(phi <= 0.05), and reports the fraction of catalyst particles outside cells. usage: msource.py world.py seed T"""
import sys, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit.world import load_world
W = load_world(sys.argv[1]); seed, T = int(sys.argv[2]), int(sys.argv[3])
s = W.init(seed, (128, 128)); acc = np.zeros(3); pout = []
for t in range(T + 1):
    if t >= 10000 and t % 1000 == 0:
        prod = W.P["bm"] * s["K"] * s["S"]; phi = s["phi"]
        acc += [prod[phi > 0.5].sum(), prod[(phi > 0.05) & (phi <= 0.5)].sum(), prod[phi <= 0.05].sum()]
        H, Wd = phi.shape; ph = phi[s["py"].astype(int) % H, s["px"].astype(int) % Wd]; pout.append(float((ph <= 0.05).mean()))
    s = W.step(s)
f = acc / acc.sum()
print("seed %d T %d: M production inside cells %.3f, rim band %.3f, bath %.3f; particles in bath (phi<=0.05) mean %.4f" % (seed, T, f[0], f[1], f[2], np.mean(pout)))
