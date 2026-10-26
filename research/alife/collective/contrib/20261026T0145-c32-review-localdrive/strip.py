"""c28: strip image of a lineage (parent track and its daughters) from ringtrack.py output and its snapshots.
usage: strip.py tracks.json snap.npz out.png parent_id [ncols]"""
import json, sys, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
d = json.load(open(sys.argv[1])); Z = np.load(sys.argv[2]); out = sys.argv[3]; pid = sys.argv[4]; nc = int(sys.argv[5]) if len(sys.argv) > 5 else 8
T = d["tracks"]; ts = Z["t"]; N = Z["phi"].shape[1]; C = 40
def pos(tr, t):
    P = tr["path"]; tt = np.array([p[0] for p in P]); i = int(np.argmin(abs(tt - t))); return P[i][1], P[i][2], P[i][0]
def ringat(tr, t):
    P = tr["path"]; tt = np.array([p[0] for p in P]); i = int(np.argmin(abs(tt - t))); r = tr["ring"][i]; return r
rows = [(pid, T[pid])] + [(c, T[str(c)]) for c in T[pid]["children"]]
fig, ax = plt.subplots(len(rows), nc, figsize=(1.9 * nc, 2.1 * len(rows)))
for r, (tid, tr) in enumerate(rows):
    sel = ts[(ts >= tr["t0"]) & (ts <= tr["t1"])]
    pick = np.unique(sel[np.linspace(0, len(sel) - 1, nc).astype(int)]) if len(sel) else []
    P0 = tr["path"][0]
    for j, t in enumerate(pick):
        k = int(np.where(ts == t)[0][0]); cy, cx, tp = pos(tr, t)
        sh = (int(N / 2 - cy), int(N / 2 - cx))
        L = np.roll(Z["L"][k].astype(float), sh, (0, 1))[N // 2 - C:N // 2 + C, N // 2 - C:N // 2 + C]
        ph = np.roll(Z["phi"][k].astype(float), sh, (0, 1))[N // 2 - C:N // 2 + C, N // 2 - C:N // 2 + C]
        a = ax[r, j]; a.imshow(L, cmap="magma", vmin=0, vmax=0.6); a.contour(ph, [0.5], colors="c", linewidths=0.6)
        dy = (cy - P0[1] + N / 2) % N - N / 2; dx = (cx - P0[2] + N / 2) % N - N / 2
        rr = ringat(tr, t)
        a.set_title(f"#{tid} t={t}\nring {rr if rr is None else round(rr, 2)} d={np.hypot(dy, dx):.0f}px", fontsize=7); a.set_xticks([]); a.set_yticks([])
    for j in range(len(pick), nc): ax[r, j].axis("off")
fig.suptitle(f"{sys.argv[1].split('/')[-1]}: track {pid} and its daughters; L (link) with phi=1/2 contour, crops follow the cell; d = displacement from track start", fontsize=8)
fig.tight_layout(); fig.savefig(out, dpi=80)
