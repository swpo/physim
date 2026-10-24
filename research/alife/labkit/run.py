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
    --damage FRAME:FRAC[:MODE]  cut a MATURE, COMPACT individual at recorded frame FRAME
                    (see labkit/metrics.py for the target rule). MODE: core (centred disk,
                    default), rim (disk centred on the boundary, breaches a membrane) or
                    half (half-plane cut). FRAC is the requested fraction of its area; FACTS
                    reports the matter fraction ACTUALLY lost, whatever the world hook does.
    --lineage-k K   lineage window in recorded frames (default META "lineage_k", else 20).
    --dt DT         time per internal step for reporting (overrides META dt; the world's
                    own numerics are untouched).
Optional META keys: "lineage_k", "radial_channels" (channels for radial.png, default all),
"species" ({name: [channels]}: separate tracking and lineage per species).
Runs never write __pycache__ (sys.dont_write_bytecode), so read-only mirrors stay clean.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # never write __pycache__ next to world files (read-only mirrors)

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
    return {str(k): _channel_list(v, names, C, "species") for k, v in sp.items()}


def _lineage_k(meta, K=None):
    """(K, source): CLI --lineage-k > META lineage_k > labkit default."""
    if K is not None:
        return int(K), "--lineage-k"
    if meta.get("lineage_k") is not None:
        return int(meta["lineage_k"]), "META lineage_k"
    return M.LINEAGE_K, "default"


def _default_min_area(H, W):
    return max(6, int(H * W / 20000))


def _normalize_matter(mat, meta, periodic, threshold=None):
    """Robust-range normalization (+ light blur) of a (T, H, W) matter stack; returns mn, thr, lo, hi."""
    T = len(mat)
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
    mn, thr, _, _ = _normalize_matter(np.stack(rec["matter"] + [m0]), W.META, periodic, threshold)
    H, Wd = m0.shape
    comps, links = _segment_frames(mn, thr, min_area or _default_min_area(H, Wd), periodic, keep_labels=False)
    tracks, _ = M.track(comps, links, (H, Wd), periodic)
    f, seg = len(comps) - 1, comps[-1]
    spans = np.zeros(seg["n"], int)
    for t in tracks:
        if t["end"] == f:
            spans[t["comp"][-1]] = f - t["start"] + 1
    j, rule, asp = M.choose_damage_target(seg, spans, K, periodic)
    if j is None:
        info["error"] = "no components at the damage frame: nothing was erased"
        return state, info, None
    q = M.choose_comparator(seg, j, spans, K, periodic)
    mask, minfo = M.damage_mask(seg, j, frac, mode, periodic)
    target = seg["lab"] == j + 1
    state = W.damage(state, mask)
    m1 = _matter(W, _fields(W, state))
    lost = m0 - m1
    before = float(m0[target].sum())
    info.update({
        "rule": rule, "track_age_frames": int(spans[j]), "component_area": float(seg["area"][j]),
        "median_area": float(np.median(seg["area"])), "n_components": int(seg["n"]),
        "aspect": round(float(asp[j]), 3), "cy": float(seg["cy"][j]), "cx": float(seg["cx"][j]),
        **minfo,
        "mask_px": int(mask.sum()), "mask_px_in_component": int((mask & target).sum()),
        # MEASURED, whatever the hook did with the mask:
        "erased_frac": float(lost[target].sum() / before) if before > 0 else None,
        "erased_px": int(((lost > 0.5 * m0) & target).sum()),  # component px that lost > half their matter
        "lost_outside_frac": float(lost[~target].sum() / before) if before > 0 else None,
        "lost_under_mask_share": float(lost[mask].sum() / lost.sum()) if lost.sum() > 0 else None,
        "comparator_area": float(seg["area"][q]) if q is not None else None,
        "comparator_cy": float(seg["cy"][q]) if q is not None else None,
        "comparator_cx": float(seg["cx"][q]) if q is not None else None,
    })
    arrays = {"pre": F.astype(np.float16), "mask": mask, "target": target,
              "comparator": (seg["lab"] == q + 1) if q is not None else None}
    return state, info, arrays


def simulate(W, seed, frames, spf, size, render_max=120, damage=None, log=print, K=None, periodic=True,
             threshold=None, min_area=None):
    """Advance the world, keeping every matter field and up to render_max full frames."""
    if damage is not None and len(damage) == 2:
        damage = (damage[0], damage[1], "core")
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
        if species is None:
            species = _species(W.META, F.shape[0])
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


