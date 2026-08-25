"""p2_seam.py W_LU DIR — P2 ALIGNED-VACUUM PATCH: traveler vs seam.

Patch: A=M0 (tau=3, Dv=1, A=3: statics-only), B=M4(5.8) (Dv=0.6897, A=4:
traveling; single onset tau_c=5.748, c=0.055 lu/tu). Both tau AND Dv are
blended (Dv via flux-form dD split). Vacua identical.

DIR=out: traveler starts at band center (48,48) kicked 180deg (-x) toward
  seam-1 at x=24; static M0 control blob at (0,24) in patch A.
DIR=in : traveler starts in patch A at (0,48) kicked 0deg (+x) toward seam-1
  — M0 world cannot travel, so this probes A-side entry: seed decays to a
  static blob or dies; the interesting variant is seeding ON the outer ramp.
  We seed at x=8 lu (rho_B=0.018 at w=4) — expect static blob (A~3 world);
  logs its fate + any seam attraction.
T=2000, rec 2.5. Checklist scoring {penetrate, rebound, pin, oscillate,
slide-along, one-way-block, refraction, seam-state} from the track.
Pre-run prediction: blend path is a straight line (tau, Dv): (3,1)->(5.8,
0.6897). At the seam mid rho=0.5: tau_eff=4.40, Dv_eff=0.845, A_eff=3.72 —
deep below the traveling onset (tau_c=5.748 on the A=4 family; M1 needs
tau>4.78 even at Dv=0.65) => traveler CANNOT pass mid-seam: prediction =
stall/pin or rebound; full crossing/refraction impossible. Logged pre-run.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worlds as WD
import patch_lib as P
G = P.G

w_lu = float(sys.argv[1])
dire = sys.argv[2] if len(sys.argv) > 2 else "out"
g, pm, rho = WD.pair_M0_M4(5.8, w_lu)
F = P.state_vacuum_map(g, pm, WD.N)
if dire == "out":
    F = WD.seed_m0(F, g, 0.0, 24.0)                 # control static, patch A
    F = WD.seed_m4(F, 48.0, 48.0, kick=(180.0, 0.5))
    x_start = 48.0
elif dire == "in":
    F = WD.seed_m4(F, 8.0, 48.0, kick=(0.0, 0.5))   # A-side entry probe
    x_start = 8.0
else:  # oblique: 45-deg incidence onto seam-1 (refraction/slide-along probe)
    F = WD.seed_m4(F, 48.0, 36.0, kick=(135.0, 0.5))
    x_start = 48.0
T = 2000.0
snap_t = (200.0, 400.0, 700.0, 1000.0, 1500.0, 2000.0)
r = P.run_patched(g, pm, F=F, L=WD.LLU, dx=WD.DX, T=T, rec_tu=2.5,
                  snap_times=snap_t, kymo_rows={0: 96}, save_fields=True)
pos = WD.pos_lu(r, 0)
tt = r["t"]
nb = pos.shape[1]
# traveler = blob whose initial x is nearest x_start
x0s = [(abs(pos[0, b, 1] - x_start), b) for b in range(nb) if not np.isnan(pos[0, b, 1])]
btr = min(x0s)[1] if x0s else -1
trav = pos[:, btr, :] if btr >= 0 else None
alive = ~np.isnan(trav[:, 1]) if trav is not None else np.array([False])
xw = trav[alive, 1] % 96.0
yw = trav[alive, 0] % 96.0
t_alive = tt[alive]
xmin, xend = (float(np.min(xw)), float(xw[-1])) if len(xw) else (-1, -1)
ymove = float(np.abs(trav[alive, 0] - trav[0, 0]).max()) if len(xw) else -1
# static control drift (dir=out only)
stat_drift = -1.0
if dire == "out" and nb > 1:
    bst = [b for b in range(nb) if b != btr and not np.isnan(pos[0, b, 1])]
    if bst:
        b = bst[0]
        m = ~np.isnan(pos[:, b, 1])
        stat_drift = float(np.hypot(pos[m, b, 0][-1] - pos[m, b, 0][0],
                                    pos[m, b, 1][-1] - pos[m, b, 1][0]))
np.savez_compressed(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "data", f"p2_w{w_lu:g}_{dire}.npz"),
                    t=tt, pos=pos, ncomp=r["ncomp0"],
                    kymo=r["kymo"][0].astype(np.float32),
                    rho_mid=rho[96].astype(np.float32),
                    snaps=np.array([r["snaps"][t][0] for t in snap_t if t in r["snaps"]],
                                   dtype=np.float32),
                    snap_t=[t for t in snap_t if t in r["snaps"]])
print(f"w={w_lu} {dire}: ncomp_end={int(r['ncomp0'][-1])} xmin={xmin:.2f} "
      f"xend={xend:.2f} ymove={ymove:.2f} static_drift={stat_drift:.2f} "
      f"alive_to_t={float(t_alive[-1]) if len(t_alive) else -1}")
P.log(dict(test="P2_traveler_at_seam", w_lu=w_lu, direction=dire, tau_B=5.8, T=T,
           seam1_lu=24.0, x_start_lu=x_start,
           tau_eff_seam=4.40, tau_eff_start=(3.0 + WD.rhoB_at(x_start, w_lu) * 2.8),
           pred="stall/pin or rebound (tau_eff(seam)=4.40, A_eff=3.72 — deep sub-onset)",
           ncomp_final=int(r["ncomp0"][-1]), trav_xmin_lu=xmin, trav_xend_lu=xend,
           trav_ymove_lu=ymove, static_ctrl_drift_lu=stat_drift,
           t_last_alive=float(t_alive[-1]) if len(t_alive) else -1.0,
           status=r["status"], npz=f"data/p2_w{w_lu:g}_{dire}.npz"))
print("logged")
