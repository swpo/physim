"""c57: per-kind body counts and areas from a labkit frames.npz of the cips-gene world (channels e,p,F,s,g1,g2);
bodies e>0.5, >=10 px, periodic wrap joined; kind = g2 if mean g2 > mean g1. usage: kinds.py pack_dir out.json"""
import sys, json, numpy as np
from scipy import ndimage
R = np.load(sys.argv[1] + '/frames.npz')['render'].astype(np.float32); out = []
for f, fr in enumerate(R):
    e, g1, g2 = fr[0], fr[4], fr[5]
    lab, n = ndimage.label(e > 0.5)
    for a, b in [(lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])]:
        for i, j in zip(a, b):
            if i and j and i != j: lab[lab == j] = i
    k1, k2, a1, a2 = 0, 0, [], []
    for j in np.unique(lab):
        if not j: continue
        m = lab == j; A = int(m.sum())
        if A < 10: continue
        if g2[m].mean() > g1[m].mean(): k2 += 1; a2.append(A)
        else: k1 += 1; a1.append(A)
    out.append({"t": f * 100, "g1_n": k1, "g2_n": k2, "g1_area_med": float(np.median(a1)) if a1 else 0, "g2_area_med": float(np.median(a2)) if a2 else 0, "g2_area_max": max(a2) if a2 else 0})
json.dump(out, open(sys.argv[2], 'w'))
for r in out[15::10] + [out[-1]]: print(r)
