"""c61: mean |theta| of the labelled vortices (distance of each vortex's trait from the ancestor) per 2000 t. python meanabs.py a.json ..."""
import sys, json, numpy as np
for p in sys.argv[1:]:
    d = json.load(open(p)); T = np.array([t for t, _ in d['traits_by_frame']])
    A = np.array([np.linalg.norm(np.array(x).reshape(-1, 3), axis=1).mean() if len(x) else np.nan for _, x in d['traits_by_frame']])
    print(p, [round(float(np.nanmean(A[(T >= a) & (T < a + 2000)])), 2) for a in range(0, int(T[-1]), 2000)])
