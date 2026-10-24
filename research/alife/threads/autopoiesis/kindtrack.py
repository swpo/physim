"""Labkit-independent overlap tracker for membrane_kinds runs.

python kindtrack.py OUT.json seed T key=val ...
Every 100 steps: cells = phi > 1/2 components (periodic). Each cell gets its kind (K2 fraction
> 1/2 -> K2). Matching by pixel overlap with the previous census:
  birth   = a parent with >= 2 overlapping children (each extra child is a birth of its kind)
  death   = a cell with no overlapping successor
  merge   = a child with >= 2 parents
  conversion = a 1-to-1 match (one parent, one child, parent has one child) whose kind changes
Also prints counts per kind over time.
"""
import sys, json
import numpy as np
from scipy import ndimage
sys.path.insert(0, ".")
from labkit.world import load_world


def labels(phi):
    lab, n = ndimage.label(phi > 0.5)
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):
        for u, v in set(zip(a.tolist(), b.tolist())):
            if u and v and u != v:
                lab[lab == v] = u
    ids = [i for i in np.unique(lab) if i]
    return lab, ids


out, seed, T = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
W = load_world("threads/autopoiesis/worlds/membrane_kinds/world.py")
for kv in sys.argv[4:]:
    k, v = kv.split("=")
    W.P[k] = type(W.P[k])(eval(v))
s = W.init(seed, (128, 128))
ev = {"birth": {"K1": 0, "K2": 0}, "death": {"K1": 0, "K2": 0}, "merge": 0,
      "conv_K1_to_K2": 0, "conv_K2_to_K1": 0}
series = []
prev = None
for t in range(T + 1):
    if t % 100 == 0 and t >= 1000:  # census after the noise start has settled
        lab, ids = labels(s["phi"])
        k1 = dict(zip(ids, ndimage.sum(s["K"], lab, ids))) if ids else {}
        k2 = dict(zip(ids, ndimage.sum(s["K2"], lab, ids))) if ids else {}
        kind = {i: ("K2" if k2[i] > k1[i] else "K1") for i in ids}
        if prev is not None:
            plab, pids, pkind = prev
            pairs = {}
            m = (plab > 0) & (lab > 0)
            for a, b in set(zip(plab[m].tolist(), lab[m].tolist())):
                pairs.setdefault(a, set()).add(b)
            children_of = pairs
            parents_of = {}
            for a, bs in pairs.items():
                for b in bs:
                    parents_of.setdefault(b, set()).add(a)
            for a in pids:
                ch = children_of.get(a, set())
                if not ch:
                    ev["death"][pkind[a]] += 1
                elif len(ch) >= 2:
                    for b in ch:
                        if len(parents_of[b]) == 1:
                            ev["birth"][kind[b]] += 1
                    ev["birth"][pkind[a]] -= 1  # one child continues the parent
                else:
                    b = next(iter(ch))
                    if len(parents_of[b]) == 1 and kind[b] != pkind[a]:
                        ev["conv_%s_to_%s" % (pkind[a], kind[b])] += 1
            ev["merge"] += sum(1 for b, ps in parents_of.items() if len(ps) >= 2)
        prev = (lab, ids, kind)
        if t % 2000 == 0:
            series.append({"t": t, "K1": sum(1 for v in kind.values() if v == "K1"),
                           "K2": sum(1 for v in kind.values() if v == "K2"), "nmut": s["nmut"]})
    s = W.step(s)
res = {"args": sys.argv[4:], "seed": seed, "T": T, "events": ev, "nmut": s["nmut"], "series": series}
json.dump(res, open(out, "w"), indent=1)
print(json.dumps({"args": sys.argv[4:], "seed": seed, "events": ev, "nmut": s["nmut"], "final": series[-1]}))
