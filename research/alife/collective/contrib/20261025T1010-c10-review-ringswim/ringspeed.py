"""Ring strength vs speed per cell. Cells = components of (K + L + wall) > thr in the recorded render frames
(min 30 px, periodic labels merged). Ring score = labkit's radial test per cell: mean L at rho = r/R_eq in [0.6, 1.3] / mean L at rho < 0.4. Speed: the cell is
matched to the next recorded frame by largest overlap (1:1 only, no split/merge in between) and to frames up to
+lag later; displacement over lag frames / sqrt(area) = body lengths per lag.
Usage: ringspeed.py pack_seed_dir thr lag"""
import sys, json, numpy as np
from scipy import ndimage
d, thr, lag = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
F = np.load(d + "/frames.npz"); R = F["render"].astype(float); rf = F["render_f"]
H, W = R.shape[2:]
def cells(i):
    m = (R[i, 1] + R[i, 2] + R[i, 3]) > thr
    lab, n = ndimage.label(m)
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):
        for u, v in set(zip(a.tolist(), b.tolist())):
            if u and v and u != v: lab[lab == v] = u
    ids = [k for k in np.unique(lab) if k and (lab == k).sum() >= 30]
    return lab, ids
def centroid(mask):
    ys, xs = np.nonzero(mask)
    cy = np.angle(np.exp(2j * np.pi * ys / H).mean()) * H / (2 * np.pi) % H
    cx = np.angle(np.exp(2j * np.pi * xs / W).mean()) * W / (2 * np.pi) % W
    return cy, cx
def ring(i, mask):
    """labkit's radial test for one cell: mean L at rho = r / R_eq in [0.6, 1.3] over mean L at rho < 0.4."""
    cy, cx = centroid(mask); Req = np.sqrt(mask.sum() / np.pi)
    yy = (np.arange(H)[:, None] - cy + H / 2) % H - H / 2; xx = (np.arange(W)[None, :] - cx + W / 2) % W - W / 2
    rho = np.hypot(yy, xx) / Req; L = R[i, 2]
    core = rho < 0.4; rim = (rho >= 0.6) & (rho <= 1.3)
    if core.sum() < 3: return np.nan
    return L[rim].mean() / max(L[core].mean(), 1e-9)


C = [cells(i) for i in range(len(R))]
rows = []
for i in range(len(R) - lag):
    lab, ids = C[i]
    for k in ids:
        m = lab == k; cur = m; ok = True
        for j in range(i + 1, i + lag + 1):
            lj, idj = C[j]
            ov = [x for x in np.unique(lj[cur]) if x in idj]
            if len(ov) != 1: ok = False; break
            cur = lj == ov[0]
            back = [x for x in np.unique(C[j - 1][0][cur]) if x]
            if len(back) != 1: ok = False; break
        if not ok: continue
        (y0, x0), (y1, x1) = centroid(m), centroid(cur)
        dy = (y1 - y0 + H / 2) % H - H / 2; dx = (x1 - x0 + W / 2) % W - W / 2
        rows.append((int(rf[i]), int(k), float(np.hypot(dy, dx) / np.sqrt(m.sum())), float(ring(i, m)), int(m.sum())))
rows = np.array([r for r in rows if np.isfinite(r[3])])
bl = rows[:, 2]; rs = rows[:, 3]
out = {"n": len(rows), "lag_frames": lag}
for name, sel in (("still (< 0.3 BL per lag)", bl < 0.3), ("moving (>= 0.5 BL per lag)", bl >= 0.5), ("fast (>= 1 BL per lag)", bl >= 1.0)):
    out[name] = {"n": int(sel.sum()), "ring median": round(float(np.median(rs[sel])), 2) if sel.any() else None,
                 "share ring >= 1.5": round(float((rs[sel] >= 1.5).mean()), 2) if sel.any() else None}
out["spearman(ring, BL)"] = round(float(np.corrcoef(np.argsort(np.argsort(rs)), np.argsort(np.argsort(bl)))[0, 1]), 2)
print(d, json.dumps(out))
