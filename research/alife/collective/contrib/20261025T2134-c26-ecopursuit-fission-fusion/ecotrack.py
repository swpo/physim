"""Species-aware demographic ledger for eco-pursuit (prey fission, deaths, predator counts).

usage: WORLD_P='{...}' python ecotrack.py world.py out_prefix seed T [every=2] [surv=100]

Prey bodies = components of A+B > thr (0.35), labelled with periodic wrap, area >= 12 px, sampled
every `every` time units. Frames are linked by overlap of the previous labels dilated by dil x dil.
Identity follows the largest piece:
  true merge:   a body with >= 2 parents each >= 25% of its mass (new track; parents end 'merge')
  fission:      a parent with >= 2 children (whose largest parent it is) each >= 25% of its mass;
                the parent ends 'split' and every such child starts a new track (born 'fission')
  otherwise     the largest child carries the parent's track on; smaller children are 'fragment's,
                and a parent with children but no continuation ends 'absorbed' (a small piece swept
                into a larger body); a parent with no child ends 'death' ('eaten' if predator > thr on it)
A fission is CLEAN when >= 2 daughters survive >= surv (or >= surv/4 and then split cleanly themselves);
a merge or death before that disqualifies a daughter. Merge products are never daughters.
Births are counted per event (clean daughters); generation = number of clean fissions in the ancestry
(founders formed from noise are generation 0). A death is 'eaten' if the predator field exceeded thr
on the dying body's last footprint. Writes out_prefix.json (ledger + series) and out_prefix_strip.png
(random clean births from the deepest generation).
"""
import json
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, "/home/user/physim/research/alife")
from labkit.world import load_world  # noqa: E402

args = [a for a in sys.argv[1:] if "=" not in a]
opt = dict(a.split("=") for a in sys.argv[1:] if "=" in a)
W = load_world(args[0])
out, seed, T = args[1], int(args[2]), float(args[3])
every, surv, thr = float(opt.get("every", 2)), float(opt.get("surv", 100)), float(opt.get("thr", 0.35))
smooth = float(opt.get("smooth", 0))  # Gaussian blur (px) of the fields before segmentation (labkit default 1)
dil = int(opt.get("dil", 5))
largest = int(opt.get("largest", 0))  # 1: the largest piece keeps the identity through fissions and merges  # linking: previous labels dilated by dil x dil (1 = plain overlap)
dt = W.P["dt"]
H, Wd = W.META["size"]
nsub = int(round(every / dt))


def label(m):
    lab, n = ndimage.label(m > thr)
    for a, b in ((lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])):
        for x, y in zip(a, b):
            if x and y and x != y:
                lab[lab == y] = x
    ids = np.unique(lab)
    ids = ids[ids > 0]
    areas = ndimage.sum(np.ones_like(m), lab, ids) if len(ids) else []
    outl = np.zeros_like(lab)
    j = 0
    for i, a in zip(ids, areas):
        if a >= 12:
            j += 1
            outl[lab == i] = j
    return outl, j


