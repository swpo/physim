"""c13. usage: splits_feed.py WORLD_P hist.pkl every out_prefix  (hist.pkl from savehist_feed.py: list of (ids, positions)).
Bodies are sets of persistent particle ids, so lineage survives particle turnover. NOMERGE=1 draws only splits whose parent
was not made by a merge in the previous 25 frames. Writes out_prefix.json (splits), out_prefix.png, out_prefix_summary.json.

Ring lineage from a saved particle history (hist.npy, every 'every' steps): bodies = components of U<ucut particles
linked within dlink; linked across frames by shared particles (>= 30% of the smaller). For each split: parent size,
children sizes, whether the parent was itself made by a merge within the last `back` frames, and the parent's size
history. Draws crops of the first K splits (parent frame -3, 0, +3, +10, +25) coloured by body."""
import sys, os, json, importlib.util as u, numpy as np
from scipy.spatial import cKDTree
from scipy.sparse.csgraph import connected_components
from scipy.sparse import coo_matrix
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import pickle; os.environ["WORLD_P"] = sys.argv[1]; HI = pickle.load(open(sys.argv[2], "rb")); Hf = [h[1] for h in HI]; IDS = [h[0] for h in HI]; every = int(sys.argv[3]); out = sys.argv[4]
ucut, dlink, nmin, back = 0.75, 0.8, 8, 25
s = u.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py")); w = u.module_from_spec(s); s.loader.exec_module(w)
L = w.P["L"]; dt = w.P["dt"] * every
def bodies(p, ids):
    U = w.energy_terms(p)[5]; idx = np.nonzero(U < ucut)[0]
    pr = cKDTree(p[idx], boxsize=L).query_pairs(dlink, output_type="ndarray")
    g = coo_matrix((np.ones(len(pr)), (pr[:, 0], pr[:, 1])), shape=(len(idx), len(idx)))
    n, lab = connected_components(g, directed=False)
    return [set(ids[idx[lab == k]].tolist()) for k in range(n) if (lab == k).sum() >= nmin]
B = [bodies(p.astype(float), ii) for p, ii in zip(Hf, IDS)]
links = []
for f in range(1, len(B)):
    a, b = B[f - 1], B[f]
    ch = {i: [j for j, y in enumerate(b) if len(x & y) >= 0.3 * min(len(x), len(y))] for i, x in enumerate(a)}
    pa = {j: [i for i in ch if j in ch[i]] for j in range(len(b))}
    links.append((ch, pa))
born_by_merge = [dict() for _ in B]
splits = []
for f in range(1, len(B)):
    a, b = B[f - 1], B[f]; ch, pa = links[f - 1]
    for j, ps in pa.items():
        if len(ps) >= 2: born_by_merge[f][j] = f
        elif len(ps) == 1 and ps[0] in born_by_merge[f - 1]: born_by_merge[f][j] = born_by_merge[f - 1][ps[0]]
    for i, kids in ch.items():
        if len(kids) >= 2:
            hist = [len(a[i])]; k = i; ff = f - 1
            while ff > 0 and len(hist) < 60:
                pp = links[ff - 1][1].get(k, [])
                if len(pp) != 1: break
                k = pp[0]; ff -= 1; hist.append(len(B[ff][k]))
            surv = []
            for j in kids:
                k = j; ok = True
                for g2 in range(f + 1, min(f + 26, len(B))):
                    c2 = links[g2 - 1][0].get(k, [])
                    if len(c2) != 1 or len(links[g2 - 1][1].get(c2[0], [])) != 1: ok = False; break
                    k = c2[0]
                surv.append(ok)
            m = i in born_by_merge[f - 1] and (f - 1 - born_by_merge[f - 1][i]) <= back
            splits.append({"t": round(f * dt, 1), "f": f, "parent": i, "parent_n": len(a[i]), "kids_n": [len(b[j]) for j in kids],
                           "kids_survive_25f": surv, "parent_from_recent_merge": bool(m), "parent_size_history_back": hist[::5]})
