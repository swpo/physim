"""Classify the repair path in labkit packs of world_r2 with a front cut at t=8 from the recorded fields:
per frame, polarized fraction (rho>1/2 inside phi>1/2), rho contrast p90-p10 inside, and the polarity offset |d|
(rho*phi centroid minus phi centroid, periodic). Non-polar = whole cell polarized and |d| < 0.02."""
import sys, numpy as np
L = 5.0
def cent(w, N):
    out = []
    for ax in (1, 0):
        a = 2 * np.pi * np.arange(N) / N
        prof = w.sum(axis=1 - ax) if ax == 1 else w.sum(axis=1)
        out.append((np.arctan2((prof * np.sin(a)).sum(), (prof * np.cos(a)).sum()) % (2 * np.pi)) * L / (2 * np.pi))
    return np.array(out)
for p in sys.argv[1:]:
    f = np.load(p); R = f["render"]; fr = f["render_f"]
    rows = []
    for j in range(len(fr)):
        phi, rho = R[j, 0], R[j, 1]; N = phi.shape[0]; m = phi > 0.5
        if m.sum() < 10: rows.append((fr[j] * 0.2, 0, 0, 0, 0)); continue
        q = rho * phi
        d = cent(q, N) - cent(phi, N); d = (d + L / 2) % L - L / 2
        rows.append((fr[j] * 0.2, m.sum() * (L / N) ** 2, ((rho > 0.5) & m).sum() / m.sum(), float(np.hypot(*d)), float(np.percentile(rho[m], 90) - np.percentile(rho[m], 10))))
    rows = np.array(rows); post = rows[rows[:, 0] > 8.0]
    nonpolar = post[(post[:, 2] > 0.97) & (post[:, 3] < 0.02)]
    print(p, "non-polar frames after cut:", len(nonpolar), ("t=%.1f-%.1f" % (nonpolar[0, 0], nonpolar[-1, 0])) if len(nonpolar) else "",
          "| min |d| after cut %.3f" % post[:15, 3].min(), "| final |d| %.3f, polarized frac %.2f" % (post[-1, 3], post[-1, 2]))
