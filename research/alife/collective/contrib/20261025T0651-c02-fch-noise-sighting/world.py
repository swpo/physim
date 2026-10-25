"""Functionalized Cahn-Hilliard (FCH) amphiphile world, from noise.

u is the amphiphile volume fraction (u=-1 solvent, u~+0.5 at a bilayer centre). Promislow-group FCH:
  u_t = Lap mu,  mu = (e^2 Lap - W''(u))(e^2 Lap u - W'(u)) + e^2 eta1 Lap u - eta2 W'(u),
  W(u) = (u+1)^2/2 * [(u-1)^2/2 + g/3 (u-2)],  eta1 = 1.45 e, eta2 = 3 e, e = 0.1, g = 0.3
(the parameters of the FCH benchmark of the Promislow group, NSF PAR 10618074; positive control: a
planted perturbed circle pearls then meanders at bath excess d=0.75, eta2=1.5e).
Semi-implicit spectral step: the linearisation about the solvent bath is implicit, the rest explicit.
Initial condition: u = -1 + OFF + AMP*uniform(-1,1) over the whole domain (unstructured).
"""
import numpy as np

EPS, G, ETA1, ETA2 = 0.1, 0.3, 1.45, 3.0
LBOX = 4 * np.pi
OFF, AMP = 0.1, 0.3
DT = 1e-2

META = {
    "name": "fch-noise",
    "family": "fch-bilayer",
    "parent": None,
    "mutation": "FCH (Promislow benchmark parameters) started from a noisy solvent bath with amphiphile excess",
    "size": (256, 256),
    "steps_per_frame": 100,
    "dt": DT,
    "channels": ["u+1 (amphiphile)"],
    "matter": [0],
    "threshold": 0.6,
    "smooth": 0.5,
}


def W1(u):
    B = (u - 1) ** 2 / 2 + G / 3 * (u - 2)
    return (u + 1) * B + (u + 1) ** 2 / 2 * ((u - 1) + G / 3)


def W2(u):
    B = (u - 1) ** 2 / 2 + G / 3 * (u - 2)
    return B + 2 * (u + 1) * ((u - 1) + G / 3) + (u + 1) ** 2 / 2


def init(seed, size):
    H, Wd = size
    rng = np.random.default_rng(seed)
    u = -1 + OFF + AMP * (2 * rng.random((H, Wd)) - 1)
    k = 2 * np.pi * np.fft.fftfreq(H, d=LBOX / H)
    k2 = k[:, None] ** 2 + k[None, :] ** 2
    a2 = W2(-1.0)
    Lmu = (EPS ** 2 * k2 + a2) ** 2 + 1.0
    return {"u": u, "k2": k2, "Lmu": Lmu, "den": 1 + DT * k2 * Lmu, "dt": DT}


def step(s):
    u, k2 = s["u"], s["k2"]
    e2, e1, e2t = EPS ** 2, ETA1 * EPS, ETA2 * EPS
    uh = np.fft.fft2(u)
    lu = np.real(np.fft.ifft2(-k2 * uh))
    w = e2 * lu - W1(u)
    lw = np.real(np.fft.ifft2(-k2 * np.fft.fft2(w)))
    mu = e2 * lw - W2(u) * w + e1 * e2 * lu - e2t * W1(u)
    s["u"] = np.real(np.fft.ifft2((uh - s["dt"] * k2 * (np.fft.fft2(mu) - s["Lmu"] * uh)) / s["den"]))
    return s


def fields(s):
    return (s["u"] + 1)[None]


def damage(s, mask):
    # remove amphiphile under the mask (reset to the bare solvent value), mass leaves the system
    s["u"][mask] = -1.0
    return s
