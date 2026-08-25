"""p3_drift.py W_LU X0_LU — P3 blob drift near a non-aligned-vacuum seam.

M0 | M0(k1_orig=-0.8) patch (du0=-0.0479, wiring identical). Background
pre-settled 300 tu, then an M0 blob poked at (x0, 48) lu, T=2500.
Transport analogy: k1-ramp mode — expect drift along the local k1 gradient
(toward the shallower-vacuum side?) + possible along-seam drift. Logs drift
vector and final standoff from seam-1 (x=24 lu).
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worlds as WD
import patch_lib as P
G = P.G

w_lu = float(sys.argv[1])
x0 = float(sys.argv[2])
g, pm, rho = WD.pair_vac(-0.8, w_lu)
F0 = P.state_vacuum_map(g, pm, WD.N)
pre = P.run_patched(g, pm, F=F0, L=WD.LLU, dx=WD.DX, T=300.0, rec_tu=100.0,
                    save_fields=True)
F = pre["fields"]
F = WD.seed_m0(F, g, x0, 48.0)
T = 2500.0
r = P.run_patched(g, pm, F=F, L=WD.LLU, dx=WD.DX, T=T, rec_tu=5.0,
                  save_fields=True)
pos = WD.pos_lu(r, 0)
m = ~np.isnan(pos[:, 0, 1])
p = pos[m, 0, :]
dxl, dyl = float(p[-1, 1] - p[0, 1]), float(p[-1, 0] - p[0, 0])
xf = float(p[-1, 1] % 96)
print(f"w={w_lu} x0={x0}: ncomp {int(r['ncomp0'][-1])} dx={dxl:+.2f} dy={dyl:+.2f} "
      f"xfinal={xf:.2f} (seam1 at 24)")
np.savez_compressed(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "data", f"p3drift_w{w_lu:g}_x{x0:g}.npz"),
                    t=r["t"], pos=pos, ncomp=r["ncomp0"])
P.log(dict(test="P3_blob_drift", w_lu=w_lu, x0_lu=x0, T=T, seam1_lu=24.0,
           du0=-0.04789, ncomp_final=int(r["ncomp0"][-1]),
           drift_dx_lu=dxl, drift_dy_lu=dyl, final_x_lu=xf,
           final_standoff_lu=xf - 24.0, status=r["status"],
           npz=f"data/p3drift_w{w_lu:g}_x{x0:g}.npz"))
print("logged")
