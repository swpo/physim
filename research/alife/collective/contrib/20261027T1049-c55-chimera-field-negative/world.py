"""c55: a field of identical phase oscillators with nonlocal Kuramoto-Sakaguchi coupling (the 2D chimera model):
    d phi/dt = omega - K Im( e^{i(phi + alpha)} conj(Z) ),     Z = G * e^{i phi}   (G: normalized Gaussian kernel, width R)
    plus small phase noise (sqrt(2 Dn) dW).
Near alpha = pi/2 the coupling is almost purely 'repulsive in phase lag', and a coherent background can coexist with
localized incoherent domains (spot chimeras, incoherent spiral cores). A body is a localized domain of low local coherence
|Z|; nothing marks it. Optional fuel: the coupling K is K0 * Y and incoherent regions burn Y, which regrows
(dY = kF (1 - Y) - e (1 - |Z|) Y + DY lap Y); fuel 0 (default) keeps K = K0.
Switches: alpha, R, fuel, ftype (0 Gaussian, 1 top-hat ring kernel).
"""
import json, os
import numpy as np
from labkit import ops

META = {
    "name": "chimera-field",
    "family": "nonlocal-oscillators",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 0.1,
    "channels": ["incoherence 1-|Z|", "cos phase", "fuel Y", "local frequency"],
    "matter": [0],
    "threshold": 0.3,
}

P = {"K": 1.0, "alpha": 1.45, "R": 6.0, "omega": 0.0, "Dn": 0.0, "dt": 0.1, "fuel": 0, "kF": 0.01, "e": 0.05,
     "DY": 0.5, "ftype": 0, "init": 0}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    q = dict(P)
    if q["init"] == 0:          # fully random phases
        phi = 2 * np.pi * rng.random((H, W))
    else:                        # smooth random phase field (random long waves)
        n = ops.fft_conv(rng.standard_normal((H, W)), ops.gauss_kernel(H, W, 8.0))
        phi = 2 * np.pi * n / n.std()
    r = ops.radial_grid(H, W)
    if q["ftype"] == 0:
        G = np.exp(-r ** 2 / (2 * q["R"] ** 2))
    else:
        G = (r <= q["R"]).astype(float)
    Gf = ops.rfft2(G / G.sum())
    ky, kx = ops.wavenumbers(H, W)
    return {"phi": phi, "Y": np.ones((H, W)), "t": 0.0, "shape": (H, W), "par": q, "Gf": Gf, "rng": rng,
            "LY": 1 / (1 + q["dt"] * q["DY"] * (kx ** 2 + ky ** 2)), "Z": np.ones((H, W), complex), "dphi": np.zeros((H, W))}


def step(s):
    q, dt, sh = s["par"], s["par"]["dt"], s["shape"]
    phi, Y = s["phi"], s["Y"]
    e = np.exp(1j * phi)
    Z = ops.irfft2(ops.rfft2(e.real) * s["Gf"], sh) + 1j * ops.irfft2(ops.rfft2(e.imag) * s["Gf"], sh)
    K = q["K"] * (Y if q["fuel"] else 1.0)
    dphi = q["omega"] - K * np.imag(np.exp(1j * (phi + q["alpha"])) * np.conj(Z))
    phi = phi + dt * dphi
    if q["Dn"] > 0:
        phi = phi + np.sqrt(2 * q["Dn"] * dt) * s["rng"].standard_normal(sh)
    s["phi"] = np.mod(phi, 2 * np.pi)
    if q["fuel"]:
        nY = Y + dt * (q["kF"] * (1 - Y) - q["e"] * (1 - np.abs(Z)) * Y)
        s["Y"] = np.clip(ops.irfft2(ops.rfft2(nY) * s["LY"], sh), 0, None)
    s["Z"], s["dphi"] = Z, dphi
    s["t"] += dt
    return s


def fields(s):
    return np.stack([1 - np.abs(s["Z"]), np.cos(s["phi"]), s["Y"], s["dphi"]])
