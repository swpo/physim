"""Measurements for evidence packs: segmentation, enclosures, topology, tracking, lineage,
radial boundary profiles and damage targeting.

Everything is periodic unless stated. Definitions are deliberately simple and stated
so judges know exactly what a number means:

- matter field: sum of the world's matter channels, divided by one global robust
  maximum for the whole run (99.9th percentile), so thresholds are fixed in time.
- component: 4-connected periodic region of matter > threshold with area >= min_area.
- hole / enclosure: a connected low-matter region that touches exactly ONE component,
  is >= min_hole pixels, and is not the largest low region (the background).
- track: a component followed through recorded frames by pixel overlap (centroid
  fallback for fast movers). A split is one component becoming >= 2 significant
  components; a merge is the reverse. merge/split ratio = merge events / split events
  (near 1 = reticulate genealogy: what divides mostly fuses again).
- persistent split: a split of a stable parent (>= K/3 frames) into >= 2 stable children
  (each >= K/3 frames as a single component) whose split-only lineages survive >= K
  frames after the split, AND that stay apart: surviving children whose descendants
  (through splits or merges) take part in the same merge within K frames of the split
  count as one, and >= 2 such groups must remain (sibling re-merge filter). K = 20
  recorded frames by default (absolute, independent of run length; META "lineage_k",
  CLI --lineage-k). Lineages do not continue through merges.
- generation: number of persistent splits on the ancestry path of a track.
- persistent homology: superlevel filtration of a normalized field (gudhi periodic
  cubical complex). H0 = blobs, H1 = loops (enclosed low regions); counts are of
  finite features with persistence above tau (fraction of the field range).
- radial profile: for one component, the mean of EVERY channel (fixed render
  normalization: 0..1 = the channel's 1st..99.5th percentile over the run, so it works
  for channels outside the matter set) in 25 bins of rho = r / R_eq over [0, 2.5],
  where r = periodic distance from the component's matter-weighted centroid (= the
  track centroid) and R_eq = sqrt(area / pi) of the component. Neighbouring components
  are NOT masked out. Per track: the top tracks at their middle-life render frame.
  Aggregate: mean +- std over all components with area >= 2 * min_area at up to 6
  render frames spread over the run (the initial frame excluded).
- boundary score of one channel's profile p: rho_peak = rho of the global maximum
  (in the rim band if 0.5 <= rho_peak <= 1.5); rim = max of p over 0.6 <= rho <= 1.3;
  core = mean of p over rho < 0.4; outside = mean of p over 1.6 <= rho <= 2.2 (means of
  bin means); rim/core = (rim + 0.01) / (core + 0.01), rim/outside likewise, capped at
  999 (1 = no contrast or an absent channel; ~100 = the denominator is ~0).
  MEMBRANE-LIKE = rim/core >= 1.5 AND rim/outside >= 1.5 on the aggregate profile; the
  number of individuals that pass on their own profile is reported alongside.
- damage target (--damage FRAME:FRAC[:MODE]): among components at FRAME whose track has
  existed >= K frames and whose area is within [0.5, 1.6] x the median component area,
  the most compact one (lowest aspect ratio = sqrt of the eigenvalue ratio of the pixel
  second-moment matrix, so elongating or pinching bodies are avoided); if none
  qualifies, the largest component. A = target area, R_eq = sqrt(A / pi).
  core: disk of area FRAC*A at the centroid. rim: a disk of the same area centred on
  the boundary pixel farthest from other components. half: pixels of the component
  (dilated by ~R_eq/4 so a layer just outside the threshold contour is cut too) beyond
  a line perpendicular to the same outward direction, offset from the centroid so that
  FRAC of the component's pixels are erased. Other components are never in the mask.
  Reported loss = matter lost inside the target's component mask (raw matter field just
  before minus just after the world's damage() call) / its matter before, whatever the
  hook actually erases.
- species (META "species" = {name: [channels]}): segmentation, tracking and lineage as
  above, run separately on each species' channel sum with its own robust range.
"""
from __future__ import annotations

import warnings

import numpy as np
from scipy import ndimage

