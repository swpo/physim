"""p4_halo.py MODE — P4 HALO LEAK across the aligned-vacuum M0|M4(4.0) seam.

B = M4 tau=4.0 (A=4 STATIC family point: far below onsets; any B-blob motion
is caused by the A-blob's halo, not autonomous drift). w=24 lu tanh seam
(parent: certify at wide). Seam-1 at 24 lu.
  ctrl   : lone B blob at (44,48)   [20 lu into B from seam]
  near   : A blob (16,48) [8 lu from seam] + B blob (44,48)   sep 28 lu
  close  : A blob (16,48) + B blob (36,48)                    sep 20 lu
  ctrlcl : lone B blob at (36,48)
  aalone : lone A blob at (16,48) — seam SELF-force control (wiring-blend
           seams may push statics even with aligned vacuum; rho_B(16)=0.33
           at w=24 so the blob sits on the ramp)
T=2000. Metrics: B displacement vs its ctrl (px), A drift, w-channel profile
along y=48 at t=1000 (halo penetration decay into B).
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worlds as WD
import patch_lib as P
G = P.G

mode = sys.argv[1]
W_LU = 24.0
g, pm, rho = WD.pair_M0_M4(4.0, W_LU)
F = P.state_vacuum_map(g, pm, WD.N)
xB = dict(ctrl=44.0, near=44.0, close=36.0, ctrlcl=36.0, aalone=None)[mode]
if mode in ("near", "close", "aalone"):
    F = WD.seed_m0(F, g, 16.0, 48.0)
if xB is not None:
    F = WD.seed_m4(F, xB, 48.0)
T = 2000.0
r = P.run_patched(g, pm, F=F, L=WD.LLU, dx=WD.DX, T=T, rec_tu=5.0,
                  snap_times=(1000.0,), save_fields=True)
pos = WD.pos_lu(r, 0)
nb = pos.shape[1]
labels = {}
for b in range(nb):
    if np.isnan(pos[0, b, 1]):
        continue
    labels["A" if abs(pos[0, b, 1] - 16.0) < 6 else "B"] = b
out = dict(test="P4_halo", mode=mode, w_lu=W_LU, xB0_lu=xB or -1.0, T=T,
           tau_B=4.0, ncomp_final=int(r["ncomp0"][-1]), status=r["status"])
for lab, b in labels.items():
    m = ~np.isnan(pos[:, b, 1])
    p = pos[m, b, :]
    out[f"{lab}_disp_lu"] = [float(p[-1, 1] - p[0, 1]), float(p[-1, 0] - p[0, 0])]
    out[f"{lab}_final_x_lu"] = float(p[-1, 1] % 96)
snap = r["snaps"][1000.0]
np.savez_compressed(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "data", f"p4_{mode}.npz"),
                    t=r["t"], pos=pos, ncomp=r["ncomp0"],
                    u_row=snap[0][96, :], v_row=snap[1][96, :],
                    w_row=snap[2][96, :],
                    fields=r["fields"].astype(np.float32))
out["npz"] = f"data/p4_{mode}.npz"
print(mode, {k: v for k, v in out.items() if k.endswith("_disp_lu")},
      "ncomp", out["ncomp_final"])
P.log(out)
print("logged")
