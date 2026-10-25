"""c13: per-body census from a labkit frames.npz of the FCH chemoton (render channels u+1, P, K).
Bodies = 8-connected components of u+1 > 0.6 with >= 12 px. For each: amphiphile mass, K on the body (bilayer
pixels), K in the enclosed lumen (holes), K in a 2-5 px exterior band. Prints a table at a few frames and the
total amphiphile in K-carrying (body K mean > 0.05) vs K-free bodies."""
import sys, json, numpy as np
from scipy import ndimage
d = np.load(sys.argv[1]); R = d["render"]; f = d["render_f"]; dtf = 3.0
st8 = np.ones((3, 3), bool)
out = []
for i in range(len(f)):
    u, K = R[i, 0], R[i, 2]
    lab, n = ndimage.label(u > 0.6, structure=st8)
    rows = []
    for j in range(1, n + 1):
        b = lab == j
        if b.sum() < 12: continue
        filled = ndimage.binary_fill_holes(b); lumen = filled & ~b
        ext = ndimage.binary_dilation(filled, iterations=5) & ~ndimage.binary_dilation(filled, iterations=2)
        rows.append(dict(px=int(b.sum()), u=round(float(u[b].sum()), 1), Kb=round(float(K[b].mean()), 3),
                         Kl=round(float(K[lumen].mean()), 3) if lumen.sum() > 3 else None, Ko=round(float(K[ext].mean()), 3),
                         lumen=int(lumen.sum())))
    kc = [r for r in rows if r["Kb"] > 0.05]; kf = [r for r in rows if r["Kb"] <= 0.05]
    out.append(dict(t=round(float(f[i]) * dtf), n=len(rows), nK=len(kc), uK=round(sum(r["u"] for r in kc)), uFree=round(sum(r["u"] for r in kf)), rows=rows))
for o in out[::max(1, len(out) // 10)] + [out[-1]]:
    print(o["t"], "bodies", o["n"], "K-carrying", o["nK"], "u in K-bodies", o["uK"], "u in K-free", o["uFree"])
    for r in o["rows"]: print("   ", r)