LINEAGE_K = 20            # default lineage window (recorded frames) for persistent splits
RHO_EDGES = np.linspace(0.0, 2.5, 26)            # 25 radial bins in rho = r / R_eq
RHO = 0.5 * (RHO_EDGES[1:] + RHO_EDGES[:-1])     # bin centres 0.05 .. 2.45
CORE_RHO, RIM_RHO, OUT_RHO, PEAK_RHO = (0.0, 0.4), (0.6, 1.3), (1.6, 2.2), (0.5, 1.5)
RATIO_EPS, RATIO_CAP, MEMBRANE_RATIO = 0.01, 999.0, 1.5
DAMAGE_AREA_BAND = (0.5, 1.6)   # target area / median component area


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


# ------------------------------------------------------------------ radial profiles
def _quiet(fn, x, axis=None):
    """nan-aware reduction without all-nan warnings (returns nan)."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        return fn(x, axis=axis)


def radial_profile(fields_norm, cy, cx, r_eq, periodic=True):
    """Mean of each channel in the RHO bins around (cy, cx), rho = r / r_eq.

    fields_norm: (C, H, W). Returns (profile (C, nbins) with nan in empty bins, pixel counts).
    Only a window of half-size 2.5 r_eq is read (capped below half the grid when periodic).
    """
    C, H, W = fields_norm.shape
    h = int(np.ceil(RHO_EDGES[-1] * r_eq)) + 1
    if periodic:
        h = min(h, (min(H, W) - 1) // 2)
    ys = np.arange(int(round(cy)) - h, int(round(cy)) + h + 1)
    xs = np.arange(int(round(cx)) - h, int(round(cx)) + h + 1)
    if periodic:
        dy, dx = _wrap(ys - cy, H), _wrap(xs - cx, W)
        ys, xs = ys % H, xs % W
    else:
        ys, xs = ys[(ys >= 0) & (ys < H)], xs[(xs >= 0) & (xs < W)]
        dy, dx = ys - cy, xs - cx
    b = (np.hypot(dy[:, None], dx[None, :]) / max(r_eq, 1e-9) / (RHO_EDGES[1] - RHO_EDGES[0])).astype(int).ravel()
    ok = b < len(RHO)
    b = b[ok]
    cnt = np.bincount(b, minlength=len(RHO))
    win = fields_norm[:, ys[:, None], xs[None, :]].reshape(C, -1)[:, ok]
    prof = np.full((C, len(RHO)), np.nan)
    has = cnt > 0
    for c in range(C):
        prof[c, has] = np.bincount(b, weights=win[c], minlength=len(RHO))[has] / cnt[has]
    return prof, cnt


def _ratio(a, b):
    if not (np.isfinite(a) and np.isfinite(b)):
        return None
    return float(min((a + RATIO_EPS) / max(b + RATIO_EPS, 1e-12), RATIO_CAP))


def boundary_score(prof):
    """Boundary score of one channel's radial profile (length len(RHO)); None if empty."""
    prof = np.asarray(prof, float)
    if not np.isfinite(prof).any():
        return None
    band = lambda lo, hi: (RHO >= lo) & (RHO <= hi)  # noqa: E731
    k = int(np.nanargmax(prof))
    rim = float(_quiet(np.nanmax, prof[band(*RIM_RHO)])) if np.isfinite(prof[band(*RIM_RHO)]).any() else np.nan
    core = float(_quiet(np.nanmean, prof[RHO < CORE_RHO[1]]))
    out = float(_quiet(np.nanmean, prof[band(*OUT_RHO)]))
    rc, ro = _ratio(rim, core), _ratio(rim, out)
    return {"rho_peak": round(float(RHO[k]), 2), "peak_in_rim": bool(PEAK_RHO[0] <= RHO[k] <= PEAK_RHO[1]),
            "rim_max": None if np.isnan(rim) else round(rim, 4), "core_mean": None if np.isnan(core) else round(core, 4),
            "outside_mean": None if np.isnan(out) else round(out, 4),
            "rim_core": None if rc is None else round(rc, 3), "rim_outside": None if ro is None else round(ro, 3),
            "membrane_like": bool(rc is not None and ro is not None and rc >= MEMBRANE_RATIO and ro >= MEMBRANE_RATIO)}


def radial_aggregate(profiles):
    """Mean and std over individuals of (C, nbins) profiles (nan-aware)."""
    P = np.stack(profiles)
    return _quiet(np.nanmean, P, 0), _quiet(np.nanstd, P, 0)


# ------------------------------------------------------------------ damage geometry
def _erode1(m, periodic=True):
    if not periodic:
        return ndimage.binary_erosion(m)
    return m & np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)


