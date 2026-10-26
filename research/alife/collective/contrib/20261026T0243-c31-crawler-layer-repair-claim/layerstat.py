import sys, numpy as np
from scipy import ndimage
L = 5.0
for f in sys.argv[1:]:
    d = np.load(f); phi, S = d["phi"], d["s"]; n = phi.shape[0]; dx = L / n
    # centre on the phi centroid (periodic, via angles)
    idx = np.arange(n) * dx
    cx = (np.angle((phi * np.exp(2j*np.pi*idx[None, :]/L)).sum()) % (2*np.pi)) * L/(2*np.pi)
    cy = (np.angle((phi * np.exp(2j*np.pi*idx[:, None]/L)).sum()) % (2*np.pi)) * L/(2*np.pi)
    sh = (int(round((L/2 - cy)/dx)), int(round((L/2 - cx)/dx)))
    p, s = np.roll(phi, sh, (0, 1)), np.roll(S, sh, (0, 1)); m = p > 0.5
    sd = (ndimage.distance_transform_edt(~m) - ndimage.distance_transform_edt(m)) * dx
    rim = np.abs(sd) < 0.06; core = sd < -0.3; out = (sd > 0.3) & (sd < 0.8)
    print(f"{f}: n={n} s rim {s[rim].mean():.3f} core {s[core].mean():.3f} out {s[out].mean():.4f} rim/core {s[rim].mean()/s[core].mean():.2f} rim/out {s[rim].mean()/s[out].mean():.1f}")
