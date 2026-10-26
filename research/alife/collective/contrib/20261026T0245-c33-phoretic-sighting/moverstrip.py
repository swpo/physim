"""moverstrip.py <npz> <out.png> [rank]: follow the rank-th most travelled cluster track and draw
a zoomed strip of 8 frames around it (A red, B blue) plus the track over the full domain."""
import sys, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, __file__.rsplit("/", 1)[0]); from clusters import clusters, pcentroid
npz, out = sys.argv[1], sys.argv[2]; rank = int(sys.argv[3]) if len(sys.argv) > 3 else 0
d = np.load(npz); X, sp, L, dt = d["x"], d["sp"], float(d["L"]), float(d["dt"]); F = len(X)
# track with the same rule as clusters.analyse, keeping member lists
prev = None; tracks = {}; nid = 0; prevmap = {}
for f in range(int(0.2 * F), F):
    lab, nc = clusters(X[f], L); cur = {}
    for k in range(nc):
        idx = np.nonzero(lab == k)[0]; tid = None
        if prev is not None:
            pl = prev[idx]; pl = pl[pl >= 0]
            if len(pl):
                b = np.bincount(pl).argmax()
                if (pl == b).mean() > 0.5 and b in prevmap: tid = prevmap[b]
        if tid is None or tid in cur.values(): tid = nid; nid += 1
        cur[k] = tid; tracks.setdefault(tid, []).append((f, pcentroid(X[f][idx], L), idx))
    prev = lab; prevmap = cur
def net(tr):
    c = np.array([q[1] for q in tr]); dc = (np.diff(c, axis=0) + L / 2) % L - L / 2
    n = np.median([len(q[2]) for q in tr]); return np.sqrt((dc.sum(0) ** 2).sum()) / (1.8 * np.sqrt(n / np.pi))
good = sorted([t for t in tracks.values() if len(t) >= 40], key=net, reverse=True); tr = good[rank]
fig = plt.figure(figsize=(20, 3.2)); fr = np.linspace(0, len(tr) - 1, 8).astype(int)
for j, q in enumerate(fr):
    f, c, idx = tr[q]; ax = fig.add_subplot(1, 9, j + 1); x = (X[f] - c + L / 2) % L - L / 2
    for k, col in ((0, "red"), (1, "blue")):
        m = (sp == k) & (np.abs(x).max(1) < 14); ax.scatter(x[m, 0], x[m, 1], s=4, c=col)
    ax.set_xlim(-14, 14); ax.set_ylim(-14, 14); ax.set_aspect(1); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"t={f * dt:.0f} n={len(idx)}", fontsize=8)
ax = fig.add_subplot(1, 9, 9); c = np.array([q[1] for q in tr]); ax.scatter(c[:, 0], c[:, 1], s=1, c=np.arange(len(c)))
ax.set_xlim(0, L); ax.set_ylim(0, L); ax.set_aspect(1); ax.set_title(f"track: net {net(tr):.1f} BL", fontsize=8)
fig.tight_layout(); fig.savefig(out, dpi=80); print(out, "net BL", round(net(tr), 1), "frames", len(tr))
