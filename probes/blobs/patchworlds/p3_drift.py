"""p3_drift.py W_PX X0_PX [SIDE] — P3 blob drift near a non-aligned-vacuum seam.

M0|M0k1(-0.8) patch (same as p3_settle). Background pre-settled 300tu, then an
M0 blob is poked at (x0_px, 96px) and tracked T=2500. Logs drift vector
(dx toward seam +, dy along seam), final standoff from seam-1 (48px).
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worlds as WD
import patch_lib as P
G = P.G

w_px = float(sys.argv[1])
x0_px = float(sys.argv[2])
gA, gB = WD.gM0(), WD.gM0k1(-0.8)
g, pm, rho = WD.build_patch(gA, gB, w_px)
N, dx = WD.N, WD.DX
F0 = P.state_vacuum_map(g, pm, N)
pre = P.run_patched(g, pm, F=F0, L=WD.LLU, dx=dx, T=300.0, rec_tu=100.0,
                    save_fields=True)
F = pre["fields"]
F = WD.seed_m0(F, g, x0_px * dx, 48.0)
T = 2500.0
r = P.run_patched(g, pm, F=F, L=WD.LLU, dx=dx, T=T, rec_tu=5.0, save_fields=True)
pos = WD.pos_px(r, 0)
ok = r["ncomp0"][-1]
p0, p1 = pos[0, 0], pos[-1, 0]
dxp, dyp = p1[1] - p0[1], p1[0] - p0[0]
standoff = (p1[1] % 192) - 48.0
print(f"w={w_px} x0={x0_px}: ncomp {r['ncomp0'][-1]}, dx={dxp:+.2f}px dy={dyp:+.2f}px, "
      f"final x={(p1[1] % 192):.2f}px (standoff {standoff:+.2f}px from seam)")
np.savez_compressed(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "data", f"p3drift_w{w_px:g}_x{x0_px:g}.npz"),
                    t=r["t"], pos=pos, ncomp=r["ncomp0"])
P.log(dict(test="P3_blob_drift", w_px=w_px, x0_px=x0_px, T=T,
           seam_px=48.0, ncomp_final=int(r["ncomp0"][-1]),
           drift_dx_px=float(dxp), drift_dy_px=float(dyp),
           final_x_px=float(p1[1] % 192), final_standoff_px=float(standoff),
           status=r["status"],
           npz=f"data/p3drift_w{w_px:g}_x{x0_px:g}.npz"))
print("logged")
