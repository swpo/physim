"""(c29) Particle-identity tracker for PPS cells.
Every DT steps: bodies = connected clusters of 'non-free' particles (N >= NMIN neighbours within r=5), linked
when closer than LINK, with >= MINP particles. Cluster a at t links to b at t+DT when they share >= FR of the
smaller one's particles (particle identity, not pixels). Events: split (1 -> >= 2), merge (>= 2 -> 1),
death (no child), birth-from-nothing (no parent: nucleation from the gas). A split is persistent when >= 2
children each live (as themselves or through further splits, never merging back into a sibling's line) for
>= HOLD steps. Generation = number of persistent splits on the ancestry. Per body: size, radius of gyration,
ring index = mean distance of its particles from the centroid / R_g of a uniform disc of the same R_max
(> 1 means particles sit at the rim, i.e. hollow), core = fraction within 0.35 R_max.
usage: ppstrack.py world.py seed T out.json [snapdir]"""
import sys, os, json, importlib.util
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

DT, FR, HOLD, NMIN, LINK, MINP = (int(os.environ.get("DT", 50)), 0.3, int(os.environ.get("HOLD", 1500)),
                                 int(os.environ.get("NMIN", 11)), float(os.environ.get("LINK", 4.0)), int(os.environ.get("MINP", 15)))
wf, seed, T, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
snapdir = sys.argv[5] if len(sys.argv) > 5 else None
spec = importlib.util.spec_from_file_location("w", wf); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
Lb = w.P["L"]


def bodies(x, y, N):
    idx = np.nonzero(N >= NMIN)[0]
    lab = -np.ones(len(x), np.int64)
    if len(idx) < MINP: return lab, []
    pts = np.c_[x[idx], y[idx]]
    pr = cKDTree(pts, boxsize=Lb).query_pairs(LINK, output_type="ndarray")
    g = coo_matrix((np.ones(len(pr)), (pr[:, 0], pr[:, 1])), shape=(len(idx), len(idx)))
    nc, cl = connected_components(g, directed=False)
    sizes = np.bincount(cl, minlength=nc); keep = np.nonzero(sizes >= MINP)[0]
    info = []
    for k, c in enumerate(keep):
        m = idx[cl == c]; lab[m] = k
        ang = 2 * np.pi / Lb
        cx = (np.angle(np.exp(1j * ang * x[m]).mean()) / ang) % Lb; cy = (np.angle(np.exp(1j * ang * y[m]).mean()) / ang) % Lb
        dx = x[m] - cx; dy = y[m] - cy; dx -= Lb * np.round(dx / Lb); dy -= Lb * np.round(dy / Lb)
        d = np.hypot(dx, dy); R = d.max() + 1e-9
        info.append({"n": int(len(m)), "cx": float(cx), "cy": float(cy), "rg": float(np.sqrt((d ** 2).mean())),
                     "ring": float(d.mean() / (2 * R / 3)), "core": float((d < 0.35 * R).mean()), "R": float(R)})
    return lab, info


s = w.init(seed, None)
frames = []; labs = []
snaps = []
for t in range(T + 1):
    if t % DT == 0:
        lab, info = bodies(s["x"], s["y"], s["N"]); labs.append(lab); frames.append((t, info))
        if snapdir and t % 250 == 0: snaps.append((t, s["x"].astype(np.float32).copy(), s["y"].astype(np.float32).copy(), s["N"].astype(np.int16).copy()))
    if t < T: s = w.step(s)

# tracks: one track per (frame, body) chain with single parent and single child
tracks = {}; cur = {}; nid = 0; events = []
for fi, (t, info) in enumerate(frames):
    lab = labs[fi]; new = {}
    if fi == 0:
        for k in range(len(info)):
            tracks[nid] = {"t0": t, "t1": t, "parents": [], "children": [], "hist": [[t] + [info[k][q] for q in ("n", "cx", "cy", "ring", "core")]]}; new[k] = nid; nid += 1
        cur = new; continue
    prev = labs[fi - 1]; both = (prev >= 0) & (lab >= 0)
    pa, ch = prev[both], lab[both]
    pairs = {}
    for a, b in zip(pa.tolist(), ch.tolist()): pairs[(a, b)] = pairs.get((a, b), 0) + 1
    pinfo = frames[fi - 1][1]
    links = [(a, b) for (a, b), c in pairs.items() if c >= FR * min(pinfo[a]["n"], info[b]["n"])]
    par = {}; chi = {}
    for a, b in links: par.setdefault(b, []).append(a); chi.setdefault(a, []).append(b)
    for b in range(len(info)):
        ps = par.get(b, [])
        if len(ps) == 1 and len(chi[ps[0]]) == 1:  # continuation
            tid = cur[ps[0]]; new[b] = tid
        else:
            tracks[nid] = {"t0": t, "t1": t, "parents": [cur[a] for a in ps if a in cur], "children": [], "hist": []}
            for a in ps:
                if a in cur: tracks[cur[a]]["children"].append(nid)
            new[b] = nid; nid += 1
            if len(ps) >= 2: events.append(["merge", t, [cur[a] for a in ps], new[b]])
            if not ps: events.append(["birth", t, None, new[b]])
        tracks[new[b]]["t1"] = t; tracks[new[b]]["hist"].append([t] + [info[b][q] for q in ("n", "cx", "cy", "ring", "core")])
    for a in range(len(pinfo)):
        if len(chi.get(a, [])) >= 2: events.append(["split", t, cur[a], [new[b] for b in chi[a]]])
        if a not in chi: events.append(["death", t, cur[a], None])
    cur = new

