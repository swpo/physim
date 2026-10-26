"""c28: c07's celltrack.py plus a per-cell link-ring score measured by distance to the cell contour
(ring = mean L within 3 px inside the contour / mean L deeper than max(4 px, half the cell's max depth)),
so elongated crescents are scored by their own wall, not by a centroid-radial profile.

Overlap tracker for phase-field cells (phi > 1/2 components on the periodic torus).

The grid size is taken from the world META["size"].
usage: python celltrack.py world.py seed T out.json [key=val ...]   (key=val override world P)

Every DT steps: label cells; link cell j at t to cell i at t-DT when they share >= FR of the
smaller one's pixels. Events: split (1 parent -> >= 2 children), merge (>= 2 parents -> 1),
death (no child), birth-from-nothing (no parent). A split is *persistent* when >= 2 of its
children each survive (as themselves or through further splits, never merging back with a
sibling's line) for >= HOLD time. Generation of a cell = number of persistent splits on its
ancestry since t0 (cells present at T0 have generation 0). Motion: each track's centroid path
(unwrapped) gives net displacement / sqrt(mean area) = body lengths.
"""
import json
import sys

import numpy as np
from scipy import ndimage

sys.path.insert(0, "/home/user/physim/research/alife")
from labkit.world import load_world

DT, FR, HOLD, T0, MINA = 20, 0.3, 400, 1000, 20
import os as _os
SNAP = [] if _os.environ.get("SNAP") else None


def plabel(mask):
    lab, n = ndimage.label(mask)
    par = list(range(n + 1))

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for a, b in ((lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])):
        for u, v in zip(a.tolist(), b.tolist()):
            if u and v and f(u) != f(v):
                par[f(v)] = f(u)
    roots = np.array([f(x) for x in range(n + 1)])
    lab = roots[lab]
    ids, lab = np.unique(lab, return_inverse=True)
    lab = lab.reshape(mask.shape)
    return lab, len(ids) - 1


def ring_score(mask, L):
    # periodic: roll the cell to the middle so it does not straddle the edge, then distance inside
    ys, xs = np.nonzero(mask)
    sy = mask.shape[0] // 2 - int(np.angle(np.exp(2j * np.pi * ys / mask.shape[0]).mean()) * mask.shape[0] / (2 * np.pi) % mask.shape[0])
    sx = mask.shape[1] // 2 - int(np.angle(np.exp(2j * np.pi * xs / mask.shape[1]).mean()) * mask.shape[1] / (2 * np.pi) % mask.shape[1])
    m = np.roll(mask, (sy, sx), (0, 1)); Lr = np.roll(L, (sy, sx), (0, 1))
    d = ndimage.distance_transform_edt(m)
    rim = m & (d <= 3)
    core = m & (d >= max(4.0, 0.5 * d.max()))
    if core.sum() < 3 or rim.sum() < 3:
        return None
    return round(float(Lr[rim].mean() / max(Lr[core].mean(), 1e-9)), 3)


def centroid(ys, xs, H, W):
    cy = np.angle(np.exp(2j * np.pi * ys / H).mean()) * H / (2 * np.pi) % H
    cx = np.angle(np.exp(2j * np.pi * xs / W).mean()) * W / (2 * np.pi) % W
    return cy, cx


def run(world, seed, T, kv):
    W = load_world(world)
    for k, v in kv.items():
        try:
            W.P[k] = float(v)
        except ValueError:
            W.P[k] = v
    H, Wd = W.META["size"]
    s = W.init(seed, (H, Wd))
    prev = None
    tracks = {}   # id -> dict(t0, t1, path[(t,cy,cx)], area[], parents[], children[])
    nid = 0
    events = []
    for t in range(T + 1):
        if t % DT == 0 and t >= T0:
            lab, n = plabel(s["phi"] > 0.5)
            areas = np.bincount(lab.ravel(), minlength=n + 1)
            keep = [i for i in range(1, n + 1) if areas[i] >= MINA]
            cur = {}
            for i in keep:
                ys, xs = np.nonzero(lab == i)
                cur[i] = dict(cent=centroid(ys, xs, H, Wd), area=int(areas[i]), ring=ring_score(lab == i, s["L"]))
            ids = {}
            if prev is None:
                for i in keep:
                    ids[i] = nid; tracks[nid] = dict(t0=t, t1=t, path=[], area=[], parents=[], children=[], gen0=True); nid += 1
            else:
                plab, pids = prev
                pairs = {}
                m = (plab > 0) & (lab > 0)
                for a, b in zip(plab[m].tolist(), lab[m].tolist()):
                    pairs[(a, b)] = pairs.get((a, b), 0) + 1
                pa = np.bincount(plab.ravel())
                par_of = {i: [] for i in keep}
                for (a, b), c in pairs.items():
                    if a in pids and b in cur and c >= FR * min(pa[a], cur[b]["area"]):
                        par_of[b].append(pids[a])
                ch_of = {}
                for b, ps in par_of.items():
                    for p in ps:
                        ch_of.setdefault(p, []).append(b)
                for b in keep:
                    ps = par_of[b]
                    if len(ps) == 1 and len(ch_of[ps[0]]) == 1:
                        ids[b] = ps[0]
                    else:
                        ids[b] = nid
                        tracks[nid] = dict(t0=t, t1=t, path=[], area=[], parents=ps, children=[], gen0=False)
                        for p in ps:
                            tracks[p]["children"].append(nid)
                        nid += 1
                for p, chs in ch_of.items():
                    if len(chs) >= 2:
                        events.append(("split", t, p, [ids[c] for c in chs]))
                for b in keep:
                    if len(par_of[b]) >= 2:
                        events.append(("merge", t, par_of[b], ids[b]))
                alive = set(ids.values())
                for p in pids.values():
                    if p not in alive and not tracks[p]["children"]:
                        events.append(("death", t, p))
            for b in keep:
                tr = tracks[ids[b]]
                tr["t1"] = t; tr["path"].append((t, *cur[b]["cent"])); tr["area"].append(cur[b]["area"]); tr.setdefault("ring", []).append(cur[b]["ring"])
            prev = (lab, ids)
        if SNAP is not None and t % 200 == 0:
            SNAP.append((t, s["phi"].astype(np.float16), s["L"].astype(np.float16), s["K"].astype(np.float16)))
        s = W.step(s)
    return tracks, events


