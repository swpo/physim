"""c13 copy of threads/autopoiesis/evotrack.py with a birth-cause ledger (birth_disk: births whose parent was hit
by a disk death in the same 100-step census interval) and EVO_WORLD to choose the world file.

Lineage tracker for membrane_evo (committee r2 arm E). Labkit-independent.

python evotrack.py OUT.json seed T key=val ...
Census every 100 steps from t_on: bodies = phi > 1/2 components (periodic), dilated 2 px for
kind sums. Each body: kind (majority catalyst), K2 fraction, tag (catalyst-weighted).
Matching by overlap with the previous census:
  birth   parent with >= 2 children: each extra child is a birth (of the child's kind);
          off-kind daughter = child kind != parent kind
  death   body with no successor (split by cause: inside a death disk in this interval or not)
  merge   child with >= 2 parents
  flip    world event hitting the body (from s["events"])
  conversion  1:1 match whose kind changed with no flip on that lineage in the interval
  first acquisition  a lineage that never flipped (and descends only from never-flipped
          lineages) whose minority-kind fraction first exceeds 1%
Series: counts and biomass per kind, mean tag.
"""
import sys, json
import numpy as np
from scipy import ndimage
sys.path.insert(0, ".")
from labkit.world import load_world


def bodies(phi):
    lab, n = ndimage.label(phi > 0.5)
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):
        for u, v in set(zip(a.tolist(), b.tolist())):
            if u and v and u != v:
                lab[lab == v] = u
    ids = [int(i) for i in np.unique(lab) if i]
    return lab, ids


out, seed, T = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
W = load_world(__import__("os").environ.get("EVO_WORLD", "threads/autopoiesis/worlds/membrane_evo/world.py"))
for kv in sys.argv[4:]:
    k, v = kv.split("=")
    W.P[k] = type(W.P[k])(eval(v))
s = W.init(seed, (128, 128))
E = {"birth": {"K1": 0, "K2": 0}, "death": {"K1": 0, "K2": 0}, "death_disk": {"K1": 0, "K2": 0},
     "birth_disk": {"K1": 0, "K2": 0}, "merge": 0, "flip": {"K1->K2": 0, "K2->K1": 0}, "conversion": {"K1->K2": 0, "K2->K1": 0},
     "first_acq": 0, "offkind_daughters": 0}
series, prev, nev = [], None, 0
tracks = {}  # census label -> lineage record {flipped: bool, home: kind at lineage origin, acq: bool}
t_on = W.P["t_on"]
for t in range(T + 1):
    if t >= t_on and t % 100 == 0:
        phi = s["phi"]
        lab, ids = bodies(phi)
        dl = ndimage.grey_dilation(lab, size=5, mode="wrap") * (phi > 0.05)
        dl = np.where(lab > 0, lab, dl)
        k1 = dict(zip(ids, ndimage.sum(s["K"], dl, ids))) if ids else {}
        k2 = dict(zip(ids, ndimage.sum(s["K2"], dl, ids))) if ids else {}
        qt = dict(zip(ids, ndimage.sum(s["Qt"], dl, ids))) if ids else {}
        f2 = {i: k2[i] / max(k1[i] + k2[i], 1e-9) for i in ids}
        kind = {i: ("K2" if f2[i] > 0.5 else "K1") for i in ids}
        # events since last census
        new = s["events"][nev:]; nev = len(s["events"])
        flipped_now = set(); disks = []
        for (te, typ, y, x, det) in new:
            if typ == "flip":
                E["flip"][det] += 1
                if lab[y, x]:
                    flipped_now.add(int(lab[y, x]))
            elif typ == "death":
                disks.append((y, x))
        cur = {}
        if prev is None:
            for i in ids:
                cur[i] = {"flipped": False, "acq": False}
        else:
            plab, pids, pkind, ptr = prev
            m = (plab > 0) & (lab > 0)
            ch, pa = {}, {}
            for a, b in set(zip(plab[m].tolist(), lab[m].tolist())):
                ch.setdefault(a, set()).add(b); pa.setdefault(b, set()).add(a)
            for a in pids:
                kids = ch.get(a, set())
                if not kids:
                    H, Wd = lab.shape
                    ys, xs = np.nonzero(plab == a)
                    hit = any(((((ys - y + H // 2) % H - H // 2) ** 2 + ((xs - x + Wd // 2) % Wd - Wd // 2) ** 2) <= W.P["r_death"] ** 2).any() for y, x in disks)
                    E["death_disk" if hit else "death"][pkind[a]] += 1
                elif len(kids) >= 2:
                    singles = [b for b in kids if len(pa[b]) == 1]
                    H, Wd = lab.shape
                    ys, xs = np.nonzero(plab == a)
                    hitp = any(((((ys - y + H // 2) % H - H // 2) ** 2 + ((xs - x + Wd // 2) % Wd - Wd // 2) ** 2) <= W.P["r_death"] ** 2).any() for y, x in disks)
                    for b in singles[1:]:
                        E["birth"][kind[b]] += 1
                        if hitp:  # c13: birth-cause ledger, a disk death hit the parent in this census interval
                            E["birth_disk"][kind[b]] += 1
                    for b in singles:
                        if kind[b] != pkind[a] and b not in flipped_now:
                            E["offkind_daughters"] += 1
            E["merge"] += sum(1 for b, ps in pa.items() if len(ps) >= 2)
            for b in ids:
                ps = pa.get(b, set())
                rec = {"flipped": any(ptr[p]["flipped"] for p in ps), "acq": any(ptr[p]["acq"] for p in ps)}
                if b in flipped_now:
                    rec["flipped"] = True
                if len(ps) == 1:
                    a = next(iter(ps))
                    if len(ch[a]) == 1 and kind[b] != pkind[a] and b not in flipped_now:
                        E["conversion"]["%s->%s" % (pkind[a], kind[b])] += 1
                cur[b] = rec
        for i in ids:  # first acquisition: minority kind appears in a never-flipped lineage
            minority = min(f2[i], 1 - f2[i])
            if not cur[i]["flipped"] and not cur[i]["acq"] and minority > 0.01:
                E["first_acq"] += 1; cur[i]["acq"] = True
        prev = (lab, ids, kind, cur)
        if t % 1000 == 0:
            series.append({"t": t, "K1": sum(1 for v in kind.values() if v == "K1"), "K2": sum(1 for v in kind.values() if v == "K2"),
                           "bio1": round(float(s["K"].sum()), 1), "bio2": round(float(s["K2"].sum()), 1),
                           "tag": round(float(sum(qt.values()) / max(sum(k1.values()) + sum(k2.values()), 1e-9)), 3)})
    s = W.step(s)
res = {"args": sys.argv[4:], "seed": seed, "T": T, "events": E, "series": series,
       "n_events": {k: sum(1 for e in s["events"] if e[1] == k) for k in ("flip", "tag", "death")}}
json.dump(res, open(out, "w"), indent=1)
f = series[-1]
print(json.dumps({"args": sys.argv[4:], "seed": seed, "E": E, "final": f}))
