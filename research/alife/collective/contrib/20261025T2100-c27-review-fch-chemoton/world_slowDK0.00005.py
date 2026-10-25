"""FCH field chemoton on the weakly functionalized (Promislow benchmark) FCH, from noise.

u amphiphile (FCH, eps=0.1, eta1=1.45 eps, eta2=3 eps, W = (u+1)^2/2 [(u-1)^2/2 + g/3 (u-2)], g=0.3),
P precursor (fed F(1-P), crosses bilayers freely), K catalyst (Gray-Scott-like K^2 P autocatalysis,
decay dK, transport div(DK g grad K) with g = exp(-beta (u+1)) and the MIN face mobility, so the bilayer
holds K). K turns P into amphiphile (r K P); amphiphile decays everywhere at kap and free monomers in the
bath (outside bilayers, indicator exp(-beta (u+1))) decay at an extra kb, so leaked product is not shared.
  du/dt = lap mu_FCH + r K P - (kap + kb exp(-beta (u+1))) (u + 1 - b)
  dP/dt = DP lap P + F (1 - P) - a K^2 P - r K P
  dK/dt = div(DK g grad K) + a K^2 P - dK K
Initial condition (unstructured over the whole domain): u = -1 + off + amp U(-1,1), P = 1/2,
K = K0 U(0,1) white noise.
"""
import numpy as np

G = 0.3
P = dict(eps=0.1, eta1=1.45, eta2=3.0, dt=0.01, S=1.0, off=0.1, amp=0.3,
         DP=0.05, DK=0.00005, beta=4.0, F=0.04, a=1.0, dK=0.1, r=0.04, kap=0.01, b=0.0, K0=1.0, gate=0, kb=0.0)
DX = 4 * np.pi / 256

META = {
    "name": "fch-pchemoton-slowDK0.00005",
    "family": "fch-bilayer",
    "parent": "collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py",
    "mutation": "add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay",
    "size": (192, 192),
    "steps_per_frame": 300,
    "dt": 0.01,
    "channels": ["amphiphile u+1", "precursor P", "catalyst K"],
    "matter": [0],
    "threshold": 0.6,
    "smooth": 0.5,
    "radial_channels": None,
}


def W1(u):
    B = (u - 1) ** 2 / 2 + G / 3 * (u - 2)
    return (u + 1) * B + (u + 1) ** 2 / 2 * ((u - 1) + G / 3)


def W2(u):
    B = (u - 1) ** 2 / 2 + G / 3 * (u - 2)
    return B + 2 * (u + 1) * ((u - 1) + G / 3) + (u + 1) ** 2 / 2


def gdiv(c, g):
    out = np.zeros_like(c)
    for ax in (0, 1):
        for sh in (1, -1):
            out += np.minimum(g, np.roll(g, -sh, ax)) * (np.roll(c, -sh, ax) - c)
    return out / DX ** 2


def lap(c):
    return (np.roll(c, 1, 0) + np.roll(c, -1, 0) + np.roll(c, 1, 1) + np.roll(c, -1, 1) - 4 * c) / DX ** 2


def init(seed, size):
    H, Wd = size
    rng = np.random.default_rng(seed)
    u = -1 + P["off"] + P["amp"] * (2 * rng.random((H, Wd)) - 1)
    K = P["K0"] * rng.random((H, Wd))
    k = 2 * np.pi * np.fft.fftfreq(H, d=DX)
    k2 = k[:, None] ** 2 + k[None, :] ** 2
    Lmu = (P["eps"] ** 2 * k2 + W2(-1.0)) ** 2 + P["S"]
    return {"u": u, "P": np.full((H, Wd), 0.5), "K": K, "k2": k2, "Lmu": Lmu, "den": 1 + P["dt"] * k2 * Lmu}


def step(s):
    u, Pc, K, k2 = s["u"], s["P"], s["K"], s["k2"]
    dt, e2 = P["dt"], P["eps"] ** 2
    uh = np.fft.fft2(u)
    lu = np.real(np.fft.ifft2(-k2 * uh))
    w = e2 * lu - W1(u)
    lw = np.real(np.fft.ifft2(-k2 * np.fft.fft2(w)))
    mu = e2 * lw - W2(u) * w + P["eta1"] * P["eps"] * e2 * lu - P["eta2"] * P["eps"] * W1(u)
    unew = np.real(np.fft.ifft2((uh - dt * k2 * (np.fft.fft2(mu) - s["Lmu"] * uh)) / s["den"]))
    g = np.exp(-P["beta"] * np.clip(u + 1, 0, None)) if P["gate"] else np.ones_like(u)
    auto = P["a"] * K * K * Pc
    prod = P["r"] * K * Pc
    s["P"] = Pc + dt * (P["DP"] * lap(Pc) + P["F"] * (1 - Pc) - auto - prod)
    s["K"] = K + dt * (P["DK"] * gdiv(K, g) + auto - P["dK"] * K)
    gb = np.exp(-P["beta"] * np.clip(u + 1, 0, None))  # bath indicator: free monomers decay faster
    s["u"] = unew + dt * (prod - (P["kap"] + P["kb"] * gb) * (u + 1 - P["b"]))
    return s


def fields(s):
    return np.stack([s["u"] + 1, s["P"], s["K"]]).astype(np.float32)


def damage(s, mask):
    """Erased matter is deleted: amphiphile reset to bare solvent, catalyst removed, precursor untouched."""
    s["u"][mask] = -1.0
    s["K"][mask] = 0.0
    return s