Tend = frames[-1][0]
def survives(i, until):
    tr = tracks[i]
    if tr["t1"] >= until: return True
    return any(len(tracks[c]["parents"]) == 1 and survives(c, until) for c in tr["children"])

def maxn(i, until):
    """largest size along i's line (continuations and single-parent descendants) up to time until"""
    tr = tracks[i]; m = max([h[1] for h in tr["hist"] if h[0] <= until], default=0)
    if tr["t1"] < until:
        for c in tr["children"]:
            if len(tracks[c]["parents"]) == 1: m = max(m, maxn(c, until))
    return m

gen = {}; psplits = []
for e in sorted([e for e in events if e[0] == "split"], key=lambda e: e[1]):
    t, p, kids = e[1], e[2], e[3]
    if t + HOLD > Tend:  # too late to test persistence
        for k in kids: gen.setdefault(k, gen.get(p, 0))
        continue
    ok = [k for k in kids if survives(k, t + HOLD)]
    if len(ok) >= 2:
        g = gen.get(p, 0) + 1
        psplits.append({"t": t, "parent": p, "kids": ok, "gen": g, "parent_n": tracks[p]["hist"][-1][1] if tracks[p]["hist"] else None,
                        "kid_n": [tracks[k]["hist"][0][1] for k in ok if tracks[k]["hist"]],
                        "kid_max_n_3000": [maxn(k, t + 3000) for k in ok]})
        for k in ok: gen[k] = g
    for k in kids: gen.setdefault(k, gen.get(p, 0))
# propagate generation along continuation/merge (max of parents) chronologically
for i in sorted(tracks, key=lambda i: tracks[i]["t0"]):
    if i not in gen and tracks[i]["parents"]: gen[i] = max(gen.get(p, 0) for p in tracks[i]["parents"])
    gen.setdefault(i, 0)
nb = [len(f[1]) for f in frames]
summary = {"seed": seed, "T": T, "bodies_final": nb[-1], "bodies_max": max(nb), "bodies_mean_2nd_half": float(np.mean(nb[len(nb) // 2:])),
           "splits": sum(e[0] == "split" for e in events), "merges": sum(e[0] == "merge" for e in events),
           "deaths": sum(e[0] == "death" for e in events), "nucleations": sum(e[0] == "birth" for e in events),
           "persistent_splits": len(psplits), "max_generation": max([p["gen"] for p in psplits], default=0),
           "settings": {"DT": DT, "HOLD": HOLD, "NMIN": NMIN, "LINK": LINK, "MINP": MINP},
           "propagule_splits_kids_reach_half_parent": sum(all(k >= 0.5 * p["parent_n"] for k in p["kid_max_n_3000"]) for p in psplits),
           "median_parent_n_at_split": float(np.median([p["parent_n"] for p in psplits])) if psplits else None,
           "counts_t": [[f[0], len(f[1]), int(sum(b["n"] for b in f[1]))] for f in frames[::10]]}
print(json.dumps({k: v for k, v in summary.items() if k != "counts_t"}))
json.dump({"summary": summary, "psplits": psplits, "events": events, "gen": {str(k): v for k, v in gen.items()},
           "tracks": {str(k): v for k, v in tracks.items()}}, open(out, "w"))
if snapdir:
    np.savez_compressed(os.path.join(snapdir, f"snaps_s{seed}.npz"), t=np.array([q[0] for q in snaps]), x=np.stack([q[1] for q in snaps]),
                        y=np.stack([q[2] for q in snaps]), N=np.stack([q[3] for q in snaps]))
