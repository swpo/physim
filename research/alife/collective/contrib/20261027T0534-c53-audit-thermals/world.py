"""c53 audit copy of 20261027T0040-c49-reacting-thermals-claim/world.py, unchanged except the fork2 switch.
c49: reacting buoyant fluid. Burning pockets in a 2D Boussinesq flow eat a regrowing fuel.

Vorticity-streamfunction form on a periodic box, gravity along -y:
    d omega = -u.grad omega + nu lap omega - mu omega + g dT/dx            (buoyancy torque; linear drag mu)
    d T     = -u.grad T + kT lap T + Q r - h T                              (heat; loss h)
    d Y     = -u.grad Y + kY lap Y - r + kF (1 - Y)                        (fuel; open regrowth = energy supply)
    r       = A Y T^2 / (T^2 + Ti^2) * [T > Tc]   (ignition-like burning: needs heat to burn, makes heat)
    u = (dpsi/dy, -dpsi/dx),  lap psi = -omega
Hot pockets burn fuel, become buoyant, rise and roll up into vortex-bound caps; nothing in the code marks a body.
Switches: g 0 (no flow: plain reaction-diffusion twin), fork_t (fuel set to 0 at fork_t and its regrowth off from then on).
"""
import json, os
import numpy as np
from labkit import ops

META = {
    "name": "reacting-thermals",
    "family": "reactive-convection",
    "size": (128, 128),
    "steps_per_frame": 200,
    "dt": 0.04,
    "channels": ["heat T", "fuel Y", "vorticity", "burn r"],
    "matter": [0],
    "threshold": 0.25,
}

P = {"nu": 0.3, "mu": 0.01, "g": 0.5, "kT": 0.1, "kY": 2.0, "Q": 1.0, "h": 0.3, "A": 1.0, "Ti": 0.5, "Tc": 0.05,
     "kF": 0.02, "noise": 0.4, "L": 4.0, "dt": 0.04, "fork_t": -1.0, "hyper": 1e-3, "fork2_t": -1.0, "fork2": {}}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    q = dict(P)
    n = ops.fft_conv(rng.standard_normal((H, W)), ops.gauss_kernel(H, W, q["L"]))
    n = n / n.std()
    T = np.clip(q["noise"] * n, 0, None)
    Y = np.ones((H, W))
    om = np.zeros((H, W))
    ky, kx = ops.wavenumbers(H, W)
    k2 = kx ** 2 + ky ** 2
    dt = q["dt"]
    kmax = np.abs(ky).max(); kxm = np.abs(kx).max()
    da = ((np.abs(ky) < (2 / 3) * kmax) & (np.abs(kx) < (2 / 3) * kxm)).astype(float)
    inv = np.where(k2 > 0, 1.0 / np.where(k2 > 0, k2, 1), 0.0)
    return {"T": T, "Y": Y, "om": om, "t": 0.0, "shape": (H, W), "par": q, "kx": kx, "ky": ky, "inv": inv, "da": da,
            "Lom": 1 / (1 + dt * (q["nu"] * k2 + q["mu"] + q["hyper"] * k2 ** 2)),
            "LT": 1 / (1 + dt * (q["kT"] * k2 + q["h"] + q["hyper"] * k2 ** 2)),
            "LY": 1 / (1 + dt * (q["kY"] * k2 + q["hyper"] * k2 ** 2)), "r": np.zeros((H, W))}


def _vel(s):
    oh = ops.rfft2(s["om"]) * s["da"]; ph = oh * s["inv"]; sh = s["shape"]
    uy = ops.irfft2(-1j * s["kx"] * ph, sh)      # u_y = -dpsi/dx
    ux = ops.irfft2(1j * s["ky"] * ph, sh)       # u_x =  dpsi/dy
    return uy, ux


def _adv(f, uy, ux, s):
    fh = ops.rfft2(f) * s["da"]; sh = s["shape"]
    a = uy * ops.irfft2(1j * s["ky"] * fh, sh) + ux * ops.irfft2(1j * s["kx"] * fh, sh)
    return ops.irfft2(ops.rfft2(a) * s["da"], sh)


def step(s):
    q, dt, sh = s["par"], s["par"]["dt"], s["shape"]
    T, Y, om = s["T"], s["Y"], s["om"]
    uy, ux = _vel(s)
    r = q["A"] * Y * T ** 2 / (T ** 2 + q["Ti"] ** 2) * (T > q["Tc"])
    r = np.minimum(r, Y / dt)
    if q["fork2_t"] >= 0 and s["t"] >= q["fork2_t"] and not s.get("forked2"):
        # c53 audit control: from fork2_t on, the parameters in fork2 replace the world's (e.g. A=0 h=0: a passive,
        # conserved-heat thermal with no burning); the implicit operators are rebuilt
        q = dict(q); q.update(q["fork2"]); s["par"] = q; s["forked2"] = True
        k2 = s["kx"] ** 2 + s["ky"] ** 2
        s["Lom"] = 1 / (1 + dt * (q["nu"] * k2 + q["mu"] + q["hyper"] * k2 ** 2))
        s["LT"] = 1 / (1 + dt * (q["kT"] * k2 + q["h"] + q["hyper"] * k2 ** 2))
        s["LY"] = 1 / (1 + dt * (q["kY"] * k2 + q["hyper"] * k2 ** 2))
    kF = q["kF"]
    if q["fork_t"] >= 0 and s["t"] >= q["fork_t"]:
        kF = 0.0
        if abs(s["t"] - q["fork_t"]) < dt / 2:      # abrupt removal: the fuel is emptied once at the fork
            Y = 0.0 * Y
            r = 0.0 * r
    dTx = ops.irfft2(1j * s["kx"] * ops.rfft2(T), sh)
    nom = om + dt * (-_adv(om, uy, ux, s) + q["g"] * dTx)
    nT = T + dt * (-_adv(T, uy, ux, s) + q["Q"] * r)
    nY = Y + dt * (-_adv(Y, uy, ux, s) - r + kF * (1 - Y))
    s["om"] = ops.irfft2(ops.rfft2(nom) * s["Lom"], sh)
    s["T"] = np.clip(ops.irfft2(ops.rfft2(nT) * s["LT"], sh), 0, None)
    s["Y"] = np.clip(ops.irfft2(ops.rfft2(nY) * s["LY"], sh), 0, None)
    s["r"] = r
    s["t"] += dt
    return s


def fields(s):
    return np.stack([s["T"], s["Y"], np.tanh(s["om"]), s["r"]])
