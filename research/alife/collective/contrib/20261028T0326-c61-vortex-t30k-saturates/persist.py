"""c61: directional persistence of the population's trait centroid: cosine between successive W-t centroid displacements."""
import sys, json, numpy as np
def cents(p, W):
    d = json.load(open(p)); T = np.array([t for t, _ in d['traits_by_frame']]); C = np.array([np.mean(np.array(x).reshape(-1, 3), 0) if len(x) else [np.nan]*3 for _, x in d['traits_by_frame']])
    out = []
    for a in np.arange(T[0], T[-1] - W / 2, W):
        m = (T >= a) & (T < a + W); out.append(np.nanmean(C[m], 0))
    return np.array(out)
W = float(sys.argv[1])
for arg in sys.argv[2:]:
    lab, p = arg.split('='); c = cents(p, W); d = np.diff(c, axis=0)
    cos = [float(np.dot(d[i], d[i+1]) / (np.linalg.norm(d[i]) * np.linalg.norm(d[i+1]) + 1e-12)) for i in range(len(d) - 1)]
    print(f'{lab}: mean cos {np.mean(cos):+.2f}  steps {np.round(np.linalg.norm(d,axis=1),2).tolist()}')
