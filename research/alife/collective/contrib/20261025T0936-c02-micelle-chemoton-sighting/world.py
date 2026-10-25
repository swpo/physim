"""Micelle chemoton: FCH micelles from noise that grow only on amphiphile made by a catalyst they hold.

Fork of c01's fch-uptake-cargo (itself a fork of c03's fch-cargo-fission): the same strongly
functionalized FCH micelle regime (eps=1, dx=0.5, eta1=4, eta2=5, white-noise start), but
  - the global amphiphile feed is removed; amphiphile is made only by a catalyst K from a precursor Pp:
        du/dt = lap mu_FCH + r K Pp - kap (u - u_bg)_+          (amphiphile decays: maintenance)
  - K partitions into amphiphile-rich cores (Scharfetter-Gummel flux, chi = -3, as c01's solute) and is
    autocatalytic on Pp (Gray-Scott-like):   dK/dt = div(DK (grad K + chi K grad u)) + a K^2 Pp - dK K
  - Pp is fed uniformly and diffuses freely:  dPp/dt = DP lap Pp + F (1 - Pp) - a K^2 Pp - r K Pp
Initial condition: FCH white noise as c03, K = K0 U(0,1) white noise, Pp = 1 (unstructured).
"""
import numpy as np

META = {
    "name": "fch-micelle-chemoton",
    "family": "fch-bilayer",
    "parent": "collective/contrib/20261025T0810-c01-fch-uptake-cargo/world.py",
    "mutation": "global amphiphile feed replaced by amphiphile made by a partitioning autocatalyst K from a fed precursor; amphiphile decays",
    "size": (128, 128),
    "steps_per_frame": 200,
    "dt": 0.02,
    "channels": ["amphiphile u (u + 1.6)", "catalyst K", "precursor Pp"],
    "matter": [0],
    "threshold": 0.5,
    "smooth": 1.0,
    "periodic": True,
    "radial_channels": [0, 1, 2],
}

P = dict(eta1=4.0, eta2=5.0, delta=0.3, mean=-1.3, amp=0.3, dx=0.5, dt=0.02, S=4.0,
         chi=-3.0, DK=1.0, DP=1.0, a=1.0, dK=0.08, F=0.01, r=0.5, kap=0.0015, K0=0.01,
         csub=4, u_bg=-1.6, scale=1.0)
import json as _json, os as _os
P.update(_json.loads(_os.environ.get("WORLD_P", "{}")))


def Wp(u, d):
    return (u + 1) * ((u - 1) ** 2 / 2 - d) + 0.5 * (u + 1) ** 2 * (u - 1)


def Wpp(u, d):
    return ((u - 1) ** 2 / 2 - d) + 2 * (u + 1) * (u - 1) + 0.5 * (u + 1) ** 2


def bern(x):
    x = np.where(np.abs(x) < 1e-8, 1e-8, x)
    return x / np.expm1(x)


def c_div(c, u, D, chi, dx):
    out = np.zeros_like(c)
    for ax in (0, 1):
        cr, ur = np.roll(c, -1, ax), np.roll(u, -1, ax)
        a = chi * (ur - u)
        F = (D / dx) * (bern(a) * c - bern(-a) * cr)
        out -= (F - np.roll(F, 1, ax)) / dx
    return out


def lap(c, dx):
    return (np.roll(c, 1, 0) + np.roll(c, -1, 0) + np.roll(c, 1, 1) + np.roll(c, -1, 1) - 4 * c) / dx ** 2


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    dx = P["dx"] / P["scale"]
    u = P["mean"] + P["amp"] * rng.standard_normal((H, W))
    K = P["K0"] * rng.random((H, W))
    ky = 2 * np.pi * np.fft.fftfreq(H, d=dx)
    kx = 2 * np.pi * np.fft.fftfreq(W, d=dx)
    kk = ky[:, None] ** 2 + kx[None, :] ** 2
    return {"u": u, "K": K, "Pp": np.ones((H, W)), "kk": kk, "dx": dx}


def step(s):
    u, K, Pp, kk, d, dt, S = s["u"], s["K"], s["Pp"], s["kk"], P["delta"], P["dt"], P["S"]
    U = np.fft.fft2(u)
    lu = np.fft.ifft2(-kk * U).real
    wp = Wp(u, d)
    nl = np.fft.ifft2(kk * np.fft.fft2(wp)).real - Wpp(u, d) * (lu - wp) + P["eta1"] * lu - P["eta2"] * wp
    U = (U - dt * kk * np.fft.fft2(nl) + dt * S * kk ** 2 * U) / (1 + dt * (kk ** 3 + S * kk ** 2))
    prod = P["r"] * K * Pp
    h = dt / P["csub"]
    for _ in range(P["csub"]):
        auto = P["a"] * K * K * Pp
        K = K + h * (c_div(K, u, P["DK"], P["chi"], s["dx"]) + auto - P["dK"] * K)
        Pp = Pp + h * (P["DP"] * lap(Pp, s["dx"]) + P["F"] * (1 - Pp) - auto - P["r"] * K * Pp)
        K = np.maximum(K, 0); Pp = np.maximum(Pp, 0)
    s["u"] = np.fft.ifft2(U).real + dt * (prod - P["kap"] * np.maximum(u - P["u_bg"], 0))
    s["K"], s["Pp"] = K, Pp
    return s


def fields(s):
    return np.stack([s["u"] - P["u_bg"], s["K"], s["Pp"]]).astype(np.float32)


def damage(s, mask):
    """Erase: amphiphile reset to solvent, catalyst deleted, precursor untouched."""
    s["u"][mask] = P["u_bg"] + 0.1
    s["K"][mask] = 0
    return s
