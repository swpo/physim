"""Swarm Chemistry (Sayama 2009), two species: self-propelled agents with species-specific kinetic recipes
(R neighbour radius, Vn normal speed, Vm max speed, c1 cohesion, c2 alignment, c3 separation, c4 random steering
probability, c5 pace keeping). Every agent responds to all agents within its own R, regardless of species
(cohesion to the neighbours' centroid, alignment to their mean velocity, separation ~ sum d/|d|^2), takes a random
kick with probability c4, is capped at Vm and relaxed toward Vn with weight c5. Periodic box, uniform random start.
Recipe 2/23 of c16's random screen: red forms tight clusters, blue a halo around them.
WORLD_P (JSON) overrides P."""
import numpy as np, json as _json, os as _os

P = dict(N=480, box=848.53, recipe=[[26.42, 2.26, 27.89, 0.76, 0.90, 50.41, 0.09, 0.28],
                                    [66.13, 8.86, 21.85, 0.58, 0.15, 85.14, 0.31, 0.86]], grid=128, blur=1.5)
P.update(_json.loads(_os.environ.get("WORLD_P", "{}")))
META = {"name": "swarmchem-23", "family": "swarm-chemistry", "parent": "new class (Sayama 2009 Swarm Chemistry)",
        "mutation": "none; recipe from a random screen", "size": (P["grid"], P["grid"]), "steps_per_frame": 20, "dt": 1.0,
        "channels": ["red density (core species)", "blue density (halo species)"], "matter": [0], "smooth": 1.0, "periodic": True,
        "domain": (P["box"], P["box"])}

def init(seed, size):
    rng = np.random.default_rng(seed); N = int(P["N"]); box = P["box"]
    rec = np.array(P["recipe"], float); k = len(rec)
    sp = np.repeat(np.arange(k), N // k)
    return {"x": rng.uniform(0, box, (len(sp), 2)), "v": rng.uniform(-1, 1, (len(sp), 2)), "sp": sp, "rec": rec, "rng": rng, "t": 0}

def step(s):
    x, v, sp, rec, rng, box = s["x"], s["v"], s["sp"], s["rec"], s["rng"], P["box"]
    R, Vn, Vm, c1, c2, c3, c4, c5 = [rec[:, i][sp] for i in range(8)]
    d = x[None, :, :] - x[:, None, :]; d -= box * np.round(d / box)
    dist = np.sqrt((d ** 2).sum(-1)) + np.eye(len(x)) * 1e9
    nb = dist < R[:, None]; cnt = nb.sum(1); has = cnt > 0
    cen = (d * nb[..., None]).sum(1) / np.maximum(cnt, 1)[:, None]
    vav = (v[None, :, :] * nb[..., None]).sum(1) / np.maximum(cnt, 1)[:, None]
    sep = -(d * nb[..., None] / np.maximum(dist, 1e-3)[..., None] ** 2).sum(1)
    a = np.where(has[:, None], c1[:, None] * cen + c2[:, None] * (vav - v) + c3[:, None] * sep, 0.0)
    rnd = rng.random(len(x)) < c4; a[rnd] += rng.uniform(-5, 5, (rnd.sum(), 2))
    vn = v + a; sp_ = np.sqrt((vn ** 2).sum(1)) + 1e-9; vn = vn * (np.minimum(sp_, Vm) / sp_)[:, None]
    sp_ = np.sqrt((vn ** 2).sum(1)) + 1e-9; vn = c5[:, None] * (Vn / sp_)[:, None] * vn + (1 - c5[:, None]) * vn
    s["x"] = (x + vn) % box; s["v"] = vn; s["t"] += 1
    return s

def fields(s):
    from scipy import ndimage
    g = int(P["grid"]); out = []
    for k in range(len(s["rec"])):
        h, _, _ = np.histogram2d(s["x"][s["sp"] == k, 1], s["x"][s["sp"] == k, 0], bins=g, range=[[0, P["box"]], [0, P["box"]]])
        out.append(ndimage.gaussian_filter(h, P["blur"], mode="wrap"))
    return np.stack(out).astype(np.float32)

def particles(s):
    return np.column_stack([s["x"], s["sp"]])
