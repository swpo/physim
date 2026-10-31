"""Behaviour and direction measures of one behav.py record (128^2 world-unit frames).

python analyze.py RUN.npz [...]  -> RUN.json next to each record

labkit's own pipeline (normalize, segment, track, lineage_stats with K=20 frames) on the
recorded matter: fv |omega| with META threshold 0.06; pm K + L + 4 phi (1 - phi) at the
default 0.35 relative threshold. Direction statistics use A4 = <cos 4 theta>: +1 for grid
axes, -1 for diagonals, 0 for no preference (theta: division axis between the two daughters'
centroids, track displacement over 5 frames, long axis of elongated bodies).
"""
import json
import sys

import numpy as np

import cc
from labkit import metrics as M
from labkit import run as R

K = 20


def wrap(d, L=cc.N0):
    return (d + L / 2) % L - L / 2


def a4(theta, w=None):
    theta = np.asarray(theta, float)
    if theta.size == 0:
        return dict(A4=None, n=0, se=None)
    w = np.ones_like(theta) if w is None else np.asarray(w, float)
    c = np.cos(4 * theta)
    m = float((w * c).sum() / w.sum())
    neff = w.sum() ** 2 / (w ** 2).sum()
    return dict(A4=round(m, 3), n=int(theta.size), se=round(float(np.sqrt(max(((w * (c - m) ** 2).sum() / w.sum()), 1e-12) / neff)), 3))


def elongation(seg, stride_ok=True):
    """(theta, aspect) of each component with area >= 20 px, periodic second moments."""
    out = []
    lab, n = seg["lab"], seg["n"]
    H, W = lab.shape
    yy, xx = np.indices(lab.shape)
    for i in range(1, n + 1):
        if seg["area"][i - 1] < 20:
            continue
        m = lab == i
        dy = wrap(yy[m] - seg["cy"][i - 1], H)
        dx = wrap(xx[m] - seg["cx"][i - 1], W)
        C = np.cov(np.stack([dx, dy]))
        ev, evec = np.linalg.eigh(C)
        if ev[0] <= 0:
            continue
        v = evec[:, 1]
        out.append((float(np.arctan2(v[1], v[0])), float(np.sqrt(ev[1] / ev[0]))))
    return out


