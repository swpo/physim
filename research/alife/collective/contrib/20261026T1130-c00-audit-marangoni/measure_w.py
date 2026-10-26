"""Auditor's cargo containment measure (W) on a labkit frames.npz, by signed distance to the body contour.

Bodies: periodic connected components of phi > 0 (render channel 0), >= 20 px (scaled by 1/dx^2).
Signed distance d (px, times dx): inside d = -(edt_in - 0.5), outside d = edt_out - 0.5, periodic (3x3 tiling).
Every pixel belongs to its nearest body ("own" pixels). Per body and per rendered frame (f >= FMIN):
    inside  = own & d <= -IN      (interior beyond the first 1-2 px from the contour)
    outside = own & OUT0 <= d <= OUT1  (a band a few px outside the ring)
    ratio   = mean(c inside) / mean(c outside)
Daughters: labkit tracker (labkit.run._normalize_matter/_segment_frames, labkit.metrics.track; the same calls labkit
uses), tracks born by "split"; the ratio of the phi>0 body that overlaps the track's labkit component most, at the
first rendered frame in [start+5, start+6]. Per-track life share: for tracks with >= 5 measured frames, the share of
their measured frames >= 2.
Also prints the mean ring (s) and cargo profile versus d, to show where the ring sits relative to the bands.
usage: measure_w.py frames.npz world.py [cargo_ch=3] [ring_ch=2] [dx=1] [--bands IN,OUT0,OUT1] [--fmin 10] [--label X]
"""
import sys, json, argparse, importlib.util, numpy as np
from scipy import ndimage
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M

ap = argparse.ArgumentParser()
ap.add_argument("frames"); ap.add_argument("world")
ap.add_argument("cargo_ch", nargs="?", type=int, default=3); ap.add_argument("ring_ch", nargs="?", type=int, default=2)
ap.add_argument("dx", nargs="?", type=float, default=1.0)
ap.add_argument("--bands", default="1.5,3,6"); ap.add_argument("--fmin", type=int, default=10)
ap.add_argument("--label", default=""); ap.add_argument("--json", default="")
a = ap.parse_args()
IN, OUT0, OUT1 = (float(x) for x in a.bands.split(","))
F = np.load(a.frames); R = F["render"].astype(np.float32); rf = [int(x) for x in F["render_f"]]
mat = F["matter"].astype(np.float32)
H, W = R.shape[2:]; sl = (slice(H, 2 * H), slice(W, 2 * W))
dx = a.dx; amin = 20 / dx ** 2


def bodies(k):
    phi = R[k, 0]; ins = phi > 0
    lab, n = M.periodic_label(ins, True)
    t = np.tile(ins, (3, 3))
    d = dx * np.where(t, -(ndimage.distance_transform_edt(t) - 0.5), ndimage.distance_transform_edt(~t) - 0.5)[sl]
    lt = np.tile(lab, (3, 3))
    _, (iy, ix) = ndimage.distance_transform_edt(lt == 0, return_indices=True)
    near = lt[iy, ix][sl]
    return lab, n, d, near


def ratio_of(k, lab, d, near, j):
    if (lab == j).sum() < amin: return np.nan
    own = near == j
    i_, o_ = own & (d <= -IN), own & (d >= OUT0) & (d <= OUT1)
    if i_.sum() < 3 or o_.sum() < 4: return np.nan
    c = R[k, a.cargo_ch]
    return float(c[i_].mean() / max(c[o_].mean(), 1e-9))


# labkit tracks (on every frame), used for daughters and per-track life shares
spec = importlib.util.spec_from_file_location("w", a.world); Wm = importlib.util.module_from_spec(spec); spec.loader.exec_module(Wm)
mn, thr, lo, hi = LR._normalize_matter(mat, Wm.META, True, Wm.META.get("threshold"))
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(*mn.shape[1:]), True)
tracks, ev = M.track(comps, links, mn.shape[1:], True)

