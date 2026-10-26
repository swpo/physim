"""(c29) Strips of PPS persistent splits: particle crops (40 x 40 units) centred on the parent's last centroid,
from 1000 steps before to 1500 after the split; ring particles blue, core gold, spore-dense brown, gas green;
the parent's particles (at its last tracked frame) are circled in red so the daughters' material can be traced.
usage: splitview.py track.json snaps.npz out.png [n_rows] [rng_seed] [min_gen]"""
import sys, json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
d = json.load(open(sys.argv[1])); Z = np.load(sys.argv[2]); out = sys.argv[3]
nr = int(sys.argv[4]) if len(sys.argv) > 4 else 4; rs = int(sys.argv[5]) if len(sys.argv) > 5 else 0
mg = int(sys.argv[6]) if len(sys.argv) > 6 else 1
L = 250.0; T = d["tracks"]; ps = [p for p in d["psplits"] if p["gen"] >= mg and p["t"] >= 1250 and p["t"] + 1500 <= Z["t"][-1]]
rng = np.random.default_rng(rs); pick = rng.choice(len(ps), size=min(nr, len(ps)), replace=False) if ps else []
cols = np.array(["#2ca02c", "#8c564b", "#1f77b4", "#e6b800"])
offs = [-1000, -500, 0, 500, 1000, 1500]
fig, axs = plt.subplots(len(pick), len(offs), figsize=(2.3 * len(offs), 2.4 * len(pick)), squeeze=False)
for r, k in enumerate(pick):
    p = ps[k]; h = T[str(p["parent"])]["hist"][-1]; cx, cy = h[2], h[3]
    for c, o in enumerate(offs):
        ax = axs[r, c]; ax.set_xticks([]); ax.set_yticks([])
        i = int(np.argmin(np.abs(Z["t"] - (p["t"] + o))))
        x, y, N = Z["x"][i], Z["y"][i], Z["N"][i]
        dx = (x - cx + L / 2) % L - L / 2; dy = (y - cy + L / 2) % L - L / 2
        m = (np.abs(dx) < 20) & (np.abs(dy) < 20)
        ax.scatter(dx[m], dy[m], s=3, c=cols[np.digitize(N[m], [13, 16, 36])])
        ax.set_xlim(-20, 20); ax.set_ylim(-20, 20); ax.set_aspect("equal")
        ax.set_title(f"t={int(Z['t'][i])} ({o:+d})" + (f"\ngen {p['gen']}, n {p['parent_n']}->{p['kid_n']}" if o == 0 else ""), fontsize=7)
fig.suptitle(f"{sys.argv[1].split('/')[-1]}: {len(pick)} randomly chosen persistent splits of generation >= {mg} (of {len(ps)})", fontsize=8)
fig.tight_layout(); fig.savefig(out, dpi=75)
