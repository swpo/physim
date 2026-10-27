"""c49: reacting buoyant fluid. Burning pockets in a 2D Boussinesq flow eat a regrowing fuel.

Vorticity-streamfunction form on a periodic box, gravity along -y:
    d omega = -u.grad omega + nu lap omega - mu omega + g dT/dx            (buoyancy torque; linear drag mu)
    d T     = -u.grad T + kT lap T + Q r - h T                              (heat; loss h)
    d Y     = -u.grad Y + kY lap Y - r + kF (1 - Y)                        (fuel; open regrowth = energy supply)
    r       = A Y T^2 / (T^2 + Ti^2) * [T > Tc]   (ignition-like burning: needs heat to burn, makes heat)
    u = (dpsi/dy, -dpsi/dx),  lap psi = -omega
Hot pockets burn fuel, become buoyant, rise and roll up into vortex-bound caps; nothing in the code marks a body.
Switches: g 0 (no flow: plain reaction-diffusion twin), fork_t (fuel set to 0 at fork_t and its regrowth off from then on);
cut_t, cut_x, cut_w (from cut_t the fuel is held at 0 in a vertical strip of width cut_w centred on x = cut_x: a local
supply cut on the path of one rising cap); dx (grid spacing; physical box = size * dx, so --size 192 with dx 2/3 is the
same box at 1.5x resolution).
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
     "kF": 0.02, "noise": 0.4, "L": 4.0, "dt": 0.04, "fork_t": -1.0, "hyper": 1e-3,
     "dx": 1.0, "cut_t": -1.0, "cut_x": 0.0, "cut_w": 0.0}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    q = dict(P)
    n = ops.fft_conv(rng.standard_normal((H, W)), ops.gauss_kernel(H, W, q["L"] / q["dx"]))
    n = n / n.std()
    T = np.clip(q["noise"] * n, 0, None)
    Y = np.ones((H, W))
    om = np.zeros((H, W))
    ky, kx = ops.wavenumbers(H, W, q["dx"])
    k2 = kx ** 2 + ky ** 2
    dt = q["dt"]
    kmax = np.abs(ky).max(); kxm = np.abs(kx).max()
    da = ((np.abs(ky) < (2 / 3) * kmax) & (np.abs(kx) < (2 / 3) * kxm)).astype(float)
    inv = np.where(k2 > 0, 1.0 / np.where(k2 > 0, k2, 1), 0.0)
    xx = np.broadcast_to(np.arange(W)[None, :] * q["dx"], (H, W))
    dxc = (xx - q["cut_x"] + W * q["dx"] / 2) % (W * q["dx"]) - W * q["dx"] / 2
    strip = np.abs(dxc) < q["cut_w"] / 2
    return {"strip": strip, "T": T, "Y": Y, "om": om, "t": 0.0, "shape": (H, W), "par": q, "kx": kx, "ky": ky, "inv": inv, "da": da,
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
    kF = q["kF"]
    if q["fork_t"] >= 0 and s["t"] >= q["fork_t"]:
        kF = 0.0
        if abs(s["t"] - q["fork_t"]) < dt / 2:      # abrupt removal: the fuel is emptied once at the fork
            Y = 0.0 * Y
            r = 0.0 * r
    if q["cut_t"] >= 0 and s["t"] >= q["cut_t"]:     # local cut: fuel emptied and kept at 0 in a vertical strip
        Y = np.where(s["strip"], 0.0, Y)
        r = np.where(s["strip"], 0.0, r)
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
