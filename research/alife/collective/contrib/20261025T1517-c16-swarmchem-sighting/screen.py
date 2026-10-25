import numpy as np, json, sys
from scipy.sparse.csgraph import connected_components
from scipy.sparse import csr_matrix
from swarm import step, random_recipe
def clusters(x, box, eps):
    d = x[None] - x[:, None]; d -= box * np.round(d / box); D = np.sqrt((d ** 2).sum(-1))
    n, lab = connected_components(csr_matrix(D < eps)); return n, lab
def pcent(p, box):
    th = 2 * np.pi * p / box; return (np.arctan2(np.sin(th).mean(0), np.cos(th).mean(0)) * box / (2 * np.pi)) % box
def analyse(x, sp, box, eps=25):
    n, lab = clusters(x, box, eps); out = []
    for c in range(n):
        m = lab == c
        if m.sum() < 15: continue
        cen = pcent(x[m], box); d = x[m] - cen; d -= box * np.round(d / box); r = np.sqrt((d ** 2).sum(1))
        s = sp[m]; kinds = np.unique(s)
        rk = {int(k): float(r[s == k].mean() / (r.mean() + 1e-9)) for k in kinds}
        out.append({"size": int(m.sum()), "cen": cen.tolist(), "R": float(r.mean()), "radial_by_species": rk})
    return out
seed0 = int(sys.argv[1]); nrec = int(sys.argv[2]); box = 600.0
res = []
for k in range(nrec):
    rng = np.random.default_rng(seed0 * 1000 + k)
    ns = 2; rec = random_recipe(rng, ns); N = 240
    sp = np.repeat(np.arange(ns), N // ns); x = rng.uniform(0, box, (N, 2)); v = rng.uniform(-1, 1, (N, 2))
    hist = []
    for t in range(600):
        x, v = step(x, v, sp, rec, box, rng)
        if t in (400, 599): hist.append(analyse(x, sp, box))
    A, B = hist
    big = [c for c in B if c["size"] >= 20]
    # motion of largest cluster between t=400 and 599 (nearest centroid)
    mv = None
    if A and B:
        a = max(A, key=lambda c: c["size"]); b = max(B, key=lambda c: c["size"])
        dd = np.array(a["cen"]) - np.array(b["cen"]); dd -= box * np.round(dd / box); mv = float(np.hypot(*dd) / (a["R"] + 1e-9))
    seg = [abs(list(c["radial_by_species"].values())[0] - list(c["radial_by_species"].values())[-1]) for c in big if len(c["radial_by_species"]) == 2]
    res.append({"k": k, "rec": rec.round(3).tolist(), "n_big": len(big), "sizes": [c["size"] for c in big], "move_BL": mv, "seg": [round(s, 2) for s in seg]})
    print(k, len(big), [c["size"] for c in big][:6], None if mv is None else round(mv, 1), [round(s, 2) for s in seg][:4], flush=True)
json.dump(res, open(f"screen_{seed0}.json", "w"))
