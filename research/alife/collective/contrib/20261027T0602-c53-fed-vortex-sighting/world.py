"""c53: fed vortices. A 2D incompressible fluid with no gravity and no imposed direction, in which vorticity is the body
and grows only where it eats a fuel that diffuses and regrows.

Vorticity-streamfunction form on a periodic box:
    d omega = -u.grad omega + nu lap omega + (k Y s - mu) omega          s = omega^2 / (omega^2 + wi^2)
    d Y     = -u.grad Y + kY lap Y - e Y s omega^2 + kF (1 - Y)
    u = (dpsi/dy, -dpsi/dx),  lap psi = -omega
Weak vorticity decays at mu; strong vorticity grows where fuel is present and eats it (bistable, ignition-like).
Nothing marks a body or a direction. Switches: fork_t (fuel emptied at fork_t, regrowth off).
"""
import json, os
import numpy as np
from labkit import ops

META = {
    "name": "fed-vortices",
    "family": "fed-vortex",
    "size": (128, 128),
    "steps_per_frame": 100,
    "dt": 0.02,
    "channels": ["|vorticity|", "fuel Y", "vorticity (signed)", "eating"],
    "matter": [0],
    "threshold": 0.06,
}

P = {"nu": 0.2, "mu": 0.1, "k": 0.5, "wi": 0.1, "kY": 1.0, "e": 10.0, "kF": 0.02, "noise": 0.06, "L": 4.0,
     "dt": 0.02, "fork_t": -1.0, "hyper": 0.01}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    q = dict(P)
    n = ops.fft_conv(rng.standard_normal((H, W)), ops.gauss_kernel(H, W, q["L"]))
    n = n - ops.fft_conv(n, ops.gauss_kernel(H, W, 4 * q["L"]))      # band-pass: no large-scale swirl in the initial noise
    om = q["noise"] * n / n.std()
    Y = np.ones((H, W))
    ky, kx = ops.wavenumbers(H, W)
    k2 = kx ** 2 + ky ** 2
    dt = q["dt"]
    kmax = np.abs(ky).max(); kxm = np.abs(kx).max()
    da = ((np.abs(ky) < (2 / 3) * kmax) & (np.abs(kx) < (2 / 3) * kxm)).astype(float)
    inv = np.where(k2 > 0, 1.0 / np.where(k2 > 0, k2, 1), 0.0)
    return {"om": om, "Y": Y, "t": 0.0, "shape": (H, W), "par": q, "kx": kx, "ky": ky, "inv": inv, "da": da,
            "Lom": 1 / (1 + dt * (q["nu"] * k2 + q["hyper"] * k2 ** 2)),
            "LY": 1 / (1 + dt * (q["kY"] * k2 + q["hyper"] * k2 ** 2)), "eat": np.zeros((H, W))}


def _vel(s):
    oh = ops.rfft2(s["om"]) * s["da"]; ph = oh * s["inv"]; sh = s["shape"]
    return ops.irfft2(-1j * s["kx"] * ph, sh), ops.irfft2(1j * s["ky"] * ph, sh)


def _adv(f, uy, ux, s):
    fh = ops.rfft2(f) * s["da"]; sh = s["shape"]
    a = uy * ops.irfft2(1j * s["ky"] * fh, sh) + ux * ops.irfft2(1j * s["kx"] * fh, sh)
    return ops.irfft2(ops.rfft2(a) * s["da"], sh)


def step(s):
    q, dt, sh = s["par"], s["par"]["dt"], s["shape"]
    om, Y = s["om"], s["Y"]
    kF = q["kF"]
    if q["fork_t"] >= 0 and s["t"] >= q["fork_t"]:
        kF = 0.0
        if abs(s["t"] - q["fork_t"]) < dt / 2:
            Y = 0.0 * Y
    uy, ux = _vel(s)
    w2 = om ** 2
    sat = w2 / (w2 + q["wi"] ** 2)
    eat = np.minimum(q["e"] * Y * sat * w2, Y / dt)
    nom = om + dt * (-_adv(om, uy, ux, s) + (q["k"] * Y * sat - q["mu"]) * om)
    nY = Y + dt * (-_adv(Y, uy, ux, s) - eat + kF * (1 - Y))
    s["om"] = ops.irfft2(ops.rfft2(nom) * s["Lom"], sh)
    s["Y"] = np.clip(ops.irfft2(ops.rfft2(nY) * s["LY"], sh), 0, None)
    s["eat"] = eat
    s["t"] += dt
    return s


def fields(s):
    return np.stack([np.abs(s["om"]), s["Y"], np.tanh(s["om"]), s["eat"]])
