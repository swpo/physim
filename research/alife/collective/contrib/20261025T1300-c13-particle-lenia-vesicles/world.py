"""Particle Lenia (Mordvintsev, Niklasson & Randazzo 2022) in a periodic box, from a random particle soup.

Each particle i feels the energy E(x) = R(x) - G(U(x)):
  U(x) = sum_j K(|x - p_j|),  K(r) = wk exp(-((r - muk)/sk)^2)       (Lenia-like ring kernel field)
  G(u) = exp(-((u - mug)/sg)^2)                                        (growth / attraction to U = mug)
  R(x) = crep/2 sum_j max(1 - |x - p_j|, 0)^2                          (short-range repulsion)
and moves by overdamped gradient descent dp_i/dt = -grad E(p_i) (self term excluded).
Pairs within muk + 3.5 sk via a periodic k-d tree. Individuals = compact particle bodies.
WORLD_P (JSON) overrides P.
"""
import numpy as np, json as _json, os as _os
from scipy.spatial import cKDTree
from scipy.ndimage import gaussian_filter

P = dict(N=3500, L=60.0, muk=4.0, sk=1.0, wk=0.022, mug=0.6, sg=0.15, crep=1.0, dt=0.1, noise=0.0)
P.update(_json.loads(_os.environ.get("WORLD_P", "{}")))
META = {
    "name": "particle-lenia",
    "family": "particle-lenia",
    "parent": "new class (Mordvintsev et al. 2022, Particle Lenia)",
    "mutation": "none (benchmark model, many particles in a periodic box)",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": P["dt"],
    "channels": ["particle density", "U field", "G(U)"],
    "matter": [0],
    "smooth": 1.0,
    "periodic": True,
    "domain": (P["L"], P["L"]),
}


def init(seed, size):
    rng = np.random.default_rng(seed)
    return {"p": rng.random((P["N"], 2)) * P["L"], "rng": rng, "size": size, "t": 0}


def energy_terms(p):
    L = P["L"]; rc = P["muk"] + 3.5 * P["sk"]
    pr = cKDTree(p, boxsize=L).query_pairs(rc, output_type="ndarray")
    i, j = pr[:, 0], pr[:, 1]
    d = p[i] - p[j]; d -= L * np.round(d / L)
    r = np.sqrt((d ** 2).sum(-1)) + 1e-9
    k = P["wk"] * np.exp(-((r - P["muk"]) / P["sk"]) ** 2)
    n = len(p)
    U = np.bincount(i, k, n) + np.bincount(j, k, n)
    return i, j, d, r, k, U


def step(s):
    p = s["p"]; L = P["L"]
    i, j, d, r, k, U = energy_terms(p)
    dk = k * (-2 * (r - P["muk"]) / P["sk"] ** 2)          # dK/dr
    gU = np.exp(-((U - P["mug"]) / P["sg"]) ** 2)
    dG = gU * (-2 * (U - P["mug"]) / P["sg"] ** 2)         # dG/dU at each particle
    dR = -P["crep"] * np.clip(1 - r, 0, None)              # dR/dr
    # grad_i E = sum_j [R'(r_ij) - G'(U_i) K'(r_ij)] (p_i - p_j) / r_ij
    ci = (dR - dG[i] * dk) / r; cj = (dR - dG[j] * dk) / r
    grad = np.zeros_like(p)
    np.add.at(grad, i, ci[:, None] * d); np.add.at(grad, j, -cj[:, None] * d)
    p = p - P["dt"] * grad
    if P["noise"]:
        p = p + np.sqrt(2 * P["noise"] * P["dt"]) * s["rng"].standard_normal(p.shape)
    s["p"] = p % L; s["t"] += 1
    return s


def fields(s):
    H, W = s["size"]; L = P["L"]
    rho = np.histogram2d(s["p"][:, 0], s["p"][:, 1], bins=[H, W], range=[[0, L], [0, L]])[0]
    ys = (np.arange(H) + 0.5) * L / H; xs = (np.arange(W) + 0.5) * L / W
    rg = np.hypot(np.minimum(ys, L - ys)[:, None], np.minimum(xs, L - xs)[None, :])
    kg = P["wk"] * np.exp(-((rg - P["muk"]) / P["sk"]) ** 2)
    kg = np.roll(np.roll(kg, 0, 0), 0, 1)
    U = np.real(np.fft.ifft2(np.fft.fft2(rho) * np.fft.fft2(kg)))
    G = np.exp(-((U - P["mug"]) / P["sg"]) ** 2)
    return np.stack([gaussian_filter(rho, 1.0, mode="wrap"), U, G]).astype(np.float32)


def particles(s):
    return s["p"].copy()
