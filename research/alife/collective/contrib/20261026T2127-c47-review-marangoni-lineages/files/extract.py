"""Per-track table for a labkit frames.npz of the Marangoni rods (labkit segmentation and tracker, as mlen.py).
For every track: genealogy, fate, rod length (median of 4 sqrt(lambda_max) over all frames), net displacement,
path, cycle, birth size, early speed, ring strength / polarity from the rendered s channel, crowding.
usage: extract.py frames.npz world.py label dx out.json [K=20]"""
import sys, json, importlib.util, numpy as np
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4]))
sys.dont_write_bytecode = True
from labkit import run as LR, metrics as M
from scipy import ndimage as ndi

fn, wpath, label, dx, out = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5]
K = int(sys.argv[6]) if len(sys.argv) > 6 else 20
F = np.load(fn); mat = F["matter"].astype(np.float32)
render = F["render"]; rf = list(F["render_f"]); rindex = {int(f): i for i, f in enumerate(rf)}
spec = importlib.util.spec_from_file_location("w", wpath); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True); byid = {t["id"]: t for t in tracks}
T = len(comps)
FT = 100 * 0.05  # time per frame (steps_per_frame x dt), same for all runs used here
RCROWD = 26.0  # crowding radius in physical units (about 2 population rod lengths on the 128 grid)


def shape(t, k):
    f = t["start"] + k
    m = comps[f]["lab"] == t["comp"][k] + 1
    ys, xs = np.nonzero(m); cy, cx = t["cy"][k], t["cx"][k]
    dy = M._wrap(ys - cy, H); dxx = M._wrap(xs - cx, Wd)
    lam, vec = np.linalg.eigh(np.cov(np.vstack([dy, dxx])))
    v = vec[:, -1]; p = dy * v[0] + dxx * v[1]
    return 4 * np.sqrt(max(lam[-1], 0)), p.max() - p.min() + 1.0, (v[0], v[1]), m


def ring(f, m, cy, cx, u):
    """s on the ring band (2 px outside the body to 1 px inside) at a rendered frame: mean band s, band/bath contrast,
    polarity = offset of the s-weighted band centroid from the body centroid, projected on the unit travel direction u
    (px; positive = s piled at the front)."""
    i = rindex.get(f)
    if i is None: return None
    s = render[i, 2].astype(np.float64)
    mw = np.pad(m, 3, mode="wrap")
    outer = ndi.binary_dilation(mw, iterations=2)[3:-3, 3:-3]; inner = ndi.binary_erosion(mw, iterations=1)[3:-3, 3:-3]
    band = outer & ~inner
    if band.sum() < 5: return None
    allbody = comps[f]["lab"] > 0
    bath = ~ndi.binary_dilation(np.pad(allbody, 6, mode="wrap"), iterations=6)[6:-6, 6:-6]
    sb = s[band]; ys, xs = np.nonzero(band)
    dy = M._wrap(ys - cy, H); dxx = M._wrap(xs - cx, Wd)
    w = sb / max(sb.sum(), 1e-12)
    py, px = (w * dy).sum(), (w * dxx).sum()
    pol = py * u[0] + px * u[1] if u is not None else np.nan
    return float(sb.mean()), float(sb.mean() / max(s[bath].mean(), 1e-9)), float(pol), float(sb.max())


