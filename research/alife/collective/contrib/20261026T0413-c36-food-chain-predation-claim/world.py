"""Closed food chain in condensates: fuel u -> prey droplets a -> predator droplets b -> waste w -> fuel u.

    c_a = (phi_a + 1 + e) / (2 + e),  c_b = (phi_b + 1) / 2          (material fractions)
    d phi_a = M lap(phi_a^3 - phi_a - kappa lap phi_a + chi c_b) + (2+e) R_a
    d phi_b = M lap(phi_b^3 - phi_b - kappa lap phi_b + chi c_a) + 2 R_b
    R_a = k1 u c_a^2 - kp c_a - k2 c_a c_b^2          (prey: autocatalytic on fuel, eaten by predator)
    R_b = k2 c_a c_b^2 - kq c_b                         (predator: autocatalytic on prey material)
    d u = Du lap u - k1 u c_a^2 + r w                   (fuel regrows from waste everywhere)
    d w = Dw lap w + kp c_a + kq c_b - r w

Every reaction is a transfer, so sum(c_a + c_b + u + w) is conserved (closed ledger, no feed).
The prey's dilute phase sits at c_a = e/(2+e) > 0, so a predator can feed on dissolved prey as well
as on prey droplets it touches. Predation is a mass-action reaction between two materials; no term
refers to a body, a distance or a kind. Ksat (default off) gives a saturating (type II) response.
"""
import os, json
import numpy as np
from labkit import ops

META = {
    "name": "condensate-food-chain",
    "family": "active-emulsion",
    "parent": "threads/active-droplets/worlds/ad1-fuel",
    "mutation": "two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel",
    "size": (256, 256),
    "steps_per_frame": 200,
    "dt": 0.5,
    "channels": ["prey a", "predator b", "fuel u", "waste w"],
    "matter": [0, 1],
    "threshold": None,
    "species": {"prey": [0], "predator": [1]},
    "radial_channels": [0, 1, 2, 3],
}

P = dict(M=0.03, kappa=1.0, A=2.0, chi=0.3, e=0.1, k1=0.1, kp=0.02, k2=0.2, kq=0.003, r=0.01,
         Du=2.0, Dw=2.0, dt=0.5, ma=-0.55, mb=-0.97, noise=0.3, nb=0.15, u0=1.0, w0=0.0, pred_on=1, Ksat=1e9, k0=0.001)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def _ca(phi_a):
    return np.clip((phi_a + 1 + P["e"]) / (2 + P["e"]), 0, None)


def _cb(phi_b):
    return np.clip((phi_b + 1) / 2, 0, None)


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    # unstructured start over the whole domain: white noise, smoothed over 2 px
    def noise():
        n = rng.standard_normal((H, W))
        n = ops.fft_conv(n, ops.gauss_kernel(H, W, 2.0))
        return n / n.std()
    pa = P["ma"] + P["noise"] * noise()
    pb = (P["mb"] + P["nb"] * noise()) if P["pred_on"] else -np.ones((H, W))
    u = P["u0"] * np.ones((H, W))
    w = P["w0"] * np.ones((H, W))
    ky, kx = ops.wavenumbers(H, W)
    k2 = kx ** 2 + ky ** 2
    dt, M = P["dt"], P["M"]
    return {"pa": pa, "pb": pb, "u": u, "w": w, "k2": k2, "shape": (H, W),
            "den": 1 + dt * M * k2 * (P["A"] + P["kappa"] * k2), "denu": 1 + dt * P["Du"] * k2,
            "denw": 1 + dt * P["Dw"] * k2}


def step(s):
    pa, pb, u, w, k2, dt, M = s["pa"], s["pb"], s["u"], s["w"], s["k2"], P["dt"], P["M"]
    ca, cb = _ca(pa), _cb(pb)
    feed = P["k1"] * u * ca ** 2 + P["k0"] * u     # k0: slow uncatalysed fuel -> prey
    eat = P["k2"] * ca * cb ** 2 / (1 + ca / P["Ksat"])
    # explicit-step safety: no reaction may take more than half of its reactant in one step
    feed = np.minimum(feed, 0.5 * np.clip(u, 0, None) / dt)
    eat = np.minimum(eat, 0.5 * ca / dt)
    Ra = feed - P["kp"] * ca - eat
    Rb = eat - P["kq"] * cb
    regen = P["r"] * w
    sh = s["shape"]
    def ch(phi, other, R, scale):
        mu_nl = phi ** 3 - phi - P["A"] * phi + P["chi"] * other
        h = (ops.rfft2(phi) - dt * M * k2 * ops.rfft2(mu_nl) + dt * scale * ops.rfft2(R)) / s["den"]
        return ops.irfft2(h, sh)
    s["pa"] = ch(pa, cb, Ra, 2 + P["e"])
    s["pb"] = ch(pb, ca, Rb, 2.0)
    s["u"] = ops.irfft2((ops.rfft2(u) + dt * ops.rfft2(regen - feed)) / s["denu"], sh)
    s["w"] = ops.irfft2((ops.rfft2(w) + dt * ops.rfft2(P["kp"] * ca + P["kq"] * cb - regen)) / s["denw"], sh)
    return s


def fields(s):
    return np.stack([_ca(s["pa"]), _cb(s["pb"]), s["u"], s["w"]])


def damage(s, mask):
    s["pa"][mask] = -1.0
    s["pb"][mask] = -1.0
    return s
