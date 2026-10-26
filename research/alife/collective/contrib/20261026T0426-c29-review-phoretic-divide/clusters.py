"""clusters.py: cluster particles (link if closer than rl), track clusters frame to frame by shared particles,
report cluster speed (body lengths travelled), size, and coat structure (B fraction in rim vs core)."""
import sys, numpy as np
from scipy.spatial import cKDTree
from scipy.sparse.csgraph import connected_components
from scipy.sparse import coo_matrix

def clusters(x, L, rl=1.5, nmin=12):
    t = cKDTree(x, boxsize=L); p = t.query_pairs(rl, output_type="ndarray"); n = len(x)
    g = coo_matrix((np.ones(len(p)), (p[:, 0], p[:, 1])), shape=(n, n))
    nc, lab = connected_components(g, directed=False); cnt = np.bincount(lab)
    big = np.nonzero(cnt >= nmin)[0]; m = {c: k for k, c in enumerate(big)}
    return np.array([m.get(l, -1) for l in lab]), len(big)

def pcentroid(x, L):
    th = x / L * 2 * np.pi; return (np.arctan2(-np.sin(th).mean(0), -np.cos(th).mean(0)) + np.pi) / (2 * np.pi) * L

def analyse(npz, rl=1.5, nmin=12, t0frac=0.4):
    d = np.load(npz); X, SP, L, dt = d["x"], d["sp"], float(d["L"]), float(d["dt"])
    if SP.ndim == 1: SP = np.repeat(SP[None], len(X), 0)
    nab = [(SP[f] == 0).sum() for f in (0, -1)], [(SP[f] == 1).sum() for f in (0, -1)]; F = len(X)
    f0 = int(F * t0frac); prev = None; tracks = {}; nid = 0; rimcore = []; out = []
    for f in range(f0, F):
        sp = SP[f]; kp = sp != 2; lab = -np.ones(len(sp), int); lab[kp], nc = clusters(X[f][kp], L, rl, nmin); cur = {}
        for k in range(nc):
            idx = np.nonzero(lab == k)[0]; c = pcentroid(X[f][idx], L)
            # track: match to the previous cluster holding most of these particles
            tid = None
            if prev is not None:
                pl = prev[idx]; pl = pl[pl >= 0]
                if len(pl):
                    best = np.bincount(pl).argmax()
                    if (pl == best).mean() > 0.5 and best in prevmap: tid = prevmap[best]
            if tid is None or tid in cur.values(): tid = nid; nid += 1
            cur[k] = tid; r = np.sqrt((((X[f][idx] - c + L / 2) % L - L / 2) ** 2).sum(1)); R = np.sqrt(len(idx) / np.pi) * 0.9
            tracks.setdefault(tid, []).append((f, c, len(idx), (sp[idx] == 1).mean()))
            if len(idx) >= 30:
                rim = r > 0.6 * r.max(); rimcore.append(((sp[idx][rim] == 1).mean(), (sp[idx][~rim] == 1).mean()))
        prev = lab; prevmap = cur
    for tid, tr in tracks.items():
        if len(tr) < 20: continue
        c = np.array([q[1] for q in tr]); dc = (np.diff(c, axis=0) + L / 2) % L - L / 2; path = np.abs(dc).sum()
        net = np.sqrt((dc.sum(0) ** 2).sum()); n = np.median([q[2] for q in tr]); diam = 2 * np.sqrt(n / np.pi) * 0.9
        out.append((tid, len(tr) * dt, n, np.median([q[3] for q in tr]), net / diam, np.sqrt((dc ** 2).sum(1)).sum() / diam))
    return out, np.array(rimcore)

if __name__ == "__main__":
    for p in sys.argv[1:]:
        out, rc = analyse(p); out.sort(key=lambda q: -q[4])
        print(p.split("/")[-1], "tracks>=20fr:", len(out), " B rim/core frac (median):", np.round(np.median(rc, 0), 2) if len(rc) else None)
        comp = [q for q in out if 0.1 <= q[3] <= 0.6 and q[1] >= 50]
        print("  composites (fB 0.1-0.6, life>=50):", len(comp), " moving >=3 BL:", sum(q[4] >= 3 for q in comp))
        for q in out[:5]: print("  id %d life %.0f n %.0f fB %.2f net %.1f BL path %.1f BL" % q)
