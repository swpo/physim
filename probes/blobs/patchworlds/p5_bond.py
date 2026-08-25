"""p5_bond.py MODE — P5 CHEMISTRY NEAR SEAMS: bonded pair straddling seam-1.

Bond ref: A=4 static bond d* = 15.40 lu (composite E7b), certified deep-static.
B world = M4(4.0) (A=4, tau far below drift onsets). Pair seeded at sep
15.4 lu straddling seam-1 (x=24): L (16.3,48), R (31.7,48).
  ctrl   : uniform M4(4.0) everywhere (pmaps={}) — the null
  cross  : M0 | M4(4.0), w=24 lu — L blob in the A->seam ramp, R in B
  crossn : same, w=4 lu (narrow-seam contrast)
T=2500. Metrics: ncomp(t), sep(t), final sep, sep std last 500, survival.
NOTE: both blobs are A4 stamps; on the A side the world is M0 (A=3, static
blob exists, d* well UNKNOWN there — M2 bond was certified at A=5, M4 at A=4;
M0 A=3 tail is mono-dominant weaker: bond may not exist in pure A).
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worlds as WD
import patch_lib as P
G = P.G

mode = sys.argv[1]
gB = G.ref_M4(4.0)
if mode == "ctrl":
    g, pm, rho = gB, {}, None
    w_lu = 0.0
else:
    w_lu = 4.0 if mode == "crossn" else 24.0
    g, pm, rho = WD.build(G.ref_M0(), gB, w_lu)
F = P.state_vacuum_map(g, pm, WD.N) if pm else G.state_vacuum(g, WD.N)
xL, xR = 16.3, 31.7
F = WD.seed_m4(F, xL, 48.0)
F = WD.seed_m4(F, xR, 48.0)
T = 2500.0
r = P.run_patched(g, pm, F=F, L=WD.LLU, dx=WD.DX, T=T, rec_tu=5.0,
                  save_fields=True)
pos = WD.pos_lu(r, 0)
sep = np.full(pos.shape[0], np.nan)
for k in range(pos.shape[0]):
    if pos.shape[1] >= 2 and not np.isnan(pos[k, :2]).any():
        d = pos[k, 0] - pos[k, 1]
        sep[k] = np.hypot(d[0], d[1])
ncf = int(r["ncomp0"][-1])
last = sep[r["t"] >= T - 500]
sep_f = float(sep[-1]) if np.isfinite(sep[-1]) else -1.0
sep_std = float(np.nanstd(last))
xs = sorted(float(pos[-1, b, 1] % 96) for b in range(min(2, pos.shape[1]))
            if not np.isnan(pos[-1, b, 1]))
print(f"{mode}: ncomp {ncf} sep_final {sep_f:.2f} (std500 {sep_std:.3f}) xs {xs}")
np.savez_compressed(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "data", f"p5_{mode}.npz"),
                    t=r["t"], pos=pos, ncomp=r["ncomp0"], sep=sep,
                    fields=r["fields"].astype(np.float32))
P.log(dict(test="P5_bond_at_seam", mode=mode, w_lu=w_lu, T=T,
           seed_sep_lu=15.4, dstar_ref_lu=15.40, seam1_lu=24.0,
           ncomp_final=ncf, sep_final_lu=sep_f, sep_std_last500=sep_std,
           final_xs_lu=xs, status=r["status"], npz=f"data/p5_{mode}.npz"))
print("logged")
