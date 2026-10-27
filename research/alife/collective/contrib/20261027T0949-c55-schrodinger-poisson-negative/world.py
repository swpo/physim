"""c55: self-gravitating wave matter (Schroedinger-Poisson, "fuzzy dark matter" units hbar/m = 1) in a periodic 2D box,
optionally opened by a gain paid for by a consumed, regrowing fuel Y:
    i psi_t = -1/2 lap psi + V psi + i (g Y - gam - sig |psi|^2) psi,      lap V = 4 pi G (|psi|^2 - <|psi|^2>)
    Y_t = DY lap Y + kF (1 - Y) - e Y |psi|^2
Split-step Fourier (kinetic half step, potential + gain full step, kinetic half step); the fuel is semi-implicit.
With g = gam = sig = 0 the dynamics is conservative: a random field undergoes Jeans collapse into clumps whose cores relax
to solitons (gravitational cooling). Nothing marks a body; a body is a self-bound lump of |psi|^2.
Switches: G 0 (no gravity: free dispersion twin); fork_t (fuel emptied at fork_t, regrowth off).
"""
import json, os
import numpy as np
from labkit import ops

META = {
    "name": "fed-wave-matter",
    "family": "schrodinger-poisson",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 0.2,
    "channels": ["density |psi|^2", "fuel Y", "potential -V", "phase cos"],
    "matter": [0],
    "threshold": 0.3,
}

P = {"G": 5e-4, "g": 0.0, "gam": 0.0, "sig": 0.0, "DY": 1.0, "kF": 0.01, "e": 0.01, "dx": 1.0, "dt": 0.2,
     "kc": 0.4, "eta": 0.0, "fork_t": -1.0, "rho0": 1.0}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    q = dict(P)
    ky = 2 * np.pi * np.fft.fftfreq(H, d=q["dx"])[:, None]
    kx = 2 * np.pi * np.fft.fftfreq(W, d=q["dx"])[None, :]
    k2 = kx ** 2 + ky ** 2
    # random field: Gaussian amplitude spectrum below kc, random phases (velocity dispersion ~ kc)
    spec = np.exp(-k2 / (2 * q["kc"] ** 2)) * np.exp(2j * np.pi * rng.random((H, W)))
    psi = np.fft.ifft2(spec)
    psi *= np.sqrt(q["rho0"] / np.mean(np.abs(psi) ** 2))
    dt = q["dt"]
    return {"psi": psi, "Y": np.ones((H, W)), "t": 0.0, "shape": (H, W), "par": q,
            "K": np.exp(-(0.5j + q["eta"]) * k2 * dt / 2), "invk2": np.where(k2 > 0, 1 / np.where(k2 > 0, k2, 1), 0.0),
            "LY": 1 / (1 + dt * q["DY"] * k2), "V": np.zeros((H, W))}


def step(s):
    q, dt = s["par"], s["par"]["dt"]
    psi, Y = s["psi"], s["Y"]
    kF = q["kF"]
    if q["fork_t"] >= 0 and s["t"] >= q["fork_t"]:
        kF = 0.0
        if abs(s["t"] - q["fork_t"]) < dt / 2:
            Y = 0.0 * Y
    psi = np.fft.ifft2(np.fft.fft2(psi) * s["K"])
    rho = (psi * psi.conj()).real
    V = np.fft.ifft2(-4 * np.pi * q["G"] * np.fft.fft2(rho - rho.mean()) * s["invk2"]).real
    psi = psi * np.exp(-1j * V * dt + (q["g"] * Y - q["gam"] - q["sig"] * rho) * dt)
    psi = np.fft.ifft2(np.fft.fft2(psi) * s["K"])
    rho = (psi * psi.conj()).real
    nY = Y + dt * (kF * (1 - Y) - q["e"] * Y * rho)
    s["Y"] = np.clip(np.fft.ifft2(np.fft.fft2(nY) * s["LY"]).real, 0, None)
    s["psi"], s["V"] = psi, V
    s["t"] += dt
    return s


def fields(s):
    rho = np.abs(s["psi"]) ** 2
    return np.stack([rho, s["Y"], -s["V"], np.cos(np.angle(s["psi"])) * (rho > 0.3)])