s = W.init(seed, (H, Wd))
tracks, cur, prev = {}, {}, None
events, series, crops = [], [], []
t, fi = 0.0, 0
while t <= T + 1e-9:
    F = np.asarray(W.fields(s), np.float32)
    prey, pred = F[0] + F[1], F[2]
    if smooth > 0:
        prey, pred = ndimage.gaussian_filter(prey, smooth, mode="wrap"), ndimage.gaussian_filter(pred, smooth, mode="wrap")
    if opt.get("species", "prey") == "pred":  # track predator bodies instead ('eaten' then means prey contact)
        prey, pred = pred, prey
    lab, n = label(prey)
    qlab, nq = label(pred)
    mass = ndimage.sum(prey, lab, np.arange(1, n + 1)) if n else np.zeros(0)
    series.append([round(t, 2), n, nq, float(prey.sum()), float(pred.sum()), float(F[3].mean())])
    crops.append(prey.astype(np.float16))
    new = {}
    if prev is None:
        for j in range(1, n + 1):
            tid = len(tracks)
            tracks[tid] = dict(birth=t, end=t, parents=[], born="init", gen=0, mass0=float(mass[j - 1]),
                               mass=float(mass[j - 1]), endby=None, frames=[(fi, j)])
            new[j] = tid
    else:
        plab, pn, pmass, ppred = prev
        pd = ndimage.grey_dilation(plab, footprint=np.ones((dil, dil)), mode="wrap") if dil > 1 else plab
        par = {j: [int(u) for u in np.unique(pd[lab == j]) if u] for j in range(1, n + 1)}
        ch = {}
        for j, ps in par.items():
            for p in ps:
                ch.setdefault(p, []).append(j)
        mainpar = {j: max(ps, key=lambda p: pmass[p - 1]) for j, ps in par.items() if ps}
        claimed = set()  # previous bodies whose identity has been passed on
        # true merges: >= 2 parents each >= 25% of the product's mass
        for j in range(1, n + 1):
            big = [p for p in par[j] if pmass[p - 1] >= 0.25 * mass[j - 1]]
            if len(big) >= 2 and largest:
                pm = max(big, key=lambda p: pmass[p - 1])
                tid = cur[pm]
                tracks[tid]["end"] = t
                tracks[tid]["mass"] = float(mass[j - 1])
                tracks[tid]["frames"].append((fi, j))
                tracks[tid]["merged"] = tracks[tid].get("merged", 0) + 1
                new[j] = tid
                for p in big:
                    if p != pm:
                        tracks[cur[p]]["endby"] = "merge"
                    claimed.add(p)
            elif len(big) >= 2:
                tid = len(tracks)
                tracks[tid] = dict(birth=t, end=t, parents=[cur[p] for p in big], born="merge", gen=None,
                                   mass0=float(mass[j - 1]), mass=float(mass[j - 1]), endby=None, frames=[(fi, j)])
                new[j] = tid
                for p in big:
                    tracks[cur[p]]["endby"] = "merge"
                    claimed.add(p)
        # fissions: a parent with >= 2 children (whose main parent it is) each >= 25% of its mass
        for p in range(1, pn + 1):
            if p in claimed:
                continue
            kids = [j for j in ch.get(p, []) if j not in new and mainpar.get(j) == p]
            bigk = [j for j in kids if mass[j - 1] >= 0.25 * pmass[p - 1]]
            if len(bigk) >= 2 and largest:
                pt = cur[p]
                jm = max(bigk, key=lambda j: mass[j - 1])
                tracks[pt]["end"] = t
                tracks[pt]["mass"] = float(mass[jm - 1])
                tracks[pt]["frames"].append((fi, jm))
                new[jm] = pt
                ids = []
                for j in bigk:
                    if j == jm:
                        continue
                    tid = len(tracks)
                    tracks[tid] = dict(birth=t, end=t, parents=[pt], born="fission", gen=None,
                                       mass0=float(mass[j - 1]), mass=float(mass[j - 1]), endby=None, frames=[(fi, j)])
                    new[j] = tid
                    ids.append(tid)
                events.append(dict(t=t, parent=pt, kids=[pt] + ids, pmass=float(pmass[p - 1])))
                claimed.add(p)
            elif len(bigk) >= 2:
                pt = cur[p]
                tracks[pt]["endby"] = "split"
                ids = []
                for j in bigk:
                    tid = len(tracks)
                    tracks[tid] = dict(birth=t, end=t, parents=[pt], born="fission", gen=None,
                                       mass0=float(mass[j - 1]), mass=float(mass[j - 1]), endby=None, frames=[(fi, j)])
                    new[j] = tid
                    ids.append(tid)
                events.append(dict(t=t, parent=pt, kids=ids, pmass=float(pmass[p - 1])))
                claimed.add(p)
            elif kids:  # the largest child carries the identity on; smaller pieces are fragments
                jm = max(kids, key=lambda j: mass[j - 1])
                tid = cur[p]
                tracks[tid]["end"] = t
                tracks[tid]["mass"] = float(mass[jm - 1])
                tracks[tid]["frames"].append((fi, jm))
                new[jm] = tid
                claimed.add(p)
        for j in range(1, n + 1):
            if j in new:
                continue
            ps = par[j]
            tid = len(tracks)
            tracks[tid] = dict(birth=t, end=t, parents=[cur[p] for p in ps], born="fragment" if ps else "nucleation",
                               gen=None, mass0=float(mass[j - 1]), mass=float(mass[j - 1]), endby=None, frames=[(fi, j)])
            new[j] = tid
        for p in range(1, pn + 1):
            if p not in claimed and tracks[cur[p]]["endby"] is None:
                # no child carries it on: it died, or was absorbed as a small piece into a larger body
                tracks[cur[p]]["endby"] = "absorbed" if ch.get(p) else ("eaten" if ppred[p - 1] else "death")
    # predator contact per prey body, for death classification at the next frame
    hasq = ndimage.maximum(pred, lab, np.arange(1, n + 1)) > thr if n else np.zeros(0, bool)
    prev = (lab, n, mass, hasq)
    cur = new
    for _ in range(nsub):
        s = W.step(s)
    t += every
    fi += 1