def _dilate(m, it, periodic=True):
    if not periodic:
        return ndimage.binary_dilation(m, iterations=it) if it > 0 else m
    for _ in range(it):
        m = m | np.roll(m, 1, 0) | np.roll(m, -1, 0) | np.roll(m, 1, 1) | np.roll(m, -1, 1)
    return m


def _offsets(shape, cy, cx, periodic=True):
    H, W = shape
    dy = np.arange(H)[:, None] - cy
    dx = np.arange(W)[None, :] - cx
    if periodic:
        dy, dx = _wrap(dy, H), _wrap(dx, W)
    return dy, dx


def aspect_ratio(mask, cy, cx, periodic=True):
    """sqrt(largest / smallest eigenvalue) of the pixel second-moment matrix (1 = round)."""
    ys, xs = np.nonzero(mask)
    if len(ys) < 3:
        return float("inf")
    H, W = mask.shape
    dy, dx = ys - cy, xs - cx
    if periodic:
        dy, dx = _wrap(dy, H), _wrap(dx, W)
    ev = np.linalg.eigvalsh(np.cov(np.stack([dy, dx]), bias=True))
    return float(np.sqrt(max(ev[1], 1e-12) / max(ev[0], 1e-12)))


def choose_damage_target(seg, spans, K, periodic=True):
    """Pick the component to damage (see the module definitions).

    spans[j]: frames the track owning component j has existed. Returns (j, rule, aspect[j]).
    """
    n = seg["n"]
    if n == 0:
        return None, "no components", []
    asp = [aspect_ratio(seg["lab"] == j + 1, seg["cy"][j], seg["cx"][j], periodic) for j in range(n)]
    med = float(np.median(seg["area"]))
    cand = [j for j in range(n) if spans[j] >= K
            and DAMAGE_AREA_BAND[0] * med <= seg["area"][j] <= DAMAGE_AREA_BAND[1] * med]
    if cand:
        return min(cand, key=lambda j: asp[j]), "mature-compact", asp
    return int(np.argmax(seg["area"])), "fallback-largest", asp


def choose_comparator(seg, j, spans, K):
    """Undamaged control: the other component closest in area (log ratio), mature ones first."""
    others = [q for q in range(seg["n"]) if q != j]
    if not others:
        return None
    mature = [q for q in others if spans[q] >= K] or others
    return min(mature, key=lambda q: abs(np.log(seg["area"][q] / max(seg["area"][j], 1))))


def _outward(seg, j, periodic=True):
    """Boundary pixel of component j farthest from every other component (+ unit direction)."""
    lab = seg["lab"]
    H, W = lab.shape
    m = lab == j + 1
    by, bx = np.nonzero(m & ~_erode1(m, periodic))
    cy, cx = seg["cy"][j], seg["cx"][j]
    oy, ox = np.nonzero((lab > 0) & ~m)
    if len(oy) and len(by):
        from scipy.spatial import cKDTree

        pts = np.stack([oy, ox], 1).astype(float)
        tree = cKDTree(pts, boxsize=(H, W)) if periodic else cKDTree(pts)
        k = int(np.argmax(tree.query(np.stack([by, bx], 1).astype(float))[0]))
    elif len(by):  # no neighbours: the boundary pixel farthest along +x
        k = int(np.argmax(_wrap(bx - cx, W) if periodic else bx - cx))
    else:
        return (cy, cx), (0.0, 1.0)
    py, px = float(by[k]), float(bx[k])
    vy, vx = (_wrap(py - cy, H), _wrap(px - cx, W)) if periodic else (py - cy, px - cx)
    nrm = float(np.hypot(vy, vx)) or 1.0
    return (py, px), (vy / nrm, vx / nrm)


def damage_mask(seg, j, frac, mode="core", periodic=True):
    """Boolean mask to hand to the world's damage() hook, and a description of it."""
    lab = seg["lab"]
    m = lab == j + 1
    others = (lab > 0) & ~m
    A = float(seg["area"][j])
    r_eq = np.sqrt(A / np.pi)
    rad = float(np.sqrt(frac * A / np.pi))
    info = {"mode": mode, "frac_requested": float(frac), "radius": rad}
    if mode == "core":
        cy, cx = seg["cy"][j], seg["cx"][j]
    elif mode == "rim":
        (cy, cx), _ = _outward(seg, j, periodic)
    elif mode == "half":
        _, (ny, nx) = _outward(seg, j, periodic)
        dy, dx = _offsets(lab.shape, seg["cy"][j], seg["cx"][j], periodic)
        proj = dy * ny + dx * nx
        cut = float(np.quantile(proj[m], 1 - frac))
        region = _dilate(m, max(1, int(round(0.25 * r_eq))), periodic) & ~others
        info.update({"direction": [round(float(ny), 3), round(float(nx), 3)], "offset": round(cut, 2)})
        return region & (proj >= cut), info
    else:
        raise ValueError(f"damage mode {mode!r}: use core, rim or half")
    dy, dx = _offsets(lab.shape, cy, cx, periodic)
    info["center"] = [round(float(cy), 2), round(float(cx), 2)]
    return (dy ** 2 + dx ** 2 <= rad ** 2) & ~others, info


