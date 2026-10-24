"""Dense tracker for clean fission of moving bodies (labkit samples too sparsely and cannot
tell division from collision debris).

Runs a world, samples the matter field every `every` time units, links bodies by overlap
(each body is dilated by 2 px so a moving body overlaps its next position), and classifies
split events. A split is CLEAN when
  - the parent track had no merge for >= `quiet` time before the split (it was a lone body), and
  - both children survive >= `surv` time without merging back into each other.
It also keeps a lineage (generation = number of clean fissions in the ancestry) and saves a crop
strip of the first clean fissions for visual checking.

usage: python fission.py world.py out_prefix seed T [every=2] [quiet=40] [surv=40] [k=v ...]
       k=v entries override world.P (screening only), e.g. g=0.2
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
opt = {k: float(kv.pop(k)) for k in ("every", "quiet", "surv", "thr", "size", "strict") if k in kv}
STRICT = bool(opt.get("strict", 1))
W = load_world(args[0])
for k, v in kv.items():
    W.P[k] = float(v)
out, seed, T = args[1], int(args[2]), float(args[3])
every, quiet, surv = opt.get("every", 2.0), opt.get("quiet", 40.0), opt.get("surv", 40.0)
thr = opt.get("thr", 0.35)
H, Wd = W.META["size"] if "size" not in opt else (int(opt["size"]),) * 2
dt = W.P["dt"]
s = W.init(seed, (H, Wd))
nsub = int(round(every / dt))
st = ndimage.generate_binary_structure(2, 1)


def matter(s):
    F = np.asarray(W.fields(s), np.float32)
    if hasattr(W, "matter"):
        return W.matter(F)
    idx = W.META["matter"]
    return F[list(idx)].sum(0) if idx is not None else F.sum(0)


def label(m):
    # periodic labelling: label a 2x2 tiled copy and fold back is overkill; merge across edges instead
    lab, n = ndimage.label(m > thr)
    for a, b in ((lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])):
        for x, y in zip(a, b):
            if x and y and x != y:
                lab[lab == y] = x
    ids = [i for i in np.unique(lab) if i]
    areas = ndimage.sum(np.ones_like(m), lab, ids) if ids else []
    keep = [i for i, a in zip(ids, areas) if a >= 12]
    out = np.zeros_like(lab)
    for j, i in enumerate(keep, 1):
        out[lab == i] = j
    return out, len(keep)


frames = []          # (t, lab, n)
crops_src = []       # keep matter for crop strips (every frame, float16)
allele_src = []      # B channel per frame, for heritable worlds
t = 0.0
while t <= T + 1e-9:
    m = matter(s)
    lab, n = label(m)
    frames.append((t, lab, n))
    crops_src.append(m.astype(np.float16))
    if "B" in (W.META["channels"] or []):
        Fx = np.asarray(W.fields(s), np.float32)
        allele_src.append(Fx[1].astype(np.float16))
    for _ in range(nsub):
        s = W.step(s)
    t += every

# --- link by overlap of dilated masks
tracks = {}          # id -> dict(birth, end, parents, kind)
cur = {}             # label in previous frame -> track id
nid = 0
events = []          # (t, kind, parents, children)
prev_lab = None
maps = []            # per frame: label -> track id
for fi, (tt, lab, n) in enumerate(frames):
    if prev_lab is None:
        for j in range(1, n + 1):
            tracks[nid] = {"birth": tt, "end": tt, "parents": [], "born_by": "init", "last_merge": -1e9}
            cur[j] = nid
            nid += 1
        prev_lab = lab
        maps.append(dict(cur))
        continue
    pd = ndimage.grey_dilation(prev_lab, footprint=np.ones((5, 5)), mode="wrap")
    links = {}
    for j in range(1, n + 1):
        under = np.unique(pd[lab == j])
        links[j] = [u for u in under if u]
    children_of = {}
    for j, ps in links.items():
        for p in ps:
            children_of.setdefault(p, []).append(j)
    new = {}
    for j in range(1, n + 1):
        ps = [cur[p] for p in links[j] if p in cur]
        if len(ps) == 1 and len(children_of.get(links[j][0], [])) == 1:
            new[j] = ps[0]
            tracks[ps[0]]["end"] = tt
            continue
        # birth of a new track: by split (one parent, several children), merge, or nucleation
        parea = np.bincount(prev_lab.ravel(), minlength=prev_lab.max() + 1)
        big = [p for p in links[j] if p in cur]
        tracks[nid] = {"birth": tt, "end": tt, "parents": ps, "last_merge": -1e9,
                       "largest": cur[max(big, key=lambda p: parea[p])] if big else None}
        if len(ps) == 0:
            tracks[nid]["born_by"] = "nucleation"
        elif len(ps) > 1:
            tracks[nid]["born_by"] = "merge"
            tracks[nid]["last_merge"] = tt
        else:
            tracks[nid]["born_by"] = "split"
        new[j] = nid
        nid += 1
    # record split events (parent label with >= 2 children)
    for p, ch in children_of.items():
        if len(ch) >= 2 and p in cur:
            events.append((tt, cur[p], [new[c] for c in ch]))
    cur = new
    maps.append(dict(new))
    prev_lab = lab


def lone_age(tid, tt):
    """time since the track's lineage last merged (follows split parents back)."""
    tr = tracks[tid]
    if tr["born_by"] == "merge":
        return tt - tr["birth"]
    if tr["born_by"] == "split" and tr["parents"]:
        return lone_age(tr["parents"][0], tt)
    return tt - tr["birth"] if tr["born_by"] == "nucleation" else tt


