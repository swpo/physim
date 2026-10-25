"""Three-kind Gray-Scott replicators on one regrowing feed, with cyclic predation (RPS).

u: feed, regrows at F(1-u).  v_i: kind i, U + 2V_i -> 3V_i, removed at (F+K).
Predation V_i + V_{i+1} -> (1+Y) V_i at rate P (kind i eats kind i+1 mod 3); the rest is lost.
MODE: cyclic | transitive (0 eats 1 and 2, 1 eats 2) | none (P=0).
Overrides: WORLD_P='{"P":..,"MODE":"..."}'.
"""
import json, os
import numpy as np
from labkit import ops

P0 = dict(DU=0.2, DV=0.1, F=0.0367, K=0.0649, P=0.5, Y=0.5, MODE="cyclic", DOMAIN=192, TON=3000)
P0.update(json.loads(os.environ.get("WORLD_P", "{}")))

META = {
    "name": "rps-gs-" + P0["MODE"],
    "family": "reaction-diffusion",
    "parent": "examples/gray_scott_mitosis",
    "mutation": "three autocatalyst kinds on one feed with cyclic predation",
    "size": (P0["DOMAIN"], P0["DOMAIN"]),
    "steps_per_frame": 100,
    "dt": 1.0,
    "channels": ["u", "v0", "v1", "v2"],
    "matter": [1, 2, 3],
    "species": {"k0": [1], "k1": [2], "k2": [3]},
}


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    # unstructured over the whole domain: a uniform random soup of small seeds of random kind
    v = np.zeros((3, H, W)); u = np.ones((H, W))
    n = H * W // 300
    yy, xx = rng.integers(0, H, n), rng.integers(0, W, n)
    kk = rng.integers(0, 3, n)
    for y, x, k in zip(yy, xx, kk):
        m = ops.disk(H, W, y, x, 3)
        v[k][m] = 0.25 + 0.1 * rng.random(); u[m] = 0.5
    v += 0.01 * rng.random((3, H, W))
    eat = np.zeros((3, 3))
    if P0["MODE"] == "cyclic":
        for i in range(3):
            eat[i, (i + 1) % 3] = P0["P"]
    elif P0["MODE"] == "transitive":
        eat[0, 1] = eat[0, 2] = eat[1, 2] = P0["P"]
    return {"u": u, "v": v, "eat": eat, "t": 0}


def step(s):
    u, v, eat = s["u"], s["v"], s["eat"]
    F, K, Y = P0["F"], P0["K"], P0["Y"]
    gain = u * v * v
    dv = gain - (F + K) * v
    s["t"] += 1
    for i in range(3 if s["t"] > P0["TON"] else 0):
        for j in range(3):
            if eat[i, j]:
                r = eat[i, j] * v[i] * v[j]
                dv[i] += Y * r
                dv[j] -= r
    s["u"] = u + P0["DU"] * ops.laplacian(u) - gain.sum(0) + F * (1 - u)
    s["v"] = v + dv + P0["DV"] * np.stack([ops.laplacian(v[i]) for i in range(3)])
    np.clip(s["v"], 0, None, out=s["v"])
    return s


def fields(s):
    return np.concatenate([s["u"][None], s["v"]])


def damage(s, mask):
    s["v"][:, mask] = 0
    s["u"][mask] = 1
    return s
