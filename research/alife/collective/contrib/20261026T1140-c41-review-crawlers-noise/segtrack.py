"""Merge-aware motion of crawler-phase-field bodies from a labkit frames.npz.

Each body is followed frame to frame by overlap (periodic labels). A segment ends when the body
merges (another component's pixels join it), splits, or its area jumps by > 15%. Within a
segment the centroid moves with the body (periodic unwrap); net displacement is divided by the
body length 2 sqrt(A/pi) at that segment's mean area. Reports, per body, its best segment and the
sum over its segments of net displacement in body lengths.
usage: segtrack.py frames.npz dt_frame L N [threshold]"""
import sys, json, numpy as np
from scipy import ndimage as ndi
fr = np.load(sys.argv[1]); dtf = float(sys.argv[2]); L = float(sys.argv[3]); N = int(sys.argv[4])
thr = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
M = fr["matter"].astype(np.float32); dx = L / N
def label(m):
    lab, n = ndi.label(m)
    # periodic merge of labels across edges
    par = list(range(n + 1))
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for a, b in list(zip(lab[0], lab[-1])) + list(zip(lab[:, 0], lab[:, -1])):
        if a and b: par[f(a)] = f(b)
    lab = np.vectorize(f)(lab) if n else lab
    ids = [i for i in np.unique(lab) if i]
    return lab, ids
yy, xx = np.mgrid[0:N, 0:N]
def cent(mask):
    out = []
    for g in (xx, yy):
        th = g[mask] * 2 * np.pi / N
        out.append((np.arctan2(np.sin(th).mean(), np.cos(th).mean()) % (2 * np.pi)) * N / (2 * np.pi))
    return np.array(out)
prev = None; segs = []; open_ = {}  # open_[label] = dict(start, pos list, areas)
nid = 0
for k in range(M.shape[0]):
    lab, ids = label(M[k] > thr)
    cur = {}
    for i in ids:
        mk = lab == i; A = mk.sum()
        if A < 30: continue
        cur[i] = (mk, A, cent(mk))
    new_open = {}
    if prev is not None:
        # overlaps
        links = {}
        for i, (mk, A, c) in cur.items():
            parents = [j for j, (pm, pA, pc) in prev.items() if (pm & mk).sum() > 0.2 * min(A, pA)]
            links[i] = parents
        children = {}
        for i, ps in links.items():
            for j in ps: children.setdefault(j, []).append(i)
        for i, ps in links.items():
            mk, A, c = cur[i]
            if len(ps) == 1 and len(children.get(ps[0], [])) == 1 and ps[0] in open_ and abs(A - prev[ps[0]][1]) < 0.15 * prev[ps[0]][1]:
                s = open_[ps[0]]
                d = (c - s["last"] + N / 2) % N - N / 2
                s["disp"] = s["disp"] + d; s["last"] = c; s["areas"].append(A); s["end"] = k
                new_open[i] = s
            else:
                new_open[i] = dict(id=nid, start=k, end=k, disp=np.zeros(2), last=c, areas=[A], why="merge" if len(ps) > 1 else ("split" if ps and len(children.get(ps[0], [])) > 1 else "jump/new"))
                nid += 1
        for j, s in open_.items():
            if all(s is not t for t in new_open.values()): segs.append(s)
    else:
        for i, (mk, A, c) in cur.items():
            new_open[i] = dict(id=nid, start=k, end=k, disp=np.zeros(2), last=c, areas=[A], why="t0"); nid += 1
    open_ = new_open; prev = cur
segs += list(open_.values())
rows = []
for s in segs:
    if s["end"] - s["start"] < 3: continue
    Am = np.mean(s["areas"]); bl = 2 * np.sqrt(Am / np.pi)
    rows.append(dict(seg=s["id"], t0=round(s["start"] * dtf, 2), t1=round(s["end"] * dtf, 2), frames=s["end"] - s["start"],
                     area_px=int(Am), net_px=round(float(np.hypot(*s["disp"])), 1), body_lengths=round(float(np.hypot(*s["disp"]) / bl), 2)))
rows.sort(key=lambda r: -r["body_lengths"])
print(json.dumps(rows[:12], indent=0))