json.dump(splits, open(out + ".json", "w"), indent=0)
good = [x for x in splits if sum(x["kids_survive_25f"]) >= 2]
print(len(splits), "splits;", len(good), "with >=2 children surviving 25 frames 1:1;", sum(not x["parent_from_recent_merge"] for x in good), "of those not from a recent merge")
for x in good: print(x)
K = [x for x in good if not x["parent_from_recent_merge"]][:7] if os.environ.get("NOMERGE") else good[:6]; offs = [-3, 0, 3, 10, 25]
if K:
    fig, ax = plt.subplots(len(K), len(offs), figsize=(2.4 * len(offs), 2.4 * len(K)), squeeze=False)
    for r, x in enumerate(K):
        par = B[x["f"] - 1][x["parent"]]; p0 = Hf[x["f"] - 1].astype(float); pos0 = {k: v for k, v in zip(IDS[x["f"] - 1].tolist(), p0)}; c = np.array([pos0[k] for k in par]); ref = c[0]; d = c - ref; d -= L * np.round(d / L); cen = ref + d.mean(0)
        for cidx, o in enumerate(offs):
            f = min(max(x["f"] + o, 0), len(B) - 1); p = Hf[f].astype(float); q = p - cen; q -= L * np.round(q / L)
            a = ax[r, cidx]; a.scatter(q[:, 1], q[:, 0], s=3, c="0.8")
            pos = {k: v for k, v in zip(IDS[f].tolist(), q)}
            for k, bb in enumerate(B[f]):
                qq = np.array([pos[i] for i in bb]); a.scatter(qq[:, 1], qq[:, 0], s=4, color=plt.cm.tab10(k % 10))
            pp = np.array([pos[i] for i in par if i in pos]).reshape(-1, 2); a.scatter(pp[:, 1], pp[:, 0], s=12, facecolors="none", edgecolors="k", linewidths=0.3)
            a.set_xlim(-7, 7); a.set_ylim(-7, 7); a.set_aspect(1); a.set_xticks([]); a.set_yticks([]); a.set_title(f"t={f*dt:.0f}", fontsize=7)
    plt.tight_layout(); plt.savefig(out + ".png", dpi=75)

# ---- merge-aware generations (c13): a split counts (persistent) when >= 2 children each survive 25 frames 1:1
# without merging; persistent-split children get parent gen + 1, everything else inherits (merge: max of parents).
pers = {(x["f"], x["parent"]) for x in splits if sum(x["kids_survive_25f"]) >= 2}
gen = [dict() for _ in B]
for j in range(len(B[0])): gen[0][j] = 0
n_merge = 0; n_birth_nothing = 0; n_death = 0
for f in range(1, len(B)):
    ch, pa = links[f - 1]
    for j in range(len(B[f])):
        ps = pa.get(j, [])
        if not ps: gen[f][j] = 0; n_birth_nothing += 1; continue
        if len(ps) >= 2: n_merge += 1
        g = max(gen[f - 1][i] for i in ps)
        if len(ps) == 1 and (f, ps[0]) in pers: g += 1
        gen[f][j] = g
    n_death += sum(1 for i, k in ch.items() if not k)
G = [max(g.values()) if g else 0 for g in gen]
nb = [len(b) for b in B]
summary = {"frames": len(B), "t_end": round((len(B) - 1) * dt), "persistent_splits": len(pers), "clean_splits_not_from_merge": sum(1 for x in splits if sum(x["kids_survive_25f"]) >= 2 and not x["parent_from_recent_merge"]),
           "all_splits": len(splits), "merges": n_merge, "births_from_nothing": n_birth_nothing, "deaths": n_death, "max_generation": max(G),
           "gen_hist_final": {int(k): int(v) for k, v in zip(*np.unique(list(gen[-1].values()), return_counts=True))},
           "bodies_every_100t": nb[::max(1, int(100 / dt))]}
json.dump(summary, open(out + "_summary.json", "w"))
print(json.dumps(summary))
