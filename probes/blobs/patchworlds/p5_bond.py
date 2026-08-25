"""p5_bond.py MODE — P5 CHEMISTRY NEAR SEAMS: bonded pair straddling seam-1.

Bond ref: A=4 static bond d*=15.40px (composite; deep-static point tau=2.0,
Dv=2.0 — pair drift onset 5.636 is far away). Pair seeded at sep 15.4px
straddling x=48px: blob-L (40.3,96)px, blob-R (55.7,96)px.
MODE:
  ctrl    : uniform M4(2.0) (pmaps={}) — the null: bond in one world
  cross   : M0 | M4(2.0), w=4px — L blob lives in M0 (A=3: no certified bond
            well), R blob in M4 (bond world A=4)
  cross12 : same, w=12px
T=2500. Metrics: ncomp(t), sep(t), final sep, sep_std last 500tu.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worlds as WD
import patch_lib as P
G = P.G

mode = sys.argv[1]
gB = WD.gM4(2.0)
if mode == "ctrl":
    g, pm, rho = gB, {}, None
    w_px = 0.0
else:
    w_px = 12.0 if mode == "cross12" else 4.0
    g, pm, rho = WD.build_patch(WD.gM0(), gB, w_px)
N, dx = WD.N, WD.DX
F = P.state_vacuum_map(g, pm, N) if pm else G.state_vacuum(g, N)
xL, xR = 40.3, 55.7
if mode == "ctrl":
    F = WD.seed_m4(F, xL * dx, 48.0)
else:
    F = WD.seed_m0(F, g, xL * dx, 48.0)       # M0-side blob: native poke
F = WD.seed_m4(F, xR * dx, 48.0)
T = 2500.0
r = P.run_patched(g, pm, F=F, L=WD.LLU, dx=dx, T=T, rec_tu=5.0, save_fields=True)
pos = WD.pos_px(r, 0)
sep = np.full(pos.shape[0], np.nan)
for k in range(pos.shape[0]):
    if pos.shape[1] >= 2 and not np.isnan(pos[k, :2]).any():
        d = pos[k, 0] - pos[k, 1]
        sep[k] = np.hypot(d[0], d[1])
ncf = int(r["ncomp0"][-1])
last = sep[r["t"] >= T - 500]
sep_f = float(sep[-1]) if np.isfinite(sep[-1]) else -1.0
sep_std = float(np.nanstd(last))
xs = sorted([float(pos[-1, b, 1] % 192) for b in range(min(2, pos.shape[1]))
             if not np.isnan(pos[-1, b, 1])])
print(f"{mode}: ncomp {ncf}, sep final {sep_f:.2f}px (std500 {sep_std:.3f}), xs {xs}")
np.savez_compressed(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "data", f"p5_{mode}.npz"),
                    t=r["t"], pos=pos, ncomp=r["ncomp0"], sep=sep,
                    fields=r["fields"].astype(np.float32))
P.log(dict(test="P5_bond_at_seam", mode=mode, w_px=w_px, T=T,
           seed_sep_px=15.4, dstar_ref_px=15.40,
           ncomp_final=ncf, sep_final_px=sep_f, sep_std_last500=sep_std,
           final_xs_px=xs, status=r["status"], npz=f"data/p5_{mode}.npz"))
print("logged")
