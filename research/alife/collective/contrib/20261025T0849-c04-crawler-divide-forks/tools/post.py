"""Mean body speed and split count after frame F0 from a labkit pack (frames.npz, metrics.json)."""
import sys, json, numpy as np
sys.path.insert(0, ".")
from crawler import plabel
d, F0 = sys.argv[1], int(sys.argv[2]); dtf = 2.5
M = np.load(d + "/frames.npz")["matter"]; H = M.shape[1]
def cents(m):
    lab, n = plabel(m > 0.25); out = []
    for k in range(1, n + 1):
        y, x = np.nonzero(lab == k)
        if len(y) < 30: continue
        out.append((np.angle(np.exp(2j*np.pi*y/H).mean())*H/2/np.pi % H, np.angle(np.exp(2j*np.pi*x/H).mean())*H/2/np.pi % H))
    return np.array(out)
sp = []
for f in range(F0, M.shape[0] - 1, 2):
    a, b = cents(M[f]), cents(M[f + 2])
    if len(a) == 0 or len(b) == 0: continue
    for c in a:
        dd = (b - c + H/2) % H - H/2; r = np.hypot(dd[:, 0], dd[:, 1]).min()
        if r < 15: sp.append(r * 0.5 / (2 * dtf))  # px -> length units (dx 0.5), per time
m = json.load(open(d + "/metrics.json"))
ns = sum(1 for s in m["persistent_splits"] if s["frame"] >= F0)
print(d, "mean speed after frame", F0, "= %.3f" % np.mean(sp), "| 90th pct %.3f" % np.percentile(sp, 90), "| persistent splits after:", ns, "| bodies at end:", len(cents(M[-1])))
