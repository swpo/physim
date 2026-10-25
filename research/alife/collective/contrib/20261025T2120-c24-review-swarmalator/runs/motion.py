"""Follow swarmalator flocks by membership overlap (continuation = one parent taking >= 50% of the child
and the child taking >= 50% of the parent) and measure net and path displacement in flock radii; also check
whether split daughters re-merge within 20 t (split undone) and whether a split was preceded by a merge
within 20 t (collision undone)."""
import sys, numpy as np, ctrack
d = np.load(sys.argv[1]); X, TH = d["X"], d["TH"]; L = 60.0
labs = [ctrack.clusters(x, L) for x in X]
def cen(x):
    a = 2 * np.pi * x / L; return (np.angle(np.exp(1j * a).mean(0)) % (2 * np.pi)) * L / (2 * np.pi)
tracks = {}; cur = {}; nid = 0
for t in range(len(X)):
    lab = labs[t]; new = {}
    for k in [k for k in np.unique(lab) if k >= 0]:
        m = lab == k; best = None
        if t > 0:
            pl = labs[t - 1][m]; vals, cnt = np.unique(pl[pl >= 0], return_counts=True)
            for v, c in zip(vals, cnt):
                if c >= 0.5 * m.sum() and c >= 0.5 * (labs[t - 1] == v).sum() and v in cur: best = cur[v]
        if best is None: best = nid; nid += 1; tracks[best] = []
        new[k] = best
        x = X[t][m]; c = cen(x); r = np.sqrt(((((x - c) + L / 2) % L - L / 2) ** 2).sum(1).mean())
        tracks[best].append((t, c, r, m.sum(), abs(np.exp(1j * TH[t][m]).mean())))
    cur = new
res = []
for k, v in tracks.items():
    if len(v) < 20: continue
    c = np.array([q[1] for q in v]); dc = np.diff(c, axis=0); dc = (dc + L / 2) % L - L / 2
    path = np.sqrt((dc ** 2).sum(1)).sum(); net = np.sqrt((dc.sum(0) ** 2).sum()); R = np.mean([q[2] for q in v])
    res.append((k, len(v), int(np.mean([q[3] for q in v])), round(R, 2), round(net / (2 * R), 1), round(path / (2 * R), 1), round(np.mean([q[4] for q in v]), 2)))
res.sort(key=lambda q: -q[5])
print("tracks >= 20 t:", len(res), "; top by path (id, life, size, radius, net/diam, path/diam, polar):")
for q in res[:8]: print(q)
print("median path/diam over tracks >= 20 t: %.1f, median net/diam %.1f" % (np.median([q[5] for q in res]), np.median([q[4] for q in res])))
