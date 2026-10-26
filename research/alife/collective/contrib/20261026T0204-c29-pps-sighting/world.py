"""Primordial Particle System (Schmickl, Stefanec & Crailsheim 2016, Sci Rep 6:37969), new class pps.

Each particle has a position p and heading phi, moves at constant speed v and turns by
    dphi = alpha + beta * N * sign(R - L)
where L and R count the other particles within radius r in the left and right half-discs relative to its
heading and N = L + R. Published parameters: r = 5, alpha = 180 deg, beta = 17 deg, v = 0.67, density 0.08
(5000 particles on a 250 x 250 torus). Default update: asynchronous, one random permutation per step, each
particle sees the current positions of the others (as in the paper). WORLD_P {"sync": 1} switches to
synchronous updates. Initial condition: uniform random positions and headings over the whole torus.
No feed, no decay, no division rule: particles are conserved and nothing else is imposed.
Fields (2 units per pixel): all particles, 'core/cell' particles (N > 35, yellow in the paper),
'ring' particles (15 < N <= 35, blue).
"""
import os, json
import numpy as np
from numba import njit

P = dict(r=5.0, alpha=180.0, beta=17.0, v=0.67, L=250.0, n=5000, sync=0, px=2.0)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))
NG = int(round(P["L"] / P["px"]))

META = {
    "name": "pps",
    "family": "particle",
    "parent": None,
    "mutation": "new class: Schmickl's Primordial Particle System, published parameters",
    "size": (NG, NG),
    "steps_per_frame": 150,
    "dt": 1.0,
    "channels": ["particles", "cell N>35", "ring 15<N<=35"],
    "matter": [0],
    "threshold": 0.35,
    "smooth": 1.5,
    "periodic": True,
    "domain": (P["L"], P["L"]),
    "radial_channels": [0, 1, 2],
}


@njit
def _build(x, y, nc, cs):
    n = x.shape[0]
    head = -np.ones(nc * nc, np.int64); nxt = -np.ones(n, np.int64)
    for i in range(n):
        cx = int(x[i] / cs) % nc; cy = int(y[i] / cs) % nc
        c = cy * nc + cx; nxt[i] = head[c]; head[c] = i
    return head, nxt


@njit
def _count(i, x, y, ph, head, nxt, nc, cs, r, Lb):
    xi, yi = x[i], y[i]; c, s = np.cos(ph[i]), np.sin(ph[i])
    cx = int(xi / cs) % nc; cy = int(yi / cs) % nc
    Lc = 0; Rc = 0; r2 = r * r
    for dyc in (-1, 0, 1):
        for dxc in (-1, 0, 1):
            j = head[((cy + dyc) % nc) * nc + (cx + dxc) % nc]
            while j >= 0:
                if j != i:
                    dx = x[j] - xi; dy = y[j] - yi
                    dx -= Lb * np.round(dx / Lb); dy -= Lb * np.round(dy / Lb)
                    if dx * dx + dy * dy <= r2:
                        if c * dy - s * dx < 0: Lc += 1
                        else: Rc += 1
                j = nxt[j]
    return Lc, Rc


@njit
def _step(x, y, ph, Nn, order, r, alpha, beta, v, Lb, sync):
    nc = int(Lb // (r + v + 0.01)); cs = Lb / nc
    head, nxt = _build(x, y, nc, cs)
    n = x.shape[0]
    if sync:
        dphi = np.zeros(n)
        for i in range(n):
            Lc, Rc = _count(i, x, y, ph, head, nxt, nc, cs, r, Lb)
            N = Lc + Rc; Nn[i] = N
            dphi[i] = alpha + beta * N * np.sign(Rc - Lc)
        for i in range(n):
            ph[i] = (ph[i] + dphi[i]) % (2 * np.pi)
            x[i] = (x[i] + v * np.cos(ph[i])) % Lb; y[i] = (y[i] + v * np.sin(ph[i])) % Lb
    else:
        for k in range(n):
            i = order[k]
            Lc, Rc = _count(i, x, y, ph, head, nxt, nc, cs, r, Lb)
            N = Lc + Rc; Nn[i] = N
            ph[i] = (ph[i] + alpha + beta * N * np.sign(Rc - Lc)) % (2 * np.pi)
            x[i] = (x[i] + v * np.cos(ph[i])) % Lb; y[i] = (y[i] + v * np.sin(ph[i])) % Lb
            # cell lists are rebuilt each step; a moved particle stays within one cell of its listed cell (cs >= r + v)


def init(seed, size):
    rng = np.random.default_rng(seed)
    n = int(P["n"]); Lb = P["L"]
    return {"x": rng.random(n) * Lb, "y": rng.random(n) * Lb, "ph": rng.random(n) * 2 * np.pi,
            "N": np.zeros(n, np.int64), "rng": rng}


def step(s):
    order = s["rng"].permutation(len(s["x"]))
    _step(s["x"], s["y"], s["ph"], s["N"], order, P["r"], np.deg2rad(P["alpha"]), np.deg2rad(P["beta"]),
          P["v"], P["L"], int(P["sync"]))
    return s


def _hist(x, y, w=None):
    h, _, _ = np.histogram2d(y, x, bins=NG, range=[[0, P["L"]], [0, P["L"]]], weights=w)
    return h / (P["px"] ** 2) / 0.32  # 1.0 = four times the mean density (0.08)


def fields(s):
    N = s["N"]
    return np.stack([_hist(s["x"], s["y"]), _hist(s["x"], s["y"], (N > 35).astype(float)),
                     _hist(s["x"], s["y"], ((N > 15) & (N <= 35)).astype(float))]).astype(np.float32)


def particles(s):
    return np.stack([s["x"], s["y"], np.digitize(s["N"], [13, 16, 36])]).T


def damage(s, mask):
    """Erased particles are relocated as background: uniformly at random over the torus, random heading."""
    ix = np.clip((s["x"] / P["px"]).astype(int), 0, NG - 1); iy = np.clip((s["y"] / P["px"]).astype(int), 0, NG - 1)
    hit = mask[iy, ix]; rng = s["rng"]; k = int(hit.sum())
    s["x"][hit] = rng.random(k) * P["L"]; s["y"][hit] = rng.random(k) * P["L"]; s["ph"][hit] = rng.random(k) * 2 * np.pi
    return s