# clean fissions and generations (process in time order)
for tid, tr in tracks.items():
    if tr["endby"] is None:
        tr["endby"] = "alive"
clean = []
for ev in sorted(events, key=lambda e: e["t"]):
    good = []
    for k in ev["kids"]:
        tr = tracks[k]
        life = tr["end"] - tr["birth"]
        ok_s = life >= surv or (tr["endby"] == "split" and life >= surv / 4)
        if tr["mass0"] >= 0.25 * ev["pmass"] and ok_s:
            good.append(k)
    pg = tracks[ev["parent"]]["gen"]
    pg = 0 if pg is None else pg
    for k in ev["kids"]:
        tracks[k]["gen"] = pg + 1 if len(good) >= 2 and k in good else pg
    if len(good) >= 2:
        clean.append(dict(t=ev["t"], parent=ev["parent"], daughters=good, gen=pg + 1))
for tid in sorted(tracks):
    tr = tracks[tid]
    if tr["gen"] is None:
        tr["gen"] = 0 if tr["born"] in ("init", "nucleation", "merge", "fragment") else max(
            [tracks[p]["gen"] or 0 for p in tr["parents"]] + [0])

ends = {}
for tr in tracks.values():
    ends[tr["endby"]] = ends.get(tr["endby"], 0) + 1
mature_deaths = sum(1 for tr in tracks.values() if tr["endby"] in ("death", "eaten") and tr["end"] - tr["birth"] >= surv)
mature_eaten = sum(1 for tr in tracks.values() if tr["endby"] == "eaten" and tr["end"] - tr["birth"] >= surv)
births_clean = sum(len(c["daughters"]) for c in clean)
maxgen = max([c["gen"] for c in clean] + [0])
res = dict(dil=dil, world=W.META["name"], P={k: W.P[k] for k in ("pred", "fork", "t_fork", "B0", "e")}, seed=seed, T=T,
           every=every, surv=surv, splits=len(events), clean_fissions=len(clean), clean_births=births_clean,
           max_generation=maxgen, ends=ends, mature_deaths=mature_deaths, mature_eaten=mature_eaten,
           merges=sum(1 for tr in tracks.values() if tr["born"] == "merge"), clean=clean[:400],
           tracks=[[tid, tr["birth"], tr["end"], tr["born"], tr["endby"], round(tr["mass0"], 2), tr["parents"]] for tid, tr in tracks.items()],
           events=[[e["t"], e["parent"], e["kids"], round(e["pmass"], 2)] for e in events],
           series_cols=["t", "prey_bodies", "pred_bodies", "prey_mass", "pred_mass", "n_mean"], series=series)
json.dump(res, open(out + ".json", "w"))
if int(opt.get("save", 0)):  # raw prey frames and track->label map for strips (scratch only, not published)
    np.savez_compressed(out + "_frames.npz", prey=np.array(crops), )
    json.dump({str(k): v["frames"] for k, v in tracks.items()}, open(out + "_frames.json", "w"))
print(json.dumps({k: v for k, v in res.items() if k not in ("clean", "series", "tracks", "events")}))

# strip: up to 6 random clean births at the deepest generation: parent before, daughters after
rng = np.random.default_rng(0)
deep = [c for c in clean if c["gen"] == maxgen] or clean
pick = [deep[i] for i in rng.choice(len(deep), min(6, len(deep)), replace=False)] if deep else []
tiles = []
R = 18
for c in pick:
    pt = tracks[c["parent"]]
    fpar, jp = pt["frames"][-1]
    labp, _ = label(crops[fpar].astype(np.float32))
    yy, xx = np.nonzero(labp == jp)
    cy, cx = int(np.median(yy)), int(np.median(xx))
    row = []
    for df in (0, 1, 10, 25, 50):
        f = min(fpar + df, len(crops) - 1)
        img = np.roll(np.roll(crops[f].astype(np.float32), H // 2 - cy, 0), Wd // 2 - cx, 1)
        row.append(img[H // 2 - R:H // 2 + R, Wd // 2 - R:Wd // 2 + R])
    tiles.append(np.concatenate(row, 1))
if tiles:
    a = np.concatenate(tiles, 0)
    a = (np.clip(a / 1.0, 0, 1) * 255).astype(np.uint8)
    Image.fromarray(a).resize((a.shape[1] * 3, a.shape[0] * 3), Image.NEAREST).save(out + "_strip.png")
