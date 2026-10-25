"""Quick ring screen: run pcell-yeff-cap with overrides, report per-cell L rim/core, rim/out, cell count."""
import sys, json, time, importlib.util, numpy as np
from scipy import ndimage
spec = importlib.util.spec_from_file_location("w", sys.argv[1]); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
ov = json.loads(sys.argv[2]); T = int(sys.argv[3]); seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
w.P.update(ov)
s = w.init(seed, (128, 128)); t0 = time.time()
def ring(s):
    phi, L = s["phi"], s["L"]
    lab, n = ndimage.label(phi > 0.5)
    rc, ro, ar, mrc = [], [], [], []
    M = s.get("M")
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < 30: continue
        d_in = ndimage.distance_transform_edt(m); R = np.sqrt(m.sum() / np.pi)
        d_out = ndimage.distance_transform_edt(~m)
        core = m & (d_in > 0.6 * R); rim = (m & (d_in <= 0.4 * R)) | (~m & (d_out <= 0.3 * R))
        out = (~m) & (d_out > 0.6 * R) & (d_out < 1.2 * R)
        if core.sum() < 3: continue
        if M is not None: mrc.append(M[rim].mean() / max(M[core].mean(), 1e-9))
        rc.append(L[rim].mean() / max(L[core].mean(), 1e-9)); ro.append(L[rim].mean() / max(L[out].mean(), 1e-9)); ar.append(m.sum())
    return n, rc, ro, ar, mrc
for t in range(1, T + 1):
    w.step(s)
    if t % (T // int(sys.argv[5] if len(sys.argv) > 5 else 5)) == 0:
        n, rc, ro, ar, mrc = ring(s)
        y = s["y"].mean()
        print(f"t={t} cells={len(rc)} N={len(s['py'])} Mrc={np.median(mrc) if mrc else 0:.2f} rimcore={np.median(rc) if rc else 0:.2f} rimout={np.median(ro) if ro else 0:.2f} area={np.median(ar) if ar else 0:.0f} y={y:.3f} ({time.time()-t0:.0f}s)", flush=True)
