"""p6_force.py W_LU D_LU — seam force probe: FRESH static M0 blob at distance
D_LU from seam-1 (x = 24 - D_LU) in the aligned-vacuum M0|M4(5.8) patch.
No kick, no crossing history. T=1500. Measures the seam's own force on a
static blob vs distance (sign + magnitude): the "is the seam a wall, well,
or nothing" curve. Also disambiguates P2 post-crossing creep (momentum/wake
memory vs static seam force).
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worlds as WD
import patch_lib as P
G = P.G

w_lu = float(sys.argv[1])
d_lu = float(sys.argv[2])
x0 = 24.0 - d_lu
g, pm, rho = WD.pair_M0_M4(5.8, w_lu)
F = P.state_vacuum_map(g, pm, WD.N)
F = WD.seed_m0(F, g, x0, 48.0)
T = 1500.0
r = P.run_patched(g, pm, F=F, L=WD.LLU, dx=WD.DX, T=T, rec_tu=5.0,
                  save_fields=False)
pos = WD.pos_lu(r, 0)
t = r["t"]
m = ~np.isnan(pos[:, 0, 1])
x = pos[m, 0, 1]
tm = t[m]
disp = float(x[-1] - x[0])
sl = tm >= tm[-1] - 300
v_end = float(np.polyfit(tm[sl], x[sl], 1)[0])
s2 = (tm >= 200) & (tm <= 600)
v_mid = float(np.polyfit(tm[s2], x[s2], 1)[0])
print(f"w={w_lu} d={d_lu}: x {x[0]:.2f}->{x[-1]:.2f} disp={disp:+.3f} "
      f"v_mid={v_mid:+.6f} v_end={v_end:+.6f} ncomp={int(r['ncomp0'][-1])}")
P.log(dict(test="P6_seam_force", w_lu=w_lu, d_lu=d_lu, x0_lu=x0, T=T,
           disp_lu=disp, v_mid=v_mid, v_end=v_end,
           ncomp_final=int(r["ncomp0"][-1]), status=r["status"]))
print("logged")
