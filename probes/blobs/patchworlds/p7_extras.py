"""p7_extras.py MODE — final discriminating controls.

taupatch: P2 crossing on a WIRING-ONLY seam (litreview-recommended mode):
  Dv=0.6897 GLOBAL, tau blended 4.35 (A=3.0 static) | 5.8 (A=4, traveling).
  Traveler at band center kicked -x at seam-1. If it crosses & parks with NO
  residual creep -> the P2/P6 creep is the Dv-gradient force, and the
  all-D-global patch mode gives clean crossings.
pair20:  uniform M4(4.0), pair at sep 20 (P4-close geometry control):
  does a same-world pair at 20 lu attract to d* or repel?
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worlds as WD
import patch_lib as P
G = P.G

mode = sys.argv[1]
if mode == "taupatch":
    gB = G.ref_M4(5.8)                    # tau=5.8, Dv=0.6897
    gA = G.ref_M4(5.8)
    gA["chans"][0]["tau"] = 4.35          # A = 3.0, same Dv
    gA["id"] = "M4fam_tau4.35"
    g, pm, rho = WD.build(gA, gB, 12.0)
    F = P.state_vacuum_map(g, pm, WD.N)
    F = WD.seed_m4(F, 48.0, 48.0, kick=(180.0, 0.5))
    r = P.run_patched(g, pm, F=F, L=WD.LLU, dx=WD.DX, T=2000.0, rec_tu=2.5,
                      kymo_rows={0: 96}, snap_times=(2000.0,), save_fields=True)
    pos = WD.pos_lu(r, 0)
    t = r["t"]
    x = pos[:, 0, 1]
    m = ~np.isnan(x)
    x, t = x[m], t[m]
    segs = {}
    for t0, t1 in ((900, 1200), (1200, 1600), (1600, 2000)):
        s = (t >= t0) & (t <= t1)
        segs[f"{t0}-{t1}"] = float(np.polyfit(t[s], x[s], 1)[0])
    ic = np.argmax(x < 24.0) if (x < 24).any() else -1
    print(f"taupatch: x {x[0]:.1f}->{x[-1]:.2f} cross_t={t[ic] if ic>=0 else -1} "
          f"v_late={segs} ncomp={int(r['ncomp0'][-1])}")
    np.savez_compressed(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "data", "p7_taupatch.npz"), t=t, x=x,
                        kymo=r["kymo"][0].astype(np.float32), ncomp=r["ncomp0"])
    P.log(dict(test="P7_taupatch_crossing", w_lu=12.0,
               pair="M4fam tau4.35 (A=3, Dv=.6897) | M4(5.8) — Dv GLOBAL",
               x0=float(x[0]), x_end=float(x[-1]),
               t_cross=float(t[ic]) if ic >= 0 else -1.0,
               v_late_segs=segs, ncomp_final=int(r["ncomp0"][-1]),
               status=r["status"], npz="data/p7_taupatch.npz"))
else:
    g = G.ref_M4(4.0)
    F = G.state_vacuum(g, WD.N)
    F = WD.seed_m4(F, 26.0, 48.0)
    F = WD.seed_m4(F, 46.0, 48.0)
    r = P.run_patched(g, {}, F=F, L=WD.LLU, dx=WD.DX, T=2000.0, rec_tu=5.0,
                      save_fields=False)
    pos = WD.pos_lu(r, 0)
    sep = np.hypot(pos[:, 0, 0] - pos[:, 1, 0], pos[:, 0, 1] - pos[:, 1, 1])
    t = r["t"]
    print(f"pair20 uniform M4(4): sep {sep[0]:.2f} -> {sep[-1]:.2f} "
          f"(t1000: {sep[np.argmin(np.abs(t-1000))]:.2f}) ncomp {int(r['ncomp0'][-1])}")
    P.log(dict(test="P7_pair20_uniformM4", tau=4.0, sep0=float(sep[0]),
               sep_t1000=float(sep[np.argmin(np.abs(t - 1000))]),
               sep_final=float(sep[-1]), ncomp_final=int(r["ncomp0"][-1]),
               status=r["status"]))
print("logged")
