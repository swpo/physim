"""Per dividing track: net displacement in labkit body lengths (net/sqrt(mean area)) and in rod lengths by
several long-axis measures; trimmed net (excluding first/last k frames, i.e. birth recoil and pre-fission
elongation); largest step; area jumps (sub-threshold fragments shed or absorbed); centroid-fallback links.
usage: mlen.py frames.npz world.py [K=20]"""
import sys, importlib.util, json, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M
F = np.load(sys.argv[1]); mat = F["matter"].astype(np.float32)
spec = importlib.util.spec_from_file_location("w", sys.argv[2]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
K = int(sys.argv[3]) if len(sys.argv) > 3 else 20
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True); byid = {t["id"]: t for t in tracks}

def shape(t, k):
    f = t["start"] + k
    m = comps[f]["lab"] == t["comp"][k] + 1
    ys, xs = np.nonzero(m); cy, cx = t["cy"][k], t["cx"][k]
    dy = M._wrap(ys - cy, H); dx = M._wrap(xs - cx, Wd)
    C = np.cov(np.vstack([dy, dx])); lam, vec = np.linalg.eigh(C)
    v = vec[:, -1]; p = dy * v[0] + dx * v[1]; q = dy * vec[0, 0] + dx * vec[1, 0]
    feret = p.max() - p.min() + 1.0; width = q.max() - q.min() + 1.0
    return 4 * np.sqrt(max(lam[-1], 0)), feret, width, (v[0], v[1])

def disp(t, a, b):
    sy = M._wrap(np.diff(t["cy"][a:b + 1]), H); sx = M._wrap(np.diff(t["cx"][a:b + 1]), Wd)
    return float(np.hypot(sy.sum(), sx.sum()))

rows = []
for t in tracks:
    kids = [c for c in t["children"] if byid[c]["birth"] == "split" and byid[c]["end"] - byid[c]["start"] + 1 >= K]
    n = len(t["cy"])
    if len(kids) < 2 or n < 5: continue
    S = [shape(t, k) for k in range(n)]
    L4 = np.array([s[0] for s in S]); Fe = np.array([s[1] for s in S]); Wi = np.array([s[2] for s in S])
    sy = M._wrap(np.diff(t["cy"]), H); sx = M._wrap(np.diff(t["cx"]), Wd); st = np.hypot(sy, sx)
    net = float(np.hypot(sy.sum(), sx.sum())); size = float(np.sqrt(np.mean(t["area"])))
    ar = np.array(t["area"], float); jump = np.abs(np.diff(ar)) / ar[:-1]
    net_tr2 = disp(t, 2, n - 3) if n > 7 else float("nan")
    net_tr3 = disp(t, 3, n - 4) if n > 9 else float("nan")
    # heading: angle between displacement and long axis (mid-life)
    vy, vx = S[n // 2][3]; dyy, dxx = sy.sum(), sx.sum()
    cosang = abs(vy * dyy + vx * dxx) / max(np.hypot(dyy, dxx), 1e-9)
    rows.append(dict(id=t["id"], birth=t["birth"], life=n, net=round(net, 1),
                     bl_labkit=round(net / size, 2), L4mean=round(L4.mean(), 1), Fmed=round(float(np.median(Fe)), 1),
                     Fmin=round(Fe.min(), 1), Fmax=round(Fe.max(), 1), Wmed=round(float(np.median(Wi)), 1),
                     aspect=round(float(np.median(Fe / Wi)), 2),
                     bl_L4=round(net / L4.mean(), 2), bl_Fmed=round(net / np.median(Fe), 2), bl_Fmax=round(net / Fe.max(), 2),
                     bl_Fmed_tr2=round(net_tr2 / np.median(Fe), 2), bl_Fmed_tr3=round(net_tr3 / np.median(Fe), 2),
                     maxstep=round(float(st.max()), 2), medstep=round(float(np.median(st)), 2),
                     max_area_jump=round(float(jump.max()), 2), straight=round(net / max(st.sum(), 1e-9), 2),
                     cos_axis=round(float(cosang), 2), parents=len(t["parents"])))
rows.sort(key=lambda r: -r["bl_labkit"])
cnt = lambda key, thr=3: sum(1 for r in rows if r[key] == r[key] and r[key] >= thr)
summ = {k: cnt(k) for k in ["bl_labkit", "bl_L4", "bl_Fmed", "bl_Fmax", "bl_Fmed_tr2", "bl_Fmed_tr3"]}
print(sys.argv[1]); print(" dividing tracks:", len(rows), " >=3 by:", json.dumps(summ))
print(" >=2.5 by Fmed:", cnt("bl_Fmed", 2.5), " best bl_Fmed:", max((r["bl_Fmed"] for r in rows), default=0))
ratio = np.median([r["Fmed"] / r["L4mean"] for r in rows]); print(" median Fmed/L4mean:", round(float(ratio), 3), " median aspect:", np.median([r["aspect"] for r in rows]))
lab_over_F = np.median([r["bl_labkit"] / r["bl_Fmed"] for r in rows]); print(" median bl_labkit/bl_Fmed:", round(float(lab_over_F), 2))
hdr = ["id", "birth", "life", "net", "bl_labkit", "L4mean", "Fmed", "Fmin", "Fmax", "aspect", "bl_L4", "bl_Fmed", "bl_Fmax", "bl_Fmed_tr2", "bl_Fmed_tr3", "maxstep", "medstep", "max_area_jump", "straight", "cos_axis"]
print(" " + " ".join(hdr))
for r in rows[:14]: print(" " + " ".join(str(r[h]) for h in hdr))
