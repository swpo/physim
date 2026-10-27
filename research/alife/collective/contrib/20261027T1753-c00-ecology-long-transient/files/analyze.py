"""c00 long-transient test of c52's coexistence: per-run time series from a labkit pack.

usage: analyze.py <pack dir> [<pack dir> ...]    (writes <pack>/long.json)

From metrics.json (labkit per-species tracking on every recorded frame, frame = 100 t, K = 20 frames):
  prey / predator body counts n(t), persistent splits per 6000-t window (labkit persistent_split_frames).
  NOTE: a persistent split needs K = 20 frames (2000 t) of survival after it, so the last 2000 t of a run can
  hold none; the last window [42000, 48000) is therefore eligible only for 4000 t and is also given as a rate.
From frames.npz render (every 4th frame = 400 t, all 5 channels): an absolute-threshold cross-check
  (c > 0.5, area >= 6 px, periodic), mean body area per kind, the fraction of prey bodies touching predator
  material (c_b > 0.5 within 2 px) and of predators touching prey (c_a > 0.5 within 2 px), max c_b.
Extinction time of a kind = first frame after which its labkit count stays 0 to the end (predators: after t=3000).
"""
import sys, json
import numpy as np
from scipy import ndimage

DTF = 100.0          # time per recorded frame
WIN = 60             # 6000 t windows
K = 20


def periodic_label(mask):
    lab, n = ndimage.label(mask)
    if n == 0:
        return lab, 0
    # merge labels across the periodic edges
    parent = list(range(n + 1))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for a, b in list(zip(lab[0], lab[-1])) + list(zip(lab[:, 0], lab[:, -1])):
        if a and b:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)
    roots = np.array([find(i) for i in range(n + 1)])
    lab = roots[lab]
    u = np.unique(lab[lab > 0])
    remap = np.zeros(n + 1, int)
    remap[u] = np.arange(1, len(u) + 1)
    return remap[lab], len(u)


def bodies(c, thr=0.5, amin=6):
    lab, n = periodic_label(c > thr)
    if n == 0:
        return lab, []
    areas = np.bincount(lab.ravel(), minlength=n + 1)
    keep = [i for i in range(1, n + 1) if areas[i] >= amin]
    return lab, [(i, int(areas[i])) for i in keep]


def touching(lab, ids, other_mask, r=2):
    # periodic: dilate a wrap-padded copy
    H, W = other_mask.shape
    pad = np.pad(other_mask, r, mode="wrap")
    grown = ndimage.binary_dilation(pad, iterations=r)[r:r + H, r:r + W]
    hit = np.unique(lab[grown & (lab > 0)])
    return sum(1 for i, _ in ids if i in set(hit.tolist()))


def last_nonzero_end(n, start):
    """first frame f >= start such that n[f:] are all 0, or None"""
    n = np.asarray(n)
    nz = np.nonzero(n[start:])[0]
    if len(nz) == 0:
        return start
    last = start + nz[-1]
    return last + 1 if last + 1 < len(n) else None


def run(pack):
    m = json.load(open(f"{pack}/metrics.json"))
    sp = m["species"]
    T = len(sp["prey"]["n_comp"])
    out = {"pack": pack, "seed": m["seed"], "frames": T, "t_end": (T - 1) * DTF,
           "size": None, "status": m["status"], "wall_s": round(m["wall_seconds"], 1)}
    for kind in ("prey", "predator"):
        s = sp[kind]
        n = s["n_comp"]
        psf = np.array(s["persistent_split_frames"], int)
        nwin = int(np.ceil((T - 1) / WIN))
        wins = []
        for w in range(nwin):
            a, b = w * WIN, (w + 1) * WIN
            elig = max(0, min(b, T - 1 - K + 1) - a)          # frames in window where a persistent split is countable
            cnt = int(((psf >= a) & (psf < b)).sum())
            wins.append({"t0": a * DTF, "t1": b * DTF, "persistent_splits": cnt, "eligible_t": elig * DTF,
                         "rate_per_1000t": round(1000 * cnt / (elig * DTF), 3) if elig else None,
                         "mean_count": round(float(np.mean(n[a:min(b, T)])), 2)})
        ext = last_nonzero_end(n, 30 if kind == "predator" else 5)
        tt = np.arange(T) * DTF
        sel = tt >= 12000
        slope = np.polyfit(tt[sel] / 10000, np.asarray(n, float)[sel], 1)[0] if sel.sum() > 2 else None
        out[kind] = {"n": n, "final": n[-1], "persistent_splits_total": len(psf), "max_generation": s["max_generation"],
                     "merge_split_ratio": s["merge_split_ratio"], "windows": wins,
                     "extinct_at_t": None if ext is None else ext * DTF,
                     "count_slope_per_10000t_after_12000": None if slope is None else round(float(slope), 3),
                     "mean_count_12000_48000": round(float(np.mean(np.asarray(n)[sel])), 2) if sel.any() else None,
                     "mean_count_last_6000": round(float(np.mean(n[-60:])), 2),
                     "last_persistent_split_t": int(psf.max()) * DTF if len(psf) else None}
    # render cross-check
    z = np.load(f"{pack}/frames.npz")
    R, rf = z["render"].astype(np.float32), z["render_f"]
    out["size"] = list(R.shape[-2:])
    rows = []
    for k, f in enumerate(rf):
        ca, cb = R[k, 0], R[k, 1]
        la, ia = bodies(ca)
        lb, ib = bodies(cb)
        rows.append({"t": float(f * DTF), "prey": len(ia), "pred": len(ib),
                     "prey_area": round(float(np.mean([a for _, a in ia])), 1) if ia else 0.0,
                     "pred_area": round(float(np.mean([a for _, a in ib])), 1) if ib else 0.0,
                     "prey_cond_frac": round(float((ca > 0.5).mean()), 4),
                     "pred_cond_frac": round(float((cb > 0.5).mean()), 4),
                     "prey_with_pred": touching(la, ia, cb > 0.5) if ia else 0,
                     "pred_on_prey": touching(lb, ib, ca > 0.5) if ib else 0,
                     "max_cb": round(float(cb.max()), 3), "mean_cb": round(float(cb.mean()), 4),
                     "mean_ca": round(float(ca.mean()), 4)})
    out["render_series"] = rows
    json.dump(out, open(f"{pack}/long.json", "w"))
    p, q = out["prey"], out["predator"]
    print(f"{pack.split('/')[-1]}: size {out['size']} T={out['t_end']:.0f} prey final {p['final']} (ext {p['extinct_at_t']}) "
          f"pred final {q['final']} (ext {q['extinct_at_t']}); persistent splits prey/pred per window "
          f"{[w['persistent_splits'] for w in p['windows']]} / {[w['persistent_splits'] for w in q['windows']]}; "
          f"slope prey {p['count_slope_per_10000t_after_12000']} pred {q['count_slope_per_10000t_after_12000']}")
    return out


if __name__ == "__main__":
    for pk in sys.argv[1:]:
        run(pk.rstrip("/"))
