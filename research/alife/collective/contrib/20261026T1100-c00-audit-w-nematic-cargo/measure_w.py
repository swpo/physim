"""Auditor's own containment (W) measurement for the nematic-cargo world.

usage: measure_w.py frames.npz world.py [--ch 3] [--sch 2] [--json out.json] [--label NAME] [--dx 1]

Independent of the claim's sd_individuals.py / inherit.py: the signed distance is measured to the
SUB-PIXEL phi = 0 isocontour (skimage marching squares on the 3x3 periodic tiling, polyline densified to
0.1 px, nearest contour point by KD-tree), negative inside phi > 0. Every pixel is owned by the body whose
contour is nearest (so neighbours' pixels never count as one body's outside).

Bodies: phi > 0 connected components (periodic) with area >= 20 px, on every rendered frame >= 20.
  inside  = own pixels with sd <= -1.0   (also reported: sd <= -1.5)
  outside = own pixels with 2 <= sd <= 5 (also reported: 3 <= sd <= 6, i.e. beyond the ring)
  in/out  = mean cargo inside / mean cargo outside (a body-frame needs >= 2 inside px and >= 6 outside px)
Ring (B screen, channel sch): rim |sd| <= 0.75, core sd <= -1.5, out 2 <= sd <= 4.
Per track (labkit tracker on the matter stack, as the pack uses): share of its rendered frames >= 2x.
Daughters: labkit tracks born by a split; in/out at the rendered frame nearest start+5 (within +-1, alive).
"""
import sys, json, argparse, importlib.util
import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree
from skimage import measure

sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("frames"); ap.add_argument("world")
ap.add_argument("--ch", type=int, default=3); ap.add_argument("--sch", type=int, default=2)
ap.add_argument("--json"); ap.add_argument("--label", default="")
ap.add_argument("--fmin", type=int, default=20); ap.add_argument("--minarea", type=float, default=20)
ap.add_argument("--dx", type=float, default=1.0)
ap.add_argument("--olo", type=float, default=2.0); ap.add_argument("--ohi", type=float, default=5.0)  # primary outside band  # grid spacing: distances in world units, min area scaled by 1/dx^2
a = ap.parse_args()
a.minarea = a.minarea / a.dx ** 2

F = np.load(a.frames)
R = F["render"].astype(np.float64); rf = [int(x) for x in F["render_f"]]
mat = F["matter"].astype(np.float32)
spec = importlib.util.spec_from_file_location("w", a.world); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
T, C, H, Wd = R.shape


def sdist(phi):
    """signed distance to the phi=0 isocontour (periodic), and nearest-body label of every pixel."""
    t = np.tile(phi, (3, 3))
    ins = t > 0
    lab, n = ndimage.label(ins)
    cs = measure.find_contours(t, 0.0)
    pts, own = [], []
    for c in cs:
        if len(c) < 2:
            continue
        seg = np.diff(c, axis=0); L = np.hypot(seg[:, 0], seg[:, 1])
        k = np.maximum(1, np.ceil(L / 0.1).astype(int))
        dense = np.concatenate([c[i] + np.outer(np.arange(k[i]) / k[i], seg[i]) for i in range(len(seg))] + [c[-1:]])
        # keep only contour points within (or 8 px around) the central tile
        m = (dense[:, 0] > H - 8) & (dense[:, 0] < 2 * H + 8) & (dense[:, 1] > Wd - 8) & (dense[:, 1] < 2 * Wd + 8)
        if not m.any():
            continue
        dense = dense[m]
        # owner: label of the nearest inside pixel
        iy = np.clip(np.round(dense[:, 0]).astype(int), 0, 3 * H - 1); ix = np.clip(np.round(dense[:, 1]).astype(int), 0, 3 * Wd - 1)
        lb = lab[iy, ix]
        if (lb == 0).any():
            fy = np.clip(np.floor(dense[:, 0]).astype(int), 0, 3 * H - 2); fx = np.clip(np.floor(dense[:, 1]).astype(int), 0, 3 * Wd - 2)
            cand = np.stack([lab[fy, fx], lab[fy + 1, fx], lab[fy, fx + 1], lab[fy + 1, fx + 1]], 1)
            lb = np.where(lb == 0, cand.max(1), lb)
        pts.append(dense); own.append(lb)
    yy, xx = np.mgrid[H:2 * H, Wd:2 * Wd]
    q = np.stack([yy.ravel(), xx.ravel()], 1).astype(float)
    if not pts:
        return None, None, None
    P = np.concatenate(pts); O = np.concatenate(own)
    d, i = cKDTree(P).query(q)
    d = d.reshape(H, Wd); o = O[i].reshape(H, Wd)
    sd = a.dx * np.where(phi > 0, -d, d)
    labc = lab[H:2 * H, Wd:2 * Wd]
    return sd, o, labc


def ratio(x, m_in, m_out):
    if m_in.sum() < 2 or m_out.sum() < 6:
        return np.nan
    return x[m_in].mean() / max(x[m_out].mean(), 1e-12)


# labkit tracks on the matter stack (same tracker as the pack and the claim's scripts)
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold"))
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True)
ridx = {f: k for k, f in enumerate(rf)}

