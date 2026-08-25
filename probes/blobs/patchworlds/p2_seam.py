"""p2_seam.py W_PX — P2 ALIGNED-VACUUM PATCH: M0 (A) | M4 tau=5.8 (B band).

Static M0 blob at (x=0, y=24) lu in patch A; A4-stamp traveler at band center
(x=48, y=48) lu kicked 180 deg (-x) toward seam-1 (x=24 lu = 48 px).
T=2000, rec 2.5. Saves npz (pos, kymo y=48lu, snaps) + results row.
Predictions logged pre-run: static stays static; traveler travels (w=4,12);
w=24: rho overlap -> tau_eff(center)=5.699 < 5.748 single onset -> may stall.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worlds as WD
import patch_lib as P
G = P.G

w_px = float(sys.argv[1])
tau_B = 5.8
gA, gB = WD.gM0(), WD.gM4(tau_B)
g, pm, rho = WD.build_patch(gA, gB, w_px)
N, dx = WD.N, WD.DX
F = P.state_vacuum_map(g, pm, N)
F = WD.seed_m0(F, g, 0.0, 24.0)
F = WD.seed_m4(F, 48.0, 48.0, kick=(180.0, 0.25))
T = 2000.0
snap_t = (400.0, 700.0, 900.0, 1100.0, 1400.0, 2000.0)
r = P.run_patched(g, pm, F=F, L=WD.LLU, dx=dx, T=T, rec_tu=2.5,
                  snap_times=snap_t, kymo_rows={0: 96}, save_fields=True)
pos = WD.pos_px(r, 0)
np.savez_compressed(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "data", f"p2_w{w_px:g}.npz"),
                    t=r["t"], pos=pos, ncomp=r["ncomp0"],
                    area=np.array([a + [np.nan]*(pos.shape[1]-len(a)) for a in r["area0"]]),
                    kymo=r["kymo"][0].astype(np.float32),
                    rho_mid=rho[96].astype(np.float32),
                    snaps=np.array([r["snaps"][t][0] for t in snap_t if t in r["snaps"]], dtype=np.float32),
                    snap_t=[t for t in snap_t if t in r["snaps"]])

# quick classification: track blobs by x at each record (raw, unwrapped)
nc = r["ncomp0"]
tt = r["t"]
def near(x, ref, tol=30.0):
    return abs(((x - ref + 96) % 192) - 96) < tol   # px, periodic-ish on 192
# static blob: initial x ~ 0/192; traveler: initial x ~ 96
stat_x, trav_x, trav_y = [], [], []
for k in range(pos.shape[0]):
    for b in range(pos.shape[1]):
        if np.isnan(pos[k, b, 1]):
            continue
        x0 = pos[k, b, 1] % 192
        if near(x0, 0.0):
            stat_x.append((tt[k], pos[k, b, 1], pos[k, b, 0]))
        elif pos[k, b, 1] < 150:
            trav_x.append((tt[k], pos[k, b, 1]))
            trav_y.append(pos[k, b, 0])
stat_x = np.array(stat_x); trav = np.array(trav_x)
stat_drift = float(np.hypot(stat_x[-1,1]-stat_x[0,1], stat_x[-1,2]-stat_x[0,2])) if len(stat_x) else -1
xmin = float(np.nanmin(trav[:,1])) if len(trav) else -1
x_end = float(trav[-1,1]) if len(trav) else -1
t_last = float(trav[-1,0]) if len(trav) else -1
print(f"w={w_px}: ncomp final {nc[-1]}, static drift {stat_drift:.2f}px, "
      f"traveler xmin {xmin:.1f}px end {x_end:.1f}px at t={t_last}")
P.log(dict(test="P2_traveler_at_seam", w_px=w_px, tau_B=tau_B, T=T,
           geometry="A=M0 outside band px[48,144); traveler at 96px kicked -x; seam-1 at 48px; static M0 blob at (0,48)px",
           ncomp_final=int(nc[-1]), static_drift_px=stat_drift,
           traveler_xmin_px=xmin, traveler_x_end_px=x_end, t_last_seen=t_last,
           npz=f"data/p2_w{w_px:g}.npz", status=r["status"]))
print("logged")
