"""(c27) Branched cut-vs-twin repair test for c28's ringswim-dl2 cells (deterministic dynamics: the twin is exact).
Run a seed to T0; pick up to NPICK mature, compact, moving cells (same cell for the last 400 steps by overlap,
moved >= 0.5 R_eq, aspect <= 1.5, area within 0.6-1.6x the median); for each, branch an undamaged twin and a
damaged arm and follow both by maximum overlap every 20 steps for T1 steps.
Damage modes: front = the 40% of the cell's pixels furthest along its direction of motion (phi, K, L erased and
S reset to bath by world.damage, i.e. matter deleted); ring = links L set to 0 in the whole cell and its wall
(chemical damage to the ring only, shape and catalyst kept).
Records per sample: area of the followed piece, number of pieces >= 20 px overlapping the lineage, link-ring
score (c28's contour-distance score), centroid. usage: twinrepair.py seed T0 T1 out"""
import sys, os, json, copy, importlib.util
import numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py"))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, T0, T1, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
NPICK = int(os.environ.get("NPICK", "2")); FRONT = float(os.environ.get("FRONT", "0.4"))
os.makedirs(out, exist_ok=True)
H, W = w.META["size"]

def plabel(m):
    lab, n = ndimage.label(m)
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):
        for u, v in set(zip(a.tolist(), b.tolist())):
            if u and v and u != v: lab[lab == v] = u
    return lab

def cen(mask):
    ys, xs = np.nonzero(mask)
    return np.array([np.angle(np.exp(2j*np.pi*ys/H).mean())*H/(2*np.pi) % H, np.angle(np.exp(2j*np.pi*xs/W).mean())*W/(2*np.pi) % W])

