"""c48: consumer body persistence in the c43 cips-consumer run. Labels q > 0.5 (>= 6 px) in every recorded frame
(100 t apart) and links a body to the next frame's bodies it overlaps. A body 'continues' if at least one successor
overlaps it; a chain ends when a body has no successor (dissolution). Reports, for bodies present at t=2000, how
long until their line (any descendant through splits/merges) ends, and the share of bodies that end without
successor per 100 t. usage: python lifetimes.py run_dir"""
import sys, json, numpy as np
from scipy import ndimage
R = np.load(sys.argv[1] + "/frames.npz")["render"]; T = len(R)
labs = []
for i in range(T):
    lab, n = ndimage.label(R[i][1] > 0.5); sz = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    keep = [j + 1 for j in range(n) if sz[j] >= 6]; labs.append((lab, keep))
ends, total = 0, 0; succ = []
for i in range(T - 1):
    lab, keep = labs[i]; lab2, keep2 = labs[i + 1]; s = []
    for j in keep:
        nxt = set(np.unique(lab2[lab == j])) & set(keep2); s.append(nxt); total += 1; ends += (len(nxt) == 0)
    succ.append(dict(zip(keep, s)))
# line survival: from frame f0, follow the set of descendants
f0 = 20; alive = {j: {j} for j in labs[f0][1]}; life = {}
for j in labs[f0][1]:
    cur = {j}; k = f0
    while cur and k < T - 1:
        nxt = set()
        for c in cur: nxt |= succ[k].get(c, set())
        cur = nxt; k += 1
    life[j] = (k - f0) * 100 if not cur else None
done = [v for v in life.values() if v is not None]
res = {"bodies_per_frame_mean": float(np.mean([len(k) for _, k in labs[f0:]])), "end_without_successor_per_100t": round(ends / max(total, 1), 4),
       "lines_from_t2000": len(life), "lines_alive_at_end": sum(1 for v in life.values() if v is None),
       "ended_line_lifetimes_t": sorted(done)}
print(json.dumps(res)); json.dump(res, open(sys.argv[1].rstrip("/").split("/")[-2] + "_lifetimes.json", "w"))
