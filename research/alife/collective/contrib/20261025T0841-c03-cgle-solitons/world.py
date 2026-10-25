"""Cubic-quintic complex Ginzburg-Landau (dissipative solitons) from noise.

A (complex): A_t = delta A + (beta + i D/2) lap A + (eps + i)|A|^2 A + (mu + i nu)|A|^4 A
delta < 0: the zero state is linearly stable; eps > 0 cubic gain, mu < 0 quintic saturation,
beta spectral filtering (diffusion), D dispersion. Localized pulses (dissipative solitons) are
bistable with A = 0. Linear part exact in Fourier, nonlinear part Heun (integrating factor).
Initial condition: smoothed complex Gaussian noise over the whole domain (|A| ~ 0.6).
Rendered channels: |A| and Re A.
"""
import numpy as np
from scipy import ndimage

META = {
    "name": "cgle-solitons",
    "family": "cgle",
    "parent": None,
    "mutation": "new class: cubic-quintic complex Ginzburg-Landau (Akhmediev / Soto-Crespo dissipative solitons)",
    "size": (96, 96),
    "steps_per_frame": 200,
    "dt": 0.01,
    "channels": ["|A|", "Re A"],
    "matter": [0],
    "threshold": 0.5,
    "smooth": 1.0,
    "periodic": True,
}

P = dict(L=40.0, delta=-0.1, beta=0.125, D=1.0, eps=0.8, mu=-0.3, nu=-0.1, amp=0.6, smooth=2.0, dt=0.01)


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    z = rng.standard_normal((H, W)) + 1j * rng.standard_normal((H, W))
    z = ndimage.gaussian_filter(z.real, P["smooth"], mode="wrap") + 1j * ndimage.gaussian_filter(z.imag, P["smooth"], mode="wrap")
    A = P["amp"] * z / np.abs(z).std()
    ky = 2 * np.pi * np.fft.fftfreq(H, d=P["L"] / W)
    kx = 2 * np.pi * np.fft.fftfreq(W, d=P["L"] / W)
    kk = ky[:, None] ** 2 + kx[None, :] ** 2
    E = np.exp((P["delta"] - (P["beta"] + 0.5j * P["D"]) * kk) * P["dt"])
    return {"A": A, "E": E}


def NL(a):
    p = np.abs(a) ** 2
    return (P["eps"] + 1j) * p * a + (P["mu"] + 1j * P["nu"]) * p * p * a


def step(s):
    A, E, dt = s["A"], s["E"], P["dt"]
    Ah = np.fft.fft2(A)
    k1 = np.fft.fft2(NL(A))
    A1 = np.fft.ifft2(E * (Ah + dt * k1))
    k2 = np.fft.fft2(NL(A1))
    s["A"] = np.fft.ifft2(E * (Ah + 0.5 * dt * k1) + 0.5 * dt * k2)
    return s


def fields(s):
    return np.stack([np.abs(s["A"]), s["A"].real]).astype(np.float32)


def damage(s, mask):
    s["A"][mask] = 0
    return s
