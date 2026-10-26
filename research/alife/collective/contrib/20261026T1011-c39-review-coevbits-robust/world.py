"""labkit wrapper for the coevolving predator-prey particle world with 20-bit matching genotypes (coevbits.py, same directory).

One labkit step = CHUNK simulation steps. Fields are 64x64 histograms of prey and predators plus the food field.
Default regime: w = 10 bits (capture exp(-h^2/w^2)). WORLD_P (JSON) overrides, e.g. {"neutral": 1, "p0": 0.22}
(neutral twin) or {"neutral": 2} (shuffled twin). The O analysis does not use labkit: see README.md.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coevbits as coev  # noqa: E402

BASE = {"eat": 0.1, "cp": 0.03, "rF": 0.01, "Nq0": 30, "Np0": 1000, "cq": 0.02, "hT": 30, "step_q": 0.6, "Rs": 4, "Ediv_q": 4,
        "w": 10}
BASE.update(json.loads(os.environ.get("WORLD_P", "{}")))
CHUNK = 100

META = {
    "name": "coevbits-matching",
    "family": "particle",
    "parent": "20261026T0125-c30-q-o-needs-moving-target",
    "mutation": "individual-based predator-prey particles with heritable 20-bit matching genotypes (capture exp(-h^2/w^2), h = Hamming distance)",
    "size": (64, 64),
    "steps_per_frame": 1,
    "dt": float(CHUNK),
    "channels": ["prey", "predator", "food"],
    "matter": [0, 1],
    "smooth": 1.0,
    "periodic": True,
    "species": {"prey": [0], "predator": [1]},
}


def init(seed, size):
    st = coev.init(seed, BASE)
    st["births"] = np.zeros(2); st["deaths"] = np.zeros(2)
    return st


def step(st):
    r = coev.run(st, CHUNK, rec_every=CHUNK, maxlog=200000)
    lg = r["log"]
    for sp in (0, 1):
        st["births"][sp] += ((lg[:, 1] == sp) & (lg[:, 2] == 1)).sum()
        st["deaths"][sp] += ((lg[:, 1] == sp) & (lg[:, 2] != 1)).sum()
    st["np"], st["nq"] = r["np"], r["nq"]
    return st


def _hist(x, y, L, G):
    h, _, _ = np.histogram2d(y, x, bins=G, range=[[0, L], [0, L]])
    return h


def fields(st):
    p = st["p"]; L = p["L"]; G = 64
    a = st["pid"] >= 0; b = st["qid"] >= 0
    F = st["F"]
    if F.shape[0] != G:
        F = F.reshape(G, F.shape[0] // G, G, -1).mean((1, 3)) if F.shape[0] > G else np.kron(F, np.ones((G // F.shape[0],) * 2))
    return np.stack([_hist(st["px"][a], st["py"][a], L, G), _hist(st["qx"][b], st["qy"][b], L, G), F])


def particles(st):
    a = st["pid"] >= 0; b = st["qid"] >= 0
    return np.r_[np.c_[st["px"][a], st["py"][a], np.zeros(a.sum())], np.c_[st["qx"][b], st["qy"][b], np.ones(b.sum())]]