clean = []
for tt, p, ch in events:
    lived = [tracks[c]["end"] - tracks[c]["birth"] >= surv for c in ch]
    if sum(lived) >= 2 and lone_age(p, tt) >= quiet:
        clean.append((tt, p, [c for c, l in zip(ch, lived) if l]))
clean_parent = {c: p for tt, p, ch in clean for c in ch}
gen = {}
for tid in sorted(tracks):          # track ids increase with birth time, so parents come first
    tr = tracks[tid]
    if tid in clean_parent:
        gen[tid] = gen.get(clean_parent[tid], 0) + 1
    elif tr["parents"]:
        # strict rule (committee r2): inherit the LARGEST parent's generation, not the max over parents
        gen[tid] = gen.get(tr.get("largest"), 0) if STRICT else max(gen.get(q, 0) for q in tr["parents"])
    else:
        gen[tid] = 0
ncomp = [f[2] for f in frames]
res = {"world": W.META["name"], "seed": seed, "T": T, "overrides": kv, "every": every, "quiet": quiet, "surv": surv,
       "splits_all": len(events), "clean_fissions": len(clean), "max_generation": max(gen.values()) if gen else 0,
       "bodies_mean_late": float(np.mean(ncomp[len(ncomp) // 2:])), "clean": [(round(a, 1), b, c) for a, b, c in clean]}
# allele composition of parent (frame before split) and children (10 t after split)
if allele_src:
    def bfrac(fi, tid):
        lab = frames[fi][1]
        js = [j for j, t_ in maps[fi].items() if t_ == tid]
        if not js:
            return None
        msk = np.isin(lab, js)
        b = allele_src[fi].astype(np.float32)[msk].sum()
        return float(b / max(crops_src[fi].astype(np.float32)[msk].sum(), 1e-9))
    comp = []
    for tt, p, ch in clean:
        fi = int(round(tt / every))
        fc = min(fi + int(10 / every), len(frames) - 1)
        comp.append({"t": tt, "parent_B": bfrac(fi - 1, p), "children_B": [bfrac(fc, c) for c in ch]})
    res_comp = comp
else:
    res_comp = []
# body sizes: parent mass 2 t before the split, each surviving child's mass 10 t after
def bmass(fi, tid):
    lab = frames[fi][1]
    js = [j for j, t_ in maps[fi].items() if t_ == tid]
    if not js:
        return None
    return float(crops_src[fi].astype(np.float32)[np.isin(lab, js)].sum())


sizes = []
for tt, p, ch in clean:
    fi = int(round(tt / every))
    fc = min(fi + int(10 / every), len(frames) - 1)
    pm = bmass(fi - 1, p)
    cm = [bmass(fc, c) for c in ch]
    sizes.append({"t": tt, "parent": pm, "children": cm})
res_sizes = sizes
# clean fissions per generation of the dividing parent
res["fissions_by_parent_gen"] = np.bincount([gen.get(p, 0) for tt, p, ch in clean]).tolist() if clean else []
res["composition"] = res_comp
res["sizes"] = res_sizes
rat = [c / max(sum(x for x in d["children"] if x), 1e-9) for d in res_sizes for c in d["children"] if c]
res["daughter_share_of_pair"] = rat
json.dump(res, open(out + ".json", "w"), indent=1, default=int)
print(f"{out}: splits {len(events)}, clean fissions {len(clean)}, max generation {res['max_generation']}, "
      f"bodies late {res['bodies_mean_late']:.1f}, fissions by parent generation {res['fissions_by_parent_gen']}")

# crop strips of up to 4 clean fissions: 8 tiles from -20 t to +30 t around the split
rows = []
for tt, p, ch in clean[:4]:
    fi = int(round(tt / every))
    lab = frames[fi][1]
    labs = [j for j, tid in maps[fi].items() if tid in ch]
    yx = np.argwhere(np.isin(lab, labs))
    # periodic mean position
    ang = 2 * np.pi * yx / np.array([H, Wd])
    c = (np.angle(np.exp(1j * ang).mean(0)) / (2 * np.pi) * np.array([H, Wd])) % np.array([H, Wd])
    tiles = []
    for k in range(-10, 16, 3):
        g = min(max(fi + k, 0), len(frames) - 1)
        m = crops_src[g].astype(np.float32)
        cr = np.roll(np.roll(m, H // 2 - int(c[0]), 0), Wd // 2 - int(c[1]), 1)[H // 2 - 30:H // 2 + 30, Wd // 2 - 30:Wd // 2 + 30]
        tiles.append(np.pad(cr / max(m.max(), 1e-9), 1, constant_values=1))
    rows.append(np.concatenate(tiles, 1))
if rows:
    img = np.clip(np.concatenate(rows, 0), 0, 1)
    Image.fromarray((img * 255).astype(np.uint8)).resize((img.shape[1] * 2, img.shape[0] * 2)).save(out + "_strip.png")
