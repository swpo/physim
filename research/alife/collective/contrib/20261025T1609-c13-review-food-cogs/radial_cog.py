"""radial profiles of A0, A1, F around isolated cog centres (A0 centre of mass), frames from t>=200. usage: radial_cog.py frames.npz out.png"""
import sys, json, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
d = np.load(sys.argv[1]); X = d['render'].astype(np.float32); out = sys.argv[2]; H, W = X.shape[2:]
yy, xx = np.mgrid[:H, :W]; nb = np.arange(0, 30); profs = []
for f in range(len(X)//5, len(X), 3):
    A = X[f]; lab, k = ndimage.label(ndimage.gaussian_filter(A[0], 1) > 0.3)
    cs = ndimage.center_of_mass(A[0], lab, range(1, k+1)); sz = ndimage.sum(np.ones_like(A[0]), lab, range(1, k+1))
    for i, (cy, cx) in enumerate(cs):
        if sz[i] < 20: continue
        dd = [np.hypot(min(abs(cy-y), H-abs(cy-y)), min(abs(cx-x), W-abs(cx-x))) for j, (y, x) in enumerate(cs) if j != i and sz[j] >= 10]
        if dd and min(dd) < 40: continue
        r = np.hypot(np.minimum(abs(yy-cy), H-abs(yy-cy)), np.minimum(abs(xx-cx), W-abs(xx-cx))).astype(int)
        profs.append([[A[c][r == q].mean() for q in nb] for c in range(3)])
P = np.array(profs); m = P.mean(0); n = len(P)
a1 = m[1]; ish = 6 + int(np.argmax(a1[6:20])); itr = 1 + int(np.argmin(a1[1:ish])); a0pk = int(np.argmax(m[0]))
res = {"n_cell_frames": n, "A1_shell_r": ish, "A1_shell": round(float(a1[ish]), 3), "A1_trough_r": itr, "A1_trough": round(float(a1[itr]), 3),
       "A1_centre": round(float(a1[0]), 3), "A1_outside_r25_29": round(float(a1[25:].mean()), 4), "A0_peak_r": a0pk, "A0_at_shell_r": round(float(m[0][ish]), 3),
       "shell_over_trough": round(float(a1[ish]/max(a1[itr], 1e-9)), 2), "shell_over_outside": round(float(a1[ish]/max(a1[25:].mean(), 1e-9)), 1),
       "per_cell_shell_over_trough_min": round(float(np.min(P[:, 1, ish]/np.maximum(P[:, 1, itr], 1e-9))), 2)}
print(json.dumps(res))
plt.figure(figsize=(5.2, 3.6))
for c, nm in enumerate(['A0 (core)', 'A1 (shell)', 'F (food)']):
    plt.plot(nb, m[c], label=nm); plt.fill_between(nb, P[:, c].min(0), P[:, c].max(0), alpha=0.15)
plt.axvline(ish, ls=':', c='C1'); plt.axvline(itr, ls=':', c='gray')
plt.xlabel('r (px) from cog centre (A0 centre of mass); R=10'); plt.ylabel('mean (band: min-max over cells)'); plt.legend(fontsize=7)
plt.title(f'isolated cogs, {n} cell-frames', fontsize=9); plt.tight_layout(); plt.savefig(out, dpi=80)
json.dump(res, open(out[:-4]+'.json', 'w'), indent=1)
