"""Independent interface profile (c19): mean shell s and fuel f binned by signed distance to the
phi = 0 contour (positive inside bodies), over frames 40..end every 10th frame. A ring shows as a
peak of s near distance 0 above both the deep-inside (d >= 3) and far-outside (d <= -4) levels.
usage: ifprofile.py out.png label1=frames1.npz [label2=frames2.npz ...]"""
import sys, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
bins = np.arange(-8, 8.5, 1.0)
fig, ax = plt.subplots(1, 2, figsize=(9, 3.5))
for arg in sys.argv[2:]:
    lab, fn = arg.split("=")
    R = np.load(fn)["render"].astype(np.float32)
    S, F, C = np.zeros(len(bins) - 1), np.zeros(len(bins) - 1), np.zeros(len(bins) - 1)
    for i in range(40, len(R), 10):
        phi, s, f = R[i, 0], R[i, 2], R[i, 3]
        ins = phi > 0
        d = np.where(ins, ndimage.distance_transform_edt(ins), -ndimage.distance_transform_edt(~ins))
        k = np.digitize(d, bins) - 1; ok = (k >= 0) & (k < len(bins) - 1)
        S += np.bincount(k[ok], s[ok], len(bins) - 1); F += np.bincount(k[ok], f[ok], len(bins) - 1)
        C += np.bincount(k[ok], minlength=len(bins) - 1)
    S, F = S / np.maximum(C, 1), F / np.maximum(C, 1); x = 0.5 * (bins[1:] + bins[:-1])
    peak = S[np.abs(x) <= 1.5].max(); core = S[x >= 3][C[x >= 3] > 0].mean(); out = S[x <= -4].mean()
    print(f"{lab}: s peak@|d|<=1.5 {peak:.3f}, core(d>=3) {core:.3f}, outside(d<=-4) {out:.3f}, peak/core {peak/core:.2f}, peak/out {peak/out:.2f}; f core {F[x>=3][C[x>=3]>0].mean():.3f}, f outside {F[x<=-4].mean():.3f}")
    ax[0].plot(x, S, "-o", label=lab); ax[1].plot(x, F, "-o", label=lab)
for a, t in zip(ax, ["shell s", "fuel f"]):
    a.axvline(0, c="k", lw=0.5); a.set_xlabel("signed distance to phi=0 (px, + inside)"); a.set_title(t); a.legend(fontsize=7)
plt.tight_layout(); plt.savefig(sys.argv[1], dpi=90)
