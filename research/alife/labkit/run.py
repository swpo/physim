"""Run a world and write a standard evidence pack.

    python -m labkit.run path/to/world.py --out path/to/pack --seeds 0 1 2 [--frames 200]
           [--spf N] [--size H W] [--damage FRAME:FRAC[:MODE]] [--lineage-k K] [--dt DT]
           [--no-movie] [--threshold T] [--min-area A]

Per seed, the pack contains:
    FACTS.md        judge-facing summary of every measurement, with warnings
    metrics.json    the same numbers, machine readable
    sheet.png       24 frames over the whole run, fixed colour scales, sim times
    tracks.png      biography strips of the most persistent individuals (fixed crops)
    radial.png      per-channel radial profiles vs rho = r / R_eq: thin lines = individuals,
                    thick line = aggregate (membrane test; works for non-matter channels)
    lineage.png     track lifetimes with split/merge links (replication evidence)
    timeseries.png  components, enclosures, channel totals, occupancy, events (+ species)
    damage.png      (--damage) the damaged individual and its descendants after the cut,
                    above an undamaged comparator of similar size
    movie.mp4       up to 120 recorded frames (small; commit only for promising worlds)
    particles.png   (particle worlds) the same 24 times drawn as particles
    frames.npz      raw recorded fields (git-ignored; regenerate from world + seed)
With several seeds, SUMMARY.md tabulates them.

Options:
    --damage FRAME:FRAC[:MODE]  cut a MATURE, COMPACT individual (a component with
                    everything it encloses: a membrane ring and its core are one) at
                    recorded frame FRAME, an integer (see labkit/metrics.py for the target
                    rule). MODE: core (centred disk, default), rim (disk centred on the
                    boundary, breaches a membrane) or half (half-plane cut). FRAC in (0, 1]
                    is the requested fraction of its area; FACTS reports the matter fraction
                    ACTUALLY lost, whatever the world hook does. The follow-up is segmented
                    with the range used to choose the target, so it always follows the
                    individual that was cut; FACTS warns if the main analysis has no track
                    for it.
    --lineage-k K   lineage window in recorded frames, an integer >= 1 (default META
                    "lineage_k", else 20).
    --dt DT         time per internal step for reporting, > 0 (overrides META dt; the
                    world's own numerics are untouched).
Optional META keys: "lineage_k", "radial_channels" (channels for radial.png, default all),
"species" ({name: [channels]}: separate tracking and lineage per species).
Bytecode: runs leave no __pycache__ behind, neither in labkit/ nor next to world files, so
read-only mirrors stay clean. labkit/__init__.py sets sys.dont_write_bytecode before any
other labkit module or the world is imported (`python -m` imports the package before this
file), and removes the one cache file the import system writes before that line runs
(its own). Inside mirrors, `python -B -m labkit.run ...` or PYTHONDONTWRITEBYTECODE=1
avoids even that transient write.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # already set by labkit/__init__.py; kept in case run.py is loaded another way

import argparse  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

from . import metrics as M  # noqa: E402
from . import render as R  # noqa: E402
from .world import load_world  # noqa: E402

THRESHOLDS = (0.2, 0.35, 0.5)  # relative to the robust matter range; 0.35 is primary
FIGURES = ("sheet.png", "particles.png", "tracks.png", "radial.png", "damage.png", "lineage.png", "timeseries.png",
           "movie.mp4")
DAMAGE_MODES = ("core", "rim", "half")


def _matter(W, F):
    if hasattr(W, "matter"):
        return np.asarray(W.matter(F), np.float32)
    idx = W.META["matter"]
    return (F if idx is None else F[list(idx)]).sum(0)


def _fields(W, state):
    F = np.array(W.fields(state), np.float32)  # a copy: the state may be mutated in place later
    return F[None] if F.ndim == 2 else F


def _channel_names(meta, C):
    names = list(meta.get("channels") or [])
    return [str(names[c]) if c < len(names) else f"c{c}" for c in range(C)]


def _channel_list(spec, names, C, what):
    """Channel indices from a list of indices and/or names (None = all channels)."""
    if spec is None:
        return list(range(C))
    if isinstance(spec, (str, int, np.integer)):
        spec = [spec]
    if len(spec) == 0:
        raise ValueError(f"META {what}: empty channel list (omit the key or use None for all channels)")
    out = []
    for c in spec:
        k = names.index(c) if isinstance(c, str) and c in names else c
        if not isinstance(k, (int, np.integer)) or not -C <= k < C:
            raise ValueError(f"META {what}: unknown channel {c!r} (channels {names})")
        out.append(int(k) % C)
    return out


def _species(meta, C):
    sp = meta.get("species") or {}
    names = _channel_names(meta, C)
    return {str(k): _channel_list(v, names, C, f"species[{k!r}]") for k, v in sp.items()}


def _lineage_k(meta, K=None):
    """(K, source): CLI --lineage-k > META lineage_k > labkit default. K must be an integer >= 1."""
    K, src = ((K, "--lineage-k") if K is not None else (meta["lineage_k"], "META lineage_k")
              if meta.get("lineage_k") is not None else (M.LINEAGE_K, "default"))
    if isinstance(K, bool) or not float(K).is_integer() or int(K) < 1:
        raise ValueError(f"{src} = {K!r}: the lineage window must be an integer >= 1 recorded frames")
    return int(K), src


def _check_dt(dt, src="dt"):
    """Time per internal step for reporting: a finite number > 0."""
    if isinstance(dt, bool) or not np.isfinite(float(dt)) or float(dt) <= 0:
        raise ValueError(f"{src} = {dt!r}: the time per internal step must be > 0")
    return float(dt)


def _default_min_area(H, W):
    return max(6, int(H * W / 20000))


def _normalize_matter(mat, meta, periodic, threshold=None, rng=None):
    """Robust-range normalization (+ light blur) of a (T, H, W) matter stack; returns mn, thr, lo, hi.

    rng: (lo, hi) to reuse a range computed elsewhere (default: this stack's 1st..99.9th percentile)."""
    T = len(mat)
    if rng is not None:
        lo, hi = (float(v) for v in rng)
    else:
        lo = float(np.percentile(mat[:: max(1, T // 40)], 1))
        hi = float(np.percentile(mat[:: max(1, T // 40)], 99.9))
    span = max(hi - lo, 1e-12)
    mn = (mat - lo) / span
    sm = float(meta.get("smooth", 1.0))  # light blur so thin filaments do not flicker as debris
    if sm > 0:
        from scipy import ndimage
        mn = np.stack([ndimage.gaussian_filter(x, sm, mode="wrap" if periodic else "nearest") for x in mn])
    thr = THRESHOLDS[1] if threshold is None else (threshold - lo) / span
    return mn, thr, lo, hi


def _segment_frames(mn, thr, min_area, periodic, keep_labels=True):
    """Segment every frame and link consecutive frames by overlap (labels of the last frame kept)."""
    comps, links, prev = [], [None], None
    for f in range(len(mn)):
        seg = M.segment(mn[f], thr, min_area, periodic)
        if prev is not None:
            links.append(M.overlaps(prev["lab"], prev["n"], seg["lab"], seg["n"]))
            if not keep_labels:
                del prev["lab"]
        comps.append(seg)
        prev = seg
    return comps, links


# ------------------------------------------------------------------ simulation
def _apply_damage(W, state, F, rec, damage, K, seg_opts):
    """Pick a mature compact target, cut it, call the world's hook and MEASURE the loss."""
    frame, frac, mode = damage
    info = {"frame": int(frame), "mode": mode, "frac_requested": float(frac), "K_frames": int(K)}
    if not hasattr(W, "damage"):
        info["error"] = "world has no damage(state, mask) hook: nothing was erased"
        return state, info, None
    periodic, threshold, min_area = seg_opts
    m0 = _matter(W, F)
    mn, thr, lo, hi = _normalize_matter(np.stack(rec["matter"] + [m0]), W.META, periodic, threshold)
    H, Wd = m0.shape
    min_area = min_area or _default_min_area(H, Wd)
    comps, links = _segment_frames(mn, thr, min_area, periodic, keep_labels=False)
    tracks, _ = M.track(comps, links, (H, Wd), periodic)
    f, seg = len(comps) - 1, comps[-1]
    spans = np.zeros(seg["n"], int)
    for t in tracks:
        if t["end"] == f:
            spans[t["comp"][-1]] = f - t["start"] + 1
    # individuals = outermost components with everything they enclose (a ring and its core are one cell)
    inds = M.individuals(seg, mn[-1], periodic)
    ispan = [int(max(spans[c] for c in d["members"])) for d in inds]
    i, rule, asp = M.choose_damage_target(inds, ispan, K, periodic)
    info.update({"seg_range": [lo, hi], "seg_threshold_rel": float(thr), "seg_min_area": int(min_area)})
    if i is None:
        info["error"] = "no components at the damage frame: nothing was erased"
        return state, info, None
    q = M.choose_comparator(inds, i, ispan, K, periodic)
    ind = inds[i]
    mask, minfo = M.damage_mask(seg["lab"], ind, frac, mode, periodic)
    target = ind["mask"]  # the filled individual: loss is measured here
    state = W.damage(state, mask)
    m1 = _matter(W, _fields(W, state))
    lost = m0 - m1
    gone = np.clip(lost, 0, None)  # matter that disappeared (gains elsewhere do not cancel it)
    before = float(m0[target].sum())
    fin = lambda v: round(float(v), 3) if np.isfinite(v) else None  # noqa: E731
    info.update({
        "rule": rule, "track_age_frames": ispan[i],
        "individual_area": float(ind["area"]), "component_area": float(ind["comp_area"]),
        "enclosed_px": int(ind["enclosed_px"]), "member_components": len(ind["members"]),
        "member_areas": [float(seg["area"][c]) for c in ind["members"]],
        "median_area": float(np.median([d["area"] for d in inds])), "n_individuals": len(inds),
        "n_components": int(seg["n"]), "n_ring_individuals": int(sum(d["ring"] for d in inds)),
        "aspect": fin(asp[i]), "cy": float(ind["cy"]), "cx": float(ind["cx"]),
        **minfo,
        "mask_px": int(mask.sum()), "mask_px_in_component": int((mask & target).sum()),
        # MEASURED, whatever the hook did with the mask:
        "erased_frac": float(lost[target].sum() / before) if before > 0 else None,
        "erased_px": int(((lost > 0.5 * m0) & target).sum()),  # individual px that lost > half their matter
        "lost_outside_frac": float(lost[~target].sum() / before) if before > 0 else None,
        "lost_under_mask_share": float(gone[mask].sum() / gone.sum()) if gone.sum() > 0 else None,
        "gained_frac": float(np.clip(-lost, 0, None).sum() / before) if before > 0 else None,
        "comparator_area": float(inds[q]["area"]) if q is not None else None,
        "comparator_cy": float(inds[q]["cy"]) if q is not None else None,
        "comparator_cx": float(inds[q]["cx"]) if q is not None else None,
        "comparator_age_frames": ispan[q] if q is not None else None,
    })
    arrays = {"pre": F.astype(np.float16), "pre_matter": m0, "mask": mask, "target": target,
              "comparator": inds[q]["mask"] if q is not None else None}
    return state, info, arrays


def simulate(W, seed, frames, spf, size, render_max=120, damage=None, log=print, K=None, periodic=True,
             threshold=None, min_area=None):
    """Advance the world, keeping every matter field and up to render_max full frames."""
    if damage is not None and len(damage) == 2:
        damage = (damage[0], damage[1], "core")
    if damage is not None:
        _check_damage(*damage)
    K = _lineage_k(W.META, K)[0]
    state = W.init(seed, size)
    render_idx = set(np.unique(np.linspace(0, frames, min(render_max, frames + 1)).round().astype(int)).tolist())
    if damage and 0 <= damage[0] <= frames:
        render_idx.add(int(damage[0]))  # the frame just after the cut is always rendered
    rec = {"matter": [], "render": [], "render_f": [], "particles": [], "totals": [], "status": "ok",
           "damage": None, "damage_arrays": None, "species": {}}
    species = None
    t0 = time.time()
    for f in range(frames + 1):
        if f > 0:
            for _ in range(spf):
                state = W.step(state)
        if damage and f == damage[0]:
            state, rec["damage"], rec["damage_arrays"] = _apply_damage(
                W, state, _fields(W, state), rec, damage, K, (periodic, threshold, min_area))
        F = _fields(W, state)
        if not np.isfinite(F).all():
            rec["status"] = f"non-finite fields at frame {f}"
            log(rec["status"])
            break
        if species is None:  # validate the optional META channel lists at frame 0, not after the run
            species = _species(W.META, F.shape[0])
            _channel_list(W.META.get("radial_channels"), _channel_names(W.META, F.shape[0]), F.shape[0], "radial_channels")
            rec["species"] = {k: [] for k in species}
        for k, idx in species.items():
            rec["species"][k].append(F[idx].sum(0))
        rec["matter"].append(_matter(W, F))
        rec["totals"].append(F.reshape(F.shape[0], -1).sum(1))
        if hasattr(W, "particles"):
            rec["particles"].append(np.array(W.particles(state), np.float32))
        if f in render_idx:
            rec["render"].append(F.astype(np.float16))
            rec["render_f"].append(f)
        if f and f % max(1, frames // 10) == 0:
            log(f"  frame {f}/{frames}  {time.time() - t0:.1f}s")
    if damage and rec["damage"] is None:
        rec["damage"] = {"frame": int(damage[0]), "mode": damage[2], "frac_requested": float(damage[1]),
                         "error": f"damage frame {damage[0]} was never reached (run has {len(rec['matter'])} frames)"}
    rec["wall"] = time.time() - t0
    return rec


# ------------------------------------------------------------------ analysis
def _jl(a, nd=4):
    """Nested list with nan -> None (strict JSON)."""
    a = np.asarray(a, float)
    if a.ndim == 0:
        return None if not np.isfinite(a) else round(float(a), nd)
    return [_jl(x, nd) for x in a]


def _radial(meta, rec, comps, tracks, top, render, scales, min_area, periodic, exclude=()):
    """Per-channel radial profiles: top tracks at mid-life and an aggregate over individuals.

    exclude: (frame, component) pairs left out of the aggregate (the damaged lineage after the cut).
    """
    C = render.shape[1]
    names = _channel_names(meta, C)
    sel = _channel_list(meta.get("radial_channels"), names, C, "radial_channels")
    rf = rec["render_f"]
    cache = {}

    def norm(k):
        if k not in cache:
            cache[k] = R.normalize(render[k].astype(np.float32), scales)[sel]
        return cache[k]

    def prof(k, f, j):
        """(profile, outside-band coverage, ring: the centroid pixel is not in the component's own mask)."""
        seg = comps[f]
        cy, cx, r_eq = seg["cy"][j], seg["cx"][j], np.sqrt(seg["area"][j] / np.pi)
        p, cnt = M.radial_profile(norm(k), cy, cx, r_eq, periodic)
        H, Wd = seg["lab"].shape
        iy, ix = int(round(cy)), int(round(cx))
        inside = periodic or (0 <= iy < H and 0 <= ix < Wd)
        ring = not (inside and seg["lab"][iy % H, ix % Wd] == j + 1)
        return p, M.band_coverage(cnt, r_eq), ring

    def scores(p):
        return {names[c]: M.boundary_score(p[n]) for n, c in enumerate(sel)}

    per_track = []
    for i in top:
        t = tracks[i]
        cand = [k for k, f in enumerate(rf) if t["start"] <= f <= t["end"]]
        if not cand:
            continue
        k = cand[len(cand) // 2]
        f = rf[k]
        j = t["comp"][f - t["start"]]
        p, cov, ring = prof(k, f, j)
        per_track.append({"track": int(i), "frame": int(f), "area": float(comps[f]["area"][j]),
                          "R_eq": round(float(np.sqrt(comps[f]["area"][j] / np.pi)), 2), "profile": p, "scores": scores(p),
                          "ring": ring, "outside_coverage": round(cov, 3), "damaged": (int(f), int(j)) in exclude})
    ks = [k for k in np.unique(np.linspace(0, len(rf) - 1, 7).round().astype(int)) if k > 0] or [0]
    profs, who, rings, trunc, n_excl = [], [], 0, 0, 0
    for k in ks:
        f = rf[k]
        for j in range(comps[f]["n"]):
            if comps[f]["area"][j] >= 2 * min_area:
                if (int(f), int(j)) in exclude:
                    n_excl += 1
                    continue
                p, cov, ring = prof(k, f, j)
                profs.append(p)
                who.append((int(f), int(j)))
                rings += ring
                trunc += cov < 0.5
    agg = None
    if profs:
        mean, std = M.radial_aggregate(profs)
        sc = scores(mean)
        indiv = {names[c]: 0 for c in sel}
        for p in profs:
            for n, c in enumerate(sel):
                s = M.boundary_score(p[n])
                indiv[names[c]] += bool(s and s["membrane_like"])
        agg = {"n_individuals": len(profs), "frames": sorted({f for f, _ in who}), "min_area": int(2 * min_area),
               "mean": mean, "std": std, "scores": sc, "n_membrane_like_individually": indiv,
               "n_ring": int(rings), "n_outside_truncated": int(trunc)}
    membrane = [names[c] for c in sel if agg and agg["scores"][names[c]] and agg["scores"][names[c]]["membrane_like"]]
    return {"rho": [round(float(r), 3) for r in M.RHO], "channels": [names[c] for c in sel], "channel_index": sel,
            "bands": {"core": list(M.CORE_RHO), "rim": list(M.RIM_RHO), "outside": list(M.OUT_RHO), "peak": list(M.PEAK_RHO)},
            "eps": M.RATIO_EPS, "cap": M.RATIO_CAP, "membrane_ratio": M.MEMBRANE_RATIO,
            "aggregate": agg, "tracks": per_track, "membrane_like": membrane, "n_damaged_excluded": int(n_excl), "_profiles": profs}


def _radial_json(rad):
    out = {k: v for k, v in rad.items() if k != "_profiles"}
    if rad["aggregate"]:
        out["aggregate"] = {**rad["aggregate"], "mean": _jl(rad["aggregate"]["mean"]), "std": _jl(rad["aggregate"]["std"])}
    out["tracks"] = [{**t, "profile": _jl(t["profile"])} for t in rad["tracks"]]
    return out


def _species_stats(meta, rec, periodic, min_area, K, dt_frame, shape):
    """Segmentation, tracking and lineage per species (own channel sum, own robust range)."""
    out = {}
    names = _channel_names(meta, len(rec["totals"][0]))
    for name, chans in _species(meta, len(names)).items():
        mat = np.stack(rec["species"][name])
        T = len(mat)
        mn, thr, lo, hi = _normalize_matter(mat, meta, periodic)
        comps, links = _segment_frames(mn, thr, min_area, periodic, keep_labels=False)
        tracks, events = M.track(comps, links, shape, periodic)
        lin = M.lineage_stats(tracks, events, T, dt_frame, shape, periodic, K=K)
        life = lin["lifetimes"]
        n_comp = [int(c["n"]) for c in comps]
        moving = [m for m in lin["motion"] if m["body_lengths"] >= 1.0 and life[m["id"]] >= K]
        splits = sum(e["type"] == "split" for e in events)
        merges = sum(e["type"] == "merge" for e in events)
        out[name] = {
            "channels": chans, "channel_names": [names[c] for c in chans], "matter_range": [lo, hi],
            "components_final": n_comp[-1], "components_mean": float(np.mean(n_comp)), "components_max": int(max(n_comp)),
            "tracks": len(tracks), "persistent_tracks": int((life >= 0.5 * T).sum()) if len(life) else 0,
            "splits": splits, "persistent_splits": len(lin["persistent_splits"]),
            "remerged_splits": len(lin["remerged_splits"]), "max_generation": int(lin["max_generation"]),
            "merges": merges, "merge_split_ratio": round(merges / splits, 3) if splits else None,
            "moving_tracks": len(moving),
            "max_body_lengths": float(max((m["body_lengths"] for m in lin["motion"]), default=0.0)),
            "persistent_split_frames": [int(e["frame"]) for e in lin["persistent_splits"]],
            "n_comp": n_comp,
        }
    return out


def _main_tracks(comps, tracks, mask, f):
    """Main-run tracks whose frame-f component lies in `mask` (the pre-cut individual): the one
    overlapping it most first, then every other one with >= half of its pixels inside (e.g. a
    core nested in a ring). [] when the run's own segmentation has nothing there."""
    if mask is None:
        return []
    seg = comps[f]
    ids = seg["lab"][mask]
    ids = ids[ids > 0]
    if not len(ids):
        return []
    cnt = np.bincount(ids, minlength=seg["n"] + 1)[1:]
    best = int(np.argmax(cnt))
    js = [best] + [int(j) for j in np.argsort(-cnt) if j != best and cnt[j] >= 0.5 * seg["area"][j]]
    owner = {t["comp"][f - t["start"]]: t["id"] for t in tracks if t["start"] <= f <= t["end"]}
    return [int(owner[j]) for j in js if j in owner]


def _pieces(seg, mn_f, comp_ids, periodic):
    """One individual's pieces at one frame: its member components grouped with what they enclose.
    Returns (largest piece area, its centroid (cy, cx), number of pieces, union of the pieces)."""
    groups = M.individuals(seg, mn_f, periodic, subset=comp_ids)
    big = max(groups, key=lambda g: g["area"])
    union = np.zeros(seg["lab"].shape, bool)
    for g in groups:
        union |= g["mask"]
    return big["area"], (big["cy"], big["cx"]), len(groups), union


def _damage_followup(meta, rec, comps, tracks, periodic, min_area):
    """Follow the damaged individual and its comparator after the cut (see labkit/metrics.py).

    The follow-up is segmented and tracked on its own: the pre-cut field at FRAME, then recorded
    frames FRAME..end, with the range and threshold labkit used to CHOOSE the target, so the
    individual followed is the one that was cut even when the run's own segmentation (whole-run
    range) has no component there. Main-run track ids are looked up for cross-reference only.
    Returns (followup dict, main-run (frame, component) pairs to leave out of the radial
    aggregate, cameras {key: [(cy, cx, state, area_rel, pieces) per recorded frame FRAME..end]}).
    """
    d, arr = rec["damage"], rec["damage_arrays"]
    if not d or arr is None:
        return None, set(), {}
    f0 = d["frame"]
    fp = max(f0 - 1, 0)  # main run: the last recorded frame before the cut (f0 = 0: frame 0, already cut)
    lo, hi = d["seg_range"]
    raw = np.stack([arr["pre_matter"]] + rec["matter"][f0:])
    mn = _normalize_matter(raw, meta, periodic, rng=(lo, hi))[0]
    fc, fl = _segment_frames(mn, d["seg_threshold_rel"], d.get("seg_min_area", min_area), periodic)
    shape = mn.shape[1:]
    ft, _ = M.track(fc, fl, shape, periodic)
    n = len(fc)  # follow-up frame i >= 1 is recorded frame f0 + i - 1; i = 0 is the pre-cut field
    out = {"segmentation": {"range": [round(float(lo), 6), round(float(hi), 6)],
                            "threshold_rel": round(float(d["seg_threshold_rel"]), 4),
                            "frames": f"pre-cut field at frame {f0}, then recorded frames {f0}..{f0 + n - 2}"},
           "baseline": f"pre-cut field at frame {f0}", "main_frame": int(fp),
           "pickup": {"r_pick_R_eq": M.PICKUP_RHO, "gap_frames": M.PICKUP_GAP}}
    cams, excl = {}, set()
    for key in ("target", "comparator"):
        mask = arr[key]
        main = _main_tracks(comps, tracks, mask, fp)
        out[f"{key}_track"] = main[0] if main else None
        out[f"{key}_main_tracks"] = main
        if mask is None:
            continue
        lab0 = fc[0]["lab"]
        seeds = [t["id"] for t in ft if t["start"] == 0 and mask[lab0 == t["comp"][0] + 1].mean() >= 0.5]
        if not seeds:
            continue
        a0 = float(d["individual_area"] if key == "target" else d["comparator_area"])
        fol = M.follow_individual(ft, seeds, fc, M.PICKUP_RHO * np.sqrt(a0 / np.pi), M.PICKUP_GAP, periodic)
        desc = set().union(*[M.descendants(ft, s) for s in fol["members"]]) - fol["members"]
        last = (d["cy"], d["cx"]) if key == "target" else (d["comparator_cy"], d["comparator_cx"])
        m0 = float(raw[0][mask].sum())
        rel, mrel, pieces, cam = [], [], [], []
        for i in range(1, n):
            f = f0 + i - 1
            alive = fol["alive"][i]
            if alive:
                area, last, npc, union = _pieces(fc[i], mn[i], [ft[t]["comp"][i - ft[t]["start"]] for t in alive], periodic)
                rel.append(round(area / a0, 3))
                mrel.append(round(float(raw[i][union].sum()) / m0, 3) if m0 > 0 else None)
                pieces.append(npc)
                cam.append((last[0], last[1], "alive", area / a0, npc))
                if key == "target":  # main-run components that hold the damaged individual
                    seg = comps[f]
                    ov = np.bincount(seg["lab"][union], minlength=seg["n"] + 1)[1:]
                    excl.update((f, int(j)) for j in np.nonzero(ov)[0]
                                if ov[j] >= 0.25 * seg["area"][j] or ov[j] >= 0.5 * union.sum())
                continue
            rel.append(None)
            mrel.append(None)
            pieces.append(0)
            into = [(ft[t]["area"][i - ft[t]["start"]], t) for t in desc if ft[t]["start"] <= i <= ft[t]["end"]]
            if into:  # its lines ended in merges with other individuals: keep the camera on the result
                t = max(into)[1]
                last = (ft[t]["cy"][i - ft[t]["start"]], ft[t]["cx"][i - ft[t]["start"]])
            cam.append((last[0], last[1], "merged" if into else "gone", None, 0))
        ls = fol["last_seen"]
        out.update({
            f"{key}_area_pre": a0,
            f"{key}_area_rel": rel,  # largest piece / individual area just before the cut, frames f0..end (None = not seen)
            f"{key}_matter_rel": mrel,  # raw matter in all its pieces (with what they enclose) / matter just before the cut
            f"{key}_pieces": pieces,  # pieces of the individual alive per frame
            f"{key}_merged_at": sorted({f0 + i - 1 for i, _ in fol["merged"]}),
            f"{key}_picked_up_at": sorted({f0 + i - 1 for i, _ in fol["picked_up"]}),
            f"{key}_last_seen": None if not ls else int(f0 + ls - 1),
        })
        cams[key] = cam
    for tid in out["target_main_tracks"]:  # and every main-run track descended from it (splits and merges)
        for i in M.descendants(tracks, tid):
            t = tracks[i]
            excl.update((f, t["comp"][f - t["start"]]) for f in range(max(t["start"], f0), t["end"] + 1))
    return out, excl, cams


def analyze(W, rec, spf, periodic=True, threshold=None, min_area=None, K=None, dt=None):
    meta = W.META
    dt = _check_dt(meta["dt"] if dt is None else dt, "META dt" if dt is None else "--dt")
    dt_frame = spf * dt
    K, K_src = _lineage_k(meta, K)
    mat = np.stack(rec["matter"])
    T = len(mat)
    mn, thr, lo, hi = _normalize_matter(mat, meta, periodic, threshold)
    H, Wd = mn.shape[1:]
    min_area = min_area or _default_min_area(H, Wd)
    comps, links = _segment_frames(mn, thr, min_area, periodic)
    n_comp, n_encl, holes_tot, occ = [], [], {t: [] for t in THRESHOLDS}, []
    for seg in comps:
        nh, _ = M.holes(seg["lab"], seg["n"], periodic=periodic)
        seg["holes"] = nh
        n_comp.append(seg["n"])
        n_encl.append(int((nh > 0).sum()))
        occ.append(float((seg["lab"] > 0).mean()))
    for t in THRESHOLDS:
        for f in np.linspace(0, T - 1, min(T, 24)).round().astype(int):
            s = M.segment(mn[f], t, min_area, periodic)
            holes_tot[t].append(int(M.holes(s["lab"], s["n"], periodic=periodic)[0].sum()))
    tracks, events = M.track(comps, links, (H, Wd), periodic)
    lin = M.lineage_stats(tracks, events, T, dt_frame, (H, Wd), periodic, K=K)

    # topology of the matter field and of each channel
    tda_frames = np.unique(np.linspace(0, T - 1, min(T, 12)).round().astype(int))
    tda = {int(f): M.persistence_counts(mn[f], periodic=periodic) for f in tda_frames}
    render = np.stack([r.astype(np.float32) for r in rec["render"]])
    scales = R.channel_scales(render)
    ch_tda = {}
    for k in np.unique(np.linspace(0, len(render) - 1, min(len(render), 6)).round().astype(int)):
        ch_tda[int(rec["render_f"][k])] = [M.persistence_counts(R.normalize(render[k], scales)[c], periodic=periodic)
                                           for c in range(render.shape[1])]

    # inside / boundary / outside organization of the most persistent tracks
    life = lin["lifetimes"]
    order = sorted(range(len(tracks)), key=lambda i: (-life[i], -(tracks[i]["end"] == T - 1)))
    top = order[:3]
    gen = lin["generation"]
    deep = sorted(range(len(tracks)), key=lambda i: (-gen[i], -life[i]))
    if deep and gen[deep[0]] > 0 and deep[0] not in top:
        top.append(deep[0])  # also show the most-derived lineage member
    else:
        top = order[:4]
    rf = rec["render_f"]
    struct = []
    for i in top:
        t = tracks[i]
        cand = [k for k, f in enumerate(rf) if t["start"] <= f <= t["end"]]
        if not cand:
            continue
        k = cand[len(cand) // 2]
        f = rf[k]
        seg = M.segment(mn[f], thr, min_area, periodic)
        j = int(np.argmin([np.hypot(M._wrap(seg["cy"][q] - t["cy"][f - t["start"]], H),
                                    M._wrap(seg["cx"][q] - t["cx"][f - t["start"]], Wd)) for q in range(seg["n"])])) if seg["n"] else None
        if j is None:
            continue
        s = M.structure(R.normalize(render[k], scales), seg["lab"] == j + 1)
        if s:
            struct.append({"track": i, "frame": int(f), "holes": int(seg_holes(seg, j, periodic)), **s})
    # the damaged individual (and its main-run descendants) after the cut stay out of the radial aggregate
    dmg, excl, dmg_cam = _damage_followup(meta, rec, comps, tracks, periodic, min_area)
    radial = _radial(meta, rec, comps, tracks, top, render, scales, min_area, periodic, excl)
    species = _species_stats(meta, rec, periodic, min_area, K, dt_frame, (H, Wd)) if rec.get("species") else {}

    totals = np.stack(rec["totals"])
    ok_tot = np.abs(totals[0]) > 1e-9
    drift = np.where(ok_tot, (totals[-1] - totals[0]) / np.where(ok_tot, np.abs(totals[0]), 1), np.nan)
    persistent = [i for i in range(len(tracks)) if life[i] >= 0.5 * T]
    moving = [m for m in lin["motion"] if m["body_lengths"] >= 1.0 and life[m["id"]] >= lin["K_frames"]]
    persist_area = [(min(tracks[i]["area"]), max(tracks[i]["area"])) for i in persistent]
    n_split = sum(e["type"] == "split" for e in events)
    n_merge = sum(e["type"] == "merge" for e in events)
    summary = {
        "frames": T, "time": (T - 1) * dt_frame, "dt": dt, "grid": [int(H), int(Wd)],
        "threshold_rel": float(thr), "matter_range": [lo, hi], "min_area": int(min_area),
        "components_final": int(n_comp[-1]), "components_mean": float(np.mean(n_comp)),
        "components_max": int(np.max(n_comp)),
        "occupancy_final": occ[-1], "occupancy_max": float(np.max(occ)),
        "tracks": len(tracks), "persistent_tracks": len(persistent),
        "longest_track_frames": int(life.max()) if len(life) else 0,
        "alive_at_end_from_start": int(sum(1 for t in tracks if t["start"] == 0 and t["end"] == T - 1)),
        "persistent_area_ratio_max": float(max((b / max(a, 1) for a, b in persist_area), default=0)),
        "enclosed_components_mean": float(np.mean(n_encl)), "enclosed_components_final": int(n_encl[-1]),
        "holes_final_by_threshold": {str(t): holes_tot[t][-1] for t in THRESHOLDS},
        "holes_mean_by_threshold": {str(t): float(np.mean(holes_tot[t])) for t in THRESHOLDS},
        "K_frames": int(K), "K_source": K_src,
        "splits": n_split,
        "persistent_splits": len(lin["persistent_splits"]),
        "remerged_splits": len(lin["remerged_splits"]),
        "max_generation": int(lin["max_generation"]),
        "merges": n_merge,
        "merge_split_ratio": round(n_merge / n_split, 3) if n_split else None,
        "nucleations": sum(t["birth"] == "nucleation" for t in tracks),
        "moving_tracks": len(moving),
        "max_speed": float(max((m["speed"] for m in moving), default=0.0)),
        "max_body_lengths": float(max((m["body_lengths"] for m in lin["motion"]), default=0.0)),
        "channel_total_drift": [None if np.isnan(d) else round(float(d), 4) for d in drift],
        "tda_matter_final": tda[int(tda_frames[-1])],
        "membrane_like_channels": radial["membrane_like"],
    }
    return {
        "summary": summary, "series": {"n_comp": n_comp, "n_enclosed": n_encl, "occupancy": occ,
                                       "totals": totals.tolist()},
        "tracks": tracks, "events": events, "lineage": lin, "tda": tda, "channel_tda": ch_tda,
        "structure": struct, "scales": scales, "top": top, "mn": mn, "comps": comps, "render": render,
        "radial": radial, "species": species, "damage": dmg, "damage_cam": dmg_cam, "dt": dt, "dt_frame": dt_frame,
    }


def seg_holes(seg, j, periodic):
    nh, _ = M.holes(seg["lab"], seg["n"], periodic=periodic)
    return nh[j] if j < len(nh) else 0


# ------------------------------------------------------------------ figures
def _radial_figure(meta, A, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rad = A["radial"]
    names, agg, rho = rad["channels"], rad["aggregate"], M.RHO
    n = len(names)
    ncol = min(n, 4)
    nrow = int(np.ceil(n / ncol))
    fig, axs = plt.subplots(nrow, ncol, figsize=(3.6 * ncol + 0.4, 3.0 * nrow + 0.6), squeeze=False)
    cmap = plt.get_cmap("tab10")
    profs = rad["_profiles"]
    thin = [profs[i] for i in np.unique(np.linspace(0, len(profs) - 1, min(len(profs), 80)).round().astype(int))] if profs else []
    for c, name in enumerate(names):
        ax = axs.flat[c]
        for lo, hi, col in (M.CORE_RHO + ("tab:blue",), M.RIM_RHO + ("tab:red",), M.OUT_RHO + ("0.5",)):
            ax.axvspan(lo, hi, color=col, alpha=0.07, lw=0)
        ax.axvline(1.0, color="0.6", lw=0.8, ls=":")
        for p in thin:
            ax.plot(rho, p[c], color="0.55", lw=0.5, alpha=0.35)
        for q, t in enumerate(rad["tracks"]):
            ax.plot(rho, t["profile"][c], color=cmap(q % 10), lw=1.0, alpha=0.9,
                    label=f"#{t['track']} t={t['frame'] * A['dt_frame']:g}" if c == 0 else None)
        title = name
        if agg:
            m, s = agg["mean"][c], agg["std"][c]
            ax.fill_between(rho, m - s, m + s, color="k", alpha=0.12, lw=0)
            ax.plot(rho, m, color="k", lw=2.6, label=f"aggregate (N={agg['n_individuals']})" if c == 0 else None)
            sc = agg["scores"][name]
            if sc:
                tag = "  MEMBRANE-LIKE" if sc["membrane_like"] else ""
                title = (f"{name}{tag}\npeak rho={sc['rho_peak']:.2f}  rim/core {_g(sc['rim_core'])}  "
                         f"rim/out {_g(sc['rim_outside'])}")
        ax.set_title(title, fontsize=9, color="tab:red" if agg and agg["scores"][name] and agg["scores"][name]["membrane_like"] else "k")
        ax.set_xlim(0, M.RHO_EDGES[-1])
        ax.set_ylim(bottom=0)
        ax.set_xlabel("rho = r / R_eq")
        if c % ncol == 0:
            ax.set_ylabel("channel (fixed render scale)")
    for ax in list(axs.flat)[n:]:
        ax.axis("off")
    if axs.flat[0].get_legend_handles_labels()[0]:
        axs.flat[0].legend(fontsize=6, loc="upper right")
    fig.suptitle(f"{meta['name']}: channel means vs rho = r / R_eq around tracked centroids\n"
                 f"bands core (blue) / rim (red) / outside (grey); thin grey = individuals at "
                 f"{len(agg['frames']) if agg else 0} frames, colour = top tracks, black = aggregate +- std", fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "radial.png", dpi=80)
    plt.close(fig)


def _damage_figure(meta, rec, A, rgb, out):
    """damage.png: the damaged individual (top) and the comparator (bottom) at ~8 render frames after
    the cut, cropped where the follow-up last saw them (never a blank tile). Returns True if written."""
    d, fu, cams = rec["damage"], A["damage"], A.get("damage_cam") or {}
    if not fu or "target" not in cams:
        return False
    rf, scales, dt_frame = rec["render_f"], A["scales"], A["dt_frame"]
    arr = rec["damage_arrays"]
    H, Wd = rgb[0].shape[:2]
    f0 = d["frame"]
    post = [k for k, f in enumerate(rf) if f0 <= f < f0 + len(cams["target"])]
    if not post:
        return False
    sel = [post[int(i)] for i in np.unique(np.linspace(0, len(post) - 1, min(8, len(post))).round().astype(int))]
    area = max(d["individual_area"], d.get("comparator_area") or 0)
    half = int(np.clip(2.0 * np.sqrt(area / np.pi) + 6, 12, min(H, Wd) // 2))
    pre_rgb = R.composite(R.normalize(arr["pre"].astype(np.float32), scales))
    tiles, labels = [], []

    def tile(img, cy, cx):
        return np.asarray(R.Image.fromarray(R.crop_periodic(img, cy, cx, half)).resize((128, 128), R.Image.NEAREST))

    for key, cy0, cx0 in (("target", d["cy"], d["cx"]), ("comparator", d.get("comparator_cy"), d.get("comparator_cx"))):
        if key not in cams:
            continue
        tid = fu.get(f"{key}_track")
        tiles.append(tile(R.outline(pre_rgb, arr["mask"]) if key == "target" else pre_rgb, cy0, cx0))
        labels.append(f"{'#%d ' % tid if tid is not None else ''}pre t={f0 * dt_frame:g}")
        for k in sel:
            cy, cx, state, rel, npc = cams[key][rf[k] - f0]
            if rf[k] == f0:  # the frame just after the cut: same framing as "pre"
                cy, cx = cy0, cx0
            tiles.append(tile(rgb[k], cy, cx))
            t = f"t={rf[k] * dt_frame:g}"
            labels.append(f"{t} a={rel:.2f}{' x%d' % npc if npc > 1 else ''}" if state == "alive" else f"{t} {state}")
    loss = d.get("erased_frac")
    tmain = fu.get("target_main_tracks") or []
    title = (f"{d['mode']} {d['frac_requested']:.2f} t={f0 * dt_frame:g}: top target "
             f"({'main ' + ', '.join('#%d' % x for x in tmain) if tmain else 'NO main-run track'}, lost "
             f"{'?' if loss is None else f'{loss:.0%}'}, red = cut), bottom "
             + ("comparator" if "comparator" in cams else "none")
             + "; a = largest piece / pre-cut area, xN pieces")
    R.contact_sheet(tiles, labels, ncols=len(sel) + 1, title=title).save(out / "damage.png")
    return True


def _g(v):
    return "n/a" if v is None else f"{v:.3g}"


def figures(W, rec, A, out, spf, movie=True):
    meta = W.META
    dt_frame = A.get("dt_frame", spf * float(meta["dt"]))
    render, scales, rf = A["render"], A["scales"], rec["render_f"]
    rgb = [R.composite(R.normalize(fr, scales)) for fr in render]
    pick = np.unique(np.linspace(0, len(rgb) - 1, min(24, len(rgb))).round().astype(int))
    chans = meta["channels"] or [f"c{i}" for i in range(render.shape[1])]
    legend = "  ".join(f"{n}" for n in chans)
    title = f"{meta['name']}  |  channels: {legend}  |  fixed colour scales"
    R.contact_sheet([rgb[k] for k in pick], [f"t={rf[k] * dt_frame:g}" for k in pick], ncols=6,
                    title=title, tile=256).save(out / "sheet.png")

    if rec["particles"]:
        P = rec["particles"]
        dom = meta.get("domain")
        if dom:
            view = (0, 0, dom[0], dom[1])
        else:
            allp = np.concatenate([p[:, :2] for p in P[:: max(1, len(P) // 20)]])
            lo, hi = np.percentile(allp, 1, 0), np.percentile(allp, 99, 0)
            c, half = (lo + hi) / 2, max(hi - lo) / 2 * 1.15 + 1
            view = (c[0] - half, c[1] - half, c[0] + half, c[1] + half)
        idx = np.unique(np.linspace(0, len(P) - 1, 24).round().astype(int))
        ims = [R.particle_canvas(P[k][:, :2], P[k][:, 2] if P[k].shape[1] > 2 else None, view, 256,
                                 radius=max(1.0, 256 / (view[2] - view[0]) * 0.4)) for k in idx]
        R.contact_sheet(ims, [f"t={k * dt_frame:g}" for k in idx], ncols=6,
                        title=f"{meta['name']} particles  |  view {tuple(round(float(v), 1) for v in view)}").save(out / "particles.png")

    # biographies of the top tracks
    tracks, top = A["tracks"], A["top"]
    rows, labels = [], []
    H, Wd = render.shape[2:]
    for i in top:
        t = tracks[i]
        cand = [k for k, f in enumerate(rf) if t["start"] <= f <= t["end"]]
        if not cand:
            continue
        sel = [cand[int(j)] for j in np.unique(np.linspace(0, len(cand) - 1, min(8, len(cand))).round().astype(int))]
        half = int(np.clip(1.6 * np.sqrt(max(t["area"]) / np.pi) + 6, 12, min(H, Wd) // 2))
        for k in sel:
            f = rf[k]
            crop = R.crop_periodic(rgb[k], t["cy"][f - t["start"]], t["cx"][f - t["start"]], half)
            rows.append(np.asarray(R.Image.fromarray(crop).resize((112, 112), R.Image.NEAREST)))
            labels.append(f"#{i} t={f * dt_frame:g}")
        while len(rows) % 8:
            rows.append(np.zeros((112, 112, 3), np.uint8))
            labels.append("")
    written = ["sheet.png"] + (["particles.png"] if rec["particles"] else [])
    if rows:
        R.contact_sheet(rows, labels, ncols=8, title="most persistent individuals (fixed crops follow the tracked centroid)").save(out / "tracks.png")
        written.append("tracks.png")
    _radial_figure(meta, A, out)
    written.append("radial.png")
    if rec.get("damage") and _damage_figure(meta, rec, A, rgb, out):
        written.append("damage.png")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    s = A["series"]
    tt = np.arange(len(s["n_comp"])) * dt_frame
    sp = A.get("species") or {}
    fig, ax = plt.subplots(3 if sp else 2, 2, figsize=(11, 9.5 if sp else 6.5))
    ax[0, 0].plot(tt, s["n_comp"], label="components")
    ax[0, 0].plot(tt, s["n_enclosed"], label="components with a hole")
    ax[0, 0].legend(); ax[0, 0].set_title("individuals")
    tot = np.array(s["totals"])
    for c in range(tot.shape[1]):
        base = np.abs(tot[0, c]) if abs(tot[0, c]) > 1e-9 else 1.0
        ax[0, 1].plot(tt, tot[:, c] / base, label=(meta["channels"] or [f"c{c}" for c in range(tot.shape[1])])[c])
    ax[0, 1].set_title("channel totals / initial"); ax[0, 1].legend(fontsize=7)
    ax[1, 0].plot(tt, s["occupancy"]); ax[1, 0].set_title("occupied fraction (matter > threshold)")
    for e in A["events"]:
        ax[1, 1].axvline(e["frame"] * dt_frame, color="tab:green" if e["type"] == "split" else "tab:red", alpha=0.35)
    for e in A["lineage"]["persistent_splits"]:
        ax[1, 1].axvline(e["frame"] * dt_frame, color="k", lw=2)
    ax[1, 1].set_title(f"events: split (green), merge (red), persistent split (black, K={A['lineage']['K_frames']})")
    for q, (name, st) in enumerate(sp.items()):
        col = plt.get_cmap("tab10")(q % 10)
        ax[2, 0].plot(tt[:len(st["n_comp"])], st["n_comp"], color=col, label=f"{name} {st['channel_names']}")
        ps = np.zeros(len(tt))
        for f in st["persistent_split_frames"]:
            ps[f:] += 1
        ax[2, 1].step(tt, ps, where="post", color=col, label=name)
    if sp:
        ax[2, 0].set_title("components per species (own channel sum and threshold)"); ax[2, 0].legend(fontsize=7)
        ax[2, 1].set_title("cumulative persistent splits per species"); ax[2, 1].legend(fontsize=7)
    for a in ax.flat:
        a.set_xlabel("time")
    fig.tight_layout(); fig.savefig(out / "timeseries.png", dpi=80); plt.close(fig)

    # lineage chart
    life = A["lineage"]["lifetimes"]
    K = A["lineage"]["K_frames"]
    keep = [t for t in tracks if life[t["id"]] >= K or t["children"] or t["birth"] == "split"]
    keep = sorted(keep, key=lambda t: -life[t["id"]])[:150]
    keep_ids = {t["id"] for t in keep}
    ypos = {t["id"]: k for k, t in enumerate(sorted(keep, key=lambda t: (t["start"], t["id"])))}
    fig, ax = plt.subplots(figsize=(11, max(3, min(12, 0.08 * len(keep) + 2))))
    gen = A["lineage"]["generation"]
    cmap = plt.get_cmap("viridis")
    gmax = max(1, max(gen.values(), default=1))
    for t in keep:
        y = ypos[t["id"]]
        ax.plot([t["start"] * dt_frame, t["end"] * dt_frame], [y, y], color=cmap(gen[t["id"]] / gmax), lw=2)
        for p in t["parents"]:
            if p in keep_ids:
                ax.plot([t["start"] * dt_frame] * 2, [ypos[p], y], color="0.6", lw=0.8)
    ax.set_xlabel("time"); ax.set_ylabel("track")
    ax.set_title(f"lineage: colour = generation (max {A['summary']['max_generation']}), "
                 f"{A['summary']['persistent_splits']} persistent splits (K={K} frames), {len(keep)} tracks shown")
    fig.tight_layout(); fig.savefig(out / "lineage.png", dpi=80); plt.close(fig)
    written += ["lineage.png", "timeseries.png"]

    if movie:
        R.save_movie(rgb, str(out / "movie.mp4"), fps=15)
        written.append("movie.mp4")
    return written


# ------------------------------------------------------------------ facts
def _radial_facts(A, warn):
    rad, lines = A["radial"], []
    agg = rad["aggregate"]
    excl = rad.get("n_damaged_excluded", 0)
    excl_note = (f"; {excl} components of the damaged lineage after the cut left out" if excl else "")
    if not agg:
        return [f"- radial profiles: no component with area >= {2 * A['summary']['min_area']} px at the sampled frames"
                f"{excl_note}"]
    lines.append(f"- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, "
                 f"rim 0.6-1.3, outside 1.6-2.2; aggregate of {agg['n_individuals']} components >= {agg['min_area']} px "
                 f"at frames {agg['frames']}{excl_note}):")
    lo, hi = M.PEAK_RHO
    for name in rad["channels"]:
        sc = agg["scores"][name]
        if not sc:
            lines.append(f"  - radial {name}: empty profile")
            continue
        if sc.get("flat"):
            lines.append(f"  - radial {name}: flat profile (no radial structure; level {_g(sc['rim_max'])}; "
                         f"aggregate of {agg['n_individuals']} individuals)")
            continue
        peak = "in" if sc["peak_in_rim"] else "OUTSIDE"
        lines.append(f"  - radial {name}: peak at rho={sc['rho_peak']:.2f} ({peak} the peak band {lo:g}-{hi:g}), "
                     f"rim/core {_g(sc['rim_core'])}, rim/outside {_g(sc['rim_outside'])} (aggregate of "
                     f"{agg['n_individuals']} individuals; "
                     f"{agg['n_membrane_like_individually'][name]}/{agg['n_individuals']} membrane-like individually; "
                     f"rim level {_g(sc['rim_max'])})" + ("  MEMBRANE-LIKE" if sc["membrane_like"] else ""))
    if agg.get("n_ring"):
        warn.append(f"radial: {agg['n_ring']} of {agg['n_individuals']} aggregate members are rings (centroid outside "
                    f"their own mask): the threshold may cut individuals into a core and a separate ring, so one "
                    f"individual is counted twice and the ring's profile is centred on its hole; check radial.png and "
                    f"raise META smooth or set META matter so one component covers each individual")
    if agg.get("n_outside_truncated"):
        warn.append(f"radial: for {agg['n_outside_truncated']} of {agg['n_individuals']} aggregate members less than "
                    f"half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open "
                    f"boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from "
                    f"the smaller members")
    ml = [n + ("" if agg["scores"][n]["peak_in_rim"] else f" (peak at rho={agg['scores'][n]['rho_peak']:.2f}, "
                                                          f"outside the peak band)") for n in rad["membrane_like"]]
    lines.append(f"- membrane-like channels (aggregate rim/core >= {M.MEMBRANE_RATIO:g} and rim/outside >= "
                 f"{M.MEMBRANE_RATIO:g}; the peak position is not part of the test): {', '.join(ml) if ml else 'none'}")
    if rad["tracks"]:
        per = "; ".join(f"#{t['track']} (t={t['frame'] * A['dt_frame']:g}, R_eq {t['R_eq']:g}"
                        f"{', ring' if t.get('ring') else ''}{', DAMAGED' if t.get('damaged') else ''}): "
                        f"{[n for n, s in t['scores'].items() if s and s['membrane_like']] or 'none'}" for t in rad["tracks"])
        lines.append(f"- membrane-like channels per top track at mid-life: {per}")
    return lines


def _damage_facts(A, rec, warn, has_png=False):
    d, fu, dt_frame = rec["damage"], A["damage"] or {}, A["dt_frame"]
    if d.get("error"):
        warn.append(f"damage requested but not applied: {d['error']}")
        return [f"- damage ({d['mode']}, {d['frac_requested']:.2f}) at frame {d['frame']}: NOT APPLIED ({d['error']})"]
    loss, f0 = d["erased_frac"], d["frame"]
    ids = lambda v: ", ".join(f"#{x}" for x in v)  # noqa: E731
    pct = lambda v: _g(None if v is None else 100 * v)  # noqa: E731
    tmain, cmain = fu.get("target_main_tracks") or [], fu.get("comparator_main_tracks") or []
    fp = fu.get("main_frame", max(f0 - 1, 0))
    nested = [round(a) for a in d["member_areas"][1:]]
    who = (f"{d['member_components']} component(s): outer component {d['component_area']:.0f} px + {d['enclosed_px']} px "
           f"it encloses ({f'nested components {nested} px + ' if nested else ''}"
           f"{d['enclosed_px'] - sum(nested):.0f} px of low-matter holes) = {d['individual_area']:.0f} px"
           if d["enclosed_px"] else f"one component of {d['individual_area']:.0f} px")
    asp = d.get("aspect")
    lines = [
        f"- damage `{d['mode']}` (requested {d['frac_requested']:.2f} of the area) at frame {f0} (t={f0 * dt_frame:g}): "
        f"target = main-run track {ids(tmain) if tmain else 'NONE (see warnings)'}; the individual is {who} = "
        f"{d['individual_area'] / max(d['median_area'], 1):.2f}x the median individual, aspect {_g(asp)} (rule {d['rule']}: "
        f"track age {d['track_age_frames']} frames vs K={d['K_frames']}; {d['n_individuals']} individuals from "
        f"{d['n_components']} components at that frame; open-ring individuals, not eligible: {d['n_ring_individuals']}); mask "
        f"{d['mask_px']} px ({d['mask_px_in_component']} inside the individual)",
        f"- damage MEASURED: the target lost {pct(loss)}% of its matter (inside the individual: its components and what "
        f"they enclose; {d['erased_px']} of {d['individual_area']:.0f} px lost > half their matter); net matter lost "
        f"outside it = {pct(d['lost_outside_frac'])}% of its matter; share of all matter that disappeared that was under "
        f"labkit's mask {_g(d.get('lost_under_mask_share'))}"
        + (f"; matter GAINED somewhere = {pct(d['gained_frac'])}% of its matter (the hook resets or adds matter)"
           if (d.get("gained_frac") or 0) > 1e-3 else ""),
    ]
    rng = d.get("seg_range")
    for key, mains in (("target", tmain), ("comparator", cmain)):
        if not mains and (key == "target" or d.get("comparator_area") is not None):
            warn.append(f"damage: the {key} has NO track in the main analysis: at recorded frame {fp} no component of the "
                        f"run's own segmentation (robust range of the whole run, "
                        f"{[round(v, 4) for v in A['summary']['matter_range']]}) overlaps it; labkit chose it with the range "
                        f"of frames 0..{f0}, {[round(v, 4) for v in rng]} (the matter level changes during the run). The "
                        f"follow-up and damage.png use that targeting segmentation; tracks.png, lineage.png and the radial "
                        f"track list cannot show it")
    if d.get("lost_under_mask_share") is not None and d["lost_under_mask_share"] < 0.5:
        warn.append(f"the world's damage() hook did not erase where labkit's mask was (only "
                    f"{d['lost_under_mask_share']:.0%} of the matter that disappeared was under it): the MEASURED loss is "
                    f"what counts")
    if asp is not None and asp > M.DAMAGE_ASPECT_WARN:
        warn.append(f"damage target is elongated (aspect {asp:.2f} > {M.DAMAGE_ASPECT_WARN:g}; rule {d['rule']}): "
                    f"it may be elongating or pinching (dividing) rather than a compact individual; check damage.png "
                    f"or damage at another frame")
    if d["rule"] != "mature-compact":
        warn.append(f"damage target is NOT a mature compact individual (rule {d['rule']}): no individual at frame "
                    f"{f0} had a track >= K={d['K_frames']} frames, an area within {list(M.DAMAGE_AREA_BAND)} x median "
                    f"and its centroid inside itself; damage later or lower --lineage-k")
    if d["mode"] == "rim":
        lines.append("- (rim mode: the disk has the requested area but is centred on the individual's outer boundary, so "
                     "about half of it lies outside the individual and cuts the layer at the edge)")
    elif loss is not None and loss < 0.5 * d["frac_requested"]:
        warn.append(f"damage erased only {loss:.0%} of the target's matter against {d['frac_requested']:.0%} requested")
    if d["mode"] == "half":
        lines.append(f"- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a "
                     f"layer just outside the threshold contour: {d['mask_px'] - d['mask_px_in_component']} of the "
                     f"{d['mask_px']} mask px are outside the individual; that loss is the 'outside' figure above)")
    if "target_area_rel" in fu:
        rel = fu["target_area_rel"]
        idx = np.unique(np.linspace(0, len(rel) - 1, 6).round().astype(int)) if rel else []
        tm = lambda fs: [round(f * dt_frame, 3) for f in fs]  # noqa: E731
        times = tm(f0 + int(i) for i in idx)
        part = {}
        for key in ("target", "comparator"):
            if f"{key}_area_rel" not in fu:
                continue
            r, pc = fu[f"{key}_area_rel"], fu[f"{key}_pieces"]
            ev = []
            if fu[f"{key}_merged_at"]:
                ev.append(f"merged with another individual at t={tm(fu[key + '_merged_at'][:6])}")
            if fu[f"{key}_picked_up_at"]:
                ev.append(f"re-nucleated pieces picked up at t={tm(fu[key + '_picked_up_at'][:6])}")
            ls = fu[f"{key}_last_seen"]
            if ls is None:
                ev.append("not seen after the cut")
            elif ls < f0 + len(r) - 1:
                ev.append(f"last seen t={ls * dt_frame:g}")
            mr = fu[f"{key}_matter_rel"]
            part[key] = (f"{[r[i] for i in idx]} (matter {[mr[i] for i in idx]}; pieces {[pc[i] for i in idx]}"
                         + (f"; {'; '.join(ev)}" if ev else "") + ")")
        cmp_txt = (f"comparator {part['comparator']}" if "comparator" in part else
                   "no comparator (no other individual at the damage frame)" if d.get("comparator_area") is None else
                   "comparator not found in the follow-up segmentation")
        seg = fu["segmentation"]
        lines.append(
            f"- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact "
            f"membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before "
            f"the cut, at t={times}: target {part.get('target', 'not found in the follow-up segmentation')}; {cmp_txt}. "
            f"Follow-up: {seg['frames']} segmented with the TARGETING range {seg['range']} (threshold "
            f"{seg['threshold_rel']:g}), so the individual followed is the one that was cut; followed through its own "
            f"splits, re-merges of its own pieces and nucleations within {M.PICKUP_RHO:g} R_eq of its pixels where it "
            f"was last seen (<= {M.PICKUP_GAP} frames earlier); None = not seen (below threshold, or merged with another individual)"
            + (" (damage.png: crops at the last known position)" if has_png else ""))
    return lines


def facts(W, rec, A, out, seed, spf, args_line, written=None):
    meta, s = W.META, A["summary"]
    dt = A.get("dt", meta["dt"])
    warn = []
    if rec["status"] != "ok":
        warn.append(f"RUN FAILED: {rec['status']} (only {s['frames']} frames analysed)")
    if s["occupancy_max"] > 0.8:
        warn.append("matter fills >80% of the domain at some point: components may be one connected sea")
    if s["components_final"] == 0:
        warn.append("no components at the end: matter died out or fell below threshold")
    drift = [d for d in s["channel_total_drift"] if d is not None]
    if drift and max(abs(d) for d in drift) > 0.5:
        warn.append("a channel total changed by more than 50% (not conserved; may be fine if the model is open)")
    if s["frames"] < 30:
        warn.append("fewer than 30 recorded frames: tracking statistics are weak")
    if s["K_frames"] > s["frames"] / 2:
        warn.append(f"lineage window K={s['K_frames']} frames is more than half the run: late splits cannot count as persistent")
    if float(dt) != float(meta["dt"]):
        warn.append(f"--dt {float(dt):g} only relabels time (world META dt {meta['dt']}): the world's integration step is "
                    "unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that")
    dt_note = f" (--dt; world META dt {meta['dt']})" if float(dt) != float(meta["dt"]) else ""
    K, dtf = s["K_frames"], A.get("dt_frame", spf * float(dt))
    lines = [
        f"# Evidence pack: {meta['name']} (seed {seed})",
        "",
        f"- world: `{os.path.relpath(meta['path'], out)}`, family `{meta['family']}`",
        f"- parent: {meta['parent']}; mutation: {meta['mutation'] or '-'}",
        f"- run: {s['frames']} frames x {spf} steps x dt {dt if dt_note else meta['dt']}{dt_note} = time {s['time']:g}; grid {s['grid']}; "
        f"wall {rec['wall']:.0f}s; status {rec['status']}",
        f"- command: `{args_line}`",
        f"- segmentation: matter > {s['threshold_rel']:.2f} of robust range {[round(v, 4) for v in s['matter_range']]}, "
        f"min area {s['min_area']} px",
        "",
        "## Measurements",
        f"- components: final {s['components_final']}, mean {s['components_mean']:.1f}, max {s['components_max']}; "
        f"occupancy final {s['occupancy_final']:.2f}",
        f"- tracks: {s['tracks']}; persistent (alive >= 50% of run): {s['persistent_tracks']}; "
        f"longest {s['longest_track_frames']} frames; alive start-to-end: {s['alive_at_end_from_start']}",
        f"- size of persistent tracks: max/min area ratio {s['persistent_area_ratio_max']:.2f} (1 = constant size)",
        f"- enclosures: components with a hole mean {s['enclosed_components_mean']:.2f}, final {s['enclosed_components_final']}; "
        f"holes at thresholds 0.2/0.35/0.5 final {list(s['holes_final_by_threshold'].values())}",
        f"- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 {s['tda_matter_final']['H0']}, "
        f"H1 {s['tda_matter_final']['H1']}",
        f"- motion: {s['moving_tracks']} long-lived tracks moved >= 1 body length; max speed {s['max_speed']:.3g}/time; "
        f"max body lengths {s['max_body_lengths']:.1f}",
        f"- replication (lineage window K = {K} frames = time {K * dtf:g}, {s['K_source']}): splits {s['splits']}, "
        f"persistent splits {s['persistent_splits']} ({s['remerged_splits']} more failed only because the siblings "
        f"re-merged within K), max generation {s['max_generation']}, merges {s['merges']}, "
        f"merge/split ratio {_g(s['merge_split_ratio'])}, nucleations {s['nucleations']}",
        f"- channel total drift (end/start - 1): {s['channel_total_drift']}",
    ]
    if A["structure"]:
        lines.append("- internal organization of top tracks (normalized channel means; rim = outer layer):")
        for st in A["structure"]:
            lines.append(f"  - track {st['track']} at frame {st['frame']}: holes {st['holes']}, "
                         f"rim-vs-core {st['rim_vs_core']:.2f}, rim-vs-outside {st['rim_vs_outside']:.2f}, "
                         f"heterogeneity {st['heterogeneity']:.2f}; core {st['core_mean']} rim {st['rim_mean']}")
    lines += _radial_facts(A, warn)
    for name, sp in (A.get("species") or {}).items():
        lines.append(f"- species `{name}` (channels {sp['channel_names']}, own threshold): components final "
                     f"{sp['components_final']}, mean {sp['components_mean']:.1f}, max {sp['components_max']}; tracks "
                     f"{sp['tracks']}, persistent {sp['persistent_tracks']}; splits {sp['splits']}, persistent splits "
                     f"{sp['persistent_splits']} (K={K}), max generation {sp['max_generation']}, merges {sp['merges']}, "
                     f"merge/split {_g(sp['merge_split_ratio'])}; moving tracks {sp['moving_tracks']}")
    files = list(written) if written is not None else [n for n in FIGURES if (out / n).exists()]
    if rec.get("damage"):
        lines += _damage_facts(A, rec, warn, "damage.png" in files)
    lines += ["", "## Warnings"] + ([f"- {w}" for w in warn] or ["- none"])
    lines += ["", "## Files", ", ".join(files + ["metrics.json"]),
              "", "Measurements are screens, not verdicts: judge them against the images."]
    (out / "FACTS.md").write_text("\n".join(lines) + "\n")
    return warn


def run_pack(world_path, out, seed=0, frames=200, spf=None, size=None, damage=None, movie=True,
             threshold=None, min_area=None, save_frames=True, quiet=False, args_line="", lineage_k=None, dt=None):
    log = (lambda *a: None) if quiet else print
    W = load_world(world_path)
    if threshold is None:
        threshold = W.META.get("threshold")  # META documents an absolute threshold; honour it
    spf = int(spf or W.META["steps_per_frame"])
    size = tuple(size or W.META["size"])
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    for name in ("damage.png", "tracks.png"):  # never leave a stale figure from an older run
        (out / name).unlink(missing_ok=True)
    log(f"[{W.META['name']}] seed {seed}: {frames} frames x {spf} steps, grid {size}")
    periodic = W.META.get("periodic", True)
    K = _lineage_k(W.META, lineage_k)[0]
    _check_dt(W.META["dt"] if dt is None else dt, "META dt" if dt is None else "--dt")  # before simulating
    rec = simulate(W, seed, frames, spf, size, damage=damage, log=log, K=K, periodic=periodic,
                   threshold=threshold, min_area=min_area)
    if len(rec["matter"]) < 2:
        why = rec["status"] if rec["status"] != "ok" else f"only {len(rec['matter'])} recorded frame (use --frames >= 1)"
        (out / "FACTS.md").write_text(f"# {W.META['name']} seed {seed}\n\nRUN FAILED: {why}\n")
        return {"seed": seed, "status": rec["status"]}
    A = analyze(W, rec, spf, periodic, threshold, min_area, K=lineage_k, dt=dt)
    written = figures(W, rec, A, out, spf, movie)
    warn = facts(W, rec, A, out, seed, spf, args_line, written)
    lin = A["lineage"]
    top_tracks = [{k: (v if k not in ("area", "cy", "cx") else [round(float(x), 2) for x in v[:: max(1, len(v) // 50)]])
                   for k, v in A["tracks"][i].items() if k != "comp"} for i in A["top"]]
    damage_doc = None
    if rec["damage"]:
        damage_doc = {**rec["damage"], "followup": A["damage"]}
    doc = {
        "world": {k: (list(v) if isinstance(v, tuple) else v) for k, v in W.META.items()},
        "seed": seed, "steps_per_frame": spf, "dt": A["dt"], "status": rec["status"], "wall_seconds": rec["wall"],
        "damage": damage_doc, "summary": A["summary"], "warnings": warn,
        "structure": A["structure"], "radial": _radial_json(A["radial"]), "species": A["species"],
        "top_tracks": top_tracks,
        "persistent_splits": lin["persistent_splits"][:50],
        "remerged_splits": lin["remerged_splits"][:50],
        "motion_top": sorted(lin["motion"], key=lambda m: -m["body_lengths"])[:10],
        "tda_matter": A["tda"], "tda_channels": A["channel_tda"], "series": A["series"],
    }
    (out / "metrics.json").write_text(json.dumps(_strict(doc), indent=1, default=str))
    if save_frames:
        np.savez_compressed(out / "frames.npz", render=A["render"].astype(np.float16), render_f=np.array(rec["render_f"]),
                            matter=np.stack(rec["matter"]).astype(np.float16))
    log(f"  -> {out}/FACTS.md  ({rec['wall']:.0f}s sim)")
    return {"seed": seed, "status": rec["status"], **A["summary"]}


def _check_damage(frame, frac, mode="core"):
    """Reject a damage spec that cannot be applied (before anything is simulated)."""
    if mode not in DAMAGE_MODES:
        raise ValueError(f"--damage mode {mode!r}: use one of {', '.join(DAMAGE_MODES)}")
    if not 0 < float(frac) <= 1:
        raise ValueError(f"--damage FRAC {frac!r}: the fraction of the area to cut must be in (0, 1]")
    if int(frame) < 0:
        raise ValueError(f"--damage FRAME {frame!r}: the recorded frame must be >= 0")


def parse_damage(text):
    """'FRAME:FRAC[:MODE]' -> (frame, frac, mode)."""
    parts = text.split(":")
    if len(parts) not in (2, 3):
        raise argparse.ArgumentTypeError(f"--damage {text!r}: use FRAME:FRAC[:MODE]")
    mode = parts[2] if len(parts) == 3 else "core"
    try:
        try:
            frame = int(parts[0])
        except ValueError:
            raise ValueError(f"--damage FRAME {parts[0]!r}: the recorded frame must be an integer") from None
        frac = float(parts[1])
        _check_damage(frame, frac, mode)
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e) if str(e).startswith("--damage") else f"--damage {text!r}: {e}")
    return frame, frac, mode


def _arg(fn):
    """argparse type from a validator (ValueError -> a clean usage error)."""
    def parse(text):
        try:
            return fn(text)
        except ValueError as e:
            raise argparse.ArgumentTypeError(str(e) if str(e).startswith("--") else f"{text!r}: {e}")
    parse.__name__ = getattr(fn, "__name__", "value")
    return parse


def _strict(o):
    """JSON-safe copy: numpy -> Python, non-finite floats -> None (metrics.json stays strict JSON)."""
    if isinstance(o, dict):
        return {(k.item() if isinstance(k, np.generic) else k): _strict(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, set)):
        return [_strict(v) for v in o]
    if isinstance(o, np.ndarray):
        return _strict(o.tolist())
    if isinstance(o, np.generic):
        o = o.item()
    if isinstance(o, float) and not np.isfinite(o):
        return None
    return o


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("world")
    ap.add_argument("--out", required=True)
    ap.add_argument("--seeds", type=int, nargs="+", default=[0])
    ap.add_argument("--frames", type=int, default=200)
    ap.add_argument("--spf", type=int, default=None)
    ap.add_argument("--size", type=int, nargs=2, default=None)
    ap.add_argument("--damage", type=parse_damage, default=None,
                    help="FRAME:FRAC[:MODE] cut a mature compact individual; MODE core (default), rim or half")
    ap.add_argument("--lineage-k", type=_arg(lambda v: _lineage_k({}, int(v))[0]), default=None,
                    help="lineage window K in recorded frames, integer >= 1 (default 20)")
    ap.add_argument("--dt", type=_arg(lambda v: _check_dt(float(v), "--dt")), default=None,
                    help="time per internal step for REPORTING only, > 0 (overrides META dt; the integration "
                         "step is unchanged, so this is not a time-step test)")
    ap.add_argument("--threshold", type=float, default=None, help="absolute matter threshold")
    ap.add_argument("--min-area", type=int, default=None)
    ap.add_argument("--no-movie", action="store_true")
    a = ap.parse_args(argv)
    args_line = "python -m labkit.run " + " ".join(sys.argv[1:] if argv is None else argv)
    rows = []
    for s in a.seeds:
        out = Path(a.out) / (f"seed{s}" if len(a.seeds) > 1 else "")
        rows.append(run_pack(a.world, out, s, a.frames, a.spf, a.size, a.damage, not a.no_movie, a.threshold,
                             a.min_area, args_line=args_line, lineage_k=a.lineage_k, dt=a.dt))
    if len(a.seeds) > 1:
        keys = ["status", "components_final", "persistent_tracks", "longest_track_frames", "enclosed_components_final",
                "moving_tracks", "persistent_splits", "max_generation", "merge_split_ratio", "occupancy_final",
                "membrane_like_channels"]
        lines = ["| seed | " + " | ".join(keys) + " |", "|" + "---|" * (len(keys) + 1)]
        for r in rows:
            lines.append(f"| {r['seed']} | " + " | ".join(str(round(r[k], 2) if isinstance(r.get(k), float) else r.get(k, "-")) for k in keys) + " |")
        (Path(a.out) / "SUMMARY.md").write_text(f"# {a.world} across seeds\n\n" + "\n".join(lines) + "\n")
        print("\n".join(lines))


if __name__ == "__main__":
    main()
