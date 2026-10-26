"""splits.py <npz> [hold_frames=40]: particle-identity genealogy of A+B clusters (food excluded).
A cluster at frame f+1 continues the cluster at f that holds most of its particles (>= 30% of the smaller);
a parent whose particles found >= 2 clusters (each >= nmin, each taking >= 20% of the parent) splits.
A split is persistent when both children live >= hold frames and never share a cluster again in that window.
Prints splits, persistent splits, merges and the persistent-split list (frame, parent size, child sizes)."""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0]); from clusters import clusters
npz = sys.argv[1]; hold = int(sys.argv[2]) if len(sys.argv) > 2 else 40
d = np.load(npz); X, SP, L, dt = d["x"], d["sp"], float(d["L"]), float(d["dt"])
if SP.ndim == 1: SP = np.repeat(SP[None], len(X), 0)
F = len(X); labs = []
for f in range(F):
    kp = SP[f] != 2; lab = -np.ones(len(kp), int); lab[kp], _ = clusters(X[f][kp], L); labs.append(lab)
splits, merges = [], 0
for f in range(F - 1):
    a, b = labs[f], labs[f + 1]
    for k in range(a.max() + 1):
        idx = a == k; nk = idx.sum(); ch = b[idx]; ch = ch[ch >= 0]
        if len(ch) == 0: continue
        cs, cn = np.unique(ch, return_counts=True); big = cs[cn >= 0.2 * nk]
        if len(big) >= 2: splits.append((f, nk, [int((b == c).sum()) for c in big], big[:2]))
    for c in range(b.max() + 1):
        par = a[b == c]; par = par[par >= 0]
        if len(par) == 0: continue
        ps, pn = np.unique(par, return_counts=True)
        if (pn >= 0.2 * (b == c).sum()).sum() >= 2: merges += 1
def members(f, c): return set(np.nonzero(labs[f] == c)[0])
pers = []
for (f, nk, sizes, (c1, c2)) in splits:
    if f + hold >= F: continue
    m1, m2 = members(f + 1, c1), members(f + 1, c2); ok = True
    for g in range(f + 2, f + 1 + hold):
        l1 = [labs[g][i] for i in m1 if labs[g][i] >= 0]; l2 = [labs[g][i] for i in m2 if labs[g][i] >= 0]
        if len(l1) < 0.3 * len(m1) or len(l2) < 0.3 * len(m2): ok = False; break
        c1g = np.bincount(l1).argmax(); c2g = np.bincount(l2).argmax()
        if c1g == c2g: ok = False; break
        m1 = set(np.nonzero(labs[g] == c1g)[0]); m2 = set(np.nonzero(labs[g] == c2g)[0])
    if ok: pers.append((f, nk, sizes))
print(npz.split("/")[-1], "frames", F, "splits", len(splits), "merges", merges, "persistent", len(pers), "(hold %d frames = %.0f t)" % (hold, hold * dt))
for p in pers[:12]: print("  t=%.0f parent %d -> %s" % (p[0] * dt, p[1], p[2]))
if len(sys.argv) > 3:  # strips of up to 4 random persistent splits: crops centred on the parent, A red, B blue, food grey
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from clusters import pcentroid
    rng = np.random.default_rng(1); pick = rng.choice(len(pers), size=min(4, len(pers)), replace=False)
    offs = [-10, 0, 5, 10, 20, 40]; fig, ax = plt.subplots(len(pick), len(offs), figsize=(2.4 * len(offs), 2.5 * len(pick)), squeeze=False)
    for r, j in enumerate(pick):
        f, nk, sizes = pers[j]
        par = [k for k in range(labs[f].max() + 1) if (labs[f] == k).sum() == nk][0]; c = pcentroid(X[f][labs[f] == par], L)
        for q, o in enumerate(offs):
            g = min(max(f + o, 0), F - 1); x = (X[g] - c + L / 2) % L - L / 2; a = ax[r, q]
            for k, col, sz in ((2, "0.75", 2), (0, "red", 5), (1, "blue", 5)):
                m = (SP[g] == k) & (np.abs(x).max(1) < 18); a.scatter(x[m, 0], x[m, 1], s=sz, c=col)
            a.set_xlim(-18, 18); a.set_ylim(-18, 18); a.set_aspect(1); a.set_xticks([]); a.set_yticks([])
            a.set_title(f"t={g * dt:.0f}" + (f" {nk}->{sizes}" if o == 0 else ""), fontsize=7)
    fig.tight_layout(); fig.savefig(sys.argv[3], dpi=80); print("strip", sys.argv[3])
