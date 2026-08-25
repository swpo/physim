"""p_controls.py — small controls that pin interpretations.

C1 pure-B blob check (P3): uniform M0-wiring world with k1_orig=-0.8 — poke,
   T=600. If dead -> P3 x0=40 death is a WORLD property (endpoint fails blob
   existence), not a seam effect => P0 pre-flight MUST include endpoints.
C2 chord check for the vacuum pair M0 -> M0k1(-0.8): dispersion at 21 s +
   2-D poke at s in {0.5, 1.0} (s=0 known good).
C3 pure-M0 pair at sep 15.4 (P5 A-side bond well?): two pokes, T=2500.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worlds as WD
import patch_lib as P
G = P.G

gA, gB = G.ref_M0(), P.ref_M0_k1(-0.8)

# C1
F = G.state_vacuum(gB, 96)
F = G.poke(F, gB, 0, 24.0, 24.0, 2.0, 3.0, 0.5)
r = G.run_genome(gB, F=F, L=48.0, dx=0.5, T=600.0, rec_tu=10.0, save_fields=False)
c1 = dict(status=r["status"], ncomp_final=int(r["ncomp0"][-1]),
          ncomp_max=int(r["ncomp0"].max()),
          area_final=(r["area0"][-1] or [0.0]))
print("C1 pure-B (k1=-0.8) poke:", c1)

# C2
rows = []
ks = np.linspace(0, 4, 300)
for s in np.linspace(0, 1, 21):
    g = P.blend_scalar(gA, gB, s)
    a = g["acts"][0]
    fu = a["lam"] - 3 * a["u0"] ** 2
    mx = -1e9
    for k in ks:
        J = np.array([[fu - a["Du"] * k * k, -g["K"][0][0], -g["K"][0][1]],
                      [1 / 3.0, -1 / 3.0 - 1.0 * k * k, 0.0],
                      [1 / 0.7, 0.0, -1 / 0.7 - 20.0 * k * k]])
        mx = max(mx, float(np.max(np.linalg.eigvals(J).real)))
    rows.append((round(float(s), 2), round(mx, 5)))
disp_ok = all(m < 0 for _, m in rows)
pokes = {}
for s in (0.5, 1.0):
    g = P.blend_scalar(gA, gB, s)
    F = G.state_vacuum(g, 96)
    F = G.poke(F, g, 0, 24.0, 24.0, 2.0, 3.0, 0.5)
    r = G.run_genome(g, F=F, L=48.0, dx=0.5, T=600.0, rec_tu=10.0, save_fields=False)
    pokes[s] = dict(status=r["status"], ncomp_final=int(r["ncomp0"][-1]))
    print(f"C2 chord s={s}:", pokes[s])
print("C2 dispersion ok:", disp_ok)

# C3
g = gA
F = G.state_vacuum(g, WD.N)
F = G.poke(F, g, 0, 16.3, 48.0, 2.0, 3.0, 0.5)
F = G.poke(F, g, 0, 31.7, 48.0, 2.0, 3.0, 0.5)
r = G.run_genome(g, F=F, L=96.0, dx=0.5, T=2500.0, rec_tu=5.0, save_fields=False)
pos = WD.pos_lu(r, 0)
sep = np.hypot(pos[:, 0, 0] - pos[:, 1, 0], pos[:, 0, 1] - pos[:, 1, 1])       if pos.shape[1] >= 2 else np.array([np.nan])
c3 = dict(ncomp_final=int(r["ncomp0"][-1]),
          sep0=float(sep[0]), sep_final=float(sep[-1]),
          sep_t1000=float(sep[np.argmin(np.abs(r["t"] - 1000))]))
print("C3 pure-M0 pair sep15.4:", c3)

P.log(dict(test="P_controls", C1_pureB_k1m08_poke=c1,
           C2_chord_dispersion_ok=disp_ok, C2_chord=rows[::5],
           C2_pokes={str(k): v for k, v in pokes.items()}, C3_pureM0_pair=c3))
print("logged")