def analyze(path):
    z = np.load(path)
    meta = json.loads(str(z["meta"]))
    rec = z["rec"]
    world = meta["world"]
    W = cc.load(world)
    fdt = meta["fdt"]
    if world == "fv":
        om = rec.astype(np.float64)
        mat = np.abs(om).astype(np.float32)
        thr_abs = W.META.get("threshold")
    else:
        mat = rec[:, 0]
        thr_abs = None
    T = len(mat)
    mn, thr, lo, hi = R._normalize_matter(mat, W.META, True, thr_abs)
    H, Wd = mn.shape[1:]
    min_area = R._default_min_area(H, Wd)
    comps, links = R._segment_frames(mn, thr, min_area, True, keep_labels=True)
    tracks, events = M.track(comps, links, (H, Wd), True)
    lin = M.lineage_stats(tracks, events, T, fdt, (H, Wd), True, K=K)
    life = lin["lifetimes"]
    ps = lin["persistent_splits"]
    splits = [e for e in events if e["type"] == "split"]
    merges = [e for e in events if e["type"] == "merge"]
    gen = lin["generation"]

    def centroid(tid, k=0):
        t = tracks[tid]
        k = min(k, len(t["cy"]) - 1)
        return t["cy"][k], t["cx"][k]

    def axis(e):
        ch = e.get("surviving_children") or e["children"]
        ch = sorted(ch, key=lambda c: -tracks[c]["area"][0])[:2]
        if len(ch) < 2:
            return None
        (y1, x1), (y2, x2) = centroid(ch[0]), centroid(ch[1])
        return float(np.arctan2(wrap(y2 - y1), wrap(x2 - x1)))

    res = dict(meta=meta, frames=T, threshold_rel=float(thr), components_final=int(comps[-1]["n"]),
               components_mean=float(np.mean([c["n"] for c in comps])), tracks=len(tracks),
               splits=len(splits), persistent_splits=len(ps), merges=len(merges),
               merge_split_ratio=round(len(merges) / max(len(splits), 1), 3),
               max_generation=int(lin["max_generation"]),
               ps_times=[float(e["frame"] * fdt) for e in ps])
    for tcut in (600, 1200, 1500, 4000, 8000):
        if tcut <= meta["T"] + 1e-9:
            res[f"ps_by_{tcut}"] = int(sum(e["frame"] * fdt <= tcut for e in ps))
            res[f"maxgen_by_{tcut}"] = int(max([max(gen[c] for c in e["surviving_children"]) for e in ps
                                                if e["frame"] * fdt <= tcut] or [0]))
    # direction statistics
    ax_ps = [a for a in map(axis, ps) if a is not None]
    ax_all = [a for a in map(axis, splits) if a is not None]
    res["division_axis_persistent"] = a4(ax_ps)
    res["division_axis_all_splits"] = a4(ax_all)
    lag = 5
    ang, wts, speeds = [], [], []
    for t in tracks:
        L = len(t["cy"])
        if L < max(K, lag + 1):
            continue
        cy, cx = np.asarray(t["cy"]), np.asarray(t["cx"])
        for k0 in range(0, L - lag, lag):
            dy, dx = wrap(cy[k0 + lag] - cy[k0]), wrap(cx[k0 + lag] - cx[k0])
            d = np.hypot(dy, dx)
            if d > 0:
                ang.append(np.arctan2(dy, dx)); wts.append(d)
        speeds.append(float(np.hypot(wrap(np.diff(cy)), wrap(np.diff(cx))).sum() / ((L - 1) * fdt)))
    res["motion_direction"] = a4(ang, wts)
    res["motion"] = dict(tracks_ge_K=len(speeds), median_path_speed=round(float(np.median(speeds)), 4) if speeds else None,
                         moving_tracks=int(sum(1 for m in lin["motion"] if m["body_lengths"] >= 1.0 and life[m["id"]] >= K)),
                         median_disp_per_frame=round(float(np.median(wts)) / lag, 4) if wts else None)
    el = []
    for f in range(0, T, 5):
        el += [x for x in elongation(comps[f]) if x[1] > 1.5]
    res["elongation_axis"] = a4([x[0] for x in el])
    res["elongation_axis"]["median_aspect"] = round(float(np.median([x[1] for x in el])), 3) if el else None
    if world == "fv":
        def sign(tid):
            t = tracks[tid]
            k = min(2, len(t["comp"]) - 1)
            f = t["start"] + k
            m = comps[f]["lab"] == t["comp"][k] + 1
            return int(np.sign(om[f][m].sum()))
        same = other = 0
        for e in ps:
            sp = sign(e["parent"]) if len(tracks[e["parent"]]["comp"]) else 0
            # parent's sign at its last frame
            t = tracks[e["parent"]]; f = t["end"]; m = comps[f]["lab"] == t["comp"][-1] + 1
            sp = int(np.sign(om[f][m].sum()))
            sc = [sign(c) for c in e["surviving_children"]]
            if sp and all(x == sp for x in sc):
                same += 1
            else:
                other += 1
        msame = mopp = 0
        for e in merges:
            ss = []
            for p in e.get("parents", []):
                t = tracks[p]; f = t["end"]; m = comps[f]["lab"] == t["comp"][-1] + 1
                ss.append(int(np.sign(om[f][m].sum())))
            if len(set(ss)) == 1:
                msame += 1
            else:
                mopp += 1
        res["daughters_same_sign"] = same
        res["daughters_not_same_sign"] = other
        res["merges_same_sign"], res["merges_opposite_sign"] = msame, mopp
        res["bodies_by_time"] = {str(int(f * fdt)): int(comps[f]["n"]) for f in range(0, T, max(1, (T - 1) // 10))}
    else:
        census = json.loads(str(z["census"]))
        rings = [c["ring_median"] for c in census if c["ring_median"] is not None and c["t"] % 1000 == 0]
        res["ring_median_over_t"] = round(float(np.median(rings)), 3) if rings else None
        res["ring_range"] = [round(min(rings), 3), round(max(rings), 3)] if rings else None
        res["rim_over_out_median"] = round(float(np.median([c["rim_over_out"] for c in census if c["rim_over_out"]])), 2)
        res["wall_A4_mean"] = round(float(np.mean([c["wall_A4"] for c in census])), 3)
        res["wall_A4_range"] = [round(min(c["wall_A4"] for c in census), 3), round(max(c["wall_A4"] for c in census), 3)]
        res["cells_by_census"] = [c["cells"] for c in census if c["t"] % 1000 == 0]
        res["bodies_by_time"] = {str(int(f * fdt)): int(comps[f]["n"]) for f in range(0, T, 20)}
    out = path.replace(".npz", ".json")
    json.dump(res, open(out, "w"), indent=1)
    return res


if __name__ == "__main__":
    for p in sys.argv[1:]:
        r = analyze(p)
        keep = ["persistent_splits", "max_generation", "merge_split_ratio", "components_final",
                "division_axis_persistent", "division_axis_all_splits", "motion_direction", "elongation_axis",
                "motion", "daughters_same_sign", "daughters_not_same_sign", "ring_median_over_t", "wall_A4_mean"]
        print(p.split("/")[-1], json.dumps({k: r[k] for k in keep if k in r}))
