"""Cargo containment per body and per frame, by signed distance to the body contour.

Bodies are labkit's own components (same normalization, threshold, min area, periodic labels,
tracking and persistent-split lineage, recomputed from the run's frames.npz with labkit's code), so
the bodies and daughters are exactly the ones labkit's FACTS/lineage count.

For each body (area >= MINA px) in each recorded frame:
  inside  = the body's pixels at Euclidean distance >= DIN px from the nearest non-body pixel
            (the interior beyond ~2 px of the contour; for small bodies with no such pixel the
            interior falls back to distance >= 1.5 px and the body-frame is flagged "small");
  outside = background pixels at distance DOUT0..DOUT1 px from the nearest body pixel, whose
            nearest body pixel belongs to THIS body (a Voronoi-split band a few px outside the
            contour; the q ring sits inside the contour at rho ~0.75, so this band is outside it).
  ratio   = mean c inside / mean c outside.
Daughters: for every persistent split (labkit definition), each surviving child is measured
DAUGHTER_LAG frames after the split (if the child track has itself split or ended by then, its
largest split-descendant alive at that frame is used).

Usage: measure_w.py <pack_dir> [<label>]   (prints a summary line block and writes <pack_dir>/w_measure.json)
"""
import sys, json
import numpy as np
from scipy import ndimage

sys.path.insert(0, "/home/user/physim/research/alife")
sys.dont_write_bytecode = True
from labkit import metrics as M          # noqa: E402
from labkit import run as LR             # noqa: E402

MINA, DIN, DOUT0, DOUT1, F0, DAUGHTER_LAG, PAD = 12, 2.5, 2.5, 5.5, 5, 5, 16
import os  # optional overrides for a band-sensitivity check: W_DIN, W_DOUT0, W_DOUT1, W_TAG (output w_measure<TAG>.json)
DIN, DOUT0, DOUT1 = (float(os.environ.get(k, v)) for k, v in (("W_DIN", DIN), ("W_DOUT0", DOUT0), ("W_DOUT1", DOUT1)))
TAG = os.environ.get("W_TAG", "")
CARGO, SHELL = 1, 2


def periodic_edt(mask, pad=PAD, return_indices=False):
    """EDT of a periodic mask (distance from each True pixel to the nearest False pixel)."""
    mp = np.pad(mask, pad, mode="wrap")
    if return_indices:
        d, ind = ndimage.distance_transform_edt(mp, return_indices=True)
        return d[pad:-pad, pad:-pad], ind[:, pad:-pad, pad:-pad]
    return ndimage.distance_transform_edt(mp)[pad:-pad, pad:-pad]


def frame_ratios(lab, n, c, q=None):
    """Per-component (in, out, ratio, small_flag, area, q_in, q_out)."""
    H, W = lab.shape
    body = lab > 0
    din = periodic_edt(body)
    labp = np.pad(lab, PAD, mode="wrap")
    dout, ind = periodic_edt(~body, return_indices=True)
    nearest = labp[ind[0], ind[1]]  # label of the nearest body pixel (periodic via padding)
    res = {}
    area = np.bincount(lab.ravel(), minlength=n + 1)
    band_all = (~body) & (dout >= DOUT0) & (dout <= DOUT1)
    for k in range(1, n + 1):
        if area[k] < MINA:
            continue
        m = lab == k
        inn = m & (din >= DIN)
        small = False
        if inn.sum() < 1:
            inn = m & (din >= 1.5)
            small = True
        if inn.sum() < 1:
            continue
        band = band_all & (nearest == k)
        if band.sum() < 4:
            continue
        ci, co = float(c[inn].mean()), float(c[band].mean())
        qi = qo = None
        if q is not None:
            qi, qo = float(q[inn].mean()), float(q[band].mean())
        res[k] = (ci, co, ci / max(co, 1e-12), small, int(area[k]), qi, qo)
    return res


