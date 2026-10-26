"""Independent M measurement on a labkit frames.npz (labkit's own segmentation and tracker).
For every dividing track (>= 2 split children living >= K frames; same selection as swimdivide.py):
net displacement in several body-length units, jump/swap diagnostics, and a growth-proof (end-to-end) displacement.
usage: mmeasure.py frames.npz world.py [K=20] [label]"""
import sys, json, importlib.util, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M
F = np.load(sys.argv[1]); mat = F["matter"].astype(np.float32)
spec = importlib.util.spec_from_file_location("w", sys.argv[2]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
K = int(sys.argv[3]) if len(sys.argv) > 3 else 20
label = sys.argv[4] if len(sys.argv) > 4 else sys.argv[1]
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True); byid = {t["id"]: t for t in tracks}

def pix(t, k):
    f = t["start"] + k; lab = comps[f]["lab"]; m = lab == t["comp"][k] + 1
    ys, xs = np.nonzero(m); cy, cx = t["cy"][k], t["cx"][k]
    return np.vstack([M._wrap(ys - cy, H), M._wrap(xs - cx, Wd)]).T, m

def feret(P):
    if len(P) > 400: P = P[np.random.default_rng(0).choice(len(P), 400, replace=False)]
    d = np.sqrt(((P[:, None, :] - P[None, :, :]) ** 2).sum(-1)); return float(d.max()) + 1.0

rows = []; allsteps = []
for t in tracks:
    kids = [c for c in t["children"] if byid[c]["birth"] == "split" and byid[c]["end"] - byid[c]["start"] + 1 >= K]
    L = len(t["cy"])
    if len(kids) < 2 or L < 5: continue
    sy = M._wrap(np.diff(t["cy"]), H); sx = M._wrap(np.diff(t["cx"]), Wd); st = np.hypot(sy, sx)
    net_vec = np.array([sy.sum(), sx.sum()]); net = float(np.hypot(*net_vec)); u = net_vec / max(net, 1e-9)
    area = np.array(t["area"], float); size = float(np.sqrt(area.mean()))
    lam4, lam12, fer, ext_u, ext12_u, aspect = [], [], [], [], [], []
    ovl = []
    prev_m = None
    for k in range(L):
        P, m = pix(t, k)
        C = np.cov(P.T); ev_ = np.linalg.eigvalsh(C)
        lam4.append(4 * np.sqrt(max(ev_[-1], 0))); lam12.append(np.sqrt(12 * max(ev_[-1], 0)))
        aspect.append(np.sqrt(max(ev_[-1], 0) / max(ev_[0], 1e-9)))
        fer.append(feret(P))
        pr = P @ u; ext_u.append(pr.max() - pr.min() + 1); ext12_u.append(np.sqrt(12 * pr.var()))
        if prev_m is not None:
            ovl.append((prev_m & m).sum() / max(min(prev_m.sum(), m.sum()), 1))
        prev_m = m
    lam4, lam12, fer, ext_u, ext12_u = map(np.array, (lam4, lam12, fer, ext_u, ext12_u)); ovl = np.array(ovl)
    # jump diagnostics: steps far above the track's median step, and whether area jumped there
    med = float(np.median(st)); dA = np.abs(np.diff(area)) / area[:-1]
    jumps = [(int(i), round(float(st[i]), 2), round(float(dA[i]), 2)) for i in range(len(st)) if st[i] > max(3 * med, 2.0)]
    # jump-corrected net: remove steps that coincide with a >= 15% area change and are > 2x the median step
    bad = (st > 2 * med) & (dA >= 0.15)
    net_corr = float(np.hypot(sy[~bad].sum(), sx[~bad].sum()))
    # growth-proof displacement: rear and front ends along u, start (first 2 frames) vs end (last 2 frames), in a common frame
    cyc = np.concatenate([[0], np.cumsum(sy)]); cxc = np.concatenate([[0], np.cumsum(sx)])
    def ends(k):
        P, _ = pix(t, k); pr = (P + np.array([cyc[k], cxc[k]])) @ u; return pr.min(), pr.max()
    r0, f0 = np.mean([ends(k)[0] for k in (0, 1)]), np.mean([ends(k)[1] for k in (0, 1)])
    r1, f1 = np.mean([ends(k)[0] for k in (L - 2, L - 1)]), np.mean([ends(k)[1] for k in (L - 2, L - 1)])
    rear, front = float(r1 - r0), float(f1 - f0)
    # early relaxation after a split birth: displacement in first 3 frames vs median per-frame step
    early = float(np.hypot(sy[:3].sum(), sx[:3].sum())) if t["birth"] == "split" else float("nan")
    rows.append(dict(id=t["id"], birth=t["birth"], start=t["start"], end=t["end"], life=L, net=round(net, 1),
        bl_lab=round(net / size, 2), bl_4lam=round(net / lam4.mean(), 2), bl_12lam=round(net / lam12.mean(), 2),
        bl_feret=round(net / fer.mean(), 2), bl_feret_max=round(net / fer.max(), 2), bl_ext_u=round(net / ext_u.mean(), 2), bl_r2=round(net / max(size, ext12_u.mean()), 2), ext12_u=round(float(ext12_u.mean()), 1), bl_2pilam=round(net / (0.8862 * lam4.mean()), 2),
        size=round(size, 2), feret_mean=round(float(fer.mean()), 1), feret_birth=round(float(fer[:2].mean()), 1), feret_div=round(float(fer[-2:].mean()), 1),
        lam4=round(float(lam4.mean()), 1), aspect=round(float(np.mean(aspect)), 2), ext_u=round(float(ext_u.mean()), 1),
        straight=round(net / max(st.sum(), 1e-9), 2), med_step=round(med, 2), max_step=round(float(st.max()), 2),
        jumps=jumps, net_corr=round(net_corr, 1), bl_lab_corr=round(net_corr / size, 2), bl_feret_corr=round(net_corr / fer.mean(), 2),
        rear=round(rear, 1), front=round(front, 1), bl_feret_rear=round(min(rear, front) / fer.mean(), 2),
        min_overlap=round(float(ovl.min()), 2) if len(ovl) else None, n_low_overlap=int((ovl < 0.1).sum()) if len(ovl) else 0,
        early3=round(early, 2)))
