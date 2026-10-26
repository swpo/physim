import sys, importlib.util, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(int(sys.argv[1]), None)
for t in range(int(sys.argv[2])): s = w.step(s)
p = w.particles(s); cols = np.array(["green", "brown", "blue", "gold"])
# magenta: > 15 neighbours within 1.3
from scipy.spatial import cKDTree
tr = cKDTree(np.c_[p[:, 0], p[:, 1]], boxsize=w.P["L"]); nn = np.array([len(q) - 1 for q in tr.query_ball_point(np.c_[p[:, 0], p[:, 1]], 1.3)])
c = cols[p[:, 2].astype(int)].astype(object); c[nn > 15] = "magenta"
fig, ax = plt.subplots(figsize=(10, 10)); ax.scatter(p[:, 0], p[:, 1], s=2, c=list(c)); ax.set_aspect("equal")
ax.set_title(f"PPS seed {sys.argv[1]} t={sys.argv[2]} (green N<13, brown 13-15, blue 16-35, gold >35, magenta >15 within 1.3)")
fig.savefig(sys.argv[3], dpi=70); print("magenta", (nn > 15).sum())
