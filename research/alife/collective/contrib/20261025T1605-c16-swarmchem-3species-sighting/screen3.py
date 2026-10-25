"""3-species random recipe screen; score: number of mixed clusters, radial segregation, and cluster-count increases (fission)."""
import numpy as np, json, sys
from scipy.sparse.csgraph import connected_components
from scipy.sparse import csr_matrix
from swarm import step, random_recipe
seed0, nrec = int(sys.argv[1]), int(sys.argv[2]); box = 700.0; N = 300
def clusters(x, eps=25):
    d = x[None] - x[:, None]; d -= box * np.round(d / box); D = np.sqrt((d ** 2).sum(-1))
    return connected_components(csr_matrix(D < eps))
res = []
for k in range(nrec):
    rng = np.random.default_rng(seed0 * 1000 + k); rec = random_recipe(rng, 3)
    sp = np.repeat(np.arange(3), N // 3); x = rng.uniform(0, box, (N, 2)); v = rng.uniform(-1, 1, (N, 2))
    ncl = []; mixed = []
    for t in range(1000):
        x, v = step(x, v, sp, rec, box, rng)
        if t % 50 == 49:
            n, lab = clusters(x); sizes = np.bincount(lab); big = np.nonzero(sizes >= 12)[0]
            ncl.append(len(big)); mixed.append(sum(1 for c in big if len(np.unique(sp[lab == c])) >= 2))
    ups = int(sum(max(0, b - a) for a, b in zip(ncl[5:], ncl[6:])))
    res.append({"k": k, "rec": rec.round(3).tolist(), "ncl": ncl, "mixed": mixed, "ups_after_t300": ups})
    print(k, ncl[-5:], mixed[-5:], ups, flush=True)
json.dump(res, open(f"screen3_{seed0}.json", "w"))