# per-frame centroid lists for crowding
cents = [np.stack([c["cy"], c["cx"]], 1) if len(c["area"]) else np.zeros((0, 2)) for c in comps]
rows = []
for t in tracks:
    n = len(t["cy"])
    kids = t["children"]
    lasting = [c for c in kids if byid[c]["birth"] == "split" and byid[c]["end"] - byid[c]["start"] + 1 >= K]
    if t["end"] == T - 1: fate = "run-end"
    elif len(lasting) >= 2: fate = "divides"
    elif kids and byid[kids[0]]["birth"] == "merge": fate = "merges"
    elif kids: fate = "split-other"
    else: fate = "vanishes"
    r = dict(run=label, id=t["id"], start=t["start"], end=t["end"], n=n, birth=t["birth"], parents=t["parents"],
             children=kids, lasting=lasting, fate=fate, dx=dx,
             dividing=bool(t["birth"] == "split" and len(lasting) >= 2 and n >= 5))
    sy = M._wrap(np.diff(t["cy"]), H); sx = M._wrap(np.diff(t["cx"]), Wd); st = np.hypot(sy, sx)
    S = [shape(t, k) for k in range(n)]
    L4 = np.array([s[0] for s in S]); Fe = np.array([s[1] for s in S])
    ar = np.array(t["area"], float)
    net = float(np.hypot(sy.sum(), sx.sum())) if n > 1 else 0.0
    path = float(st.sum())
    r.update(L4med=float(np.median(L4)) * dx, L4mean=float(L4.mean()) * dx, Fmed=float(np.median(Fe)) * dx,
             L_birth=float(np.median(L4[:3])) * dx, L_end=float(np.median(L4[-3:])) * dx,
             A_birth=float(ar[:2].mean()) * dx * dx, A_end=float(ar[-2:].mean()) * dx * dx, A_mean=float(ar.mean()) * dx * dx,
             net=net * dx, path=path * dx, straight=net / max(path, 1e-9),
             disp_rl=net / float(np.median(L4)) if n > 1 else 0.0,  # primary trait: net / median 4 sqrt(lambda_max)
             disp_rl_L4mean=net / float(L4.mean()) if n > 1 else 0.0, disp_rl_F=net / float(np.median(Fe)) if n > 1 else 0.0,
             vnet=net * dx / max(n - 1, 1) / FT, vpath=path * dx / max(n - 1, 1) / FT,
             vnet_rl=(net / float(np.median(L4))) / max(n - 1, 1),  # rod lengths per frame
             cycle=n * FT, maxstep=float(st.max()) * dx if n > 1 else 0.0,
             cy=float(np.mean(t["cy"])) * dx, cx=float(np.mean(t["cx"])) * dx,
             dir=[float(sy.sum()), float(sx.sum())], y0=float(t["cy"][0]) * dx, x0=float(t["cx"][0]) * dx,
             y1=float(t["cy"][-1]) * dx, x1=float(t["cx"][-1]) * dx, Lbox=H * dx)
    # early speed: first min(15, n-1) frames, rod lengths per frame (Lmed of those frames) and physical
    ke = min(15, n - 1)
    if ke >= 3:
        ne = float(np.hypot(sy[:ke].sum(), sx[:ke].sum()))
        r.update(v_early_rl=ne / float(np.median(L4[:ke + 1])) / ke, v_early=ne * dx / ke / FT, ke=ke,
                 vpath_early=float(st[:ke].sum()) * dx / ke / FT)
        r["A_k"] = float(ar[ke - 1:ke + 2].mean()) * dx * dx  # area at the end of the early window (3-frame mean)
        r["A_0"] = float(ar[:3].mean()) * dx * dx
        nl = float(np.hypot(sy[-ke:].sum(), sx[-ke:].sum()))
        r.update(v_late=nl * dx / ke / FT, vpath_late=float(st[-ke:].sum()) * dx / ke / FT)
    # orientation of travel vs long axis (mid-life)
    if net > 0:
        u = np.array([sy.sum(), sx.sum()]) / net
        vy, vx = S[n // 2][2]; r["cos_axis"] = float(abs(vy * u[0] + vx * u[1]))
    # ring strength and polarity over rendered frames (instantaneous travel direction from +-2 frames)
    rs = []
    for k in range(n):
        f = t["start"] + k
        if f not in rindex: continue
        a, b = max(0, k - 2), min(n - 1, k + 2)
        if b - a >= 2:
            dv = np.array([sy[a:b].sum(), sx[a:b].sum()]); nv = np.hypot(*dv)
            uu = dv / nv if nv > 0.5 else None
        else: uu = None
        q = ring(f, S[k][3], t["cy"][k], t["cx"][k], uu)
        if q: rs.append(q + ((nv / max(b - a, 1)) if uu is not None else np.nan,))
    if rs:
        R = np.array(rs, float)
        r.update(ring_s=float(np.nanmean(R[:, 0])), ring_contrast=float(np.nanmean(R[:, 1])),
                 ring_pol=float(np.nanmean(R[:, 2])) * dx, ring_pol_rl=float(np.nanmean(R[:, 2]) / np.median(L4)),
                 ring_smax=float(np.nanmean(R[:, 3])), nring=len(rs))
        ok = np.isfinite(R[:, 2]) & np.isfinite(R[:, 4])
        if ok.sum() >= 5 and np.std(R[ok, 2]) > 0 and np.std(R[ok, 4]) > 0:
            r["ring_pol_speed_corr"] = float(np.corrcoef(R[ok, 2], R[ok, 4])[0, 1])
    # crowding: neighbours within RCROWD (physical), nearest-neighbour distance, components in frame
    nb, nnd, ncomp = [], [], []
    for k in range(n):
        f = t["start"] + k; C = cents[f]
        d = np.hypot(M._wrap(C[:, 0] - t["cy"][k], H), M._wrap(C[:, 1] - t["cx"][k], Wd)) * dx
        d = np.delete(d, t["comp"][k])
        nb.append((d < RCROWD).sum()); nnd.append(d.min() if len(d) else np.nan); ncomp.append(len(C))
    r.update(crowd=float(np.mean(nb)), nnd=float(np.nanmean(nnd)), ncomp_birth=int(ncomp[0]), ncomp_mean=float(np.mean(ncomp)),
             crowd_birth=float(np.mean(nb[:3])))
    rows.append(r)

# parent-relative quantities: heading persistence, front/back daughter
rb = {r["id"]: r for r in rows}
for r in rows:
    if r["birth"] == "split" and len(r["parents"]) == 1:
        p = rb[r["parents"][0]]; t = byid[r["id"]]; pt = byid[p["id"]]
        pu = np.array(p["dir"]); pn = np.hypot(*pu)
        cu = np.array(r["dir"]); cn = np.hypot(*cu)
        if pn > 0 and cn > 0: r["cos_parent"] = float(pu @ cu / pn / cn)
        if pn > 0:
            off = np.array([M._wrap(t["cy"][0] - pt["cy"][-1], H), M._wrap(t["cx"][0] - pt["cx"][-1], Wd)])
            r["front"] = float(off @ pu / pn) * dx  # >0: daughter born on the parent's leading side
json.dump(dict(label=label, file=fn, T=T, H=H, W=Wd, dx=dx, K=K, rows=rows), open(out, "w"))
nd = sum(r["dividing"] for r in rows)
print(f"{label}: {T} frames, {len(tracks)} tracks, {nd} dividing (split-born, >=2 children living >={K} frames); "
      f">=3 rod lengths: {sum(r['dividing'] and r['disp_rl'] >= 3 for r in rows)}; best {max([r['disp_rl'] for r in rows if r['dividing']] or [0]):.2f}")