def _radial(meta, rec, comps, tracks, top, render, scales, min_area, periodic):
    """Per-channel radial profiles: top tracks at mid-life and an aggregate over individuals."""
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
        seg = comps[f]
        return M.radial_profile(norm(k), seg["cy"][j], seg["cx"][j], np.sqrt(seg["area"][j] / np.pi), periodic)[0]

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
        p = prof(k, f, j)
        per_track.append({"track": int(i), "frame": int(f), "area": float(comps[f]["area"][j]),
                          "R_eq": round(float(np.sqrt(comps[f]["area"][j] / np.pi)), 2), "profile": p, "scores": scores(p)})
    ks = [k for k in np.unique(np.linspace(0, len(rf) - 1, 7).round().astype(int)) if k > 0] or [0]
    profs, who = [], []
    for k in ks:
        f = rf[k]
        for j in range(comps[f]["n"]):
            if comps[f]["area"][j] >= 2 * min_area:
                profs.append(prof(k, f, j))
                who.append((int(f), int(j)))
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
               "mean": mean, "std": std, "scores": sc, "n_membrane_like_individually": indiv}
    membrane = [names[c] for c in sel if agg and agg["scores"][names[c]] and agg["scores"][names[c]]["membrane_like"]]
    return {"rho": [round(float(r), 3) for r in M.RHO], "channels": [names[c] for c in sel], "channel_index": sel,
            "bands": {"core": list(M.CORE_RHO), "rim": list(M.RIM_RHO), "outside": list(M.OUT_RHO), "peak": list(M.PEAK_RHO)},
            "eps": M.RATIO_EPS, "cap": M.RATIO_CAP, "membrane_ratio": M.MEMBRANE_RATIO,
            "aggregate": agg, "tracks": per_track, "membrane_like": membrane, "_profiles": profs}


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


def _track_at(comps, tracks, mask, f):
    """Track owning the frame-f component that overlaps `mask` most (None if no overlap)."""
    if mask is None:
        return None
    ids = comps[f]["lab"][mask]
    ids = ids[ids > 0]
    if not len(ids):
        return None
    j = int(np.bincount(ids).argmax()) - 1
    for t in tracks:
        if t["start"] <= f <= t["end"] and t["comp"][f - t["start"]] == j:
            return t["id"]
    return None


def _follow(tracks, tid, f, split_only=True):
    """Largest descendant of tid alive at frame f as (track id, area, cy, cx), and the number alive.

    split_only: the lineage as in lineage_stats (a merge ends it); else also through merges.
    """
    alive = []
    for i in M.descendants(tracks, tid, f, split_only):
        t = tracks[i]
        if t["start"] <= f <= t["end"]:
            k = f - t["start"]
            alive.append((t["area"][k], i, t["cy"][k], t["cx"][k]))
    if not alive:
        return None, 0
    a, i, cy, cx = max(alive)
    return (i, float(a), float(cy), float(cx)), len(alive)


def _damage_followup(rec, comps, tracks, T):
    d, arr = rec["damage"], rec["damage_arrays"]
    if not d or arr is None:
        return None
    f0 = d["frame"]
    fp = max(f0 - 1, 0)  # the last recorded frame before the cut
    out = {"target_track": _track_at(comps, tracks, arr["target"], fp),
           "comparator_track": _track_at(comps, tracks, arr["comparator"], fp)}
    for key in ("target", "comparator"):
        tid = out[f"{key}_track"]
        if tid is None:
            continue
        t = tracks[tid]
        a0 = float(t["area"][fp - t["start"]])
        rel, pieces = [], []
        for f in range(f0, T):
            big, n = _follow(tracks, tid, f)
            rel.append(None if big is None else round(big[1] / a0, 3))
            pieces.append(n)
        out[f"{key}_area_pre"] = a0
        out[f"{key}_area_rel"] = rel  # largest split-descendant area / area just before the cut, frames f0..end
        out[f"{key}_pieces"] = pieces  # split-descendants alive per frame (None area = lineage ended or merged)
        out[f"{key}_descendants"] = sorted(M.descendants(tracks, tid, split_only=True) - {tid})
    return out


