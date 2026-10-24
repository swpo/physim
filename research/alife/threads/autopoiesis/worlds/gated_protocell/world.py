"""Gated protocell: a continuum SCL loop on top of a Gray-Scott replicator.

S substrate (fed from a reservoir), K catalyst (autocatalytic, Gray-Scott v), L free link,
M membrane (bonded link). The autopoietic loop:
    K + S -> K + L                      (catalyst makes links)
    L -> M where |grad L| is large      (links polymerize at the edge of the link cloud)
    M gates diffusion of K and L        (div(D g(M) grad u), g = exp(-M/m0): the membrane is
                                         impermeable to catalyst and links, permeable to S)
    K autocatalysis needs L             (S K^2 h(L), h = Hill(L, L0): the catalyst only grows
                                         where links are held in, i.e. inside a membrane)
The non-diffusive ingredients are the state-dependent mobility (gated flux, a sharp
permeability barrier) and the gradient-triggered polymerization that places M on the
interface of the L cloud.
"""
import numpy as np

META = {
    "name": "gated-protocell",
    "family": "autopoiesis",
    "parent": "threads/autopoiesis/worlds/scl_lattice (continuum transcription) + examples/gray_scott_mitosis",
    "mutation": "SCL loop as fields: gated (membrane-dependent) diffusion of K and L, gradient-triggered polymerization L->M, K autocatalysis requires held-in L",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 1.0,
    "channels": ["S", "K catalyst", "L free link", "M membrane"],
    "matter": [1, 3],
    "smooth": 1.0,
    "periodic": True,
}

P = dict(DS=0.2, DK=0.1, DL=0.2, DM=0.01, F=0.0367, k=0.0649, b=0.1, dL=0.002, cM=2.0, dM=0.01,
         m0=0.08, L0=0.1, hill=2, gmin=0.0, gateK=1, gate=1.0, IC="spots", nspots=4)


def lap(u):
    return np.roll(u, 1, 0) + np.roll(u, -1, 0) + np.roll(u, 1, 1) + np.roll(u, -1, 1) - 4 * u


def gated_div(u, g, D):
    # div(D g grad u) with face mobility = min of the two cells (a thin barrier blocks fully)
    out = np.zeros_like(u)
    for ax in (0, 1):
        gf = np.minimum(g, np.roll(g, -1, ax))
        flux = D * gf * (np.roll(u, -1, ax) - u)
        out += flux - np.roll(flux, 1, ax)
    return out


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    S, K = np.ones((H, W)), np.zeros((H, W))
    L, M = np.zeros((H, W)), np.zeros((H, W))
    yy, xx = np.mgrid[0:H, 0:W]
    for _ in range(P["nspots"]):
        y, x = rng.integers(0, H), rng.integers(0, W)
        m = ((yy - y) ** 2 + (xx - x) ** 2) <= 16
        S[m], K[m], L[m] = 0.5, 0.25, 0.5
    K += 0.01 * rng.random((H, W))
    return {"S": S, "K": K, "L": L, "M": M}


def step(s):
    S, K, L, M = s["S"], s["K"], s["L"], s["M"]
    g = P["gmin"] + (1 - P["gmin"]) * np.exp(-M / P["m0"]) if P["gate"] else np.ones_like(M)
    hL = L ** P["hill"] / (L ** P["hill"] + P["L0"] ** P["hill"])
    auto = S * K * K * hL
    prodL = P["b"] * K * S
    lim = np.minimum(1.0, 0.5 * S / np.maximum(auto + prodL, 1e-12))  # never consume more S than is there
    auto, prodL = auto * lim, prodL * lim
    Ls = 0.25 * (np.roll(L, 1, 0) + np.roll(L, -1, 0) + np.roll(L, 1, 1) + np.roll(L, -1, 1))  # smoothed: no checkerboard
    gy = 0.5 * (np.roll(Ls, -1, 0) - np.roll(Ls, 1, 0))
    gx = 0.5 * (np.roll(Ls, -1, 1) - np.roll(Ls, 1, 1))
    form = L * np.minimum(P["cM"] * np.sqrt(gy * gy + gx * gx), 0.2) * (1 - M)
    s["S"] = np.maximum(S + P["DS"] * lap(S) - auto - prodL + P["F"] * (1 - S), 0)
    s["K"] = np.maximum(K + gated_div(K, g if P["gateK"] else 1.0 + 0 * g, P["DK"]) + auto - (P["F"] + P["k"]) * K, 0)
    s["L"] = np.maximum(L + gated_div(L, g, P["DL"]) + prodL - P["dL"] * L - form, 0)
    s["M"] = np.clip(M + P["DM"] * lap(M) + form - P["dM"] * M, 0, 1)
    return s


def fields(s):
    return np.stack([s["S"], s["K"], s["L"], s["M"]]).astype(np.float32)


def stats(s):
    return {k: round(float(v.sum()), 1) for k, v in s.items()}


def damage(s, mask):
    """labkit centres the disk on the centroid; for a membrane-bounded cell we move it outward
    by the cell's equivalent radius along +x so it removes a membrane arc and part of the
    interior. Everything in the disk is reset to the bath (S=1, K=L=M=0)."""
    H, W = mask.shape
    ys, xs = np.nonzero(mask)
    if len(ys) == 0:
        return s
    r = np.sqrt(len(ys) / np.pi)
    R = r / np.sqrt(0.3)
    cy, cx = ys.mean(), xs.mean() + 0.8 * R
    yy, xx = np.mgrid[0:H, 0:W]
    dy = (yy - cy + H / 2) % H - H / 2
    dx = (xx - cx + W / 2) % W - W / 2
    hole = dy ** 2 + dx ** 2 <= (1.2 * r) ** 2
    s["S"][hole], s["K"][hole], s["L"][hole], s["M"][hole] = 1, 0, 0, 0
    return s
