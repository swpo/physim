"""c43: splits2.py with the minimum body area as argument 6 (default 30).
Prey division strips: a prey droplet (c_a > 0.5, area >= 30) at frame t whose pixels are covered at t+1
by >= 2 droplets of area >= 30 that each persist >= 5 frames. Reports how many splits had predator
material (c_b > 0.3) within 6 px of the parent at t ("bite" splits) and draws 8 random ones.
usage: splits2.py frames.npz out.png seed [chan: 0 prey, 1 predator] [dt per frame]
c42: generalized to either species; the "near" test reports the OTHER species within 6 px; the frame time is an argument."""
import sys, json, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
R = np.load(sys.argv[1])['render']; rng = np.random.default_rng(int(sys.argv[3]))
CH = int(sys.argv[4]) if len(sys.argv) > 4 else 0; OT = 1 - CH; DTF = float(sys.argv[5]) if len(sys.argv) > 5 else 100.0
T = len(R); A = int(sys.argv[6]) if len(sys.argv) > 6 else 30
labs = [ndimage.label(f[CH] > 0.5)[0] for f in R]
def big(L):
    a = np.bincount(L.ravel()); return {i for i in range(1, len(a)) if a[i] >= A}
bigs = [big(L) for L in labs]
def persists(t, i, n=5):
    m = labs[t] == i
    for k in range(t + 1, min(T, t + n)):
        ov = labs[k][m]; ov = ov[ov > 0]
        if not ov.size: return False
        j = np.bincount(ov).argmax()
        if j not in bigs[k]: return False
        m = labs[k] == j
    return t + n <= T
ev = []
for t in range(5, T - 6):
    L0, L1 = labs[t], labs[t + 1]
    for i in bigs[t]:
        m = L0 == i; kids = [j for j in np.unique(L1[m]) if j > 0 and j in bigs[t + 1] and (L1[m] == j).sum() >= 10]
        if len(kids) >= 2:
            # each kid must map back mainly to i (no merge partner)
            ok = all(np.bincount(L0[L1 == j][L0[L1 == j] > 0]).argmax() == i for j in kids)
            if ok and all(persists(t + 1, j) for j in kids):
                cy, cx = [int(v) for v in ndimage.center_of_mass(m)]
                near = ndimage.binary_dilation(m, iterations=6)
                bite = bool((R[t][OT][near] > 0.3).any())
                ev.append((t, cy, cx, bite))
nb = sum(e[3] for e in ev)
print(json.dumps({"splits": len(ev), "other_species_near": nb, "alone": len(ev) - nb,
                  "frames": [e[0] for e in ev]}))
pick = [ev[k] for k in rng.choice(len(ev), size=min(8, len(ev)), replace=False)] if ev else []
fig, ax = plt.subplots(max(1, len(pick)), 5, figsize=(7.5, 1.6 * max(1, len(pick))), squeeze=False)
H = R.shape[-1]; h = 22
for r, (t, cy, cx, bite) in enumerate(sorted(pick)):
    for c, dt in enumerate((-2, 0, 1, 3, 5)):
        f = R[t + dt]; ys = (np.arange(cy - h, cy + h) % H); xs = (np.arange(cx - h, cx + h) % H)
        rgb = np.stack([f[1], f[0], 0.35 * f[2]], -1)[np.ix_(ys, xs)].clip(0, 1)
        ax[r, c].imshow(rgb); ax[r, c].set_xticks([]); ax[r, c].set_yticks([])
        ax[r, c].set_title(f"t={(t + dt) * DTF:.0f}" + (" bite" if (bite and c == 1) else ""), fontsize=7)
plt.suptitle(f"random {['prey', 'predator'][CH]} divisions (green prey, red predator); split between cols 2 and 3; n={len(ev)}", fontsize=8)
plt.tight_layout(); plt.savefig(sys.argv[2], dpi=90)
