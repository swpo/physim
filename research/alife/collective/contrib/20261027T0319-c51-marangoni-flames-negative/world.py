"""c51: Marangoni flames. Burning pockets on a regrowing fuel at a liquid surface whose tension falls with heat.

The surface flow is compressible and driven by the Marangoni stress grad(sigma), sigma = -m T, smoothed by the
substrate's viscous response (deep layer: u_k = i k sigma_k / (eta (|k| + kd))):
    d T = -div(u T) + kT lap T + Q r - h T
    d Y = -div(u Y) + kY lap Y - r + kF (1 - Y)
    r   = A Y T^2 / (T^2 + Ti^2) [T > Tc]
Hot regions push the surface away from themselves; nothing in the code marks a body or a direction.
Switches: m 0 (no flow: the plain reaction-diffusion twin), fork_t (fuel emptied at fork_t, regrowth off).
"""
import json, os
import numpy as np
from labkit import ops

META = {"name": "marangoni-flames", "family": "reactive-marangoni", "size": (128, 128), "steps_per_frame": 25,
        "dt": 0.04, "channels": ["heat T", "fuel Y", "|u|", "burn r"], "matter": [0], "threshold": 0.25}
P = {"m": 2.0, "eta": 1.0, "kd": 0.1, "kT": 0.1, "kY": 2.0, "Q": 1.0, "h": 0.3, "A": 1.0, "Ti": 0.5, "Tc": 0.05,
     "kF": 0.02, "noise": 0.4, "L": 4.0, "dt": 0.04, "fork_t": -1.0, "uY": 1.0, "my": 0.0, "mt": 1.0}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    n = ops.fft_conv(rng.standard_normal((H, W)), ops.gauss_kernel(H, W, P["L"])); n = n / n.std()
    ky, kx = ops.wavenumbers(H, W); k2 = kx ** 2 + ky ** 2; dt = P["dt"]
    return {"T": np.clip(P["noise"] * n, 0, None), "Y": np.ones((H, W)), "t": 0.0, "shape": (H, W), "kx": kx, "ky": ky,
            "resp": P["m"] / (P["eta"] * (np.sqrt(k2) + P["kd"])),
            "LT": 1 / (1 + dt * (P["kT"] * k2 + P["h"])), "LY": 1 / (1 + dt * P["kY"] * k2), "r": np.zeros((H, W)),
            "uy": np.zeros((H, W)), "ux": np.zeros((H, W))}


def step(s):
    q, dt, sh = P, P["dt"], s["shape"]
    T, Y = s["T"], s["Y"]
    Th = ops.rfft2(q["mt"] * T - q["my"] * Y)       # sigma = -m (T - my Y): with my > 0 fuel raises the tension
    uy = ops.irfft2(-1j * s["ky"] * Th * s["resp"], sh)    # u = -m grad(T - my Y) smoothed
    ux = ops.irfft2(-1j * s["kx"] * Th * s["resp"], sh)
    r = q["A"] * Y * T ** 2 / (T ** 2 + q["Ti"] ** 2) * (T > q["Tc"])
    r = np.minimum(r, Y / dt)
    kF = q["kF"]
    if q["fork_t"] >= 0 and s["t"] >= q["fork_t"]:
        kF = 0.0
        if not s.get("forked"):
            Y = 0.0 * Y; r = 0.0 * r; s["forked"] = True
    nT = T + dt * (-ops.upwind_flux_div(T, uy, ux) + q["Q"] * r)
    nY = Y + dt * (-q["uY"] * ops.upwind_flux_div(Y, uy, ux) - r + kF * (1 - Y))
    s["T"] = np.clip(ops.irfft2(ops.rfft2(nT) * s["LT"], sh), 0, None)
    s["Y"] = np.clip(ops.irfft2(ops.rfft2(nY) * s["LY"], sh), 0, None)
    s["r"], s["uy"], s["ux"] = r, uy, ux
    s["t"] += dt
    return s


def fields(s):
    return np.stack([s["T"], s["Y"], np.hypot(s["uy"], s["ux"]), s["r"]])
