"""Functionalized Cahn-Hilliard (FCH) amphiphile world: bilayer vesicles from noise.

One conserved field u (amphiphile density; solvent near the low well).
    F[u] = int 1/2 (lap u - W'(u))^2 - eta1/2 |grad u|^2 - eta2 W(u)
    du/dt = lap mu + feed,   mu = (lap - W''(u))(lap u - W'(u)) + eta1 lap u - eta2 W'(u)
    W(u)  = 1/2 (u+1)^2 ((u-1)^2/2 - delta)    (W(-1) = 0, deeper well near u = 1)
Units: epsilon = 1, grid dx = 0.5. The eta terms are O(1) here (strongly functionalized),
so the uniform solvent state sits near u = -1.5, not -1. Sixth order, conserved: semi-implicit
spectral step with the k^6 part and a stabiliser S k^4 implicit, the rest explicit.
In 2D a bilayer is a curve (u high on a thin line, solvent on both sides); a closed bilayer
is a vesicle (a ring with a solvent lumen); a 'pore' is a micelle (a spot).
feed: uniform influx of amphiphile into the whole domain (an open system); 0 = closed.
"""
import numpy as np

META = {
    "name": "fch-micelle-fission",
    "family": "fch-bilayer",
    "parent": None,
    "mutation": "new class: functionalized Cahn-Hilliard (Promislow/Gavish) with an asymmetric double well, O(1) functionalization",
    "size": (128, 128),
    "steps_per_frame": 200,
    "dt": 0.02,
    "channels": ["amphiphile u (shifted, u + 1.6)"],
    "matter": None,
    "threshold": 0.5,
    "smooth": 1.0,
    "periodic": True,
}

P = dict(eta1=4.0, eta2=5.0, delta=0.3, mean=-1.3, amp=0.3, dx=0.5, dt=0.02, S=4.0, feed=0.0005, feed_on=0, u_bg=-1.6)


def Wp(u, d):
    return (u + 1) * ((u - 1) ** 2 / 2 - d) + 0.5 * (u + 1) ** 2 * (u - 1)


def Wpp(u, d):
    return ((u - 1) ** 2 / 2 - d) + 2 * (u + 1) * (u - 1) + 0.5 * (u + 1) ** 2


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    u = P["mean"] + P["amp"] * rng.standard_normal((H, W))  # white noise over the whole domain
    ky = 2 * np.pi * np.fft.fftfreq(H, d=P["dx"])
    kx = 2 * np.pi * np.fft.fftfreq(W, d=P["dx"])
    kk = ky[:, None] ** 2 + kx[None, :] ** 2
    return {"u": u, "kk": kk, "n": 0}


def step(s):
    u, kk, d, dt, S = s["u"], s["kk"], P["delta"], P["dt"], P["S"]
    U = np.fft.fft2(u)
    lu = np.fft.ifft2(-kk * U).real
    wp = Wp(u, d)
    r = lu - wp
    nl = np.fft.ifft2(kk * np.fft.fft2(wp)).real - Wpp(u, d) * r + P["eta1"] * lu - P["eta2"] * wp
    U = (U - dt * kk * np.fft.fft2(nl) + dt * S * kk ** 2 * U) / (1 + dt * (kk ** 3 + S * kk ** 2))
    s["u"] = np.fft.ifft2(U).real
    s["n"] += 1
    if P["feed"] and s["n"] >= P["feed_on"]:
        s["u"] += dt * P["feed"]
    return s


def fields(s):
    return (s["u"] - P["u_bg"])[None].astype(np.float32)


def stats(s):
    return {"mean_u": round(float(s["u"].mean()), 4), "max_u": round(float(s["u"].max()), 3)}


def damage(s, mask):
    """Erased amphiphile is deleted: masked pixels reset to the solvent background."""
    s["u"][mask] = P["u_bg"] + 0.1
    return s