def ring_score(mask, L):
    c = cen(mask); sy, sx = int(H//2 - c[0]), int(W//2 - c[1])
    m = np.roll(mask, (sy, sx), (0, 1)); Lr = np.roll(L, (sy, sx), (0, 1))
    d = ndimage.distance_transform_edt(m); rim = m & (d <= 3); core = m & (d >= max(4.0, 0.5 * d.max()))
    if core.sum() < 3 or rim.sum() < 3: return None
    return float(Lr[rim].mean() / max(Lr[core].mean(), 1e-9))

def closure(mask, L, th=0.15):
    """share of the cell's contour band (inside, within 2 px of the edge) where links exceed th"""
    d = ndimage.distance_transform_edt(np.pad(mask, 3, mode="wrap"))[3:-3, 3:-3]
    band = mask & (d <= 2)
    return float((L[band] > th).mean()) if band.sum() else None

def wrapd(a, b):
    d = (a - b + np.array([H, W]) / 2) % np.array([H, W]) - np.array([H, W]) / 2
    return d

s = w.init(seed, (H, W))
hist = []
for t in range(T0):
    if t >= T0 - 400 and t % 20 == 0: hist.append(plabel(s["phi"] > 0.5))
    s = w.step(s)
lab = plabel(s["phi"] > 0.5); hist.append(lab)
ids, areas = np.unique(lab[lab > 0], return_counts=True); med = np.median(areas)
cands = []
for k, A in zip(ids, areas):
    if not (0.6 * med <= A <= 1.6 * med): continue
    m = lab == k; cur = m; ok = True
    for L0 in hist[-2::-1]:
        ov = L0[cur]; ov = ov[ov > 0]
        if len(ov) == 0: ok = False; break
        kk = np.bincount(ov).argmax(); prevm = L0 == kk
        if prevm.sum() > 1.4 * cur.sum() or prevm.sum() < 0.6 * cur.sum(): ok = False; break  # split/merge in window
        cur = prevm
    if not ok: continue
    v = wrapd(cen(m), cen(cur)); Req = np.sqrt(A / np.pi)
    ys, xs = np.nonzero(np.roll(m, (int(H//2 - cen(m)[0]), int(W//2 - cen(m)[1])), (0, 1)))
    ev = np.linalg.eigvalsh(np.cov(np.vstack([ys, xs])))
    asp = np.sqrt(ev[1] / max(ev[0], 1e-9))
    if np.hypot(*v) < 0.5 * Req or asp > 1.5: continue
    cands.append((float(np.hypot(*v)), int(k), v, int(A), float(asp)))
cands.sort(key=lambda z: -z[0])
picks = cands[:NPICK]
print("seed", seed, "median area", med, "candidates", len(cands), "picks", [(c[1], c[3], round(c[0], 1), round(c[4], 2)) for c in picks], flush=True)
res = {"seed": seed, "T0": T0, "T1": T1, "cells": []}
rows = []
for dist, k, v, A, asp in picks:
    m0 = lab == k; c0 = cen(m0)
    yy, xx = np.mgrid[0:H, 0:W]
    dy = (yy - c0[0] + H / 2) % H - H / 2; dx = (xx - c0[1] + W / 2) % W - W / 2
    proj = (dy * v[0] + dx * v[1]) / np.hypot(*v)
    for mode in os.environ.get("MODES", "front,ring").split(","):
        arms = {"twin": copy.deepcopy(s), "cut": copy.deepcopy(s)}
        if mode == "front":
            mask = m0 & (proj > np.quantile(proj[m0], 1 - FRONT))
            info = {"erased_px": int(mask.sum()), "erased_frac": float(mask.sum() / A),
                    "erased_L_frac": float(s["L"][mask].sum() / s["L"][m0].sum()), "erased_K_frac": float(s["K"][mask].sum() / s["K"][m0].sum())}
            if os.environ.get("ZERO_S"):  # (c32) stricter wound: matter deleted and no substrate left at the wound
                for q in ("K", "L", "phi", "S"): arms["cut"][q][mask] = 0.0
                info["zero_S"] = True
            elif os.environ.get("KEEP_S"):  # wound left with the substrate it had (no fresh bath S at the wound)
                for q in ("K", "L", "phi"): arms["cut"][q][mask] = 0.0
                info["keep_S"] = True
            else:
                arms["cut"] = w.damage(arms["cut"], mask)
            if os.environ.get("KILL_K"):  # (c32) control: also remove the catalyst from the rest of the cell
                arms["cut"]["K"][ndimage.binary_dilation(m0, iterations=4)] = 0.0
                info["kill_K"] = True
        else:
            reg = ndimage.binary_dilation(m0, iterations=4)
            info = {"erased_L": float(s["L"][reg].sum()), "erased_frac_area": 0.0}
            arms["cut"]["L"][reg] = 0.0
        tr = {a: [] for a in arms}; cur = {a: m0.copy() for a in arms}; snaps = {a: [] for a in arms}
        for i in range(T1 + 1):
            if i % 20 == 0:
                for a, st in arms.items():
                    Lb = plabel(st["phi"] > 0.5); ov = Lb[cur[a]]; ov = ov[ov > 0]
                    if len(ov) == 0: tr[a].append([i, 0, 0, None, np.nan, np.nan, None]); cur[a] = np.zeros_like(m0); continue
                    cnt = np.bincount(ov); kk = cnt.argmax(); mm = Lb == kk
                    npieces = int(sum(1 for q in np.nonzero(cnt)[0] if q > 0 and (Lb == q).sum() >= 20))
                    cc = cen(mm); cur[a] = mm
                    tr[a].append([i, int(mm.sum()), npieces, ring_score(mm, st["L"]), float(cc[0]), float(cc[1]), closure(mm, st["L"])])
                    if i % int(os.environ.get("SNAP", T1 // 6)) == 0:
                        sh = (int(H//2 - cc[0]), int(W//2 - cc[1]))
                        snaps[a].append((i, np.roll(st["phi"], sh, (0, 1))[H//2-28:H//2+28, W//2-28:W//2+28], np.roll(st["L"], sh, (0, 1))[H//2-28:H//2+28, W//2-28:W//2+28]))
            if i < T1:
                for a in arms: arms[a] = w.step(arms[a])
        summ = {}
        for a in arms:
            R = tr[a]; ar = np.array([r[1] for r in R], float); rs = [r[3] for r in R]
            pos = np.array([[r[4], r[5]] for r in R]); ok = ~np.isnan(pos[:, 0])
            steps = [wrapd(pos[j + 1], pos[j]) for j in range(len(pos) - 1) if ok[j] and ok[j + 1] and abs(ar[j+1] - ar[j]) < 0.3 * max(ar[j], 1)]
            path = float(np.hypot(*np.sum(steps, 0))) if steps else 0.0
            late = [x for x in rs[len(rs)//2:] if x is not None]
            summ[a] = {"area_start": int(ar[0]), "area_min": int(ar.min()), "area_end": int(ar[-1]),
                       "ring_start": rs[0], "ring_min": min([x for x in rs if x is not None], default=None),
                       "ring_median_2nd_half": float(np.median(late)) if late else None,
                       "frac_ring_ge_1p5_2nd_half": float(np.mean([x >= 1.5 for x in late])) if late else None,
                       "net_disp_px": round(path, 1), "net_disp_BL": round(path / (2 * np.sqrt(A / np.pi)), 2),
                       "lost_at": next((r[0] for r in R if r[1] == 0), None), "max_pieces": int(max(r[2] for r in R)),
                       "closure_t": [[r[0], None if r[6] is None else round(r[6], 3)] for r in R[:60:3]],
                       "first_closure_ge_0p9": next((r[0] for r in R if r[6] is not None and r[6] >= 0.9), None),
                       "area_back_to_start_at": next((r[0] for r in R[1:] if r[1] >= ar[0] * (1.0 if a == "twin" else 1 / (1 - FRONT))), None)}
        rec = {"cell": k, "area": A, "aspect": asp, "mode": mode, "damage": info, **{f"{a}": summ[a] for a in arms},
               "tracks": {a: [[r[0], r[1], r[2], None if r[3] is None else round(r[3], 3), None if np.isnan(r[4]) else round(r[4], 2), None if np.isnan(r[5]) else round(r[5], 2), None if r[6] is None else round(r[6], 3)] for r in tr[a]] for a in arms}}
        res["cells"].append(rec); print(json.dumps({k2: v2 for k2, v2 in rec.items() if k2 != "tracks"}), flush=True)
        rows.append((k, mode, snaps, tr))
fig, axs = plt.subplots(2 * len(rows), 8, figsize=(16, 4.2 * len(rows)))
for r, (k, mode, snaps, tr) in enumerate(rows):
    for j, a in enumerate(("twin", "cut")):
        row = axs[2 * r + j]
        for q in range(7):  # first 7 snapshots
            ax = row[q]; ax.set_xticks([]); ax.set_yticks([])
            if q < len(snaps[a]):
                i, ph, L = snaps[a][q]
                ax.imshow(L, cmap="viridis", vmin=0, vmax=0.6); ax.contour(ph, [0.5], colors="w", linewidths=0.6)
                ax.set_title(f"cell {k} {mode} {a} +{i}", fontsize=7)
        ax = row[7]; T = [x[0] for x in tr[a]]
        ax.plot(T, [x[3] if x[3] is not None else np.nan for x in tr[a]], label="ring score"); ax.axhline(1.5, color="k", lw=0.5)
        ax2 = ax.twinx(); ax2.plot(T, [x[1] for x in tr[a]], "r", lw=0.8, label="area"); ax.set_title(f"{a}: ring (blue), area (red)", fontsize=7)
fig.suptitle(f"ringswim-dl2 seed {seed}: branched twin vs damaged arm from t={T0}; link L (colour) and phi=1/2 contour (white)", fontsize=9)
fig.tight_layout(); fig.savefig(f"{out}/twinrepair.png", dpi=55)
json.dump(res, open(f"{out}/result.json", "w"), indent=1, default=float)