def analyse(tracks, events, T, N=128):
    # descendants never merging with a sibling's line: approximate by "lineage survives HOLD"
    def survives(i, until):
        tr = tracks[i]
        if tr["t1"] >= until:
            return True
        chs = tr["children"]
        if not chs:
            return False
        # a merge child has >= 2 parents: counts as lost identity
        return any(len(tracks[c]["parents"]) == 1 and survives(c, until) for c in chs)
    psplits = []
    for e in events:
        if e[0] != "split":
            continue
        _, t, p, chs = e
        ok = [c for c in chs if survives(c, t + HOLD)]
        if len(ok) >= 2:
            # siblings must not merge back with each other within HOLD
            psplits.append(dict(t=t, parent=p, children=ok))
    ps_children = {c for e in psplits for c in e["children"]}
    gen = {}
    for i in sorted(tracks):
        tr = tracks[i]
        if not tr["parents"]:
            gen[i] = 0
        else:
            gen[i] = max(gen.get(p, 0) for p in tr["parents"]) + (1 if (len(tr["parents"]) == 1 and i in ps_children) else 0)
    motion = []
    for i, tr in tracks.items():
        P = tr["path"]
        if len(P) < 5:
            continue
        cy = np.array([p[1] for p in P]); cx = np.array([p[2] for p in P])
        dy = (np.diff(cy) + N / 2) % N - N / 2; dx = (np.diff(cx) + N / 2) % N - N / 2
        net = float(np.hypot(dy.sum(), dx.sum())); size = float(np.sqrt(np.mean(tr["area"])))
        motion.append(dict(id=i, life=tr["t1"] - tr["t0"], net=round(net, 1), BL=round(net / size, 2), size=round(size, 1),
                           speed=round(net / max(1, tr["t1"] - tr["t0"]), 4)))
    motion.sort(key=lambda m: -m["BL"])
    n_split = sum(e[0] == "split" for e in events); n_merge = sum(e[0] == "merge" for e in events)
    own_split = {e["parent"] for e in psplits}
    mot = {m["id"]: m for m in motion}
    cand = [dict(id=i, gen=gen[i], BL=mot[i]["BL"], life=mot[i]["life"], t0=tracks[i]["t0"], t1=tracks[i]["t1"],
                 parents=tracks[i]["parents"], children=tracks[i]["children"])
            for i in tracks if i in mot and i in own_split and gen[i] >= 2 and mot[i]["BL"] >= 3]
    cand.sort(key=lambda c: (-c["gen"], -c["BL"]))
    return dict(candidates=cand[:10], persistent_splits=len(psplits), max_generation=max(gen.values()) if gen else 0,
                splits=n_split, merges=n_merge, deaths=sum(e[0] == "death" for e in events),
                tracks_ge3BL=sum(m["BL"] >= 3 for m in motion), tracks_ge5BL=sum(m["BL"] >= 5 for m in motion),
                top_motion=motion[:10], split_times=[p["t"] for p in psplits],
                gen_hist={str(g): sum(1 for v in gen.values() if v == g) for g in sorted(set(gen.values()))})


if __name__ == "__main__":
    world, seed, T, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    kv = dict(a.split("=", 1) for a in sys.argv[5:])
    tracks, events = run(world, seed, T, kv)
    A = analyse(tracks, events, T, load_world(world).META["size"][0])
    A.update(world=world, seed=seed, T=T, params=kv)
    json.dump(dict(summary=A, tracks={str(k): dict(t0=v["t0"], t1=v["t1"], parents=v["parents"], children=v["children"],
              path=[[int(p[0]), round(float(p[1]), 1), round(float(p[2]), 1)] for p in v["path"]], area=v["area"], ring=v.get("ring", [])) for k, v in tracks.items()},
              events=[list(map(lambda x: x if not isinstance(x, np.generic) else x.item(), e)) for e in events]), open(out, "w"), default=str)
    if SNAP is not None:
        np.savez_compressed(_os.environ["SNAP"], t=np.array([x[0] for x in SNAP]), phi=np.stack([x[1] for x in SNAP]),
                            L=np.stack([x[2] for x in SNAP]), K=np.stack([x[3] for x in SNAP]))
    print(json.dumps({k: v for k, v in A.items() if k != "top_motion"}))
    print(json.dumps(A["top_motion"][:5]))
    print(json.dumps(A["candidates"]))