per_frame = {}   # k -> list of dict(label, ratios...)
cache = {}
bf = []          # body-frame records
for k, f in enumerate(rf):
    if f < a.fmin:
        continue
    phi = R[k, 0]
    sd, own, labc = sdist(phi)
    if sd is None:
        continue
    cache[k] = (sd, own, labc)
    x = R[k, a.ch]; s = R[k, a.sch]
    for j in np.unique(labc[labc > 0]):
        body = labc == j
        if body.sum() < a.minarea:
            continue
        o = own == j
        r1 = ratio(x, o & (sd <= -1.0), o & (sd >= a.olo) & (sd <= a.ohi))
        r2 = ratio(x, o & (sd <= -1.5), o & (sd >= a.olo) & (sd <= a.ohi))
        r3 = ratio(x, o & (sd <= -1.0), o & (sd >= 3) & (sd <= 6))
        rim, core, out = o & (np.abs(sd) <= 0.75), o & (sd <= -1.5), o & (sd >= 2) & (sd <= 4)
        rc = s[rim].mean() / max(s[core].mean(), 1e-12) if core.sum() >= 2 and rim.sum() >= 4 else np.nan
        ro = s[rim].mean() / max(s[out].mean(), 1e-12) if out.sum() >= 4 and rim.sum() >= 4 else np.nan
        bf.append(dict(k=k, f=f, j=int(j), area=int(body.sum()), r=r1, r_core15=r2, r_out36=r3, ring_rc=rc, ring_ro=ro))


def body_ratio_at(t, f):
    """in/out of track t at matter frame f, if rendered: the phi>0 component overlapping its labkit mask."""
    k = ridx.get(f)
    if k is None or k not in cache or f < t["start"] or f > t["end"]:
        return np.nan
    sd, own, labc = cache[k]
    ci = t["comp"][f - t["start"]]
    m = comps[f]["lab"] == ci + 1
    ls = labc[m & (labc > 0)]
    if ls.size == 0:
        return np.nan
    j = np.bincount(ls).argmax()
    if (labc == j).sum() < a.minarea:
        return np.nan
    o = own == j
    return ratio(R[k, a.ch], o & (sd <= -1.0), o & (sd >= a.olo) & (sd <= a.ohi))


# per-track share of life >= 2x (tracks with >= 10 measured rendered frames)
trk = []
for t in tracks:
    v = np.array([body_ratio_at(t, f) for f in range(max(t["start"], a.fmin), t["end"] + 1) if f in ridx])
    v = v[np.isfinite(v)]
    if len(v) >= 10:
        trk.append(((v >= 2).mean(), float(np.median(v)), t["id"]))

# daughters 5 frames after birth
dau = []
for t in tracks:
    if t["birth"] != "split":
        continue
    best = np.nan
    for f in (t["start"] + 5, t["start"] + 4, t["start"] + 6):
        if f <= t["end"] and f in ridx:
            best = body_ratio_at(t, f)
            if np.isfinite(best):
                break
    if np.isfinite(best):
        dau.append((t["id"], t["start"], len(t["cy"]), best))

r = np.array([b["r"] for b in bf]); r = r[np.isfinite(r)]
r2 = np.array([b["r_core15"] for b in bf]); r2 = r2[np.isfinite(r2)]
r3 = np.array([b["r_out36"] for b in bf]); r3 = r3[np.isfinite(r3)]
rc = np.array([b["ring_rc"] for b in bf]); ro = np.array([b["ring_ro"] for b in bf]); okr = np.isfinite(rc) & np.isfinite(ro)
dv = np.array([d[3] for d in dau]); dv12 = np.array([d[3] for d in dau if d[2] >= 12])
ts = np.array([x[0] for x in trk])
# share of all cargo on phi>0 pixels, second half
half = [k for k, f in enumerate(rf) if f >= rf[-1] // 2]
onbody = float(np.mean([R[k, a.ch][R[k, 0] > 0].sum() / max(R[k, a.ch].sum(), 1e-12) for k in half]))
occ = float(np.mean([(R[k, 0] > 0).mean() for k in half]))

out = dict(label=a.label, frames=a.frames, n_bodyframes=int(len(r)), median_in_out=float(np.median(r)) if len(r) else None,
           share_ge2=float((r >= 2).mean()) if len(r) else None,
           q25_q75=[float(np.percentile(r, 25)), float(np.percentile(r, 75))] if len(r) else None,
           median_in_out_core15=float(np.median(r2)) if len(r2) else None, share_ge2_core15=float((r2 >= 2).mean()) if len(r2) else None,
           median_in_out_out36=float(np.median(r3)) if len(r3) else None, share_ge2_out36=float((r3 >= 2).mean()) if len(r3) else None,
           share_lt1=float((r < 1).mean()) if len(r) else None,
           ring_bodyframes=int(okr.sum()), ring_both_ge15=float(((rc[okr] >= 1.5) & (ro[okr] >= 1.5)).mean()) if okr.any() else None,
           ring_median_rc=float(np.median(rc[okr])) if okr.any() else None, ring_median_ro=float(np.median(ro[okr])) if okr.any() else None,
           n_tracks_ge10=len(trk), tracks_majority_ge2=float((ts > 0.5).mean()) if len(ts) else None,
           tracks_median_share_ge2=float(np.median(ts)) if len(ts) else None,
           n_daughters=int(len(dv)), daughters_median=float(np.median(dv)) if len(dv) else None,
           daughters_share_ge2=float((dv >= 2).mean()) if len(dv) else None,
           n_daughters_ge12=int(len(dv12)), daughters_ge12_share_ge2=float((dv12 >= 2).mean()) if len(dv12) else None,
           cargo_on_body_frac_2nd_half=onbody, occupancy_2nd_half=occ,
           n_tracks=len(tracks), n_split_events=sum(1 for e in ev if e["type"] == "split"))
for kk, vv in out.items():
    print(f"{kk}: {vv}")
if a.json:
    json.dump(out, open(a.json, "w"), indent=1)
