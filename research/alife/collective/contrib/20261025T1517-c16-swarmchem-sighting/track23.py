"""Recipe 2/23: track red-core clusters (red agents linked within eps) every 20 steps; blue radial density around them."""
import numpy as np, json, sys
from scipy.sparse.csgraph import connected_components
from scipy.sparse import csr_matrix
from swarm import step, random_recipe
N, T, run_seed, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
box = float(sys.argv[5]) if len(sys.argv) > 5 else 600.0 * np.sqrt(N / 240)
rng = np.random.default_rng(2 * 1000 + 23); rec = random_recipe(rng, 2); rng = np.random.default_rng(run_seed)
sp = np.repeat(np.arange(2), N // 2); x = rng.uniform(0, box, (N, 2)); v = rng.uniform(-1, 1, (N, 2))
def pdiff(a, b): d = a - b; return d - box * np.round(d / box)
def pcent(p):
    th = 2 * np.pi * p / box; return (np.arctan2(np.sin(th).mean(0), np.cos(th).mean(0)) * box / (2 * np.pi)) % box
rec_out = []; prof = np.zeros((2, 30)); nprof = 0
for t in range(T + 1):
    if t % 20 == 0:
        xr = x[sp == 0]; D = np.sqrt((pdiff(xr[None], xr[:, None]) ** 2).sum(-1))
        n, lab = connected_components(csr_matrix(D < 15))
        cl = []
        for c in range(n):
            m = lab == c
            if m.sum() < 8: continue
            cen = pcent(xr[m]); r = np.sqrt((pdiff(xr[m], cen) ** 2).sum(1)).mean()
            cl.append({"n": int(m.sum()), "cen": cen.round(1).tolist(), "R": round(float(r), 2)})
            if t >= T // 3:
                for s_ in (0, 1):
                    d = np.sqrt((pdiff(x[sp == s_], cen) ** 2).sum(1)) / max(r, 1)
                    h, _ = np.histogram(d, bins=30, range=(0, 6)); prof[s_] += h / (np.pi * ((np.arange(1, 31) * 0.2) ** 2 - (np.arange(30) * 0.2) ** 2) * r * r)
                nprof += 1
        rec_out.append({"t": t, "clusters": cl})
    x, v = step(x, v, sp, rec, box, rng)
json.dump({"N": N, "T": T, "seed": run_seed, "box": box, "rec": rec.tolist(), "series": rec_out, "radial_profile_density": (prof / max(nprof, 1)).tolist(), "radial_bins_rho": (np.arange(30) * 0.2 + 0.1).tolist()}, open(out, "w"))
c = [len(r["clusters"]) for r in rec_out]; print("clusters over time", c[::max(1, len(c)//15)])
print("red density by rho", np.round((prof / max(nprof, 1))[0][:20], 4).tolist()); print("blue density by rho", np.round((prof / max(nprof, 1))[1][:20], 4).tolist())