def analyze(W, rec, spf, periodic=True, threshold=None, min_area=None, K=None, dt=None):
    meta = W.META
    dt = float(meta["dt"] if dt is None else dt)
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
    radial = _radial(meta, rec, comps, tracks, top, render, scales, min_area, periodic)
    species = _species_stats(meta, rec, periodic, min_area, K, dt_frame, (H, Wd)) if rec.get("species") else {}
    dmg = _damage_followup(rec, comps, tracks, T)

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
        "radial": radial, "species": species, "damage": dmg, "dt": dt, "dt_frame": dt_frame,
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
    d, fu = rec["damage"], A["damage"]
    if not fu or fu["target_track"] is None:
        return
    tracks, rf, scales, dt_frame = A["tracks"], rec["render_f"], A["scales"], A["dt_frame"]
    arr = rec["damage_arrays"]
    H, Wd = rgb[0].shape[:2]
    f0 = d["frame"]
    post = [k for k, f in enumerate(rf) if f >= f0]
    sel = [post[int(i)] for i in np.unique(np.linspace(0, len(post) - 1, min(8, len(post))).round().astype(int))]
    area = max(d["component_area"], d.get("comparator_area") or 0)
    half = int(np.clip(2.0 * np.sqrt(area / np.pi) + 6, 12, min(H, Wd) // 2))
    pre_rgb = R.composite(R.normalize(arr["pre"].astype(np.float32), scales))
    tiles, labels = [], []

    def tile(img, cy, cx):
        return np.asarray(R.Image.fromarray(R.crop_periodic(img, cy, cx, half)).resize((112, 112), R.Image.NEAREST))

    for key, cy0, cx0 in (("target", d["cy"], d["cx"]), ("comparator", d.get("comparator_cy"), d.get("comparator_cx"))):
        tid = fu[f"{key}_track"]
        if tid is None:
            continue
        img = R.outline(pre_rgb, arr["mask"]) if key == "target" else pre_rgb
        tiles.append(tile(img, cy0, cx0))
        labels.append(f"#{tid} pre t={f0 * dt_frame:g}")
        for k in sel:
            big, nalive = _follow(tracks, tid, rf[k])
            if big is not None and rf[k] == f0:  # the frame just after the cut: same framing as "pre"
                big = (big[0], big[1], cy0, cx0)
            tag = ""
            if big is None:  # lineage ended: keep the camera on what it merged into, if anything
                big, _ = _follow(tracks, tid, rf[k], split_only=False)
                tag = "into "
            if big is None:
                tiles.append(np.zeros((112, 112, 3), np.uint8))
                labels.append(f"gone t={rf[k] * dt_frame:g}")
                continue
            tiles.append(tile(rgb[k], big[2], big[3]))
            labels.append(f"{tag}#{big[0]}{'+' + str(nalive - 1) if nalive > 1 else ''} t={rf[k] * dt_frame:g}")
    loss = d.get("erased_frac")
    title = (f"damage {d['mode']} {d['frac_requested']:.2f} t={f0 * dt_frame:g}: top target #{fu['target_track']} "
             f"(lost {'?' if loss is None else f'{loss:.0%}'} of matter, red = cut) + split-descendants; "
             f"bottom comparator #{fu['comparator_track']}")
    R.contact_sheet(tiles, labels, ncols=len(sel) + 1, title=title).save(out / "damage.png")


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
    if rows:
        R.contact_sheet(rows, labels, ncols=8, title="most persistent individuals (fixed crops follow the tracked centroid)").save(out / "tracks.png")
    _radial_figure(meta, A, out)
    if rec.get("damage"):
        _damage_figure(meta, rec, A, rgb, out)

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

    if movie:
        R.save_movie(rgb, str(out / "movie.mp4"), fps=15)


# ------------------------------------------------------------------ facts
def _radial_facts(A):
    rad, lines = A["radial"], []
    agg = rad["aggregate"]
    if not agg:
        return [f"- radial profiles: no component with area >= {2 * A['summary']['min_area']} px at the sampled frames"]
    lines.append(f"- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, "
                 f"rim 0.6-1.3, outside 1.6-2.2; aggregate of {agg['n_individuals']} components >= {agg['min_area']} px "
                 f"at frames {agg['frames']}):")
    for name in rad["channels"]:
        sc = agg["scores"][name]
        if not sc:
            lines.append(f"  - radial {name}: empty profile")
            continue
        lines.append(f"  - radial {name}: peak at rho={sc['rho_peak']:.2f}, rim/core {_g(sc['rim_core'])}, "
                     f"rim/outside {_g(sc['rim_outside'])} (aggregate of {agg['n_individuals']} individuals; "
                     f"{agg['n_membrane_like_individually'][name]}/{agg['n_individuals']} membrane-like individually; "
                     f"rim level {_g(sc['rim_max'])})" + ("  MEMBRANE-LIKE" if sc["membrane_like"] else ""))
    ml = rad["membrane_like"]
    lines.append(f"- membrane-like channels (aggregate rim/core >= {M.MEMBRANE_RATIO:g} and rim/outside >= "
                 f"{M.MEMBRANE_RATIO:g}): {', '.join(ml) if ml else 'none'}")
    if rad["tracks"]:
        per = "; ".join(f"#{t['track']} (t={t['frame'] * A['dt_frame']:g}, R_eq {t['R_eq']:g}): "
                        f"{[n for n, s in t['scores'].items() if s and s['membrane_like']] or 'none'}" for t in rad["tracks"])
        lines.append(f"- membrane-like channels per top track at mid-life: {per}")
    return lines


def _damage_facts(A, rec, warn):
    d, fu, dt_frame = rec["damage"], A["damage"], A["dt_frame"]
    if d.get("error"):
        warn.append(f"damage requested but not applied: {d['error']}")
        return [f"- damage ({d['mode']}, {d['frac_requested']:.2f}) at frame {d['frame']}: NOT APPLIED ({d['error']})"]
    loss = d["erased_frac"]
    lines = [
        f"- damage `{d['mode']}` (requested {d['frac_requested']:.2f} of the area) at frame {d['frame']} "
        f"(t={d['frame'] * dt_frame:g}): target track #{fu['target_track'] if fu else '?'} (rule {d['rule']}: track age "
        f"{d['track_age_frames']} frames vs K={d['K_frames']}, area {d['component_area']:.0f} px = "
        f"{d['component_area'] / max(d['median_area'], 1):.2f}x median, aspect {d['aspect']:.2f}); mask {d['mask_px']} px "
        f"({d['mask_px_in_component']} inside the component)",
        f"- damage MEASURED: the target lost {_g(None if loss is None else 100 * loss)}% of its matter "
        f"({d['erased_px']} of {d['component_area']:.0f} px lost > half their matter); matter lost outside it = "
        f"{_g(None if d['lost_outside_frac'] is None else 100 * d['lost_outside_frac'])}% of its matter; share of all lost "
        f"matter that was under labkit's mask {_g(d.get('lost_under_mask_share'))}",
    ]
    if d.get("lost_under_mask_share") is not None and d["lost_under_mask_share"] < 0.5:
        warn.append(f"the world's damage() hook did not erase where labkit's mask was (only "
                    f"{d['lost_under_mask_share']:.0%} of the lost matter was under it): the MEASURED loss is what counts")
    if d["rule"] != "mature-compact":
        warn.append(f"damage target is NOT a mature compact individual (rule {d['rule']}): no component at frame "
                    f"{d['frame']} had a track >= K={d['K_frames']} frames and an area within "
                    f"{list(M.DAMAGE_AREA_BAND)} x median; damage later or lower --lineage-k")
    if d["mode"] == "rim":
        lines.append("- (rim mode: the disk has the requested area but is centred on the boundary, so about half of it "
                     "lies outside the matter component and cuts the layer at the edge)")
    elif loss is not None and loss < 0.5 * d["frac_requested"]:
        warn.append(f"damage erased only {loss:.0%} of the target's matter against {d['frac_requested']:.0%} requested")
    if fu:
        idx = np.unique(np.linspace(0, len(fu.get("target_area_rel", [])) - 1, 6).round().astype(int)) if fu.get("target_area_rel") else []
        times = [round((d["frame"] + int(i)) * dt_frame, 3) for i in idx]
        tgt = [fu["target_area_rel"][i] for i in idx]
        cmp_ = [fu["comparator_area_rel"][i] for i in idx] if fu.get("comparator_area_rel") else None
        lines.append(f"- after damage, largest descendant area / area before the cut at t={times}: target #{fu['target_track']} "
                     f"{tgt}; comparator #{fu['comparator_track']} {cmp_ if cmp_ else 'n/a'}; target descendants "
                     f"{fu.get('target_descendants', [])[:12]} (damage.png)")
    return lines


def facts(W, rec, A, out, seed, spf, args_line):
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
    lines += _radial_facts(A)
    for name, sp in (A.get("species") or {}).items():
        lines.append(f"- species `{name}` (channels {sp['channel_names']}, own threshold): components final "
                     f"{sp['components_final']}, mean {sp['components_mean']:.1f}, max {sp['components_max']}; tracks "
                     f"{sp['tracks']}, persistent {sp['persistent_tracks']}; splits {sp['splits']}, persistent splits "
                     f"{sp['persistent_splits']} (K={K}), max generation {sp['max_generation']}, merges {sp['merges']}, "
                     f"merge/split {_g(sp['merge_split_ratio'])}; moving tracks {sp['moving_tracks']}")
    if rec.get("damage"):
        lines += _damage_facts(A, rec, warn)
    files = ["sheet.png", "tracks.png", "radial.png", "lineage.png", "timeseries.png"]
    files += ["damage.png"] if (out / "damage.png").exists() and rec.get("damage") else []
    files += ["particles.png"] if rec["particles"] else []
    lines += ["", "## Warnings"] + ([f"- {w}" for w in warn] or ["- none"])
    lines += ["", "## Files", ", ".join(files) + ", movie.mp4, metrics.json",
              "", "Measurements are screens, not verdicts: judge them against the images."]
    (out / "FACTS.md").write_text("\n".join(lines) + "\n")
    return warn


def run_pack(world_path, out, seed=0, frames=200, spf=None, size=None, damage=None, movie=True,
             threshold=None, min_area=None, save_frames=True, quiet=False, args_line="", lineage_k=None, dt=None):
    log = (lambda *a: None) if quiet else print
    W = load_world(world_path)
    spf = int(spf or W.META["steps_per_frame"])
    size = tuple(size or W.META["size"])
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "damage.png").unlink(missing_ok=True)  # never leave a stale damage figure from an older run
    log(f"[{W.META['name']}] seed {seed}: {frames} frames x {spf} steps, grid {size}")
    periodic = W.META.get("periodic", True)
    K = _lineage_k(W.META, lineage_k)[0]
    rec = simulate(W, seed, frames, spf, size, damage=damage, log=log, K=K, periodic=periodic,
                   threshold=threshold, min_area=min_area)
    if len(rec["matter"]) < 2:
        (out / "FACTS.md").write_text(f"# {W.META['name']} seed {seed}\n\nRUN FAILED: {rec['status']}\n")
        return {"seed": seed, "status": rec["status"]}
    A = analyze(W, rec, spf, periodic, threshold, min_area, K=lineage_k, dt=dt)
    figures(W, rec, A, out, spf, movie)
    warn = facts(W, rec, A, out, seed, spf, args_line)
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
    (out / "metrics.json").write_text(json.dumps(doc, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)))
    if save_frames:
        np.savez_compressed(out / "frames.npz", render=A["render"].astype(np.float16), render_f=np.array(rec["render_f"]),
                            matter=np.stack(rec["matter"]).astype(np.float16))
    log(f"  -> {out}/FACTS.md  ({rec['wall']:.0f}s sim)")
    return {"seed": seed, "status": rec["status"], **A["summary"]}


def parse_damage(text):
    """'FRAME:FRAC[:MODE]' -> (frame, frac, mode)."""
    parts = text.split(":")
    if len(parts) not in (2, 3):
        raise argparse.ArgumentTypeError(f"--damage {text!r}: use FRAME:FRAC[:MODE]")
    mode = parts[2] if len(parts) == 3 else "core"
    if mode not in DAMAGE_MODES:
        raise argparse.ArgumentTypeError(f"--damage mode {mode!r}: use one of {', '.join(DAMAGE_MODES)}")
    return int(float(parts[0])), float(parts[1]), mode


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
    ap.add_argument("--lineage-k", type=int, default=None, help="lineage window K in recorded frames (default 20)")
    ap.add_argument("--dt", type=float, default=None, help="time per internal step for reporting (overrides META dt)")
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