rows.sort(key=lambda r: -r["bl_lab"])
def cnt(key, thr=3.0): return sum(r[key] >= thr for r in rows)
print(f"== {label}: grid {H}x{Wd}, {len(comps)} frames, {len(tracks)} tracks, {len(rows)} dividing tracks (2 split children >= {K} frames)")
print("  passing >= 3:", {k: cnt(k) for k in ["bl_lab", "bl_lab_corr", "bl_4lam", "bl_12lam", "bl_2pilam", "bl_feret", "bl_feret_max", "bl_ext_u", "bl_r2", "bl_feret_corr", "bl_feret_rear"]})
print("  best:", {k: max((r[k] for r in rows), default=None) for k in ["bl_lab", "bl_4lam", "bl_12lam", "bl_2pilam", "bl_feret", "bl_ext_u", "bl_r2", "bl_feret_rear"]})
print("  median over dividing tracks: sqrt(area) %.2f, feret %.1f, 4sqrt(lam) %.1f, aspect %.2f, feret/sqrt(area) %.2f" % (
    np.median([r["size"] for r in rows]), np.median([r["feret_mean"] for r in rows]), np.median([r["lam4"] for r in rows]),
    np.median([r["aspect"] for r in rows]), np.median([r["feret_mean"] / r["size"] for r in rows])))
print("  tracks with any low-overlap link (centroid fallback, possible swap):", sum(r["n_low_overlap"] > 0 for r in rows))
print("  births of the >=3 labkit tracks:", [r["birth"] for r in rows if r["bl_lab"] >= 3])
for r in rows:
    if r["bl_lab"] >= 3: print("   id %d life %d net %.1f | lab %.2f 4lam %.2f 2pilam %.2f feret %.2f ext_u %.2f r2 %.2f rear %.2f | feret %.1f (birth %.1f div %.1f) ext12u %.1f size %.2f straight %.2f" % (r["id"], r["life"], r["net"], r["bl_lab"], r["bl_4lam"], r["bl_2pilam"], r["bl_feret"], r["bl_ext_u"], r["bl_r2"], r["bl_feret_rear"], r["feret_mean"], r["feret_birth"], r["feret_div"], r["ext12_u"], r["size"], r["straight"]))
json.dump(rows, open(sys.argv[1].replace("/", "_").strip("_")[-60:] + ".json" if False else "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/mpanel/rows_" + label + ".json", "w"))