# ------------------------------------------------------------------ tracking
def _wrap(d, L):
    return d if L is None else (d + L / 2) % L - L / 2


def track(comps, links, shape=None, periodic=True):
    """Follow components through frames.

    comps[f]: dict with arrays area, cy, cx (length n_f).
    links[f] (f >= 1): (prev_idx, next_idx, overlap_count) between frames f-1 and f.
    Returns (tracks, events). tracks[i]["comp"][k] is the component index in frame start + k.
    """
    H, W = (shape if (periodic and shape is not None) else (None, None))
    tracks, events = [], []
    owner = {}  # component index in the previous frame -> track id

    def new_track(f, i, kind, parents):
        tid = len(tracks)
        tracks.append({"id": tid, "start": f, "end": f, "birth": kind, "parents": parents,
                       "children": [], "area": [comps[f]["area"][i]],
                       "cy": [comps[f]["cy"][i]], "cx": [comps[f]["cx"][i]], "comp": [int(i)]})
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
                t["comp"].append(int(n_))
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


def descendants(tracks, tid, fmax=None):
    """Track ids reachable from tid through children (splits AND merges), started <= fmax."""
    seen, stack = set(), [tid]
    while stack:
        i = stack.pop()
        if i in seen or (fmax is not None and tracks[i]["start"] > fmax):
            continue
        seen.add(i)
        stack.extend(tracks[i]["children"])
    return seen


def lineage_stats(tracks, events, n_frames, dt_frame, shape=None, periodic=True, K=None):
    """Lifetimes, persistent splits (with the sibling re-merge filter), generations and motility."""
    H, W = (shape if (periodic and shape is not None) else (None, None))
    K = int(K) if K is not None else LINEAGE_K
    ind_min = max(3, K // 3)  # an "individual" must stay a single stable component this long

    def span(t):
        return t["end"] - t["start"] + 1

    # lineages continue only through splits; a merge ends the lineages that merged
    lin_end = {}
    for t in reversed(tracks):
        lin_end[t["id"]] = max([t["end"]] + [lin_end[c] for c in t["children"] if tracks[c]["birth"] == "split"])
    merges_at = {}
    for e in events:
        if e["type"] == "merge":
            merges_at.setdefault(e["frame"], []).append(e)
    persistent_splits, remerged_splits = [], []
    for e in events:
        if e["type"] != "split" or span(tracks[e["parent"]]) < ind_min:
            continue
        surv = [c for c in e["children"] if span(tracks[c]) >= ind_min and lin_end[c] - e["frame"] >= K]
        if len(surv) < 2:
            continue
        # sibling re-merge filter: survivors whose descendants merge together within K are one group
        f0, f1 = e["frame"], e["frame"] + K
        owner = {}
        for k, c in enumerate(surv):
            for d in descendants(tracks, c, f1):
                owner.setdefault(d, set()).add(k)
        group = list(range(len(surv)))

        def root(k):
            while group[k] != k:
                k = group[k]
            return k
        rejoined = []
        for g in range(f0 + 1, f1 + 1):
            for m in merges_at.get(g, []):
                ks = sorted(set().union(*[owner.get(p, set()) for p in m["parents"]]))
                for k in ks[1:]:
                    a, b = root(ks[0]), root(k)
                    if a != b:
                        group[max(a, b)] = min(a, b)
                        rejoined.append({"frame": g, "children": [surv[ks[0]], surv[k]]})
        n_groups = len({root(k) for k in range(len(surv))})
        if n_groups >= 2:
            persistent_splits.append({**e, "surviving_children": surv, "groups": n_groups})
        else:
            remerged_splits.append({**e, "surviving_children": surv, "remerged": rejoined})
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
        "remerged_splits": remerged_splits,
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
