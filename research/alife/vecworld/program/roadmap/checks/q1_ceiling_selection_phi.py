"""Q1 check, part 2: the same family as q1_ceiling_selection.py, but now the WORLD is fixed and the coarse-graining
C (4 x 16) is chosen among 200 random projections to maximise the ceiling c(4). What happens to content?
Content measures: I1 (predictive information of o, nats per tick) and the participation ratio of the correlation
matrix of y = C x (effective number of independent macro numbers, 1..4)."""
import json
import sys

import numpy as np

# reuse the closed forms of part 1 without re-running its 4000-world loop (run from this folder)
src = open("q1_ceiling_selection.py").read().split("rows = []")[0]
ns = {}
exec(compile(src, "q1_head", "exec"), ns)
world_stats, dlyap, n0, n1, r = ns["world_stats"], ns["dlyap"], ns["n0"], ns["n1"], ns["r"]

rng = np.random.default_rng(20261110)
NW, NC = 150, 200
out = []
for w in range(NW):
    rho = rng.uniform(0.6, 0.99)                     # worlds with something to predict
    A = rng.standard_normal((n0, n0)) / np.sqrt(n0)
    A *= rho / np.max(np.abs(np.linalg.eigvals(A)))
    Gm = rng.standard_normal((n0, n0)) / np.sqrt(n0)
    Q = 0.09 * (Gm @ Gm.T + 0.1 * np.eye(n0))
    Sig = dlyap(A, Q)
    cs, i1, pr, sh = [], [], [], []
    for j in range(NC):
        C = rng.standard_normal((n1, n0)) / np.sqrt(n0)
        s = world_stats(A, Q, C)
        S = C @ Sig @ C.T
        d = np.sqrt(np.diag(S))
        lam = np.linalg.eigvalsh(S / np.outer(d, d))
        cs.append(s["c"]); i1.append(s["I1"]); sh.append(s["share_past"])
        pr.append(lam.sum() ** 2 / (lam ** 2).sum())
    cs, i1, pr, sh = map(np.array, (cs, i1, pr, sh))
    k = int(np.argmax(cs))
    ra, rb = np.argsort(np.argsort(cs)), np.argsort(np.argsort(i1))
    out.append({"c_best": cs[k], "c_med": np.median(cs), "I1_best": i1[k], "I1_med": np.median(i1),
                "PR_best": pr[k], "PR_med": np.median(pr), "share_best": sh[k], "share_med": np.median(sh),
                "spearman_c_I1": float(np.corrcoef(ra, rb)[0, 1]),
                "spearman_c_PR": float(np.corrcoef(ra, np.argsort(np.argsort(pr)))[0, 1])})
agg = {k: round(float(np.median([o[k] for o in out])), 4) for k in out[0]}
agg["frac_worlds_best_ceiling_has_lower_PR_than_median"] = round(float(np.mean([o["PR_best"] < o["PR_med"] for o in out])), 3)
agg["frac_worlds_best_ceiling_has_lower_I1_than_median"] = round(float(np.mean([o["I1_best"] < o["I1_med"] for o in out])), 3)
res = {"family": {"worlds": NW, "random_C_per_world": NC, "rho": "U(0.6, 0.99)", "tau": 4, "seed": 20261110},
       "median_over_worlds": agg}
json.dump(res, open(sys.argv[1], "w"), indent=1)
print(json.dumps(res, indent=1))
