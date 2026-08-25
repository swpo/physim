"""p0_chord.py — P0 HOMOTOPY PRE-FLIGHT (mandatory template, litreview R2).

Straight-line genome chord M0 -> M4(5.8): tau 3->5.8, Dv 1->0.6897 (all else
equal; aligned vacuum). Per s in 21 points:
  (a) vacuum dispersion max_k Re lambda(k) (analytic 3x3 Jacobian),
  (b) 0-D funnel: du/dt at u0+eps grid — basin edge vs upper root,
  (c) 2-D poke persistence at s in {0.25, 0.5, 0.75}: L=48 lu, T=300,
      dressed poke (l0 A1: tau=5.7-class worlds die on bare pokes).
Verdict gate: no s with (a) > 0 or (c) blowup/cancer (ncomp>6).
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worlds as WD
import patch_lib as P
G = P.G

gA, gB = G.ref_M0(), G.ref_M4(5.8)
u0 = gA["acts"][0]["u0"]
rows = []
ks = np.linspace(0, 4, 400)
for s in np.linspace(0, 1, 21):
    g = P.blend_scalar(gA, gB, s)
    a = g["acts"][0]
    tau, Dv = g["chans"][0]["tau"], g["chans"][0]["D"]
    fu = a["lam"] - 3 * a["u0"] ** 2
    mx = -1e9
    for k in ks:
        J = np.array([[fu - a["Du"] * k * k, -g["K"][0][0], -g["K"][0][1]],
                      [1 / tau, -1 / tau - Dv * k * k, 0.0],
                      [1 / 0.7, 0.0, -1 / 0.7 - 20.0 * k * k]])
        mx = max(mx, float(np.max(np.linalg.eigvals(J).real)))
    roots = G.cubic_roots(a["lam"], a["k1"])
    rows.append(dict(s=round(float(s), 3), tau=round(tau, 4), Dv=round(Dv, 4),
                     A=round(tau * Dv, 4), disp_max=round(mx, 5),
                     n_roots=len(roots)))
disp_ok = all(r["disp_max"] < 0 for r in rows)
print("dispersion stable along chord:", disp_ok,
      "| A range", min(r["A"] for r in rows), max(r["A"] for r in rows))

pokes = {}
for s in (0.25, 0.5, 0.75):
    g = P.blend_scalar(gA, gB, s)
    F = G.state_vacuum(g, 96)
    F = P.dressed_poke(F, g, 0, 24.0, 24.0, 0.5, kick_px=0.5)
    r = G.run_genome(g, F=F, L=48.0, dx=0.5, T=300.0, rec_tu=10.0,
                     stop_all_dead=False, save_fields=False)
    nc = int(r["ncomp0"][-1])
    pokes[s] = dict(status=r["status"], ncomp_final=nc,
                    area_final=(r["area0"][-1] or [0]))
    print(f"s={s}: {r['status']} ncomp={nc} area={pokes[s]['area_final']}")
bad = [s for s, v in pokes.items() if v["status"] != "ok" or v["ncomp_final"] > 6]
verdict = "PASS" if disp_ok and not bad else "FAIL"
print("P0 verdict:", verdict)
P.log(dict(test="P0_homotopy_chord", pair="M0->M4(5.8)", verdict=verdict,
           dispersion_stable=disp_ok, chord=rows[::4],
           poke_2d={str(k): v for k, v in pokes.items()},
           note="mandatory pre-flight template (litreview R2); chord A=tau*Dv stays in [3, 4.005]"))
print("logged")
