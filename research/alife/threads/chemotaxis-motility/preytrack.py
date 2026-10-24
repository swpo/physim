"""Prey-only, merge-aware lineage ledger for evopursuit (answers the committee's r2 audit).

Runs the world, labels PREY bodies (A+B, channels 0-1) every `every` time units and links them by
overlap of 2-px-dilated masks. Generation rule (strict, "largest parent"):
  - clean fission (lone parent: no merge in its lineage for >= quiet; >= 2 daughters surviving >= surv)
    gives each surviving daughter gen(parent) + 1;
  - a merge product inherits the generation of its LARGEST parent (by prey mass), not the max;
  - any other new track (unclean split, nucleation) inherits its largest parent's generation, or 0.
Kinds: a body is B if its B fraction > 0.8, A if < 0.2, else mixed (fraction measured on the
track's first frame for births, last frame for deaths).
Ledger per kind: clean-fission births (by parent kind), off-kind daughters, deaths (track vanishes
without a successor; eaten and toxin deaths are not separated), and mutation CONVERSIONS taken from
the world's own mutation log (an event that flips its body's majority allele).
Strips: up to 4 clean B births drawn at random from those with parent gen >= (max B-parent gen - 1).

usage: python preytrack.py world.py out_prefix seed T [every=2] [quiet=40] [surv=40] [k=v ...]
"""
import json
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, ".")
from labkit.world import load_world  # noqa: E402

args = [a for a in sys.argv[1:] if "=" not in a]
kv = dict(a.split("=") for a in sys.argv[1:] if "=" in a)
opt = {k: float(kv.pop(k)) for k in ("every", "quiet", "surv", "size") if k in kv}
W = load_world(args[0])
for k, v in kv.items():
    W.P[k] = float(v)
out, seed, T = args[1], int(args[2]), float(args[3])
every, quiet, surv = opt.get("every", 2.0), opt.get("quiet", 40.0), opt.get("surv", 40.0)
H, Wd = W.META["size"] if "size" not in opt else (int(opt["size"]),) * 2
dt = W.P["dt"]
s = W.init(seed, (H, Wd))
nsub = int(round(every / dt))
THR = 0.35


def label(m):
    lab, n = ndimage.label(m > THR)
    for a, b in ((lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])):
        for x, y in zip(a, b):
            if x and y and x != y:
                lab[lab == y] = x
    ids = [i for i in np.unique(lab) if i]
    areas = ndimage.sum(np.ones_like(m), lab, ids) if ids else []
    keep = [i for i, a in zip(ids, areas) if a >= 12]
    o = np.zeros_like(lab)
    for j, i in enumerate(keep, 1):
        o[lab == i] = j
    return o, len(keep)


frames, prey_src, fb_src = [], [], []
t = 0.0
while t <= T + 1e-9:
    F = np.asarray(W.fields(s), np.float32)
    prey = F[0] + F[1]
    lab, n = label(prey)
    if n:
        ids = range(1, n + 1)
        mass = np.array(ndimage.sum(prey, lab, ids))
        fb = np.array(ndimage.sum(F[1], lab, ids)) / np.maximum(mass, 1e-9)
    else:
        mass, fb = np.zeros(0), np.zeros(0)
    frames.append((t, lab, n, mass, fb))
    prey_src.append(prey.astype(np.float16))
    fb_src.append(F[1].astype(np.float16))
    for _ in range(nsub):
        s = W.step(s)
    t += every

tracks, cur, nid, events, maps = {}, {}, 0, [], []
prev = None
for fi, (tt, lab, n, mass, fb) in enumerate(frames):
    if prev is None:
        for j in range(1, n + 1):
            tracks[nid] = dict(birth=tt, end=tt, parents=[], born_by="init", fb0=fb[j - 1], fb1=fb[j - 1],
                               m0=mass[j - 1], m1=mass[j - 1], successor=False)
            cur[j] = nid
            nid += 1
        maps.append(dict(cur))
        prev = (lab, n, mass)
        continue
    pd = ndimage.grey_dilation(prev[0], footprint=np.ones((5, 5)), mode="wrap")
    links = {j: [u for u in np.unique(pd[lab == j]) if u] for j in range(1, n + 1)}
    children_of = {}
    for j, ps in links.items():
        for p in ps:
            children_of.setdefault(p, []).append(j)
    new = {}
    for j in range(1, n + 1):
        ps = [p for p in links[j] if p in cur]
        if len(ps) == 1 and len(children_of.get(ps[0], [])) == 1:
            tid = cur[ps[0]]
            new[j] = tid
            tracks[tid].update(end=tt, fb1=fb[j - 1], m1=mass[j - 1])
            continue
        pids = [cur[p] for p in ps]
        pm = [prev[2][p - 1] for p in ps]
        born_by = "nucleation" if not ps else ("merge" if len(ps) > 1 else "split")
        tracks[nid] = dict(birth=tt, end=tt, parents=pids, born_by=born_by, fb0=fb[j - 1], fb1=fb[j - 1],
                           m0=mass[j - 1], m1=mass[j - 1], successor=False,
                           largest=pids[int(np.argmax(pm))] if pids else None)
        for q in pids:
            tracks[q]["successor"] = True
        new[j] = nid
        nid += 1
    for p, ch in children_of.items():
        if len(ch) >= 2 and p in cur:
            events.append((tt, cur[p], [new[c] for c in ch]))
    cur = new
    maps.append(dict(new))
    prev = (lab, n, mass)


