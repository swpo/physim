"""Particle Lenia (Mordvintsev, Niklasson, Randazzo 2022), numpy port of the published 2D demo.

Each particle descends E = R - G evaluated at its own position, with
U(x) = w_k sum_j exp(-((|x-p_j| - mu_k)/sigma_k)^2), G = exp(-((U - mu_g)/sigma_g)^2),
R(x) = c_rep/2 sum_j max(1 - |x-p_j|, 0)^2. Open plane; fields() rasterizes U on a fixed window.
"""
import numpy as np

META = {
    "name": "particle-lenia-ref",
    "family": "particle",
    "parent": None,
    "mutation": "reference",
    "size": (128, 128),
    "steps_per_frame": 20,
    "dt": 0.1,
    "channels": ["U (particle field)"],
    "periodic": False,
}

P = dict(mu_k=4.0, sigma_k=1.0, w_k=0.022, mu_g=0.6, sigma_g=0.15, c_rep=1.0)
VIEW = 40.0  # half width of the rasterized window


def init(seed, size):
    rng = np.random.default_rng(seed)
    pts = (rng.random((200, 2)) - 0.5) * 12.0
    H, W = size
    gy, gx = np.meshgrid(np.linspace(-VIEW, VIEW, H), np.linspace(-VIEW, VIEW, W), indexing="ij")
    return {"p": pts, "grid": np.stack([gx.ravel(), gy.ravel()], 1), "shape": (H, W)}


def velocity(p):
    d = p[:, None, :] - p[None, :, :]
    r = np.sqrt((d ** 2).sum(-1) + 1e-10)
    k = np.exp(-((r - P["mu_k"]) / P["sigma_k"]) ** 2)
    U = P["w_k"] * k.sum(1)
    dU = P["w_k"] * ((k * (-2 * (r - P["mu_k"]) / P["sigma_k"] ** 2) / r)[..., None] * d).sum(1)
    G = np.exp(-((U - P["mu_g"]) / P["sigma_g"]) ** 2)
    dG = (G * (-2 * (U - P["mu_g"]) / P["sigma_g"] ** 2))[:, None] * dU
    rep = np.clip(1 - r, 0, None)
    np.fill_diagonal(rep, 0)
    dR = P["c_rep"] * ((-rep / r)[..., None] * d).sum(1)
    return -(dR - dG)


def step(s):
    s["p"] = s["p"] + META["dt"] * velocity(s["p"])
    return s


def fields(s):
    g, p = s["grid"], s["p"]
    U = np.zeros(len(g))
    for i in range(0, len(g), 4096):
        r = np.sqrt(((g[i:i + 4096, None, :] - p[None]) ** 2).sum(-1))
        U[i:i + 4096] = P["w_k"] * np.exp(-((r - P["mu_k"]) / P["sigma_k"]) ** 2).sum(1)
    return U.reshape(s["shape"])[None]


def particles(s):
    return s["p"]
