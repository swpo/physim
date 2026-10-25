"""Link ring on swimming cells: for every celltrack track that moves >= 3 body lengths, measure the
L rim/core and rim/outside ratios of that cell at each check of its life, and compare with all
other cells at the same checks. rim = inside, <= 2.5 px from the phi=1/2 boundary; core = inside,
distance >= half the cell's max inner distance; outside = 3-6 px beyond the boundary.
usage: ringmove.py world.py seed celltrack.json T"""
import sys, json, numpy as np
from scipy import ndimage
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit.world import load_world
W = load_world(sys.argv[1]); seed = int(sys.argv[2]); ct = json.load(open(sys.argv[3])); T = int(sys.argv[4])
tracks = ct["tracks"]
def bl(t):
    p = np.array(t["path"], float); a = np.mean(t["area"])
    d = np.diff(p[:, 1:], axis=0); d = (d + 64) % 128 - 64
    return np.hypot(*d.sum(0)) / np.sqrt(a)
movers = {k: t for k, t in tracks.items() if len(t["path"]) > 2 and bl(t) >= 3}
print("tracks moving >= 3 BL:", len(movers))
pos = {}  # time -> list of (track id, y, x)
for k, t in tracks.items():
    for (tt, y, x) in t["path"]:
        pos.setdefault(int(tt), []).append((k, y, x))
s = W.init(seed, (128, 128)); res = {"mover": [], "other": []}
dt = W.META.get("dt", 1.0)
for step in range(1, T + 1):
    s = W.step(s)
    t = int(round(step * dt))
    if t % 100 or t not in pos: continue
    M = s["phi"] > 0.5; lab, n = ndimage.label(M)
    for k, y, x in pos[t]:
        j = lab[int(round(y)) % 128, int(round(x)) % 128]
        if not j: continue
        c = lab == j
        if c[0].any() or c[-1].any() or c[:, 0].any() or c[:, -1].any(): continue  # skip cells cut by the border
        d = ndimage.distance_transform_edt(c); do = ndimage.distance_transform_edt(~c)
        rim = c & (d <= 2.5); core = c & (d >= 0.5 * d.max()); out = (do >= 3) & (do <= 6) & ~M
        if core.sum() < 3 or out.sum() < 3: continue
        L = s["L"]
        res["mover" if k in movers else "other"].append((L[rim].mean() / max(L[core].mean(), 1e-9), L[rim].mean() / max(L[out].mean(), 1e-9)))
for g, v in res.items():
    v = np.array(v)
    print(f"{g}: n={len(v)} cell-checks, L rim/core median {np.median(v[:,0]):.2f} (share >= 1.5: {np.mean(v[:,0] >= 1.5):.2f}), rim/outside median {np.median(v[:,1]):.2f} (share >= 1.5: {np.mean(v[:,1] >= 1.5):.2f})")