def lone_age(tid, tt):
    tr = tracks[tid]
    if tr["born_by"] == "merge":
        return tt - tr["birth"]
    if tr["born_by"] == "split" and tr["parents"]:
        return lone_age(tr["parents"][0], tt)
    return tt - tr["birth"] if tr["born_by"] == "nucleation" else tt


clean = []
for tt, p, ch in events:
    lived = [c for c in ch if tracks[c]["end"] - tracks[c]["birth"] >= surv]
    if len(lived) >= 2 and lone_age(p, tt) >= quiet:
        clean.append((tt, p, lived))
clean_parent = {c: p for tt, p, ch in clean for c in ch}
gen = {}
for tid in sorted(tracks):
    tr = tracks[tid]
    if tid in clean_parent:
        gen[tid] = gen[clean_parent[tid]] + 1
    elif tr.get("largest") is not None:
        gen[tid] = gen[tr["largest"]]
    else:
        gen[tid] = 0


def kind(f):
    return "B" if f > 0.8 else ("A" if f < 0.2 else "mix")


births = {"A": 0, "B": 0, "mix": 0}
offkind = 0
bbirths = []
for tt, p, ch in clean:
    pk = kind(tracks[p]["fb1"])
    births[pk] += len(ch)
    for c in ch:
        if pk != "mix" and kind(tracks[c]["fb0"]) != pk:
            offkind += 1
    if pk == "B":
        bbirths.append((tt, p, ch))
deaths = {"A": 0, "B": 0, "mix": 0}
for tid, tr in tracks.items():
    if not tr["successor"] and tr["end"] < T - every:
        deaths[kind(tr["fb1"])] += 1
muts = getattr(W, "ledger", lambda s: [])(s)
conv_AB = sum(1 for m in muts if len(m) >= 6 and m[4] < 0.5 <= m[5])
conv_BA = sum(1 for m in muts if len(m) >= 6 and m[4] >= 0.5 > m[5])
res = dict(world=W.META["name"], seed=seed, T=T, overrides=kv, every=every, quiet=quiet, surv=surv,
           clean_fissions=len(clean), births_by_parent_kind=births, offkind_daughters=offkind,
           deaths_by_kind=deaths, mutation_events=len(muts), conversions_A_to_B=conv_AB, conversions_B_to_A=conv_BA,
           max_generation=max(gen.values()) if gen else 0,
           max_generation_B_parent=max([gen[p] for _, p, _ in bbirths], default=-1),
           B_births_by_parent_gen=np.bincount([gen[p] for _, p, _ in bbirths]).tolist() if bbirths else [],
           mutations=muts)
json.dump(res, open(out + ".json", "w"), indent=1, default=float)
print(f"{out}: clean fissions {len(clean)}; births by parent kind {births}; off-kind daughters {offkind}; "
      f"deaths {deaths}; mutation events {len(muts)}, conversions A->B {conv_AB}, B->A {conv_BA}; "
      f"max gen {res['max_generation']}, B births by parent gen {res['B_births_by_parent_gen']}")

rng = np.random.default_rng(seed)
if bbirths:
    gmax = max(gen[p] for _, p, _ in bbirths)
    pool = [b for b in bbirths if gen[b[1]] >= gmax - 1]
    pick = [pool[i] for i in rng.choice(len(pool), min(4, len(pool)), replace=False)]
    rows = []
    for tt, p, ch in pick:
        fi = int(round(tt / every))
        lab = frames[fi][1]
        labs = [j for j, tid in maps[fi].items() if tid in ch]
        yx = np.argwhere(np.isin(lab, labs))
        ang = 2 * np.pi * yx / np.array([H, Wd])
        c = (np.angle(np.exp(1j * ang).mean(0)) / (2 * np.pi) * np.array([H, Wd])) % np.array([H, Wd])
        tiles = []
        for k in range(-10, 16, 3):
            g = min(max(fi + k, 0), len(frames) - 1)
            pr = prey_src[g].astype(np.float32)
            b = fb_src[g].astype(np.float32)
            rgb = np.stack([b, 0.6 * pr, pr - b], -1) / max(pr.max(), 1e-9)   # B orange-ish, A cyan-ish
            cr = np.roll(np.roll(rgb, H // 2 - int(c[0]), 0), Wd // 2 - int(c[1]), 1)[H // 2 - 30:H // 2 + 30, Wd // 2 - 30:Wd // 2 + 30]
            tiles.append(np.pad(cr, ((1, 1), (1, 1), (0, 0)), constant_values=1))
        rows.append(np.concatenate(tiles, 1))
    img = np.clip(np.concatenate(rows, 0), 0, 1)
    Image.fromarray((img * 255).astype(np.uint8)).resize((img.shape[1] * 2, img.shape[0] * 2)).save(out + "_Bbirths.png")
