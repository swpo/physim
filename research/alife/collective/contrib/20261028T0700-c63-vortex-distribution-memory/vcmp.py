"""c63: per-window trait-cloud measures for trait3c.py JSONs ('traits_by_frame', every 30 t), in the units of c61's vnov.py.
Per window of W t (default 1000), up to Tmax: n (mean labelled vortices), R (RMS distance of traits from the window's
centroid), D0 (mean distance of a vortex's trait from the ancestor 0), far (share of vortex samples farther than THR from
every trait recorded more than 1000 t earlier; THR default 0.4 = one class of c58's dm), hull (max distance from the
ancestor of any trait seen so far). python vcmp.py OUT.json W Tmax THR label=file.json ..."""
import sys, json, numpy as np
from scipy.spatial import cKDTree
out, W, Tm, THR = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
res = {}
for arg in sys.argv[5:]:
    lab, p = arg.split('=')
    d = json.load(open(p)); T = np.array([t for t, _ in d['traits_by_frame']]); X = [np.array(x, float).reshape(-1, 3) for _, x in d['traits_by_frame']]
    rows = []; hull = 0.0
    for w0 in np.arange(W, Tm + 1e-9, W):
        idx = [i for i in range(len(T)) if w0 - W <= T[i] < w0 and len(X[i])]
        if not idx: continue
        Y = np.concatenate([X[i] for i in idx]); c = Y.mean(0)
        past = [X[i] for i in range(len(T)) if T[i] < w0 - W - 1000 and len(X[i])]
        if past:
            tree = cKDTree(np.concatenate(past)); dd, _ = tree.query(Y); far = float((dd > THR).mean())
        else: far = None
        hull = max(hull, float(np.linalg.norm(Y, axis=1).max()))
        rows.append({'t': float(w0), 'n': round(len(Y) / len(idx), 1), 'R': round(float(np.sqrt(((Y - c) ** 2).sum(1).mean())), 3),
                     'D0': round(float(np.linalg.norm(Y, axis=1).mean()), 3), 'far': None if far is None else round(far, 3), 'hull': round(hull, 2)})
    res[lab] = rows
    print(lab); print('  t    ', ' '.join(f"{r['t']:6.0f}" for r in rows))
    for k in ('R', 'D0', 'far', 'hull'): print(f'  {k:5s}', ' '.join('     -' if r[k] is None else f'{r[k]:6.2f}' for r in rows))
json.dump(res, open(out, 'w'), indent=1)
