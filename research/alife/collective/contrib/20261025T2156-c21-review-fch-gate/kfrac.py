"""(c21) Share of catalyst K inside bilayers (u+1 > 0.5) and channel totals, at the last render frame and averaged
over render frames with t >= 300, from labkit frames (channels u+1, P, K). usage: kfrac.py frames.npz [...]"""
import sys, numpy as np
for fn in sys.argv[1:]:
    F = np.load(fn); R = F["render"].astype(np.float64); rf = np.array(F["render_f"]) * 3.0
    def one(k):
        u, K = R[k, 0], R[k, 2]; m = u > 0.5
        return K[m].sum() / max(K.sum(), 1e-12), m.mean(), u.sum(), K.sum()
    last = one(len(R) - 1); late = np.array([one(k) for k in range(len(R)) if rf[k] >= 300])
    print(f"{fn}: t={rf[-1]:.0f} K_in_bilayer {last[0]:.2f} bilayer_area {last[1]:.3f} u_total {last[2]:.0f} K_total {last[3]:.1f} | t>=300 mean K_in_bilayer {late[:, 0].mean():.2f}")
