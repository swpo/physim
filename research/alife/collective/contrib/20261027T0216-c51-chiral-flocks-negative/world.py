"""c51: a Toner-Tu polar active fluid that eats. Flocking continuum (density rho, polarization p) on a regrowing food c.

    d rho = -v0 div(rho p) + Dr lap rho + k c rho^2/(1 + rho^2/ra^2) - d rho  (self-advection; autocatalytic growth on food; death)
    d p   = -lam v0 (p.grad) p + (alpha (rho - rc)/(rho + rc) - |p|^2) p - w grad rho + Dp lap p     (Toner-Tu)
    d c   = Dc lap c - k c rho^2/(1 + rho^2/ra^2) + kf (1 - c)                                      (food eaten by the agents, regrown)
Agents order (|p| > 0) only where they are dense (rho > rc); the pressure term w grad rho turns them away from crowds.
Nothing in the code marks a body. Switches: v0 0 (no self-propulsion: a plain growth-diffusion twin), fork_t (food
set to 0 at fork_t and its regrowth off from then on).
"""
import json, os
import numpy as np
from labkit import ops

META = {
    "name": "chiral-eating-flocks", "family": "polar-active-fluid",
    "size": (128, 128), "steps_per_frame": 40, "dt": 0.25,
    "channels": ["density rho", "food c", "|p|", "p_x"],
    "matter": [0], "threshold": None,
}
P = {"v0": 0.25, "Dr": 0.08, "k": 1.0, "d": 0.1016, "lam": 0.8, "alpha": 1.0, "rc": 0.15, "ra": 10.0, "w": 0.5, "Dp": 0.5,
     "Dc": 0.5, "kf": 0.0367, "noise": 0.3, "rho0": 0.25, "L": 3.0, "dt": 0.25, "fork_t": -1.0, "rs": 0.0, "nv": 2.0, "chi": 0.0}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def _ud(f, vy, vx):
    """(v.grad) f with first-order upwind differences."""
    fyp = np.roll(f, -1, -2) - f; fym = f - np.roll(f, 1, -2)
    fxp = np.roll(f, -1, -1) - f; fxm = f - np.roll(f, 1, -1)
    return vy * np.where(vy > 0, fym, fyp) + vx * np.where(vx > 0, fxm, fxp)


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    def sm(): n = ops.fft_conv(rng.standard_normal((H, W)), ops.gauss_kernel(H, W, P["L"])); return n / n.std()
    rho = np.clip(P["rho0"] * sm(), 0, None)
    py, px = P["noise"] * sm(), P["noise"] * sm()
    ky, kx = ops.wavenumbers(H, W); k2 = kx ** 2 + ky ** 2; dt = P["dt"]
    return {"rho": rho, "py": py, "px": px, "c": np.ones((H, W)), "t": 0.0, "shape": (H, W),
            "Lr": 1 / (1 + dt * P["Dr"] * k2), "Lp": 1 / (1 + dt * P["Dp"] * k2), "Lc": 1 / (1 + dt * P["Dc"] * k2)}


def step(s):
    q, dt, sh = P, P["dt"], s["shape"]
    rho, py, px, c = s["rho"], s["py"], s["px"], s["c"]
    kf = q["kf"]
    if q["fork_t"] >= 0 and s["t"] >= q["fork_t"]:
        kf = 0.0
        if not s.get("forked"):
            c = 0.0 * c; s["forked"] = True
    v0 = q["v0"] * rho ** q["nv"] / (rho ** q["nv"] + q["rs"] ** q["nv"]) if q["rs"] > 0 else q["v0"]   # speed rises with density
    eat = q["k"] * c * rho ** 2 / (1 + (rho / q["ra"]) ** 2)
    nr = rho + dt * (-ops.upwind_flux_div(rho, v0 * py, v0 * px) + eat - q["d"] * rho)
    a = q["alpha"] * (rho - q["rc"]) / (rho + q["rc"]) - (py ** 2 + px ** 2)
    gy, gx = ops.grad(rho)
    vy, vx = q["lam"] * v0 * py, q["lam"] * v0 * px
    om = q["chi"]                                  # chiral rotation rate of the polarization
    npy = py + dt * (-_ud(py, vy, vx) + a * py - q["w"] * gy + om * px)
    npx = px + dt * (-_ud(px, vy, vx) + a * px - q["w"] * gx - om * py)
    nc = c + dt * (-eat + kf * (1 - c))
    s["rho"] = np.clip(ops.irfft2(ops.rfft2(nr) * s["Lr"], sh), 0, None)
    s["py"] = ops.irfft2(ops.rfft2(npy) * s["Lp"], sh)
    s["px"] = ops.irfft2(ops.rfft2(npx) * s["Lp"], sh)
    s["c"] = np.clip(ops.irfft2(ops.rfft2(nc) * s["Lc"], sh), 0, None)
    s["t"] += dt
    return s


def fields(s):
    return np.stack([s["rho"], s["c"], np.hypot(s["py"], s["px"]), s["px"]])
