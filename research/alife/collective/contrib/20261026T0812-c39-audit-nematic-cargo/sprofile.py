"""(c39) Signed-distance profile of surfactant s (ch2) and cargo c (ch3) around all bodies (phi>0), periodic,
pooled over render frames >= 20. Prints mean s and c per 1-px distance bin from d=-4 (deep inside) to d=+14
(far bath), and the Boltzmann prediction exp(-kappa (s_in - s_out)) for the cargo in/out ratio.
usage: sprofile.py frames.npz [kappa=20]"""
import sys, numpy as np
from scipy import ndimage
F = np.load(sys.argv[1]); R = F["render"].astype(np.float32); rf = list(F["render_f"])
kap = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0
H, W = R.shape[2:]; sl = (slice(H, 2 * H), slice(W, 2 * W))
bins = np.arange(-4, 15); S = {b: [] for b in bins}; C = {b: [] for b in bins}
for k, f in enumerate(rf):
    if f < 20: continue
    ins = R[k, 0] > 0; t = np.tile(ins, (3, 3))
    d = np.where(t, -(ndimage.distance_transform_edt(t) - 0.5), ndimage.distance_transform_edt(~t) - 0.5)[sl]
    db = np.clip(np.floor(d + 0.5), -4, 14).astype(int)
    for b in bins:
        m = db == b
        if m.any(): S[b].append(R[k, 2][m].mean()); C[b].append(R[k, 3][m].mean())
print("d    s_mean   c_mean")
for b in bins:
    if S[b]: print(f"{b:3d}  {np.mean(S[b]):.3f}   {np.mean(C[b]):.4f}")
sin = np.mean([np.mean(S[b]) for b in (-3, -2, -1) if S[b]]); sout = np.mean([np.mean(S[b]) for b in (2, 3, 4) if S[b]])
cin = np.mean([np.mean(C[b]) for b in (-3, -2, -1) if C[b]]); cout = np.mean([np.mean(C[b]) for b in (2, 3, 4) if C[b]])
sfar = np.mean([np.mean(S[b]) for b in range(8, 15) if S[b]])
print(f"s inside(d -3..-1) {sin:.3f}, near out(2..4) {sout:.3f}, far bath(8..14) {sfar:.3f}, rim(0) {np.mean(S[0]):.3f}")
print(f"cargo in/out (pooled means) {cin/cout:.2f}; Boltzmann exp(kappa (s_out - s_in)) {np.exp(kap*(sout-sin)):.2f}")