def main(pack, label=None):
    F = np.load(pack + "/frames.npz")
    R, rf, mat = F["render"].astype(np.float32), list(F["render_f"]), F["matter"].astype(np.float32)
    meta = json.load(open(pack + "/metrics.json"))
    wmeta = meta["world"]
    periodic = wmeta.get("periodic", True)
    mn, thr, lo, hi = LR._normalize_matter(mat, wmeta, periodic, wmeta.get("threshold"))  # labkit honours META threshold
    T, H, W = mn.shape
    min_area = meta["summary"]["min_area"]
    comps, links = LR._segment_frames(mn, thr, min_area, periodic)
    tracks, events = M.track(comps, links, (H, W), periodic)
    lin = M.lineage_stats(tracks, events, T, 1.0, (H, W), periodic, K=meta["summary"]["K_frames"])
    assert len(rf) == T and rf == list(range(T)), "expects every frame rendered"
    per = {}  # (frame, comp) -> tuple
    for f in range(1, T):
        r = frame_ratios(comps[f]["lab"], comps[f]["n"], R[f, CARGO], R[f, SHELL])
        for k, v in r.items():
            per[(f, k - 1)] = v  # labkit comp index = label - 1
    rows = [(f, k, *v) for (f, k), v in per.items() if f >= F0]
    ratios = np.array([r[4] for r in rows])
    late = np.array([r[4] for r in rows if r[0] >= 30])
    qin = np.array([r[7] for r in rows]); qout = np.array([r[8] for r in rows])
    # per-track share of life >= 2x (tracks alive >= 10 measured frames)
    life_ok = []
    for t in tracks:
        v = [per[(t["start"] + i, ci)][2] for i, ci in enumerate(t["comp"]) if (t["start"] + i, ci) in per and t["start"] + i >= F0]
        if len(v) >= 10:
            life_ok.append(np.mean(np.array(v) >= 2) > 0.5)
    # daughters
    dres = []
    for e in lin["persistent_splits"]:
        f1 = e["frame"] + DAUGHTER_LAG
        if f1 >= T:
            continue
        for ch in e["surviving_children"]:
            cand = [d for d in M.descendants(tracks, ch, f1) if tracks[d]["start"] <= f1 <= tracks[d]["end"]]
            cand = [d for d in cand if d == ch or tracks[d]["birth"] == "split"]
            if not cand:
                continue
            best = max(cand, key=lambda d: tracks[d]["area"][f1 - tracks[d]["start"]])
            ci = tracks[best]["comp"][f1 - tracks[best]["start"]]
            if (f1, ci) in per:
                dres.append((e["frame"], ch, best, per[(f1, ci)][2]))
    dr = np.array([d[3] for d in dres])
    out = {
        "pack": pack, "label": label or pack, "threshold_rel": thr, "range": [lo, hi],
        "n_body_frames": int(len(ratios)), "frames_from": F0,
        "median_in_out": float(np.median(ratios)), "share_ge2": float(np.mean(ratios >= 2)),
        "p10_in_out": float(np.percentile(ratios, 10)), "p90_in_out": float(np.percentile(ratios, 90)),
        "late_n": int(len(late)), "late_median": float(np.median(late)), "late_share_ge2": float(np.mean(late >= 2)),
        "small_share": float(np.mean([r[5] for r in rows])),
        "median_q_in": float(np.median(qin)), "median_q_out": float(np.median(qout)),
        "tracks_ge2_most_life": [int(np.sum(life_ok)), len(life_ok)],
        "persistent_splits": len(lin["persistent_splits"]), "max_generation": int(lin["max_generation"]),
        "daughters_n": int(len(dr)), "daughters_ge2": int(np.sum(dr >= 2)) if len(dr) else 0,
        "daughters_median": float(np.median(dr)) if len(dr) else None,
        "daughters_min": float(dr.min()) if len(dr) else None,
        "daughters_p10": float(np.percentile(dr, 10)) if len(dr) else None,
        "daughters": [[int(a), int(b), int(c_), float(v)] for a, b, c_, v in dres],
        "per_frame": {int(f): [float(np.median([r[4] for r in rows if r[0] == f])),
                               float(np.mean([r[4] >= 2 for r in rows if r[0] == f])),
                               int(sum(1 for r in rows if r[0] == f))]
                      for f in range(F0, T, 5) if any(r[0] == f for r in rows)},
    }
    json.dump(out, open(pack + "/w_measure" + TAG + ".json", "w"), indent=1)
    print(f"== {out['label']}: body-frames {out['n_body_frames']} (frames >= {F0}); median in/out {out['median_in_out']:.2f} "
          f"(p10 {out['p10_in_out']:.2f}, p90 {out['p90_in_out']:.2f}); share >= 2x {out['share_ge2']:.3f}; "
          f"t>=120: median {out['late_median']:.2f}, share {out['late_share_ge2']:.3f}; "
          f"tracks >=2x most of life {out['tracks_ge2_most_life']}; daughters >=2x at +{DAUGHTER_LAG}: "
          f"{out['daughters_ge2']}/{out['daughters_n']} (median {out['daughters_median']}); "
          f"persistent splits {out['persistent_splits']}, max gen {out['max_generation']}; "
          f"median q in/out {out['median_q_in']:.3f}/{out['median_q_out']:.3f}; small-body fallback {out['small_share']:.2f}")
    for f, v in out["per_frame"].items():
        print(f"   frame {f:3d}: median {v[0]:6.2f}  share>=2 {v[1]:.2f}  bodies {v[2]}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
