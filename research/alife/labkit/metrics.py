"""Measurements for evidence packs: segmentation, enclosures, topology, tracking, lineage.

Everything is periodic unless stated. Definitions are deliberately simple and stated
so judges know exactly what a number means:

- matter field: sum of the world's matter channels, divided by one global robust
  maximum for the whole run (99.9th percentile), so thresholds are fixed in time.
- component: 4-connected periodic region of matter > threshold with area >= min_area.
- hole / enclosure: a connected low-matter region that touches exactly ONE component,
  is >= min_hole pixels, and is not the largest low region (the background).
- track: a component followed through recorded frames by pixel overlap (centroid
  fallback for fast movers). A split is one component becoming >= 2 significant
  components; a merge is the reverse.
- persistent split: a split of a stable parent (>= K/3 frames) into >= 2 stable children
  (each >= K/3 frames as a single component) whose split-only lineages survive >= K
  frames (K = 10% of the run, min 5). Lineages do not continue through merges.
- generation: number of persistent splits on the ancestry path of a track.
- persistent homology: superlevel filtration of a normalized field (gudhi periodic
  cubical complex). H0 = blobs, H1 = loops (enclosed low regions); counts are of
  finite features with persistence above tau (fraction of the field range).
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage


# ------------------------------------------------------------------ segmentation
def periodic_label(mask, periodic=True):
    """4-connected labels with wrap-around merging. Returns (labels int32, n)."""
    lab, n = ndimage.label(mask)
    if n == 0 or not periodic:
        return lab.astype(np.int32), int(n)
    pairs = []
    for a, b in ((lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])):
        m = (a > 0) & (b > 0)
        if m.any():
            pairs.append(np.stack([a[m], b[m]], 1))
    if not pairs:
        return lab.astype(np.int32), int(n)
    pairs = np.unique(np.concatenate(pairs), axis=0)
    parent = np.arange(n + 1)

    def find(i):
        root = i
        while parent[root] != root:
            root = parent[root]
        while parent[i] != root:
            parent[i], i = root, parent[i]
        return root

    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    roots = np.array([find(i) for i in range(n + 1)])
    _, inv = np.unique(roots, return_inverse=True)
    return inv[lab].astype(np.int32), int(inv.max())


def drop_small(lab, n, min_area):
    """Remove components smaller than min_area and relabel consecutively."""
    if n == 0:
        return lab, 0
    areas = np.bincount(lab.ravel(), minlength=n + 1)
    keep = areas >= min_area
    keep[0] = False
    remap = np.zeros(n + 1, np.int32)
    remap[keep] = np.arange(1, keep.sum() + 1)
    return remap[lab], int(keep.sum())


def circ_centroids(lab, n, weights=None):
    """Periodic (circular-mean) centroids of labels 1..n. Returns (cy, cx) arrays."""
    H, W = lab.shape
    if n == 0:
        return np.zeros(0), np.zeros(0)
    w = np.ones(lab.shape) if weights is None else weights
    flat = lab.ravel()
    out = []
    for size, axis in ((H, 0), (W, 1)):
        ang = 2 * np.pi * np.indices(lab.shape)[axis] / size
        c = np.bincount(flat, weights=(w * np.cos(ang)).ravel(), minlength=n + 1)[1:]
        s = np.bincount(flat, weights=(w * np.sin(ang)).ravel(), minlength=n + 1)[1:]
        out.append((np.arctan2(s, c) % (2 * np.pi)) * size / (2 * np.pi))
    return out[0], out[1]


def segment(m, thr, min_area=6, periodic=True):
    """Components of m > thr. Returns dict with labels and per-component arrays."""
    lab, n = periodic_label(m > thr, periodic)
    lab, n = drop_small(lab, n, min_area)
    area = np.bincount(lab.ravel(), minlength=n + 1)[1:].astype(float)
    mass = np.bincount(lab.ravel(), weights=m.ravel(), minlength=n + 1)[1:]
    cy, cx = circ_centroids(lab, n, m)
    return {"lab": lab, "n": n, "area": area, "mass": mass, "cy": cy, "cx": cx}


def holes(lab, n, min_hole=4, max_frac=0.25, periodic=True):
    """Enclosed low regions per component. Returns (n_holes[n], hole_area[n])."""
    nh = np.zeros(n, int)
    ha = np.zeros(n, float)
    if n == 0:
        return nh, ha
    comp, nc = periodic_label(lab == 0, periodic)
    if nc == 0:
        return nh, ha
    areas = np.bincount(comp.ravel(), minlength=nc + 1)
    areas[0] = 0
    big = int(areas.argmax())
    pairs = []
    for sh in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        l2 = np.roll(lab, sh, (0, 1))
        msk = (comp > 0) & (l2 > 0)
        if msk.any():
            pairs.append(np.stack([comp[msk], l2[msk]], 1))
    if not pairs:
        return nh, ha
    pairs = np.unique(np.concatenate(pairs), axis=0)
    cnt = np.bincount(pairs[:, 0], minlength=nc + 1)
    owner = np.zeros(nc + 1, int)
    owner[pairs[:, 0]] = pairs[:, 1]
    idx = np.arange(nc + 1)
    is_hole = (cnt == 1) & (areas >= min_hole) & (areas < max_frac * lab.size) & (idx != big)
    if is_hole.any():
        nh += np.bincount(owner[is_hole] - 1, minlength=n)[:n]
        ha += np.bincount(owner[is_hole] - 1, weights=areas[is_hole], minlength=n)[:n]
    return nh, ha


def overlaps(labA, nA, labB, nB):
    """Pixel overlap counts between components of two label images (0-based indices)."""
    m = (labA > 0) & (labB > 0)
    if not m.any():
        return np.zeros(0, int), np.zeros(0, int), np.zeros(0, int)
    codes = labA[m].astype(np.int64) * (nB + 1) + labB[m]
    u, c = np.unique(codes, return_counts=True)
    return (u // (nB + 1)) - 1, (u % (nB + 1)) - 1, c


# ------------------------------------------------------------------ topology
def persistence_counts(f, taus=(0.1, 0.25, 0.5), periodic=True):
    """Counts of H0 / H1 features of the superlevel filtration of f (normalized to [0, 1])."""
    import gudhi

    lo, hi = float(f.min()), float(f.max())
    if hi - lo < 1e-12:
        return {"H0": [0] * len(taus), "H1": [0] * len(taus)}
    g = (f - lo) / (hi - lo)
    if periodic:
        cc = gudhi.PeriodicCubicalComplex(top_dimensional_cells=-g, periodic_dimensions=[True, True])
    else:
        cc = gudhi.CubicalComplex(top_dimensional_cells=-g)
    cc.compute_persistence(homology_coeff_field=2, min_persistence=min(taus) * 0.99)
    out = {}
    for d in (0, 1):
        iv = np.asarray(cc.persistence_intervals_in_dimension(d))
        if iv.size == 0:
            out[f"H{d}"] = [0] * len(taus)
            continue
        fin = iv[np.isfinite(iv[:, 1])]
        pers = fin[:, 1] - fin[:, 0]
        counts = [int((pers > t).sum()) for t in taus]
        if d == 0:  # the essential class (global max) is a blob too
            counts = [c + 1 for c in counts]
        out[f"H{d}"] = counts
    return out


# ------------------------------------------------------------------ structure
def structure(fields_norm, mask):
    """Inside/boundary/outside organization of one component (fields normalized to ~[0,1]).

    rim = mask minus its erosion (depth ~ quarter radius); core = erosion; shell = a ring
    of the same depth just outside. Returns contrasts between mean channel vectors and
    the within-component heterogeneity (mean per-channel std).
    """
    area = mask.sum()
    if area < 9:
        return None
    r = max(1, int(round(0.25 * np.sqrt(area / np.pi))))
    core = ndimage.binary_erosion(mask, iterations=r)
    rim = mask & ~core
    shell = ndimage.binary_dilation(mask, iterations=r) & ~mask
    if core.sum() < 3 or rim.sum() < 3 or shell.sum() < 3:
        return None
    mc = fields_norm[:, core].mean(1)
    mr = fields_norm[:, rim].mean(1)
    ms = fields_norm[:, shell].mean(1)
    return {
        "rim_vs_core": float(np.linalg.norm(mr - mc)),
        "rim_vs_outside": float(np.linalg.norm(mr - ms)),
        "core_vs_outside": float(np.linalg.norm(mc - ms)),
        "heterogeneity": float(fields_norm[:, mask].std(1).mean()),
        "core_mean": [round(float(v), 3) for v in mc],
        "rim_mean": [round(float(v), 3) for v in mr],
        "outside_mean": [round(float(v), 3) for v in ms],
    }


# ------------------------------------------------------------------ tracking
def _wrap(d, L):
    return d if L is None else (d + L / 2) % L - L / 2


def track(comps, links, shape=None, periodic=True):
    """Follow components through frames.

    comps[f]: dict with arrays area, cy, cx (length n_f).
    links[f] (f >= 1): (prev_idx, next_idx, overlap_count) between frames f-1 and f.
    Returns (tracks, events).
    """
    H, W = (shape if (periodic and shape is not None) else (None, None))
    tracks, events = [], []
    owner = {}  # component index in the previous frame -> track id

    def new_track(f, i, kind, parents):
        tid = len(tracks)
        tracks.append({"id": tid, "start": f, "end": f, "birth": kind, "parents": parents,
                       "children": [], "area": [comps[f]["area"][i]],
                       "cy": [comps[f]["cy"][i]], "cx": [comps[f]["cx"][i]]})
        for p in parents:
            tracks[p]["children"].append(tid)
        return tid

    for i in range(len(comps[0]["area"])):
        owner[i] = new_track(0, i, "initial", [])

    for f in range(1, len(comps)):
        A, B = comps[f - 1], comps[f]
        nA, nB = len(A["area"]), len(B["area"])
        pi, ni, cnt = links[f]
        children = [[] for _ in range(nA)]
        parents = [[] for _ in range(nB)]
        for p, n_, c in zip(pi, ni, cnt):
            if c >= 0.1 * B["area"][n_] or c >= 0.1 * A["area"][p]:
                children[p].append(n_)
                parents[n_].append(p)
        # centroid fallback for unmatched fast movers
        free_p = [p for p in range(nA) if not children[p]]
        free_n = [n_ for n_ in range(nB) if not parents[n_]]
        if free_p and free_n:
            cand = []
            for p in free_p:
                rad = max(4.0, 1.5 * np.sqrt(A["area"][p] / np.pi) + 2)
                for n_ in free_n:
                    ratio = B["area"][n_] / max(A["area"][p], 1)
                    if 1 / 3 <= ratio <= 3:
                        d = np.hypot(_wrap(B["cy"][n_] - A["cy"][p], H), _wrap(B["cx"][n_] - A["cx"][p], W))
                        if d <= rad:
                            cand.append((d, p, n_))
            used_p, used_n = set(), set()
            for d, p, n_ in sorted(cand):
                if p not in used_p and n_ not in used_n:
                    children[p].append(n_)
                    parents[n_].append(p)
                    used_p.add(p)
                    used_n.add(n_)
        new_owner = {}
        for n_ in range(nB):
            P = parents[n_]
            if len(P) == 1 and len(children[P[0]]) == 1 and P[0] in owner:
                tid = owner[P[0]]
                t = tracks[tid]
                t["end"] = f
                t["area"].append(B["area"][n_])
                t["cy"].append(B["cy"][n_])
                t["cx"].append(B["cx"][n_])
                new_owner[n_] = tid
            else:
                kind = "nucleation" if not P else ("split" if len(P) == 1 else "merge")
                ptracks = sorted({owner[p] for p in P if p in owner})
                new_owner[n_] = new_track(f, n_, kind, ptracks)
        for p in range(nA):
            if len(children[p]) >= 2 and p in owner:
                events.append({"frame": f, "type": "split", "parent": owner[p],
                               "children": [new_owner[c] for c in children[p]]})
        for n_ in range(nB):
            if len(parents[n_]) >= 2:
                events.append({"frame": f, "type": "merge", "child": new_owner[n_],
                               "parents": [owner[p] for p in parents[n_] if p in owner]})
        owner = new_owner
    return tracks, events


def lineage_stats(tracks, events, n_frames, dt_frame, shape=None, periodic=True, K=None):
    """Lifetimes, persistent splits, generations and motility from tracks/events."""
    H, W = (shape if (periodic and shape is not None) else (None, None))
    K = K if K is not None else max(5, int(0.1 * n_frames))
    ind_min = max(3, K // 3)  # an "individual" must stay a single stable component this long

    def span(t):
        return t["end"] - t["start"] + 1

    # lineages continue only through splits; a merge ends the lineages that merged
    lin_end = {}
    for t in reversed(tracks):
        lin_end[t["id"]] = max([t["end"]] + [lin_end[c] for c in t["children"] if tracks[c]["birth"] == "split"])
    persistent_splits = []
    for e in events:
        if e["type"] != "split" or span(tracks[e["parent"]]) < ind_min:
            continue
        surv = [c for c in e["children"] if span(tracks[c]) >= ind_min and lin_end[c] - e["frame"] >= K]
        if len(surv) >= 2:
            persistent_splits.append({**e, "surviving_children": surv})
    ps_children = {c for e in persistent_splits for c in e["children"]}
    gen = {}
    for t in tracks:
        if not t["parents"]:
            gen[t["id"]] = 0
        elif t["birth"] == "split":
            gen[t["id"]] = gen[t["parents"][0]] + (1 if t["id"] in ps_children else 0)
        else:
            gen[t["id"]] = max(gen[p] for p in t["parents"])
    life = np.array([t["end"] - t["start"] + 1 for t in tracks]) if tracks else np.zeros(0)
    motion = []
    for t in tracks:
        L = len(t["cy"])
        if L < 5:
            continue
        dy = _wrap(np.diff(t["cy"]), H)
        dx = _wrap(np.diff(t["cx"]), W)
        net = float(np.hypot(dy.sum(), dx.sum()))
        path = float(np.hypot(dy, dx).sum())
        size = float(np.sqrt(np.mean(t["area"])))
        motion.append({"id": t["id"], "net": net, "path": path, "size": size,
                       "speed": net / ((L - 1) * dt_frame), "body_lengths": net / max(size, 1)})
    return {
        "K_frames": K,
        "lifetimes": life,
        "persistent_splits": persistent_splits,
        "generation": gen,
        "max_generation": max(gen.values()) if gen else 0,
        "motion": motion,
        "lineage_end": lin_end,
    }


# ------------------------------------------------------------------ particles
def particle_clusters(pos, radius, min_size=5, box=None):
    """Clusters of particles within `radius` (periodic if box given). Returns labels (-1 = none)."""
    from scipy.spatial import cKDTree

    N = len(pos)
    if box is not None:
        tree = cKDTree(np.mod(pos, box), boxsize=box)
    else:
        tree = cKDTree(pos)
    pairs = tree.query_pairs(radius, output_type="ndarray")
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components

    g = coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(N, N)) if len(pairs) else coo_matrix((N, N))
    _, lab = connected_components(g, directed=False)
    sizes = np.bincount(lab)
    keep = sizes >= min_size
    remap = -np.ones(len(sizes), int)
    remap[keep] = np.arange(keep.sum())
    return remap[lab]


def cluster_comps(pos, lab, box=None):
    n = lab.max() + 1 if lab.size and lab.max() >= 0 else 0
    area = np.bincount(lab[lab >= 0], minlength=n).astype(float)
    if n == 0:
        return {"n": 0, "area": area, "cy": np.zeros(0), "cx": np.zeros(0)}
    if box is not None:
        cs = []
        for ax, L in ((1, box[1]), (0, box[0])):
            ang = 2 * np.pi * pos[lab >= 0, ax] / L
            c = np.bincount(lab[lab >= 0], weights=np.cos(ang), minlength=n)
            s = np.bincount(lab[lab >= 0], weights=np.sin(ang), minlength=n)
            cs.append((np.arctan2(s, c) % (2 * np.pi)) * L / (2 * np.pi))
        cy, cx = cs
    else:
        cy = np.bincount(lab[lab >= 0], weights=pos[lab >= 0, 1], minlength=n) / area
        cx = np.bincount(lab[lab >= 0], weights=pos[lab >= 0, 0], minlength=n) / area
    return {"n": n, "area": area, "cy": cy, "cx": cx}


def cluster_links(labA, labB):
    m = (labA >= 0) & (labB >= 0)
    if not m.any():
        return np.zeros(0, int), np.zeros(0, int), np.zeros(0, int)
    nB = labB.max() + 1
    codes = labA[m].astype(np.int64) * nB + labB[m]
    u, c = np.unique(codes, return_counts=True)
    return u // nB, u % nB, c
