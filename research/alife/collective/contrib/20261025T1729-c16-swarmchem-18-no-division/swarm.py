"""Swarm Chemistry (Sayama 2009): heterogeneous self-propelled agents; each species k has a kinetic recipe
(R neighbour radius, Vn normal speed, Vm max speed, c1 cohesion, c2 alignment, c3 separation, c4 random steering
probability, c5 pace keeping). Agents see all agents within R regardless of species. Periodic box."""
import numpy as np

def step(x, v, sp, rec, box, rng, dt=1.0):
    R, Vn, Vm, c1, c2, c3, c4, c5 = [rec[:, i][sp] for i in range(8)]
    d = x[None, :, :] - x[:, None, :]; d -= box * np.round(d / box)
    dist = np.sqrt((d ** 2).sum(-1)) + np.eye(len(x)) * 1e9
    nb = dist < R[:, None]; cnt = nb.sum(1)
    has = cnt > 0
    cen = (d * nb[..., None]).sum(1) / np.maximum(cnt, 1)[:, None]              # relative centroid of neighbours
    vav = (v[None, :, :] * nb[..., None]).sum(1) / np.maximum(cnt, 1)[:, None]
    sep = -(d * nb[..., None] / np.maximum(dist, 1e-3)[..., None] ** 2).sum(1)
    a = np.where(has[:, None], c1[:, None] * cen + c2[:, None] * (vav - v) + c3[:, None] * sep, 0.0)
    rnd = rng.random(len(x)) < c4
    a[rnd] += rng.uniform(-5, 5, (rnd.sum(), 2))
    vn = v + a * dt
    s = np.sqrt((vn ** 2).sum(1)) + 1e-9
    vn = vn * (np.minimum(s, Vm) / s)[:, None]
    s = np.sqrt((vn ** 2).sum(1)) + 1e-9
    vn = c5[:, None] * (Vn / s)[:, None] * vn + (1 - c5[:, None]) * vn
    return (x + vn * dt) % box, vn

def random_recipe(rng, k):
    return np.stack([rng.uniform(0, 300, k), rng.uniform(0, 20, k), rng.uniform(0, 40, k), rng.uniform(0, 1, k),
                     rng.uniform(0, 1, k), rng.uniform(0, 100, k), rng.uniform(0, 0.5, k), rng.uniform(0, 1, k)], 1)
