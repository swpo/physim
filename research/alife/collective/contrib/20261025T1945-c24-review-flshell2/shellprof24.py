"""S around isolated bodies (no other body within 30 px), frames t>=100: radial profile (px) and angular closure at the S peak radius."""
import sys, json, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
res = {}; fig, ax = plt.subplots(1, 3, figsize=(13, 3.4))
for s in (24,):
    d = np.load(f'rerun/seed{s}/frames.npz'); X = d['render'].astype(np.float32); H, W = X.shape[2:]; yy, xx = np.mgrid[:H, :W]
    profs = []; clos = []
    for f in range(len(X)//8, len(X), 4):
        A = X[f, :2].sum(0); S = X[f, 3]
        lab, k = ndimage.label(ndimage.gaussian_filter(A, 1, mode='wrap') > 0.15)
        cs = ndimage.center_of_mass(A, lab, range(1, k+1)); sz = ndimage.sum(np.ones_like(A), lab, range(1, k+1))
        for i, (cy, cx) in enumerate(cs):
            if sz[i] < 20: continue
            dd = [np.hypot(min(abs(cy-y), H-abs(cy-y)), min(abs(cx-x), W-abs(cx-x))) for j, (y, x) in enumerate(cs) if j != i and sz[j] >= 10]
            if dd and min(dd) < 30: continue
            dy = (yy - cy + H/2) % H - H/2; dx = (xx - cx + W/2) % W - W/2; r = np.hypot(dy, dx); th = np.arctan2(dy, dx)
            p = np.array([[X[f, c][(r >= q) & (r < q+1)].mean() for q in range(25)] for c in (0, 1, 3)]); profs.append(p)
            rp = int(np.argmax(p[2])); band = (r >= rp - 1) & (r < rp + 2)
            bins = np.digitize(th[band], np.linspace(-np.pi, np.pi, 25)); vals = [S[band][bins == b].max() if (bins == b).any() else 0 for b in range(1, 25)]
            clos.append(np.mean(np.array(vals) > 0.3))
    P = np.array(profs); m = P.mean(0); rp = int(np.argmax(m[2]))
    res[s] = {"n_body_frames": len(P), "S_peak_r_px": rp, "S_peak": round(float(m[2][rp]), 3), "S_inside_r<4": round(float(m[2][:4].mean()), 4), "S_outside_r20-24": round(float(m[2][20:].mean()), 4),
              "A_at_S_peak": round(float(m[0][rp] + m[1][rp]), 4), "closure_median_fraction_of_24_sectors_S>0.3": round(float(np.median(clos)), 2), "closed_rings_fraction": round(float(np.mean(np.array(clos) >= 0.95)), 2)}
    for c, nm in enumerate(['A0', 'A1', 'S']): ax[0].plot(range(25), m[c], label=nm)
    ax[0].set_title(f'seed {s}: {len(P)} isolated body-frames', fontsize=9); ax[0].set_xlabel('r (px) from body centre'); ax[0].legend(fontsize=7)
plt.tight_layout(); plt.savefig('shellprof_s24.png', dpi=70); print(json.dumps(res, indent=1)); json.dump(res, open('shellprof_s24.json', 'w'), indent=1)