bf = []                 # (frame, body label, ratio)
prof_bins = np.arange(-6, 10.5, 1.0)
prof_s = np.zeros(len(prof_bins) - 1); prof_c = np.zeros_like(prof_s); prof_n = np.zeros_like(prof_s)
cache = {}
for k, f in enumerate(rf):
    if f < a.fmin: continue
    lab, n, d, near = bodies(k); cache[k] = (lab, d, near)
    for j in range(1, n + 1):
        r = ratio_of(k, lab, d, near, j)
        if np.isfinite(r): bf.append((f, j, r))
    sel = near > 0
    idx = np.digitize(d[sel], prof_bins) - 1; ok = (idx >= 0) & (idx < len(prof_s))
    prof_s += np.bincount(idx[ok], weights=R[k, a.ring_ch][sel][ok], minlength=len(prof_s))
    prof_c += np.bincount(idx[ok], weights=R[k, a.cargo_ch][sel][ok], minlength=len(prof_s))
    prof_n += np.bincount(idx[ok], minlength=len(prof_s))
ridx = {f: k for k, f in enumerate(rf)}
rmap = {(f, j): r for f, j, r in bf}


def track_ratio(t, f):
    k = ridx.get(f)
    if k is None or f < t["start"] or f > t["end"]: return np.nan
    if k not in cache: cache[k] = (lambda b: (b[0], b[2], b[3]))(bodies(k))
    lab, d, near = cache[k]
    m = comps[f]["lab"] == (t["comp"][f - t["start"]] + 1)
    js, cnt = np.unique(lab[m & (lab > 0)], return_counts=True)
    if len(js) == 0: return np.nan
    j = int(js[cnt.argmax()])
    return rmap.get((f, j), ratio_of(k, lab, d, near, j))


dau, dau_all = [], []
for t in tracks:
    if t["birth"] != "split": continue
    r = np.nan
    for f in (t["start"] + 5, t["start"] + 6):
        r = track_ratio(t, f)
        if np.isfinite(r): break
    dau_all.append(r)
    if t["end"] - t["start"] + 1 >= 12: dau.append(r)
life = []
for t in tracks:
    v = np.array([track_ratio(t, f) for f in range(max(t["start"], a.fmin), t["end"] + 1) if f in ridx])
    v = v[np.isfinite(v)]
    if len(v) >= 5: life.append((v >= 2).mean())
w = np.array([r for _, _, r in bf]); dau = np.array(dau); dau = dau[np.isfinite(dau)]
dau_all = np.array(dau_all); dau_all = dau_all[np.isfinite(dau_all)]; life = np.array(life)
res = dict(label=a.label, frames=a.frames, bands=dict(inside_d_le=-IN, outside=[OUT0, OUT1]), body_frames=int(len(w)),
           median_in_out=round(float(np.median(w)), 3) if len(w) else None,
           share_ge2=round(float((w >= 2).mean()), 3) if len(w) else None,
           q10_q90=[round(float(np.percentile(w, 10)), 3), round(float(np.percentile(w, 90)), 3)] if len(w) else None,
           daughters_ge12=dict(n=int(len(dau)), ge2=int((dau >= 2).sum()), share=round(float((dau >= 2).mean()), 3) if len(dau) else None,
                               median=round(float(np.median(dau)), 3) if len(dau) else None),
           daughters_all=dict(n=int(len(dau_all)), ge2=int((dau_all >= 2).sum()), share=round(float((dau_all >= 2).mean()), 3) if len(dau_all) else None),
           tracks_life=dict(n=int(len(life)), share_tracks_majority_ge2=round(float((life > 0.5).mean()), 3) if len(life) else None),
           profile_d=[round(float(0.5 * (prof_bins[i] + prof_bins[i + 1])), 1) for i in range(len(prof_s))],
           profile_ring=[round(float(x), 4) for x in prof_s / np.maximum(prof_n, 1)],
           profile_cargo=[round(float(x), 4) for x in prof_c / np.maximum(prof_n, 1)])
print(f"{a.label} {a.frames}: bands inside d<=-{IN}, outside {OUT0}<=d<={OUT1}; body-frames {res['body_frames']}, "
      f"median in/out {res['median_in_out']}, share >= 2 {res['share_ge2']}, q10-q90 {res['q10_q90']}; "
      f"daughters(>=12 fr) 5 fr after birth {res['daughters_ge12']}; all split-born {res['daughters_all']}; tracks majority>=2 {res['tracks_life']}")
print("  d:     ", " ".join(f"{x:6.1f}" for x in res["profile_d"]))
print("  ring:  ", " ".join(f"{x:6.3f}" for x in res["profile_ring"]))
print("  cargo: ", " ".join(f"{x:6.3f}" for x in res["profile_cargo"]))
if a.json:
    with open(a.json, "a") as fh: fh.write(json.dumps(res) + "\n")
