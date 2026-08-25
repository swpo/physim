"""p2_refspeed.py — uniform M4(5.8) control: same stamp+kick protocol, no patch.
Validates the P2 pre-seam speed (certified late-window c=0.055; what does the
SAME protocol show in the first 250 tu?)."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worlds as WD
import patch_lib as P
G = P.G

g = G.ref_M4(5.8)
F = G.state_vacuum(g, WD.N)
F = WD.seed_m4(F, 48.0, 48.0, kick=(180.0, 0.5))
r = P.run_patched(g, {}, F=F, L=WD.LLU, dx=WD.DX, T=2000.0, rec_tu=2.5,
                  save_fields=False)
pos = WD.pos_lu(r, 0)
t = r["t"]
x = pos[:, 0, 1]
def vwin(t0, t1):
    s = (t >= t0) & (t <= t1)
    return float(np.polyfit(t[s], x[s], 1)[0])
segs = {f"{a}-{b}": round(vwin(a, b), 5) for a, b in
        ((0, 100), (100, 250), (250, 500), (500, 1000), (1000, 2000))}
print("uniform M4(5.8) vx by window:", segs)
print("x: 0->", float(x[0]), " 2000->", float(x[-1]), "ncomp", int(r["ncomp0"][-1]))
P.log(dict(test="P2_refspeed_uniform", tau=5.8, vx_windows=segs,
           x0=float(x[0]), x_end=float(x[-1]), ncomp_final=int(r["ncomp0"][-1]),
           note="same stamp+kick protocol as P2, no patch; certified late c=0.055"))
print("logged")
