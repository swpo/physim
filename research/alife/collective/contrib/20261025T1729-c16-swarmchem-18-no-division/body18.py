"""Recipe 3/18 bodies: clusters of all agents (link eps) with >= MIN agents, every DT steps; splits (one body -> >= 2 bodies
that each keep >= MIN agents for HOLD steps) and merges by agent overlap; radial composition (blue share vs distance from body centre)."""
import numpy as np, json, sys
from scipy.sparse.csgraph import connected_components
from scipy.sparse import csr_matrix
from swarm import step, random_recipe
seed, T, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
N, box, EPS, MIN, DT = 1200, 1400.0, 30.0, 60, 20
rng = np.random.default_rng(3 * 1000 + 18); rec = random_recipe(rng, 3); rng = np.random.default_rng(seed)
sp = np.repeat(np.arange(3), N // 3); x = rng.uniform(0, box, (N, 2)); v = rng.uniform(-1, 1, (N, 2))
def pd(a, b): d = a - b; return d - box * np.round(d / box)
def pcent(p):
    th = 2 * np.pi * p / box; return (np.arctan2(np.sin(th).mean(0), np.cos(th).mean(0)) * box / (2 * np.pi)) % box
hist = []; radial = np.zeros((3, 12)); nrad = 0
for t in range(T + 1):
    if t % DT == 0:
        D = np.sqrt((pd(x[None], x[:, None]) ** 2).sum(-1)); n, lab = connected_components(csr_matrix(D < EPS))
        sizes = np.bincount(lab); big = [c for c in range(n) if sizes[c] >= MIN]
        memb = {int(c): set(np.nonzero(lab == c)[0].tolist()) for c in big}
        hist.append({"t": t, "bodies": memb})
        if t >= 500:
            for c in big:
                m = lab == c; cen = pcent(x[m]); r = np.sqrt((pd(x[m], cen) ** 2).sum(1)); rr = r / (r.max() + 1e-9)
                for k in range(3):
                    h, _ = np.histogram(rr[sp[m] == k], bins=12, range=(0, 1)); radial[k] += h
                nrad += 1
    x, v = step(x, v, sp, rec, box, rng)
# events: body at t -> bodies at t+DT sharing >= 30% of its agents
splits = merges = 0; psplits = 0; ev = []
H = int(400 / DT)
for i in range(len(hist) - 1):
    A, B = hist[i]["bodies"], hist[i + 1]["bodies"]
    for a, sa in A.items():
        kids = [b for b, sb in B.items() if len(sa & sb) >= 0.3 * min(len(sb), len(sa)) and len(sa & sb) > 10]
        if len(kids) >= 2:
            splits += 1
            # persistent: each kid's agents stay mostly separate for H snapshots
            ok = True
            if i + 1 + H < len(hist):
                C = hist[i + 1 + H]["bodies"]
                homes = []
                for b in kids:
                    best = max(C.items(), key=lambda kv: len(kv[1] & B[b]), default=(None, set()))
                    homes.append(best[0])
                ok = len(set(homes)) == len(homes) and None not in homes
            else: ok = False
            psplits += ok; ev.append((hist[i]["t"], len(sa), [len(B[b]) for b in kids], bool(ok)))
    for b, sb in B.items():
        pars = [a for a, sa in A.items() if len(sa & sb) >= 0.3 * min(len(sb), len(sa)) and len(sa & sb) > 10]
        if len(pars) >= 2: merges += 1
tot = radial.sum(0); share = (radial / np.maximum(tot, 1)).round(3).tolist()
nb = [len(h["bodies"]) for h in hist]
res = {"seed": seed, "T": T, "bodies_mean": float(np.mean(nb[25:])), "bodies_range": [int(min(nb[25:])), int(max(nb[25:]))], "splits": splits, "persistent_splits_400": int(psplits), "merges": merges,
       "split_events": ev[:40], "species_share_by_r_over_rmax": {"red": share[0], "blue": share[1], "green": share[2]}, "recipe": rec.round(3).tolist()}
json.dump(res, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ("split_events", "recipe")}))
