"""Per-rod, per-frame kinematics for a wrapped Marangoni run (labkit frames.npz + the wrapper's flow.npz).
Segmentation and tracking are labkit's (as c00's extract.py). For every track and frame: centroid (unwrapped along the
track), area, own length L4 = 4 sqrt(lambda_max), long-axis unit vector, body-mean flow velocity, surfactant-ring dipole
(s-weighted offset of a band 2 px outside to 1 px inside the body, from the body centroid), mar(t).
usage: trackrods.py RUNDIR [K=40]  ->  RUNDIR/rods.json"""
import sys, json, importlib.util
from pathlib import Path
import numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
sys.dont_write_bytecode = True
from labkit import run as LR, metrics as M
from scipy import ndimage as ndi

run = Path(sys.argv[1]); K = int(sys.argv[2]) if len(sys.argv) > 2 else 40
BASE = "/home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py"
spec = importlib.util.spec_from_file_location("w", BASE); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
F = np.load(run / "frames.npz"); mat = F["matter"].astype(np.float32)
fl = np.load(run / "flow.npz")
T = len(mat); assert len(fl["n"]) == T, (len(fl["n"]), T)
spf = int(fl["n"][1] - fl["n"][0]); FT = spf * float(fl["dt"])
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True)
byid = {t["id"]: t for t in tracks}

# per-frame per-component measurements
yy, xx = np.mgrid[0:H, 0:Wd]
per = []
for f in range(T):
    lab = comps[f]["lab"]; nC = len(comps[f]["area"])
    vx = fl["vx"][f].astype(np.float64); vy = fl["vy"][f].astype(np.float64); s = fl["s"][f].astype(np.float64)
    allbody = lab > 0
    rows = []
    for i in range(nC):
        m = lab == i + 1
        ys, xs = np.nonzero(m); cy, cx = comps[f]["cy"][i], comps[f]["cx"][i]
        dy = M._wrap(ys - cy, H); dxx = M._wrap(xs - cx, Wd)
        if len(ys) >= 3:
            lam, vec = np.linalg.eigh(np.cov(np.vstack([dy, dxx])))
            L4 = 4 * np.sqrt(max(lam[-1], 0)); ax = vec[:, -1]; ecc = float(lam[-1] / max(lam[0], 1e-9))
        else:
            L4, ax, ecc = 1.0, np.array([1.0, 0.0]), 1.0
        U = (float(vy[m].mean()), float(vx[m].mean()))
        mw = np.pad(m, 3, mode="wrap")
        outer = ndi.binary_dilation(mw, iterations=2)[3:-3, 3:-3]; inner = ndi.binary_erosion(mw, iterations=1)[3:-3, 3:-3]
        band = outer & ~inner & ~(allbody & ~m)
        by, bx = np.nonzero(band); sb = s[band]
        if sb.sum() > 0:
            ddy = M._wrap(by - cy, H); ddx = M._wrap(bx - cx, Wd); w = sb / sb.sum()
            dip = (float((w * ddy).sum()), float((w * ddx).sum())); smean = float(sb.mean())
        else:
            dip, smean = (0.0, 0.0), 0.0
        rows.append(dict(L4=float(L4), ax=(float(ax[0]), float(ax[1])), ecc=ecc, U=U, dip=dip, sring=smean))
    per.append(rows)

out = []
for t in tracks:
    n = len(t["cy"])
    cy = np.array(t["cy"], float); cx = np.array(t["cx"], float)
    uy = np.concatenate([[cy[0]], cy[0] + np.cumsum(M._wrap(np.diff(cy), H))])
    ux = np.concatenate([[cx[0]], cx[0] + np.cumsum(M._wrap(np.diff(cx), Wd))])
    R = [per[t["start"] + k][t["comp"][k]] for k in range(n)]
    kids = t["children"]
    lasting = [c for c in kids if byid[c]["birth"] == "split" and byid[c]["end"] - byid[c]["start"] + 1 >= K]
    if t["end"] == T - 1: fate = "run-end"
    elif len(lasting) >= 2: fate = "divides"
    elif kids and byid[kids[0]]["birth"] == "merge": fate = "merges"
    elif kids: fate = "split-other"
    else: fate = "vanishes"
    out.append(dict(id=t["id"], start=t["start"], end=t["end"], n=n, birth=t["birth"], parents=t["parents"], children=kids,
                    lasting=lasting, fate=fate, dividing=bool(t["birth"] == "split" and len(lasting) >= 2 and n >= 5),
                    y=uy.round(3).tolist(), x=ux.round(3).tolist(), area=[float(a) for a in t["area"]],
                    L4=[round(r["L4"], 3) for r in R], ax=[[round(a, 4) for a in r["ax"]] for r in R],
                    ecc=[round(r["ecc"], 3) for r in R], U=[[round(a, 5) for a in r["U"]] for r in R],
                    dip=[[round(a, 4) for a in r["dip"]] for r in R], sring=[round(r["sring"], 5) for r in R]))
ncomp = [len(c["area"]) for c in comps]
json.dump(dict(run=str(run), T=T, H=H, W=Wd, FT=FT, K=K, mar=fl["mar"].tolist(), ncomp=ncomp,
               s_total=fl["s_total"].tolist(), clip_frac=float(fl["clip_frac"]) if "clip_frac" in fl else None,
               cfg=str(fl["cfg"]), tracks=out), open(run / "rods.json", "w"))
print(f"{run}: {T} frames, FT {FT}, {len(tracks)} tracks, {sum(o['dividing'] for o in out)} dividing, comps final {ncomp[-1]}")
