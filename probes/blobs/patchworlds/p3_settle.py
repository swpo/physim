"""p3_settle.py W_PX — P3 NON-ALIGNED VACUA, background settle (no blob).

A = M0 (k1_orig=-0.7, u0=-0.7035); B = M0 with k1_orig=-0.8 (u0=-0.7514):
du0 = -0.0479 (ds3_014-scale mismatch). No iso-vacuum correction: pmaps on
k1_g and u0 only (wiring identical). Pre-run predicted seam source at w=8px:
chord residual 1.25e-3 + Du lap u0 1.12e-3 ~ 2.4e-3 (controller: ~2e-3). Run
vacuum T=1000, rhs_probe: log initial RHS max, final residual motion, final
u(x) profile vs naive blend, nucleation count.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worlds as WD
import patch_lib as P
G = P.G

w_px = float(sys.argv[1])
gA, gB = WD.gM0(), WD.gM0k1(-0.8)
g, pm, rho = WD.build_patch(gA, gB, w_px)
print("pmaps:", {k: list(v) for k, v in pm.items()})
N, dx = WD.N, WD.DX
F0 = P.state_vacuum_map(g, pm, N)
T = 1000.0
r = P.run_patched(g, pm, F=F0, L=WD.LLU, dx=dx, T=T, rec_tu=5.0,
                  rhs_probe=True, save_fields=True, snap_times=(1000.0,))
rhs_max0 = r["rhs0"]["max_abs"]
Ff = r["fields"]
u0map = pm["u0"][0]
prof_u = Ff[0][96, :]
prof_u0 = u0map[96, :]
dev = prof_u - prof_u0
# residual motion at end: one more RHS eval via a tiny re-run
r2 = P.run_patched(g, pm, F=Ff, L=WD.LLU, dx=dx, T=0.1, rec_tu=0.1,
                   rhs_probe=True, save_fields=False)
rhs_end = r2["rhs0"]["max_abs"]
nuc = int(r["ncomp0"][-1])
print(f"w={w_px}: RHS0 max u={rhs_max0[0]:.3e}; end RHS u={rhs_end[0]:.3e}; "
      f"max|u-u0map|={np.max(np.abs(dev)):.4f} at x={np.argmax(np.abs(dev))/2:.0f}lu; nuc={nuc}")
np.savez_compressed(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "data", f"p3settle_w{w_px:g}.npz"),
                    prof_u=prof_u, prof_u0=prof_u0, rho=rho[96],
                    x_px=np.arange(N), fields=Ff.astype(np.float32))
P.log(dict(test="P3_settle", w_px=w_px, du0=-0.04789, T=T,
           mismatch="k1_orig -0.7 vs -0.8 (u0 -0.7035 vs -0.7514), wiring identical",
           rhs_t0_max=[float(v) for v in rhs_max0],
           rhs_end_max=[float(v) for v in rhs_end],
           max_settled_dev_from_naive_u0=float(np.max(np.abs(dev))),
           nucleated_ncomp=nuc, status=r["status"],
           npz=f"data/p3settle_w{w_px:g}.npz"))
print("logged")
