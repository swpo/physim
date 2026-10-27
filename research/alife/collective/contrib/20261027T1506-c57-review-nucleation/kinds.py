"""c57: per-kind body counts and areas from a labkit frames.npz of the cips-gene world (channels e,p,F,s,g1,g2);
bodies e>0.5, >=10 px, periodic wrap joined; kind = the larger mean label if it is >= 0.5, else none (as c48 ana.py). usage: kinds.py pack_dir out.json"""
import sys, json, numpy as np
from scipy import ndimage
Fz = np.load(sys.argv[1] + '/frames.npz'); R = Fz['render'].astype(np.float32); RF = Fz['render_f']; out = []
for f, fr in enumerate(R):
    e, g1, g2 = fr[0], fr[4], fr[5]
    lab, n = ndimage.label(e > 0.5)
    for a, b in [(lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])]:
        for i, j in zip(a, b):
            if i and j and i != j: lab[lab == j] = i
    k1, k2, k0, a1, a2 = 0, 0, 0, [], []
    for j in np.unique(lab):
        if not j: continue
        m = lab == j; A = int(m.sum())
        if A < 10: continue
        m1, m2 = g1[m].mean(), g2[m].mean()
        if m2 >= 0.5 and m2 > m1: k2 += 1; a2.append(A)
        elif m1 >= 0.5 and m1 > m2: k1 += 1; a1.append(A)
        else: k0 += 1
    out.append({"t": int(RF[f]) * 100, "g1_n": k1, "g2_n": k2, "none_n": k0, "g1_area_med": float(np.median(a1)) if a1 else 0, "g2_area_med": float(np.median(a2)) if a2 else 0, "g2_area_max": max(a2) if a2 else 0})
json.dump(out, open(sys.argv[2], 'w'))
for r in out[20::20] + [out[-1]]: print(r['t'], r['g1_n'], r['g2_n'], r['none_n'])
