"""c55: Barkley's two-field model of transitional pipe flow (PRE 84, 016309, 2011), written in the frame moving with the
bulk speed U and extended to a periodic 2D strip, with multiplicative noise on the turbulence field:
    q_t = q (u + r - 1 - (r + delta)(q - 1)^2) + Dq lap q + sigma q xi           (turbulence intensity, puffs)
    u_t = eps1 (1 - u) - eps2 u q - u_x + Du lap u                              (centreline velocity, depleted by q)
u relaxes to the laminar profile 1 and is advected through the puff from upstream; a puff lives on the u it finds and
leaves a depleted wake. Nothing marks a body; a body is a localized region of q > threshold.
Switches: r (Reynolds-like control), sigma (noise), Dy (scale of y diffusion relative to x, 0 < Dy <= 1).
"""
import json, os
import numpy as np
from labkit import ops

META = {
    "name": "barkley-puffs",
    "family": "subcritical-turbulence",
    "size": (32, 512),
    "steps_per_frame": 200,
    "dt": 0.05,
    "channels": ["turbulence q", "centreline u"],
    "matter": [0],
    "threshold": 0.4,
}

P = {"r": 0.7, "delta": 0.1, "eps1": 0.04, "eps2": 0.2, "Dq": 1.0, "Du": 0.05, "Dy": 1.0, "sigma": 0.3, "dt": 0.05,
     "dx": 1.0, "init_frac": 0.3, "L": 6.0}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    q = dict(P)
    n = ops.fft_conv(rng.standard_normal((H, W)), ops.gauss_kernel(H, W, q["L"]))
    n = n / n.std()
    thr = np.quantile(n, 1 - q["init_frac"])
    Q = np.where(n > thr, 2.0, 0.0) * rng.random((H, W))         # random turbulent patches over the whole strip
    U = np.ones((H, W))
    ky, kx = ops.wavenumbers(H, W, q["dx"])
    dt = q["dt"]
    Lq = 1 / (1 + dt * q["Dq"] * (kx ** 2 + q["Dy"] * ky ** 2))
    Lu = np.exp(dt * (-1j * kx - q["Du"] * (kx ** 2 + ky ** 2)))
    return {"q": Q, "u": U, "t": 0.0, "shape": (H, W), "par": q, "Lq": Lq, "Lu": Lu, "rng": rng}


def step(s):
    p, dt, sh = s["par"], s["par"]["dt"], s["shape"]
    q, u = s["q"], s["u"]
    fq = q * (u + p["r"] - 1 - (p["r"] + p["delta"]) * (q - 1) ** 2)
    nq = q + dt * fq + p["sigma"] * q * np.sqrt(dt) * s["rng"].standard_normal(sh)
    nu = u + dt * (p["eps1"] * (1 - u) - p["eps2"] * u * q)
    s["q"] = np.clip(ops.irfft2(ops.rfft2(nq) * s["Lq"], sh), 0, None)
    s["u"] = ops.irfft2(ops.rfft2(nu) * s["Lu"], sh)
    s["t"] += dt
    return s


def fields(s):
    return np.stack([s["q"], s["u"]])
