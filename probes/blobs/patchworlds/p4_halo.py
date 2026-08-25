"""p4_halo.py MODE — P4 HALO LEAK across an aligned-vacuum M0|M4(5.6) seam.

Patch: A=M0, B=M4 tau=5.6 (static family; single onset 5.748, pair 5.636 —
5.6 is static so any B-blob motion is attributable to the A-blob halo).
w=4px seam at 48px. MODE:
  ctrl : only B blob at (63,96)px         (15px into B from seam)
  near : A blob (40,96) + B blob (63,96)  (A 8px from seam; A-B sep 23px)
  far  : A blob (40,96) + B blob (73,96)  (sep 33px)
  ctrlfar: only B at (73,96)
T=2000. Logs: B displacement vector vs ctrl, A displacement, w-halo profile
along y=96px at t=1000 (decay in A vs decay across seam into B).
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worlds as WD
import patch_lib as P
G = P.G

mode = sys.argv[1]
gA, gB = WD.gM0(), WD.gM4(5.6)
g, pm, rho = WD.build_patch(gA, gB, 4.0)
N, dx = WD.N, WD.DX
F = P.state_vacuum_map(g, pm, N)
xB = 63.0 if mode in ("ctrl", "near") else 73.0
if mode in ("near", "far"):
    F = WD.seed_m0(F, g, 20.0, 48.0)          # A blob at 40px=20lu
F = WD.seed_m4(F, xB * dx, 48.0)              # B blob (A4 stamp, static at 5.6)
T = 2000.0
r = P.run_patched(g, pm, F=F, L=WD.LLU, dx=dx, T=T, rec_tu=5.0,
                  snap_times=(1000.0,), save_fields=True)
pos = WD.pos_px(r, 0)
nb = pos.shape[1]
# identify blobs by initial x
labels = {}
for b in range(nb):
    x0 = pos[0, b, 1]
    labels["A" if abs(x0 - 40.0) < 8 else "B"] = b
out = dict(test="P4_halo", mode=mode, xB0_px=xB, T=T, w_px=4.0,
           ncomp_final=int(r["ncomp0"][-1]), status=r["status"])
for lab, b in labels.items():
    p0, p1 = pos[0, b], pos[-1, b]
    out[f"{lab}_disp_px"] = [float(p1[1] - p0[1]), float(p1[0] - p0[0])]
    out[f"{lab}_final_x_px"] = float(p1[1] % 192)
# w-halo profile at t=1000 along the blob row (w = chan index 2 -> field na+1=2)
snap = r["snaps"][1000.0]
wrow = snap[2][96, :].copy()
np.savez_compressed(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "data", f"p4_{mode}.npz"),
                    t=r["t"], pos=pos, ncomp=r["ncomp0"], w_row=wrow,
                    u_row=snap[0][96, :], v_row=snap[1][96, :],
                    fields=r["fields"].astype(np.float32))
out["npz"] = f"data/p4_{mode}.npz"
disp = {k: v for k, v in out.items() if k.endswith("_disp_px")}
print(f"{mode}: ncomp {out['ncomp_final']} disp {disp}")
P.log(out)
print("logged")
